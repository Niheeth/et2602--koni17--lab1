#!/usr/bin/python
import socket,sys, re
from threading import Thread
soc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
if (len(sys.argv) < 2):
	print("ENTER: ./chatserver hostname:port")
	sys.exit()
in_list = sys.argv[1].split(':')
HOSTNAME =in_list[0]
PORTNUMBER = int(in_list[1])
cli = {}
client_soc = []
soc.bind((HOSTNAME,PORTNUMBER))

def approve_connection() :
    while True :
        c,c_addr = soc.accept()
        print("%s:%s has connected." % c_addr)
        c.sendall(("Hello 1\n").encode('ascii'))
        client_soc.append(c)
        Thread(target= manage_client, args=(c,c_addr)).start()

def manage_client(c,c_addr) :

    n = c.recv(2048).decode('utf-8')
    identity = n[4:]
    if n[:4] != "NICK":
        c.sendall(("ERROR malformed command\n").encode('ascii'))
        identity = 'notset'
    elif len(identity)<=12 and re.match("^[A-Za-z0-9\_]+$",identity) is not None:
        c.send("OK \n")
    else:
        c.sendall((" ERROR malformed command\n").encode('ascii'))
        identity = 'notset'
    # message = "%s has joined the chat \n"% identity
    # broadcast(message,c)
    cli[c] = identity
    while True :
        m = c.recv(2048).decode('utf-8')
        message = m.strip("MSG ")
        if not message:
            c.close()
            del cli[c]
   #         send = "%s has left the chat \n"% identity
    #        print("%s:%s has diconnected." % c_addr)
      #      broadcast(send,c)
            break
        else :
            if identity=='notset':
                c.sendall("ERROR no nick set\n".encode('ascii'))
            if len(message) > 255 and re.match("^[^\x00-\x7F]*$",message) is None:
                c.sendall(("ERROR malformed command\n").encode('ascii'))
                # message_send = "MSG "+identity +" "
            else:
                message_send = "MSG "+identity +" "+ message
                broadcast(message_send,c)

def broadcast(msgs, client_connection):
    for q in client_soc:
        if q != soc and q != client_connection :
            try:
                print("broadcasting")
                q.sendall(msgs.encode('utf-8'))
            except:
                pass

while True:
    soc.listen(100)
    print("Server started")
    recieve_thread = Thread(target=approve_connection)
    recieve_thread.start()
    recieve_thread.join()
    soc.close()
