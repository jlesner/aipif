import random
from Context import Context
from text.positive_prompt_samples import positive_prompt_samples
from text.Gpt35TextMaker import Gpt35TextMaker

context = Context() # empty since no configuration is needed for StubTextMaker

text_maker = Gpt35TextMaker(context)

for i in range(1):
    positive_prompt_text = positive_prompt_samples[random.randint(0, len(positive_prompt_samples)-1)]
    # style_prompt_text = style_prompt_samples[random.randint(0, len(style_prompt_samples)-1)]

    make_text_output =  text_maker.make_text({\
            "positive_prompt_text": "Please give a more vivid description the picture this passage paints: " + positive_prompt_text, \
            # "style_prompt_text": style_prompt_text, \
        })

    print(f"positive_prompt_text: {positive_prompt_text}")
    # print(f"style_prompt_text: {style_prompt_text}")
    print(f"make_text_output: {make_text_output}")
    print(f"\n")
