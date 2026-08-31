from app.shell import Shell
import sys
import os
import subprocess


def main():

    
    
    my_shell = Shell()
    while True:
        sys.stdout.write("$ ")
        user_input = input()
        parts = my_shell.parse_input(user_input)
        command = parts[0]
        args = parts[1:]
        result = None
        if command in my_shell.commands:
            result = my_shell.commands[command](*args)
        else:
            my_shell.run_not_found(command, *args)
            
        if ">" in args and result:
            idx = args.index(">")
            file_name = args[idx + 1]
            real_args = args[:idx]
            print(f"Redirecting output of command '{command}' to file '{file_name}'")
            my_shell.redirect(command, real_args, file_name)
        elif result:
            print(result)




if __name__ == "__main__":
    main()
