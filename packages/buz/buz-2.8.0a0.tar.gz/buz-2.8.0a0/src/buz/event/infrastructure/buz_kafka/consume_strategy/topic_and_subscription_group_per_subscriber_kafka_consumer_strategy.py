from typing import List
from buz.event.infrastructure.buz_kafka.consume_strategy.consume_strategy import KafkaConsumeStrategy
from buz.event.subscriber import Subscriber


class TopicAndSubscriptionGroupPerSubscriberKafkaConsumerStrategy(KafkaConsumeStrategy):
    def get_topics(self, subscriber: Subscriber) -> List[str]:
        event_class = subscriber.handles()
        return [event_class.fqn()]

    def get_subscription_group(self, subscriber: Subscriber) -> str:
        return subscriber.fqn()
