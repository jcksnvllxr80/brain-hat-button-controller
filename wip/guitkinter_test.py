import tkinter as tk
from tkinter import messagebox
import time

class button_with_timer(tk.Button):

  def __init__(self, container, text, command, width, height):
    self.container = container
    tk.Button.__init__(self, self.container, text=text, command=command, width=width, height=height)
    self.bind("<ButtonPress>", self.on_press)
    self.bind("<ButtonRelease>", self.on_release)
    self.button_press_time = 0
    self.button_release_time = 0
    self.long_press = False

  def on_press(self, button):
    self.button_press_time = time.time()
    # self.log("button was pressed at {0}".format(self.button_press_time))

  def on_release(self, button):
    self.button_release_time = time.time()
    # self.log("button was released at {0}".format(self.button_release_time))
    delta = self.button_release_time - self.button_press_time
    if delta > 0.75:
      self.long_press = True
    else:
      self.long_press = False 
    self.log("\ndelta:\n{0:.2f}\npress:\n{1}".format(delta, "long" if self.long_press else "short"))

  def log(self, message):
    now = time.strftime("%I:%M:%S", time.localtime())
    print("{}\n{}".format(now, message.strip()))
    text_area.delete('1.0', tk.END)
    text_area.insert("end", "{}\n{}".format(now, message.strip()))
    text_area.see("end")

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
  text_area.pack()

# button callbacks
def photo():
  tk.messagebox.showinfo("photo", "photo button was pressed!")

def select():
  tk.messagebox.showinfo("select", "select button was pressed!")

def up():
  tk.messagebox.showinfo("up", "up button was pressed!")

def down():
  tk.messagebox.showinfo("down", "down button was pressed!")

def left():
  tk.messagebox.showinfo("left", "left button was pressed!")

def right():
  tk.messagebox.showinfo("right", "right button was pressed!")

def menu():
  tk.messagebox.showinfo("menu", "menu button was pressed!")

# create top-level window
win = tk.Tk()
win.attributes('-alpha',0.5)
left_button_frame = tk.Frame(win)
left_button_frame.pack(fill=tk.X, side=tk.LEFT)
right_button_frame = tk.Frame(win)
right_button_frame.pack(fill=tk.X, side=tk.RIGHT)

positionRight = 0
positionDown = 0
win.geometry("+{}+{}".format(positionRight, positionDown))

text_area = tk.Text(right_button_frame, height=10, width=8)
select_btn = button_with_timer(right_button_frame, text="select", command=select, width=8, height=3)
photo_btn = button_with_timer(right_button_frame, text="photo", command=photo, width=8, height=3)
up_btn = button_with_timer(left_button_frame, text="up", command=up, width=8, height=3)
down_btn = button_with_timer(left_button_frame, text="down", command=down, width=8, height=3)
left_btn = button_with_timer(left_button_frame, text="left", command=left, width=8, height=3)
right_btn = button_with_timer(left_button_frame, text="right", command=right, width=8, height=3)
menu_btn = button_with_timer(right_button_frame, text="menu", command=menu, width=8, height=3)


# initialise and start main lophoto
init(win)
tk.mainloop()
