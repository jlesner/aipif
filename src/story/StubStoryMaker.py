from story.StoryMaker import StoryMaker

class StubStoryMaker(StoryMaker):

    def make_story(self, description_prompt:dict):
        return "file://stub_story.html"
    
