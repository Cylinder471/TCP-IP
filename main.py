from CLIENT import *
from SERVER import *
from threading import Thread

def server():
    print("hello")
    newServer = Server(ipaddr="127.0.0.1", portn=3241)
    newServer.receive_file(filepath="received_data.txt", logpath="logfile.txt")

th = Thread(target = server)
th.start()

error_probability = int(input("Вероятность ошибки: "))

newclient = Client(ipadd="127.0.0.1", portn=3241, error_probability=error_probability)
newclient.send_file(filename="file.txt")