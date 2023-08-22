from Context import Context
from media.MediaManager import MediaManager
from diffusers import DiffusionPipeline, utils
import torch
import io
import tomesd
import time
import random

class SdPictureMaker:
    """
    Base class for objects that implement make_picture()

    Arguments:
        context:Context
            replaces global variables for tracking config / state / stats

    """
    def __init__(self, context:Context):
        self._context = context
        
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
    
    def make_picture(self, prompt_dict: dict):
        """
        Generates a picture based on the provided `prompt_dict`.
        
        Arguments:
        - `prompt_dict` (dict): A dictionary containing:
        * `positive_prompt_text` (str): Describes the picture or situation.
        * `negative_prompt_text` (optional str): Describes what should not be in the picture.
        * `style_prompt_text` (optional str): Describes the desired picture style.

        Returns:
            None or web browser playable url str of music matching `prompt_dict`
        """

        save_img = True
        
        prompt, neg_prompt = self.create_prompt(prompt_dict)
            
        base = DiffusionPipeline.from_pretrained(
            "stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16, variant="fp16", use_safetensors=True
        )
        base.enable_model_cpu_offload()
        tomesd.apply_patch(base, ratio=0.5)
        refiner = DiffusionPipeline.from_pretrained(
            "stabilityai/stable-diffusion-xl-refiner-1.0",
            text_encoder_2=base.text_encoder_2,
            vae=base.vae,
            torch_dtype=torch.float16,
            use_safetensors=True,
            variant="fp16",
        )
        refiner.enable_model_cpu_offload()
        n_steps = 25 #default 25
        high_noise_frac = 0.8

        image = base(
            prompt=prompt,
            negative_prompt=neg_prompt,
            num_inference_steps=n_steps,
            denoising_end=high_noise_frac,
            output_type="latent",
            height = 768, #default 768
            width = 768,
        ).images
        image = refiner(
            prompt=prompt,
            num_inference_steps=n_steps,
            denoising_start=high_noise_frac,
            image=image,
        ).images[0]
        with io.BytesIO() as output:
            image.save(output, format="PNG")
            image_bytes = output.getvalue()
        if save_img:
            file_name = time.strftime("%Y%m%d_%H%M%S") + ''.join([str(random.randint(1, 9)) for _ in range(5)]) + ".png"
            image.save(file_name)
        url = MediaManager.bytes_to_png_url(image_bytes)
        return url
        
    def make_picture_fast(self, prompt_dict: dict):
        """
        Generates a picture based on the provided `prompt_dict`.
        
        Arguments:
        - `prompt_dict` (dict): A dictionary containing:
        * `positive_prompt_text` (str): Describes the picture or situation.
        * `negative_prompt_text` (optional str): Describes what should not be in the picture.
        * `style_prompt_text` (optional str): Describes the desired picture style.

        Returns:
            None or web browser playable url str of music matching `prompt_dict`
        """

        save_img = True
        
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
        
        url = MediaManager.bytes_to_png_url(image_bytes)
        return url
            

