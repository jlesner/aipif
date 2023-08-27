
import os

os.environ['SUNO_USE_SMALL_MODELS'] = 'True'

from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
# from IPython.display import Audio


class BarkSoundMaker():

    def make_sound(self, prompt_dict: dict):
        # temp_directory= os.getenv('TEMP_DIRECTORY')
        # text_prompt= prompt_dict['positive_prompt_text']
        
      
        # download and load all models
        preload_models()

        # generate audio from text
        # text_prompt = """
        #     Hello, my name is Suno. And, uh — and I like pizza. [laughs] 
        #     But I also have other interests such as playing tic tac toe.
        # """
        # audio_array = generate_audio(text_prompt)

        # I have a silky smooth voice, and today I will tell you about 
        # the exercise regimen of the common sloth.
        text_prompt = """

        After Max and his mom returned to their cozy hole in the cheese factory, 
        they realized that their home was the safest and happiest place for them. 
        They spent their days enjoying each other's company and the delicious cheese.
        """
        audio_array = generate_audio(text_prompt, history_prompt="v2/en_speaker_1")


        # save audio to disk
        write_wav("bark_generation.wav", SAMPLE_RATE, audio_array)
        
        # play text in notebook
        # Audio(audio_array, rate=SAMPLE_RATE)


        return None
    

if __name__ == "__main__":
    BarkSoundMaker().make_sound(None)