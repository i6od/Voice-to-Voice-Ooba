from pickle import TRUE
import re
import json
import time
import requests
import traceback
import aispeech
import wave

import transcribe
message_log = []
AI_RESPONSE_FILENAME = 'ai-response.txt'
logging_eventhandlers = []
PORT = 5000
history = []

def send_user_input(user_input):
    global message_log
    print(message_log)
    log_message(f"User: {user_input}")
    message_log.append({"role": "user", "content": user_input})
    url = f'http://0.0.0.0:{PORT}/v1/chat/completions'
    headers = {"Content-Type": "application/json"}
    json = {
            "messages": [
                {"role": "system", "content": f"You are an ai assistant"},
                {"role": "user", "content": f"{user_input}"}
            ],
            "history": f"{history}",
            "stop": ["### Instruction:"],
            "temperature": 0.7,
            "max_tokens": 800,
            "stream": False
        }
    
    response = requests.post(url, headers=headers, json=json)
    if response.status_code == 200:
        result = response.json()['choices'][0]['message']['content']
        history.append({"role": "system", "content": result } )
        history.append({"role": "user", "content": user_input } )
        text = result
        log_message(f'{text}')
        aispeech.initialize(text)
        time.sleep(0.1)
        
                    
        


def log_message(message_text):
    print(message_text)
    global logging_eventhandlers
    for eventhandler in logging_eventhandlers:
        eventhandler(message_text)
