"""
CPU Algorithms Module
- FCFS
- SJF (non-preemptive)
- SRT (preemptive)
- RR (round-robin) (quantum = 4ms)
"""

from collections import deque
from typing import List, Dict, Tuple
import heapq

"""
# Pseudo code for FCFS
1. Sort processes by arrival time
2. Initialize current_time = 0
3. For each process in sorted order:
    a. If current_time < process.arrival_time:
        i. current_time = process.arrival_time
    b. waiting_time = current_time - process.arrival_time
    c. turnaround_time = waiting_time + process.burst_time
    d. current_time += process.burst_time
    e. Store waiting_time and turnaround_time for the process
4. Calculate average waiting time and average turnaround time
"""

def fcfs(processes: List[Dict[str, int]]) -> Tuple[List[Dict[str, int]], float, float]:
    """
    First-Come, First-Served Scheduling Algorithm
    Jobs execute in the order they arrive.
    """
    processes = sorted(processes, key=lambda x: x['arrival_time'])
    current_time = 0
    total_waiting_time = 0
    total_turnaround_time = 0

    for process in processes:
        # If CPU is idle, move current_time to process arrival time
        if current_time < process['arrival_time']:
            current_time = process['arrival_time']
        # Calculate waiting time and turnaround time
        waiting_time = current_time - process['arrival_time']
        turnaround_time = waiting_time + process['burst_time']
        # increment current time
        total_waiting_time += waiting_time
        total_turnaround_time += turnaround_time
        # Move current time forward
        current_time += process['burst_time']
        process['waiting_time'] = waiting_time
        process['turnaround_time'] = turnaround_time

    # Calculate average waiting time and average turnaround time
    avg_waiting_time = total_waiting_time / len(processes)
    avg_turnaround_time = total_turnaround_time / len(processes)

    return processes, avg_waiting_time, avg_turnaround_time

"""
# Pseudo code for SJF (non-preemptive)
1. Sort processes by arrival time
2. Initialize current_time = 0
3. While there are unprocessed processes:
    a. Get all processes that have arrived by current_time
    b. If no processes have arrived, increment current_time
    c. Else, select the process with the shortest burst time from the arrived processes
        i. waiting_time = current_time - process.arrival_time
        ii. turnaround_time = waiting_time + process.burst_time
        iii. current_time += process.burst_time
        iv. Store waiting_time and turnaround_time for the process
4. Calculate average waiting time and average turnaround time
"""

def sjf(processes: List[Dict[str, int]]) -> Tuple[List[Dict[str, int]], float, float]:
    """
    Shortest Job First Scheduling Algorithm (Non-Preemptive)
    Jobs with the shortest burst time are executed first.
    """
    processes = sorted(processes, key=lambda x: x['arrival_time'])
    current_time = 0
    total_waiting_time = 0
    total_turnaround_time = 0
    completed_processes = 0
    n = len(processes)
    is_completed = [False] * n

    while completed_processes < n:
        # Get all processes that have arrived by current_time
        arrived_processes = [i for i in range(n) if processes[i]['arrival_time'] <= current_time and not is_completed[i]]
        
        if not arrived_processes:
            current_time += 1
            continue
        
        # Select the process with the shortest burst time
        idx = min(arrived_processes, key=lambda i: processes[i]['burst_time'])
        process = processes[idx]
        
        # Calculate waiting time and turnaround time
        waiting_time = current_time - process['arrival_time']
        turnaround_time = waiting_time + process['burst_time']
        
        # Update times and mark process as completed
        total_waiting_time += waiting_time
        total_turnaround_time += turnaround_time
        current_time += process['burst_time']
        is_completed[idx] = True
        completed_processes += 1
        
        process['waiting_time'] = waiting_time
        process['turnaround_time'] = turnaround_time

    # Calculate average waiting time and average turnaround time
    avg_waiting_time = total_waiting_time / n
    avg_turnaround_time = total_turnaround_time / n

    return processes, avg_waiting_time, avg_turnaround_time

"""
Pseudocode for SRT
1. Sort processes by arrival time.
2. Set current_time = 0.
3. While there are still processes not done:
   a. Find all processes that have arrived (arrival_time ≤ current_time).
   b. Among them, pick the one with the smallest remaining burst time.
   c. Run that process for 1 unit of time.
   d. Reduce its remaining burst time by 1.
   e. Increase current_time by 1.
   f. If the process finishes (remaining time = 0), record its finish, waiting, and turnaround times.
4. Continue until all processes are complete.
5. Compute average waiting time and average turnaround time
"""

"""
Pseudocode for RR
1. Sort all processes by their arrival time.
2. Set current_time = 0.
3. Put all processes that have arrived into a queue (called the ready_queue).
4. While there are still processes left to finish:
   a. If the ready_queue is empty, move current_time forward until a process arrives.
   b. Take the first process from the queue.
   c. Run it for up to the time quantum (for example, 4ms).
   d. Reduce its remaining burst time by how long it ran.
   e. Increase current_time by the amount of time the CPU just used.
   f. If new processes have arrived during that time, add them to the queue.
   g. If the current process is not yet done, put it at the **end of the queue**.
   h. If it’s done, record its finish, waiting, and turnaround times.
5. Repeat until every process has finished.
6. Compute average waiting time and average turnaround time
"""
