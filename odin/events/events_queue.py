from queue import PriorityQueue
from ..utilities import params


class EventsQueue(PriorityQueue):
    """Events Queue Class

    The events queue handles the order in which events are processed by Odin.
    Events are first processed according to their intrinsic priority and then
    according to the order in which the events were placed into the queue. This
    second means of prioritization is used to enforce the idea that, for
    example, signal events placed into the queue before other signal events are
    inherently more desirable than signal events placed into the queue later.
    """
    def __init__(self):
        """Initialize parameters of the events queue."""
        super(EventsQueue, self).__init__()
        self.count = 0

    def put(self, event):
        """Place an event into the events queue. An item is placed into the
        priority queue using the current count of value. This allows the order
        of events to be preserved within the priority queue without sacrificing
        the priority inherent to event types.

        Parameters
        ----------
        event: An event object.
            The event object to be placed into the events queue. This can be one
            of a market, signal, order, fill, manage, or rebalance event.
        """
        # Extract the priority for the event. We also differentiate between buy
        # and sell event types in the case of a signal event.
        p = params.priority_dict[event.event_type]
        if event.event_type == params.Events.signal:
            p = p[event.trade_type]

        super(EventsQueue, self).put((p, self.count, event))
        self.count += 1

    def get(self, *args, **kwargs):
        """Retrieve an object from the events queue. An object is retrieved from
        the events queue and the count of objects of that type in the events
        queue is decremented.
        """
        priority, count, event = super(EventsQueue, self).get(*args, **kwargs)
        return event

    def clear(self):
        """Remove all events from the events queue."""
        while not self.empty():
            self.get(False)

