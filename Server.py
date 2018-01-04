
import pika, sys, uuid
import random
import socket

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='rpc_queue')

connections = {}

def Gen_send_sukodu_Random_9Numbers():
    stringNXY = ''
    added = [0]
    for y in range(0, 9, 3):
        for x in range(0, 9, 3):
            if len(added) == 10:
                return
            i = 0
            while i in added:
                i = random.randint(1, 9)
            try:
                stringNXY += str(i)
                stringNXY += str(random.randint(x, x + 2))
                stringNXY += str(random.randint(y, y + 2))
            except ValueError:
                print("Bugs in Generating the Numbers")
    return stringNXY


def on_request(ch, method, props, body):
    print ("\nIn on request")
    body = body.decode('utf-8')
    #print (body)
    print(body)
    userName = body.split(':')[0]    
    print ("User Name is : " + userName)
    body = body.split(':')[1]
    print ("Message is : " + body)


    if userName in connections:
        print ("\n\nUserName is in connections")
        print ("Old Correlation Id is " + connections[userName])
        print ("Received Correlation Id : " + props.correlation_id )
        connections[userName] = props.correlation_id
        print ("New Correlation Id in connections is " + connections[userName])
        print ("---------------------------------------------------------")


    if ((len(body) > 4 and len(body) < 9)):
        print("\n\nUserName is NOT in connections")
        print("Correlation Id : " + props.correlation_id)
        connections[userName] = props.correlation_id
        print("Correlation Id in connections is " + connections[userName])
        print("---------------------------------------------------------")
        body = Gen_send_sukodu_Random_9Numbers()
        #body = userName + ':' + body
        #broadcast(data)
    else:
        body = userName + ':' + body
        broadcast(body)


    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id= \
                                                         props.correlation_id),
                     body=str(body))
    ch.basic_ack(delivery_tag=method.delivery_tag)

def broadcast(msg):
    print("\nInside broadcast msg is " + msg)
    msg = msg.encode('utf-8')
    for connection in connections:
        print ("user Name is connections is : " + connection)
        correlation_id = connections[connection]
        channel.basic_publish(exchange='broadcast_exchange', routing_key='', properties=pika.BasicProperties(correlation_id=                                                          correlation_id), body=msg)

if __name__== "__main__":
    connetionCnt = 0
    my_ip = 'localhost'
    PORT = 8888
    conns = {}
    
    sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sckt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sckt.bind(('localhost', 7123))
    sckt.listen(2)
    broadcastSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    broadcastSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    broadcastSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    
    while connetionCnt < 2:
        print ("Server Broadcasting")
        broadcastSocket.sendto(my_ip + ' ' + str(7123), ('<broadcast>', PORT))
        connection, address = sckt.accept()
        print ("Client Connected")
        conns[address] = connection
        connetionCnt = connetionCnt + 1
        print ("connetionCnt is : " + str(connetionCnt) )
        
    for val in conns:
        conns[val].send("Ok")
        
    print("Starting RabbitMQ Server")        

    channel.exchange_declare(exchange='broadcast_exchange', exchange_type='fanout')
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(on_request, queue='rpc_queue')

    print(" [x] Awaiting RPC requests")

    try:
        channel.start_consuming()
    except KeyboardInterrupt as e:
        print('Ctrl+C issued ...')
        print('Terminating ...')
        sys.exit(0)



