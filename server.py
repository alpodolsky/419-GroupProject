import socket
import time
import random
from _thread import start_new_thread, allocate_lock
from PlayFairCipher import PLEncrypt, PLDecrypt
from laboyCipher import encrypt as laboy_encrypt, decrypt as laboy_decrypt
from Porta import encrypt as porta_encrypt
from keyGenerator import generateKey

# buf_plaintext = [] probably won't need this
buf_ciphertext = []
full_ciphertext = []
full_plaintext = []
keys = []
encryption_method = ''
lock = allocate_lock()

def main():
    # global user_count
    global encryption_method

    key_type = ''
    user_count = 0

    # portno = int(input("Gimme port no: "))

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((socket.gethostname(), 10103))

    server_socket.listen(5)

    threads = []

    while True:
        client_socket, client_address = server_socket.accept()
        print(f'Connection from {client_address} has been established')

        if user_count < 2:

            client_socket.send(bytes(f"Welcome to the server. You are user: {user_count}", 'utf-8'))

            # Should just recieve 'hello' for confirmation
            client_message = client_socket.recv(1024).decode('utf-8')
            print(f'Received this from client: {client_message}')

            if user_count == 0:
                key_type = client_socket.recv(1024).decode('utf-8')
                encryption_method = client_socket.recv(1024).decode('utf-8').lstrip().rstrip()
                print("This is the encryption method: ", encryption_method)

            keys.append(generateKey(encryption_method))
            print(f'My user count is {user_count} and my key is {keys[user_count]}')

            if key_type == 'ske':
                keys.append(keys[0]) # Both keys for both users are the same

            threads.append(start_new_thread(handle_comms, (client_socket,user_count)))

        else:
            #somthing for the attacker
            client_message = client_socket.recv(1024).decode('utf-8')
            print(f'Received this from attacker: {client_message}')
            
            threads.append(start_new_thread(handle_attack, (client_socket,)))

        user_count+=1

    exit()

# Every time the server recieves a message, 
# it will be stored as itself in plaintext[] and as encrypted in ciphertext[]
def recv_message(client_socket, key, user_count):
    global buf_ciphertext
    global full_ciphertext
    global full_plaintext
    global encryption_method

    plaintext_message = client_socket.recv(1024).decode('utf-8')
    print(f'Received this from client {user_count}: {plaintext_message}')
    
    # Store this in full_plaintext for chuck
    full_plaintext.append(plaintext_message)

    if encryption_method == 'playfair':
        encrypted_message = PLEncrypt(plaintext_message, key) 
        buf_ciphertext.append(encrypted_message)
        full_ciphertext.append(encrypted_message)
    elif encryption_method == 'porta':
        encrypted_message = porta_encrypt(plaintext_message, key)
        buf_ciphertext.append(encrypted_message)
        full_ciphertext.append(encrypted_message)
    elif encryption_method == 'laboy':
        encrypted_message = laboy_encrypt(plaintext_message, key[0], key[1])
        buf_ciphertext.append(encrypted_message)
        full_ciphertext.append(encrypted_message)

    return

# Every time the server sends out a message,
# it will decrypt the ciphertext and send that (not the message in plaintext)
def send_message(client_socket, encrypted_message, key, user_count):
    global buf_ciphertext
    global full_ciphertext
    global full_plaintext
    global encryption_method
    decrypted_message = ''
    
    # Store this in full_plaintext for chuck

    if encryption_method == 'playfair':
        decrypted_message = PLDecrypt(encrypted_message, key)
    elif encryption_method == 'porta':
        decrypted_message = porta_encrypt(encrypted_message, key)
    elif encryption_method == 'laboy':
        decrypted_message = laboy_decrypt(encrypted_message, key[0], key[1])

    print(f'Sending this from client {user_count}: {decrypted_message}')

    client_socket.send(bytes(decrypted_message, 'utf-8'))

    return

def handle_comms(client_socket, user_count):
    global buf_ciphertext
    global full_plaintext
    global encryption_method
    global keys

    if user_count == 0: # First user, so we need to receive

        while(len(keys) == 1):
            time.sleep(1)

        recv_message(client_socket, keys[0], user_count)

        while True:
            client_message = ''
            num_messages = len(buf_ciphertext)
            if num_messages == 2: # Recieved a message from the other client, so we need to send

                print(f'User count is {user_count} and my key for sending is {keys[1]}')
                send_message(client_socket, buf_ciphertext[-1], keys[1], user_count)

                buf_ciphertext = []

            elif num_messages == 0: # No messages have been received from this client

                print(f'User count is {user_count} and my key for receiving is {keys[0]}')
                recv_message(client_socket, keys[0], user_count)

            else:
                time.sleep(1)
            print(f"Plaintext Messages so far: {full_plaintext}")
            print(f"Ciphertext Messages so far: {full_ciphertext}")
            print(f'Ciphertext messages right now: {buf_ciphertext}')
            print()
        print(full_plaintext)

    elif user_count == 1:
        while True:
            num_messages = len(buf_ciphertext)
            if num_messages == 1: # Alice has sent a message. Now Bob has to receive it and send a message

                print(f'User count is {user_count} and my key for sending is {keys[0]}')
                send_message(client_socket, buf_ciphertext[-1], keys[0], user_count)

                time.sleep(1)

                print(f'User count is {user_count} and my key for receiving is {keys[1]}')
                recv_message(client_socket, keys[1], user_count)

    return

def handle_attack(client_socket):
    global lock
    global keys
    global full_ciphertext
    global full_plaintext
    while True:

        query_method = client_socket.recv(1024).decode('utf-8')

        if query_method == 's':
            break

        if query_method == 'ciphertext-only':
            lock.acquire()
            ciphertexts = full_ciphertext[-5:]
            lock.release()
            for ciphertext in ciphertexts:
                client_socket.send(bytes(ciphertext, 'utf-8'))
                time.sleep(1)
        
        elif query_method == 'known-plaintext':
            lock.acquire()
            ciphertexts = full_ciphertext[-5:]
            plaintexts = full_plaintext[-5:]
            lock.release()
            for i in range(5):
                client_socket.send(bytes(ciphertexts[i] + ',' + plaintexts[i], 'utf-8'))
                time.sleep(1)

        elif query_method == 'chosen-plaintext':
            message = client_socket.recv(1024).decode('utf-8')
            if encryption_method == 'playfair':
                encrypted_message = PLEncrypt(message, keys[0])
            elif encryption_method == 'porta':
                encrypted_message = porta_encrypt(message, keys[0])
            elif encryption_method == 'laboy':
                encrypted_message = laboy_encrypt(message, keys[0][0], keys[0][1])
            client_socket.send(bytes(encrypted_message, 'utf-8'))
            time.sleep(1)
        
        elif query_method == 'chosen-ciphertext':
            message = client_socket.recv(1024).decode('utf-8')
            if encryption_method == 'playfair':
                decrypted_message = PLDecrypt(message, keys[0])
            elif encryption_method == 'porta':
                decrypted_message = porta_encrypt(message, keys[0])
            elif encryption_method == 'laboy':
                decrypted_message = laboy_decrypt(message, keys[0][0], keys[0][1])
            client_socket.send(bytes(decrypted_message, 'utf-8'))
            time.sleep(1)


if __name__ == '__main__':
    main()