# Rudimentary MicroPython implementation of the proprietary Lab126 IPC (LIPC) protocol used internally by Kindle.

import os
from tools import command_with_output_singleline as run_cmd
from tools import command_with_output_bearable as command_with_output

class LIPCError(Exception):
    """Custom error type for LIPC-related issues."""

class LIPCPropertyError(LIPCError):
    """LIPC property access error, raised when attempting to read a write-only property or write to a read-only property."""

class LIPCService():
    """
    Represents a LIPC service, allowing interaction with its properties and events."""
    write_ban: list[str]
    read_ban: list[str]
    convert_to_int: list[str]
    properties: list[str]
    def __init__(self, service_name: str):
        super().__setattr__("service_name", service_name)
        super().__setattr__("write_ban", [])
        super().__setattr__("read_ban", [])
        super().__setattr__("convert_to_int", [])
        super().__setattr__("properties", [])
        test_prop = run_cmd(f"lipc-get-prop {self.service_name} __test__")
        if "lipcErrNoSuchSource" in test_prop:
            raise KeyError(f"Service '{self.service_name}' does not exist")
        if "lipcErr" in test_prop:
            raise LIPCError(test_prop.split("lipcErr")[1].rstrip(")"))
        probe_props = command_with_output(f"lipc-probe {self.service_name}")
        for prop in probe_props:
            prop_bits = prop.split()
            if "r" not in prop_bits[0]:
                self.read_ban.append(prop_bits[2])
            if "w" not in prop_bits[0]:
                self.write_ban.append(prop_bits[2])
            if prop_bits[1] == "Int":
                self.convert_to_int.append(prop_bits[2])
            self.properties.append(prop_bits[2])
    def __getattr__(self, name):
        if name in self.read_ban:
            raise LIPCPropertyError(f"Property '{name}' is write-only")
        if name not in self.properties:
            raise AttributeError(f"Property '{name}' does not exist")
        value = run_cmd(f"lipc-get-prop {self.service_name} {name}")
        if "lipcErr" in value:
            raise LIPCError(value.split("lipcErr")[1].rstrip(")"))
        if name in self.convert_to_int:
            value = int(value)
        return value
    def __setattr__(self, name, value):
        if name in self.write_ban:
            raise LIPCPropertyError(f"Property '{name}' is read-only")
        if name not in self.properties:
            raise AttributeError(f"Property '{name}' does not exist")
        value = run_cmd(f"lipc-set-prop {self.service_name} {name} {value}")
        if "lipcErr" in value:
            raise LIPCError(value.split("lipcErr")[1].rstrip(")"))
    def wait_event(self, event_name):
        return run_cmd(f"lipc-wait-event {self.service_name} {event_name}")
    def __dir__(self):
        # 1. Grab normal attributes (methods, class attributes, internal vars)
        default_attrs = super().__dir__()
        # 2. Return a combined, deduplicated sorted list
        return sorted(set(list(default_attrs) + self.properties))