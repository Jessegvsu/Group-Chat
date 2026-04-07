from threading import Thread
from socketserver import StreamRequestHandler, TCPServer
from socket import socket, AF_INET, SOCK_STREAM, create_connection, gaierror
class GroupChat(StreamRequestHandler):

    def handle(self):
        #recieve message nad put into list.
        print(f"Received from {self.client_address}")
        client_request_message = []
        while True:
            line = self.rfile.readline(1000)
            print(f"From client: {line}")
            client_request_message.append(line)
            if (len(line) == 2) or (len(line) == 0):
                break

        #send message back to client.
        for line in client_request_message:
            self.wfile.write(line)

if __name__ == '__main__':

    try:
        print("GroupChat ready at port 5000. Press Ctrl-C to stop")
        HOST, PORT = "localhost", 5000
        TCPServer.allow_reuse_port = True
        TCPServer.allow_reuse_address = True
        with TCPServer((HOST, PORT), GroupChat) as server:
            server.serve_forever()
    except KeyboardInterrupt:
        print("Keyboard interrupt detected")