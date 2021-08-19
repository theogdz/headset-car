import picar_4wd as fc
import sys
import tty
import termios
import asyncio

import socket

HOST = '10.0.0.157' # IP of your Raspberry Pi
PORT = 5999         # IIT's Network have this port available

power_val = 10      # Amount of Power to the Motorse; Default value is 50 but reduced to 10
key = 'status'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print('Received: ', repr(data))
            threshold = b'90'       # threshold to enable the car to move; emotivbci sends in scale of 0-100 of the strength of the output
            if data >= threshold:
                fc.forward(power_val)   # move forward command for the motor
                print('move forward')
            else:
                fc.stop()               # threshold not met, then don't move
                print('stop')


def readchar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def readkey(getchar_fn=None):
    getchar = getchar_fn or readchar
    c1 = getchar()
    if ord(c1) != 0x1b:
        return c1
    c2 = getchar()
    if ord(c2) != 0x5b:
        return c1
    c3 = getchar()
    return chr(0x10 + ord(c3) - 65)

# def Keyborad_control():
    # while True:
        # global power_val
        # key=readkey()
        # if key=='6':
            # if power_val <=90:
                # power_val += 10
                # print("power_val:",power_val)
        # elif key=='4':
            # if power_val >=10:
                # power_val -= 10
                # print("power_val:",power_val)
        # if key=='w':
            # fc.forward(power_val)
        # elif key=='a':
            # fc.turn_left(power_val)
        # elif key=='s':
            # fc.backward(power_val)
        # elif key=='d':
            # fc.turn_right(power_val)
        # else:
            # fc.stop()
        # if key=='q':
            # print("quit")  
            # break  
            
# def car_control():
    # global power_val
    # threshold = 95
    # if data >= threshold:
        # fc.forwad(power_val)
    # else:
        # fc.stop()  
        
# if __name__ == '__main__':
    # kb_ctrl()






