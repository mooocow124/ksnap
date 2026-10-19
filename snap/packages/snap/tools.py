# Generic tooling used for package management

import os
import random

def command_with_output(command) -> list: # Run a command and return its output as a string using UNIX FIFO
    myfifo = "/tmp/snap_fifo_" + str(random.randint(0, 1000000)) # Create a random FIFO name to avoid collisions
    os.system("mkfifo " + myfifo) # Create the FIFO
    os.system(command + " > " + myfifo + " &") # Run the command and redirect its output to the FIFO
    output = []
    with open(myfifo, "r") as fifo: # Open the FIFO for reading
        output.append(fifo.read()) # Read the output from the FIFO
    os.system("rm " + myfifo) # Remove the FIFO
    return output

def command_with_output_singleline(command) -> str:
    output = command_with_output(command)
    for line in output:
        if line.rstrip("\n"):
            return line.rstrip("\n")
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

### WIP FUNCTION ###
def direct_install(url: str): # Install a package directly from a URL
    if url.startswith("gh://"): # GitHub shorthand
        url_repo_path = url[5:] # get the part after gh://
        url_bits = url_repo_path.split("/") # split the repo path into its components
        if len(url_bits) < 2: # If the repo path is invalid
            raise ValueError("Invalid GitHub repo path. Must be in the format 'gh://username/repo'")
        url = f"https://github.com/{url_bits[0]}/{url_bits[1]}/archive/main.zip"
    return url
