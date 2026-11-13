
import wave
import numpy as np
import os

# should be happy birthday?
# start_beat, midi_note, duration_beats
score = [
    (0, 60, 0.5), (0.5, 60, 0.5),
    (1, 62, 1), (2, 60, 1), (3, 65, 1), (4, 64, 2),

    (6, 60, 0.5), (6.5, 60, 0.5),
    (7, 62, 1), (8, 60, 1), (9, 67, 1), (10, 65, 2),

    (12, 60, 0.5), (12.5, 60, 0.5),
    (13, 72, 1), (14, 69, 1), (15, 65, 1), (16, 64, 1), (17, 62, 1),

    (18, 70, 0.5), (18.5, 70, 0.5),
    (19, 69, 1), (20, 65, 1), (21, 67, 1), (22, 65, 2),
]

def midi_to_hz(midi_value):
    return 440 * pow(2, (midi_value - 69) / 12)

def beat_to_seconds(beat, bpm):
    # 120 bpm -> 2 bps, 1 beat 0.5s
    return beat / bpm * 60

def write_wav(bytes, path, sample_rate):
    with wave.open(os.path.join(__file__, path) , 'wb') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(bytes)

def render(score, bpm, sample_rate):
    """
        Render the score. So it looks like it's just 2 values. 0.3 and -0.3. But you can make music with that.
        Different notes come from how fast does the speaker oscilate between them.

        Args:
            score: list of midi notes with beats
            bpm: which one to runs the score in, determines how fast the piece goes
            sample_rate: something like a framerate? but for music? how finely to measure the sound
    """
    # 1
    piece_length = max([start + duration for (start, note, duration) in score])
    # 2
    snapshot_count = beat_to_seconds(piece_length, bpm) * sample_rate
    #3
    final_score = np.zeros(int(snapshot_count))

    for (start, note, duration) in score:
        slice_start = int(beat_to_seconds(start, bpm) * sample_rate)
        slice_end = int(slice_start + beat_to_seconds(duration, bpm) * sample_rate)
        n = slice_end - slice_start
        seconds = np.arange(n) / sample_rate #arange works like range()
        fraction = (seconds * midi_to_hz(note)) % 1
        score_slice = np.where(fraction < 0.5, 0.3, -0.3) # works like map()
        final_score[int(slice_start):int(slice_end)] = score_slice

    final_score_bytes = np.astype(final_score * 32767, np.int16).tobytes()
    return write_wav(final_score_bytes, '../arrival.wav', sample_rate)

render(score, 120, 44100)