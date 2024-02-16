import pyttsx3

def reproducir_audio(palabra):
    engine = pyttsx3.init()
    engine.say(palabra)
    engine.runAndWait()


#detector = "HOLA"
#reproducir_audio("La palabra deletreada fue: ", palabra)
