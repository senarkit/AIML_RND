# ╔════════════════════════════════════════════════════════════════════════════╗
# ║                  MULTI SPEAKER - OVERLAPPED CONVERSATION                   ║
# ╚════════════════════════════════════════════════════════════════════════════╝


from gtts import gTTS
from pydub import AudioSegment
import os


def make_tts(text, lang="en"):
    """Generate a TTS mp3 and convert to AudioSegment"""
    # Create a unique filename for each TTS call
    temp_filename = "tmp_" + str(hash(text)) + ".mp3"
    tts = gTTS(text=text, lang=lang)
    tts.save(temp_filename)
    audio_segment = AudioSegment.from_file(temp_filename, format="mp3")
    os.remove(temp_filename)  # Clean up the temporary file
    return audio_segment


def create_conversation(speaker_texts):
    """Concatenate speaker turns sequentially with a pause"""
    if not speaker_texts:
        return AudioSegment.silent(duration=0)

    # Use the first text to start the conversation
    conversation = make_tts(speaker_texts[0])

    # Add subsequent speaker turns with a small pause in between
    for text in speaker_texts[1:]:
        pause = AudioSegment.silent(duration=500)  # 500ms pause
        speaker_turn = make_tts(text)
        conversation += pause + speaker_turn
    return conversation


# Example texts for speakers (each list represents a single channel's conversation)
speakers_ch1 = ["Hello, how are you doing today?", "I am fine, thank you! What about you?"]
speakers_ch2 = [
    "Hey everyone, good morning!",
    "Did you finish the project yesterday?",
    "Yes, I submitted it right before the deadline.",
]

# Generate conversations for each channel
ch1_conversation = create_conversation(speakers_ch1)
ch2_conversation = create_conversation(speakers_ch2)

# Ensure both audio segments have the same frame rate and sample width
FRAME_RATE = 44100
SAMPLE_WIDTH = 2  # 2 bytes for 16-bit audio

ch1_conversation = ch1_conversation.set_frame_rate(FRAME_RATE).set_sample_width(SAMPLE_WIDTH)
ch2_conversation = ch2_conversation.set_frame_rate(FRAME_RATE).set_sample_width(SAMPLE_WIDTH)

# Pad the shorter audio segment with silence
if len(ch1_conversation) > len(ch2_conversation):
    silence_to_add = len(ch1_conversation) - len(ch2_conversation)
    ch2_conversation = ch2_conversation + AudioSegment.silent(duration=silence_to_add)
else:
    silence_to_add = len(ch2_conversation) - len(ch1_conversation)
    ch1_conversation = ch1_conversation + AudioSegment.silent(duration=silence_to_add)


# Manually combine into a stereo file by creating a new segment and overlaying
# Create a new, silent stereo segment of the correct length
stereo_audio = AudioSegment.silent(duration=len(ch1_conversation), frame_rate=FRAME_RATE)

# Set the sample width and channels on the newly created silent segment
stereo_audio = stereo_audio.set_sample_width(SAMPLE_WIDTH).set_channels(2)

# Overlay the first conversation on the left channel (channel 0)
stereo_audio = stereo_audio.overlay(ch1_conversation, position=0, gain_during_overlay=0)

# Overlay the second conversation on the right channel (channel 1)
stereo_audio = stereo_audio.overlay(ch2_conversation, position=0, gain_during_overlay=0)

# Export the final stereo WAV file
output_path = "data/multi_speaker_overlapped.wav"
stereo_audio.export(output_path, format="wav")
print(f"✅ Saved {output_path}")





# ╔════════════════════════════════════════════════════════════════════════════╗
# ║                  MULTI SPEAKER - SEQUENTIAL CONVERSATION                   ║
# ╚════════════════════════════════════════════════════════════════════════════╝

from gtts import gTTS
from pydub import AudioSegment
import os
from itertools import zip_longest  # Import zip_longest


def make_tts(text, lang="en"):
    """Generate a TTS mp3 and convert to AudioSegment"""
    # Create a unique filename for each TTS call
    temp_filename = "tmp_" + str(hash(text)) + ".mp3"
    tts = gTTS(text=text, lang=lang)
    tts.save(temp_filename)
    audio_segment = AudioSegment.from_file(temp_filename, format="mp3")
    os.remove(temp_filename)  # Clean up the temporary file
    return audio_segment


# --- No longer need the old create_conversation function ---

# Example texts for speakers (each list represents a channel's conversation)
speakers_ch1 = ["Hello, how are you doing today?", "I am fine, thank you! What about you?"]
speakers_ch2 = [
    "Hey everyone, good morning!",
    "Did you finish the project yesterday?",
    "Yes, I submitted it right before the deadline.",
]

# Define a pause to insert between speakers
PAUSE_DURATION_MS = 1000  # 1-second pause for a more natural flow
pause = AudioSegment.silent(duration=PAUSE_DURATION_MS)

# Start with an empty stereo audio segment
final_conversation = AudioSegment.empty()

# Interleave the conversations using zip_longest
# This pairs turns from each speaker. If one speaker has more to say, it will continue alone.
for text1, text2 in zip_longest(speakers_ch1, speakers_ch2):

    # Process speaker 1's turn if they have something to say
    if text1:
        turn1_mono = make_tts(text1)
        # Pan the audio to the left channel
        turn1_stereo = turn1_mono.pan(-1.0)
        final_conversation += turn1_stereo + pause

    # Process speaker 2's turn if they have something to say
    if text2:
        turn2_mono = make_tts(text2)
        # Pan the audio to the right channel
        turn2_stereo = turn2_mono.pan(+1.0)
        final_conversation += turn2_stereo + pause

# Export the final stereo WAV file
output_path = "data/multi_speaker_sequential.wav"
final_conversation.export(output_path, format="wav")
print(f"✅ Saved sequential conversation to {output_path}")







