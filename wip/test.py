#!/usr/bin/python
'''
trying to make a python equivalent for the linux command below
raspivid -n -ih -t 0 -rot 0 -w 1280 -h 720 -fps 15 -b 1000000 -o - | ncat -lkv4 9090
'''
import socket
import time
import picamera
with picamera.PiCamera() as camera:
	camera.resolution = (640, 480)
	camera.framerate = 24
	server_socket = socket.socket()
	server_socket.bind(('0.0.0.0', 8000))
	server_socket.listen(0)
	while True:
		connection = server_socket.accept()[0].makefile('wb')
		camera.start_recording(connection, format='h264')

		connection.close()
		connection.flush()
