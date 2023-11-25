This script copies a file called HelloWorld.html with a simple message into the directory specified by the 
user. It then returns an HTTP response that mimicks what would be returned if the html file were
requested by the user via a GET request. The response is printed to stdout if no error has occured 
previously, otherwise the program exits cleanly with an appropriate error message.

A port number and directory is requred as input, the port number is checked and only used if it is a well known
or registered port number.

To run: python3 part1.py -d [DIRECTORY] -p [PORT]

Examples: 
  
  Input:
    python3 part1/part1.py -p 30 -d /Users/fabricekurmann/Desktop/CS/School/CSE150/finalProject/fkurmann/part1/

  Output:
    HTTP/1.1 200 OK
    Date: Wed, 22 Nov 2023 21:11:05 GMT
    Server: FabriceKurmann
    Last-Modified: Mon, 20 Nov 2023 23:04:31 GMT
    Content-Length: 218
    Content-Type: text/html

    <!doctype html>
    <html>
    <head>
    <title>Hellow World</title>
    <meta name="description" content="Hello World">
    <meta name="keywords" content="">
    </head>

    <body>
      Hello World, I am Fabrice Kurmann, fkurmann
    </body>
    </html>

  Input:
    python3 part1/part1.py -p 30     
  
  Output:
    Invalid arguments provided, please provide both a port and directory.
