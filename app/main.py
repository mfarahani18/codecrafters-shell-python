from app.shell import Shell
import sys


def main():
    my_shell = Shell()
    while True:
        sys.stdout.write("$ ")
        user_input = input()
        parts = my_shell.parse_input(user_input)
        command = parts[0]
        args = parts[1:]
        
        redirected = False

        redirect_symbols = [">", "1>"]
        for symbol in redirect_symbols:
            if symbol in args:
                idx = args.index(symbol)
                file_name = args[idx + 1]
                real_args = args[:idx]
                my_shell.redirect(command, real_args, file_name)
                redirected = True
                break

        if redirected:
            continue

        if command in my_shell.commands:
            result = my_shell.commands[command](*args)

            if result is not None:
                print(result)
        else:
            my_shell.run_not_found(command, *args)


if __name__ == "__main__":
    main()