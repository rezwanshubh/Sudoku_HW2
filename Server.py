import socket

if __name__ == "__main__":
    connetionCnt = 0 # count the number of connections
    my_ip = 'localhost' # Server
    PORT = 8888 # broadcast port
    conns = {} # list to srote the connections

    #TCP socket creation
    sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sckt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sckt.bind(('localhost', 7123)) #binding the socket
    sckt.listen(2)

    #broadcast scoket creation
    broadcastSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    broadcastSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    broadcastSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    while connetionCnt < 2:
        print ("Server Broadcasting")
        #broadcasting the TCP IP and scoket to the clients
        broadcastSocket.sendto(my_ip + ' ' + str(7123), ('<broadcast>', PORT))
        connection, address = sckt.accept()
        print ("Client Connected")
        conns[address] = connection
        connetionCnt = connetionCnt + 1
        print ("connetionCnt is : " + str(connetionCnt))

    # when two clients are connected we need to inform the clients to connect using indirect communication
    for val in conns:
        conns[val].send("Ok")