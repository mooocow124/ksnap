# Generic tooling used for package management

import os
import random

def get_snap_dir() -> str: # Get the directory of the snap fs
    return os.path.dirname(os.path.realpath(__file__))

def command_with_output(command) -> list: # Run a command and return its output as a string using UNIX FIFO
    myfifo = "/tmp/snap_fifo_" + str(random.randint(0, 1000000)) # Create a random FIFO name to avoid collisions
    os.system("mkfifo " + myfifo) # Create the FIFO
    os.system(command + " > " + myfifo + " &") # Run the command and redirect its output to the FIFO
    output = []
    with open(myfifo, "r") as fifo: # Open the FIFO for reading
        output.append(fifo.read()) # Read the output from the FIFO
    os.system("rm " + myfifo) # Remove the FIFO
    return output

def command_with_output_bearable(command) -> list: # The original is NOT bearable to use
    output = command_with_output(command)
    for (i, line) in enumerate(output):
        if line.rstrip("\n"):
            output[i] = line.rstrip("\n")
        else:
            output[i] = None
    for line in output:
        if line is None:
            output.remove(line)
    return output

def command_with_output_singleline(command) -> str: # Pretty obvious innit
    output = command_with_output_bearable(command)
    try:
        return output[0]
    except IndexError:
        return ""

def rm_rf(path): # Helper function to recursively remove a directory and its contents, or a file
    mode = os.stat(path)[0]

    # Check if it's a directory (S_IFDIR is 0x4000)
    if mode & 0x4000:
        for entry in os.listdir(path):
            rm_rf(f"{path.rstrip('/')}/{entry}")
        os.rmdir(path)
    else:
        os.remove(path)