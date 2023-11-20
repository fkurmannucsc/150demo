import argparse
import socket
import sys 
import os


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
    
    self.parser.add_argument('-p', '--port', type=int, default=80, action = 'store', help='Port number')
    self.parser.add_argument('-d', '--directory', action = 'store', help='Absolute path to directory')

    if inOpts is None :
      self.args = self.parser.parse_args()
    else :
      self.args = self.parser.parse_args(inOpts)

class Interface():
  def __init__(self, port, directory):
    self.portNumber = port
    self.directory = directory
    self.responses = {
      200: 'OK', 
      404: 'File Not Found', 
      501: 'Not Implemented', 
      505: 'HTTP Version Not Supported',
    }

  def evaluatePort(self):
    if self.portNumber == 80:
      print("{port} {path}".format(port=self.portNumber, path=self.directory))
    elif self.portNumber > 0 and self.portNumber < 1024:
      print("Well known port number {port} entered - could cause a conflict.\n\n{directory}".format(port=self.portNumber, directory=self.directory))
    elif self.portNumber < 49152:
      print("Registered port number {port} entered - could cause a conflict.\n\n{directory}".format(port=self.portNumber, directory=self.directory))
    else:
      print("Terminating program, port number is not allowed.")
      return 1
    return 0
  
  def evaluatePath(self):
    if not os.path.isabs(self.directory):
      return 1
    return 0
  
  def socket(self):
    try: 
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
      print ("Socket successfully created")
    except socket.error as err: 
      print ("socket creation failed with error %s" %(err))
    
    # default port for socket 
    port = 80
    
    try: 
      host_ip = socket.gethostbyname('www.google.com') 
    except socket.gaierror: 
    
      # this means could not resolve the host 
      print ("there was an error resolving the host")
      sys.exit() 
    
    # connecting to the server 
    s.connect((host_ip, port)) 
    
    print ("the socket has successfully connected to google") 

# Main
""" """
def main(args = None):
  # Get commands
  if args == None:
    commandInput = CommandLine()
  else:
    commandInput = CommandLine(args)

  # Greate Interface object
  interface = Interface(commandInput.args.port, commandInput.args.directory)

  # Search for port numbers
  output = interface.evaluatePort()
  return output

if __name__ == "__main__":
 main()

'''
File Errors: Print an error message to stderr and exit the program if the absolute path
to the specified root directory (entered on the command line) does not exist.
○ Socket Errors: The socket operations should handle any errors or exceptions thrown. The
server application should continue to listen for subsequent client requests, and not crash.
An example of an error that you could experience is trying to use a port which is already
in use by some other process.'''