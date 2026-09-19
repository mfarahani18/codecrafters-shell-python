# import os
# import re
# import sys
# import subprocess
# import readline



# class Shell:

#     builtin_commands = ["echo", "exit", "type", "pwd", "cd", "complete", "jobs", "history", "declare" ]

#     def __init__(self):
#         self.completions = {}
#         self.jobs_data = {}
#         self.history_data = []
#         self.last_append_index = 0
#         self.variables = {}
        
#         self.histfile = os.environ.get("HISTFILE")
#         if self.histfile:
#             with open(self.histfile) as file:
#                 for line in file:
#                     line = line.rstrip("\n")
#                     if line:
#                         self.history_data.append(line)
#             self.last_append_index = len(self.history_data)
            
            
#         self.commands = {
#             "exit": lambda: self.exit(),
#             "echo": lambda *real_args: self.echo(*real_args),
#             "pwd": lambda: self.pwd(),
#             "cd": lambda *real_args: self.cd(*real_args),
#             "type": lambda *real_args: self.type(*real_args),
#             "complete": lambda *real_args: self.complete(*real_args),
#             "jobs": lambda: self.jobs(),
#             "history": lambda *real_args: self.history(*real_args),
#             "declare": lambda *real_args: self.declare(*real_args),
#             }
#     def find_matches(self, text, args):
#         matches = []

#         if args:
#             if "/" in args[-1]:
#                 return self.find_file_by_path(args[-1])

#             return self.find_entry_by_prefix(args[-1])

#         if text == "":
#             return self.find_entry_by_prefix("")

#         for cmd in self.builtin_commands:
#             if cmd.startswith(text):
#                 matches.append(cmd)

#         external_commands = self.find_executable_by_prefix(text)

#         for cmd in external_commands:
#             if cmd not in matches:
#                 matches.append(cmd)

#         return matches

#     def autocomplete(self, text, state):
#         line = readline.get_line_buffer()
#         command, *args = line.split()
#         COMP_LINE = line
#         COMP_POINT = str(len(COMP_LINE))
#         if command in self.completions:
#             full_path = self.completions[command]
#             if len(args) < 2:
#                 previous = command
#             else:
#                 previous = args[-2]
                
#             result = subprocess.run(
#                 [full_path, command, text, previous],
#                 capture_output=True,
#                 text=True,
#                 env={"COMP_LINE": COMP_LINE, "COMP_POINT": COMP_POINT}
#             )
            
#             matches = result.stdout.split()
#         else:
#             matches = self.find_matches(text, args)

#         if state < len(matches):
#             if matches[state].endswith("/"):
#                 return matches[state]
                
#             if len(matches) == 1:
#                 return matches[state] + " "
#                 # if text and matches[state].startswith(text):
#                 #     return matches[state][len(text):] + " "
#                 # return matches[state] + " "
#             return matches[state]
        
#         return None
    
#     def display_matches(self, user_input, matches, longest_match_length):
#         sys.stdout.write("\r\n")
#         sys.stdout.write(" ".join(sorted(matches)))
#         sys.stdout.write("\r\n$ " + readline.get_line_buffer())
#         sys.stdout.flush()

#     def redirect(self, command, real_args, file_name, symbol):
#         directory = os.path.dirname(file_name)

#         if directory:
#             os.makedirs(directory, exist_ok=True)

#         if command in self.commands:
#             output = self.commands[command](*real_args)
#             error = ""
#         else:
#             output, error = self.run_not_found(
#                 command, *real_args, capture=True)
        
#         if symbol in [">", "1>"]:
#             with open(file_name, "w") as f:
#                 if output:
#                     f.write(output)

#             if error:
#                 sys.stderr.write(error)
        
#         elif symbol in [">>", "1>>"]:
#             with open(file_name, "a") as f:
#                 if output:
#                     f.write(output)

#             if error:
#                 sys.stderr.write(error)

#         elif symbol == "2>":
#             # with open(file_name, "w") as f:
#                 if output:
#                     sys.stdout.write(output)

