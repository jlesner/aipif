import os
import time
import openai
import sys

from text.TextMaker import TextMaker

openai.api_key = os.getenv("OPENAI_API_KEY")

class Gpt4oMiniTextMaker(TextMaker):
    def make_text(self, prompt_dict: dict, retry_count: int = 0):
        try:
            completion = openai.ChatCompletion.create(
                model='gpt-4o-mini',
                messages=[
                    {'role': 'user', 'content': prompt_dict['positive_prompt_text']}
                ],
                temperature=0.6
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

if __name__ == "__main__":
    input_text = sys.stdin.read()  # Read input from STDIN until EOF.
    prompt_dict = {
        'positive_prompt_text': input_text
    }
    text_maker = Gpt4oMiniTextMaker()
    result = text_maker.make_text(prompt_dict)
    print(result)  # Write the result to STDOUT.
