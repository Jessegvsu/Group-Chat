import socketserver
from socketserver import TCPServer
import threading

lock = threading.Lock()
names = []
clients = {}
class GroupChat(socketserver.BaseRequestHandler):

    def send(self, message, sender_name):
        #open socket with name
        with lock:
            for name, sock in clients.items():
                if name != sender_name:
                    print(f"Sending {sender_name + " " + message}")
                    sock.sendall((sender_name + " " + message).encode("utf-8"))

    def handle(self):
        name = None
        #parses message

        try:
            while True:
                self.data = self.request.recv(1024)
                if not self.data:
                    break

                name = self.data[:10].decode("utf-8")

                #if the name included in client message has not been recieved,
                # add it to names and open new thread with name and start thread.
                if name not in names:
                    with lock:
                        names.append(name)
                        clients[name] = self.request
                        print(f"New user {name}")

                #print data from client for server use
                print(f"Received from: {self.client_address[0]}:")
                print(f"Recieved message From {name.strip()}: {self.data[10:].decode("utf-8")}")


                #if client message is system quit close socket to client

                if self.data[10:] == b"system: quit":
                    #delete name from names and client list
                    with lock:
                        del clients[name]
                        names.remove(name)
                        self.request.close()
                        break

                #send message back to client reflecting what it is.
                self.send(self.data[10:].decode("utf-8"), name)


        except ConnectionResetError:
            print("Connection reset by peer")



if __name__ == '__main__':

    try:
        print("GroupChat ready at port 5000. Press Ctrl-C to stop")
        HOST, PORT = "localhost", 5000
        TCPServer.allow_reuse_port = True
        TCPServer.allow_reuse_address = True
        with socketserver.ThreadingTCPServer((HOST, PORT), GroupChat) as server:
            server.serve_forever()

    except KeyboardInterrupt:
        print("Keyboard interrupt detected")