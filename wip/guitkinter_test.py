# Write your code here :-)
from tkinter import *
from tkinter import messagebox

# initialise main window
def init(win):
  win.title("Hello World application")
  win.minsize(800, 480)
  btn.pack()

# button callbacks
def photo():
  messagebox.showinfo("photo", "photo button was pressed!")

def select():
  messagebox.showinfo("select", "select button was pressed!")

def up():
  messagebox.showinfo("up", "up button was pressed!")

def down():
  messagebox.showinfo("down", "down button was pressed!")

def left():
  messagebox.showinfo("left", "left button was pressed!")

def right():
  messagebox.showinfo("right", "right button was pressed!")

def menu():
  messagebox.showinfo("menu", "menu button was pressed!")

# create top-level window
win = Tk()
positionRight = 0
positionDown = 0
win.geometry("+{}+{}".format(positionRight, positionDown))
select_btn = Button(win, text="select", command=select)
photo_btn = Button(win, text="photo", command=photo)
up_btn = Button(win, text="up", command=up)
down_btn = Button(win, text="down", command=down)
left_btn = Button(win, text="left", command=left
right_btn = Button(win, text="right", command=right)
menu_btn = Button(win, text="menu", command=menu)

# initialise and start main lophoto
init(win)
mainloop()
