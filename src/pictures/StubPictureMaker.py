from music.MusicMaker import MusicMaker

class StubPictureMaker(MusicMaker):

    def make_picture(self, description_prompt:dict):
        return "file://stub_picture.png"
    
