import socket
import pika


class Client(threading.Thread):

    def __init__(self, server):
        self.nickname = ""
        self.tags = []
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=server))
        self.channel = self.connection.channel()
        self.callback_queue = self.channel.queue_declare(exclusive=True).method.queue

        self.broadcast_queue = self.channel.queue_declare(exclusive=True).method.queue
        self.channel.queue_bind(exchange='broadcast_exchange', queue=self.broadcast_queue)

        self.channel.basic_consume(self.__on_callback, no_ack=True, queue=self.callback_queue)
        self.channel.basic_consume(self.__on_broadcast, no_ack=True, queue=self.broadcast_queue)

        threading.Thread.__init__(self)

    def __on_callback(self, ch, method, props, body):
        body = body.decode('utf-8')
        #print ("Inside Call Back : " + body)

        if (len(body) == 27):  # 9 numbers and x y coordinates
            global Randomnumber
            Randomnumber = body
            #print ("Inside Call back Random Number is : " + Randomnumber)

    def __on_message(self, ch, method, props, body):
         pass

    def __on_broadcast(self, ch, method, props, body):
        message = body.decode('utf-8')
        userName = body.split(':')[0]
        #print ("User Name is : " + userName)
        body = body.split(':')[1]
        #print ("Message is : " + body)
        #print("Inside On Broadcast")
        #print ("message is " + message)
        #print ("lenght of message is " + str(len(message)))

        if (len(body) == 4):  #
            global Checker
            Checker = body
            #print ("Checker is : " + Checker)
        else:
            global increment
            global nickname
            increment = body
            if not userName == value1:
                nickname = userName
            #print ("increment is " + increment)

    def call(self, msg):

        msg = msg.encode('utf-8')
        #print (msg)
        self.call_back_response = None
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,
                                       correlation_id=self.corr_id,
                                   ),
                                   body=msg)

    def run(self):
        self.channel.start_consuming()

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

        client = Client(host)
        client.setDaemon(True)
        client.start()

        while (True):
            value1 = enterbox("   Please Enter Your Nickname", "Welcome To Sukodu")
            if ((len(value1) > 8 or len(value1)< 5 ) or (value1 == '') or (value1.isspace())):
                msgbox("Your Nickname should be in between 4 to 8 length, Please Try Again......","Wrong Input")
            else:
                msgbox("You Are Welcome  :" + str(value1), "Session has started")
                global nickname
                #nickname = value1
                userName = '' + ':' + value1
                print("Sending The user name " + userName)
                client.call(userName)              

while True:
    message = raw_input('>')
    if message == 'exit':
        exiting = True
        break
    client.call(message)