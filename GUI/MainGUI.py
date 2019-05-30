from tkinter import *
from tkinter import filedialog
import tkinter as TKINTER
from ConfigurationManager import Configuration
from ConfigurationManager import ConfigWriter
from ConfigurationManager import ConfigReader
import ast


def setSourceFolder():
	file = filedialog.askopenfilename()
	sourceFolder.delete(0, 'end')
	sourceFolder.insert(0, str(file))

def printConfiguration(configuration):
	print("Target Size: " + str(type(configuration.targetSize)) + " : " + str(configuration.targetSize))
	print("Vertex Limit: " + str(type(configuration.vertexLimit)) + " : " + str(configuration.vertexLimit))
	print("Smoothing: " + str(type(configuration.smoothing)) + " : " + str(configuration.smoothing))
	print("Decimate: " + str(type(configuration.decimate)) + " : " + str(configuration.decimate))
	print("ExportToFbx: " + str(type(configuration.exportToFBX)) + " : " + str(configuration.exportToFBX))
	print("File Types: " + str(type(configuration.fileTypeToImport)) + " : " + str(configuration.fileTypeToImport))
	print("Source file path: " + str(type(configuration.folderPath)) + " : " + str(configuration.folderPath))

def storeConfiguration():
	configuration = Configuration.Configuration()
	configuration.decimate = bool(decimate.get())
	configuration.smoothing = bool(smoothing.get())
	configuration.targetSize = ast.literal_eval(targetsize.get())
	configuration.exportToFBX = bool(exporttofbx.get())
	configuration.folderPath = sourceFolder.get()
	configuration.vertexLimit = int(vertexlimit.get())
	configuration.fileTypeToImport = ast.literal_eval(filetypetoimport.get())
	confgWriter = ConfigWriter.ConfigWriter()
	confgWriter.storeConfig(configuration)
	printConfiguration(configuration)

def loadConfiguration():
	confgReader = ConfigReader.ConfigReader()
	configuration = confgReader.readConfig()
	decimate.set(configuration.decimate)
	smoothing.set(configuration.smoothing)
	targetsize.delete(0, 'end')
	targetsize.insert(0, str(configuration.targetSize))
	exporttofbx.set(configuration.exportToFBX)
	sourceFolder.delete(0, 'end')
	sourceFolder.insert(0, configuration.folderPath)
	vertexlimit.delete(0, 'end')
	vertexlimit.insert(0, configuration.vertexLimit)
	filetypetoimport.delete(0, 'end')
	filetypetoimport.insert(0, str(configuration.fileTypeToImport))
	printConfiguration(configuration)


window = Tk()

window.title("Welcome to the ply converter")
window.grid_columnconfigure(1, minsize=10)
window.geometry('1260x720')

lbl = Label(window, text="Model source files folder")
lbl.grid(column=0, row=0)

sourceFolder = Entry(window, width=122)
sourceFolder.grid(column=1, row=0, sticky=TKINTER.W, columnspan=3)
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

startbtn = Button(window, text="Start", command=storeConfiguration)
startbtn.grid(column=0, sticky=TKINTER.W, row=11)

startbtn = Button(window, text="Read and print", command=loadConfiguration)
startbtn.grid(column=1, sticky=TKINTER.W, row=11)

window.mainloop()
