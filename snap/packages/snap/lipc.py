# Rudimentary MicroPython implementation of the proprietary Lab126 IPC (LIPC) protocol used internally by Kindle.

import os
from tools import command_with_output_singleline as run_cmd

class LIPCService():
    def __init__(self, service_name):
        super().__setattr__("service_name", service_name)
        test_prop = run_cmd(f"lipc-get-prop {self.service_name} __test__")
        if "lipcErrNoSuchSource" in test_prop:
            raise ValueError(f"{self.service_name} is not a valid LIPC service")
    def __getattr__(self, name):
        value = run_cmd(f"lipc-get-prop {self.service_name} {name}")
        if "lipcErrNoSuchProperty" in value:
            raise AttributeError(f"{self.service_name} has no property {name}")
        return value
    def __setattr__(self, name, value):
        run_cmd(f"lipc-set-prop {self.service_name} {name} {value}")
    def wait_event(self, event_name):
        return run_cmd(f"lipc-wait-event {self.service_name} {event_name}")