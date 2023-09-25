from pickle import TRUE
import re
import speech_recognition as sr
import pyttsx3
import json
import requests
import traceback
import chatbot
import wave
import pyaudio
import whisper
from threading import Thread

whisper_filter_list = ['you', 'thank you.',
                       'thanks for watching.', "Thank you for watching."]

MIC_OUTPUT_FILENAME = "outfile.wav"
VOICE_OUTPUT_FILENAME = "audioResponse.wav"

logging_eventhandlers = []

def initialize_model():
    global model
    model = whisper.load_model("tiny")
    
auto_recording = False

def start_record_auto():
    global auto_recording
    auto_recording = True
    thread = Thread(target=start_STTS_loop_chat)
    thread.start()

def start_STTS_loop_chat():
    global auto_recording
    while auto_recording:
        listen()

def stop_record_auto():
    global auto_recording, ambience_adjusted
    auto_recording = False
    ambience_adjusted = False

def listen():
    r = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        r.adjust_for_ambient_noise(source, duration=0.2)
        print("Speak now")
        audio = r.listen(source)
        with open(MIC_OUTPUT_FILENAME, "wb") as file:
            file.write(audio.get_wav_data())
            print("Transcribing")
            global model
        initialize_model()
        audio = whisper.load_audio(MIC_OUTPUT_FILENAME)
        audio = whisper.pad_or_trim(audio)
        mel = whisper.log_mel_spectrogram(audio).to(model.device)
        options = whisper.DecodingOptions(task='transcribe',
                                          language='english', without_timestamps=True, fp16=False if model.device == 'cpu' else None)
        result = whisper.decode(model, mel, options)
        user_input = result.text
        global whisper_filter_list
        if (user_input == ''):
            return
        print(f'filtering')
        if (user_input.strip().lower() in whisper_filter_list):
            print(f'Input filtered.')
            return
        
        chatbot.send_user_input(user_input)
        return
        
def log_message(message_text):
    print(message_text)
    global logging_eventhandlers
    for eventhandler in logging_eventhandlers:
        eventhandler(message_text)

        
