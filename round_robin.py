from collections import deque

# Job data: (Job ID, Arrival Time, CPU Burst)
jobs = [
    ('A', 0, 16),
    ('B', 2, 2),
    ('C', 4, 6),
    ('D', 6, 4),
    ('E', 8, 10),
    ('F', 10, 6),
    ('G', 12, 8),
    ('H', 14, 12),
    ('I', 16, 4),
    ('J', 19, 6)
]

time_quantum = 4

# Initialize job info
job_info = {job[0]: {'arrival': job[1], 'burst': job[2], 'remaining': job[2], 'completion': 0, 'waiting': 0} for job in jobs}
ready_queue = deque()
time = 0
completed = 0
n = len(jobs)

# Sort jobs by arrival time
jobs.sort(key=lambda x: x[1])
job_index = 0

# Simulation loop
while completed < n:
    # Add jobs that have arrived to the ready queue
    while job_index < n and jobs[job_index][1] <= time:
        ready_queue.append(jobs[job_index][0])
        job_index += 1

    if ready_queue:
        current_job = ready_queue.popleft()
        job = job_info[current_job]

        exec_time = min(time_quantum, job['remaining'])
        time += exec_time
        job['remaining'] -= exec_time

        # Add newly arrived jobs during execution
        while job_index < n and jobs[job_index][1] <= time:
            ready_queue.append(jobs[job_index][0])
            job_index += 1

        if job['remaining'] == 0:
            job['completion'] = time
            completed += 1
        else:
            ready_queue.append(current_job)
    else:
        # If no job is ready, jump to next arrival
        time = jobs[job_index][1]

# Calculate waiting and turnaround times
total_waiting = 0
total_turnaround = 0

print(f"{'Job':<4}{'Arrival':<8}{'Burst':<6}{'Completion':<10}{'Waiting':<8}{'Turnaround':<11}")
for job_id in job_info:
    job = job_info[job_id]
    turnaround = job['completion'] - job['arrival']
    waiting = turnaround - job['burst']
    job['waiting'] = waiting
    total_waiting += waiting
    total_turnaround += turnaround
    print(f"{job_id:<4}{job['arrival']:<8}{job['burst']:<6}{job['completion']:<10}{waiting:<8}{turnaround:<11}")

# Averages
avg_waiting = total_waiting / n
avg_turnaround = total_turnaround / n
print(f"\nAverage Waiting Time: {avg_waiting:.2f} ms")
print(f"Average Turnaround Time: {avg_turnaround:.2f} ms")
