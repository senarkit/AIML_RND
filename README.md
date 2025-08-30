## Pyannot Offline - using Safetensor

#### To Setup :
1. Create virtual env : `py -3.11 -m venv venv` <br>
2. Install the requirements : `pip install -r requirements.txt` <br>
    Check the packages are installed : <br>
    a) `pip install huggingface_hub` <br>
    b) `pip install pyannote.audio torch safetensors`
3. generate token key from hf account : https://huggingface.co/settings/tokens <br>
4. `hf auth login`. It will ask for HF token <br>
5. Accept agreements : <br>
    https://huggingface.co/pyannote/speaker-diarization-3.1 <br>
    https://huggingface.co/pyannote/segmentation-3.0 <br>
    https://huggingface.co/pyannote/embedding <br>

6. Download all repos involved <br>
    hf download pyannote/speaker-diarization-3.1 --local-dir ./diarization <br>
    hf download pyannote/segmentation-3.0 --local-dir ./segmentation <br>
    hf download pyannote/embedding --local-dir ./embedding <br>


7. Create Synthetic Audio : <br>
   `python generate_audio.py` - This will generate the synthetic audio files for both overlapping and sequential conversations.It uses Google's Text-to-Speech API for audio generation. <br>


8. Run using existing HF Pyannote [Comparison] : <br>
   `python pyannote_huggingface.py` - This script performs speaker diarization using pre-trained models from Hugging Face. It processes audio files, segments them, and identifies speakers, saving the results in RTTM format. This does not use the downloaded models. <br>

9. Run safetensor conversion : <br>
   `python pyannote_safetensor.py` - This script converts the PyTorch model weights to Safetensor format for both segmentation and embedding models. <br>

10. Run local pipeline : <br>
   `python pyannote_local_pipeline.py` - This script performs speaker diarization using the locally downloaded models. It processes audio files, segments them, and identifies speakers, saving the results in RTTM format. This has used the model weights from safetensor and rebuild the segmentation and embedding models. <br>