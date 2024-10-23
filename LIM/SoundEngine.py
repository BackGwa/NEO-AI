import requests, os
from playsound import playsound
import speech_recognition as stt

class TTSEngine:
    def __init__(self, api_key: str, model_id: str, voice_id: str):
        self.model_id = model_id
        self.endpoint = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        self.headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": api_key
        }
    
    def speak(self, prompt: str):
        data = {
            "text": prompt,
            "model_id": self.model_id,
            "voice_settings": {
                "stability": 0.75,
                "similarity_boost": 0.5
            }
        }
        response = requests.post(self.endpoint, json=data, headers=self.headers)
        if response.status_code == 200:
            with open("voice.mp3", "wb") as f:
                f.write(response.content)
            playsound("voice.mp3")
            os.remove("voice.mp3")

class STTEngine:
    def __init__(self, device_index: int = 0):
        self.Recognizer = stt.Recognizer()
        self.mic = stt.Microphone(device_index=device_index)
    
    def listen(self, timeout: int = 2) -> str:
        try:
            with self.mic as source:
                self.Recognizer.adjust_for_ambient_noise(source)
                audio = self.Recognizer.listen(source, timeout=timeout)
                result = self.Recognizer.recognize_google(audio, language='ko-KR')
                return result
        except:
            return ""