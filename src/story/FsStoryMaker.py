import subprocess

class FsStoryMaker():

    def __init__(self, url_prefix:str = "http://aipif-2023.s3.amazonaws.com/story/"):
        self._url_prefix = url_prefix

    def make_story(self, prompt_dict: dict):
        rq_id = prompt_dict['rq_id']
        command = f'bash -c "(. story.bash && fs_story_make "{rq_id}" )'
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
