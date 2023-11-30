import argparse
import socket
import sys 
import os
import re
import csv
import shutil # To copy filesystem directory


from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime

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

""" Class responsible for error checking of inputs and for interacting with file system. """
class Interface():
  def __init__(self, port, directory):
    self.portNumber = port
    self.directory = directory
    
  def evaluatePort(self):
    if self.portNumber == 80:
      print("{port} {path}".format(port=self.portNumber, path=self.directory))
    elif (self.portNumber >= 0 and self.portNumber < 1024):
      # pass
      print("Well-known port number {port} entered - could cause a conflict.\n{port} {directory}".format(port=self.portNumber, directory=self.directory))
    elif (self.portNumber > 1023 and self.portNumber < 49152):
      # pass
      print("Registered port number {port} entered - could cause a conflict.\n{port} {directory}".format(port=self.portNumber, directory=self.directory))
    else:
      print("Terminating program, port number is not allowed.", file=sys.stderr)
      sys.exit(1)
      
    return 0
  
  def evaluateDirectory(self):
    if not os.path.isabs(self.directory) or not os.path.isdir(self.directory):
      print('Directory {directory} does not exist.'.format(directory=self.directory), file=sys.stderr)
      sys.exit(1)
    return 0

""" Socket class. """
class Socket():
  def __init__(self, port, path):
    self.responseOptions = {200: 'OK', 404: 'File Not Found', 501: 'Not Implemented', 505: 'HTTP Version Not Supported'}

    # Attributes for HTTP response
    now = datetime.now()
    stamp = mktime(now.timetuple())
    self.currentTime = format_date_time(stamp)
    self.lastMod = ''
    self.length = '0'
    self.fileType = ''
    self.body= ''

    # User inputted values
    self.port = int(port)
    self.address = '127.0.0.1'
    self.path = path
    self.file = ''
    self.filePath = ''

    # Tracking for output files
    self.txtResponses = []
    self.csvRows = []

  """ Helper function to write the CSV file. """
  def writeCSV(self, metadata): 
    metadata.insert(6,"Bytes sent:")
    metadata.insert(4,"Requested URL")
    metadata.insert(0,"4-Tuple:")
    metadata.insert(0,"Client request served")
    # print(metadata)
    self.csvRows.append(metadata)
         
    csvFile = open(self.path + '/fkurmannSocketOutput.csv', 'w') 
    csvWriter = csv.writer(csvFile)  
    csvWriter.writerows(self.csvRows) 
    csvFile.close()

  """ Helper function to write the text file. """
  def writeTXT(self): 
    txtFile = open(self.path + '/fkurmannHTTPResponses.txt', 'w') 
    for item in self.txtResponses:
      txtFile.write(item)
    txtFile.close()

  """ Function to make the http res object. """
  def makeResponse(self, code):
    templateResponse = '''HTTP/1.1 {code} {description}\r\nContent-Length: {length}\r\nContent-Type: {type}\r\nDate: {date}\r\nLast-Modified: {lastMod}\r\nConnection: close\r\n\r\n'''.format(code=code, 
              description=self.responseOptions[code], 
              date=self.currentTime, 
              lastMod=self.lastMod,
              length=self.length,
              type=self.fileType)
    return templateResponse
  
  """ Function to get data and metadata to fill http response object with a file's content. """
  def getFileData(self):
    # Locate the file in filesystem
    # print(self.filePath)

    # Get the type of the file
    try:
      self.makeFileType()
    except:
      pass

    # Get current time and last modified times, translate them to HTTP format
    now = datetime.now()
    stamp = mktime(now.timetuple())
    self.currentTime = format_date_time(stamp)

    try:
      lastModified = datetime.fromtimestamp(os.path.getmtime(self.filePath))
      stamp = mktime(lastModified.timetuple())
      self.lastMod = format_date_time(stamp)
    except:
      pass

    # Get the size of the file
    try:
      self.length = str(os.path.getsize(self.filePath))
    except:
      pass

    # Get the body of the file
    try:
      if int(self.length) < 1000:
        # Get and store the text file
        file = open(self.filePath, "r")
        self.body = file.read()
        file.close()
        return 0
      else:
        # Get and store the non text file
        file = open(self.filePath, "rb")
        self.body = file.read()
        file.close()
        return 1
    except:
      return 0

  ''' Function that handles backend server work including getting the file or trying to.
  Returns the integer status code to return in the HTTP response. '''
  def runSocket(self):
    # Open a connection socket
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
      serverSocket.bind((self.address, self.port))
    except:
      print("Error, port {port} could not be connected to.".format(port=self.port), file=sys.stderr)
      sys.exit(1)
    
    serverSocket.listen(1)
    print('Welcome socket created: {IP}, {port}'.format(IP=self.address, port=self.port))
    
    while True:
       # Reset everything
      self.lastMod = ''
      self.length = '0'
      self.fileType = ''
      self.body= ''
      self.file = ''
      self.filePath = ''

      # Open connection
      connectionSocket, addr = serverSocket.accept()
      incomingMessage = connectionSocket.recv(1024).decode()
      print('Connection socket created: {IP}, {port}'.format(IP=addr[0], port=addr[1]))

      # Serve the client, malformed requests return 505
      try:
        code = self.interpretRequest(incomingMessage)
      except:
        code = 505

      # Exit condition, does not respond to this, does not update txt and CSV files with this transmission.
      if self.file == "STOP":
        print("Client requested STOP, closing server.")
        connectionSocket.close()
        break

      transferType = 0
      # Get file data if file is found
      if code == 200:
        transferType = self.getFileData()
      
      returnMessage = self.makeResponse(code)
      print(returnMessage)
      # print(self.body[:20])

      # Binary file transfer
      if transferType == 1:
        connectionSocket.send(returnMessage.encode() + self.body)
      # Text file transfer
      else:
        connectionSocket.send(returnMessage.encode() + self.body.encode())

      connectionSocket.close()
      print('Connection to {IP}, {port} is now closed.'.format(IP=addr[0], port=addr[1]))

      # Add metadata for CSV file and response for txt file, then update those files
      self.txtResponses.append(returnMessage)
      try:
        self.writeTXT()
        self.writeCSV([self.address, self.port, addr[0], addr[1], self.file, "HTTP/1.1" + " " + str(code) + " " + self.responseOptions[code], self.length])
      except:
        print("Error opening output txt and csv files.", file=sys.stderr)
    
    serverSocket.close()
      
  """ Extracts crucial information form the request and returns the 200 code to send back. """
  def interpretRequest(self, request):
    # print(str(request))
    # Get essential information from request
    requestType = (re.search('.*/.* HTTP/.\..', str(request))).group()
    requestType = requestType.split(' ')
    method = requestType[0]
    version = requestType[2]
    body = requestType[1][1:]
    self.file = body

    # Check for request type
    if method != "GET":
      return 501
    # Check for correct HTTP version
    if version != "HTTP/1.1":
      return 505
    # Check if requested path is valid
    try: 
      self.makePath()
    except:
      return 404
    if self.evaluatePath() == 1:
      return 404
    # Get requested file
    else:
      return 200
  
  """ Helper method to check that file is in filesystem. """
  def evaluatePath(self):
    try:
      file = open(self.filePath, "rb")
      file.close()
      return 0
    except:
      return 1
  
  """ Helper function to locate files in the file system and make the search path. """
  def makePath(self):
    if self.file == 'favicon.ico':
      return self.filePath
    directory = {
      'helloWorld.html':'/',
      'filesystem.zip':'/filesystem/',
      'README.docx':'/filesystem/',
      'dog1.jpg':'/filesystem/HTMLfile_with_local_images/',
      'dog2.jpg':'/filesystem/HTMLfile_with_local_images/',
      'Example1.html':'/filesystem/HTMLfile_with_local_images/',
      'Example2.html':'/filesystem/HTMLfile_with_online_images/',
      '10MB.zip':'/filesystem/large_file/',
      'loon.jpg':'/filesystem/randomBinaryFiles/'
    }
    self.filePath = self.path + directory[self.file] + self.file
    return self.filePath
  
  """ Helper function to return the correct file type for response header. """
  def makeFileType(self):
    directory = {
      '.csv':'text/csv',
      '.png':'image/png',
      '.jpg':'image/jpeg',
      '.gif':'image/gif',
      '.zip':'application/zip',
      '.txt':'text/plain',
      '.html':'text/html',
      '.doc':'application/msword',
      '.docx':'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    }
    fileExtension = re.search('\..*', self.file).group()
    if fileExtension == '.ico':
      return self.fileType
    self.fileType = directory[fileExtension]
    return self.fileType

""" Main method, parse input and call evaluation function. """
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

  # Check directory
  output = interface.evaluateDirectory()
  # Search for port numbers
  output += interface.evaluatePort()
  

  # Should never occur, should stop before this check
  if output != 0:
    print("Port and/or directories invalid.", file=sys.stderr)
    sys.exit(1)

  # Copy filesystem into the desired directory
  # script_directory = (os.path.dirname(os.path.abspath(sys.argv[0])))[:-5]
  # print(script_directory)
  # source_dir = script_directory + "filesystem"
  # destination_dir = commandInput.args.directory + "/"
  # source_dir = 'C:\\Users\\fabricekurmann\\Desktop\\CS\\School\\CSE150\\finalProject\\fkurmann\\filesystem'
  # destination_dir = 'C:\\Users\\fabricekurmann\\Desktop\\CS\\School\\CSE150\\finalProject\\fkurmann\\part0'
  # print(source_dir, destination_dir)
  # # Either copy the filesystem or it already lives in the requested directory and continue.
  # try:
  #   shutil.copytree(source_dir, destination_dir)
  # except:
  #   pass

  # Start the server
  server = Socket(commandInput.args.port, commandInput.args.directory)

  # Get the contents and metadata of the requested file, print http object output
  server.runSocket()
  return 0

if __name__ == "__main__":
 main()
