import threading

class BoundedBuffer:

    def __init__(self, size):
        self.buffer = [None] * size
        self.size = size
        self.count = 0  
        self.in_pos = 0  
        self.out_pos = 0
        
        # Synchronization primitives
        self.mutex = threading.Lock()
        self.not_full = threading.Condition(self.mutex)
        self.not_empty = threading.Condition(self.mutex)

    def add(self, item):
        with self.not_full:
            while self.count == self.size:
                self.not_full.wait()

            self.buffer[self.in_pos] = item
            self.in_pos = (self.in_pos + 1) % self.size
            self.count += 1

            self.not_empty.notify()

    def remove(self):
        with self.not_empty:
            while self.count == 0:
                self.not_empty.wait()

            item = self.buffer[self.out_pos]
            self.out_pos = (self.out_pos + 1) % self.size
            self.count -= 1

            self.not_full.notify()
            return item
    
    def __str__(self):
        rStr = "[ "
        for i in range(self.out_pos, self.in_pos):
            rStr += str(self.buffer[i]) + " "
        rStr += "]"
        return rStr