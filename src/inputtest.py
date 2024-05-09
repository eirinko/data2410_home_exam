import ipaddress

def ip_ok(ip):
    '''Function for checking if the IP address is ok'''
    try:
       val = ipaddress.ip_address(ip)
       return True
    except ValueError:
       return False

def port_ok(port):
    '''Function for checking if the port is in range'''
    return port in range(1024,65536)
