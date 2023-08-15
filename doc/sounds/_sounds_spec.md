# Overview

Examples: Barking dogs / Honking cars / Squawking chickens / Burping / Farting

Sound effects are typically short and played once when triggered.

Options
* https://github.com/steven2358/awesome-generative-ai#audio
* https://github.com/suno-ai/bark looks promising

# Task

Build a prototype that transforms information about a desired sound into a wav / mp3 file of that sound.

Prototype will be a python function:

```make_sound(description_prompt) => url_to_sound_file```

where `description_prompt` is a dictionary that 
* will contain `positive_prompt_text` describing the sound or situation that needs it
* may contain `negative_prompt_text` describing what the sound should not be

This prototype 
* can use the `description_prompt` to select sounds (recommender AI)
* can use the `description_prompt` to create sounds (generative AI)
* can use existing AI sound effect generation tools via APIs or running locally.
