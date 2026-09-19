# Python Shell

A lightweight Unix-like shell implemented in Python.

This project is an educational shell implementation developed to understand how command-line interpreters work internally, including command parsing, built-in commands, external command execution, pipelines, redirections, background jobs, command history, variables, and tab completion.

The project has been developed incrementally through the CodeCrafters Shell challenge, with a focus on understanding the underlying mechanisms rather than relying on high-level shell libraries.

---

## Features

### Built-in Commands

The shell currently supports the following built-in commands:

* `echo`
* `exit`
* `pwd`
* `cd`
* `type`
* `history`
* `declare`
* `complete`
* `jobs`

Example:

```bash
$ echo Hello World
Hello World

$ pwd
/home/user/project

$ cd /tmp

$ type echo
echo is a shell builtin
```

---

## External Commands

Commands that are not built into the shell are searched for in the system `PATH`.

For example:

```bash
$ ls
$ cat file.txt
$ grep hello file.txt
```

The shell searches the directories listed in `PATH` and executes the corresponding executable when found.

Executable extensions such as:

```text
.exe
.cmd
.bat
```

are also considered.

If a command cannot be found:

```bash
$ unknown-command
unknown-command: command not found
```

---

## Command Parsing

The shell contains its own command parser instead of relying on Python's `split()`.

It supports:

* whitespace separation
* single quotes
* double quotes
* escaping
* escaped characters inside double quotes

Examples:

```bash
$ echo hello world
hello world

$ echo "hello world"
hello world

$ echo 'hello world'
hello world

$ echo hello\ world
hello world
```

The parser keeps quoted text together as a single argument.

---

## Environment and Shell Variables

The shell supports shell variables through the `declare` command.

Example:

```bash
$ declare name=John
$ echo $name
John
```

Brace-style expansion is also supported:

```bash
$ echo ${name}
John
```

Undefined variables expand to an empty string.

```bash
$ echo $unknown

```

Variable names follow the standard identifier pattern:

```text
[a-zA-Z_][a-zA-Z0-9_]*
```

---

## Pipelines

Multiple commands can be connected using `|`.

Example:

```bash
$ echo hello | cat
hello
```

Multiple pipeline stages are supported:

```bash
$ command1 | command2 | command3
```

The implementation uses operating-system pipes through Python's `os.pipe()` and connects processes using `subprocess.Popen()`.

Built-in commands can also participate in pipelines.

---

## Output Redirection

The shell supports standard output and error redirection.

### Overwrite output

```bash
$ echo hello > output.txt
```

### Explicit stdout redirection

```bash
$ echo hello 1> output.txt
```

### Append output

```bash
$ echo hello >> output.txt
```

### Explicit stdout append

```bash
$ echo hello 1>> output.txt
```

### Redirect stderr

```bash
$ command 2> error.txt
```

### Append stderr

```bash
$ command 2>> error.txt
```

Parent directories are automatically created when necessary.

For example:

```bash
$ echo hello > logs/output.txt
```

will create the `logs` directory if it does not already exist.

---

## Background Processes

Commands can be executed in the background using `&`.

Example:

```bash
$ sleep 10 &
[1] 12345
```

The shell keeps track of background processes and assigns each process a job number.

---

## Job Management

The `jobs` command displays active and completed background jobs.

Example:

```bash
$ jobs
[1]+  running                 sleep 10 &
```

Completed jobs are detected automatically when the shell checks for finished processes.

The shell also displays completion information such as:

```text
[1]+  Done                    sleep 10
```

Job markers are maintained for the most recent jobs.

---

## Command History

The shell keeps track of commands entered during the session.

Running:

```bash
$ history
```

prints the command history:

```text
1 echo hello
2 pwd
3 ls
```

The shell also supports displaying a specific number of recent commands:

```bash
$ history 5
```

### Read history from a file

```bash
$ history -r history.txt
```

### Write history to a file

```bash
$ history -w history.txt
```

### Append new history entries

```bash
$ history -a history.txt
```

---

## Persistent History

If the `HISTFILE` environment variable is set, the shell loads history from that file when starting.

Example:

```bash
export HISTFILE=/tmp/shell_history
```

When the shell exits, the current history is written back to the configured history file.

---

## Up-Arrow History Navigation

The shell integrates with Python's `readline` module.

This provides command-line editing and history navigation through the terminal.

For example:

```text
↑
```

can be used to navigate through previously entered commands.

---

## Tab Completion

The shell provides command and file completion through `readline`.

Pressing:

```text
Tab
```

can complete:

* built-in commands
* executable commands found in `PATH`
* files
* directories

