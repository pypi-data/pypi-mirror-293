from buz.event import Event
from buz.event.infrastructure.buz_kafka.publish_strategy.publish_strategy import KafkaPublishStrategy


class TopicPerEventWithPrefixKafkaPublishStrategy(KafkaPublishStrategy):
    def __init__(self, prefix: str):
        self._prefix = prefix

    def get_topic(self, event: Event) -> str:
        return f"{self._prefix}.{event.fqn()}"
