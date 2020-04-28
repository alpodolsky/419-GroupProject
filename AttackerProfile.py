import time
import socket
from itertools import chain, combinations_with_replacement

class Attacker():
    def __init__(self, name):
        self.name = name
    
    def startup(self):
        self.ip_address = socket.gethostname()
        self.port_no = 10103
    
    def create_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip_address, self.port_no))

    def send_message(self, msg):
        num_bytes = self.socket.send(bytes(msg, 'utf-8'))
        time.sleep(1)
    
    def recv_message(self):
        message_from_server = self.socket.recv(1024).decode('utf-8')

        return message_from_server

    def network_loop(self):

        self.send_message('Hlelo')


        while True:
            print("You have 4 query methods: ciphertext-only, known-plaintext, chosen-plaintext, chosen-ciphertext")
            self.query_method = input("Which query method would you like: ")

            if self.query_method == 's':
                break

            self.send_message(self.query_method)
            
            self.cipher_texts = []
            self.plain_texts = []

            if self.query_method == 'ciphertext-only':
                for i in range(5):
                    self.cipher_texts.append(self.recv_message())
                    print(self.cipher_texts[i])
                print(f'This is your cipher-texts: {self.cipher_texts}')

            elif self.query_method == 'known-plaintext':
                for i in range(5):
                    plain_ciphers = self.recv_message().split(',')
                    self.cipher_texts.append(plain_ciphers[0])
                    print(self.cipher_texts[i])
                    self.plain_texts.append(plain_ciphers[1])
                    print(self.plain_texts[i])
                print(f'This is your cipher-texts: {self.cipher_texts}')
                print(f'This is your plain-texts: {self.plain_texts}')
                    
            elif self.query_method == 'chosen-plaintext':
                message = input("Enter a message you would like to have encrypted: ")
                self.send_message(message)
                encrypted_message = self.recv_message()
                print(f'This is the encrypted message: {encrypted_message}')

            elif self.query_method == 'chosen-ciphertext':
                message = input("Enter a message you would like to have decrypted: ")
                self.send_message(message)
                decrypted_message = self.recv_message()
                print(f'This is the decrypted message: {decrypted_message}')




def frequency_analysis(ciphertext):

    master_frequency_dict = {
        'e' : .1202, 't' : .0910, 'a' : .0812, 'o' : .0768, 'i' : .0731,
        'n' : .0695, 's' : .0628, 'r' : .0602, 'h' : .0592, 'd' : .0432,
        'l' : .0398, 'u' : .0288, 'c' : .0271, 'm' : .0261, 'f' : .0230,
        'y' : .0211, 'w' : .0209, 'g' : .0203, 'p' : .0182, 'b' : .0149,
        'v' : .0111, 'k' : .0069, 'x' : .0017, 'q' : .0011, 'j' : .0010,
        'z' : .0007
    }
    frequency_dict = {c : ciphertext.count(c) / len(ciphertext.replace(' ', '')) for c in list(set(ciphertext)) if c != ' '}
    print(frequency_dict)

# Works for cipher-text only, 
def brute_force(ciphertext, plaintext):
    possible_characters = 'abcdefghijklmnopqrstuvwxyz0123456789'

    

    # print([''.join(x) for x in combinations_with_replacement(possible_characters, 2)])

    # Another implementation, might not be as good
    for i in range(10): # We're gonna try all 10 character keys
        for key in [''.join(x) for x in combinations_with_replacement(possible_characters, 1)]:
            # Here we send the server the key and the cipher text.
            # Then we check if the response is the same as our plaintext. If it is, then chuck has cracked the key
            break


if __name__ == "__main__":
    attacker = Attacker('Chuck')
    attacker.startup()
    attacker.create_socket()
    attacker.network_loop()