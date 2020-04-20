import socket
flag = 0

def main():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    port = input("Gimme port: ")

    server_socket.bind(('localhost', int(port)))

    server_socket.listen(5)

    while True:

        c, addr = server_socket.accept()

        mesg = c.recv(1024)
        print("Message recvd: ", str(mesg))

        c.send(b'OK')
main()