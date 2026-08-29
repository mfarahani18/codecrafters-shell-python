from app.shell import Shell
import sys
import os
import subprocess

def main():

    my_shell = Shell()

    commands = {
    "exit": lambda : my_shell.exit(),
    "echo": lambda *args : print(my_shell.echo(*args)),
    "pwd": lambda : print(my_shell.pwd()),
    "cd": lambda *args: my_shell.cd(*args),
    "type": lambda *args: my_shell.type(*args),
    }


    while True:
        sys.stdout.write("$ ")
        parts = my_shell.parse_input(user_input)
        command = parts[0]
        args = parts[1:]

        if command in commands:
            commands[command](*args)
        else:
            my_shell.run_not_found(command, *args)


if __name__ == "__main__":
    main()