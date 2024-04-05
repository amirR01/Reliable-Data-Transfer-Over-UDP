#Amir Hossein Rahmati 99103922

import socket

NCAT_SERVER_PORT = 54321
LOSSY_LINK_SEND_PORT = 13133

def remodify_udp_packet(packet_data):
    # Removing sequence number from the payload

    sequence_number = int.from_bytes(packet_data[:4], byteorder='big')
    modified_payload = packet_data[4:]

    return (modified_payload, sequence_number)

def create_ack_packet(sequence_number):

    # Create the ACK packet
    ack_packet = sequence_number.to_bytes(4, byteorder='big')

    return ack_packet

def server():
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_sock.bind(('localhost', LOSSY_LINK_SEND_PORT))
    print("server is listening on port: ", LOSSY_LINK_SEND_PORT)


    nact_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("server is sending on port: ", NCAT_SERVER_PORT)
    waiting_sequence_number = 0

    while True:
        data, address = client_sock.recvfrom(4096)
        if data:
            modified_packet, sequence_number = remodify_udp_packet(data)
            

            if sequence_number == waiting_sequence_number:
                nact_sock.sendto(modified_packet, ('localhost', NCAT_SERVER_PORT))
                waiting_sequence_number += 1
    
            client_sock.sendto(create_ack_packet(waiting_sequence_number), address)
        

            
server()