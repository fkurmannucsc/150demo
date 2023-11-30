This is the server program for a simple HTTP server that is able to serve GET requests for files in the filesystem directory of the root folder for this program. To run, the server must be started by running this program with both command line arguments and the directory argument matching the root directory of this project folder. Then, a brower or terminal based connection can be made via the loopback address and same port specified when running the server program to communicate with the server.

HTTP responses will be returned and the client server connection will remain open until the server program is halted or the request for STOP is made from the client by requesting STOP in place of a specific file.

A port number and directory is requred as input, the port number is checked and only used if it is a well known or registered port number. Note that on certain computers, port 80 will result in an error since that port is already reserved.

In addition to helpful debugging output to stdout, stderr receives output detailing exceptions and error handling. Finally, two files are added or updated in the project root directory every time the program is run, they are fkurmannHTTPResponses.txt and fkurmannSocketOutput.CSV and they contain the HTTP response headers returned during a session and the socket connection details for a session, respectivley.

To run: python3 part2.py -d [DIRECTORY] -p [PORT]

Examples: 
  
  Input:
    python3 part2/part2.py -p 8080 -d /Users/fabricekurmann/Desktop/CS/School/CSE150/finalProject/fkur 

  Output:
    Directory /Users/fabricekurmann/Desktop/CS/School/CSE150/finalProject/fkur does not exist.

The above example shows how invalid directories are checked for before the server runs.
   
  Input:
    python3 part2/part2.py -d /Users/fabricekurmann/Desktop/CS/School/CSE150/finalProject/fkurmann
  
  Output:
    Invalid arguments provided, please provide both a port and directory.

The above example shows how both a port and directory must be entered.

Input:
    python3 part2/part2.py -p 8080 -d /Users/fabricekurmann/Desktop/CS/School/CSE150/finalProject/fkurmann
  
  Output:
    Registered port number 8080 entered - could cause a conflict.
    8080 /Users/fabricekurmann/Desktop/CS/School/CSE150/finalProject/fkurmann
    Welcome socket created: 127.0.0.1, 8080
    Connection socket created: 127.0.0.1, 55815
    Connection to 127.0.0.1, 55815 is now closed.
    Connection socket created: 127.0.0.1, 55816
    Connection to 127.0.0.1, 55816 is now closed.
    Connection socket created: 127.0.0.1, 55818
    Connection to 127.0.0.1, 55818 is now closed.
    Connection socket created: 127.0.0.1, 55821
    Connection to 127.0.0.1, 55821 is now closed.
    Connection socket created: 127.0.0.1, 55855
    Connection to 127.0.0.1, 55855 is now closed.
    Connection socket created: 127.0.0.1, 55856
    Connection to 127.0.0.1, 55856 is now closed.
    Connection socket created: 127.0.0.1, 55858

The above example shows a successful server start and outputs to stdout based on a few valid and invalid client requests.