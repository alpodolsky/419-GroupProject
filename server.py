import socket
import time
from _thread import start_new_thread

user_count = 0
messages = []

def main():
    global user_count

    # portno = int(input("Gimme port no: "))

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((socket.gethostname(), 10103))

    server_socket.listen(5)

    threads = []

    while True:
        client_socket, client_address = server_socket.accept()
        print(f'Connection from {client_address} has been established')
        client_socket.send(bytes(f"Welcome to the server. You are user: {user_count}", 'utf-8'))
        # client_message = client_socket.recv(1024).decode('utf-8')
        # print(f'Received this from client: {client_message}')
        recv_message(client_socket, user_count)

        threads.append(start_new_thread(handle_comms, (client_socket,user_count)))

        user_count+=1

    exit()

def recv_message(socket, user_count):
    message = socket.recv(1024).decode('utf-8')
    print(f'Received this from client {user_count}: {message}')

def handle_comms(client_socket, user_count):
    global messages

    if user_count == 0: # First user, so we need to receive
        client_message = client_socket.recv(1024).decode('utf-8')
        messages.append(client_message)
        print(f'Received this from client: {client_message}')
        while True:
            client_message = ''
            num_messages = len(messages)
            if num_messages == 2: # Recieved a message from the other client, so we need to send
                client_socket.send(bytes(messages[-1], 'utf-8'))
                messages = []
            elif num_messages == 0: # No messages have been received from this client
                client_message = client_socket.recv(1024).decode('utf-8')
                if client_message == 'Stop' or not client_message:
                    break
            else:
                time.sleep(5)
            if client_message:
                messages.append(client_message)
                client_message = ''
            print(f"Messages so far: {messages}")
            print(f'Received this from client {user_count}: {client_message}')
        print(messages)

    elif user_count == 1:
        while True:
            num_messages = len(messages)
            if num_messages == 1: # Alice has sent a message. Now Bob has to receive it and send a message
                client_socket.send(bytes(messages[-1], 'utf-8'))
                time.sleep(1)
                client_message = client_socket.recv(1024).decode('utf-8')
                messages.append(client_message)
                print(f'Received this from client {user_count}: {client_message}')


    return

'''

When a new user is added, we need to tell the new user whether or not he is the 
first one there.

If he's the first one there, then we need to change our global flag to 1.
Then we need to make sure that the receiving user knows this so that he can send first.

If he's not the first one there, then our global flag can remain
Then the receiving user has to make sure that he receives whatever is inside the messages
array

'''



if __name__ == '__main__':
    main()