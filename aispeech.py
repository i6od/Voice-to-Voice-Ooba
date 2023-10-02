import time
from pathlib import Path
import torch
import pyaudio
import wave
import sys
from array import array
from struct import pack

torch._C._jit_set_profiling_mode(False)


VOICE_OUTPUT_FILENAME = "audioResponse.wav"

#so sending input from file to file lol
device = torch.device('cpu')
sample_rate = 48000
speaker='en_21'
params = {
    'activate': True,
    'speaker': 'en_21',
    'language': 'en',
    'model_id': 'v3_en',
    'sample_rate': 48000,
    'device': 'cpu',
    'show_text': True,
    'autoplay': True,
    'voice_pitch': 'medium',
    'voice_speed': 'medium',
}

# why is it called oobapi for a function?????

def initialize(text):
        content = text
        
        model, example_text = torch.hub.load(repo_or_dir='snakers4/silero-models', model='silero_tts', language=params['language'], speaker=params['model_id'])
        model.to(params['device'])
        output_file = Path(f'audioResponse.wav')
        
        model.save_wav(text=content,
                        speaker=speaker,
                        sample_rate=sample_rate,audio_path=str(output_file))
        print("******************Ai SPEEKING***************************")




        CHUNK = 1024
        wf = wave.open("audioResponse.wav", 'rb')
        print("ai speaking:", content)
        p=pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
        data = wf.readframes(CHUNK)
        while len(data)>0:
            stream.write(data)
            data = wf.readframes(CHUNK)
            

        stream.stop_stream()
        stream.close()
        p.terminate()
        
        time.sleep(0.1)

    
if __name__ == '__main__':
    
    oobaapi()
    PlayAudio()
    
