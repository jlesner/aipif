import time
import random
from text.TextMaker import TextMaker

class DelayedTextMaker(TextMaker):

    def make_text(self, prompt_dict:dict):
        delay = random.randint(0, 60)
        time.sleep(delay)
        return f"result of DelayedTextMaker after {delay} seconds for positive_prompt={prompt_dict['positive_prompt']}"
    
