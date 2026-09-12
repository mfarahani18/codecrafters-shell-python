import os
import sys
import subprocess
import readline



class Shell:

    builtin_commands = ["echo", "exit", "type", "pwd", "cd", "complete", "jobs" ]

    def __init__(self):
        self.completions = {}
        
        self.commands = {
            "exit": lambda: self.exit(),
            "echo": lambda *real_args: self.echo(*real_args),
            "pwd": lambda: self.pwd(),
            "cd": lambda *real_args: self.cd(*real_args),
            "type": lambda *real_args: self.type(*real_args),
            "complete": lambda *real_args: self.complete(*real_args),
            "jobs": lambda: self.jobs(),
            }
    def find_matches(self, text, args):
        matches = []

        if args:
            if "/" in args[-1]:
                return self.find_file_by_path(args[-1])

            return self.find_entry_by_prefix(args[-1])

        if text == "":
            return self.find_entry_by_prefix("")

        for cmd in self.builtin_commands:
            if cmd.startswith(text):
                matches.append(cmd)

        external_commands = self.find_executable_by_prefix(text)

        for cmd in external_commands:
            if cmd not in matches:
                matches.append(cmd)

        return matches

    def autocomplete(self, text, state):
        line = readline.get_line_buffer()
        command, *args = line.split()
        COMP_LINE = line
        COMP_POINT = str(len(COMP_LINE))
        if command in self.completions:
            full_path = self.completions[command]
            if len(args) < 2:
                previous = command
            else:
                previous = args[-2]
                
            result = subprocess.run(
                [full_path, command, text, previous],
                capture_output=True,
                text=True,
                env={"COMP_LINE": COMP_LINE, "COMP_POINT": COMP_POINT}
            )
            
            matches = result.stdout.split()
        else:
            matches = self.find_matches(text, args)

        if state < len(matches):
            if matches[state].endswith("/"):
                return matches[state]
                
            if len(matches) == 1:
                return matches[state] + " "
                # if text and matches[state].startswith(text):
                #     return matches[state][len(text):] + " "
                # return matches[state] + " "
            return matches[state]
        
        return None
    
    def display_matches(self, user_input, matches, longest_match_length):
        sys.stdout.write("\r\n")
        sys.stdout.write(" ".join(sorted(matches)))
        sys.stdout.write("\r\n$ " + readline.get_line_buffer())
        sys.stdout.flush()

    def redirect(self, command, real_args, file_name, symbol):
        directory = os.path.dirname(file_name)

        if directory:
            os.makedirs(directory, exist_ok=True)

        if command in self.commands:
            output = self.commands[command](*real_args)
            error = ""
        else:
            output, error = self.run_not_found(
                command, *real_args, capture=True)
        
        if symbol in [">", "1>"]:
            with open(file_name, "w") as f:
                if output:
                    f.write(output)

            if error:
                sys.stderr.write(error)
        
        elif symbol in [">>", "1>>"]:
            with open(file_name, "a") as f:
                if output:
                    f.write(output)

            if error:
                sys.stderr.write(error)

        elif symbol == "2>":
            # with open(file_name, "w") as f:
                if output:
                    sys.stdout.write(output)

                with open(file_name, "w") as f:
                    if error:
                        f.write(error)

        elif symbol == "2>>":
            if output:
                sys.stdout.write(output)
            
            with open(file_name, "a") as f:
                if error:
                    f.write(error)


    def find_executable(self, command):
        y = os.environ.get("PATH", "")
        z = y.split(os.pathsep)

        for i in z:
            full_path = os.path.join(i, command)

            if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                return full_path

            for ext in [".exe", ".cmd", ".bat"]:
                candidate = full_path + ext

                if os.path.isfile(candidate):
                    return candidate

        return None

    def find_executable_by_prefix(self, perfix):
        matches = []
        
        path = os.environ.get("PATH", "")
        paths = path.split(os.pathsep)

        for path in paths:
            if not os.path.isdir(path):
                continue

            for file_name in os.listdir(path):
                if file_name.startswith(perfix):
                    full_path = os.path.join(path, file_name)
                    if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                        if file_name not in matches:
                            matches.append(file_name)

        return matches

    def find_entry_by_prefix(self, perfix):
        matches = []
        path = os.getcwd()

        for entry in os.listdir(path):
            if entry.startswith(perfix):
                full_path = os.path.join(path, entry)

                if os.path.isdir(full_path):
                    if entry + "/" not in matches:
                        matches.append(entry + "/")
                else:
                    if entry not in matches:
                        matches.append(entry)

        return matches

    def find_file_by_path(self,text):
        matches = []

        idx = text.rfind("/")

        directory = text[:idx]
        file_name = text[idx + 1:]
        prefix = text[:idx + 1]

        for entry in os.listdir(directory):
            if entry.startswith(file_name):
                full_path = os.path.join(directory, entry)
                if os.path.isdir(full_path):
                    entry_name = prefix + entry + "/"
                    if entry_name not in matches:
                        matches.append(entry_name)
                else:
                    entry_name = prefix + entry
                    if entry_name not in matches:
                        matches.append(entry_name)

        return matches


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
                    # if i + 1 < len(text) and text[i + 1].isalpha():
                    #     word += char
                    # else:
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

        return args

    def pwd(self):
        result = os.getcwd()
        return result + "\n"

    def exit(self):
        sys.exit()

    def echo(self, *args):
        return " ".join(args) + "\n"

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
            return f"{args[0]} is a shell builtin\n"

        full_path = self.find_executable(args[0])
        
        if full_path:
            return f"{args[0]} is {full_path}\n"

        return f"{args[0]}: not found\n"
    
    def jobs(self):
        pass

    def complete(self, *args):
        if args[0] == "-C":
            valu = args[1]
            key = args[2]
            self.completions[key] = valu
        elif args[0] == "-p":
                if args[1] in self.completions:
                    return f"complete -C '{self.completions[args[1]]}' {args[1]}\n"
                else:
                    return f"complete: {args[1]}: no completion specification\n"
        elif args[0] == "-r":
            self.completions.pop(args[1], None)
            
    def run_not_found(self, command, *args, capture=False):
        
        full_path = self.find_executable(command)

        if full_path:
            if capture:
                result = subprocess.run(
                    [command, *args],
                    executable=full_path,
                    capture_output=True,
                    text=True,
                )
                return result.stdout, result.stderr

            subprocess.run([command, *args],
                            executable=full_path)
            return None

        if capture:
            return "", f"{command}: command not found\n"

        print(f"{command}: command not found")
        return ""