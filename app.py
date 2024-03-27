from threading import Thread
import sounddevice as sd
import soundfile as sf
import tempfile
import queue
import numpy as np
import winsound
from faster_whisper import WhisperModel
import os
import time as pytime
from browser import Browser
from external_commands import ExternalCommands
from queue import Queue
from popup_window import init_popup

seconds_to_command = 2
silence_threshold = 0.025
silence_duration = 2
fs = 16000
should_listen = True

def generate_and_save_audio(audio_queue: queue.Queue, fs: int):
    global should_listen
    buffer = []
    recording = False
    listening = False
    silence_counter = 0
    silence_detected = False
    listen_start_time = 0

    def callback(indata, frames, time, status):
        nonlocal recording, listening, silence_counter, buffer, silence_detected, listen_start_time
        if not should_listen:
            return
        
        audio_data = indata[:, 0]
        current_time = pytime.time()
        
        if recording:
            buffer.extend(audio_data.tolist())
            if np.mean(np.abs(audio_data)) < silence_threshold:
                if not silence_detected:
                    silence_detected = True
                    silence_counter = current_time
                elif current_time - silence_counter >= silence_duration:
                    recording = False
                    silence_detected = False
                    audio_queue.put(np.array(buffer, dtype=np.float32))
                    buffer.clear()
                    silence_counter = 0
            else:
                silence_detected = False
                silence_counter = 0
        else:
            buffer.extend(audio_data.tolist())
            if np.mean(np.abs(audio_data)) > silence_threshold/2:
                if not listening:
                    listening = True
                    listen_start_time = current_time
                
            if listening and current_time - listen_start_time >= seconds_to_command:
                audio_chunk = np.array(buffer, dtype=np.float32)
                buffer.clear()
                listening = False
                transcribed_text = transcribe_audio(audio_chunk, model)
                normalized_text = ExternalCommands.normalize_message(transcribed_text)
                if "luma" in normalized_text:
                    print("Faça a sua solicitação")
                    winsound.Beep(440, 300)
                    recording = True

    with sd.InputStream(callback=callback, channels=1, samplerate=fs):
        print('Ouvindo...')
        while True:
            pytime.sleep(0.1)

def transcribe_audio(audio_data: np.ndarray, model: WhisperModel):
    temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    sf.write(temp_file.name, audio_data, fs)
    temp_file.close()
    segments, _ = model.transcribe(temp_file.name, beam_size=5, language="pt")
    transcribed_text = ' '.join([segment.text for segment in segments])
    print(transcribed_text)
    os.remove(temp_file.name)
    return transcribed_text

if __name__ == "__main__":
    popup_queue = Queue()
    tk_thread = Thread(target=init_popup, args=(popup_queue,))
    tk_thread.start()
    browser_class = Browser(popup_queue)
    model = WhisperModel("small", device="cuda", compute_type="int8_float16")
    audio_queue = queue.Queue()
    generator_thread = Thread(target=generate_and_save_audio, args=(audio_queue, fs))
    generator_thread.start()
    while True:
        audio_data = audio_queue.get()
        if audio_data is not None:
            should_listen = False
            transcribed_text = transcribe_audio(audio_data, model)
            notes = [(280, 300), (440, 300)]
            for freq, duration in notes:
                winsound.Beep(freq, duration)
            answer = browser_class.exec(transcribed_text)
            popup_queue.put(answer)
            print("Prompt finalizado, ouvindo...")
            should_listen = True
