from music.MusicMaker import MusicMaker

class StubMusicMaker(MusicMaker):

    def make_music(self, prompt_dict:dict):
        return "file://stub_music.mp3"
    
