from threading import Thread
from LIM import LanguageEngine, TTSEngine, InterpretEngine, STTEngine
from secret import *


le = LanguageEngine(LE_API_KEY, MODEL, PROMPT)
ie = InterpretEngine(OW_API_KEY)
tts = TTSEngine(SE_API_KEY, SE_MODEL, VOICE_ID)
stt = STTEngine()


def main():
    lim_thread = Thread(target=lim_module)
    lim_thread.start()


def lim_module():
    while True:
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
        if len(request) > 2: continue

        print("REQUEST:", request[1])
        result = le.request(request[1])

        # LIM Processing
        if result[0] == "command":
            try:    result = eval(result[1])
            except: result = "수행할 수 없는 요청이에요."
        else:
            result = result[1]

        # Result Processing
        print("RESULT:", result)
        tts.speak(result)
        print()


if __name__ == "__main__":
    main()