import socket

server = "192.168.178.63"
port = 9876


# Create IPv4 TCP socket:
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
s.connect ((server, port))

        