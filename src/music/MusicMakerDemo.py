import random
from Context import Context
# from StubMusicMaker import StubMusicMaker
from MusicGenMusicMaker import MusicGenMusicMaker
from music.positive_prompt_samples import positive_prompt_samples
from music.style_prompt_samples import style_prompt_samples

context = Context() # empty since no configuration is needed for StubMusicMaker

# music_maker = StubMusicMaker(context)
music_maker = MusicGenMusicMaker(context)

# for i in range(10):
# for i in range(3):
#     positive_prompt_text = positive_prompt_samples[random.randint(0, len(positive_prompt_samples)-1)]
#     style_prompt_text = style_prompt_samples[random.randint(0, len(style_prompt_samples)-1)]

#     make_music_output =  music_maker.make_music({\
#             "positive_prompt_text": positive_prompt_text, \
#             "style_prompt_text": style_prompt_text, \
#         })

#     print(f"positive_prompt_text: {positive_prompt_text}")
#     print(f"style_prompt_text: {style_prompt_text}")
#     print(f"make_music_output: {make_music_output}")
#     print(f"\n")\

positive_prompt_text = positive_prompt_samples[random.randint(0, len(positive_prompt_samples)-1)]
# positive_prompt_text = "A light-hearted, tropical melody with undertones of mysterious space vibes. Imagine a ukulele playing alongside a theremin, creating an atmosphere of both relaxation and intrigue."
style_prompt_text = style_prompt_samples[random.randint(0, len(style_prompt_samples)-1)]

make_music_output =  music_maker.make_music({\
        "positive_prompt_text": positive_prompt_text, \
        "style_prompt_text": style_prompt_text, \
    })

print(f"positive_prompt_text: {positive_prompt_text}")
print(f"style_prompt_text: {style_prompt_text}")
print(f"make_music_output: {make_music_output}")
print(f"\n")
