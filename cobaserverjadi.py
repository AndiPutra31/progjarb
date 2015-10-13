import sys
import socket
import select

HOST = '' 
SOCKET_LIST = []
RECV_BUFFER = 4096 
PORT = 9009
aye = []
username = []
list=[]
index=0

def chat_server():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)
 
    # add server socket object to the list of readable connections
    SOCKET_LIST.append(server_socket)
 
    print "Chat server started on port " + str(PORT)
 
    while 1:

        # get the list sockets which are ready to be read through select
        # 4th arg, time_out  = 0 : poll and never block
        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)
      
        for sock in ready_to_read:
            # a new connection request recieved
            if sock == server_socket: 
                sockfd, addr = server_socket.accept()
		SOCKET_LIST.append(sockfd)
		aye.append(addr)
             
            # a message from a client, not a new connection
            else:
                # process data recieved from client, 
                try:
                    # receiving data from the socket.
                    #data = sock.recv(RECV_BUFFER)
                    #if data:
                        # there is something in the socket
			data2 =sock.recv(6)
			
			if data2 =='login ' :
				data1 =sock.recv(6)
				a=aye.index(sock.getpeername())
				b=len(username)
			  	if username.count(data1) == 0 :
					if a < b :
	        	          		broadcast(server_socket, sockfd, "\r["+username[a]+"] change to ["+data1+"]\n")
						sock.send("\rChange username successfull\n")
						username[a]=data1
					else :
						username.append(data1)
			  			list.append(sock)
						user=username[aye.index(addr)]
		                  		broadcast(server_socket, sockfd, "\r["+user+"] entered our chatting room\n")
						sock.send("Login Successfull\n")

				else :
					sock.send("username already exist\n")
				
			if data2 =='kirim ' :
			  data3=sock.recv(6)
			  if username.count(data3) == 0 :
			  	sock.send("Unknown user , please check at command 'list'\n")
			  else :  
				tujuan=list[username.index(data3)]
				data4=sock.recv(RECV_BUFFER)
  			  	aza=aye.index(sock.getpeername())
  		          	tujuan.send("\r" + '['+ str(username[aza]) +'] : ' + data4) 

			if data2 =='list\n' :
			  sock.send("\rList User :\n")
			  for index in range(len(username)) :
			      sock.send("\r"+username[index]+ "\n")
			      #sock.send("\n")
                 	if data2 =='broad ' :
			 data4=sock.recv(RECV_BUFFER)
			 aza=aye.index(sock.getpeername())
		         broadcast(server_socket, sock,"\r" + '['+ str(username[aza]) +'] ' + data4) 
	
			if data2 =='logout' :
	 		    da=aye.index(sock.getpeername())
	                    broadcast(server_socket, sock, "\rClient ["+username[da]+"] is offline\n")
			    username.remove(username(da))
			    aye.remove(aye[da])
			    SOCK_LIST.remove(SOCKET_LIST[da+1])

			 			 
                    #else:
                        # remove the socket that's broken    
                     #   if sock in SOCKET_LIST:
                      #      SOCKET_LIST.remove(sock)

                        # at this stage, no data means probably the connection has been broken
                       # broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr) 

                # exception 
		#nambah ini :
                except:
		   # da=aye.index(sock.getpeername())
                    broadcast(server_socket, sock, "\rClient ["+username[da]+"] is offline\n")
		    #username.remove(username(da))
		    #aye.remove(aye[da])
		    #SOCK_LIST.remove(SOCKET_LIST[da+1])
                    continue

    server_socket.close()
    
# broadcast chat messages to all connected clients
def broadcast (server_socket, sock, message):
    for socket in SOCKET_LIST:
        # send the message only to peer
        if socket != server_socket and socket != sock :
            try :
                socket.sendall(message)
            except :
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)
 
if __name__ == "__main__":

    sys.exit(chat_server())       
