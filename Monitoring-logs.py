import time
import psutil
import sys
from datetime import datetime

LOG_FILE = '/app/logs/logs-text'  # Ensure this path is correct based on your setup

def log_alert(process_name, status):
    """Log an alert to a text file and stdout."""
    subject = f"Process Alert: {process_name} is {status}"
    body = f"The process '{process_name}' is {status}."
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {subject}\n{body}\n\n"

    # Log to file
    with open(LOG_FILE, 'a') as log_file:
        log_file.write(log_entry)

    # Log to stdout (Docker will capture this)
    print(log_entry, end='')  # Avoid double newlines

    # Optionally log to stderr in case of issues (for visibility)
    sys.stderr.write(log_entry)

def monitor_processes():
    """Check if all processes are running or not running."""
    while True:
        # Iterate over all running processes on the system
        for proc in psutil.process_iter(['pid', 'name']):
            process_name = proc.info['name']
            process_pid = proc.info['pid']

            # Check if the process is still running
            try:
                proc_status = proc.status()  # Get the current status of the process
                status = 'running' if proc_status == psutil.STATUS_RUNNING else 'not running'
                log_alert(process_name, status)
            except (psutil.NoSuchProcess, psutil.ZombieProcess):
                # Process no longer exists or is a zombie
                status = 'not running'
                log_alert(process_name, status)

        # Sleep for some time before checking again (e.g., every 30 seconds)
        time.sleep(30)

if __name__ == "__main__":
    monitor_processes()
