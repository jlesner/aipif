# IMPORTANT: Check GDOCs version for latest

# Overview

AI models exist that can accept text (and/or sound) inputs (humming) and generate music

* Music from text descriptions:
    * "Majestic horn blasts heralding the arrival of a royal king and queen, with cymbals crashing in celebration."
    * "A rousing bagpipe melody leading a parade of knights and castles in the green Scottish highlands.",

* Music from other sounds
    * "Make piano verson of this tune I will hum for you..."
    * "Please make piano version of this tune..."

NOTE: In games music is typically played continuously try to make music that can loop.

# Task

Build a prototype that transforms information about desired music into a url a web browser can play.

Ideally the prototype will be a python function:

```make_music(prompt_dict) => url_to_music_file```

Where `prompt_dict` is a dictionary that:
* will contain `positive_prompt_text` string describing the sound or situation that needs it
    * See `postive_prompt_samples.py`
* may contain `negative_prompt_text` string describing what the sound should not be

This prototype:
* can use the `prompt_dict` to SELECT EXISTING music (recommender AI)
    * rather than generate music one option is to get existing music from open source asset libraries
    * these open source assets will hopefully come with descriptive labels / file names
    * task becomes use `prompt_dict` to select music from existing collection of music
    * if library is not too big perhaps an LLM can be prompted to do this selection?
    * "For SITUATION below please pick the best music from the MUSIC_LIST below. \nSITUATUON:\n{situation}\nMUSIC_LIST:\n{music_list}\n"
* can use the `prompt_dict` to CREATE NEW music (generative AI)
    * can use existing AI sound effect generation tools via APIs or running locally.
    * see https://github.com/steven2358/awesome-generative-ai#audio
