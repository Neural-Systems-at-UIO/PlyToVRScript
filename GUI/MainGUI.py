from tkinter import *
from tkinter import filedialog
import tkinter as TKINTER


def setSourceFolder():
	file = filedialog.askopenfilename()
	txt.insert(0, str(file))


def customPrint():
	print("Target Size: " + str(targetsize.get()))
	print("Vertex Limit: " + str(vertexlimit.get()))
	print("Smoothing: " + str(smoothing.get()))
	print("Decimate: " + str(decimate.get()))
	print("ExportToFbx: " + str(exporttofbx.get()))
	print("File Types: " + str(filetypetoimport.get()))
	print("Source file path: " + str(txt.get()))


window = Tk()

window.title("Welcome to the ply converter")
window.grid_columnconfigure(1, minsize=10)
window.geometry('1260x720')

lbl = Label(window, text="Model source files folder")
lbl.grid(column=0, row=0)

txt = Entry(window, width=122)
txt.grid(column=1, row=0, sticky=TKINTER.W, columnspan=3)
selectfolderbtn = Button(window, text="Select folder", command=setSourceFolder)
selectfolderbtn.grid(column=2, sticky=TKINTER.W, row=0)

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
smoothing = IntVar()
Checkbutton(window, width=122, variable=smoothing).grid(column=1, sticky=TKINTER.W, row=7)

decimatelabel = Label(window, text="decimate")
decimatelabel.grid(column=0, sticky=TKINTER.W, row=8)
decimate = IntVar()
Checkbutton(window, width=122, variable=decimate).grid(column=1, sticky=TKINTER.W, row=8)

exporttofbxlabel = Label(window, text="exporttofbx")
exporttofbxlabel.grid(column=0, sticky=TKINTER.W, row=9)
exporttofbx = IntVar()
Checkbutton(window, width=122, variable=exporttofbx).grid(column=1, sticky=TKINTER.W, row=9)

filetypetoimportlabel = Label(window, text="filetypetoimport")
filetypetoimportlabel.grid(column=0, sticky=TKINTER.W, row=10)
filetypetoimport = Entry(window, width=122)
filetypetoimport.grid(column=1, sticky=TKINTER.W, row=10)

startbtn = Button(window, text="Start", command=customPrint)
startbtn.grid(column=0, sticky=TKINTER.W, row=11)

window.mainloop()
