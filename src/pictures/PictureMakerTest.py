import random
from Context import Context
from pictures.StubPictureMaker import StubPictureMaker
from postive_prompt_samples import postive_prompt_samples
from style_prompt_samples import style_prompt_samples

context = Context() # empty since no configuration is needed for StubPictureMaker

picture_maker = StubPictureMaker(context)

for i in range(10):
    positive_prompt_text =  postive_prompt_samples[random.randint(0, len(postive_prompt_samples)-1)]
    style_prompt_text = style_prompt_samples[random.randint(0, len(style_prompt_samples)-1)]

    make_picture_output =  picture_maker.make_picture(
        {positive_prompt_text: positive_prompt_text, \
         style_prompt_text: style_prompt_text}\
    )

    print(f"positive_prompt_text: {positive_prompt_text}")
    print(f"style_prompt_text: {style_prompt_text}")
    print(f"make_picture_output: {make_picture_output}")
    print(f"\n")
