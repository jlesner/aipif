from common.ContextAware import ContextAware

class StoryMaker(ContextAware):


    def make_story(self, prompt_dict: dict):
        """
        Generates a story based on the provided `prompt_dict`.

        Arguments:
        - `prompt_dict` (dict): A dictionary containing:
        * `positive_prompt_text` (str): Describes the picture or situation.        
        * `positive_prompt_images` (optional list of str): Image URL strings as positive examples.

        Returns:
            None or web browser playable url str of story matching `prompt_dict`
        """
        raise Exception("Function not implemented")
