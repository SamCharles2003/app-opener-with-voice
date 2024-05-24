import time
from vosk import Model, KaldiRecognizer
import pyttsx3
import pyaudio
from AppOpener import give_appnames,open,close


model = Model(r"C:\Users\sam charles\PycharmProjects\vosk-model-en-in-0.5")
recognizer = KaldiRecognizer(model, 16000)


assistance_name="SAM"
action_list=["OPEN","CLOSE"]

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

mic=pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000 , input=True , frames_per_buffer=8192)
stream.start_stream()

def listener():
    while True:
        data = stream.read(8192)
        if recognizer.AcceptWaveform(data):
            text = recognizer.Result()
            #print(text[14:-3])
            #main(text[14:-3])
            return text[14:-3]


def main():
    while True:
        #close("firefox", match_closest=True, output=False)
        #open("whatsapp",output=True)
        apps = give_appnames(upper=True)
        print(apps)
        raw_incoming_string = listener()
        voice_text = raw_incoming_string.upper()
        print("Incoming String(1): ", voice_text)
        if voice_text == assistance_name:
            print("Listening......")
            engine.say("Listening")
            time.sleep(1)
            engine.runAndWait()
            raw_incoming_string = listener()
            voice_text = raw_incoming_string.upper()
            print(voice_text)
            if "CLOSE " in voice_text:
                app_name = voice_text.replace("CLOSE ", "")
                close(app_name, match_closest=True,output=False)
                engine.say("Closing"+ str(app_name))
                engine.runAndWait()
            elif "OPEN " in voice_text:
                app_name = voice_text.replace("OPEN ", "")
                print("App name",app_name)
                open(app_name, match_closest=True)
                engine.say("opening"+str(app_name))
                engine.runAndWait()




if __name__=="__main__":
    main()

