import simpy
import random

# Constants
NUM_PROCESS = 25
CPU_SIZE = 1
RAM_SIZE = 100
GAS_STATION_WAIT_MEAN = 5


# Function to simulate process solving
def process(env, proc_id, laps, CPU, RAM, RAM_SIZE):
    print(f'{env.now}:{proc_id} llega a la cola del waiting room. Procesos en espera {len(CPU.queue)}')
    while (laps > 0):
        with CPU.request() as req:
            yield req
            print(f'{env.now}: {proc_id} Está listo para entrar a proceso.')
            if laps == 0:
                break
            elif laps < 3:
                laps_cant = laps
            else:
                laps_cant = 3
            
            for lap in range(1, laps_cant + 1):
                print(f'{env.now}: {proc_id} instrucciones restantes: {laps}')
                laps -= 1
                yield env.timeout(1)  # Time to complete Proces
            
        option = random.randint(1, 2)
        if option == 1:
            yield env.timeout(1) 
        else:
            continue

        

##            if lap % 3 == 0:  # Time for gas after every 3 laps
        RAM.put(RAM_SIZE)
        print(f' {proc_id} exits the cpu at {env.now}')


# Function to generate instructions with ram capacity
def generate_process(env, CPU, RAM):
    RAM_usage = random.randint(1, 10)
    with RAM.get(RAM_usage) as req:
        yield req
        for i in range(NUM_PROCESS):
            laps = random.randint(1, 10)
            proc_id = f'Proc-{i+1}'
            env.process(process(env, proc_id, laps, CPU, RAM, RAM_SIZE))
            yield env.timeout(2)  # Time between car arrivals


# Setup and start the simulation
env = simpy.Environment()
RAM = simpy.Container(env, init=RAM_SIZE, capacity=RAM_SIZE)
CPU = simpy.Resource(env, capacity=CPU_SIZE)
env.process(generate_process(env, CPU, RAM))
env.run()
