import os
import sys
import subprocess


class Shell:

    builtin_commands = ["echo", "exit", "type", "pwd", "cd"]

    def __init__(self):
        self.commands = {
            "exit": lambda: self.exit(),
            "echo": lambda *real_args: self.echo(*real_args),
            "pwd": lambda: self.pwd(),
            "cd": lambda *real_args: self.cd(*real_args),
            "type": lambda *real_args: self.type(*real_args),
        }

    def redirect(self, command, real_args, file_name):
        directory = os.path.dirname(file_name)
        print(file_name)
        print(directory)
        if directory:
            os.makedirs(directory, exist_ok=True)
        output = self.commands[command](*real_args)
        if output:
            with open(file_name, "w") as f:
                f.write(output)
        else:
            raise ValueError(f"Command '{command}' did not return any output.")

    def parse_input(self, text):
        args = []
        word = ""

        in_single_quotes = False
        in_double_quotes = False
        escape_next = False

        for i, char in enumerate(text):
            if escape_next:
                word += char
                escape_next = False
                continue
            if char == "\\":
                if in_single_quotes:
                    word += char
                elif in_double_quotes:
                    if i + 1 < len(text) and text[i + 1] in ['"', "\\"]:
                        escape_next = True
                    else:
                        word += char
                else:
                    escape_next = True
                continue
            elif char == "'" and not in_double_quotes:
                in_single_quotes = not in_single_quotes
            elif char == '"' and not in_single_quotes:
                in_double_quotes = not in_double_quotes
            elif char.isspace() and not in_single_quotes and not in_double_quotes:
                if word:
                    args.append(word)
                    word = ""
            else:
                word += char

        if word:
            args.append(word)
        # print(args)

        return args

    def pwd(self):
        result = os.getcwd()
        return result

    def exit(self):
        sys.exit()

    def echo(self, *args):
        return " ".join(args)

    def cd(self, *args):
        if args[0] == "~":
            home = os.environ["HOME"]
            os.chdir(home)
        elif os.path.isdir(args[0]):
            os.chdir(args[0])
        else:
            print(f"cd: {args[0]}: No such file or directory")

    def type(self, *args):
        if args[0] in self.builtin_commands:
            print(f"{args[0]} is a shell builtin")

        else:
            y = os.environ["PATH"]
            z = y.split(os.pathsep)

            found = False

            for i in z:
                full_path = os.path.join(i, args[0])

                if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                    print(f"{args[0]} is {full_path}")
                    found = True
                    break

            if found == False:  # if not found
                print(f"{args[0]}: not found")

    def is_command_exists(self, command):
        # Check if the command exists in the system
        pass

    def run_not_found(self, command, *args):
        y = os.environ["PATH"]
        z = y.split(os.pathsep)

        found = False

        for i in z:
            full_path = os.path.join(i, command)

            if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                subprocess.run([command, *args], executable=full_path)

                found = True
                break

        if found == False:  # if not found
            print(f"{command}: command not found")
