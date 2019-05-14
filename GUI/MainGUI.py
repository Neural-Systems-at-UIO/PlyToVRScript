from tkinter import *
from tkinter import filedialog

def setSourceFolder():
    file = filedialog.askopenfilename()
    txt.insert(0, str(file))

#Make these into hardcoded settings.
fields = ["targetsize", "vertexlimit", "smoothing", "decimate", "folderpath", "exporttofbx", "filetypetoimport"]

def fetch(entries):
   for entry in entries:
      field = entry[0]
      text  = entry[1].get()
      print('%s: "%s"' % (field, text))

def makeform(root, fields):
   entries = []
   offset = 5
   for field in fields:
      lab = Label(width=15, text=field, anchor='w')
      ent = Entry(width=100)
      lab.grid(column=0, row=offset)
      ent.grid(column=1, row=offset)
      entries.append((field, ent))
      offset = offset + 1

   return entries

window = Tk()

window.title("Welcome to the ply converter")
window.grid_columnconfigure(1, minsize=10)
window.geometry('1260x720')

lbl = Label(window, text="Model source files folder")

lbl.grid(column=0, row=0)

btn = Button(window, text="Select folder", command=setSourceFolder)

btn.grid(column=4, row=1)

txt = Entry(window, width=122)

txt.grid(column=0, row=1, columnspan=3)

lbl2 = Label(window, text="Settings:                    ")

lbl2.grid(column=0, row=4)

ents = makeform(window, fields)
window.bind('<Return>', (lambda event, e=ents: fetch(e)))


window.mainloop()