import argparse
import socket
import sys 
import os

from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime

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

""" CSV class responsible for handling every task associated with the CSV log. """
class CSV():
  def __init__(self):
    pass

""" HTTP class responsible for reading and writing the HTTP headers. """
class HTTPObject():
  def __init__(self):
    self.responses = {
      200: 'OK', 
      404: 'File Not Found', 
      501: 'Not Implemented', 
      505: 'HTTP Version Not Supported',
      'test': 'check'
    }
    self.currentTime = 'Tue, 19 Feb 2002 11:24:55 GMT'
    self.lastMod = 'Tue, 19 Feb 2002 18:06:55 GMT'
    self.length = '0'

  def makeRequest(self, file, host, agent, accept, language, encoding, charset, keepAlive, connection, body):
    templateRequest = '''GET /{file} HTTP/1.1\r
Host: {host}\r
User-Agent: {agent}\r
Accept: {accept}\r
Accept-Language: {language}\r
Accept-Encoding: {encoding}\r
Accept-Charset: {charset}\r
Keep-Alive: {keepAlive}\r
Connection: {connection}\r
\r
{body}'''.format(file=file, 
                  host=host,
                  agent=agent,
                  accept=accept,
                  language=language,
                  encoding=encoding,
                  charset=charset,
                  keepAlive=keepAlive,
                  connection=connection,
                  body=body)
    return templateRequest

  def makeResponse(self, code, server):
    templateResponse = '''HTTP/1.1 {code} {description}\r
Date: {date}\r
Server: {server}\r
Last-Modified: {lastMod}\r
Content-Length: {length}\r
Content-Type: {type}\r
\r
{body}'''.format( code=code, 
                  description=self.responses[code], 
                  date=self.currentTime, 
                  server=server, 
                  lastMod=self.lastMod,
                  length=self.length,
                  type=self.type,
                  body=self.body)
    return templateResponse
  
  def getFileData(self, path):
    # Get and store the file TODO, break up into chunks
    f = open(path+"HelloWorld.html", "r")
    self.body = f.read()
    f.close()

    # Get current time and last modified times, translate them to HTTP format
    now = datetime.now()
    stamp = mktime(now.timetuple())
    self.currentTime = format_date_time(stamp)

    lastModified = datetime.fromtimestamp(os.path.getmtime(path + "HelloWorld.html"))
    stamp = mktime(lastModified.timetuple())
    self.lastMod = format_date_time(stamp)

    # Get the size of the file
    self.length = str(os.path.getsize(path + "HelloWorld.html"))

    # Get the type of the file
    self.type = 'text/html'


""" Class responsible for error checking of inputs and for interacting with file system. """
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
      sys.exit(1)
      
    return 0
  
  def evaluatePath(self):
    if not os.path.isabs(self.directory):
      print('Directory {directory} does not exist.'.format(directory=self.directory), file=sys.stderr)
      sys.exit(1)
    return 0
  
  # def socket(self):
  #   try: 
  #     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
  #     print ("Socket successfully created")
  #   except socket.error as err: 
  #     print ("socket creation failed with error %s" %(err))
    
  #   # default port for socket 
  #   port = 80
    
  #   try: 
  #     host_ip = socket.gethostbyname('www.google.com') 
  #   except socket.gaierror: 
    
  #     # this means could not resolve the host 
  #     print ("there was an error resolving the host")
  #     sys.exit() 
    
  #   # connecting to the server 
  #   s.connect((host_ip, port)) 
    
  #   print ("the socket has successfully connected to google") 
  
  ''' Function that handles packend server work including getting the file or trying to.
  Returns the integer status code to return in the HTTP response. '''
  # def serve(self):
  #   # Check for request type
  #   if REQUESTYPE not "GET":
  #     return 501
    
  #   # Check for correct HTTP version
  #   if VERSION not "HTTP/1.1":
  #     return 505
    
  #   # Look for file
  #   if FILEFOUND:


  #     return 200

  #   else:
  #     return 404
  #   pass


# Main
""" """
def main(args = None):
  # Get commands
  if args == None:
    commandInput = CommandLine()
  else:
    commandInput = CommandLine(args)

  # Check for arguments given
  if commandInput.args.port == None or commandInput.args.directory == None:
    print("Invalid arguments provided, please provide both a port and directory.", file=sys.stderr)
    sys.exit(1)
  
  # Greate Interface object
  interface = Interface(commandInput.args.port, commandInput.args.directory)

  # Search for port numbers
  output = interface.evaluatePort()
  
  # Check path
  output = interface.evaluatePath()

  HTTPBuilder = HTTPObject()

  # Get the contents and metadata of the requested file
  HTTPBuilder.getFileData(commandInput.args.directory)
  # testReq = HTTPBuilder.makeRequest("test", "test", "test", "test", "test", "test", "test", "test", "test", "test",)

  testRes = HTTPBuilder.makeResponse(200, 'FabriceKurmann')

  

  # print(testReq)
  print(testRes)
  
  return 0

  


if __name__ == "__main__":
 main()

'''
File Errors: Print an error message to stderr and exit the program if the absolute path
to the specified root directory (entered on the command line) does not exist.
○ Socket Errors: The socket operations should handle any errors or exceptions thrown. The
server application should continue to listen for subsequent client requests, and not crash.
An example of an error that you could experience is trying to use a port which is already
in use by some other process.'''