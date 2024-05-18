# DATA2410 Home Exam 2024
This is my solution to the home exam in the course DATA2410 Networking and cloud computing, spring of 2024. 
Description of the exam is given here: https://github.com/safiqul/drtp-oppgave/

## Using application.py
### A simple file transfer program with DATA2410 Reliable Transport Protocol (DRTP)
When using this program, you need to invoke the server first, and then the client. 

To invoke the server on your computer, you can use the following code:

`python3 application.py -s`

Then, in another terminal window, use the following code to invoke the client:

`python3 application.py -c -f <file_name>`

The client will then try to send the file with <file_name> to the server using the default IP address and port number. 

### Options
The solution uses argparse, and there are some optional arguments available for both the server and the client. 
Be sure to always use the same IP address and port for both client and server. The default values are 127.0.0.1 and 8088 for IP address and port, respectively. Here's a look at the --help page:

![image](https://github.com/eirinko/data2410_home_exam/assets/31256905/048762e2-bc84-4d2d-b19c-ae1e599af5b5)


#### Server options
**IP:** Default value set to 127.0.0.1, but can be set to something else with the IPv4 format (ex 10.1.2.3) with the following code:

`python3 application.py -s -i <IP_address>`

**Port:** Default value set to 8088, but can be set to something else within range [1024,65535] with the following code:

`python3 application.py -s -p <port_no>`

**Discard:** A test case where a data packet is discarded. If -d 5 is passed to the server, data packet with seq no 5 is discarded.

`python3 application.py -s -d <discard_packet_number>`

#### Client options
**File:** must be included, or else the client doesn't know which file to send. 

**IP:** Default value set to 127.0.0.1, but can be set to something else with the IPv4 format (ex. 10.1.2.3) with the following code:

`python3 application.py -c -f <file_name> -i <IP_address>`

**Port:** Default value set to 8088, but can be set to something else within range [1024,65535] with the following code:

`python3 application.py -c -f <file_name> -p <port_no>`

**Window:** Default sliding window size is set to 3, but it can be changed using this option. If you pass -w 10 to the client, the window size will be 10. 

`python3 application.py -c -f <file_name> -w <window_size>`

