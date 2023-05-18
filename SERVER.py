import socket
from calc import mod2div
from configuration import *


class Server:
	def __init__(self, ipaddr, portn, frame_size, buffer_size):
		self.FRAME_SIZE = frame_size
		self.BUFFER_SIZE = buffer_size
		self.socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket_.bind((ipaddr, portn))
		self.socket_.listen(5)

	def iszero(self, data):
		for x in data:
			if x != '0':
				return False
		return True

	def isCurrupted(self, message):
		return not self.iszero(mod2div(message, CRC_GENERATOR))

	def decode(self, message):
		message = message[: 1 - len(CRC_GENERATOR)]
		n = int(message, 2)
		return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()

	def log(self, loghandle, itr, received_frame, retries_count):

		loghandle.write("Frame Number : " + str(itr) + "\n")
		loghandle.write("Frame Content : \"" +
						self.decode(received_frame) + "\"\n")
		loghandle.write("Retries : " + str(retries_count) + "\n\n")

	def receive_file(self, filepath, logpath):

		received_socket, addr = self.socket_.accept()

		f = open(filepath, 'w')
		l = open(logpath, 'w')

		itr = 1
		retries_count = 0

		while 1:
			itr += 1
			received_frame = received_socket.recv(self.BUFFER_SIZE).decode()
			if received_frame == END_OF_FILE:
				f.close()
				l.close()
				self.socket_.close()
				print("Файл принят")
				return

			if self.isCurrupted(received_frame):
				retries_count += 1
				received_socket.send(REJECT.encode())

			else:
				# Received file
				f.write(self.decode(received_frame))

				# Log
				self.log(l, itr, received_frame, retries_count)

				retries_count = 0
				received_socket.send(ACCEPT.encode())
