'''
  ETTTP_Sever_skeleton.py
 
  34743-02 Information Communications
  Term Project on Implementation of Ewah Tic-Tac-Toe Protocol
 
  Skeleton Code Prepared by JeiHee Cho
  May 24, 2023
 
 '''

import random
import tkinter as tk
from socket import *
import _thread

from ETTTP_TicTacToe_skeleton import TTT, check_msg

    
if __name__ == '__main__':
    
    global send_header, recv_header
    SERVER_PORT = 12000
    SIZE = 1024
    server_socket = socket(AF_INET,SOCK_STREAM)
    server_socket.bind(('',SERVER_PORT))
    server_socket.listen()
    MY_IP = '127.0.0.1'
    
    while True:
        client_socket, client_addr = server_socket.accept()
        
        start = random.randrange(0,2)   # select random to start
        
        ######################### Fill Out ################################
        # Send start move information to peer
        msg = 'SEND ETTTP/1.0\r\nHost:' + MY_IP + '\r\nFirst-Move:'+ str(start) +'\r\n\r\n' # create first move message
        client_socket.send(str(msg).encode()) # encode first move message and send to client

        # Receive ack - if ack is correct, start game
        ackmsg = client_socket.recv(SIZE) # receive ACK message from client
        ackmsg = ackmsg.decode() # decode ACK message

        if check_msg(ackmsg, MY_IP) != True: # check if received ACK message is in ETTTP format, and if not
            client_socket.close() # close socket and end connection
            break # break while loop

        num = ackmsg.find('First-Move:') # find 'First-Move:' in the message
        numstart = ackmsg[num + 11] # get start from client as numstart
        
        if str(start) != numstart: # check if start is equal to received start, and if not
            client_socket.close() # close socket and end connection
            break # break while loop 

        ###################################################################
        
        root = TTT(client=False,target_socket=client_socket, src_addr=MY_IP,dst_addr=client_addr[0])
        root.play(start_user=start)
        root.mainloop()
        
        client_socket.close()
        
        break
    server_socket.close()