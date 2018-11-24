import random
from lotnisko.conf import CONFIG

class QueueStrategy(object):

    @classmethod
    def annoyed_passenger(self, passenger, avg_waiting_time):
        """
        Service time modelled after annoyed passenger.
        He starts his obnoxious behavior after waiting 3x the average waiting time.
        Security does nothing most of the time, sometimes the person starts a quarrel blocking the rest of queue.
        """
        if passenger.get_total_waiting_time() > 3*avg_waiting_time:
            if random.random() > CONFIG["annoyed_passenger_luck"]:
                print("Annoyed passenger encountered - what a douchebag!")
                return avg_waiting_time*CONFIG["annoyed_passenger_penalty_factor"]
        return 0

    @classmethod
    def racial_profiling(self, passenger, avg_waiting_time):
        """
        Service time modelled after racial profiling.
        If a high risk passenger enters the gate chance is he will get an extra check
        """
        if passenger.risk_level/CONFIG["racial_profiling_coefficient"] > random.random():
            print("This guy over here is sus - let's inspect him!")
            return avg_waiting_time*10
        return 0

    @classmethod
    def exponential_wait(self, passenger, avg_waiting_time, inefficiency=0):
        """
        Service time modelled after exponential distribution.
        Computes desired service time(beta) based on abstract employee inefficiency metric,
        then draws samples using expovariate with parameter lambda = 1/beta
        """
        mean_service_time = avg_waiting_time + 3*inefficiency ** 2
        return random.expovariate(1.0/mean_service_time)
