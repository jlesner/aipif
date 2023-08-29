
import os
import time
import openai

from text.TextMaker import TextMaker

openai.api_key = os.getenv("OPENAI_API_KEY")

class Gpt35TextMaker(TextMaker):

 def make_text(self, prompt_dict:dict, retry_count:int=0):
    try:
        completion = openai.ChatCompletion.create( 
            model = 'gpt-3.5-turbo',
            messages = [ 
                {'role': 'user', 'content': prompt_dict['positive_prompt_text']}
            ],
            temperature = 0.6
        )
        return completion['choices'][0]['message']['content']

    except openai.error.OpenAIError as error:
        if "throttle" in str(error).lower():
            print("Throttle error detected! Waiting for 60 seconds before retrying.")
            time.sleep(60)  # Delay for 60 seconds.
            if retry_count < 3:
                return self.make_text(prompt_dict, retry_count+1)  # Recursive call to try again.
            else:
                raise Exception("Too many throttle retries! Aborting.")
        else:
            raise error  # If it's not a throttle error, raise the exception.



# def generate_prompt(animal):
#     return """Suggest three names for an animal that is a superhero.

# Animal: Cat
# Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
# Animal: Dog
# Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
# Animal: {}
# Names:""".format(
#         animal.capitalize()
#     )
    
