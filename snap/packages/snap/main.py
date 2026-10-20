# Safeguard against running this script from a different directory
import sys

# Get the directory of the currently running file
script_dir = __file__.rsplit('/', 1)[0] if '/' in __file__ else '.'

if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

import sys
import tomli
import actions
from tools import load_state, state_commit

def execute(commands):
    print("Executing transaction!")
    state = load_state()
    i = 0
    length = len(commands) # amount of commands given
    for command in commands.keys():
        i += 1
        print(f"Executing '{command}', command {i} out of {length}")
        state = actions.commands[command](commands[command], state)
    state_commit(state)
    print("Finished transaction.")

def main(): # parse arguments and return actions and their parameters
    arguments = sys.argv[1:]
    flags = []
    commands = {}
    for arg in arguments:
        if arg[0] == "-": # get the flags (-x) and don't process them as commands
            flags.append(arg)
        else:
            commandbits = arg.split(":")
            command = commandbits[0] # get the actual command, ie rm, or info, et cetera
            command_argument = ":".join(commandbits[:0] + commandbits[0 + 1 :]) # merge all the indices after 0 to get the argument for the command
            commands[command] = command_argument
    if len(commands) != 0: # If any command is given
        print("Full transaction:")
        for command in commands.keys(): # List commands
            print(f"Call command '{command}' with parameter '{commands[command]}'")
        print(f"Flags: {flags}")
        if "-y" in flags:
            goahead = "y"
        else:
            goahead = input("Proceed with transaction? [Y/N] ")
        goahead = goahead + "z" # hack to prevent an IndexError if blank input
        if goahead.lower()[0] == "y":
            execute(commands)
        else:
            print("Aborting transaction.")
    else:
        if '-help' in flags or '--help' in flags: # show help dialogue
            actions.help()
        else:
            print("Todo in next release: implement updating all packages when command called with no args")

if __name__ == "__main__":
    main()