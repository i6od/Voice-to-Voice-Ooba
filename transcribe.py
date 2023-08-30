# Import necessary libraries
import os
from pickle import TRUE
import re
import speech_recognition as sr
import pyttsx3
import json
import time
import requests
import traceback
import chatbot
import wave
import pyaudio
import whisper

whisper_filter_list = ['you', 'thank you.',
                       'thanks for watching.', "Thank you for watching."]
MIC_OUTPUT_FILENAME = "PUSH_TO_TALK_OUTPUT_FILE.wav"
VOICE_OUTPUT_FILENAME = "audioResponse.wav"
# Speech Recognizer

r = sr.Recognizer()
print("Loading Speech Recognizer")

def initialize_model():
    global model
    model = whisper.load_model("tiny")

def listen():
    mic = sr.Microphone()
    with mic as source:
        r.adjust_for_ambient_noise(source, duration=0.2)
        print("Speak now")
        audio = r.listen(source)
        with open(MIC_OUTPUT_FILENAME, "wb") as file:
            file.write(audio.get_wav_data())
            print("sending to whisper")
        global model
        initialize_model()
        audio = whisper.load_audio(MIC_OUTPUT_FILENAME)
        audio = whisper.pad_or_trim(audio)
        mel = whisper.log_mel_spectrogram(audio).to(model.device)
        options = whisper.DecodingOptions(task='transcribe',
                                          language='english', without_timestamps=True, fp16=False if model.device == 'cpu' else None)
        result = whisper.decode(model, mel, options)
        
        
        user_input = result.text
        print("You:", user_input)
        chatbot.ooba_api(user_input)

        return 
        

if __name__ == "__main__":
    while True:
        time.sleep(1)
        listen()

        