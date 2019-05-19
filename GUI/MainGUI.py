from tkinter import *
from tkinter import filedialog
import tkinter as TKINTER

def setSourceFolder():
    file = filedialog.askopenfilename()
    txt.insert(0, str(file))


def print():
   t = ""
   targetsize.getvar("t")
   print(t)

window = Tk()

window.title("Welcome to the ply converter")
window.grid_columnconfigure(1, minsize=10)
window.geometry('1260x720')

lbl = Label(window, text="Model source files folder")
lbl.grid(column=0, row=0)

txt = Entry(window, width=122)
txt.grid(column=0, row=1, columnspan=3)
selectfolderbtn = Button(window, text="Select folder", command=setSourceFolder)
selectfolderbtn.grid(column=4, row=1)

lbl2 = Label(window, text="Settings:")
lbl2.grid(column=0, sticky=TKINTER.W, row=4)

targetsizelabel = Label(window, text="targetsize")
targetsizelabel.grid(column=0, sticky=TKINTER.W, row=5)
targetsize = Entry(window, width=122)
targetsize.grid(column=1, sticky=TKINTER.W, row=5)

vertexlimitlabel = Label(window, text="vertexlimit")
vertexlimitlabel.grid(column=0, sticky=TKINTER.W, row=6)
vertexlimit = Entry(window, width=122)
vertexlimit.grid(column=1, sticky=TKINTER.W, row=6)

smoothinglabel = Label(window, text="smoothing")
smoothinglabel.grid(column=0, sticky=TKINTER.W, row=7)
smoothing = Checkbutton(window, width=122)
smoothing.grid(column=1, sticky=TKINTER.W, row=7)

decimatelabel = Label(window, text="decimate")
decimatelabel.grid(column=0, sticky=TKINTER.W, row=8)
decimate = Checkbutton(window, width=122)
decimate.grid(column=1, sticky=TKINTER.W, row=8)

exporttofbxlabel = Label(window, text="exporttofbx")
exporttofbxlabel.grid(column=0, sticky=TKINTER.W, row=9)
exporttofbx = Checkbutton(window, width=122)
exporttofbx.grid(column=1, sticky=TKINTER.W, row=9)

filetypetoimportlabel = Label(window, text="filetypetoimport")
filetypetoimportlabel.grid(column=0, sticky=TKINTER.W, row=10)
filetypetoimport = Entry(window, width=122)
filetypetoimport.grid(column=1, sticky=TKINTER.W, row=10)

startbtn = Button(window, text="Start", command=print)
startbtn.grid(column=0, sticky=TKINTER.W, row=11)

window.mainloop()