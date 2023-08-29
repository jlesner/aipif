
import os
import subprocess
import tempfile

from media.MediaManager import MediaManager
from media.RqMediaManager import RqMediaManager

os.environ['SUNO_USE_SMALL_MODELS'] = 'True'

from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav

class BarkSoundMaker():

    def __init__(self, rq_mgr:RqMediaManager = RqMediaManager()):
        self._rq_mgr = rq_mgr
        self._fs_mgr = MediaManager()
        preload_models()

    def make_sound(self, prompt_dict: dict):

        text_prompt = prompt_dict['positive_prompt_text']
        audio_array = generate_audio(text_prompt, history_prompt="v2/en_speaker_6")

        temp_name = tempfile.mktemp()

        wavpath = temp_name + ".wav"
        mp3path = temp_name + ".mp3"
        write_wav(wavpath, SAMPLE_RATE, audio_array)

        cmd = [
            "ffmpeg", "-y",
            "-i", wavpath,
            "-acodec", "libmp3lame",
            "-q:a", "4",
            mp3path
        ]
        subprocess.run(cmd)
        os.remove(wavpath)

        mp3_bytes = self._fs_mgr.binary_file_read(mp3path)        
        os.remove(mp3path)

        rq_id= prompt_dict["rq_id"]
        return self._rq_mgr.file_write(rq_id, ".mp3", mp3_bytes, "audio/mpeg")

if __name__ == "__main__":
    BarkSoundMaker().make_sound(None)