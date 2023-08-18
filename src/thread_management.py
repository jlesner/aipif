import threading

class Model_Task:
    def __init__(self, process_function=None, prompt_dict={}): # not sure if should be None or empty dict
        self.process_function = process_function
        self.input_dict = prompt_dict
        self.output = None

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

def worker(context,id):
    while True:
        item = context.state['todo_tasks'].remove()
        if item == context.config['sentinel']:
            context.state['todo_tasks'].add(item)
            print(f"Worker {id} received termination signal")
            break
        process_result = item.process_function(item.input_dict)
        item.output = process_result
        print(f"Worker {id} processing {item.process_function.__name__} request to {process_result}")
        context.state['done_tasks'].add(item)