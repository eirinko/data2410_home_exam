# DATA2410 Home Exam 2024
This is my solution to the home exam in the course DATA2410 Networking and cloud computing, spring of 2024. 
Description of the exam is given here: https://github.com/safiqul/drtp-oppgave/

## Using application.py
### A simple file transfer program with DATA2410 Reliable Transport Protocol (DRTP)
When using this program, you need to invoke the server first, and then the client. 

To invoke the server on your computer, you can use the following code:

`python3 application.py -s`

Then, use the following code to invoke the client:

`python3 application.py -c -f <file_name>`

The client will then try to send the file <file_name> to the server using sockets and the default IP address and port. 

### Options
The solution uses argparse, and there are some optional arguments available for both the server and the client. 
Be sure to always use the same IP address and port for both client and server. The default values are 127.0.0.1 and 8088 for IP address and port, respectively. 

#### Server options
IP
Port
Discard

#### Client options
File: must be included, or else the client doesn't know which file to send. 


IP: Default value set to 127.0.0.1, but can be set to something else with the format 10.1.2.3 with the following code:
`-i <your_chosen_IP_address>`

Port: Default value set to 8088, but can be set to something else within range [1024,65535] with the following code:
`-p <your_chosen_port_no>`

Window: 


