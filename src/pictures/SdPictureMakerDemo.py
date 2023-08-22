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

positive_prompt_text = "A pizza overflowing with weird and colorful toppings: spiral-shaped fruits, floating cheese balls, and gummy worms that wiggle."
# Penguin and Alien stand with wide eyes and open mouths, shocked at the pizza's appearance."
# style_prompt_text = ""

# make_picture_output =  picture_maker.make_picture({\
make_picture_output =  picture_maker.make_picture_fast({\
        "positive_prompt_text": positive_prompt_text, \
        # "style_prompt_text": style_prompt_text, \
    })

print(f"positive_prompt_text: {positive_prompt_text}")
# print(f"style_prompt_text: {style_prompt_text}")
print(f"make_picture_output: {make_picture_output}")
print(f"\n")


# picture_maker.make_picture(

# $ export PYTHONPATH=src ; env time python3 src/pictures/SdPictureMakerDemo.py
# Fetching 9 files: 100%|███████████████████████████████████████████████████████████████| 9/9 [05:00<00:00, 33.39s/it]
# Loading pipeline components...: 100%|█████████████████████████████████████████████████| 5/5 [00:01<00:00,  3.81it/s]
#   0%|                                                                                        | 0/20 [00:00<?, ?it/s]

# 100%|███████████████████████████████████████████████████████████████████████████████| 20/20 [12:01<00:00, 36.06s/it]
#   0%|                                                                                                      | 0/5 [00:00<?, ?it/s]

# 100%|█████████████████████████████████████████████████████████████████████████████████████████████| 5/5 [20:16<00:00, 243.23s/it]

# Command terminated by signal 9
# 2743.90user 538.50system 1:21:44elapsed 66%CPU (0avgtext+0avgdata 10764064maxresident)k
# 24238488inputs+23040560outputs (98151major+3082238minor)pagefaults 0swaps
# $ 


# picture_maker.make_picture_fast()

# 237.50user 90.19system 10:39.74elapsed 51%CPU (0avgtext+0avgdata 6398080maxresident)k
# 2925136inputs+10709968outputs (10741major+744855minor)pagefaults 0swaps
# $
