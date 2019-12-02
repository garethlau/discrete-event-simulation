import simpy
import random
import itertools
import numpy as np
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class Distribution():
    def __init__(self, distribution):
        self.distribution = distribution
        self.intervals = np.diff(distribution)

    def next(self, curr):
        for i in self.distribution:
            if (curr < i):
                return i

    def get_interval(self):
        return np.delete(self.intervals, 0)[0]



def run_sim(socketio):

    ### Simulation Functions
    def revenue(time):
        if (time > 16 * 60 and time < 21 * 60):
            return random.randint(20, 45)
        else:
            return random.randint(5, 15)

    def customer(name, env, booth, visit_duration, patience):
        arrive_time = env.now
        with booth.request() as req:
            results = yield req | env.timeout(patience)
            if req in results:
                seated_time = env.now
                yield env.timeout(visit_duration)
                data['served'] += 1
                data['revenue'] += revenue(env.now)
                print("{} waited for {} minutes and stayed for {} minutes ".format(name, seated_time - arrive_time, visit_duration))
            else:
                data['left'] += 1
                print("{} waited {} left".format(name, patience))

    def customer_generator(env, num, booth, visit_duration, patience, interval, data):
        for i in range(num):
            v = random.randint(*visit_duration)
            p = random.uniform(*patience)
            size = random.uniform(1, 4)
            c = customer_group(i, size, env, booth, v, p)
            env.process(c)
            # t = random.expovariate(1.0 / interval)
            t = distribution.get_interval()
            yield env.timeout(t)
            

    def customer_group(name, size, env, booth, visit_duration, patience):
        arrive_time = env.now
        with booth.request() as req:
            results = yield req | env.timeout(patience)
            if req in results:
                seated_time = env.now
                yield env.timeout(visit_duration)
                data['served'] += size
                data['revenue'] += revenue(env.now) * size
                
                log = {
                    "name": name,
                    "seated_time": seated_time,
                    "arrive_time": arrive_time,
                    "visit_duration": visit_duration,
                    "patience": patience
                }
                socketio.emit('sim-update', log)  
                print("{} waited for {} minutes and stayed for {} minutes ".format(name, seated_time - arrive_time, visit_duration))
            else:
                data['left'] += 1
                log = {
                    "name": name,
                    "seated_time": 0,
                    "arrive_time": arrive_time,
                    "visit_duration": 0,
                    "patience": patience
                }
                socketio.emit('sim-update', log)
                print("{} waited {} left".format(name, patience))


    print("IN RUN SIMULATION")
    # Params
    NUM_BOOTHS = 6
    VISIT_DURATION = [20, 40]
    INTERVAL = 10.0
    SIM_TIME = 24 * 60
    PATIENCE= [5, 10]
    NUM_CUSTOMERS = 100

    N_MEAN = 19 * 60
    N_STD = 200

    U_LOW = 11 * 60
    U_HIGH = 24 * 60

    data = {
        "total": 0,
        "served": 0,
        "revenue": 0,
        "left": 0,
    }

    env = simpy.Environment()
    booth = simpy.Resource(env, capacity=NUM_BOOTHS)

    # Create arrival time frequency distribution
    np.random.seed(42)
    n = np.random.normal(size=50, loc=N_MEAN, scale=N_STD)
    u = np.random.uniform(size=50, low=U_LOW, high=U_HIGH)
    # Combine normal and uniform distribution
    c = np.concatenate((u, n), axis=0)
    c = np.sort(c)
    distribution = Distribution(c)  

    # Run simulation
    env.process(customer_generator(env, NUM_CUSTOMERS, booth, VISIT_DURATION, PATIENCE, INTERVAL, data))
    env.run(until=SIM_TIME)
    data['total'] = NUM_CUSTOMERS
    print(data)  
    return data