import random
import simpy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from lotnisko.helpers import name_generator
from lotnisko.passenger import PassengerRegistry
from lotnisko.queue import EntryQueue, SecurityQueue

random.seed(41)

#%%

def constant_avg_waiting_time():
    return 60

def one_inefficient_queue_with_dynamic_avg_time_updates(num_queues, inefficiency_factor):

    airport = simpy.Environment()
    registry = PassengerRegistry(airport)
    security_queues = [SecurityQueue(airport,
                                     name_generator.get_name(),
                                     avg_waiting_time=registry.get_mean_wait_time,
                                     inefficiency=0) for queue in range(0, num_queues-1)]
    security_queues.append(
        SecurityQueue(airport,
                      name_generator.get_name(),
                      avg_waiting_time=registry.get_mean_wait_time,
                      inefficiency=inefficiency_factor)
    )
    entry_queue = EntryQueue(airport,
                             registry=registry,
                             sec_queues=security_queues,
                             num_guests=2305,
                             avg_waiting_time=registry.get_mean_wait_time)
    airport.process(entry_queue.check())
    airport.run()
    return entry_queue.registry.summarize()

#%%
one_inefficient_queue_with_dynamic_avg_time_updates(10,10)

#%%
results10 = pd.DataFrame([one_inefficient_queue_with_dynamic_avg_time_updates(j, 10)[0] for j in range(1,31) for i in range(1000)])
results10_sum = pd.DataFrame([round((results10[(k-1)*1000:k*1000].apply(np.mean)/60000),2) for k in range(1,31,1)])

x = np.arange(1,31)
mean = results10_sum.iloc[:,1]
q2 = results10_sum.iloc[:,5]

plt.figure(figsize=(8,5))
plt.plot(x, mean, 'r', label = "E(τ)")
plt.plot(x, q2, 'g', label = "Q2(τ)")
plt.legend()
plt.grid()
plt.xlabel("liczba kolejek")
plt.ylabel("przeciętny czas obsługi pasażera")
plt.savefig("port1.png",bbox_inches = "tight")

#%%
eps_par = pd.DataFrame([one_inefficient_queue_with_dynamic_avg_time_updates(20, e)[0] for e in range(0,51,5) for i in range(1000)])
eps_par_sum = pd.DataFrame([round((eps_par[(k-1)*1000:k*1000].apply(np.mean)/60000),2) for k in range(1,12)])

x2 = np.arange(0,51,5)
mean_2 = eps_par_sum.iloc[:,1]
q2_2 = eps_par_sum.iloc[:,5]

plt.figure(figsize=(8,5))
plt.plot(x2, mean_2, 'b', label = "E(τ)")
plt.plot(x2, q2_2, 'y', label = "Q2(τ)")
plt.legend()
plt.grid()
plt.xlabel("nieefektywność kolejek")
plt.ylabel("przeciętny czas obsługi pasażera")
plt.savefig("port2.png",bbox_inches = "tight")