import io
import time
import random
# import tomesd
import torch
from diffusers import DiffusionPipeline
# , utils
from PIL import Image
from media.MediaManager import MediaManager
from pictures.PictureMaker import PictureMaker
from media.RqMediaManager import RqMediaManager

class FastLocalSdPictureMaker():

    def __init__(self, rq_mgr:RqMediaManager = RqMediaManager()):
        self._rq_mgr = rq_mgr

    def make_picture(self, prompt_dict: dict):
        save_img = False
        prompt, neg_prompt = self.create_prompt(prompt_dict)

        pipeline = DiffusionPipeline.from_pretrained("Lykon/DreamShaper", torch_dtype=torch.float16)
        pipeline = pipeline.to("cuda")
        image = pipeline(prompt=prompt,negative_prompt=neg_prompt).images[0]

        with io.BytesIO() as output:
            image.save(output, format="PNG")
            image_bytes = output.getvalue()

        if save_img:
            file_name = time.strftime("%Y%m%d_%H%M%S") + ''.join([str(random.randint(1, 9)) for _ in range(5)]) + ".png"
            image.save(file_name)

        if "rq_id" in prompt_dict:
            rq_id= prompt_dict["rq_id"]
            # return self._rq_mgr.file_write(rq_id, ".png", image_bytes, "image/png")
            img = Image.open(io.BytesIO(image_bytes))
            jpeg_buffer = io.BytesIO()
            img.save(jpeg_buffer, format="JPEG")
            jpeg_image_bytes = jpeg_buffer.getvalue()
            return self._rq_mgr.file_write(rq_id, ".jpg", jpeg_image_bytes, "image/jpeg")

        url = MediaManager().bytes_to_png_url(image_bytes)
        return url

    def create_prompt(self,prompt_dict: dict):
        prompt_types = ["positive","negative","style"]
        prompt_data = dict()
        for prompt_type in prompt_types:
            text_key = f"{prompt_type}_prompt_text"
            if text_key in prompt_dict:
                prompt_data[text_key] = prompt_dict[text_key]

        pos_text = prompt_data.get("positive_prompt_text")
        neg_text = prompt_data.get("negative_prompt_text")
        style_text = prompt_data.get("style_prompt_text")

        if pos_text == None:
            raise Exception("PictureMaker: No Positive Prompt")

        prompt = pos_text if style_text == None else pos_text + " in the style of " + style_text
        neg_prompt = neg_text

        return (prompt,neg_prompt)


