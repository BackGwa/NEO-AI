from threading import Thread
import gpiozero

class IOEngine:
    def __init__(self):
        pass

    def register_input(self, pin: int, func):
        T = Thread(target=self.__reading_input__, args=(pin, func,), daemon=True)
        T.start()
    
    def __reading_input__(self, pin: int, func):
        i_in = gpiozero.Button(pin)
        while True:
            if i_in.is_pressed:
                try: func()
                except: pass