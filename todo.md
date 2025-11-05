# MIR/Audio features
  - use MFCC features for genre/emotion classification
  - music similarity
  - pitch/timbre analysis

## Mood detection indicators
| Feature                | Low Value Mood          | High Value Mood         | Sample Values           |
|------------------------|-------------------------|-------------------------|-------------------------|
| `tempo_bpm`            | Calm, Reflective        | Energetic, Intense      | 60 BPM (slow) → 140 BPM (fast) |
| `spectral_centroid_hz` | Dark, Bass-heavy        | Bright, Treble-focused  | 800 Hz (dark) → 4000 Hz (bright) |
| `zero_crossing_rate`   | Smooth, Sustained       | Noisy, Percussive       | 0.03 (tonal) → 0.15 (percussive) |
| `chroma_energy`        | Atonal, Unstable        | Harmonic, Structured    | 0.2 (noise) → 0.8 (chords) |
| `rms_energy`           | Quiet, Intimate         | Loud, Powerful          | 0.05 (quiet) → 0.35 (loud) |
| `mfcc_delta_var`       | Stable, Predictable     | Dynamic, Unpredictable  | 10 (calm) → 100+ (aggressive) |

  ### Tempo
    - Fast tempo > 120 bpm -> Energetic/upbeat moods
    - Slow tempo < 80 bpm -> Calm/melancholic moods
  ### Spectral features(Brightness/Darkness)
    - spectral_centroid_hz
      - brightness = spectral_centroid_hz / 2000 (2000=human hearing)


## What is timbre?
  - Tone quality and tone color
