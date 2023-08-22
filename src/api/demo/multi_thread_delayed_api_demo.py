import time
import random
import threading
from common.Context import Context
from common.BoundedBuffer import BoundedBuffer
from pictures.DelayedPictureMaker import DelayedPictureMaker
from sounds.DelayedSoundMaker import DelayedSoundMaker
from music.DelayedMusicMaker import DelayedMusicMaker
from text.DelayedTextMaker import DelayedTextMaker

class Model_Task:
    def __init__(self, process_function=None, prompt_dict={}): # not sure if should be None or empty dict
        self.process_function = process_function
        self.input_dict = prompt_dict
        self.output = None

def context_configure(context:Context):
    # if your module needs to be configured, you can do it here
    # eventually we will have a config file and/or command line args
    #
    # WARNING: DO NOT CHECKIN YOUR API KEYS / SECRETS
    #
    context.config['story_maker_port'] = 8080
    context.config['sentinel'] = "STOP"
    context.config['num_workers'] = 5
    

def state_setup(context:Context):
    # setup context.state using context.config 
    
    # for now we hardcode function bindings
    context.state['todo_tasks'] = BoundedBuffer(10)
    context.state['done_tasks'] = BoundedBuffer(10)

    context.state['make_picture'] = DelayedPictureMaker(context).make_picture
    context.state['make_sound'] = DelayedSoundMaker(context).make_sound
    context.state['make_music'] = DelayedMusicMaker(context).make_music
    context.state['make_story'] = DelayedTextMaker(context).make_text

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

def task_manager(context:Context):
    for i in range(5):
        activity = random.choice(['make_picture', 'make_sound', 'make_music', 'make_story'])
        # context.state[activity]({"positive_prompt_text": f"iteration {i}"})
        task = Model_Task(process_function=context.state[activity], prompt_dict={"positive_prompt_text": f"iteration {i}"})
        context.state['todo_tasks'].add(task)
        print(f"Manager producing {task.process_function.__name__} for {task.input_dict}")
        time.sleep(random.random())
    print("Manager done!")
    context.state['todo_tasks'].add(context.config['sentinel'])

if __name__ == '__main__':
    context = Context()
    context_configure(context)
    state_setup(context)
    print("starting tasks!")
    manager_thread = threading.Thread(target=task_manager, args=(context,))
    manager_thread.start()

    worker_threads = []
    for i in range(context.config['num_workers']):
        worker_thread = threading.Thread(target=worker, args=(context,i))
        worker_thread.start()
        worker_threads.append(worker_thread)
    
    for worker_thread in worker_threads:
        worker_thread.join()

    manager_thread.join()

    print("all done!")
    print(context.state['done_tasks'])  