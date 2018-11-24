import abc
import random
from lotnisko.strategy import QueueStrategy

class QueueABC(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def check(self):
        pass


class EntryQueue(QueueABC):
    def __init__(self, env, registry, sec_queues, num_guests=10, avg_waiting_time=120, verbose=True):
        self.avg_waiting_time = avg_waiting_time
        self.num_guests = num_guests
        self.sec_queues = sec_queues
        self.env = env
        self.registry = registry
        self.verbose = verbose

    def check(self):
        for guest in range(self.num_guests):
            passenger = self.registry.create_passenger(guest)
            with passenger:
                yield self.env.timeout(QueueStrategy.exponential_wait(passenger, self.avg_waiting_time()))
            target_queue = passenger.select_queue(self.sec_queues)

            if self.verbose:
                print("Dispatched passenger {0} to queue {1}, waiting time: {2}".format(
                    passenger, target_queue, passenger.last_wait()))

            yield self.env.process(target_queue.check(passenger))


class SecurityQueue(QueueABC):
    def __init__(self, env, name, inefficiency, avg_waiting_time, verbose=True):
        self.env = env
        self.avg_waiting_time = avg_waiting_time
        self.inefficiency = inefficiency
        self.name = name
        self.verbose = verbose

    def __repr__(self):
        return self.name

    def check(self, passenger):
        with passenger:
            yield self.env.timeout(QueueStrategy.exponential_wait(passenger,
                                                                  avg_waiting_time=self.avg_waiting_time(),
                                                                  inefficiency=self.inefficiency))
            yield self.env.timeout(QueueStrategy.annoyed_passenger(passenger,
                                                                   self.avg_waiting_time()))
            profiling = QueueStrategy.racial_profiling(
                passenger, self.avg_waiting_time())

            if profiling > 0:
                yield self.env.timeout(profiling)
                # TODO implement a queue: self.env.process(rectal_search_queue)

        if self.verbose:
            print("Queue {0} Cleared passenger {1} from security. waiting time {2}".format(
                self.name, passenger, passenger.last_wait()))
