# Wrote in Python3 by YAOYE LU(z5188093)
 #1.send 10 ping requests to the server, separated by approximately one second
	#1.1 payload of data: PING sequenceNum timestamp
	#1.2 write the client so that it executes with:
		#$python PingClient.py host port

import time
import socket
import select
import sys

#sys.argv contains the command-line arguments passed to the script. 
if len(sys.argv)!=3:
	print("No Such Command!")
	print("Usage:$python Filename.py host port")
	sys.exit()
mysock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
seq = 0
rtt = {}
mysock.setblocking(False)
host = sys.argv[1]
port = int(sys.argv[2])
IP=socket.gethostbyname(host)
# packet_loss = 0
while seq<10:
	message = "ping"+" "+ str(seq)+ " " + str(time.ctime()) + "\r\n"
	mysock.sendto(message.encode("utf-8"),(host,port))
	time1 = time.time()
	ready = select.select([mysock], [], [], 1)
	if ready[0]:
		data=mysock.recv(1024)
		time2=time.time()
		rtt[seq] = round((float(time2)-float(time1))*1000,1)
		print(f"ping to {IP} seq={seq} rtt={rtt[seq]} ms")
	else:
		# packet_loss += 1
		print(f'ping to {IP} seq={seq} time out')
	seq +=1
rtt_l = list(rtt.values())
min_rtt = min(rtt_l)
max_rtt = max(rtt_l)
avg_rtt = round(sum(rtt_l)/len(rtt_l),1)
print (f"round-trip min/avg/max= {min_rtt}/{avg_rtt}/{max_rtt} ms")
mysock.close()