#                 with open(file_name, "w") as f:
#                     if error:
#                         f.write(error)

#         elif symbol == "2>>":
#             if output:
#                 sys.stdout.write(output)
            
#             with open(file_name, "a") as f:
#                 if error:
#                     f.write(error)


#     def find_executable(self, command):
#         y = os.environ.get("PATH", "")
#         z = y.split(os.pathsep)

#         for i in z:
#             full_path = os.path.join(i, command)

#             if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
#                 return full_path

#             for ext in [".exe", ".cmd", ".bat"]:
#                 candidate = full_path + ext

#                 if os.path.isfile(candidate):
#                     return candidate

#         return None

#     def find_executable_by_prefix(self, perfix):
#         matches = []
        
#         path = os.environ.get("PATH", "")
#         paths = path.split(os.pathsep)

#         for path in paths:
#             if not os.path.isdir(path):
#                 continue

#             for file_name in os.listdir(path):
#                 if file_name.startswith(perfix):
#                     full_path = os.path.join(path, file_name)
#                     if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
#                         if file_name not in matches:
#                             matches.append(file_name)

#         return matches

#     def find_entry_by_prefix(self, perfix):
#         matches = []
#         path = os.getcwd()

#         for entry in os.listdir(path):
#             if entry.startswith(perfix):
#                 full_path = os.path.join(path, entry)

#                 if os.path.isdir(full_path):
#                     if entry + "/" not in matches:
#                         matches.append(entry + "/")
#                 else:
#                     if entry not in matches:
#                         matches.append(entry)

#         return matches

#     def find_file_by_path(self,text):
#         matches = []

#         idx = text.rfind("/")

#         directory = text[:idx]
#         file_name = text[idx + 1:]
#         prefix = text[:idx + 1]

#         for entry in os.listdir(directory):
#             if entry.startswith(file_name):
#                 full_path = os.path.join(directory, entry)
#                 if os.path.isdir(full_path):
#                     entry_name = prefix + entry + "/"
#                     if entry_name not in matches:
#                         matches.append(entry_name)
#                 else:
#                     entry_name = prefix + entry
#                     if entry_name not in matches:
#                         matches.append(entry_name)

#         return matches


#     def parse_input(self, text):
#         args = []
#         word = ""

#         in_single_quotes = False
#         in_double_quotes = False
#         escape_next = False

#         for i, char in enumerate(text):

#             if escape_next:
#                 word += char
#                 escape_next = False
#                 continue

#             if char == "\\":
#                 if in_single_quotes:
#                     word += char

#                 elif in_double_quotes:
#                     if i + 1 < len(text) and text[i + 1] in ['"', "\\"]:
#                         escape_next = True
#                     else:
#                         word += char

#                 else:
#                     # if i + 1 < len(text) and text[i + 1].isalpha():
#                     #     word += char
#                     # else:
#                     escape_next = True

#                 continue

#             elif char == "'" and not in_double_quotes:
#                 in_single_quotes = not in_single_quotes

#             elif char == '"' and not in_single_quotes:
#                 in_double_quotes = not in_double_quotes

#             elif char.isspace() and not in_single_quotes and not in_double_quotes:
#                 if word:
#                     args.append(word)
#                     word = ""

#             else:
#                 word += char

#         if word:
#             args.append(word)

#         return args

#     def pwd(self):
#         result = os.getcwd()
#         return result + "\n"
    
#     def exit(self):
#         if self.histfile:
#             with open(self.histfile, "w") as file:
#                 for command in self.history_data:
#                     file.write(command + "\n")
#         sys.exit()

#     def echo(self, *args):
#         return " ".join(args) + "\n"

#     def cd(self, *args):
#         if args[0] == "~":
#             home = os.environ["HOME"]
#             os.chdir(home)

#         elif os.path.isdir(args[0]):
#             os.chdir(args[0])

#         else:
#             print(f"cd: {args[0]}: No such file or directory")

