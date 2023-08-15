from sounds.SoundMaker import SoundMaker

class StubSoundMaker(SoundMaker):

    def make_sound(self, description_prompt:dict):
        return "file://stub_sound.wav"
    
