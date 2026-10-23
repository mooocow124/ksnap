import os
import random
from tools import get_snap, resolve_unique_schemas, get_snap_dir, path_join

def rm(pkg, state):
    print(f"Removing package {pkg}...")
    # Implementation for removing package
    if pkg not in state["package_required"]:
        print(f"Package {pkg} is not installed and thus cannot be removed.")
        return state
    package_snap = get_snap(pkg)
    depends = state["package_depended_on"]
    if pkg in depends:
        print(f"Package {pkg} is required by other packages: {depends[pkg]}, thus full removal may not be possible. Removing from required anyway.")
    if package_snap.get("install", {}).get("uninstall") is False:
        print(f"Package {pkg} is marked as non-removable. Aborting removal.")
        return state
    state["package_required"].remove(pkg)
    def iterate(providers):
        for provider in list(providers.keys()):
            if pkg in providers[provider]:
                providers[provider].remove(pkg)
            if len(providers[provider]) == 0:
                del providers[provider]
    iterate(state["kual_providers"])
    iterate(state["service_providers"])
    iterate(state["shim_providers"])
    iterate(state["package_depended_on"])
    return state

def add(pkg, state):
    print(f"Adding package {pkg}...")
    # Implementation for adding package
    packages_installed = os.listdir(path_join(get_snap_dir(), "packages"))
    package_url = resolve_unique_schemas(pkg)
    print(f"Downloading URL {package_url}")
    scratch_path = path_join(get_snap_dir(), "scratch.zip")
    tempkg = path_join(get_snap_dir(), "packages", f"temp_{random.randint(0, 1000000)}")
    package_wget = os.system(f'wget -O "{scratch_path}" "{package_url}"')
    if package_wget != 0:
        print("Aborting, failed to download package.")
        os.system(f'rm -f "{scratch_path}"')
        return state
    print("Extracting package..")
    package_unzip = os.system(f'unzip "{scratch_path}" -d "{tempkg}"')
    if package_unzip != 0:
        print("Aborting, failed to unzip package.")
        os.system(f'rm -rf "{tempkg}"')
        return state
    temp_snap = get_snap("temp")
    pkgname = temp_snap["name"]
    if pkgname in packages_installed:
        print(f"Package {pkgname} is already installed, adding to required.")
        os.system(f'rm -rf "{tempkg}"')
    else:
        os.rename(tempkg, path_join(get_snap_dir(), "packages", pkgname))
    state["package_required"].append(pkgname)
    return state

def gen_shims():
    pass

def info(pkg, state):
    if pkg == "commands":
        print(commands.keys())
    return state

subhelpers = {"commands": lambda: print("Available commands:", list(commands.keys())),
              "flags": lambda: print("Todo: implement flags list")}

def help(subhelp=None, state=None): # Subhelp is the specific module to help with
    if subhelp:
        try:
            subhelpers[subhelp]()
        except KeyError:
            print("No such module exists. For general help, try `ksnap help -y`")
    else:
        print(helpdialogue)
    return state

commands = {
    "rm": rm,
    "help": help,
    "info": info
}

helpdialogue = '''
ksnap v0.0.1
Package manager for modern jailbroken Amazon Kindles
Each argument follows a structure of `action:argument`.
For example: `ksnap add:https://github.com/mooocow124/snap_example_pkg rm:someotherpackage`
You can add any git repo as a package.
For a list of commands at this time, run `ksnap help:commands`.
For flags, we use - as a prefix instead of --. For example, `ksnap -help`.
Tested devices: Kindle Paperwhite 12th gen, OS version 5.20.1, jailbroken with Vera
We'd love it if you contribute!
https://github.com/mooocow124/ksnap
'''

