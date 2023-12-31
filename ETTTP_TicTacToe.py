'''
  ETTTP_TicTacToe_skeleton.py
 
  34743-02 Information Communications
  Term Project on Implementation of Ewah Tic-Tac-Toe Protocol
 
  Skeleton Code Prepared by JeiHee Cho
  May 24, 2023
 
 '''

import random
import tkinter as tk
from socket import *
import _thread

SIZE=1024

class TTT(tk.Tk):
    def __init__(self, target_socket,src_addr,dst_addr, client=True):
        super().__init__()
        
        self.my_turn = -1

        self.geometry('500x800')

        self.active = 'GAME ACTIVE'
        self.socket = target_socket
        
        self.send_ip = dst_addr
        self.recv_ip = src_addr
        
        self.total_cells = 9
        self.line_size = 3
        
        
        # Set variables for Client and Server UI
        ############## updated ###########################
        if client:
            self.myID = 1   #0: server, 1: client
            self.title('34743-02-Tic-Tac-Toe Client')
            self.user = {'value': self.line_size+1, 'bg': 'blue',
                     'win': 'Result: You Won!', 'text':'O','Name':"ME"}
            self.computer = {'value': 1, 'bg': 'orange',
                             'win': 'Result: You Lost!', 'text':'X','Name':"YOU"}   
        else:
            self.myID = 0
            self.title('34743-02-Tic-Tac-Toe Server')
            self.user = {'value': 1, 'bg': 'orange',
                         'win': 'Result: You Won!', 'text':'X','Name':"ME"}   
            self.computer = {'value': self.line_size+1, 'bg': 'blue',
                     'win': 'Result: You Lost!', 'text':'O','Name':"YOU"}
        ##################################################

            
        self.board_bg = 'white'
        self.all_lines = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
                          (0, 3, 6), (1, 4, 7), (2, 5, 8),
                          (0, 4, 8), (2, 4, 6))

        self.create_control_frame()

    def create_control_frame(self):
        '''
        Make Quit button to quit game 
        Click this button to exit game

        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.control_frame = tk.Frame()
        self.control_frame.pack(side=tk.TOP)

        self.b_quit = tk.Button(self.control_frame, text='Quit',
                                command=self.quit)
        self.b_quit.pack(side=tk.RIGHT)
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    def create_status_frame(self):
        '''
        Status UI that shows "Hold" or "Ready"
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.status_frame = tk.Frame()
        self.status_frame.pack(expand=True,anchor='w',padx=20)
        
        self.l_status_bullet = tk.Label(self.status_frame,text='O',font=('Helevetica',25,'bold'),justify='left')
        self.l_status_bullet.pack(side=tk.LEFT,anchor='w')
        self.l_status = tk.Label(self.status_frame,font=('Helevetica',25,'bold'),justify='left')
        self.l_status.pack(side=tk.RIGHT,anchor='w')
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    def create_result_frame(self):
        '''
        UI that shows Result
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.result_frame = tk.Frame()
        self.result_frame.pack(expand=True,anchor='w',padx=20)
        
        self.l_result = tk.Label(self.result_frame,font=('Helevetica',25,'bold'),justify='left')
        self.l_result.pack(side=tk.BOTTOM,anchor='w')
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    def create_debug_frame(self):
        '''
        Debug UI that gets input from the user
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.debug_frame = tk.Frame()
        self.debug_frame.pack(expand=True)
        
        self.t_debug = tk.Text(self.debug_frame,height=2,width=50)
        self.t_debug.pack(side=tk.LEFT)
        self.b_debug = tk.Button(self.debug_frame,text="Send",command=self.send_debug)
        self.b_debug.pack(side=tk.RIGHT)
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    
    def create_board_frame(self):
        '''
        Tic-Tac-Toe Board UI
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.board_frame = tk.Frame()
        self.board_frame.pack(expand=True)

        self.cell = [None] * self.total_cells
        self.setText=[None]*self.total_cells
        self.board = [0] * self.total_cells
        self.remaining_moves = list(range(self.total_cells))
        for i in range(self.total_cells):
            self.setText[i] = tk.StringVar()
            self.setText[i].set("  ")
            self.cell[i] = tk.Label(self.board_frame, highlightthickness=1,borderwidth=5,relief='solid',
                                    width=5, height=3,
                                    bg=self.board_bg,compound="center",
                                    textvariable=self.setText[i],font=('Helevetica',30,'bold'))
            self.cell[i].bind('<Button-1>',
                              lambda e, move=i: self.my_move(e, move))
            r, c = divmod(i, self.line_size)
            self.cell[i].grid(row=r, column=c,sticky="nsew")
            
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def play(self, start_user=1):
        '''
        Call this function to initiate the game
        
        start_user: if its 0, start by "server" and if its 1, start by "client"
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.last_click = 0
        self.create_board_frame()
        self.create_status_frame()
        self.create_result_frame()
        self.create_debug_frame()
        self.state = self.active
        if start_user == self.myID:
            self.my_turn = 1    
            self.user['text'] = 'X'
            self.computer['text'] = 'O'
            self.l_status_bullet.config(fg='green')
            self.l_status['text'] = ['Ready']
        else:
            self.my_turn = 0
            self.user['text'] = 'O'
            self.computer['text'] = 'X'
            self.l_status_bullet.config(fg='red')
            self.l_status['text'] = ['Hold']
            _thread.start_new_thread(self.get_move,())
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def quit(self):
        '''
        Call this function to close GUI
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.destroy()
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    def my_move(self, e, user_move):    
        '''
        Read button when the player clicks the button
        
        e: event
        user_move: button number, from 0 to 8 
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        
        # When it is not my turn or the selected location is already taken, do nothing
        if self.board[user_move] != 0 or not self.my_turn:
            return
        # Send move to peer 
        valid = self.send_move(user_move)
        
        # If ACK is not returned from the peer or it is not valid, exit game
        if not valid:
            self.quit()
            
        # Update Tic-Tac-Toe board based on user's selection
        self.update_board(self.user, user_move)
        
        # If the game is not over, change turn
        if self.state == self.active:    
            self.my_turn = 0
            self.l_status_bullet.config(fg='red')
            self.l_status ['text'] = ['Hold']
            _thread.start_new_thread(self.get_move,())
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def get_move(self):
        '''
        Function to get move from other peer
        Get message using socket, and check if it is valid
        If is valid, send ACK message
        If is not, close socket and quit
        '''
        ###################  Fill Out  #######################
        msg = self.socket.recv(SIZE)                      # get message using socket
        msg = msg.decode()                                # decode received message

        msg_valid_check = check_msg(msg, self.recv_ip)    # check validation of received message
        
        
        if not msg_valid_check:                           # Message is not valid
            self.socket.close()                           # close socket
            self.quit()                                   # quit game
            return                                        # close function
        
        else:                                             # If message is valid - send ack, update board and change turn
            num = msg.find('(')                           # check the index of '('
            locx, locy = msg[num + 1], msg[num + 3]       # check the coordinates of received move
            loc = 3 * int(locx) + int(locy)               # index of received move in board

            ackmsg='ACK ETTTP/1.0\r\nHost:' + self.recv_ip + '\r\nNew-Move:('+ locx + ',' + locy + ')\r\n\r\n'      # ack message
            self.socket.send(ackmsg.encode())             # send ack message
            
            ######################################################   
            
            
            #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
            self.update_board(self.computer, loc)
            if self.state == self.active:  
                self.my_turn = 1
                self.l_status_bullet.config(fg='green')
                self.l_status ['text'] = ['Ready']
            #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                

    def send_debug(self):
        '''
        Function to send message to peer using input from the textbox
        Need to check if this turn is my turn or not
        '''

        if not self.my_turn:
            self.t_debug.delete(1.0,"end")
            return
        # get message from the input box
        d_msg = self.t_debug.get(1.0,"end")
        d_msg = d_msg.replace("\\r\\n","\r\n")   # msg is sanitized as \r\n is modified when it is given as input
        self.t_debug.delete(1.0,"end")
        
        ###################  Fill Out  #######################
        '''
        Check if the selected location is already taken or not
        '''
        num = d_msg.find('(')                                   # check the index of '('
        locx, locy = int(d_msg[num + 1]), int(d_msg[num + 3])   # check the coordinates of received move
        if locx < 0 or locx >= 3 or locy < 0 or locy >= 3:      # if the coordinates are out of the range
            return                                              # close function

        tloc = 3 * locx + locy                                  # index of received move in board
        if self.board[tloc] != 0:                               # if the selected location is already taken
            return                                              # close function
        '''
        Send message to peer
        '''
        msg = 'SEND ETTTP/1.0\r\nHost:' + self.recv_ip + '\r\nNew-Move:('+ str(locx) + ',' + str(locy) + ')\r\n\r\n'   # send message
        self.socket.send(str(msg).encode())                     # send message
        '''
        Get ack
        '''
        ackmsg = self.socket.recv(SIZE)                         # receive ack message
        ackmsg = ackmsg.decode()                                # decode received message

        valid = check_msg(msg, self.recv_ip)                    # check validation of received message

        if not valid:                                           # Message is not valid
            self.socket.close()                                 # close socket
            self.quit()                                         # quit game
            return                                              # close function
        
        acknum = ackmsg.find('(')                               # check the index of '('
        locx, locy = int(ackmsg[acknum + 1]), int(ackmsg[acknum + 3])   # check the coordinates of received move
        loc = 3 * locx + locy                                   # peer's move, from 0 to 8

        if tloc != loc:                                         # If the move entered and the move received in the ack message do not match
            self.socket.close()                                 # close socket
            self.quit()                                         # quit game
            return                                              # close function

        ######################################################  
        
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.update_board(self.user, loc)
            
        if self.state == self.active:    # always after my move
            self.my_turn = 0
            self.l_status_bullet.config(fg='red')
            self.l_status ['text'] = ['Hold']
            _thread.start_new_thread(self.get_move,())
            
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
        
    def send_move(self,selection):
        '''
        Function to send message to peer using button click
        selection indicates the selected button
        '''
        row,col = divmod(selection,3)
        ###################  Fill Out  #######################

        # send message and check ACK
        msg = 'SEND ETTTP/1.0\r\nHost:' + self.recv_ip + '\r\nNew-Move:('+ str(row) + ',' + str(col) + ')\r\n\r\n'   # send message
        self.socket.send(str(msg).encode())                              # send message

        ackmsg = self.socket.recv(SIZE)                                  # receive ack message
        ackmsg = ackmsg.decode()                                         # decode received message

        valid = check_msg(ackmsg, self.recv_ip)                          # check validation of received message

        if not valid:                                                    # Message is not valid
            self.socket.close()                                          # close socket
            self.quit()                                                  # quit game
            return False                                                 # return false
        
        acknum = ackmsg.find('(')                                        # check the index of '('
        locx, locy = int(ackmsg[acknum + 1]), int(ackmsg[acknum + 3])    # check the coordinates of received move
        loc = 3 * locx + locy                                            # peer's move, from 0 to 8

        if selection != loc:                                             # If the move entered and the move received in the ack message do not match
            self.socket.close()                                          # close socket
            self.quit()                                                  # quit game
            return False                                                 # return false                                                 
        
        return True                                                      # close function  
        ######################################################  

    
    def check_result(self,winner):
        '''
        Function to check if the result between peers are same
        get: if it is false, it means this user is winner and need to report the result first
        '''
        # no skeleton
        ###################  Fill Out  #######################

        # winner
        if self.user['Name'] == winner:                                   # if this user is winner
            winnermsg = 'RESULT ETTTP/1.0\r\nHost:' + self.recv_ip + '\r\nWinner:ME\r\n\r\n'    # report the result first
            self.socket.send(winnermsg.encode())                          # send report message

            resultack = self.socket.recv(SIZE)                            # receive result message
            resultack = resultack.decode()                                # decode result message

            valid = check_msg(resultack, self.recv_ip)                    # check if received result message is vaild

            if not valid:                                                 # if message is not valid
                return False                                              # return false
            
                                                                          # if message is vaild
            num = resultack.find('Winner:')                               # find winner
            if resultack[num+7:num+10] == 'YOU':                          # if the reslut between peers are same
                return True                                               # return true
            else: return False                                            # if not, return false

        else:                                                             # if this user is loser
            result = self.socket.recv(SIZE)                               # receive result message
            result = result.decode()                                      # decode result message

            valid = check_msg(result, self.recv_ip)                       # check if received result message is vaild

            if not valid:                                                 # Message is not valid
                return False                                              # return false
            
            num = result.find('Winner:')                                  # check the index of 'Winner:'   
            if result[num+7:num+9] == 'ME':                               # if winner is 'ME'  
                losermsg = 'RESULT ETTTP/1.0\r\nHost:' + self.recv_ip + '\r\nWinner:YOU\r\n\r\n'  # loser (ack) message
                self.socket.send(losermsg.encode())                       # send loser (ack) message
                return True                                               # return true
            else: return False                                            # return false
            
        ######################################################  

        
    #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
    def update_board(self, player, move):
        '''
        This function updates Board if is clicked
        
        '''
        self.board[move] = player['value']
        self.remaining_moves.remove(move)
        self.cell[self.last_click]['bg'] = self.board_bg
        self.last_click = move
        self.setText[move].set(player['text'])
        self.cell[move]['bg'] = player['bg']
        self.update_status(player)

    def update_status(self, player):
        '''
        This function checks status - define if the game is over or not
        '''
        winner_sum = self.line_size * player['value']
        for line in self.all_lines:
            if sum(self.board[i] for i in line) == winner_sum:
                self.l_status_bullet.config(fg='red')
                self.l_status ['text'] = ['Hold']
                self.highlight_winning_line(player, line)
                correct = self.check_result(player['Name'])
                if correct:
                    self.state = player['win']
                    self.l_result['text'] = player['win']
                else:
                    self.l_result['text'] = "Somethings wrong..."

    def highlight_winning_line(self, player, line):
        '''
        This function highlights the winning line
        '''
        for i in line:
            self.cell[i]['bg'] = 'red'

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# End of Root class

