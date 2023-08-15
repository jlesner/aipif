from sounds.SoundMaker import SoundMaker

class StubSoundMaker(SoundMaker):

    def make_sound(self, prompt_dict:dict):
        return "file://stub_sound.mp3"
    
