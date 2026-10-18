SNAP_DIR = "/mnt/us/snap" # set this to whatever directory `snap` folder of git repo is in

def rm(pkg):
    pass

def info(pkg):
    if pkg == "commands":
        print(commands.keys())

subhelpers = {"commands": lambda: print("Available commands:", list(commands.keys())),
              "flags": lambda: print("Todo: implement flags list")}

def help(subhelp=None): # Subhelp is the specific module to help with
    if subhelp:
        try:
            subhelpers[subhelp]()
        except KeyError:
            print("No such module exists. For general help, try `ksnap help -y`")
    else:
        print(helpdialogue)

commands = {
    "rm": rm,
    "help": help
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

