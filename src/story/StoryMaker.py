from Context import Context

class StoryMaker:
    """
    Base class for objects that implement make_story()

    Arguments:
        context:Context
            replaces global variables for tracking config / state / stats

    """
    def __init__(self, context:Context):
        self._context = context

    def make_story(self, description_prompt: dict):
        """
        Generates story based on the provided `description_prompt`.
        
        Arguments:
        - `description_prompt` (dict): A dictionary containing:
        * `positive_prompt_text` (str): Describes the story or situation.
        * `negative_prompt_text` (optional str): Describes what should not be in the story.
        * `style_prompt_text` (optional str): Describes the desired story style.
        * `style_prompt_images` (optional list of str): Image URL strings showing the desired story style. 
        * `positive_prompt_images` (optional list of str): Image URL strings as positive examples.
        * `negative_prompt_images` (optional list of str): Image URL strings as negative examples.

        Returns:
            None or web browser playable url of story matching `description_prompt`
        """
        raise Exception("Function not implemented")
