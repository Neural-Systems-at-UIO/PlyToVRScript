from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Progressbar
from tkinter import messagebox
import tkinter as TKINTER
import sys
import os
sys.path.append(str(os.path.realpath(os.path.join(__file__, "../.."))))
from ConfigurationManager import Configuration
from ConfigurationManager import ConfigWriter
from ConfigurationManager import ConfigReader
import ast
import subprocess
import threading
import winsound

def printGUI(text):
    outputTextBox.configure(state='normal')
    outputTextBox.insert('end', text)
    outputTextBox.configure(state='disabled')
    outputTextBox.see(END)


def startBlenderThread(configuration):
    clickedYes = messagebox.askyesno("Confirm run",
                                     'Decimate er satt til ' + str(configuration.decimate) +': ' + vertexlimit.get() +
                                     '.\nDouble check the settings!\nDont forget:\nMake sure that the files selected '
                                     'are locally available (i.e. not a network drive)\nDelete messages are '
                                     'expected!\nMake sure the computer will not power down during the process. A '
                                     'laptop running on battery will take longer.\nA single model can use up to a few '
                                     'hours depending on size, complexity and host hardware.\nMultiple models will '
                                     'require a much longer period of time to complete.\nIf the colours seem off or '
                                     'are missing, refer to the readme.')
    if not clickedYes:
        return
    p_bar.start(5)
    runbtn.config(state="disabled")
    storeConfiguration()
    print("Running blender...")
    printGUI("Running blender...")
    command = ["blender", "--python", "BlenderTest.py"]
    if openGUI.get() is 0:
        command.insert(1, "--background")
    
    blenderProcess = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                      universal_newlines=True)
    for stdout_line in iter(blenderProcess.stdout.readline, ""):
        print(stdout_line)
        printGUI(stdout_line)
    
    for stdout_line in iter(blenderProcess.stderr.readline, ""):
        print(stdout_line)
        printGUI(stdout_line)
    
    blenderProcess.stdout.close()
    blenderProcess.stderr.close()
    
    confgReader = ConfigReader.ConfigReader()
    configuration = confgReader.readConfig()
    configuration.executedFromBlender = True
    confgWriter = ConfigWriter.ConfigWriter()
    confgWriter.storeConfig(configuration)
    runbtn.config(state="normal")
    p_bar.stop()
    
    duration = 1000  # milliseconds
    freq = 440  # Hz
    winsound.Beep(freq, duration)


# return_code = blenderProcess.wait()
# if return_code:
#     raise subprocess.CalledProcessError(return_code, command)

def runCommand():
    confgReader = ConfigReader.ConfigReader()
    configuration = confgReader.readConfig()
    configuration.executedFromBlender = False
    confgWriter = ConfigWriter.ConfigWriter()
    confgWriter.storeConfig(configuration)
    
    t = threading.Thread(target=startBlenderThread(configuration))
    t.daemon = True  # close pipe if GUI process exits
    t.start()


def setSourceFolder():
    file = filedialog.askdirectory()
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
    configuration.targetSize = ast.literal_eval("[" + targetsize.get() + "]")
    configuration.exportToFBX = bool(exporttofbx.get())
    configuration.folderPath = sourceFolder.get()
    configuration.vertexLimit = int(vertexlimit.get())
    configuration.fileTypeToImport = ast.literal_eval(
        "[\'" + "".join(filetypetoimport.get().split()).replace(",", "\',\'") + "\']")
    confgWriter = ConfigWriter.ConfigWriter()
    confgWriter.storeConfig(configuration)
    printConfiguration(configuration)
    printGUI("Configuration stored successfully!\n")


def loadConfiguration():
    confgReader = ConfigReader.ConfigReader()
    configuration = confgReader.readConfig()
    decimate.set(configuration.decimate)
    smoothing.set(configuration.smoothing)
    targetsize.delete(0, 'end')
    targetsize.insert(0, str(','.join(str(e) for e in configuration.targetSize)))
    exporttofbx.set(configuration.exportToFBX)
    sourceFolder.delete(0, 'end')
    sourceFolder.insert(0, configuration.folderPath)
    vertexlimit.delete(0, 'end')
    vertexlimit.insert(0, configuration.vertexLimit)
    filetypetoimport.delete(0, 'end')
    filetypetoimport.insert(0, str(','.join(configuration.fileTypeToImport)))
    printConfiguration(configuration)
    printGUI("Configuration loaded successfully!\n")


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

targetsizelabel = Label(window, text="Target size")
targetsizelabel.grid(column=0, sticky=TKINTER.W, row=5)
targetsize = Entry(window, width=122)
targetsize.grid(column=1, sticky=TKINTER.W, row=5)

vertexlimitlabel = Label(window, text="Vertex limit")
vertexlimitlabel.grid(column=0, sticky=TKINTER.W, row=6)
vertexlimit = Entry(window, width=122)
vertexlimit.grid(column=1, sticky=TKINTER.W, row=6)

smoothinglabel = Label(window, text="Smoothing")
smoothinglabel.grid(column=0, sticky=TKINTER.W, row=7)
smoothing = IntVar()
Checkbutton(window, width=122, variable=smoothing).grid(column=1, sticky=TKINTER.W, row=7)

decimatelabel = Label(window, text="Decimate")
decimatelabel.grid(column=0, sticky=TKINTER.W, row=8)
decimate = IntVar()
Checkbutton(window, width=122, variable=decimate).grid(column=1, sticky=TKINTER.W, row=8)

exporttofbxlabel = Label(window, text="Export to FBX")
exporttofbxlabel.grid(column=0, sticky=TKINTER.W, row=9)
exporttofbx = IntVar()
Checkbutton(window, width=122, variable=exporttofbx).grid(column=1, sticky=TKINTER.W, row=9)

filetypetoimportlabel = Label(window, text="File types to import")
filetypetoimportlabel.grid(column=0, sticky=TKINTER.W, row=10)
filetypetoimport = Entry(window, width=122)
filetypetoimport.grid(column=1, sticky=TKINTER.W, row=10)

storeButton = Button(window, text="Store config", command=storeConfiguration)
storeButton.grid(column=0, sticky=TKINTER.W, row=11)

readButton = Button(window, text="Load config", command=loadConfiguration)
readButton.grid(column=1, sticky=TKINTER.W, row=11)

runbtn = Button(window, text="Run", command=runCommand)
runbtn.grid(column=2, sticky=TKINTER.W, row=11)

txt_frm = Frame(window, width=108, height=20)
txt_frm.grid(column=0, sticky=TKINTER.W, row=14, columnspan=3)
outputTextBox = Text(txt_frm, width=108, state='disabled', height=20)
outputTextBox.grid(row=0, column=0)
scrollb = Scrollbar(txt_frm, command=outputTextBox.yview)
scrollb.grid(row=0, column=1, sticky='nsew')
outputTextBox['yscrollcommand'] = scrollb.set

openGUIlabel = Label(window, text="View model in Blender")
openGUIlabel.grid(column=1, sticky=TKINTER.E, row=12)
openGUI = IntVar()
Checkbutton(window, variable=openGUI).grid(column=2, sticky=TKINTER.W, row=12)

p_bar = Progressbar(window, orient=HORIZONTAL, length=100, mode='indeterminate')
p_bar.grid(row=15, columnspan=1, column=0, sticky=TKINTER.W)

loadConfiguration()

window.mainloop()
