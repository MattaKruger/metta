# Audio Feature Extraction

This directory contains scripts for extracting audio features from music files using [librosa](https://librosa.org/). The extracted features are stored in a SQLite database for analysis and Music Information Retrieval (MIR) applications.

## 📋 Table of Contents

- [Overview](#overview)
- [Scripts](#scripts)
- [Extracted Features](#extracted-features)
- [Installation](#installation)
- [Usage](#usage)
- [Database Schema](#database-schema)
- [Feature Interpretation](#feature-interpretation)
- [Examples](#examples)
- [Mood Detection](#mood-detection)

## 🎵 Overview

The feature extraction system analyzes audio files and extracts 23 different features including:

- **Spectral features** (brightness, timbre)
- **Temporal features** (energy, dynamics)
- **Harmonic features** (chroma, pitch content)
- **Rhythmic features** (tempo, beats per minute)
- **MFCC coefficients** (13 coefficients for machine learning)

All features are stored in a SQLite database (`audio_features.db`) for easy querying and analysis.

## 📁 Scripts

### `extract_features.py`
Core module containing feature extraction functions using librosa.

**Functions:**
- `extract_audio_features(filepath)` - Extract features from a single audio file
- `extract_features_from_directory(directory)` - Batch process all audio files in a directory

### `extract_from_data.py`
Command-line script to extract features from the `/data` directory and save to database.

**Usage:**
```bash
# Extract from default ./data directory
python extract_from_data.py

# Extract from custom directory
python extract_from_data.py --directory /path/to/music

# Force re-extraction (ignore existing records)
python extract_from_data.py --force
```

### `view_features.py`
Query and display extracted features from the database.

**Usage:**
```bash
# Show summary of all features
python view_features.py --summary

# Show detailed view (default)
python view_features.py

# Limit results
python view_features.py --limit 5

# Filter by filename
python view_features.py --filename "NBSS"

# Output as JSON
python view_features.py --json
```

## 🎛️ Extracted Features

### 1. Basic Audio Information
| Feature | Description | Typical Values |
|---------|-------------|----------------|
| `duration_seconds` | Total length of audio | 30-600 seconds |
| `sample_rate_hz` | Samples per second | 22050 or 44100 Hz |

### 2. Spectral Features
| Feature | Description | Typical Values |
|---------|-------------|----------------|
| `spectral_centroid_hz` | "Center of mass" of frequencies | 800-4000 Hz |
| `spectral_rolloff_hz` | Frequency with 85% of energy | 2000-8000 Hz |

**Interpretation:**
- **Low centroid** (<1500 Hz): Dark, bass-heavy sounds (kick drums, cello)
- **Mid centroid** (1500-3000 Hz): Balanced sounds (vocals, guitars)
- **High centroid** (>3000 Hz): Bright, treble-rich sounds (cymbals, hi-hats)

### 3. Temporal Features
| Feature | Description | Typical Values |
|---------|-------------|----------------|
| `zero_crossing_rate` | Signal zero-crossings per second | 0.02-0.15 |
| `rms_energy` | Root mean square energy (loudness) | 0.01-0.5 |

**Interpretation:**
- **Low ZCR** (0.02-0.05): Smooth, sustained sounds
- **High ZCR** (>0.1): Noisy, percussive sounds

### 4. Tempo
| Feature | Description | Typical Values |
|---------|-------------|----------------|
| `tempo_bpm` | Estimated beats per minute | 60-180 BPM |

**Interpretation:**
- **Slow** (60-90 BPM): Ballads, ambient
- **Medium** (90-140 BPM): Pop, rock, dance
- **Fast** (140+ BPM): Techno, drum & bass

### 5. Chroma Features
| Feature | Description | Typical Values |
|---------|-------------|----------------|
| `chroma_energy` | Harmonic pitch content | 0.2-0.8 |

**Interpretation:**
- **Low** (<0.4): Percussive, atonal content
- **High** (>0.6): Rich harmonic content (chords, melodies)

### 6. MFCC Coefficients
| Feature | Description | Usage |
|---------|-------------|-------|
| `mfcc_0` to `mfcc_12` | Mel-frequency cepstral coefficients | Genre classification, similarity |

**Interpretation:**
- `mfcc_0`: Overall loudness/energy
- `mfcc_1-3`: Broad spectral shape (bass to treble)
- `mfcc_4-12`: Fine-grained texture and timbre

## 🚀 Installation

```bash
# Install dependencies
pip install librosa numpy sqlmodel

# Or using the project's pyproject.toml
pip install -e .
```

**Supported Audio Formats:**
- `.wav` (WAV/RIFF)
- `.mp3` (MPEG-1 Audio Layer III)
- `.flac` (Free Lossless Audio Codec)
- `.m4a` (MPEG-4 Audio)
- `.ogg` (Ogg Vorbis)

## 💻 Usage

### Basic Workflow

1. **Extract features from your music collection:**
```bash
python extract_from_data.py --directory ./data
```

2. **View extracted features:**
```bash
python view_features.py --summary
```

3. **Query specific files:**
```bash
python view_features.py --filename "techno"
```

### Python API Usage

```python
from extract_features import extract_audio_features

# Extract features from a single file
features = extract_audio_features("song.flac")

print(f"Tempo: {features.tempo_bpm:.1f} BPM")
print(f"Energy: {features.rms_energy:.4f}")
print(f"Brightness: {features.spectral_centroid_hz:.1f} Hz")
```

### Batch Processing

```python
from extract_features import extract_features_from_directory

# Process entire directory
features_list = extract_features_from_directory("./music_library")

# Analyze results
for f in features_list:
    print(f"{f.filename}: {f.tempo_bpm:.1f} BPM")
```

## 🗄️ Database Schema

Features are stored in the `audio_features` table with the following schema:

```sql
CREATE TABLE audiofeatures (
    id INTEGER PRIMARY KEY,
    filename TEXT NOT NULL,
    created_at TIMESTAMP,
    duration_seconds REAL,
    sample_rate_hz INTEGER,
    spectral_centroid_hz REAL,
    spectral_rolloff_hz REAL,
    zero_crossing_rate REAL,
    rms_energy REAL,
    tempo_bpm REAL,
    chroma_energy REAL,
    mfcc_0 REAL,
    mfcc_1 REAL,
    ... (through mfcc_12)
);
```

## 📊 Feature Interpretation

### Mood Detection Indicators

| Feature | Low Value Mood | High Value Mood | Sample Values |
|---------|----------------|-----------------|---------------|
| `tempo_bpm` | Calm, Reflective | Energetic, Intense | 60 BPM (slow) → 140 BPM (fast) |
| `spectral_centroid_hz` | Dark, Bass-heavy | Bright, Treble-focused | 800 Hz (dark) → 4000 Hz (bright) |
| `zero_crossing_rate` | Smooth, Sustained | Noisy, Percussive | 0.03 (tonal) → 0.15 (percussive) |
| `chroma_energy` | Atonal, Unstable | Harmonic, Structured | 0.2 (noise) → 0.8 (chords) |
| `rms_energy` | Quiet, Intimate | Loud, Powerful | 0.05 (quiet) → 0.35 (loud) |

### Music Classification Heuristics

**High Energy Tracks:**
```
tempo_bpm > 120 AND rms_energy > 0.3
→ Energetic, dance, upbeat
```

**Dark/Atmospheric:**
```
spectral_centroid_hz < 1500 AND tempo_bpm < 100
→ Ambient, dark, atmospheric
```

**Percussive/Rhythmic:**
```
zero_crossing_rate > 0.1 AND chroma_energy < 0.4
→ Drum-focused, percussive
```

**Harmonic/Melodic:**
```
chroma_energy > 0.6 AND zero_crossing_rate < 0.06
→ Melodic, harmonic-rich
```

## 📖 Examples

### Example 1: Find High-Energy Tracks

```python
from sqlmodel import Session, select, create_engine
from models.features import AudioFeatures

engine = create_engine("sqlite:///./audio_features.db")

with Session(engine) as session:
    statement = select(AudioFeatures).where(
        AudioFeatures.tempo_bpm > 130,
        AudioFeatures.rms_energy > 0.3
    )
    high_energy = session.exec(statement).all()
    
    for track in high_energy:
        print(f"{track.filename}: {track.tempo_bpm:.1f} BPM")
```

### Example 2: Calculate Brightness

```python
features = extract_audio_features("track.flac")

# Brightness normalized around 2000 Hz (human hearing threshold)
brightness = features.spectral_centroid_hz / 2000

if brightness > 1.5:
    print("Bright/aggressive sound")
elif brightness < 0.8:
    print("Dark/mellow sound")
else:
    print("Balanced sound")
```

### Example 3: Genre Classification Features

```python
# Extract feature vector for ML classification
feature_vector = [
    features.tempo_bpm,
    features.spectral_centroid_hz,
    features.rms_energy,
    features.zero_crossing_rate,
    features.chroma_energy,
    features.mfcc_0,
    features.mfcc_1,
    # ... through mfcc_12
]

# Use with scikit-learn, etc.
```

## 🎭 Mood Detection

Based on extracted features, you can classify music mood:

```python
def detect_mood(features: AudioFeatures) -> str:
    """Simple mood classification based on audio features."""
    
    # High energy + fast tempo
    if features.rms_energy > 0.3 and features.tempo_bpm > 120:
        if features.spectral_centroid_hz > 2500:
            return "Energetic/Aggressive"
        else:
            return "Driving/Intense"
    
    # Low energy + slow tempo
    elif features.rms_energy < 0.2 and features.tempo_bpm < 90:
        if features.spectral_centroid_hz < 1500:
            return "Dark/Melancholic"
        else:
            return "Calm/Peaceful"
    
    # Percussive content
    elif features.zero_crossing_rate > 0.1 and features.chroma_energy < 0.4:
        return "Percussive/Rhythmic"
    
    # Harmonic content
    elif features.chroma_energy > 0.6:
        return "Melodic/Harmonic"
    
    return "Neutral/Balanced"
```

## 🔍 Tips & Best Practices

1. **Duplicate Prevention:** By default, `extract_from_data.py` skips files already in the database. Use `--force` to re-extract.

2. **Batch Processing:** For large collections, process in smaller batches to monitor progress.

3. **Feature Normalization:** When comparing features across tracks, consider normalizing values (especially MFCCs).

4. **Sample Rate:** Librosa defaults to 22050 Hz. Adjust in `extract_features.py` if higher fidelity is needed.

5. **Error Handling:** Corrupted files are skipped automatically with a warning message.

## 📚 Further Reading

- [Librosa Documentation](https://librosa.org/doc/latest/index.html)
- [Music Information Retrieval](https://musicinformationretrieval.com/)
- [MFCC Explanation](https://en.wikipedia.org/wiki/Mel-frequency_cepstrum)
- [Audio Feature Analysis Tutorial](https://librosa.org/doc/latest/tutorial.html)

## 🤝 Contributing

When adding new features:

1. Update `extract_features.py` extraction function
2. Add columns to `AudioFeatures` model in `models/features.py`
3. Document the feature in this README
4. Update mood detection heuristics if applicable

---

**Created:** 2025  
**Dependencies:** librosa, numpy, sqlmodel  
**License:** See LICENSE file