def check_msg(msg, recv_ip):                                        
    '''
    Function that checks if received message is ETTTP format
    '''
    ###################  Fill Out  #######################
    checkmsg = msg.split('\r\n')
    '''
    split string (checkmsg) by '\r\n' --> list with 5 factors
    ex) 'RESULT ETTTP/1.0\r\nHost:127.0.0.1\r\nWinner:YOU\r\n\r\n'
         ==> ['RESULT ETTTP/1.0', 'Host:127.0.0.1', 'Winner:YOU', '', '']
    '''
       
    if len(checkmsg) != 5:                                               # if the number of the list(checkmsg)'s factor is not 5
        return False                                                     # return false
    
    if not (checkmsg[3] == '' and checkmsg[4] == ''):                    # if the checkmsg[3] and checkmsg[4] aren't ''
        return False                                                     # return false

    if not (checkmsg[0] == 'SEND ETTTP/1.0' or checkmsg[0] == 'ACK ETTTP/1.0' or checkmsg[0] == 'RESULT ETTTP/1.0'):
        # if the checkmsg[0] is not 'SEND ETTTP/1.0', 'ACK ETTTP/1.0' or 'RESULT ETTTP/1.0'
        return False                                                     # return false
    
    hostip = 'Host:' + recv_ip                                           # prepare for checkmsg[1] ('Host:127.0.0.1')

    if (checkmsg[1] != hostip):                                          # if the checkmsg[1] is not hostip
        return False                                                     # return false
    
    if (checkmsg[2][0:10] == 'New-Move:(' and checkmsg[2][11] == ',' and checkmsg[2][13] == ')'):  # if checkmsg[2] is 'New-Move:(x, y)
        return True                                                      # return True
    
    elif (checkmsg[2][0:11] == 'First-Move:'):                           # if checkmsg[2] is 'First-Move:'
        return True                                                      # return True
    
    elif (checkmsg[2] == 'Winner:YOU' or checkmsg[2] == 'Winner:ME'):    # if checkmsg[2] is 'Winner:YOU' or 'Winner:ME'
        return True                                                      # return True

    return False                                                         # return false
    ######################################################  