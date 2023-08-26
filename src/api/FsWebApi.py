
import hashlib
import json
import os
import sys
# from common.ContextAware import ContextAware

class FsWebApi():

    def __init__(self, queue_path:str="story/_queue"):
        self._queue_path = queue_path
        path = self._queue_path
        if not os.path.exists(path) or not os.path.isdir(path):
            raise ValueError(f"'{path}' is not a valid directory path")

    def story_suggest(self, story_prompt:str):
        request_hash = hashlib.sha256(story_prompt.encode()).hexdigest()
        rq_id = request_hash[:8]

        request_xml = f'''
<queue>
    <request type="make_story">
        <positive_prompt_text>{story_prompt}</positive_prompt_text>
        <rq id="{rq_id}"/>
    </request>
</queue>
        '''

        fpath = f"{self._queue_path}/make_story-{rq_id}-req.xml"
        with open(fpath, 'w') as file:
            file.write(request_xml)

        print(f"Queued {fpath} with {request_xml}", file=sys.stderr)

    def story_delete(self, rq_id:str):
        pass

    def request_retry(self, rq_id:str):
        pass

    def json_story_list(self) -> json:
        return json.dumps(
            [
                ("🌟🍀🦄🍍🚀🎸", "097a99d0"),
                ("🎈🌵🦉🍉🚁🎻", "0caf2351"),
                ("🌕🍒🦎🍓🚂🎷", "0f3f26b6"),
                ("🎉🌻🦖🍏🚜🎺", "1306e381"),
                ("🌈🍋🦚🍇🚓🎶", "172f3386"),
                ("🎊🌼🦜🍔🚕🎵", "1843526c"),
                ("🌙🍎🦢🍩🚢🎤", "185f8db3"),
                ("🎋🍉🦋🍖🚤🎼", "1ad999b6"),
                ("🌠🍓🦗🍜🚘🎧", "1ef4bdbb"),
                ("🎍🍑🦘🍛🚖🎸", "22eb2a07"),
                ("🌌🍅🦙🍝🚍🎻", "27131044"),
                ("🎎🍈🦡🍞🚔🎷", "27378438"),
                ("🌑🍇🦒🍟🚐🎺", "2b5ea0b4"),
                ("🎏🍊🦓🍠🚑🎶", "34862083"),
                ("🌔🍎🦂🍡🚎🎵", "3afc8665"),
                ("🎐🍋🦔🍢🚛🎤", "40265b0e"),
                ("🌖🍌🦕🍣🚚🎼", "47b9da95"),
                ("🎒🍍🦏🍤🚜🎧", "4991422f"),
                ("🌓🍏🦜🍥🚝🎸", "4c5347f0"),
                ("🎑🍐🦑🍦🚞🎻", "4f99c6a8")
            ]
        )

    def json_queue_list(self) -> json:
        path = self._queue_path
        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        file_data = {file: os.path.getsize(os.path.join(path, file)) for file in files}        
        return json.dumps(file_data)

    def dict_to_xml(self, data):
        xml = ['<root>']
        for key, value in data.items():
            xml.append(f'<file name="{key}">{value}</file>')
        xml.append('</root>')
        return ''.join(xml)

    def xml_queue_list(self) -> str:
        path = self._queue_path
        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        file_data = {file: os.path.getsize(os.path.join(path, file)) for file in files}
        return self.dict_to_xml(file_data)


if __name__ == "__main__":
    api = FsWebApi()
    api.story_suggest("Hello")
    print(api.json_story_list())
    # print(api.json_queue_list())
    # print(api.xml_queue_list())