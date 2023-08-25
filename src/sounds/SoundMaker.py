from common.ContextAware import ContextAware
from sounds.selection import select_title, generate_keywords
from sounds.collection import collect_sounds, preview_sound

class SoundMaker(ContextAware):

    def make_sound(self, prompt_dict: dict):
        """
        Generates sound based on the provided `prompt_dict`.
        
        Arguments:
        - `prompt_dict`(dict): A dictionary containing:
        * `positive_prompt_text` (str): Describes the sound or situation.
        * `negative_prompt_text` (optional str): Describes what should not be in the sound.        
        * `style_prompt_text` (optional str): Describes the desired sound style.
        * `style_prompt_sounds` (optional list of str): Sound URL strings showing the desired sound style. Useful for providing 
            the AI model with examples, especially for children's books where the same voices etc may appear in different situations.
        * `positive_prompt_sounds` (optional list of str): Image URL strings as positive examples.
        * `negative_prompt_sounds` (optional list of str): Image URL strings as negative examples.

        Returns:
            None or web browser playable url str of sound matching `prompt_dict`
        """
                
        #prompt, negative_prompt = self.make_prompt(prompt_dict)
        prompt= prompt_dict['positive_prompt_text']
        
        # openai generates keywords from the prompt
        keywords= generate_keywords(prompt)
        
        #print("keywords:",keywords)
        
        # keywords are used to query and collect sounds from freesound and results are written to sounds.txt
        collect_sounds(keywords)
        
        # langchain uses openai to read sounds.txt and selects most relevant sound id based on prompt
        title_id= select_title(prompt)
        title_id= title_id.strip() #remove leading and trailing whitespace from id
        #print(f"id: {title_id}")
        
        # download sound file from selected sound id to SoundFiles directory as 'title_id.mp3'
        preview_sound(title_id)
        path= f'SoundFiles/{title_id}.mp3'
        
        # use media manager to create sound url and return it
        return generate_audio_html(path)
    
    def make_prompt(self, prompt_dict):
        negative_prompt= ''
        prompt= prompt_dict['positive_prompt_text']
        if 'style_prompt_text' in prompt_dict:
            prompt= prompt + " The sound profile is: " + prompt_dict['style_prompt_text']
        if 'negative_prompt_text' in prompt_dict:
            negative_prompt= prompt_dict['negative_prompt_sounds']
        return prompt, negative_prompt
    
def generate_audio_html(file_path):
    from media.MediaManager import MediaManager
    from media.FileMediaManager import FileMediaManager

    sound = FileMediaManager().file_read(file_path)

    sound_url = MediaManager().bytes_to_mp4_url(sound)

    return sound_url

