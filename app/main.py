import sys
import os


def main():

    builtin_commands = ["echo", "exit", "type"]

    while True:
        sys.stdout.write("$ ")

        command = input()

        if command == "exit":
            sys.exit()

        elif command[0:5] == "echo ":
            print(command[5:])

        elif command[0:5] == "type ":
            x = command.split()

            if x[1] in builtin_commands:
                print(f"{x[1]} is a shell builtin")

            else:
                y = os.environ["PATH"]
                z = y.split(os.pathsep)

                found = False

                for i in z:
                    full_path = os.path.join(i, x[1])

                    if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                        print(f"{x[1]} is {full_path}")
                        found = True
                        break

                if  found==False: #if not found
                    print(f"{command[5:]}: not found")

        else:
            print(f"{command}: command not found")


if __name__ == "__main__":
    main()