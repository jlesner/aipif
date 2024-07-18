import sys
import torch
import torchaudio
from einops import rearrange
from stable_audio_tools import get_pretrained_model
from stable_audio_tools.inference.generation import generate_diffusion_cond

# Set outfile from first command line argument
if len(sys.argv) > 1:
    outfile = sys.argv[1]
    print(f"Output file: {outfile}")
else:
    print("Error: Output file not specified.")
    sys.exit(1)

# Set prompt from second command line argument
if len(sys.argv) > 2:
    prompt = sys.argv[2]
    print(f"Prompt: {prompt}")
else:
    print("Error: Prompt not specified.")
    sys.exit(1)

device = "cuda" if torch.cuda.is_available() else "cpu"

# Download model
model, model_config = get_pretrained_model("stabilityai/stable-audio-open-1.0")
sample_rate = model_config["sample_rate"]
sample_size = model_config["sample_size"]

model = model.to(device)

# Set up text and timing conditioning
conditioning = [{
    # "prompt": "128 BPM tech house drum loop",
    # "prompt": "The sound of rustling leaves and the playful chattering of monkeys filled the air, creating a lively and energetic atmosphere.",
    # "prompt": "The sound of chirping birds and rustling leaves filled the air, creating a peaceful and harmonious ambiance.",
    # "prompt": "A gentle tinkling sound filled the air, like the delicate chimes of a wind chime on a breezy day.",
    "prompt": prompt,
    "seconds_start": 0, 
    "seconds_total": 30
    # "seconds_total": 7
}]

# Generate stereo audio
output = generate_diffusion_cond(
    model,
    steps=100,
    # steps=50,
    cfg_scale=7,
    conditioning=conditioning,
    sample_size=sample_size,
    sigma_min=0.3,
    sigma_max=500,
    sampler_type="dpmpp-3m-sde",
    device=device
)

# Rearrange audio batch to a single sequence
output = rearrange(output, "b d n -> d (b n)")

# Peak normalize, clip, convert to int16, and save to file
output = output.to(torch.float32).div(torch.max(torch.abs(output))).clamp(-1, 1).mul(32767).to(torch.int16).cpu()
torchaudio.save(outfile, output, sample_rate)
