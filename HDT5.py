import simpy
import random
import time


# Constants
CSV_FILE = 'Process_time_Start.csv'
NUM_PROCESS = 25
Inter_process = 3
CPU_SIZE = 1
RAM_SIZE = 100
Num_CPU = 1
Interval = 10

random.seed(10)
Process_time = {}


# Function to simulate process solving
def process(env, proc_id, instructions, CPU, RAM, RAM_usage,Start):
    
    print(f'{env.now}: {proc_id} llega a la cola del waiting room. Procesos en espera {len(CPU.queue)}')
    while (instructions > 0):
        with CPU.request() as req:
            yield req
            print(f'{env.now}: {proc_id} Está listo para entrar a proceso.')
            if instructions == 0:
                break
            elif instructions < Inter_process:
                instructions_cant = instructions
            else:
                instructions_cant = Inter_process
            
            for lap in range(1, instructions_cant + 1):
                print(f'{env.now}: {proc_id} instrucciones restantes: {instructions}')
                instructions -= 1
                yield env.timeout(1)  # Time to complete Proces
            
        option = random.randint(1, 2)
        if option == 1:
            yield env.timeout(1) 
        else:
            continue

        

# End of the process
    
    RAM.put(RAM_usage)
    print(f'{env.now}: {proc_id} exits the cpu at {env.now}')
    End = time.perf_counter()
    timet = f"{End - Start:0.4f}"
    Process_time[proc_id] = timet
    


# Function to generate instructions with ram capacity
def generate_process(env, CPU, RAM):
    intval = round(random.expovariate(1.0 / Interval))
    
    RAM_usage = random.randint(1, 10)
    for i in range(NUM_PROCESS):
        yield env.timeout(intval)
        Start = time.perf_counter()
        print(f'{env.now}: Proc-{i+1} espera a suficiente memoria RAM: {RAM.level}/{RAM_SIZE}')
        with RAM.get(RAM_usage) as reqRAM:
            yield reqRAM
            print(f'{env.now}: Proc-{i+1} tiene suficiente memoria RAM')
            instructions = random.randint(1, 10)
            proc_id = f'Proc-{i+1}'
            
            env.process(process(env, proc_id, instructions, CPU, RAM, RAM_usage,Start))



# Setup and start the simulation
env = simpy.Environment()
RAM = simpy.Container(env, init=RAM_SIZE, capacity=RAM_SIZE)
CPU = simpy.Resource(env, capacity=CPU_SIZE)
env.process(generate_process(env, CPU, RAM))
env.run()

with open(CSV_FILE, 'w') as file:
    file.write('Process, Time\n')
    for key, value in Process_time.items():
        file.write(f'{key}, {value}\n')