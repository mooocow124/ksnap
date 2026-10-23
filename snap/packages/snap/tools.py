# Generic tooling used for package management
import os
import random
import requests
import json
import tomli

def get_snap_dir() -> str:
    path = __file__
    
    # 1. Resolve to an absolute path if it's relative
    if not path.startswith('/'):
        cwd = os.getcwd().rstrip('/')
        path = f"{cwd}/{path}"
    
    # 2. Normalize basic relative segments (e.g. /./ or /../)
    parts = []
    for segment in path.split('/'):
        if segment in ('', '.'):
            continue
        elif segment == '..':
            if parts:
                parts.pop()
        else:
            parts.append(segment)
            
    # 3. Drop the filename itself (equivalent to dirname)
    if len(parts) > 3:  # Ensure we don't pop too much and lose the root
        parts.pop()
        parts.pop()
        parts.pop()
        
    return '/' + '/'.join(parts)

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

def path_join(*parts):
    return "/" + "/".join(p.strip("/") for p in parts if p)

def resolve_url_to_file():
    pass

def resolve_unique_schemas(url: str) -> str:
    if url.startswith("gh://"):
        schema = "gh"
        rest = url[len("gh://"):]
    elif url.startswith("cb://"):
        schema = "cb"
        rest = url[len("cb://"):]
    else:
        return url

    if ":" in rest:
        repo, spec = rest.split(":", 1)
    else:
        repo, spec = rest, None

    repo = repo.strip("/")

    # Check for releases specifier
    if spec and (spec.startswith("releases/") or spec.startswith("release/") or spec == "releases"):
        if schema != "gh":
            return "Releases are not supported for Codeberg"

        filename = spec.split("/", 1)[1] if "/" in spec else ""
        return f"https://github.com/{repo}/releases/latest/download/{filename}"

    # Default to HEAD so both platforms resolve the default branch automatically
    ref = spec if spec else "HEAD"

    if schema == "gh":
        return f"https://github.com/{repo}/archive/{ref}.zip"
    elif schema == "cb":
        return f"https://codeberg.org/{repo}/archive/{ref}.zip"

    return url

def load_state():
    state_path = path_join(get_snap_dir(), "state.json")
    with open(state_path, "r") as f:
        return json.load(f)

def state_commit(state):
    snap_dir = get_snap_dir()
    state_path = path_join(snap_dir, "state.json")
    temp_path = path_join(snap_dir, "state.json.tmp")

    # Check existing state
    try:
        with open(state_path, "r") as f:
            if json.load(f) == state:
                return
    except (OSError, ValueError):
        # File doesn't exist (ENOENT) or contains invalid JSON
        pass

    # Write to a temp file first (mode "w" truncates by default)
    with open(temp_path, "w") as f:
        json.dump(state, f)

    # In POSIX / Unix port, os.rename cleanly overwrites the destination
    # Use os.replace if your build has it; otherwise os.rename works.
    os.rename(temp_path, state_path)  # Atomic operation to replace the old state file

def get_snap(pkg):
    try:
        with open(path_join(get_snap_dir(), "packages", pkg, "snap.toml"), "r") as f:
            return tomli.loads(f.read())
    except OSError:
        return {}

def gen_depends(state):
    depends = {}
    for pkg in state["package_depended_on"]:
        for dep in state["package_depended_on"][pkg]:
            if dep not in depends:
                depends[dep] = []
            depends[dep].append(pkg)
    return depends