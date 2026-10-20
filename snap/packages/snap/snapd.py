### COMPLETE THIS LATER
# Safeguard against running this script from a different directory
import sys

# Get the directory of the currently running file
script_dir = __file__.rsplit('/', 1)[0] if '/' in __file__ else '.'

if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

import os
import tomli
from tools import path_join

services = {}

def parse_service_file(path):
    with open(path, 'r') as f:
        service = tomli.loads(f.read())
    return service

def index_services():
    """Index userspace services"""
    try:
        dir_services = os.listdir('/mnt/us/snap/services')
    except OSError:
        print("No services directory found, skipping indexing of services")
        return
    for service in dir_services:
        if service.endswith('.service.toml'):
            services[service.rstrip(".service.toml")] = parse_service_file(path_join('/mnt/us/snap/services', service))

def run_service(service_name):
    """Run a userspace service"""
    if service_name not in services:
        print(f"Service {service_name} not found")
        return
    service = services[service_name]
    command = service["command"]
    if command:
        os.system(command)
    else:
        print(f"No command found for service {service_name}")

def init():
    content = 'echo PATH="$PATH:/mnt/us/snap/shims"'
    with open("/tmp/root/.profile", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    init()