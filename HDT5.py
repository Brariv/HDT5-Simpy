import simpy
import random
import time



# Constants
CSV_FILE = 'Process_time.csv'

Inter_process = 3
CPU_SIZE = 2
RAM_SIZE = 100
Interval = 10
NUM_PROCESS = 25

TimeAv = []
random.seed(10)
Process_time = []

def save_to_csv(data, filename):
    print(f'Average time: {sum(TimeAv) / len(TimeAv)}')
    print(f'Standar Deviation: {round((sum((x - (sum(TimeAv) / len(TimeAv))) ** 2 for x in TimeAv) / len(TimeAv)) ** 0.5, 4)}')
    Process_time.append(NUM_PROCESS)
    Process_time.append(sum(TimeAv) / len(TimeAv))
    Process_time.append(round((sum((x - (sum(TimeAv) / len(TimeAv))) ** 2 for x in TimeAv) / len(TimeAv)) ** 0.5, 4))

    # Append the average time and Standar Deviation of the process to the CSV file
    with open(CSV_FILE, 'a') as file:
        file.write(f'{Process_time[0]},{Process_time[1]},{Process_time[2]}\n')
        file.close()

# Function to simulate process solving
def process(env, proc_id, instructions, CPU, RAM, RAM_usage,Start,NUM_PROCESS):
    
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
    TimeAv.append(float(timet))
    


# Function to generate instructions with ram capacity
def generate_process(env, CPU, RAM, NUM_PROCESS):
    Start = time.perf_counter()
    intval = round(random.expovariate(1.0 / Interval))
    RAM_usage = random.randint(1, 10)
    for i in range(NUM_PROCESS):
        yield env.timeout(intval)
        print(f'{env.now}: Proc-{i+1} espera a suficiente memoria RAM: {RAM.level}/{RAM_SIZE}')
        with RAM.get(RAM_usage) as reqRAM:
            yield reqRAM
            print(f'{env.now}: Proc-{i+1} tiene suficiente memoria RAM')
            instructions = random.randint(1, 10)
            proc_id = f'Proc-{i+1}'
            
            env.process(process(env, proc_id, instructions, CPU, RAM, RAM_usage,Start,NUM_PROCESS))



# Setup and start the simulation
env = simpy.Environment()
RAM = simpy.Container(env, init=RAM_SIZE, capacity=RAM_SIZE)
CPU = simpy.Resource(env, capacity=CPU_SIZE)
env.process(generate_process(env, CPU, RAM, NUM_PROCESS))
env.run()
save_to_csv(TimeAv, CSV_FILE)


