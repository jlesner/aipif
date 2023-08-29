import re
import subprocess
import sys

class FsStoryMaker():

    def __init__(self, url_prefix:str = "http://aipif-2023.s3.amazonaws.com/story/"):
        self._url_prefix = url_prefix

    def sanitize(self, input_string):
        blacklist = [
            "&", ";", "|", ">", "<", "$", "`", "\\", 
            "'", '"', "(", ")", "{", "}", "[", "]", 
            "!", "*", "?", "~", "^", "#", "%"
        ]

        for char in blacklist:
            input_string = input_string.replace(char, "_")
        
        input_string = input_string.replace("$((", "_").replace("$(", "_").replace("))", "_").replace(")", "_")
        
        return input_string

    def make_story(self, prompt_dict: dict) -> str:
        rq_id = prompt_dict['rq_id']
        positive_prompt_text = prompt_dict['positive_prompt_text']
        command = f'bash -c "(cd ~/aipif/src/story && . story2.bash && py_fs_story_make {self.sanitize(rq_id)} {self.sanitize(positive_prompt_text)}  )"'
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, text=True)
        
        while True:
            output = process.stdout.readline().decode('utf-8')
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())

        # if process.returncode == 0:
        #     return f"{self._url_prefix}{rq_id}_twine.html"
        # else:
        #     return None


        url = f"{self._url_prefix}{rq_id}_twine.html"

        print(f"FsStoryMaker.make_story() returning: {url}", file=sys.stderr)

        return url


if __name__ == "__main__":        
    maker = FsStoryMaker() 
    
    # user_input = "rm -rf / 😉 && echo 'hacked'! 😊"
    # print(maker.sanitize(user_input))

    print(maker.make_story({\
            "positive_prompt_text": "🌌🍅🦙🍝🚍🎻", \
            "rq_id": "test", \
            # "style_prompt_text": style_prompt_text, \
        }))