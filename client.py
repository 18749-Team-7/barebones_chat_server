import argparse
import socket
import threading
import os
import time

STR_ENCODING = 'utf-8'

LOGIN_STR = 'login>'
LOGOUT_STR = 'logout>'

BUF_SIZE = 1024

BLACK =     "\u001b[30m"
RED =       "\u001b[31m"
GREEN =     "\u001b[32m"
YELLOW =    "\u001b[33m"
BLUE =      "\u001b[34m"
MAGENTA =   "\u001b[35m"
CYAN =      "\u001b[36m"
WHITE =     "\u001b[37m"
RESET =     "\u001b[0m"
UP =        "\033[A"

def receive_thread(s):
    while(True):
        try:
            data, addr = s.recvfrom(BUF_SIZE)
            print(data.decode(STR_ENCODING))
        except:
            pass

def udp_client(ip, port, username):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # IPv4, UDP

        # Log in to chat server
        login_packet = LOGIN_STR + username
        s.sendto(login_packet.encode(STR_ENCODING), (ip, port))

        # Spawn thread to handle printing received messages
        threading.Thread(target=receive_thread,args=(s,)).start()

        # Chat!
        while(True):
            message = input()
            if (message):
                print(UP) # Cover input() line with the chat line from the server.
                s.sendto(message.encode(STR_ENCODING), (ip, port))

    # Press ctrl + c to log out
    except KeyboardInterrupt:
        logout_packet = LOGOUT_STR + username
        s.sendto(logout_packet.encode(STR_ENCODING), (ip, port))
        s.close()
        os._exit(1)


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-ip', '--ip', help="Server IP Address", required=True)
    parser.add_argument('-p', '--port', help="Server Port", type=int, default=5000)
    parser.add_argument('-u', '--username', help="Chat user/display name", required=True)
    
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    start_time = time.time()

    args = get_args()
    udp_client(args.ip, args.port, args.username)

    print("\nTotal time taken: " + str(time.time() - start_time) + " seconds")