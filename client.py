import socket
import threading

def listen(sock):
    #listens for new messages and prints them
    while True:
        try:
            recieved = sock.recv(1024)
            if not recieved:
                break
            message = recieved.decode("utf-8")
            name = message[:10].strip()
            output = f"[{name}] {message[10:]}"
            print(output)
        except:
            print("Connection closed")
            break

if __name__ == '__main__':
    '''
    while True:
        try:
            print("Type server IP address:")
            IP = input()
            print("Type server port:")
            port = int(input())
            break
        except (ValueError, TypeError):
            print("Please enter a valid port number:")
'''
    IP = "localhost"
    port = 5000
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((IP, port))
        print("Connected to", IP, " @ port ", port)

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
        #sends name by itself to server
        sock.sendall(name.encode("utf-8"))
        #loop for sending to server
        print("Type: 'system: quit' to exit")
        while True:
            data = name + input()
            #print("Sent: " + data)
            if data == name + "system: quit":
                sock.sendall(data.encode("utf-8"))
                sock.close()
                break
            sock.sendall(data.encode("utf-8"))
    print("program closed")