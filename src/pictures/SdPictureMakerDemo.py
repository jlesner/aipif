# export PYTHONPATH=src ; env time python3 src/pictures/SdPictureMakerDemo.py

import random
from Context import Context
from pictures.FastLocalSdPictureMaker import FastLocalSdPictureMaker
from pictures.positive_prompt_samples import positive_prompt_samples
from pictures.style_prompt_samples import style_prompt_samples

context = Context() # empty since no configuration is needed 

picture_maker = FastLocalSdPictureMaker(context)

# for i in range(10):
#     positive_prompt_text = positive_prompt_samples[random.randint(0, len(positive_prompt_samples)-1)]
#     style_prompt_text = style_prompt_samples[random.randint(0, len(style_prompt_samples)-1)]

positive_prompt_text = "A pizza overflowing with weird and colorful toppings: spiral-shaped fruits, floating cheese balls, and gummy worms that wiggle."
# Penguin and Alien stand with wide eyes and open mouths, shocked at the pizza's appearance."
style_prompt_text = "Expressive, sketchy line drawings often filled with humor and energy in the style of art from Quentin Blake"

# make_picture_output =  picture_maker.make_picture({\
make_picture_output =  picture_maker.make_picture({\
        "positive_prompt_text": positive_prompt_text, \
        "negative_prompt_text": "Disfigured, blurry, nude", \
        "style_prompt_text": style_prompt_text, \
    })

print(f"positive_prompt_text: {positive_prompt_text}")
print(f"style_prompt_text: {style_prompt_text}")
print(f"make_picture_output: {make_picture_output}")
print(f"\n")

