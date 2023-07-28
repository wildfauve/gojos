from gojos.util import event_queue


class Publisher(event_queue.EventQueue):

    def publish_event1_create(self, msg: dict):
        self.__class__.publish(event_queue.Envelope('event1.create', msg))


class Subscriber(event_queue.EventQueue):

    def __init__(self):
        self.events = []
    def event1_create_subscription(self):
        self.__class__.subscribe('event1.create', self.add_event)
        return self

    def add_event(self, event):
        self.events.append(event)
        return self


def test_subscribe_observer():
    sub = Subscriber().event1_create_subscription()

    pub = Publisher()
    pub.publish_event1_create({'msg': 'hello'})

    assert len(sub.events) == 1
    assert sub.events[0].eventType == 'event1.create'
    assert sub.events[0].payload == {'msg': 'hello'}


