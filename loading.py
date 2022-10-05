import threading
import time

class LoadingSpin(threading.Thread):
    def __init__(self, dt = 1):
        super().__init__()
        self.loading = True
        self.dt = dt
        self.symbols = [".", "..", "..."]
        
    def run(self):
        while self.loading:
            for symbol in self.symbols:
                print(symbol)
                time.sleep(self.dt)
    
    def stop(self):
        self.loading = False

loader = LoadingSpin()
