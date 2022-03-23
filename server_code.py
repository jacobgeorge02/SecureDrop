import socket
import os
import sys

# device's IP address
#IP to use for the server to get IP
serverHostIP = "0.0.0.0"
#Datagram protocol
serverPort = 5001 
buffer = 4096

s = socket.socket()

# bind the socket to the local address
s.bind((serverHostIP, serverPort))

#listen for connections from client code
s.listen(10)
print(f"[*] Listening as {serverHostIP}:{serverPort}")
# accept connection if there is any
client_socket, address = s.accept() 
print(f"[+] {address} is connected.")

#recieved info from file
fileRecieved = client_socket.recv(buffer).decode()
fileName, sizeOfFile = fileRecieved.split()
fileName = os.path.basename(fileName)
sizeOfFile = int(sizeOfFile)

# start receiving the file from the socket
with open(fileName, "wb") as f:
    while True:
        bytes_read = client_socket.recv(buffer)
        if not bytes_read:    
            break
        f.write(bytes_read)

# close socket and server
client_socket.close()
s.close()