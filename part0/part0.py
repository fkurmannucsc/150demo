import argparse
import sys

# CommandLine
""" Handle the command line arguments. """
class CommandLine():
  """ Constructor implements an arg parser to interpret the command line argv string using argparse. """
  def __init__(self, inOpts=None):
    self.parser = argparse.ArgumentParser(
      description = 'CSE 150 Final', 
      epilog = '', 
      add_help = True,
      prefix_chars = '-', 
      usage = 'python3 part0.py -p [PORT] -d [DIRECTORY]' 
    )
    
    self.parser.add_argument('-p', '--port', type=int, action = 'store', help='Port number')
    self.parser.add_argument('-d', '--directory', action = 'store', help='Absolute path to directory')

    if inOpts is None :
      self.args = self.parser.parse_args()
    else :
      self.args = self.parser.parse_args(inOpts)

class Interface():
  def __init__(self, port, directory):
    self.portNumber = port
    self.directory = directory

  def evaluatePort(self):
    if self.portNumber == 80:
      print("{port} {path}".format(port=self.portNumber, path=self.directory))
    elif (self.portNumber >= 0 and self.portNumber < 1024):
      print("Well-known port number {port} entered - could cause a conflict.\n{port} {directory}".format(port=self.portNumber, directory=self.directory))
    elif (self.portNumber > 1023 and self.portNumber < 49152):
      print("Registered port number {port} entered - could cause a conflict.\n{port} {directory}".format(port=self.portNumber, directory=self.directory))
    else:
      print("Terminating program, port number is not allowed.", file=sys.stderr)
      return 1
    return 0

# Main
""" Main method, parse input and call evaluation function. """
def main(args = None):
  # Get commands
  if args == None:
    commandInput = CommandLine()
  else:
    commandInput = CommandLine(args)

  # Greate Interface object
  interface = Interface(commandInput.args.port, commandInput.args.directory)

  # Search for port numbers
  try: 
    output = interface.evaluatePort()
    return output
  except:
    print("Invalid arguments provided, please provide both a port and directory.", file=sys.stderr)
    return 1

if __name__ == "__main__":
 main()