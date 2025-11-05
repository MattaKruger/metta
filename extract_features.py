"""
Audio Feature Extraction Module

This module provides functions to extract meaningful audio features from audio files
using librosa. These features are commonly used in music information retrieval (MIR),
audio classification, and machine learning tasks.

Extracted Features:
===================

1. BASIC AUDIO INFORMATION
   - duration_seconds: Total length of the audio file in seconds
   - sample_rate_hz: Number of audio samples per second (Hz). Common values are 22050 Hz or 44100 Hz.
                    Higher sample rates capture more high-frequency detail but require more storage.

2. SPECTRAL FEATURES
   These features analyze the frequency content of the audio signal.

   - spectral_centroid_hz: The "center of mass" of the frequency spectrum.
                           Indicates where most of the sound energy is concentrated.
                           - Low values (< 2 kHz): Darker, bass-heavy sounds (e.g., low drums, cello)
                           - Mid values (2-5 kHz): Balanced sounds (e.g., voice, guitar)
                           - High values (> 5 kHz): Brighter, treble-rich sounds (e.g., cymbals, hi-hats)
                           Useful for distinguishing timbre and tone quality.

   - spectral_rolloff_hz: The frequency below which 85% of the audio energy is contained.
                          Similar to spectral centroid but represents where "most" energy ends.
                          - Helps identify the presence of high-frequency content
                          - Generally higher than spectral centroid
                          - Useful for detecting percussive vs. sustained sounds

3. TEMPORAL FEATURES
   These features capture how the audio signal changes over time.

   - zero_crossing_rate: How many times the audio signal crosses zero per second.
                         Indicates how "noisy" or "unpredictable" the signal is.
                         - Low values (0.02-0.05): Smooth, tonal sounds (e.g., vowels, sustained notes)
                         - High values (0.1+): Noisy, percussive, or consonant sounds
                         Useful for speech/music classification and voice activity detection.

   - rms_energy: Root Mean Square energy - a measure of the signal's loudness/power.
                 Calculated as the square root of the mean of the squared signal.
                 - Range: 0 to 1 (normalized)
                 - Low values (.01-.1): Quiet passages
                 - High values (.3+): Loud passages
                 Useful for onset detection and energy-based segmentation.

4. MFCC (MEL-FREQUENCY CEPSTRAL COEFFICIENTS)
   MFCCs are the most widely used features in audio processing an
 recognition.
   They represent the audio in a way that mimics human hearing.

   The Mel scale compresses the frequency axis based on how humans perceive pitch:
   - Low frequencies are spread out (humans are more sensitive to differences in bass)
   - High frequencies are compressed (humans are less sensitive to differences in treble)

   - mfcc_0 to mfcc_12: 13 coefficients representing different aspects of the sound
     * mfcc_0: Represents overall loudness/energy of the signal
     * mfcc_1 to mfcc_12: Capture spectral characteristics

   Each coefficient represents a different aspect of the frequency spectrum:
   - Early coefficients (0-3) capture broad spectral shape (bass to treble)
   - Later coefficients (4-12) capture fine details and texture

   Uses: Widely used in music genre classification, speaker recognition, music similarity,
         and audio classification tasks.

5. CHROMA FEATURES
   - chroma_energy: Mean energy across the 12 chromatic (musical) pitch classes.
                    Based on the musical notes: C, C#, D, D#, E, F, F#, G, G#, A, A#, B

                    Represents the average "colorfulness" or "harmonic content" of the audio.
                    - Low values: Less harmonic content (more noise, percussion)
                    - High values: Rich harmonic content (sustained notes, chords)

                    Useful for:
                    * Music key detection
                    * Chord recognition
                    * Audio similarity based on harmonic content

6. TEMPO
   - tempo_bpm: Estimated tempo in Beats Per Minute.
                Calculated using onset detection and beat tracking.
                - Low values (60-90 BPM): Slow, relaxing music
                - Mid values (90-140 BPM): Typical pop, rock, dance music
                - High values (140+ BPM): Energetic, fast-paced music

                Useful for:
                * Genre classification
                * Music mood/energy detection
                * Synchronization and beat alignment

APPLICATION EXAMPLES:
====================

Music Genre Classification:
  Use MFCCs (0-12) + Spectral Centroid + RMS Energy to classify into genres.

Audio Similarity/Recommendation:
  Compare MFCC profiles and chromatic features between songs.

Speech/Music Classification:
  High zero crossing rate + low chroma energy → likely speech
  Low zero crossing rate + high chroma energy → likely music

Music Mood Detection:
  High energy + high tempo + bright spectral features → happy/energetic
  Low energy + low tempo + dark spectral features → sad/calm

Onset/Beat Detection:
  Use RMS energy changes and spectral features to find music events.

"""

from pathlib import Path
from typing import List

import librosa
import numpy as np

from .models.audio_features import AudioFeatures


