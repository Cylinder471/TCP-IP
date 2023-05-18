from CLIENT import *
from SERVER import *
from threading import Thread
import time
output_file = ""
buf_size = 10240
frame_size = 0

def server():
    newServer = Server(ipaddr="127.0.0.1", portn=3241, frame_size=frame_size, buffer_size=buf_size)
    newServer.receive_file(filepath=output_file, logpath="logfile.txt")

error_probability = int(input("Вероятность ошибки в %: "))
input_file = input("Название входного файла: ")
output_file = input("Название выходного файла: ")
frame_size = int(input("Размер блока данных в байтах: "))

th = Thread(target = server)
th.start()
newclient = Client(ipadd="127.0.0.1", portn=3241, error_probability=error_probability, frame_size=frame_size, buffer_size=buf_size)
start_time = time.time()
newclient.send_file(filename=input_file)
send_time = time.time() - start_time
print(f"Время отправки - {send_time} с")