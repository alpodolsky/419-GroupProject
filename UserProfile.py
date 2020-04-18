from essential_generators import DocumentGenerator
import socket

'''

	Variables that could be unecessary inclue name, 

'''

class User():
	def __init__(self, name, ip_addres=None, port_no=None, encryption_method=None, socket=None):
		self.name = name
		self.gen = DocumentGenerator()
		self.ip_addres = ip_addres
		self.port_no = port_no
		self.encryption_method = encryption_method
		self.socket = socket

	# Takes care of getting the encryption method, ip address, and port number
	def startup(self):
		print("Here are your options for encrypting:")

		# Add the print statements for the encryption methods (subject to change)
		print('For shared key encryption, type "ske"')
		print('For private key encryption, type "pke"')

		self.encryption_method = input("So which encryption option would you like?: ")

		# All this code is subject to change based on how the server is created
		self.ip_address = input("Please tell me the server IP: ")
		self.port_no = input("Please tell me the port of the server: ")

	# Takes care of creating our socket
	def create_socket(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.connect((self.ip_address), self.port_no)

	# Takes care of sending a random message from socket
	def send_message(self):
		max_messages = 4
		message = ''

		for num_message in range(max_messages):
			random_sentence = self.gen.sentence()
			if (len(message) + random_sentence > 1024):
				break
			else:
				message = message + " " + random_sentence
		
		self.socket.sendall(message.encode('utf-8'))
	
	def network_loop(self):
		self.socket = create_socket()

		# Send server the user type
		self.socket.sendall(b'User')
		self.socket.sendall(self.encryption_method.encode('utf-8'))

		# Receive confirmation that server got the user info. Also this info will tell
		# the client whether they are receiving a message from someone already there
		# or are the first to send. BASICALLY THIS IS WHERE WE RECEIVE GEN INFO FROM SERVER
		server_message = self.socket.recv(16)

		if server_message == 1: # Temporary case, but if this is 1, then this client is receiving info
			self.socket.recv(1024)

		# Condition for this loop will change based on how we plan on terminating the message chat
		while(True):
			# Creating random sentences and send them to the server
			self.send_message()
			self.socket.recv(1024)

if __name__ == '__main__':
	user = User('Alice')
	user.startup()
	user.network_loop()
