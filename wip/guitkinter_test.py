# Write your code here :-)
from tkinter import *
from tkinter import messagebox
 
# initialise main window
def init(win):
win.title("Hello World application")
win.minsize(500, 100)
btn.pack()
 
# button callback
def hello():
messagebox.showinfo("Hello", "Pleased to meet you!")
 
# create top-level window
win = Tk()
 
# Gets the requested values of the height and widht.
windowWidth = win.winfo_reqwidth()
windowHeight = win.winfo_reqheight()
 
# Gets both half the screen width/height and window width/height
positionRight = int(win.winfo_screenwidth()/2 - windowWidth/2)
positionDown = int(win.winfo_screenheight()/2 - windowHeight/2)
 
# Positions the window in the center of the page.
win.geometry("+{}+{}".format(positionRight, positionDown))
 
# create a button
btn = Button(win, text="Hello", command=hello)
 
# initialise and start main loop
init(win)
mainloop()