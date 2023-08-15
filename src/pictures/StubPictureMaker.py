from PictureMaker import PictureMaker

class StubPictureMaker(PictureMaker):

    def make_picture(self, * prompt_dict:dict):
        return "file://stub_picture.png"
    
