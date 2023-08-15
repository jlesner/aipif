
# Overview 

AI models exist that accept text and/or image inputs and generate remarkable output images.
* Pictures from text descriptions ( “Bunny washing hands” ) 
* Pictures from other pictures ( “Make cartoon version of this photo here” )

# Task

Build a prototype that transforms information about a desired picture into a jpg or png file of that picture. 

The prototype will be a python function:

```make_picture(description_prompt) => url_to_picture_file```

The `description_prompt` is a dictionary that 
* will contain `positive_prompt_text` describing the picture or the situation
* may contain `negative_prompt_text` describing  what the picture should not be
* may contain `positive_prompt_images` list of image url as positive examples
* may contain `negative_prompt_images` list of image url as negative examples

This prototype 
* must use the `description_prompt` to create new pictures (generative AI)
* can leverage existing AI picture generation tools via APIs or running locally.
* can generate simple pictures such as stick people or pencil cartoons
* can generate anime or photos if those are easier to generate