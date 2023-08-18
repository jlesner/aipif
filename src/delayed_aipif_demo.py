import logging
import random
from Context import Context
from pictures.DelayedPictureMaker import DelayedPictureMaker
from sounds.DelayedSoundMaker import DelayedSoundMaker
from music.DelayedMusicMaker import DelayedMusicMaker
from text.DelayedTextMaker import DelayedTextMaker


def context_configure(context:Context):
    # if your module needs to be configured, you can do it here
    # eventually we will have a config file and/or command line args
    #
    # WARNING: DO NOT CHECKIN YOUR API KEYS / SECRETS
    #
    context.config['story_maker_port'] = 8080
    

def state_setup(context:Context):
    # setup context.state using context.config 
    
    # for now we hardcode function bindings
    context.state['make_picture'] = DelayedPictureMaker(context).make_picture
    context.state['make_sound'] = DelayedSoundMaker(context).make_sound
    context.state['make_music'] = DelayedMusicMaker(context).make_music
    context.state['make_story'] = DelayedTextMaker(context).make_text

def activity_simulate(context:Context):
    for i in range(50):
        activity = random.choice(['make_picture', 'make_sound', 'make_music', 'make_story'])        
        context.state[activity]({"positive_prompt_text": f"iteration {i}"})
        print(f"{activity} iteration {i}")


if __name__ == '__main__':
    logging.basicConfig(filename=__file__[:-3] +'.log', filemode='w', level=logging.DEBUG)
    context = Context()
    context_configure(context)
    state_setup(context)
    activity_simulate(context)