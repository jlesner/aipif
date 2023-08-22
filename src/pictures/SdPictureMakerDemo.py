import random
from Context import Context
from pictures.SdPictureMaker import SdPictureMaker
from pictures.positive_prompt_samples import positive_prompt_samples
from pictures.style_prompt_samples import style_prompt_samples

context = Context() # empty since no configuration is needed for StubPictureMaker

picture_maker = SdPictureMaker(context)

# for i in range(10):
#     positive_prompt_text = positive_prompt_samples[random.randint(0, len(positive_prompt_samples)-1)]
#     style_prompt_text = style_prompt_samples[random.randint(0, len(style_prompt_samples)-1)]

positive_prompt_text = "A pizza overflowing with weird and colorful toppings: spiral-shaped fruits, floating cheese balls, and gummy worms that wiggle. Penguin and Alien stand with wide eyes and open mouths, shocked at the pizza's appearance."
# style_prompt_text = ""

make_picture_output =  picture_maker.make_picture({\
        "positive_prompt_text": positive_prompt_text, \
        # "style_prompt_text": style_prompt_text, \
    })

print(f"positive_prompt_text: {positive_prompt_text}")
# print(f"style_prompt_text: {style_prompt_text}")
print(f"make_picture_output: {make_picture_output}")
print(f"\n")
