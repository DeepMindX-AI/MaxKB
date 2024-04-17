from blinker import signal
initialized = signal('initialized')
print(initialized)
print(initialized is signal('initialized'))

from blinker import signal

# Create a signal
task_completed = signal('task_completed')

# Define a function that acts on the signal
def report_completion(sender):
    print(f"2. {sender} has completed the task.")

# Connect the function to the signal
task_completed.connect(report_completion)

# Function that completes a task and sends a signal
def complete_task(task_name):
    print(f"1. Completing {task_name}...")
    # Simulate completing a task
    task_completed.send(task_name)

# Call the function
complete_task("Data Analysis")
