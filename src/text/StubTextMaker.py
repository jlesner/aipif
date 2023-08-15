from text.TextMaker import TextMaker

class StubTextMaker(TextMaker):

    def make_text(self, prompt_dict:dict):
        return "This is a stub reply from LLM"
    
