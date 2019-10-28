import argparse
import socket
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

def udp_server(port, logfile, verbose=False):
    try:
        users = dict()
        
        host = socket.gethostbyname(socket.gethostname())
        print(RED + "Starting chat server on " + str(host) + ":" + str(port) + RESET)
        with open(logfile, 'a') as f:
                f.write(str(time.ctime()) + ": Starting server" + '\n')

        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # IPv4, UDP
        s.bind((host,port))

        while(True):
            data, addr = s.recvfrom(BUF_SIZE)
            data = data.decode(STR_ENCODING)

            # Check for new user login
            if ((addr not in users) and (data.startswith(LOGIN_STR))):
                username = data[len(LOGIN_STR):]
                # Send login message to new user
                message = "You have joined the chat as: " + username
                s.sendto(message.encode(STR_ENCODING), addr)

                # Send login message to all other users
                message = "User " + username + " has joined the chat."
                for user in users:
                    s.sendto(message.encode(STR_ENCODING), user)
                
                users[addr] = username

            # Check for user logout
            elif ((addr  in users) and (data.startswith(LOGOUT_STR))):
                username = users.pop(addr)
                # Send logout message to all other users
                message = "User " + username + " has left the chat."
                for user in users:
                    s.sendto(message.encode(STR_ENCODING), user)

            # Regular chat message
            elif (addr  in users):
                username = users[addr]
                message = username + ": " + data
                for user in users:
                    s.sendto(message.encode(STR_ENCODING), user)

            # Erroneous message
            else:
                message = "Erroneous message. Please try again"
                s.sendto(message.encode(STR_ENCODING), addr)

            # Logging
            if(verbose): print(message)
            with open(logfile, 'a') as f:
                f.write(str(time.ctime()) + ": " + message + '\n')

    except KeyboardInterrupt:
        # Closing the server
        s.close()
        print(RED + "Closing chat server on " + str(host) + ":" + str(port) + RESET)
        with open(logfile, 'a') as f:
            f.write(str(time.ctime()) + ": Closing server " + '\n')


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
    udp_server(args.port, args.logfile, args.verbose)

    print("\nTotal time taken: " + str(time.time() - start_time) + " seconds")