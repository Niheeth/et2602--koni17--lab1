#!/usr/bin/python
import socket,sys,select,string
soc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
if (len(sys.argv) < 3):
	print("ENTER: ./chatclient hostname:port username")
	sys.exit()
in_list = sys.argv[1].split(':')
#print(in_list)
HOSTNAME = in_list[0]
PORTNUMBER = int(in_list[1])
username = sys.argv[2]
soc.settimeout(8)
soc.connect((HOSTNAME,PORTNUMBER))
#print("connection established")
nick = "NICK " + username
soc.send(nick)
x =''
while True :
	list_of_socket = [sys.stdin,soc]
	read_list,write_list,error_list = select.select(list_of_socket,[], [])
	for i in read_list:
		if i == soc:
			message_recieved = i.recv(2048)
			if not message_recieved:
				print("connection-lost")
				sys.exit()
			else:
			        if message_recieved != 'MSG ' +username+' '+x :
		                    sys.stdout.write(message_recieved.strip('MSG '))
		                    sys.stdout.flush()
			        else :
			            continue
				
		else:
		     x = ''
		     message = sys.stdin.readline()
		     x += message
		     text ='MSG ' + message
		     soc.send(text)
		     sys.stdout.write("You : ")
		     sys.stdout.write(message)
		     sys.stdout.flush()


s.close()
