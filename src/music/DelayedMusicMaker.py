import time
import random
from music.MusicMaker import MusicMaker

class DelayedMusicMaker(MusicMaker):

    def make_music(self, prompt_dict:dict):
        delay = random.randint(0, 10)
        time.sleep(delay)
        return f"result of DelayedMusicMaker after {delay} seconds for positive_prompt_text={prompt_dict['positive_prompt_text']}"
    
