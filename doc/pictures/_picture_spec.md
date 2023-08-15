
# Overview 

AI models exist that accept text and/or image inputs and generate remarkable output images.
* Pictures from text descriptions ( “Bunny washing hands” ) 
* Pictures from other pictures ( “Make cartoon version of this photo here” )

# Task

Build a prototype that transforms information about a desired picture into a jpg or png file of that picture. 

The prototype will be a python function:

```make_picture(description_prompt) => url_to_picture_file```

The `description_prompt` is a dictionary that 
* will contain `positive_prompt_text` string describing the picture or the situation
    * see `postive_prompt_samples.py` 
* may contain `negative_prompt_text` string describing what should not be in the picture
* may contain `style_prompt_text` string describing the desired picture style
    * see `style_prompt_samples.py`
* may contain `style_prompt_images` list of image url strings showing desired picture style
    * the idea here is to supply AI model with examples of what we want (for example previous generated images)
    * this is important because children's books often show the SAME characters doing different things
* may contain `positive_prompt_images` list of image url strings as positive examples
* may contain `negative_prompt_images` list of image url strings as negative examples


This prototype 
* must use the `description_prompt` to create new picture (generative AI)
* can leverage existing AI picture generation tools via APIs or running locally.
* can generate simple pictures such as stick people or pencil cartoons
* can generate anime or photos if those are easier to generate

