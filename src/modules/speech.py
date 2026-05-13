import pyttsx3

engine = None

def get_engine():
    global engine
    if engine is None:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
    return engine

def speak(text):
    try:
        get_engine().say(text)
        get_engine().runAndWait()
    except:
        pass