from typing import Iterable, Optional

from prometheus_client import REGISTRY, CollectorRegistry
from prometheus_client.metrics_core import Metric
from prometheus_client.registry import Collector


class FaststreamCollectorGroup(Collector):
    registry: CollectorRegistry
    prefix: str

    def __init__(self, registry: Optional[CollectorRegistry] = None, prefix: str = 'faststream') -> None:
        if not isinstance(registry, CollectorRegistry):
            registry = REGISTRY

        self.registry = registry
        self.prefix = prefix

    def collect(self) -> Iterable[Metric]:
        yield

        return
