import sys
import json
import os
import boto3
import hashlib

class S3WebApi():

    def __init__(self, queue_path:str="_queue", bucket_name:str='aipif-2023'):
        self._s3_client = boto3.client('s3')
        self._queue_path = queue_path
        self._bucket_name = bucket_name

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

        s3_key = f"{self._queue_path}/make_story-{rq_id}-req.xml"

        self._s3_client.put_object(
            Bucket=self._bucket_name,
            Key=s3_key,
            Body=request_xml,
            ContentType='application/xml'
        )

        print(f"Queued {s3_key} in S3 bucket {self._bucket_name} with content {request_xml}", file=sys.stderr)

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
    api = S3WebApi()
    api.story_suggest("Hello")
    print(api.json_story_list())
    # print(api.json_queue_list())
    # print(api.xml_queue_list())


