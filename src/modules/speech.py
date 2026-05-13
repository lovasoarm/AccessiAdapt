try:
    import pyttsx3
    ENGINE_AVAILABLE = True
except ImportError:
    ENGINE_AVAILABLE = False
    pyttsx3 = None

_engine = None

def get_engine():
    global _engine
    if not ENGINE_AVAILABLE:
        return None
    if _engine is None:
        _engine = pyttsx3.init()
        _engine.setProperty('rate', 150)
    return _engine

def speak(text):
    try:
        engine = get_engine()
        if engine:
            engine.say(text)
            engine.runAndWait()
    except:
        pass