#     def type(self, *args):
#         if args[0] in self.builtin_commands:
#             return f"{args[0]} is a shell builtin\n"

#         full_path = self.find_executable(args[0])
        
#         if full_path:
#             return f"{args[0]} is {full_path}\n"

#         return f"{args[0]}: not found\n"
    
#     def print_done_job(self, job_number, data, job_numbers):
#         status = f"{'Done':<24}"
#         done_command = data["command"].rstrip(" &")

#         if job_number == job_numbers[-1]:
#             print(f"[{job_number}]+  {status}{done_command}")

#         elif len(job_numbers) > 1 and job_number == job_numbers[-2]:
#             print(f"[{job_number}]-  {status}{done_command}")

#         else:
#             print(f"[{job_number}]   {status}{done_command}")
        
#     def reap_jobs(self):
#         job_numbers = list(self.jobs_data.keys())
#         finished_jobs = []

#         for job_number, data in self.jobs_data.items():
#             if data["process"].poll() is not None:
#                 self.print_done_job(job_number, data, job_numbers)
#                 finished_jobs.append(job_number)

#         for job_number in finished_jobs:
#             del self.jobs_data[job_number]

                
#     def jobs(self):
         
#         job_numbers = list(self.jobs_data.keys())
#         finished_jobs = []
#         for job_number, data in self.jobs_data.items():
            
#             if data["process"].poll() is None:
                
#                 status = f"{data['status']:<24}"
                
#                 if job_number == job_numbers[-1]:
#                     print(f"[{job_number}]+  {status}{data['command']}")
                    
#                 elif len(job_numbers) > 1 and job_number == job_numbers[-2]:
#                     print(f"[{job_number}]-  {status}{data['command']}")
                    
#                 else:
#                     print(f"[{job_number}]   {status}{data['command']}")
#             else:
#                 self.print_done_job(job_number, data, job_numbers)
#                 finished_jobs.append(job_number)
                
#         for job_number in finished_jobs:
#             del self.jobs_data[job_number]
            
#     def history(self, *args):
#         if not args :
#             for number, command in enumerate(self.history_data):
#                 print(f"{number + 1} {command}")
                
#         elif args[0] == "-r":
#             path = args[1]
#             with open(path) as file:
#                 for line in file:
#                     line = line.rstrip("\n")
#                     if line:
#                         self.history_data.append(line)
#         elif args[0] == "-w":
#             path = args[1]
#             with open(path, "w") as file:
#                 for command in self.history_data:
#                     file.write(command + "\n")
#         elif args[0] == "-a":
#             path = args[1]
#             with open(path, "a") as file:
#                 for command in self.history_data[self.last_append_index:]:
#                     file.write(command + "\n")
#             self.last_append_index = len(self.history_data)
            
#         else:
#             number = int(args[0])
#             recent_history = self.history_data[-number:]
#             start = len(self.history_data) - number + 1
#             for i, command in enumerate(recent_history, start=start):
#                 print(f"{i} {command}")
            
#     def declare(self, *args):

#         if args[0] == "-p":
#             if args[1] in self.variables:
#                 print(f'declare -- {args[1]}="{self.variables[args[1]]}"')
#             else:
#                 print(f"declare: {args[1]}: not found")

#         else:
#             name, value = args[0].split("=")
#             if re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", name):
#                 self.variables[name] = value
#             else:
#                 print(f"declare: `{args[0]}': not a valid identifier")

#     def expand_variables(self, parts):
#         excpanded=[]
        
#         for part in parts:
             
#             part = re.sub(
#                         r"\$\{([a-zA-Z_][a-zA-Z0-9_]*)\}|\$([a-zA-Z_][a-zA-Z0-9_]*)",
#                         lambda match: self.variables.get(match.group(1) or match.group(2), ""),
#                         part
#                     )            
#             if part != "":
#                 excpanded.append(part)
    
#         return excpanded
#     def run_background(self, command, args, original_command):
#         process = subprocess.Popen([command, *args[:-1]])
        
