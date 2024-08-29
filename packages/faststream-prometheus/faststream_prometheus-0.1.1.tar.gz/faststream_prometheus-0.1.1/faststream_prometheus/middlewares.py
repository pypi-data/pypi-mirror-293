from typing import Any, Optional

from faststream import BaseMiddleware
from faststream.broker.message import StreamMessage
from prometheus_client import CollectorRegistry

from faststream_prometheus.collectors import FaststreamCollectorGroup


class FaststreamPrometheusMiddleware(BaseMiddleware):
    def __init__(self, msg: Any | None = None) -> None:
        super().__init__(msg)

    async def on_receive(self) -> None:
        return await super().on_receive()

    async def on_publish(self, msg: Any, *args: Any, **kwargs: Any) -> Any:
        return await super().on_publish(msg, *args, **kwargs)

    async def on_consume(self, msg: StreamMessage[Any]) -> StreamMessage[Any]:
        return await super().on_consume(msg)


class FaststreamPrometheusMiddlewareFactory(object):
    def __init__(self, registry: Optional[CollectorRegistry] = None, prefix: str = 'faststream'):
        self.faststream_collector_group = FaststreamCollectorGroup(registry, prefix)

    def __call__(self, msg: Optional[Any] = None) -> Any:
        return FaststreamPrometheusMiddleware(self.faststream_collector_group, msg)
