import sys


def main():
    # TODO: Uncomment the code below to pass the first stage
    builtin_commands = ["echo", "exit", "type"]
    while True:
        sys.stdout.write("$ ")
        command = input()
        if command == "exit":
            sys.exit() #or break
        elif command[0:5] == "echo ":
            print(command[5:])
        elif command[0:5] == "type ":
            x = command.split()
            if x[1] in builtin_commands:
                print(f"{x[1]} is a shell builtin")
            else:
                print(f"{command[5:]}: command not found")
        else:
            print(f"{command}: command not found")

        


if __name__ == "__main__":
    main()
