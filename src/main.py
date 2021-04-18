# __author__  = Billal Fauzan
# __version__ = 1.0 

# Global module
from os.path import splitext
from os.path import isdir
from os import mkdir
from getpass import getuser

# Tkinter module
from tkinter import Tk
from tkinter import Button
from tkinter import Frame
from tkinter import Label
from tkinter import Entry
from tkinter import Text
from tkinter import StringVar
from tkinter import filedialog
from tkinter.filedialog import asksaveasfilename
from tkinter import messagebox
from tkinter.messagebox import askokcancel

# Tkinter position
from tkinter import N
from tkinter import X
from tkinter import LEFT
from tkinter import RIGHT
from tkinter import CENTER
from tkinter import BOTTOM
from tkinter import END
from tkinter import DISABLED
from tkinter import NORMAL

# pdf module
import pdf2image
from pdf2image.exceptions import PDFPageCountError

class PdfConverter(object):
    def __init__(self):
        self.root = Tk()
        self.frame = Frame(self.root)
        self.frame.pack(fill=X)

        self.input_path = ""
        self.output_path = ""
        self.username = getuser()

    def call_console(self, text="", typeC="INFO"):
        text = "[ " + typeC + " ] " + text + "\n"
        self.entry_console.configure(state=NORMAL)
        self.entry_console.insert(END, text)
        self.entry_console.configure(state=DISABLED)

    def createEntry(self):
        self.entry_input = Entry(self.frame, textvariable=StringVar())
        self.entry_input.delete(0, END)
        self.entry_input.insert(0, self.input_path)
        self.entry_input.grid(row=0, column=1, ipadx=50)

        self.entry_console = Text(self.frame, width=40)
        self.entry_console.configure(state=DISABLED)
        self.entry_console.grid(row=4, column=1, ipadx=0, ipady=50, pady=10, padx=0)

    def createLabel(self):
        Label(self.frame, text="Input file").grid(row=0, column=0)
        Label(self.frame, text="Console:" + " " * 90).grid(row=3, column=1)

    def createButton(self):
        Button(self.frame, text="Open", command=self.openFileAsk).grid(row=0, column=3, pady=0)
        Button(self.frame, text="Convert", command=self.convert).grid(row=1, column=1, pady=5)
        Button(self.frame, text="Information", command=self.information).grid(row=2, column=1, pady=0)

    def information(self):
        messagebox.showinfo("Credit", "Author: Billal Fauzan\nVersion: 1.0")

    def openFileAsk(self):
        self.call_console("Opening window file")
        extension = [("All Files", "*"), ("Pdf Files", "*.pdf")]
        openFile = filedialog.askopenfilename(filetypes=extension)
        if openFile != "":
            self.input_path = openFile
            try:
                if self.input_path.endswith(".pdf"):
                    self.call_console("File input: " + self.input_path)
                    self.entry_input.delete(0, END)
                    self.entry_input.insert(0, self.input_path)
                    filename = openFile.split("/")[-1]
                    filename = splitext(filename)
                    # print (filename)
                else:
                    self.call_console("Unable extension", typeC="ERROR")
                    messagebox.showwarning("Warning", "Unable extension")
                    self.input_path = ""
            except AttributeError:
                self.call_console("Reload window file")

    def convert(self):
        if self.input_path == "":
            self.call_console("Please choice a file", "WARN")
            messagebox.showwarning("Warning", "Please choice a file")
        else:
            try:
                mkdir("/home/" + self.username + "/pdf2image")
                self.call_console("Create a folder output")
            except OSError:
                self.call_console("Folder output is exist")
            self.call_console("Reading PDF...")
            try:
                pdf = pdf2image.convert_from_path(self.input_path, 300)
                self.call_console("Convert to image, please wait a minute")
                self.call_console("Starting to convert")
                i = 0
                for image in pdf:
                    i += 1
                    filename = self.input_path.split("/")[-1]
                    filename = "/home/" + self.username + "/pdf2image/" + splitext(filename)[0] + str(i) + ".png"
                    self.call_console("Saving to " + filename)
                    image.save(filename, "PNG")
                self.call_console("Success")
            except PDFPageCountError:
                self.call_console("Failed to count pages", "ERROR")
                messagebox.showerror("Failed", "Failed to count pages")

    def main(self):
        self.createLabel()
        self.createEntry()
        self.createButton()

        # Settings
        self.root.title("PDF Converter")
        self.root.geometry("500x500")
        self.root.mainloop()

if __name__ == "__main__":
    pdfconverter = PdfConverter()
    pdfconverter.main()
