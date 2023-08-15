
# Overview

AI models exist that can accept text and/or sound inputs (humming) and generate music
* Music from text descriptions ( “Bunny washing hands” ) 
* Music from other sounds ( "Make piano play this tune I will hum for you..." )

Unlike sound effects, music is typically looped and played continuously when triggered.

See https://github.com/steven2358/awesome-generative-ai#audio

# Task

Build a prototype that transforms information about desired music (description or melody) into a wav / mp3 file of that or similar “feeling” music. 

Ideally the prototype will be a python function:

```make_music(description_prompt) => url_to_music_file```

Where `description_prompt` is a dictionary that 
* will contain `positive_prompt_text` describing the sound or situation that needs it
* may contain `negative_prompt_text` describing what the sound should not be

This prototype
* can use the `description_prompt` to select music (recommender AI)
* can use the `description_prompt` to create music (generative AI)
* can use existing AI music generation tools via APIs or running locally.
