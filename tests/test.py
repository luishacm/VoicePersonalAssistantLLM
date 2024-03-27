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

silence_threshold = 0.025
silence_duration = 2
fs = 16000

def generate_and_save_audio(audio_queue: queue.Queue, fs: int):
    buffer = []
    recording = False
    silence_counter = 0
    silence_detected = False

    def callback(indata, frames, time, status):
        nonlocal recording, silence_counter, buffer, silence_detected
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
            if len(buffer) >= fs * 2:
                audio_chunk = np.array(buffer[:fs * 2], dtype=np.float32)
                buffer = buffer[fs * 2:]
                if np.mean(np.abs(audio_chunk)) > silence_threshold/3:
                    transcribed_text = transcribe_audio(audio_chunk, model)
                    normalized_text = transcribed_text.lower().replace(",", "").replace(".", "").replace(" ", "")
                    if "maria" in normalized_text:
                        print("Faça a sua solicitação")
                        notes = [
                            (440, 300),
                            (280, 300),
                        ]

                        for freq, duration in notes:
                            winsound.Beep(freq, duration)
                        recording = True
                        buffer.clear()

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
    model = WhisperModel("small", device="cuda", compute_type="int8_float16")
    audio_queue = queue.Queue()
    generator_thread = Thread(target=generate_and_save_audio, args=(audio_queue, fs))
    generator_thread.start()

    while True:
        audio_data = audio_queue.get()
        if audio_data is not None:
            transcribed_text = transcribe_audio(audio_data, model)
            print(f"Texto transcrito: {transcribed_text}")
