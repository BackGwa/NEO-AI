from threading import Thread

class IOEngine:
    def __init__(self):
        pass

    def register_input(self, pin: int, func):
        T = Thread(target=self.__reading_input__, args=(pin, func,), daemon=True)
        T.start()
    
    def __reading_input__(self, pin: int, func):
        while True:
            if pin: # TODO : pin input logic
                try: func()
                except: pass