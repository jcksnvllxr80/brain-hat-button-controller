# Write your code here :-)
from tkinter import *
from tkinter import messagebox

# initialise main window
def init(win):
  win.title("Hello World application")
  win.minsize(800, 480)
  select_btn.pack()
  photo_btn.pack()
  up_btn.pack()
  down_btn.pack()
  left_btn.pack()
  right_btn.pack()
  menu_btn.pack()

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

select_btn = Button(win, text="select", command=select, width=10, justify="left")
photo_btn = Button(win, text="photo", command=photo, width=10, justify="left")
up_btn = Button(win, text="up", command=up, width=10, justify="left")
down_btn = Button(win, text="down", command=down, width=10, justify="left")
left_btn = Button(win, text="left", command=left, width=10, justify="left")
right_btn = Button(win, text="right", command=right, width=10, justify="left")
menu_btn = Button(win, text="menu", command=menu, width=10, justify="left")

# initialise and start main lophoto
init(win)
mainloop()
