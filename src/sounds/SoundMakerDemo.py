import random
# from common.Context import Context
from sounds.SoundMaker import SoundMaker
from sounds.positive_prompt_samples import positive_prompt_samples
from sounds.style_prompt_samples import style_prompt_samples

# context = Context() # empty since no configuration is needed for StubSoundMaker

sound_maker = SoundMaker()

positive_prompt_text = positive_prompt_samples[random.randint(0, len(positive_prompt_samples)-1)]
style_prompt_text = style_prompt_samples[random.randint(0, len(style_prompt_samples)-1)]

print(f"positive_prompt_text: {positive_prompt_text}")

make_sound_output =  sound_maker.make_sound({\
        "positive_prompt_text": positive_prompt_text, \
        "style_prompt_text": "", \
    })

#print(f"style_prompt_text: {style_prompt_text}")
# print(f"make_sound_output: {make_sound_output}")
print(f"\n")
