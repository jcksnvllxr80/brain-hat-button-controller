#!/usr/bin/python
'''
trying to make a python equivalent for the linux command below
raspivid -n -ih -t 0 -rot 0 -w 1280 -h 720 -fps 15 -b 1000000 -o - | ncat -lkv4 9090
'''
import socket
import time
import picamera
from threading import Thread

def stream_video(thread_name, server_socket, cam):
	while True:
		connection = server_socket.accept()[0].makefile('wb')
		cam.start_recording(connection, format='h264')

camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate = 24
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)
Thread(target=stream_video, args=('stream video', server_socket, camera)).start()
camera.start_recording('my_video1.h264', splitter_port=0)
camera.wait_recording(60)
camera.stop_recording(splitter_port=0)


import picamera
with picamera.PiCamera() as camera:
    camera.resolution = (1332, 990)
    camera.start_recording('my_video.h264')
    camera.start_recording('my_video1.h264', splitter_port=0)
