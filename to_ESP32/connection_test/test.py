import socket
hostname = socket.gethostbyname(socket.getfqdn('STRIP_New_Strip'))
print(hostname)