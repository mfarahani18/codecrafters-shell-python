import os
import sys

class Shell():

     builtin_commands = ["echo", "exit", "type", "pwd", "cd"]

     def pwd(self):
          return os.getcwd()
     
     def exit(self):
          sys.exit()

     def echo(self, *args):
          return " ".join(args)

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
                print(f"{args[0]} is a shell builtin")

          else:
               y = os.environ["PATH"]
               z = y.split(os.pathsep)

               found = False

               for i in z:
                    full_path = os.path.join(i, args[0])

                    if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                         print(f"{args[0]} is {full_path}")
                         found = True
                         break

               if found == False:  # if not found
                    print(f"{args[0]}: not found")

     def run_not_found(self, command, *args):
         y = os.environ["PATH"]
         z = y.split(os.pathsep)

         found = False

         for i in z:
             full_path = os.path.join(i, command)

             if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                 subprocess.run([command] + args, executable=full_path)

                 found = True
                 break

         if found == False:  # if not found
             print(f"{command}: command not found")
