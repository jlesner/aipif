import os
from common.Context import Context
from media.RqMediaManager import RqMediaManager
from music.MusicMaker import MusicMaker
from media.MediaManager import MediaManager
import subprocess

from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write
from datetime import datetime

class RqMusicGenMusicMaker():

   def __init__(self, rq_mgr:RqMediaManager = RqMediaManager()):
      self._rq_mgr = rq_mgr
      self._fs_mgr = MediaManager()

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

      wavpath = outfile_name + ".wav"
      mp3path = outfile_name + ".mp3"

      cmd = [
         "ffmpeg", "-y",
         "-i", wavpath,
         "-vn",
         "-acodec", "libmp3lame",
         "-q:a", "4",
         "-af", "afade=t=in:ss=0:d=5,afade=t=out:st=10:d=5",
         mp3path
      ]
      subprocess.run(cmd)

      os.remove(wavpath)
      mp3_bytes = self._fs_mgr.binary_file_read(mp3path)
      os.remove(mp3path)

      rq_id= prompt_dict["rq_id"]
      return self._rq_mgr.file_write(rq_id, ".mp3", mp3_bytes, "audio/mpeg")
      # return  mgr.bytes_to_mp3_url(mp3_bytes)

if __name__ == '__main__':

   mm = RqMusicGenMusicMaker()

   make_music_output =  mm.make_music({\
         "positive_prompt_text": "A cheerful, uplifting melody that captures the spirit of new beginnings.", \
         "style_prompt_text": "", \
         "rq_id": "test"
      })
   
   print(make_music_output)