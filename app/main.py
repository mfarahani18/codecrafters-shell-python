from app.shell import Shell
import readline
import subprocess
import sys
import io


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
        my_shell.reap_jobs()
        sys.stdout.write("$ ")
        user_input = input()
        parts = my_shell.parse_input(user_input)
        
        if "|" in parts:
            idx = parts.index("|")
            left = parts[:idx]
            right = parts[idx + 1:]
            
            command = left[0]
            args = left[1:]
            
            right_command = right[0]
            right_args = right[1:]
            
            if command in my_shell.builtin_commands:
                result = my_shell.commands[command](*args)
                
                process2 = subprocess.Popen(
                    [right_command, *right_args],
                    stdin=subprocess.PIPE,
                    text=True,
                )
                
                process2.communicate(input=result)
                
            else:
                if right_command in my_shell.commands:
                    result = my_shell.commands[command](*args)
                    process2 = subprocess.Popen(
                        [right_command, *right_args],
                        stdin=subprocess.PIPE,
                        text=True,
                    )
                    
                    process2.communicate(input=result)
                    
                else:
                    process1 = subprocess.Popen(
                        [command, *args],
                        stdout=subprocess.PIPE,
                        text=True,
                    )
                
                    process2 = subprocess.Popen(
                        [right_command, *right_args],
                        stdin=process1.stdout,
                        text=True,
                    )
                    
                    process1.stdout.close()
                    process1.wait()
                    
            continue
                
            
        command = parts[0]
        args = parts[1:]

        if args and args[-1] == "&":
            print(my_shell.run_background(command, args, user_input))
            continue
        
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
