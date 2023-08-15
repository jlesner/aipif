from music.MusicMaker import MusicMaker

class StubMusicMaker(MusicMaker):

    def make_music(self, description_prompt:dict):
        return "file://stub_music.mp3"
    
