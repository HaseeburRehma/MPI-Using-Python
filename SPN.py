from mpi4py import MPI

def calculate_average_waiting_time(jobs):
    total_waiting_time = 0
    for job in jobs:
        total_waiting_time += job['waiting_time']
    return total_waiting_time / len(jobs)

def calculate_average_turnaround_time(jobs):
    total_turnaround_time = 0
    for job in jobs:
        total_turnaround_time += job['turnaround_time']
    return total_turnaround_time / len(jobs)

def calculate_average_response_time(jobs):
    total_response_time = 0
    for job in jobs:
        total_response_time += job['response_time']
    return total_response_time / len(jobs)

def spn_scheduler(jobs):
    num_cpus = MPI.COMM_WORLD.Get_size()
    rank = MPI.COMM_WORLD.Get_rank()
    jobs_per_cpu = len(jobs) // num_cpus
    remainder = len(jobs) % num_cpus

    if rank < remainder:
        jobs_count = jobs_per_cpu + 1
        start_index = rank * jobs_count
        end_index = start_index + jobs_count
    else:
        jobs_count = jobs_per_cpu
        start_index = rank * jobs_count + remainder
        end_index = start_index + jobs_count

    my_jobs = jobs[start_index:end_index]
    my_jobs.sort(key=lambda x: x['burst_time'])  # Sort jobs based on burst time (shortest first)

    waiting_time = 0
    turnaround_time = 0
    response_time = 0
    current_time = 0

    for job in my_jobs:
        if current_time < job['arrival_time']:
            current_time = job['arrival_time']
        job['waiting_time'] = current_time - job['arrival_time']
        waiting_time += job['waiting_time']
        job['turnaround_time'] = job['waiting_time'] + job['burst_time']
        turnaround_time += job['turnaround_time']
        job['response_time'] = job['waiting_time']
        response_time += job['response_time']
        current_time += job['burst_time']

    return waiting_time, turnaround_time, response_time

if __name__ == '__main__':
    # Example list of jobs
    jobs = [{'arrival_time': 0, 'burst_time': 5},
            {'arrival_time': 1, 'burst_time': 3},
            {'arrival_time': 2, 'burst_time': 8},
            {'arrival_time': 3, 'burst_time': 6},
            {'arrival_time': 4, 'burst_time': 4},
            {'arrival_time': 5, 'burst_time': 2}]

    # Initialize MPI
    MPI.COMM_WORLD.Init()
    num_cpus = MPI.COMM_WORLD.Get_size()
    rank = MPI.COMM_WORLD.Get_rank()

    if rank == 0:
        # Master process
        average_waiting_time = 0
        average_turnaround_time = 0
        average_response_time = 0

        # Distribute jobs to worker processes
        for i in range(num_cpus):
            MPI.COMM_WORLD.send(jobs, dest=i)

        # Collect results from worker processes
        for i in range(num_cpus):
            waiting_time, turnaround_time, response_time = MPI.COMM_WORLD.recv(source=i)
            average_waiting_time += waiting_time
            average_turnaround_time += turnaround_time
            average_response_time