Examples:

```bash
$ ec<Tab>
echo
```

Directory completion is represented with `/`:

```bash
$ cd Doc<Tab>
Documents/
```

Path-based completion is also supported:

```bash
$ cat src/ma<Tab>
src/main.py
```

---

## Custom Command Completion

The shell supports registering external completion programs using:

```bash
complete -C <completion-program> <command>
```

For example:

```bash
$ complete -C /path/to/completer mycommand
```

The completion configuration can be inspected with:

```bash
$ complete -p mycommand
```

and removed with:

```bash
$ complete -r mycommand
```

The completion process receives completion information through:

```text
COMP_LINE
COMP_POINT
```

---

## Project Structure

A simplified project structure looks like this:

```text
.
├── app/
│   ├── __init__.py
│   └── shell.py
│
├── main.py
├── your_program.sh
└── README.md
```

### `main.py`

Responsible for starting the shell and configuring `readline`.

```text
main.py
   │
   └── Shell.run()
```

### `shell.py`

Contains the main shell implementation, including:

```text
Shell
├── Main loop
├── Command execution
├── Command parser
├── Variable expansion
├── Built-in commands
├── PATH lookup
├── Pipelines
├── Redirections
├── Background jobs
├── History
├── Tab completion
└── Custom completion
```

---

## Architecture

The shell follows a simple command-processing pipeline:

```text
User Input
    │
    ▼
parse_input()
    │
    ▼
expand_variables()
    │
    ├───────────────┐
    │               │
    ▼               ▼
Pipeline?       Normal command
    │               │
    ▼               ├── Background?
run_pipeline()      │
                    ├── Redirection?
                    │
                    ▼
              Execute command
                    │
             ┌──────┴──────┐
             ▼             ▼
          Built-in      External
                         command
```

The implementation intentionally keeps the core shell logic inside the `Shell` class while separating different responsibilities into focused methods.

---

## Technologies

The project is implemented using Python and relies primarily on the standard library.

Main modules:

* `os`
* `sys`
* `re`
* `subprocess`
* `readline`

No external shell framework is required.

---

## Running the Shell

Make sure Python is installed:

```bash
python3 --version
```

Then run:

```bash
python3 main.py
```

Or, if the project provides an executable script:

```bash
./your_program.sh
```

You should see:

```text
$ 
```

The shell is now ready to accept commands.

---

## Example Session

```text
$ echo Hello World
Hello World

$ pwd
/home/user/shell

$ declare name=Python

$ echo Hello $name
Hello Python

$ echo apple | cat
apple

$ echo test > output.txt

$ cat output.txt
test

$ sleep 5 &
[1] 12345

$ jobs
[1]+  running                 sleep 5 &
```

---

## Design Goals

The main goals of this project are:

1. Understand how a shell processes user input.
2. Implement command parsing manually.
3. Understand how `PATH` is used to locate executables.
4. Learn how processes are created and managed.
5. Understand Unix pipes and input/output redirection.
6. Implement background process management.
7. Implement persistent command history.
8. Understand terminal command completion.
9. Keep the implementation readable and maintainable.
10. Refactor the code without changing existing shell behavior.

---

## Refactoring Approach

The code is structured around a simple principle:

> Improve the internal structure without changing the externally observable behavior.

For example, the main program is intentionally kept small:

```python
shell = Shell()
shell.run()
```

while command processing is handled by the `Shell` class.

Large responsibilities are divided into focused methods such as:

```text
_execute_command()
_handle_redirection()
_run_custom_completion()
_print_full_history()
_append_history_file()
_job_marker()
_split_pipeline()
_run_first_pipeline_command()
_run_middle_pipeline_command()
_run_last_pipeline_command()
```

This makes the implementation easier to read, debug, test, and extend.

---

## Testing

The project is developed incrementally and tested against the CodeCrafters Shell stages.

The implementation covers shell functionality including:

* command execution
* built-in commands
* `PATH` lookup
* quoting and escaping
* pipelines
* redirections
* background processes
* jobs
* history
* variables
* tab completion
* custom completion

When modifying the shell, existing behavior should be preserved and the CodeCrafters test suite should be run again.

---

## Future Improvements

Possible future improvements include:

* more complete shell syntax parsing
* improved error handling
* additional redirection types
* environment-variable support
* improved process/job control
* more advanced command completion
* improved quoting and escaping rules
* automated unit tests
* further separation of shell components

These improvements can be introduced incrementally while keeping the current functionality stable.

---

## License

This project is intended primarily as an educational project for learning shell internals, Python process management, command parsing, and software engineering practices.
