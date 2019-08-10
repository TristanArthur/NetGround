import socket
import sys
from ipinfo import IPAddress



class Logger:

    def __init__(self, name=''):

        self.log_count = 0
        self.name = name

    def log(self, message):

        print('{}({}): {}'.format(self.name, self.log_count, message))
        self.log_count += 1


class Server:

    def __init__(self):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = 12345

        self.logger = Logger('SERVER')
        self.logger.log('SERVER STARTED')

        self.sock.bind(('', self.port))
        self.logger.log('Socket binded to ' + str(self.port))
        self.sock.listen(5)
        self.logger.log('Listening...')

        self.connection = None

    def listen(self):

        self.connection, addr = self.sock.accept()
        self.logger.log('Connection received from ' + str(addr))
        self.connection.send(str.encode('Server connected\n'))
        self.connection.close()

    def run(self):

        while True:
            self.listen()


class Client:

    def __init__(self):

        self.sock = socket.socket()
        self.port = 12345

        self.logger = Logger('CLIENT')
        self.logger.log('CLIENT STARTED')

    def connect(self, ip):

        self.sock.connect((str(ip), self.port))
        print(self.sock.recv(1024).decode())
        self.sock.close()


if __name__ == '__main__':

    if sys.argv[1].lower() == 'server':
        s = Server()
        s.listen()
    elif sys.argv[1].lower() == 'client':
        server_address = IPAddress('128.0.10.1')
        c = Client()
        c.connect(server_address)
    else:
        print('ERROR: unknown command ', sys.argv[1])
        print('usage: python connection.py [client/server]')
