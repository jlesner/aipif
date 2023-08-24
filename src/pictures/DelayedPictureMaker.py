import time
import random
from pictures.PictureMaker import PictureMaker

class DelayedPictureMaker(PictureMaker):

    def make_picture(self, prompt_dict:dict):
        delay = random.randint(0, 10)
        time.sleep(delay)
        return f"result of DelayedPictureMaker after {delay} seconds for positive_prompt_text={prompt_dict['positive_prompt_text']}"

