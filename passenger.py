import pandas as pd
import random
import numpy as np
from lotnisko.conf import CONFIG


class PassengerRegistry(object):
    def __init__(self, env):
        self.passengers = []
        self.env = env
        self.waitsum = 0.0

    def create_passenger(self, number):
        passenger = Passenger(number, self.env, self)
        self.passengers.append(passenger)
        return passenger

    def summarize(self):
        df = pd.DataFrame(
            list(map(lambda x: x.get_total_waiting_time(), self.passengers)))
        return(df.describe())

    def register_wait(self, wait):
        self.waitsum += wait

    def get_mean_wait_time(self):
        no_passengers = len(self.passengers)
        if no_passengers == 1:
            return CONFIG['avg_waiting_time']
        return self.waitsum/len(self.passengers)


class Passenger(object):
    def __init__(self, number, env, registry):
        self.waits = []
        self._number = number
        self.env = env
        self.registry = registry
        self._risk_level = np.minimum(np.random.poisson(
            CONFIG["passenger_risk_poisson_lambda"], 1), 10)

    def __enter__(self):
        self.start = self.env.now
        return self

    def __exit__(self, *args):
        self.waits.append(self.env.now - self.start)
        self.registry.register_wait(self.waits[-1])

    def __repr__(self):
        return str(self._number)

    def last_wait(self):
        try:
            return self.waits[-1]
        except IndexError:
            return 0

    def select_queue(self, queues):
        return random.choice(queues)

    def get_total_waiting_time(self):
        return sum(self.waits)

    @property
    def risk_level(self):
        return self._risk_level
