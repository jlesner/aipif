# IMPORTANT: Check GDOCs version for latest

# Overview

Examples: Barking dogs / Honking cars / Squawking chickens / Burping / Farting

Sound effects are typically short and played once when triggered.

# Task

Build a prototype that transforms information about a desired sound into a wav / mp3 file of that sound.

Prototype will be a python function:

```make_text(prompt_dict) => llm_generated_text```

where `prompt_dict` is a dictionary that 
* will contain `positive_prompt_text` string describing the sound or situation that needs it
    * see `positive_prompt_samples.py`
* may contain `negative_prompt_text` string describing what the sound should not be
* may contain `style_prompt_text` string describing the desired sound style

This prototype:

* can use the `prompt_dict` to SELECT SOUNDS (recommender AI)
    * rather than generate sounds one option is to get sounds from open source sound effects library
    * these open source sounds will hopefully come with descriptive labels like their file names
    * task then becomes use `prompt_dict` to select best sound we already have
    * if sound library is not too big perhaps an LLM can be prompted to do this selection?
    * "For SITUATION below please pick the best sound effect from the SOUND_LIST below. \nSITUATUON:\n{situation}\nSOUND_LIST:\n{sound_list}\n"
    
* can use the `prompt_dict` to CREATE SOUNDS (generative AI)
    * can use existing AI sound effect generation tools via APIs or running locally.
    * https://github.com/suno-ai/bark looks promising
    * other options https://github.com/steven2358/awesome-generative-ai#audio
