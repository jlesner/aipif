from common.ContextAware import ContextAware

class MusicMaker(ContextAware):

    def make_music(self, prompt_dict: dict):
        """
        Generates music based on the provided description prompt.
        
        Arguments:
        - prompt_dict (dict): A dictionary containing:
        * `positive_prompt_text` (str): Describes the picture or situation.
        * `negative_prompt_text` (optional str): Describes what should not be in the picture.
        * `style_prompt_text` (optional str): Describes the desired picture style.
        * `style_prompt_images` (optional list of str): Image URL strings showing the desired picture style. Useful for providing 
            the AI model with examples, especially for children's books where the same characters may appear in different situations.
        * `positive_prompt_images` (optional list of str): Image URL strings as positive examples.
        * `negative_prompt_images` (optional list of str): Image URL strings as negative examples.

        Returns:
            None or web browser playable url of music matching `prompt_dict`
        """
        raise Exception("Function not implemented")
