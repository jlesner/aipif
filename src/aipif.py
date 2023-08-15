import logging
from Context import Context
from pictures.StubPictureMaker import StubPictureMaker
from sounds.StubSoundMaker import StubSoundMaker
from music.StubMusicMaker import StubMusicMaker
from story.StubStoryMaker import StubStoryMaker


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
    context.state['make_picture'] = StubPictureMaker(context).make_picture
    context.state['make_sound'] = StubSoundMaker(context).make_sound
    context.state['make_music'] = StubMusicMaker(context).make_music
    context.state['make_story'] = StubStoryMaker(context).make_story


if __name__ == '__main__':
    logging.basicConfig(filename=__file__[:-3] +'.log', filemode='w', level=logging.DEBUG)
    context = Context()
    context_configure(context)
    state_setup(context)