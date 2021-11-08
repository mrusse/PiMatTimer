import socket
import pyautogui
import _thread
import os

serverSocket = socket.socket()
print("Server socket created")

ip = "192.168.1.217"
port = 35491

serverSocket.bind((ip, port))
print("Server socket bound with with ip {} port {}".format(ip, port))

serverSocket.listen()
count = 0

(clientConnection, clientAddress) = serverSocket.accept()
pyautogui.press('space')  
while(True):

    data = clientConnection.recv(1024)
    data = data.decode('ascii')

    print(data)
    if data == "a":
        for i in range (100):
            print('space')
            pyautogui.press('space') 

    if(data == "exit"):
        print("Connection closed")
        quit()
