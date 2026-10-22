def try_type(input: str, type: type):
    try:
        if type is not bool:
            return type(input)
        else:
            input = input.lower().strip()
            if input in ("false", "n", "0", "no", "f"):
                return False
            elif input in ("true", "y", "1", "yes", "t"):
                return True
            else:
                raise ValueError()
    except (ValueError, TypeError):
        return None

class SnapCommand():
    subcommands: dict[str, SnapCommand]
    flags: dict[str, tuple[type]]
    parameters: list[tuple[str, tuple[type]]]
    parameters_enabled: bool
    def __init__(self, flags, parameters) -> None:
        self.flags = flags
        self.parameters = parameters
    def parse(self, args: list):
        to_append = []
        new_args = []
        for arg in args:
            try:
                if arg[0] == "-":
                    to_append.append(arg)
                else:
                    new_args.append(arg)
            except IndexError:
                continue
        for item in to_append:
            new_args.append(item)
        args = new_args
        if args[0] in self.subcommands:
            self.subcommands[args[0]].parse(args[1:])
            return