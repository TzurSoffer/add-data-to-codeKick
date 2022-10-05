import threading
import time
import os

class LoadingSpin(threading.Thread):
    def __init__(self):
        super().__init__()
        self.loading = True
        self.symbols = [" / ", " ― ", " \ ", " | "]
        
    def run(self):
        while self.loading:
            for symbol in self.symbols:
                print(symbol)
                time.sleep(1)
                #os.system('cls' if os.name == 'nt' else 'clear')
    
    def stop(self):
        self.loading = False

loader = LoadingSpin()