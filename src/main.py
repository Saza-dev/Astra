from core.Astra import Astra
from voice.voice_engine import speak
from voice.voice_recognizer import command


if __name__ == "__main__":
    while True:
        # query = command().lower()
        query = input ("Enter your command-> ")
        if query == "none":
            continue
        response = Astra(query)
        print("\r",end="",flush=True)
        print(f"Assistant: {response}\n")
        speak(response)
        
