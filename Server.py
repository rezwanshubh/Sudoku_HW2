import pika, sys, uuid
import random
import socket

def on_request(ch, method, props, body):
    print ("\nIn on request")
    body = body.decode('utf-8')
    userName = body.split(':')[0]
    body = body.split(':')[1]

    # Since with each connection the cilent is sending a new correaltion ID we need to store that new value to communicate with them
    # This if condition is checking whether an connection is already estabilshed
    if userName in connections:
        #print ("\n\nUserName is in connections")
        #print ("Old Correlation Id is " + connections[userName])
        #print ("Received Correlation Id : " + props.correlation_id)
        connections[userName] = props.correlation_id
        #print ("New Correlation Id in connections is " + connections[userName])
        #print ("---------------------------------------------------------")

    #this if condition try to send the Sudoku numbers to the new connected client
    if ((len(body) > 4 and len(body) < 9)):
        print ("New Clinet Connected")
        #print("\n\nUserName is NOT in connections")
        #print("Correlation Id : " + props.correlation_id)
        connections[userName] = props.correlation_id
        #print("Correlation Id in connections is " + connections[userName])
        #print("---------------------------------------------------------")
        body = Gen_send_sukodu_Random_9Numbers()
        # body = userName + ':' + body
        # broadcast(data)
    else:
        body = userName + ':' + body
        broadcast(body)

    #This is the function to send the respond back to the client
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id= \
                                                         props.correlation_id),
                     body=str(body))
    ch.basic_ack(delivery_tag=method.delivery_tag)

# this fucntion is used to broadcast data to the clients
def broadcast(msg):
    #print("\nInside broadcast msg is " + msg)
    msg = msg.encode('utf-8')
    #sending the message to the clients stored in the server
    for connection in connections:
        #print ("user Name is connections is : " + connection)
        correlation_id = connections[connection]
        channel.basic_publish(exchange='broadcast_exchange', routing_key='',
                              properties=pika.BasicProperties(correlation_id=correlation_id), body=msg)

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