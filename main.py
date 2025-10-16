"""
Runs main program with menu to select scheduling algorithm.
"""


from scheduler import load_processes, run_all

if __name__ == "__main__":
    print("🧠 CPU Scheduling Algorithm Simulator")
    print("-------------------------------------")

    processes = load_processes("data.csv")
    print(f"Loaded {len(processes)} processes from data.csv")

    run_all(processes)