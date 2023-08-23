from text.DelayedTextMaker import DelayedTextMaker
from text.StubTextMaker import StubTextMaker
from text.TextMaker import TextMaker
import hashlib
import os
import json

class CachingTextMaker(TextMaker):

    def __init__(self, text_maker: TextMaker, cache_dir: str = '_cache'):
        self.text_maker = text_maker
        self.cache_dir = cache_dir
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def _get_hash(self, prompt_dict: dict) -> str:
        data_str = json.dumps(prompt_dict, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()

    def _cache_filepath(self, hash_value: str) -> str:
        return os.path.join(self.cache_dir, hash_value)

    def make_text(self, prompt_dict: dict) -> str:
        hash_value = self._get_hash(prompt_dict)
        filepath = self._cache_filepath(hash_value)
        in_fp = filepath + "_in.json"
        out_fp = filepath + "_out.xml"
        
        if os.path.exists(out_fp):
            with open(out_fp, 'r') as file:
                return file.read()
            
        result = self.text_maker.make_text(prompt_dict)

        with open(out_fp, 'w') as file:
            file.write(result)

        with open(in_fp, 'w') as file:
            file.write(json.dumps(prompt_dict)) 

        return result

if __name__ == '__main__':

    text_maker = CachingTextMaker(DelayedTextMaker())

    result = text_maker.make_text({\
            "positive_prompt_text": "Please give a more vivid description of picture this passage paints: ", \
        })

    print(result)

    result = text_maker.make_text({\
            "positive_prompt_text": "Please give a more vivid description of picture this passage paints: ", \
        })

    print(result)