#         if not self.jobs_data:
#             job_number = 1
#         else:
#             job_number = max(self.jobs_data.keys()) + 1
        
#         self.jobs_data[job_number] = {
#             "process": process,
#             "pid": process.pid,
#             "command": original_command,
#             "status": "running"
#         }
        
        
#         return f"[{job_number}] {process.pid}"

#     def complete(self, *args):
#         if args[0] == "-C":
#             valu = args[1]
#             key = args[2]
#             self.completions[key] = valu
#         elif args[0] == "-p":
#                 if args[1] in self.completions:
#                     return f"complete -C '{self.completions[args[1]]}' {args[1]}\n"
#                 else:
#                     return f"complete: {args[1]}: no completion specification\n"
#         elif args[0] == "-r":
#             self.completions.pop(args[1], None)
    
#     def run_pipeline(self, parts):
        
#         commands = []
#         current = []
#         for part in parts:
#             if part == "|":
#                 commands.append(current)
#                 current = []
#             else:
#                 current.append(part)
#         commands.append(current)
        
#         processes = []
#         previous_pipe = None
        
#         for i,command_parts in enumerate(commands):
            
#             command = command_parts[0]
#             args = command_parts[1:]
            
#             if command not in self.builtin_commands:
#                 full_path = self.find_executable(command)
#             else:
#                 full_path = None
#             if i == 0:
#                 r , w = os.pipe()
                
#                 if command in self.builtin_commands:
#                     result = self.commands[command](*args)
#                     if result is not None:
#                         data  = result.encode()
#                         os.write(w, data)                
#                 else:
#                     process = subprocess.Popen(
#                         [command, *args],
#                         executable=full_path,
#                         stdout=w,
#                     )
#                     processes.append(process)
#                 os.close(w)
#                 previous_pipe = r
                    
            
#             elif i == len(commands) - 1:
                
#                 if command in self.builtin_commands:
#                     result = self.commands[command](*args)
                    
#                     if result is not None:
#                         sys.stdout.write(result)
#                         sys.stdout.flush()

#                 else:
#                     process = subprocess.Popen(
#                         [command, *args],
#                         stdin=previous_pipe,
#                         executable=full_path,
#                         text=True,
#                     )
#                     processes.append(process)
                    
#                 if previous_pipe is not None:
#                     os.close(previous_pipe)
#             else:
#                 r , w = os.pipe()
                
#                 if command in self.builtin_commands:
#                     result = self.commands[command](*args)
                    
#                     if result is not None:
#                         data = result.encode()
#                         os.write(w, data)
 
#                 else:
#                     process = subprocess.Popen(
#                         [command, *args],
#                         executable=full_path,
#                         stdin=previous_pipe,
#                         stdout=w,
#                     )
#                     processes.append(process)
                    
#                 os.close(previous_pipe)
#                 os.close(w)
#                 previous_pipe = r
                
#         for process in processes:
#             process.wait()
            
#     def run_not_found(self, command, *args, capture=False):
        
#         full_path = self.find_executable(command)

#         if full_path:
#             if capture:
#                 result = subprocess.run(
#                     [command, *args],
#                     executable=full_path,
#                     capture_output=True,
#                     text=True,
#                 )
#                 return result.stdout, result.stderr

#             subprocess.run([command, *args],
#                             executable=full_path)
#             return None

#         if capture:
#             return "", f"{command}: command not found\n"

#         print(f"{command}: command not found")
#         return ""
import os
import re
import sys
import subprocess
import readline


