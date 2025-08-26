import pyttsx3 

def initialize_engine():
    
    engine = pyttsx3.init("sapi5")  

    voices = engine.getProperty('voices')
    engine.setProperty('voice',voices[1].id) # female voice

    rate = engine.getProperty('rate')
    engine.setProperty('rate',rate-50)

    volume = engine.getProperty('volume')
    engine.setProperty('volume',volume+0.25)

    return engine 

def speak(text):
    engine = initialize_engine()
    engine.say(text)
    engine.runAndWait()