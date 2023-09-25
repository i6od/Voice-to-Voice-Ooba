import customtkinter as ctk
import json
from threading import Thread

import keyboard
import pyaudio

from threading import Event
from enum import Enum
import sounddevice as sd
import speech_recognition as sr
import numpy as np
import time

import chatbot
import transcribe
import aispeech

pageChange_eventhandlers = []


class ChatFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        global current_page
        super().__init__(master, **kwargs)

        self.isRecording = False
        self.thread = Thread(target=transcribe.start_record_auto)
        # add widgets onto the frame...
        self.textbox = ctk.CTkTextbox(self, width=400, height=400)
        self.textbox.grid(row=0, column=0, rowspan=4, columnspan=4)
        # configure textbox to be read-only
        self.textbox.configure(state="disabled")
        chatbot.logging_eventhandlers.append(self.log_message_on_console)

        self.user_input_var = ctk.StringVar(self, '')
        self.voicevox_api_key_input = ctk.CTkEntry(
            master=self, textvariable=self.user_input_var, width=200)
        self.voicevox_api_key_input.grid(
            row=4, column=0, padx=10, pady=10, sticky='W', columnspan=2)
        self.send_button = ctk.CTkButton(master=self,
                                                   width=32,
                                                   height=32,
                                                   border_width=0,
                                                   corner_radius=8,
                                                   text="send",
                                                   command=self.send_user_input,
                                                   fg_color='grey'
                                                   )
        self.send_button.grid(row=4, column=2, pady=10)
        self.recordButton = ctk.CTkButton(master=self,
                                                    width=120,
                                                    height=32,
                                                    border_width=0,
                                                    corner_radius=8,
                                                    text="Start Recording",
                                                    command=self.recordButton_callback,
                                                    fg_color='grey'
                                                    )
        self.recordButton.grid(row=4, column=3, pady=10)
    def clear_console(self):
        self.textbox.configure(state="normal")
        self.textbox.delete('1.0', ctk.END)
        self.textbox.configure(state="disabled")

    def send_user_input(self):
        text = self.user_input_var.get()
        self.user_input_var.set('')
        thread = Thread(target=chatbot.send_user_input, args=[text,])
        thread.start()

    def recordButton_callback(self):
        if (self.isRecording):
            self.recordButton.configure(
                text="Start Recording", fg_color='grey')
            self.isRecording = False
            transcribe.stop_record_auto()
        else:
            self.recordButton.configure(
                text="Stop Recording", fg_color='#fc7b5b')
            self.isRecording = True
            transcribe.start_record_auto()

    def log_message_on_console(self, message_text):
        # insert at line 0 character 0
        self.textbox.configure(state="normal")
        self.textbox.insert(ctk.INSERT, message_text+'\n')
        self.textbox.configure(state="disabled")
        self.textbox.see("end")

class SidebarFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        global current_page
        super().__init__(master, **kwargs)

        chat_button = ctk.CTkButton(master=self,
                                              width=120,
                                              height=32,
                                              border_width=0,
                                              corner_radius=0,
                                              text="Chat",
                                              fg_color='grey'
                                              )
        chat_button.pack(anchor="s")
    def change_page(self, page):
        global current_page
    current_page = ""

    global pageChange_eventhandlers
    for eventhandler in pageChange_eventhandlers:
        eventhandler()

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x500")
        self.title("Voice to Voice Ooba Api")
        self.resizable(False, False)

        sidebar = SidebarFrame(master=self, width=25, height=500)
        sidebar.grid(row=0, column=0, padx=20,
                     pady=20, sticky="nswe")
        container = ChatFrame(
            master=self, width=600, height=500, bg_color='#f0f0f0')
        container.grid(row=0, column=1, padx=5,
                       pady=20, sticky="nswe")

        
        

app = App()
app.configure(background='#fafafa')
app.mainloop()


