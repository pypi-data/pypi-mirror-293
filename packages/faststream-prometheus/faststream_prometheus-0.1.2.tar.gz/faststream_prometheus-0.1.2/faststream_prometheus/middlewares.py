from __future__ import annotations

import logging
from typing import Any, Optional

from faststream import BaseMiddleware
from faststream.broker.message import StreamMessage
from faststream.kafka.message import KafkaMessage
from faststream.nats.message import NatsMessage
from faststream.rabbit.message import RabbitMessage
from faststream.redis.message import RedisMessage
from prometheus_client import CollectorRegistry

from faststream_prometheus.collectors import SafeFaststreamCollector

logger = logging.getLogger('faststream_prometheus')


class FaststreamPrometheusMiddleware(BaseMiddleware):
    msg: Optional[Any] = None

    def __init__(self, registry: Optional[CollectorRegistry] = None, prefix: str = 'faststream'):
        self.faststream_collector_group = SafeFaststreamCollector.get_collector(registry, prefix)

    async def on_receive(self) -> None:
        self.faststream_collector_group.on_receive()
        return await super().on_receive()

    async def on_consume(self, msg: StreamMessage[Any]) -> StreamMessage[Any]:
        if isinstance(msg, KafkaMessage):
            self.faststream_collector_group.receive_kafka_message(msg)

        elif isinstance(msg, RedisMessage):
            self.faststream_collector_group.receive_redis_message(msg)

        elif isinstance(msg, RabbitMessage):
            self.faststream_collector_group.receive_rabbit_message(msg)

        elif isinstance(msg, NatsMessage):
            self.faststream_collector_group.receive_nats_message(msg)

        logger.warning(f'Unexpected message type: {type(logger)}')

        return await super().on_consume(msg)

    async def on_publish(self, msg: Any, *args: Any, **kwargs: Any) -> Any:
        self.faststream_collector_group.on_publish()

        return await super().on_publish(msg, *args, **kwargs)

    async def after_publish(self, err: Optional[Exception]) -> None:
        self.faststream_collector_group.after_publish(err)

        return await super().after_publish(err)

    def __call__(self, msg: Optional[Any]) -> FaststreamPrometheusMiddleware:
        self.msg = msg
        return self
