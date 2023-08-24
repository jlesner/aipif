from media.FileMediaManager import FileMediaManager
from media.RqMediaManager import RqMediaManager
from pictures.PictureMaker import PictureMaker

class RqStubPictureMaker():

    def __init__(self, rq_mgr:RqMediaManager = RqMediaManager()):
        self._rq_mgr = rq_mgr
        self.png_bytes = FileMediaManager().file_read("../static/dog.png")
        
    def make_picture(self, prompt_dict:dict):        
        
        if "rq_id" in prompt_dict:
            rq_id= prompt_dict["rq_id"]
            return self._rq_mgr.file_write(rq_id, ".png", self.png_bytes, "image/png")
        
        return "file://stub_picture.png"