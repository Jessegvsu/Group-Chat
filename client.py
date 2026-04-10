import socket
import threading

def listen(sock):
    while True:
        try:
            recieved = sock.recv(1024)
            if not recieved:
                break
            print(recieved.decode("utf-8"))
        except:
            print("Connection closed")
            break

if __name__ == '__main__':
    #Connects to server

    while True:
        try:
            print("Type server IP address:")
            IP = input()
            print("Type server port:")
            port = int(input())
            print("Connected to", IP, " @ port ", port)
            break
        except (ValueError, TypeError):
            print("Please enter a valid port number:")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((IP, port))

        while True:
            print("Type a your name")
            name = input()
            if len(name) > 10:
                print("Name too long.")
            else:
                break

        while True:
            name = name + " "
            if len(name) >= 10:
                break
        thread = threading.Thread(target=listen, args=(sock,))
        thread.start()
        #create loop for interacting with server

        while True:
            data = name + input()
            #print("Sent: " + data)
            if data == name + "system: quit":
                sock.sendall(data.encode("utf-8"))
                sock.close()
                break
            sock.sendall(data.encode("utf-8"))
            #received = str(sock.recv(1024), "utf-8")
            #print("Received:", received)
    print("program closed")