#Amir Hossein Rahmati 99103922

import socket
import time
import threading

NCAT_CLIENT_PORT = 12345
LOSSY_LINK_LISTEN_PORT = 12122
TIME_OUT_TIME = 0.25
WINDOW_SIZE = 10

class packet:
    def __init__(self, data, seq_num):
        self.received_packet = data
        self.seq_num = seq_num
    
packets = []
packets_lock = threading.Lock()


def modify_udp_packet(packet_data, sequence_number):

    # Adding sequence number to the payload
    sequence_bytes = sequence_number.to_bytes(4, byteorder='big')
    modified_payload = sequence_bytes + packet_data

    return modified_payload
    
def client_listen(port):
    sequence_number = 0
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('localhost', port))

    print("client is listening on port: ", port)
    while True:
        data, address = sock.recvfrom(4096)

        # Add the received packet to the list of packets
        packets_lock.acquire()
        packets.append(packet(data, sequence_number))
        sequence_number += 1
        packets_lock.release()

def client_send_packets(sock):
    # Create a UDP socket
    while True:
        packets_lock.acquire()
        for i in range(min(len(packets),WINDOW_SIZE)):
                new_packet = modify_udp_packet(packets[i].received_packet, packets[i].seq_num)
                sock.sendto(new_packet, ('localhost', LOSSY_LINK_LISTEN_PORT))
        packets_lock.release()
        time.sleep(TIME_OUT_TIME)

def client_receive_ack(sock):
    global packets
    while True:
        data, address = sock.recvfrom(4096)
        ack = int.from_bytes(data, byteorder='big')
        # Update the list of packets
        packets_lock.acquire()
        for i in range(len(packets)):
            if packets[i].seq_num >= ack:
                packets = packets[i:]
                break
        packets_lock.release()

def client():
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("client sends to port: ", LOSSY_LINK_LISTEN_PORT)

    # Start the threads
    listen_thread = threading.Thread(target=client_listen, args=(NCAT_CLIENT_PORT,))
    send_thread = threading.Thread(target=client_send_packets, args=(sock,))
    ack_thread = threading.Thread(target=client_receive_ack, args=(sock,))

    listen_thread.start()
    send_thread.start()
    ack_thread.start()

    listen_thread.join()
    send_thread.join()
    ack_thread.join()

client()