def extract_audio_features(filepath: str) -> AudioFeatures:
    """
    Extract audio features from an audio file using librosa.

    This function loads an audio file and extracts a comprehensive set of features
    including spectral, temporal, harmonic, and rhythmic characteristics. All features
    are averaged across the entire audio file to produce a single feature vector.

    Args:
        filepath (str): Path to the audio file (.wav, .mp3, .flac, .m4a, .ogg, etc.)

    Returns:
        AudioFeatures: A SQLModel instance containing all extracted features with
                      the following attributes:
                      - filename: Original audio filename
                      - duration_seconds: Total audio duration
                      - sample_rate_hz: Audio sample rate
                      - spectral_centroid_hz: Center of mass of frequency spectrum
                      - spectral_rolloff_hz: Frequency containing 85% of energy
                      - zero_crossing_rate: Rate of signal zero-crossings
                      - rms_energy: Root mean square energy (loudness)
                      - tempo_bpm: Estimated tempo
                      - chroma_energy: Mean harmonic energy
                      - mfcc_0 to mfcc_12: 13 Mel-Frequency Cepstral Coefficients

    Raises:
        FileNotFoundError: If the audio file does not exist at the specified path.
        RuntimeError: If audio processing fails (corrupted file, unsupported format, etc.)

    Example:
        >>> features = extract_audio_features("song.wav")
        >>> print(f"Tempo: {features.tempo_bpm} BPM")
        >>> print(f"Duration: {features.duration_seconds} seconds")
    """
    file_path = Path(filepath)

    if not file_path.exists():
        raise FileNotFoundError(f"Audio file not found: {filepath}")

    try:
        # Load the audio file
        # y: Audio time series
        # sr: Sample rate (samples per second)
        y, sr = librosa.load(filepath)
        filename = file_path.name

        # ==================== BASIC AUDIO INFORMATION ====================
        duration_seconds = float(librosa.get_duration(y=y, sr=sr))
        sample_rate_hz = int(sr)

        # ==================== SPECTRAL FEATURES ====================
        # Spectral Centroid: Center of mass of the frequency spectrum
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        spectral_centroid_hz = float(np.mean(spectral_centroid))

        # Spectral Rolloff: Frequency below which 85% of the energy is concentrated
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
        spectral_rolloff_hz = float(np.mean(spectral_rolloff))

        # ==================== TEMPORAL FEATURES ====================
        # Zero Crossing Rate: How often the signal changes sign (crosses zero)
        zcr = librosa.feature.zero_crossing_rate(y)[0]
        zero_crossing_rate = float(np.mean(zcr))

        # RMS Energy: Root Mean Square energy - represents loudness/power
        rms = librosa.feature.rms(y=y)[0]
        rms_energy = float(np.mean(rms))

        # ==================== MFCC COEFFICIENTS ====================
        # Mel-Frequency Cepstral Coefficients: Represent audio as humans hear it
        # 13 coefficients capture different aspects of spectral content
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        mfcc_values = {f"mfcc_{i}": float(np.mean(mfccs[i])) for i in range(len(mfccs))}

        # ==================== CHROMA FEATURES ====================
        # Chroma STFT: Energy in 12 musical pitch classes (C, C#, D, ... B)
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        chroma_energy = float(np.mean(chroma))

        # ==================== TEMPO/RHYTHM ====================
        # Estimate tempo using onset strength and beat tracking
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
        # Extract scalar value - ensure tempo is a single float
        tempo_bpm = float(np.asarray(tempo).item() if np.isscalar(tempo) else tempo[0])

        # ==================== CREATE AND RETURN AUDIOFEATURES MODEL ====================
        features = AudioFeatures(
            filename=filename,
            duration_seconds=duration_seconds,
            sample_rate_hz=sample_rate_hz,
            spectral_centroid_hz=spectral_centroid_hz,
            spectral_rolloff_hz=spectral_rolloff_hz,
            zero_crossing_rate=zero_crossing_rate,
            rms_energy=rms_energy,
            tempo_bpm=tempo_bpm,
            chroma_energy=chroma_energy,
            **mfcc_values,
        )

        return features

    except Exception as e:
        raise RuntimeError(f"Error processing audio file {filename}: {str(e)}") from e


def extract_features_from_directory(directory: str) -> List[AudioFeatures]:
    """
    Extract audio features from all audio files in a directory.

    Recursively processes all audio files with supported formats in the given directory.
    Skips files that cannot be processed and continues with the rest.

    Supported audio formats:
        - .wav (WAV/RIFF)
        - .mp3 (MPEG-1 Audio Layer III)
        - .flac (Free Lossless Audio Codec)
        - .m4a (MPEG-4 Audio)
        - .ogg (Ogg Vorbis)

    Args:
        directory (str): Path to directory containing audio files

    Returns:
        List[AudioFeatures]: List of AudioFeatures instances for all successfully
        processed audio files in the directory.

    Raises:
        FileNotFoundError: If the directory does not exist.

    Example:
        >>> features_list = extract_features_from_directory("./music_library")
        >>> print(f"Processed {len(features_list)} files")
        >>> for features in features_list:
            ...     print(f"{features.filename}: {features.tempo_bpm} BPM")
    """
    audio_extensions = {".flac", ".wav", ".mp3", ".m4a", ".ogg"}
    dir_path = Path(directory)

    if not dir_path.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")

    all_features = []

    # Sort files for consistent processing order
    for filepath in sorted(dir_path.iterdir()):
        if filepath.suffix.lower() in audio_extensions:
            try:
                features = extract_audio_features(str(filepath))
                all_features.append(features)
            except Exception as e:
                # Log warning and continue processing remaining files
                print(f"Warning: Skipped {filepath.name} - {str(e)}")
                continue

    return all_features
