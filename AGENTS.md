# Synth agent guide

## Audience and mentoring

- The developer is an SDET learning Python through this project. They have never played an instrument.
- Do not write project source files for them. Write code only when they explicitly ask for a specific piece.
- Give hints, pointers to docs, and reviews of their code. When stuck, show the smallest fragment that unblocks them and explain it.
- Full help is welcome on music theory, math, design, testing strategy, and Python concepts. Explain music terms from zero, with concrete numbers.
- Point out bugs and better idioms, and explain why.

## Goal

A tool that places frequencies on a timeline and plays synth and retro music. Long term: draggable voices, voices driven by math functions `f(beat)`, multiple voices, scales, waveforms, save and load.

The current goal is an MVP: one hardcoded monophonic piece, a simple browser page, and a Play button. No editing in the UI yet.

## Pitch

- Notes are MIDI note numbers: one integer per piano key. +1 is one semitone, +12 is one octave.
- Middle C is 60. A4 is 69 and equals 440 Hz.
- Convert to hertz only at render time: `f(n) = 440 * 2 ** ((n - 69) / 12)`.
- No scale snapping yet. Note names are labels.

## Time

- Score time is in beats.
- Tempo is 120 BPM, so one beat is `60 / bpm` seconds.

## Score format

- A score is a list of `(start_beat, midi_note, duration_beats)` tuples.
- Notes do not overlap. A gap is silence.

## Sound

- Square wave (retro): `+0.3` for the first half of each period, `-0.3` for the second half, `0.0` for silence.
- Period is `1 / frequency` seconds. Sample time is `i / sample_rate`.
- Sample rate 44100, mono, 16-bit WAV. Floats in `-1.0..1.0` scale to integers in `-32767..32767`.

## Stack

- Python 3.11 or newer.
- The app uses the standard library (`math`, `wave`, `io`, `http.server`) plus NumPy for the sample arrays.
- Tests use pytest. Run `python -m pytest` from the project root.

## Layout

```
synth/
  src/
    __init__.py
    music.py      # score, pitch, time, render, write_wav
    server.py     # HTTP only
  test/
    test_*.py
```

- `__init__.py` is empty. It only marks `src` as a package.
- Tests import `from src.music import ...`.
- `music.py` holds pure logic: no HTTP and no HTML.

## Testing conventions

- Tests live under `test/`. Files are `test_*.py`, and tests are plain functions named `test_*`. No `unittest.TestCase`.
- One behavior per test. Use `@pytest.mark.parametrize` for tables of inputs.
- Compare floats with `pytest.approx`.
- Tests import the library and never reimplement its formulas. They do not open sockets or play audio.
- Add `conftest.py` only when two or more test modules share a fixture.

## Browser page

- Served at `http://127.0.0.1:8000/`.
- An SVG timeline is generated in Python from the same score as the audio, so the picture and the sound cannot drift apart.
- Each note is a `<circle>` with `data-beat` and `data-midi` attributes. These are the stable hooks for future browser tests.
- A Play button controls an `<audio>` element that points at `/arrival.wav`. A status element shows `ready` or `playing`.

## Later

Browser tests with Playwright, a coverage run, ruff, and CI. Not part of the MVP.
