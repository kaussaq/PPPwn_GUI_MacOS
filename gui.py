import tkinter as tk
import tkinter.ttk
from tkinter import *
from tkinter import filedialog
import os
import psutil
import subprocess
import customtkinter
import sys


class ConsoleRedirector:
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        self.widget.insert(tk.END, text)
        self.widget.see(tk.END)  # Auto-scroll to the bottom

def run_script():
    # take selected interface from drop down
    chosen_int = interfaces_dropdown.get()

    # Run script command
    script_path = "pppwn.py"  # Replace with your script path
    process = subprocess.Popen(["python3", "pppwn.py", "--interface="+ chosen_int], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    #process = subprocess.run(["python3", "pppwn.py", "--interface=" + chosen_int])

    #Redirect stdout and stderr to the console widget
    sys.stdout = ConsoleRedirector(console_text)
    sys.stderr = ConsoleRedirector(console_text)

    # Capture and display the output
    for line in process.stdout:
        print(line, end="")
    for line in process.stderr:
        print(line, end="")

    # Restore stdout and stderr
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

#get user name of machine to work in file path starting directory to not confuse user
username = os.getlogin()

# ------------------------
#   Application-GUI
# ------------------------

#Create Frame of Application and window title
root = customtkinter.CTk()
root.title('PPPwn GUI Mac-Intel/ARM')

frame=customtkinter.CTkFrame(master=root)
frame.pack(pady=10, padx=10, fill="both", expand=True)

# Create a scrolled text widget for displaying the console output
console_text = customtkinter.CTkTextbox(frame, wrap=tk.WORD, width=500, height=500)
console_text.pack(anchor="center", pady=10, padx=10) #Anchor the console box to the middle of the screen and add some padding
console_text.configure(scrollbar_button_color="", scrollbar_button_hover_color="") #Make scroll-bar invisible
font_spec = ("Cascadia Code", 12)  # Font family and size

#Ask for Stage2.bin file location for payload to be injected
root.filename = filedialog.askopenfilename(initialdir=("/Users/" + username + "/"), title="Select Stage2.bin")

#paste output of file location onto Gui
bin2_filepath = Label(root, text="Injected Stage2.bin file is: " + root.filename)
bin2_filepath.pack(anchor=tkinter.W)

#replace stage2.bin in script dir with one selected by user
os.replace(root.filename, "stage2/stage2.bin")


#Take list of all interfaces on machine
niclist = list(psutil.net_io_counters(pernic=True))

#Create Dropdown menu with list of available interfaces on the device
choices=niclist
interfaces_dropdown_label=tkinter.Label(root, text="Select PPPwn Interface")
interfaces_dropdown_label.pack(anchor=tkinter.W, pady=10)
interfaces_dropdown = tkinter.ttk.Combobox(root, values=choices)
interfaces_dropdown.pack(anchor=tkinter.W)

#Create button to begin exploit
jbbutton = Button(root, text="JailBreak", command=run_script)
jbbutton.pack()



root.mainloop()
