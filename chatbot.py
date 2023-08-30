
# Import necessary libraries
import os
from pickle import TRUE
import re
import json
import time
import requests
import traceback
import aispeech
import wave





def ooba_api(user_input):
            print(f"Sending: {user_input} to OOBABOOGA API")
            
            
            uri = 'http://127.0.0.1:5000/api/v1/chat'

            request = {
                'user_input': user_input,
                'max_new_tokens': 50,
                'auto_max_new_tokens': False,
        
                'mode': 'chat',  # Valid options: 'chat', 'chat-instruct', 'instruct'
                'character': 'Example',
                'instruction_template': 'Samantha',  # Will get autodetected if unset
            
                # 'name1': 'name of user', # Optional
                # 'name2': 'name of character', # Optional
                # 'context': 'character context', # Optional
                # 'greeting': 'greeting', # Optional
                # 'name1_instruct': 'You', # Optional
                # 'name2_instruct': 'Assistant', # Optional
                # 'context_instruct': 'context_instruct', # Optional
                # 'turn_template': 'turn_template', # Optional
                'regenerate': False,
                '_continue': False,
                'stop_at_newline': False,
                'chat_generation_attempts': 1,
                'chat-instruct_command': 'Continue the chat dialogue below. Write a single reply for the character "<|character|>".\n\n<|prompt|>',

                # Generation params. If 'preset' is set to different than 'None', the values
                # in presets/preset-name.yaml are used instead of the individual numbers.
                'preset': 'Midnight Enigma',
                'do_sample': True,
                'temperature': 0.7,
                'top_p': 0.1,
                'typical_p': 1,
                'epsilon_cutoff': 0,  # In units of 1e-4
                'eta_cutoff': 0,  # In units of 1e-4
                'tfs': 1,
                'top_a': 0,
                'repetition_penalty': 1.18,
                'repetition_penalty_range': 0,
                'top_k': 40,
                'min_length': 0,
                'no_repeat_ngram_size': 0,
                'num_beams': 1,
                'penalty_alpha': 0,
                'length_penalty': 1,
                'early_stopping': False,
                'mirostat_mode': 0,
                'mirostat_tau': 5,
                'mirostat_eta': 0.1,

                'seed': -1,
                'add_bos_token': True,
                'truncation_length': 2048,
                'ban_eos_token': False,
                'skip_special_tokens': True,
                'stopping_strings': ["\n\n", "Observation:"]
                }
            response = requests.post(uri, json=request)
            if response.status_code == 200:
                    result = response.json()['results'][0]['history']
                    
                    text = result["visible"][0][1]
                    print('Sending Ai Response to Generate Speech')
                    
                    aispeech.oobaapi(text)

                    time.sleep(0.1)

if __name__ == '__main__':

    ooba_api()