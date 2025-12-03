import time
import csv
import os
import re

def tail(filename):
    with open(filename, "r") as f:
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if not line:
                time.sleep(1)
                continue
            yield line.strip()

def parse_access_log(line):
    match = re.match(r'^(\S+) (\S+) (\S+) \[(.*?)\] "(.*?)" (\d+) (\S+)', line)
    if match:
        return list(match.groups())
    return None

def parse_error_log(line):
    match = re.match(r'^\[(.*?)\] \[(.*?)\] \[pid (\d+)\] (.*?)$', line)
    if match:
        return list(match.groups())
    return None

def write_to_csv(filename, data, headers):
    file_exists = os.path.isfile(filename)
    with open(filename, mode='a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(headers)
        writer.writerow(data)

def monitor_logs():
    access_log = "/var/log/apache2/access.log"
    error_log = "/var/log/apache2/error.log"
    access_csv = "/opt/apache_log_monitor/access_log.csv"
    error_csv = "/opt/apache_log_monitor/error_log.csv"

    for line in tail(access_log):
        parsed = parse_access_log(line)
        if parsed:
            write_to_csv(access_csv, parsed, ["IP", "Identd", "User", "Timestamp", "Request", "Status", "Size"])

    for line in tail(error_log):
        parsed = parse_error_log(line)
        if parsed:
            write_to_csv(error_csv, parsed, ["Timestamp", "Severity", "PID", "Message"])

if _name_ == "_main_":
    monitor_logs()
