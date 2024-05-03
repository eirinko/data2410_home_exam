#Function for checking if the ip address is the correct format.
def ip_ok(ip):
    test_ip = ip.split(".")
    inrange = True
    for number in test_ip:
        if int(number) not in range (0,256): # Assuming we want inclusive 0 and inclusive 255. 
            inrange = False
    return len(test_ip)==4 and inrange

def port_ok(port):
    return port in range(1024,65536)


#Create tests?