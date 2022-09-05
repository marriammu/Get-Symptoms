import socket 
import threading
import time
import cryptography
from cryptography import fernet
from cryptography.fernet import Fernet

key = b'h_31cC-cjISYrMX7FABt_GEXpKRAXerreSXay8LesC0=' # generating key for security purpose
fernet =Fernet(key)

HEADER = 256 #fixed length header of 256 bytes
PORT = 5050 #defining a port to work on.(5050 as to pick a port that is not being used for something else like 8080 for hhtp communication)
SERVER = socket.gethostbyname(socket.gethostname()) #gets IP Address of the machine we are working on.  (automatically)
ADDR = (SERVER, PORT) #soket number
FORMAT = 'utf-8' # the format in which the message is encoded when sent and decoded when recieved from byte format into a string . 
DISCONNECT_MESSAGE = "!DISCONNECT" #message that stops the connection.
Pain="pain" #variable to check that pain is recieved
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET: tells the socket what type of IP Address we are looking for for a specific connection #SOCK_STREAM: tells the server we are streaming data through the socket 
server.bind(ADDR)

def handle_client(conn, addr): #### handle each connection indvidually ####  #runs in parallel for each client
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        try:
            common_symp=0
            less_symp=0
            sever_symp=0
            
            conn.settimeout(30.0)# set time 30 sec
            count=0
            var=0
            msg_length = conn.recv(HEADER).decode(FORMAT) #every message sent to the server is going to be first a headr of length 256 that tells us the length of the message to come.
            conn.settimeout(None)
            if msg_length:
                msg_length = int(msg_length)#length of the message
                msg = conn.recv(msg_length)
                msg= fernet.decrypt(msg).decode() ##decrypt each message encrypted after server recieving
                if msg != DISCONNECT_MESSAGE:
                    print("Message",msg)
                else:
                    print(f"[DISCONNECTED] {addr} has disconnected")
                    connected = False #ends the connection between server and client 
                
                if ((count ==0)&((Pain not in msg)&(msg != 'check'))):
                    conn.send("Message recieved".encode(FORMAT)) #confirmation message are recieved by the server
                

                if((count==0) &(Pain in msg)&(msg != 'check')):# if message recieved is symptoms
                    
                    if ("sever" in msg): #for sever symptoms
                        conn.send("SEE A DOCTOR IMMEDIATELY !!!! ".encode(FORMAT)) #send the best descision for patient's symptoms
                        
                    elif ("less" in msg): # for less common symptoms
                        conn.send("Isolate at Home ".encode(FORMAT)) #send the best descision for patient's symptoms
                    elif("comm" in msg): # for less common symptoms
                        conn.send("Rest at Home ".encode(FORMAT)) #send the best descision for patient's symptoms
                            
                
                print(f"[{addr}] {msg}")
        except socket.timeout as e: #if the time is out
            print("Timeout") 
            print(f"[DISCONNECTED] {addr} has disconnected")
            conn.send("Timeout".encode(FORMAT)) #send time is out for the client
            time.sleep(8) #wait 8 sec to disconnect
            connected=False
            
    conn.close()

        
def start(): ###handels the new connections and distributes them to where they need to go####
    server.listen() #makes the server ready to recien=ve requests from clients. 
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept() # the server accepts the connection request from the client 
        thread = threading.Thread(target=handle_client, args=(conn, addr)) #passthe IP address and port number of the client initiating the connection to handle client function. 
        thread.start() #we use threading to be able to accept the requests , send and recieve data from multiple clients. 
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}") #prints number of active connections.


print("[STARTING] server is starting...")
start()