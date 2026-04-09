import socket
import sys
if __name__ == '__main__':
    #Connects to server
    print("Type port number:")
    while True:
        try:
            port = int(input())
            print("Connected to", port)
            break
        except (ValueError, TypeError):
            print("Please enter a valid port number:")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(("localhost", port))

        #create loop for interacting with server
        while True:
            data = input()
            if data == "system: quit":
                sock.sendall(data.encode("utf-8"))
                sock.sendall(b"\n")
                sock.close()
                break
            sock.sendall(data.encode("utf-8"))
            sock.sendall(b"\n")
            received = str(sock.recv(1024), "utf-8")
            print("Received:", received)
    print("program closed")








