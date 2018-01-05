import socket

if __name__ == '__main__':
    
    broadcastSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    broadcastSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    broadcastSocket.settimeout(1)
    broadcastSocket.bind(('', 8888))
    print "Client is now Running...... "
    while True:
        try:
            data = broadcastSocket.recv(1024)
            print("Data is " + data)
            break
        except socket.timeout:
            pass
    broadcastSocket.close() # close the broadcast socket

# Initialize the TCP socket
# The client connected already with server, sending and receiving the messages will be via TCP socket (sckt)
    sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sckt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    host = str(data.split()[0]) # To get the port from broadcast connection to announce it in TCP socket
    print (host)
    port = int(data.split()[1]) # To get the host from broadcast connection to announce it in TCP socket
    print (port)
    print("Trying To Connect To Server")
    server =(host,port)
    sckt.connect(server)
    print("Connected To Server")
    
    response = sckt.recv(1024)
    
    print (response)
    time.sleep(1)
    
    if response == 'Ok':