class Shell:
    builtin_commands = [
        "echo",
        "exit",
        "type",
        "pwd",
        "cd",
        "complete",
        "jobs",
        "history",
        "declare",
    ]

    redirect_symbols = [">", "1>", "2>", ">>", "1>>", "2>>"]

    def __init__(self):
        self.completions = {}
        self.jobs_data = {}
        self.history_data = []
        self.last_append_index = 0
        self.variables = {}

        self.histfile = os.environ.get("HISTFILE")
        self._load_history()

        self.commands = {
            "exit": self.exit,
            "echo": self.echo,
            "pwd": self.pwd,
            "cd": self.cd,
            "type": self.type,
            "complete": self.complete,
            "jobs": self.jobs,
            "history": self.history,
            "declare": self.declare,
        }

    # =========================================================
    # Main loop
    # =========================================================

    def run(self):
        while True:
            self.reap_jobs()

            try:
                user_input = input("$ ")
            except EOFError:
                break

            if not user_input.strip():
                continue

            self.history_data.append(user_input)
            self.execute_line(user_input)

    def execute_line(self, user_input):
        parts = self.parse_input(user_input)

        if not parts:
            return

        parts = self.expand_variables(parts)

        if "|" in parts:
            self.run_pipeline(parts)
            return

        command = parts[0]
        args = parts[1:]

        if args and args[-1] == "&":
            print(self.run_background(command, args, user_input))
            return

        if self._handle_redirection(command, args):
            return

        self._execute_command(command, args)

    def _execute_command(self, command, args):
        if command in self.commands:
            result = self.commands[command](*args)

            if result is not None:
                sys.stdout.write(result)
        else:
            self.run_not_found(command, *args)

    # =========================================================
    # Redirection
    # =========================================================

    def _handle_redirection(self, command, args):
        for symbol in self.redirect_symbols:
            if symbol in args:
                idx = args.index(symbol)
                file_name = args[idx + 1]
                real_args = args[:idx]

                self.redirect(
                    command,
                    real_args,
                    file_name,
                    symbol,
                )
                return True

        return False

    def redirect(self, command, real_args, file_name, symbol):
        directory = os.path.dirname(file_name)

        if directory:
            os.makedirs(directory, exist_ok=True)

        output, error = self._run_for_redirection(
            command,
            real_args,
        )

        if symbol in [">", "1>"]:
            self._redirect_stdout(
                file_name,
                output,
                append=False,
            )

            if error:
                sys.stderr.write(error)

        elif symbol in [">>", "1>>"]:
            self._redirect_stdout(
                file_name,
                output,
                append=True,
            )

            if error:
                sys.stderr.write(error)

        elif symbol == "2>":
            if output:
                sys.stdout.write(output)

            self._redirect_stderr(
                file_name,
                error,
                append=False,
            )

        elif symbol == "2>>":
            if output:
                sys.stdout.write(output)

            self._redirect_stderr(
                file_name,
                error,
                append=True,
            )

    def _run_for_redirection(self, command, args):
        if command in self.commands:
            output = self.commands[command](*args)
            return output, ""

        return self.run_not_found(
            command,
            *args,
            capture=True,
        )

    def _redirect_stdout(self, file_name, output, append):
        mode = "a" if append else "w"

        with open(file_name, mode) as file:
            if output:
                file.write(output)

    def _redirect_stderr(self, file_name, error, append):
        mode = "a" if append else "w"

        with open(file_name, mode) as file:
            if error:
                file.write(error)

    # =========================================================
    # PATH / External commands
    # =========================================================

    def find_executable(self, command):
        path = os.environ.get("PATH", "")
        paths = path.split(os.pathsep)

        for directory in paths:
            full_path = os.path.join(directory, command)

            if (
                os.path.isfile(full_path)
                and os.access(full_path, os.X_OK)
            ):
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
                if not file_name.startswith(perfix):
                    continue

                full_path = os.path.join(path, file_name)

                if (
                    os.path.isfile(full_path)
                    and os.access(full_path, os.X_OK)
                    and file_name not in matches
                ):
                    matches.append(file_name)

        return matches

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

            subprocess.run(
                [command, *args],
                executable=full_path,
            )

            return None

        if capture:
            return "", f"{command}: command not found\n"

        print(f"{command}: command not found")
        return ""

    # =========================================================
    # Autocomplete
    # =========================================================

    def find_matches(self, text, args):
        if args:
            return self._find_argument_matches(args[-1])

        return self._find_command_matches(text)

    def _find_argument_matches(self, text):
        if "/" in text:
            return self.find_file_by_path(text)

        return self.find_entry_by_prefix(text)

    def _find_command_matches(self, text):
        matches = []

        if text == "":
            return self.find_entry_by_prefix("")

        for command in self.builtin_commands:
            if command.startswith(text):
                matches.append(command)

        external_commands = self.find_executable_by_prefix(text)

        for command in external_commands:
            if command not in matches:
                matches.append(command)

        return matches

    def autocomplete(self, text, state):
        line = readline.get_line_buffer()
        command, *args = line.split()

        comp_line = line
        comp_point = str(len(comp_line))

        if command in self.completions:
            matches = self._run_custom_completion(
                command,
                args,
                text,
                comp_line,
                comp_point,
            )
        else:
            matches = self.find_matches(text, args)

        if state < len(matches):
            match = matches[state]

            if match.endswith("/"):
                return match

            if len(matches) == 1:
                return match + " "

            return match

        return None

    def _run_custom_completion(
        self,
        command,
        args,
        text,
        comp_line,
        comp_point,
    ):
        full_path = self.completions[command]

        if len(args) < 2:
            previous = command
        else:
            previous = args[-2]

        result = subprocess.run(
            [
                full_path,
                command,
                text,
                previous,
            ],
            capture_output=True,
            text=True,
            env={
                "COMP_LINE": comp_line,
                "COMP_POINT": comp_point,
            },
        )

        return result.stdout.split()

    def display_matches(
        self,
        user_input,
        matches,
        longest_match_length,
    ):
        sys.stdout.write("\r\n")
        sys.stdout.write(" ".join(sorted(matches)))
        sys.stdout.write(
            "\r\n$ " + readline.get_line_buffer()
        )
        sys.stdout.flush()

    def find_entry_by_prefix(self, perfix):
        matches = []
        path = os.getcwd()

        for entry in os.listdir(path):
            if not entry.startswith(perfix):
                continue

            full_path = os.path.join(path, entry)

            if os.path.isdir(full_path):
                entry = entry + "/"

            if entry not in matches:
                matches.append(entry)

        return matches

    def find_file_by_path(self, text):
        matches = []

        idx = text.rfind("/")
        directory = text[:idx]
        file_name = text[idx + 1:]
        prefix = text[:idx + 1]

        for entry in os.listdir(directory):
            if not entry.startswith(file_name):
                continue

            full_path = os.path.join(directory, entry)

            if os.path.isdir(full_path):
                entry_name = prefix + entry + "/"
            else:
                entry_name = prefix + entry

            if entry_name not in matches:
                matches.append(entry_name)

        return matches

    # =========================================================
    # Parser
    # =========================================================

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
                    if (
                        i + 1 < len(text)
                        and text[i + 1] in ['"', "\\"]
                    ):
                        escape_next = True
                    else:
                        word += char

                else:
                    escape_next = True

                continue

            if char == "'" and not in_double_quotes:
                in_single_quotes = not in_single_quotes

            elif char == '"' and not in_single_quotes:
                in_double_quotes = not in_double_quotes

            elif (
                char.isspace()
                and not in_single_quotes
                and not in_double_quotes
            ):
                if word:
                    args.append(word)
                    word = ""

            else:
                word += char

        if word:
            args.append(word)

        return args

    # =========================================================
    # Variables
    # =========================================================

    def expand_variables(self, parts):
        expanded = []

        for part in parts:
            part = re.sub(
                r"\$\{([a-zA-Z_][a-zA-Z0-9_]*)\}"
                r"|\$([a-zA-Z_][a-zA-Z0-9_]*)",
                lambda match: self.variables.get(
                    match.group(1) or match.group(2),
                    "",
                ),
                part,
            )

            if part != "":
                expanded.append(part)

        return expanded

    def declare(self, *args):
        if args[0] == "-p":
            if args[1] in self.variables:
                print(
                    f'declare -- {args[1]}='
                    f'"{self.variables[args[1]]}"'
                )
            else:
                print(
                    f"declare: {args[1]}: not found"
                )

            return

        name, value = args[0].split("=")

        if re.match(
            r"^[a-zA-Z_][a-zA-Z0-9_]*$",
            name,
        ):
            self.variables[name] = value
        else:
            print(
                f"declare: `{args[0]}': "
                f"not a valid identifier"
            )

    # =========================================================
    # Built-in commands
    # =========================================================

    def pwd(self):
        result = os.getcwd()
        return result + "\n"

    def exit(self):
        if self.histfile:
            self._write_history_file(
                self.histfile,
                self.history_data,
            )

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
            print(
                f"cd: {args[0]}: "
                f"No such file or directory"
            )

    def type(self, *args):
        if args[0] in self.builtin_commands:
            return f"{args[0]} is a shell builtin\n"

        full_path = self.find_executable(args[0])

        if full_path:
            return f"{args[0]} is {full_path}\n"

        return f"{args[0]}: not found\n"

    # =========================================================
    # History
    # =========================================================

    def _load_history(self):
        if not self.histfile:
            return

        with open(self.histfile) as file:
            for line in file:
                line = line.rstrip("\n")

                if line:
                    self.history_data.append(line)

        self.last_append_index = len(
            self.history_data
        )

    def history(self, *args):
        if not args:
            self._print_full_history()

        elif args[0] == "-r":
            self._read_history_file(args[1])

        elif args[0] == "-w":
            self._write_history_file(
                args[1],
                self.history_data,
            )

        elif args[0] == "-a":
            self._append_history_file(args[1])

        else:
            self._print_recent_history(
                int(args[0])
            )

    def _print_full_history(self):
        for number, command in enumerate(
            self.history_data,
            start=1,
        ):
            print(f"{number} {command}")

    def _read_history_file(self, path):
        with open(path) as file:
            for line in file:
                line = line.rstrip("\n")

                if line:
                    self.history_data.append(line)

    def _write_history_file(self, path, history):
        with open(path, "w") as file:
            for command in history:
                file.write(command + "\n")

    def _append_history_file(self, path):
        with open(path, "a") as file:
            for command in self.history_data[
                self.last_append_index:
            ]:
                file.write(command + "\n")

        self.last_append_index = len(
            self.history_data
        )

    def _print_recent_history(self, number):
        recent_history = self.history_data[-number:]
        start = len(self.history_data) - number + 1

        for index, command in enumerate(
            recent_history,
            start=start,
        ):
            print(f"{index} {command}")

    # =========================================================
    # Jobs
    # =========================================================

    def run_background(
        self,
        command,
        args,
        original_command,
    ):
        process = subprocess.Popen(
            [command, *args[:-1]]
        )

        if not self.jobs_data:
            job_number = 1
        else:
            job_number = max(
                self.jobs_data.keys()
            ) + 1

        self.jobs_data[job_number] = {
            "process": process,
            "pid": process.pid,
            "command": original_command,
            "status": "running",
        }

        return f"[{job_number}] {process.pid}"

    def reap_jobs(self):
        job_numbers = list(
            self.jobs_data.keys()
        )

        finished_jobs = []

        for job_number, data in self.jobs_data.items():
            if data["process"].poll() is not None:
                self.print_done_job(
                    job_number,
                    data,
                    job_numbers,
                )

                finished_jobs.append(job_number)

        for job_number in finished_jobs:
            del self.jobs_data[job_number]

    def jobs(self):
        job_numbers = list(
            self.jobs_data.keys()
        )

        finished_jobs = []

        for job_number, data in self.jobs_data.items():
            if data["process"].poll() is None:
                self._print_running_job(
                    job_number,
                    data,
                    job_numbers,
                )
            else:
                self.print_done_job(
                    job_number,
                    data,
                    job_numbers,
                )

                finished_jobs.append(job_number)

        for job_number in finished_jobs:
            del self.jobs_data[job_number]

    def _job_marker(self, job_number, job_numbers):
        if job_number == job_numbers[-1]:
            return "+"

        if (
            len(job_numbers) > 1
            and job_number == job_numbers[-2]
        ):
            return "-"

        return " "

    def _print_running_job(
        self,
        job_number,
        data,
        job_numbers,
    ):
        status = f"{data['status']:<24}"
        marker = self._job_marker(
            job_number,
            job_numbers,
        )

        print(
            f"[{job_number}]{marker}  "
            f"{status}{data['command']}"
        )

    def print_done_job(
        self,
        job_number,
        data,
        job_numbers,
    ):
        status = f"{'Done':<24}"
        done_command = data["command"].rstrip(" &")
        marker = self._job_marker(
            job_number,
            job_numbers,
        )

        print(
            f"[{job_number}]{marker}  "
            f"{status}{done_command}"
        )

    # =========================================================
    # Completion command
    # =========================================================

    def complete(self, *args):
        if args[0] == "-C":
            value = args[1]
            key = args[2]
            self.completions[key] = value

        elif args[0] == "-p":
            if args[1] in self.completions:
                return (
                    f"complete -C "
                    f"'{self.completions[args[1]]}' "
                    f"{args[1]}\n"
                )

            return (
                f"complete: {args[1]}: "
                f"no completion specification\n"
            )

        elif args[0] == "-r":
            self.completions.pop(
                args[1],
                None,
            )

    # =========================================================
    # Pipeline
    # =========================================================

    def run_pipeline(self, parts):
        commands = self._split_pipeline(parts)

        processes = []
        previous_pipe = None

        for i, command_parts in enumerate(commands):
            command = command_parts[0]
            args = command_parts[1:]

            if i == 0:
                previous_pipe = (
                    self._run_first_pipeline_command(
                        command,
                        args,
                        processes,
                    )
                )

            elif i == len(commands) - 1:
                self._run_last_pipeline_command(
                    command,
                    args,
                    previous_pipe,
                    processes,
                )

                if previous_pipe is not None:
                    os.close(previous_pipe)

            else:
                previous_pipe = (
                    self._run_middle_pipeline_command(
                        command,
                        args,
                        previous_pipe,
                        processes,
                    )
                )

        for process in processes:
            process.wait()

    def _split_pipeline(self, parts):
        commands = []
        current = []

        for part in parts:
            if part == "|":
                commands.append(current)
                current = []
            else:
                current.append(part)

        commands.append(current)

        return commands

    def _run_first_pipeline_command(
        self,
        command,
        args,
        processes,
    ):
        read_pipe, write_pipe = os.pipe()

        if command in self.builtin_commands:
            result = self.commands[command](*args)

            if result is not None:
                os.write(
                    write_pipe,
                    result.encode(),
                )
        else:
            full_path = self.find_executable(command)

            process = subprocess.Popen(
                [command, *args],
                executable=full_path,
                stdout=write_pipe,
            )

            processes.append(process)

        os.close(write_pipe)

        return read_pipe

    def _run_middle_pipeline_command(
        self,
        command,
        args,
        previous_pipe,
        processes,
    ):
        read_pipe, write_pipe = os.pipe()

        if command in self.builtin_commands:
            result = self.commands[command](*args)

            if result is not None:
                os.write(
                    write_pipe,
                    result.encode(),
                )
        else:
            full_path = self.find_executable(command)

            process = subprocess.Popen(
                [command, *args],
                executable=full_path,
                stdin=previous_pipe,
                stdout=write_pipe,
            )

            processes.append(process)

        os.close(previous_pipe)
        os.close(write_pipe)

        return read_pipe

    def _run_last_pipeline_command(
        self,
        command,
        args,
        previous_pipe,
        processes,
    ):
        if command in self.builtin_commands:
            result = self.commands[command](*args)

            if result is not None:
                sys.stdout.write(result)
                sys.stdout.flush()

            return

        full_path = self.find_executable(command)

        process = subprocess.Popen(
            [command, *args],
            executable=full_path,
            stdin=previous_pipe,
            text=True,
        )

        processes.append(process)