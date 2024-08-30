import json
import os
from functools import partial
from typing import Dict, Callable, Literal, Annotated
from typing import List, Union
from typing import Optional

import zenoh
from datetime import datetime
from google.protobuf.message import Message
from pydantic import BaseModel, Field

_SESSION: Optional[zenoh.Session] = None


class PUB(BaseModel):
    socket_type: Literal["PUB"]
    topic_name: str


class SUB(BaseModel):
    socket_type: Literal["SUB"]
    topic_name: str


Socket = Annotated[Union[PUB, SUB], Field(discriminator="socket_type")]


class Sockets(BaseModel):
    sockets: List[Socket]


class Topic:
    def __init__(self, name: str):
        self.name = name


class PublisherTopic(Topic):
    def __init__(self, name: str, session: zenoh.Session):
        super().__init__(name)
        # check if session is set otherwise initialize it
        self.name = name
        self._session = session
        self._pub = session.declare_publisher(f"{name}")

    def publish(self, message: Message) -> None:
        if not message.HasField("timestamp"):
            message.timestamp.FromDatetime(datetime.now())
        self._pub.put(message.SerializeToString())


class SubscriberTopic(Topic):
    def __init__(self, name: str, session: zenoh.Session):
        super().__init__(name)
        self._subscribers = []
        self.name = name
        self._session = session

    @staticmethod
    def retrieve_payload(*args, callback: Callable, **kwargs):
        sample = args[0]
        callback(sample.payload)

    def subscribe(self, callback: Callable) -> None:
        retrieve_callback = partial(SubscriberTopic.retrieve_payload, callback=callback)
        sub = self._session.declare_subscriber(f"{self.name}", retrieve_callback)
        self._subscribers.append(sub)


_TOPICS: Dict[str, Union[PublisherTopic, SubscriberTopic]] = {}


def get_topic(name: str) -> Union[PublisherTopic, SubscriberTopic]:
    global _SESSION
    if _SESSION is None:
        initialize()
    global _TOPICS
    if name not in _TOPICS:
        raise ValueError(f"Topic {name} not found. Available topics: {list(_TOPICS.keys())}")

    return _TOPICS[name]


def initialize() -> None:
    try:
        socket_data_env = os.environ["SOCKETS"]
        socket_data = Sockets.model_validate_json(socket_data_env)
    except KeyError:
        raise ValueError("`SOCKETS` environment variable not set")
    except json.JSONDecodeError:
        raise ValueError("`SOCKETS` environment variable is not a valid JSON")

    config = None
    if "COMM_CONFIG" in os.environ:
        config = json.loads(os.environ["COMM_CONFIG"])
        config = zenoh.Config.from_obj(config)
    session = zenoh.open(config=config)
    global _TOPICS
    for socket in socket_data.sockets:
        if isinstance(socket, PUB):
            _TOPICS[socket.topic_name] = PublisherTopic(name=socket.topic_name, session=session)
        elif isinstance(socket, SUB):
            _TOPICS[socket.topic_name] = SubscriberTopic(name=socket.topic_name, session=session)
        else:
            raise ValueError(f"Invalid socket type {socket.socket_type}")

    global _SESSION
    _SESSION = session


def cleanup() -> None:
    global _SESSION
    if _SESSION is not None:
        _SESSION.close()
        _SESSION = None
        global _TOPICS
        _TOPICS = {}
