import pytest
from src.music import midi_to_hz, beat_to_seconds

@pytest.mark.parametrize(
    ("midi_note", "hz"),
    [
        (69, 440),
        (57, 220),
        (60, 261.63),
    ],
)
def test_midi_to_hz(midi_note, hz):
    assert midi_to_hz(midi_note) == pytest.approx(hz, abs=0.01)


@pytest.mark.parametrize(
    ('beat', 'bpm', 'seconds'),
    [
        (0, 120, 0),
        (1, 120, 0.5),
        (4, 120, 2),
        (1, 60, 1),
    ],
)
def test_beat_to_seconds(beat, bpm, seconds):
    assert beat_to_seconds(beat, bpm) == seconds