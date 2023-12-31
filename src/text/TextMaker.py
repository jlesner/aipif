
from common.ContextAware import ContextAware

class TextMaker(ContextAware):

    def make_text(self, prompt_dict: dict) -> str:
        """
        Generates text  based on the provided `prompt_dict`.
        
        Arguments:
        - `prompt_dict` (dict): A dictionary containing:
        * `positive_prompt_text` (str): Describes the story or situation.
        * `negative_prompt_text` (optional str): Describes what should not be in the story.
        * `style_prompt_text` (optional str): Describes the desired story style.
        * `style_prompt_images` (optional list of str): Image URL strings showing the desired story style. 
        * `positive_prompt_images` (optional list of str): Image URL strings as positive examples.
        * `negative_prompt_images` (optional list of str): Image URL strings as negative examples.

        Returns:
            None or web browser playable url of story matching `prompt_dict`
        """
        raise Exception("Function not implemented")
