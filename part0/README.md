This script returns a different output to stdout based on the port number given in stdin.
Output is either just the path if port 80 is given, or a message about well known, registered, 
our unregistered port numbers. 

In addition to a port number, a directory path is given in stdin that is returned in stdout.

The script simply compares the given port number to the established ranges for well known and 
registered port numbers and enters the output printing condition that matches.

To run: python3 part0.py -d [DIRECTORY] -p [PORT]

Examples: 
  
  Input:
    python3 part0.py -p 100 -d /home/username/web

  Output:
    Well-known port number 100 entered - could cause a conflict.

    100 /home/username/web

  Input:
    python3 part0.py -p 80 -d /home/username/web
  
  Output:
    80 /home/username/web
