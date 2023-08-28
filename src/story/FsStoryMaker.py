import re
import subprocess

class FsStoryMaker():

    def __init__(self, url_prefix:str = "http://aipif-2023.s3.amazonaws.com/story/"):
        self._url_prefix = url_prefix


    def sanitize(self, input_string):
        # Common dangerous characters in bash
        blacklist = [
            "&", ";", "|", ">", "<", "$", "`", "\\", 
            "'", '"', "(", ")", "{", "}", "[", "]", 
            "!", "*", "?", "~", "^", "#", "%"
        ]
        # Replace blacklisted characters with an underscore
        for char in blacklist:
            input_string = input_string.replace(char, "_")
        
        # Further replace common command substitution syntax
        input_string = input_string.replace("$((", "_").replace("$(", "_").replace("))", "_").replace(")", "_")
        
        return input_string

    def make_story(self, prompt_dict: dict):
        rq_id = prompt_dict['rq_id']
        positive_prompt_text = prompt_dict['positive_prompt_text']
        command = f'bash -c "(cd ~/aipif/src/story && . story2.bash && fs_story_make {self.sanitize(rq_id)} {self.sanitize(positive_prompt_text)} )"'
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        
        while True:
            output = process.stdout.readline().decode('utf-8')
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())

        if process.returncode == 0:
            return f"{self._url_prefix}{rq_id}_twine.html"
        else:
            return None

if __name__ == "__main__":        
    maker = FsStoryMaker() 
    
    # user_input = "rm -rf / 😉 && echo 'hacked'! 😊"
    # print(maker.sanitize(user_input))

    print(maker.make_story({\
            "positive_prompt_text": "🌌🍅🦙🍝🚍🎻", \
            "rq_id": "test", \
            # "style_prompt_text": style_prompt_text, \
        }))