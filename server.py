import socketserver
import threading
from socketserver import TCPServer

class GroupChat(socketserver.BaseRequestHandler):
    def listen(self, name):
        #
    def handle(self):

        names = []
        threads = []
        #parses message

        try:
            while True:
                pieces =[b'']
                total = 0
                while b'\n' not in pieces[-1] and total < 10_000:
                    pieces.append(self.request.recv(2000))
                    total += len(pieces[-1])
                self.data = b''.join(pieces)
                name = self.data[:10].decode("utf-8")

                #if the name included in client message has not been recieved,
                # add it to names and open new thread with name and start thread.
                if name not in names:
                    names.append(name)
                    thread = threading.Thread(target=self.listen, args=name)
                    threads.append(thread)
                    thread.start()

                #print data from client for server use
                print(f"Received from: {self.client_address[0]}:")
                print(f"Recieved message: {self.data.decode("utf-8")}")

                #if client message is system quit close socket to client
                #   MODIFY TO ACCOUNT FOR THREADS
                if self.data == b"system: quit":
                    self.request.close()
                    break

                #send message back to client reflecting what it is.
                #   REMOVE TO ACCOUNT FOR SENDING TO MULTIPLE CLIENTS
                self.request.sendall(f"Server recieved: {self.data}".encode("utf-8"))

        except ConnectionResetError:
            self.request.close()
            print("Connection reset by peer")



if __name__ == '__main__':

    try:
        print("GroupChat ready at port 5000. Press Ctrl-C to stop")
        HOST, PORT = "localhost", 5000
        TCPServer.allow_reuse_port = True
        TCPServer.allow_reuse_address = True
        with socketserver.TCPServer((HOST, PORT), GroupChat) as server:
            server.serve_forever()

    except KeyboardInterrupt:
        print("Keyboard interrupt detected")