from Context import Context

class PictureMaker:
    """
    Base class for objects that implement make_picture()

    Arguments:
        context:Context
            replaces global variables for tracking config / state / stats

    """
    def __init__(self, context:Context):
        self._context = context

    def make_picture(self, description_prompt: dict):
        """
        Generates a picture based on the provided `description_prompt`.
        
        Arguments:
        - `description_prompt` (dict): A dictionary containing:
        * `positive_prompt_text` (str): Describes the picture or situation.
        * `negative_prompt_text` (optional str): Describes what should not be in the picture.
        * `style_prompt_text` (optional str): Describes the desired picture style.
        * `style_prompt_images` (optional list of str): Image URL strings showing the desired picture style. Useful for providing 
            the AI model with examples, especially for children's books where the same characters may appear in different situations.
        * `positive_prompt_images` (optional list of str): Image URL strings as positive examples.
        * `negative_prompt_images` (optional list of str): Image URL strings as negative examples.

        Returns:
            None or web browser playable url str of music matching `description_prompt`
        """
        raise Exception("Function not implemented")
