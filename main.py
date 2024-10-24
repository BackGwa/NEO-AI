from threading import Thread
from LIM import LanguageEngine
from LIM import TTSEngine
from LIM import STTEngine
from LIM import InterpretEngine
from LIM import DetectionEngine
from LIM import IOEngine
from LIM import MessageEngine
from secret import *

ioe = IOEngine()
de = DetectionEngine("res/SDXM.pt")
le = LanguageEngine(LE_API_KEY, MODEL, PROMPT)
me = MessageEngine(CONTACT)
ie = InterpretEngine(ioe, me, REQUEST_PIN, OW_API_KEY)
tts = TTSEngine(SE_API_KEY, SE_MODEL, VOICE_ID)
stt = STTEngine()

background_listen = True

def main():
    ioe.register_input(REQUEST_PIN, hold_lim)
    ioe.register_input(SOS_PIN, sos)

    lim_thread = Thread(target=background_lim)
    lim_thread.start()


def background_lim():
    while True:
        if background_listen:
            # Listen Speak
            text = stt.listen(timeout=5)
            calling = ""

            # STT Result Check
            if text == "": continue

            print("SPEAK:", text)

            for sign in CALL_SIGN:
                if not sign in text: calling = ""
                else:
                    calling = sign
                    break

            if calling == "": continue

            # LIM Request
            request = text.split(calling, maxsplit=1)
            if len(request) < 2: continue

            lim_request(request[1])


def hold_lim():
    global background_listen
    background_listen = False
    request = stt.listen(timeout=5)
    lim_request(request)
    background_listen = True


def sos():
    pass


def lim_request(request: str):
        print("REQUEST:", request)
        result = le.request(request)

        if result[0] == "command":
            try:    result = eval(result[1])
            except: result = "죄송해요. 요청을 수행하려 했지만, 문제가 발생했어요."
        else:
            result = result[1]

        print("RESULT:", result)
        tts.speak(result)
        print()


if __name__ == "__main__":
    main()