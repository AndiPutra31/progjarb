import sys
import socket
import select
 
def chat_client():
    host = 'localhost'
    port = 9009
        
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
     
    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print 'Unable to connect'
        sys.exit()
     
    print 'Connected to remote host. You can start sending messages\n'
    print 'Command :\n'
    print '1. login\n'
    print '2. kirim -> untuk sendto\n'
    print '3. broad -> untuk broadcast\n'
    print '4. list\n'
    print '5. logout\n'
    sys.stdout.write('[Me] : '); sys.stdout.flush()
     
    while 1:
        socket_list = [sys.stdin, s]
         
        # Get the list sockets which are readable
        ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])
         
        for sock in ready_to_read:             
            if sock == s:
                # incoming message from remote server, s
                data = sock.recv(4096)
                if not data :
                    print '\nDisconnected from chat server'
                    sys.exit()
                else :
                  #print data
                  sys.stdout.write(data)
 		  sys.stdout.write('[Me] : '); sys.stdout.flush()
             	  
            else :
                # user entered a message
                msg = sys.stdin.readline()
                s.send(msg)
		if msg == 'logout\n' :
			sys.exit()
                sys.stdout.write('[Me] : '); sys.stdout.flush() 

if __name__ == "__main__":

    sys.exit(chat_client())
