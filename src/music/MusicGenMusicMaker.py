from common.Context import Context
from music.MusicMaker import MusicMaker
from media.MediaManager import MediaManager

from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write
from datetime import datetime

class MusicGenMusicMaker(MusicMaker):
   def __init__(self, context: Context):
      super().__init__(context)
      # Setting up the model can take several seconds, so do it just once.
      # Setting up the model will be silent after required files have been downloaded 
      # (i.e., all runs after the initial run), so print something to indicate that the model is being set up.
      print("Setting up MusicGen model...")
      
      # Using small model, since a GPU with at least 16GB RAM is recommended 
      # for medium-sized models (i.e., 'medium' and 'melody' models)
      self.model = MusicGen.get_pretrained("small")
      self.model.set_generation_params(duration=15)

   
   def make_music(self, prompt_dict: dict):
      print("Making music...")
      descriptions = [prompt_dict["positive_prompt_text"]]
      wav = self.model.generate(descriptions)[0]   # Generate a single output for the prompt
      timestamp = int(datetime.now().timestamp())
      outfile_name = f"output_{timestamp}"

      audio_write(
         outfile_name, 
         wav.cpu(), 
         self.model.sample_rate, 
         strategy="loudness", 
         loudness_compressor=True)

      mgr = MediaManager()
      outfile_bytes = mgr.binary_file_read(outfile_name + ".wav")
      out_url = mgr.bytes_to_wav_url(outfile_bytes)

      return out_url