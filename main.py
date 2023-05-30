#!/usr/bin/env python3

import os
import can
import tkinter as tk

def translate(dlc, data):
    data = 0
    for i in range(dlc):
        data += (data[i] * (10 ** i))

    return data


class GUI_Window:
    def __init__(self):
        os.system('sudo ip link set can0 type can bitrate 500000')
        os.system('sudo ifconfig can0 up')
        self.can0 = can.interface.Bus(channel='can0', bustype='socketcan')

        self.window = tk.Tk()
        self.window.title("Le GUI")

        self.main_frame = tk.Frame(master=self.window)
        self.main_frame.pack()

        self.setup_rows()

        self.state = False

        self.window.attributes('-fullscreen', True)
        self.window.bind("<Escape>", self.end_fullscreen)

    def end_fullscreen(self, event=None):
        self.state = False
        self.window.attributes("-fullscreen", False)

        width = self.window.winfo_screenwidth() / 2
        height= self.window.winfo_screenheight() / 2
        self.window.geometry("%dx%d" % (width, height))
        return "break"

    def setup_rows(self):
        self.r1_frame = tk.Frame(master=self.window)
        self.r1_frame.pack(fill = tk.BOTH, expand=True)

        self.r1_label = tk.Label(master=self.r1_frame, text="value goes here", font='Arial 100 bold')
        self.r1_label.place(relx = 0.5, rely = 0.5, anchor=tk.CENTER)
        # self.r1_label.pack(fill = tk.BOTH)

    def update(self):

        # receive the new number
        msg = self.can0.recv(1.0)
        data = "–"

        if msg is not None and msg.arbitration_id == 0x190:
            data = translate(msg.dlc, msg.data)
        
        self.r1_label['text'] = data
        
        self.window.after(100, self.update)

if __name__ == "__main__":
    gui = GUI_Window()
    gui.update()

    gui.window.mainloop() # never actually run...
