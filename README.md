# Reliable-Data-Transfer-Over-UDP
This is a simple reliable data transfer protocol implemented over UDP. The protocol is based on the Go-Back-N protocol. The protocol is implemented in Python.

### CLIENT DETAILS ###
- The client receive the udp packets from the ncat sender in one thread. it will buffer the packets and it will assign each packet a sequence number.
- Other thread of the client sends packets to the server. it will modify the packets and adds the sequence number to the packet and sent it to the server in correct order. it has a timeout value that it resend the packets when it comes to the timeout.
- Another thread of the client is listening for the acks from the server. it will receive the acks and it will remove the sent packets from the buffer.
### SERVER DETAILS ###
- The server receives the packets from the client and if the sequence number is the one it is expecting, it will send an ack to the client. and it will sent the packet to the ncat receiver. but if the sequence number is not the one it is expecting, it will send an ack for the expected sequence number.

### HOW TO TEST ###
- run server with the following command:
```
make server
```
- Then run client with the following command:
```
make client
```
- Then run lossy link with the following command:
```
make lossy_link
``` 
- Then run ncat receiver with the following command:
```
ncat --recv-only -u -l 54321
```
- Then send packets with the following command:
```
seq 1000 | { while read; do sleep 0.01; echo "$REPLY"; done; } | ncat --send-only -u 127.0.0.1 12345
```

- you can see the packets order in the ncat receiver.



