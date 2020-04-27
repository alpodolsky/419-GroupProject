# from essential_generators import DocumentGenerator
import socket
import random
import time

'''

	Variables that could be unecessary inclue name, 

'''

class User():
	def __init__(self, name, ip_address=None, port_no=None, socket=None):
		self.name = name
		#self.gen = DocumentGenerator()
		self.ip_address = ip_address
		self.port_no = port_no
		self.socket = socket

	# Takes care of getting the encryption method, ip address, and port number
	def startup(self):
		print("Here are your options for encrypting:")

		# All this code is subject to change based on how the server is created
		# self.ip_address = input("Please tell me the server IP: ")
		# self.port_no = int(input("Please tell me the port of the server: "))
		self.ip_address = socket.gethostname()
		self.port_no = 10103

	# Takes care of creating our socket
	def create_socket(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.connect((self.ip_address, self.port_no))

	def gen_random_sentences(self):
		nouns = ("puppy", "car", "rabbit", "girl", "monkey")
		verbs = ("runs", "hits", "jumps", "drives", "barfs") 
		adv = ("crazily.", "dutifully.", "foolishly.", "merrily.", "occasionally.")
		adj = ("adorable", "clueless", "dirty", "odd", "stupid")
		num = random.randrange(0,5)
		l = [nouns, verbs, adj, adv]
		return ' '.join([random.choice(i) for i in l])

	def send_message(self, msg, user_flag):
		# print(f'Sending this to server: {msg}')
		num_bytes = self.socket.send(bytes(msg, 'utf-8'))

		if user_flag == '0': # This is alice sending message
			print(f'Alice: {msg}')
		elif user_flag == '1':
			print(f'Bob: {msg}')
		# print(f'Number of bytes sent: {num_bytes}')
		time.sleep(1)

	def recv_message(self, user_flag):
		message_from_server = self.socket.recv(1024).decode('utf-8')
		# print(f'Received this message from server: {message_from_server}')
		if user_flag == '0': # This is alice sending message
			print(f'Bob: {message_from_server}')
		elif user_flag == '1':
			print(f'Alice: {message_from_server}')

	def network_loop(self):

		msg = self.socket.recv(1024).decode('utf-8')
		print(msg)
		user_flag = msg[-1]

		message_to_send = "Hello"
		self.send_message(message_to_send, 10) # User flag doesn't matter in this case
		
		# First user
		if user_flag == '0':

			# Piece of code is meant for dealing with what kind of key they would like
			key_type = input("What kind of key type would you like? Type pke for private key or ske for shared key: ")
			self.send_message(key_type, 10)

			# Piece of code is meant for dealing with what kind of encryption method is sent
			print('Your encryption methods include: playfair, laboy, and porta')
			self.send_message(input("So which encryption option would you like?: "), 10)

			i = 0
			while i < 5:
				message_to_send = self.gen_random_sentences()
				# print(f'Sending "{message_to_send}" to server')
				# n = self.socket.send(bytes(message_to_send, 'utf-8'))
				self.send_message(message_to_send, user_flag)
				self.recv_message(user_flag)


				# message_from_server = self.socket.recv(1024)
				# # print(f'Received this message from server: {message_from_server}')
				# print(f'Bob: {message_from_server}')
				i += 1
			self.socket.send(bytes('Stop', 'utf-8'))
		
		# Not the first user
		else:
			i = 0
			while i < 5:
				self.recv_message(user_flag)
				# message_from_server = self.socket.recv(1024)
				# print(f'Received this message from server: {message_from_server}')
				message_to_send = self.gen_random_sentences()
				self.send_message(message_to_send, user_flag)
				i += 1

	def close_socket(self):
		self.socket.close()

if __name__ == '__main__':
	user = User('Alice')
	user.startup()
	user.create_socket()
	user.network_loop()
