
import json
from common.ContextAware import ContextAware

class WebApi(ContextAware):

    def story_suggest(self, story_prompt:str):
        pass

    def story_delete(self, rq_id:str):
        pass

    def request_retry(self, rq_id:str):
        pass

    def story_list(self) -> json:
        pass

    def queue_list(self) -> json:
        pass
