from app.shell import Shell
import readline
import subprocess
import sys


def main():
    my_shell = Shell()

    readline.set_completer(my_shell.autocomplete)
    readline.parse_and_bind("tab: complete")
    readline.set_completer_delims(" \t\n")
    readline.set_completion_display_matches_hook(my_shell.display_matches)

    while True:

        # try:
        #     user_input = input("$ ")
        # except EOFError:
        #     break
        # if not user_input.strip():
        #     continue
        sys.stdout.write("$ ")
        user_input = input()
        parts = my_shell.parse_input(user_input)
        command = parts[0]
        args = parts[1:]

        if args[-1] == "&":
            process = subprocess.Popen([command, *args[:-1]])
            print(process.pid)
            
        redirected = False

        redirect_symbols = [">", "1>", "2>", ">>", "1>>", "2>>"]
        for symbol in redirect_symbols:
            if symbol in args:
                idx = args.index(symbol)
                file_name = args[idx + 1]
                real_args = args[:idx]
                my_shell.redirect(command, real_args, file_name, symbol)
                redirected = True
                break

        if redirected:
            continue

        if command in my_shell.commands:
            result = my_shell.commands[command](*args)
            if result is not None:
                sys.stdout.write(result)
        else:
            my_shell.run_not_found(command, *args)



if __name__ == "__main__":
    main()
