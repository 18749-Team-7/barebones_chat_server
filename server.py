import argparse
import socket
import time
import threading
import os

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

# Global variables
users = dict()
users_mutex = threading.Lock() # Lock between client servicing thread

file_mutex = threading.Lock()

def broadcast(message):
    # Inform all other clients that a new client has joined
    users_mutex.acquire()
    for _, s_client in users.items():
        s_client.send(message.encode(STR_ENCODING))
    users_mutex.release()
    return

def client_service_thread(s, addr, logfile, verbose=False):
    # Client has connected to the server
    data = s.recv(BUF_SIZE)
    data = data.decode(STR_ENCODING)
    username = data[len(LOGIN_STR):]

    # Send login message to new user
    message = "You have joined the chat as: {}".format(username)
    s.send(message.encode(STR_ENCODING))

    # Send login message to all other users
    message = "User {} has joined the chat.".format(username)

    broadcast(message)

    # Add the client to the dictionary
    users_mutex.acquire()
    users[username] = s
    users_mutex.release()
    
    while True:
        data = s.recv(BUF_SIZE)
        data = data.decode(STR_ENCODING)

        # If the client is attempting to logout
        if data.startswith(LOGOUT_STR):
            # Delete the current client from the dictionary
            users_mutex.acquire()
            del users[username]
            users_mutex.release()

            message = "User {} has left the chat.".format(username)

            # Inform others that user has logged out
            broadcast(message)

            s.close()
            return
            
        else:
            message = "{}: {}".format(username, data)

            # Send message to all clients
            broadcast(message)

        # Logging
        if(verbose): print(message)

        file_mutex.acquire()
        with open(logfile, 'a') as f:
            f.write("{}: {}\n".format(time.ctime(), message))
        file_mutex.release()
    return

def tcp_server(port, logfile, verbose=False):
    try:
        
        host_ip = socket.gethostbyname(socket.gethostname())
        print(RED + "Starting chat server on " + str(host_ip) + ":" + str(port) + RESET)
        with open(logfile, 'a') as f:
            f.write("{}: Starting server\n".format(time.ctime()))

        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # IPv4, TCPIP
        s.bind((host_ip, port))
        s.listen(5)

        while(True):
            # Accept a new connection
            conn, addr = s.accept()

            # Initiate a client listening thread
            threading.Thread(target=client_service_thread, args=(conn,addr, logfile, verbose)).start()

    except KeyboardInterrupt:
        # Closing the server
        s.close()
        print()
        print(RED + "Closing chat server on " + str(host_ip) + ":" + str(port) + RESET)
        with open(logfile, 'a') as f:
            f.write("{}: Closing server\n".format(time.ctime()))


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--port', help="Server port", type=int, default=5000)
    parser.add_argument('-l', '--logfile', help="Log file name", default='chat.log')
    parser.add_argument('-v', '--verbose', help="Print every chat message", action='store_true')

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    start_time = time.time()

    args = get_args()
    tcp_server(args.port, args.logfile, args.verbose)

    print("\nTotal time taken: " + str(time.time() - start_time) + " seconds")

    # Exit
    os._exit(1)