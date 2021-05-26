#!/usr/bin/python
'''
trying to make a python equivalent for the linux command below
raspivid -n -ih -t 0 -rot 0 -w 1280 -h 720 -fps 15 -b 1000000 -o - | ncat -lkv4 9090
'''
import socket
from io import BytesIO
import time
import picamera
from threading import Thread

def stream_video_to_network(cam):
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 9090))
    server_socket.listen(0)
    while True:
        connection = server_socket.accept()[0].makefile('wb')
        cam.start_recording(connection, format='h264', resize=(640, 480))

def stream_video_to_memory(cam):
    stream = BytesIO()
    cam.start_recording(stream, format='mjpeg', quality=23)

camera = picamera.PiCamera()
# camera.resolution = (4056, 3040)
camera.resolution = (4056, 3040)
camera.framerate = 24
# Thread(target=stream_video_network, args=(camera,)).start()
Thread(target=stream_video_to_memory, args=(camera,)).start()
camera.start_recording('my_video1.h264', format='h264', resize=(640, 480), splitter_port=0)



import picamera
with picamera.PiCamera() as camera:
    camera.resolution = (1332, 990)
    camera.start_recording('my_video.h264')
    camera.start_recording('my_video1.h264', splitter_port=0)





server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 9090))
server_socket.listen(0)
connection = server_socket.accept()[0].makefile('wb')
camera.start_recording(connection, format='h264', resize=(640, 480), splitter_port=0)