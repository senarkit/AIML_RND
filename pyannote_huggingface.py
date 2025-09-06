# instantiate the pipeline
from pyannote.audio import Pipeline
from huggingface_hub import HfFolder

audio = "data/candice.wav"

token = HfFolder.get_token()
pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1", use_auth_token=token
)

# run the pipeline on an audio file
diarization = pipeline(f"{audio}")

# dump the diarization output to disk using RTTM format
with open(f"{audio.split('.')[0]}_hf.rttm", "w") as rttm:
    diarization.write_rttm(rttm)