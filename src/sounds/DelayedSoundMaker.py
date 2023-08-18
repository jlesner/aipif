import time
import random
from sounds.SoundMaker import SoundMaker

class DelayedSoundMaker(SoundMaker):

    def make_sound(self, prompt_dict:dict):
        delay = random.randint(0, 60)
        time.sleep(delay)
        return f"result of DelayedSoundMaker after {delay} seconds for positive_prompt_text={prompt_dict['positive_prompt_text']}"

    
