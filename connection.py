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

    def __init__(self, port=20):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port

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

    def __init__(self, port=20):

        self.sock = socket.socket()

        self.logger = Logger('CLIENT')
        self.logger.log('CLIENT STARTED')

    def connect(self, ip, port):

        self.sock.connect((str(ip), port))
        self.logger.log('Connected to server')

    def send(self, message):

        try:
            self.sock.sendall(str.encode(message))
        except:
            # Send fail
            self.logger.log('ERROR message send failed')
            sys.exit()

    def receive(self):

        print(self.sock.recv(4096).decode())

    def close(self):

        self.sock.close()


if __name__ == '__main__':

    if sys.argv[1].lower() == 'server':
        s = Server()
        s.listen()
    elif sys.argv[1].lower() == 'client':
        server_address = IPAddress('172.217.167.78')
        c = Client()
        c.connect(server_address, 80)
        c.send('&quot;GET / HTTP/1.1\r\n\r\n&quot;')
        c.receive()
        c.close()
    else:
        print('ERROR: unknown command ', sys.argv[1])
        print('usage: python connection.py [client/server]')
