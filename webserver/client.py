import socket

socketObject = socket.socket()
socketObject.connect(("192.168.0.55", 35491))

print("Connected to localhost")


while(True):
    name = input("Enter data: ")
    bytes = str.encode(name)

    socketObject.sendall(bytes)

    #data = socketObject.recv(1024)
    #print(data)

    #if(data==b''):
        #print("Connection closed")
        #break

socketObject.close()   
