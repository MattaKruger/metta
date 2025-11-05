#!/usr/bin/env python3
"""
View Extracted Audio Features from Database

This script queries and displays audio features stored in the SQLite database.

Usage:
    python view_features.py
    python view_features.py --limit 5
    python view_features.py --filename "NBSS II.flac"
    python view_features.py --json
"""

import argparse
import json
from typing import Optional

from sqlalchemy.pool import StaticPool
from sqlmodel import Session, create_engine, select

from models.features import AudioFeatures

# Database configuration
DATABASE_URL = "sqlite:///./audio_features.db"

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


def format_feature_table(features: list[AudioFeatures]) -> str:
    """Format features as a readable table."""
    if not features:
        return "No features found."

    output = []
    output.append("=" * 100)
    output.append(f"Total Features: {len(features)}")
    output.append("=" * 100)

    for i, f in enumerate(features, 1):
        output.append(f"\n[{i}] {f.filename}")
        output.append("-" * 100)
        output.append(f"  ID: {f.id}")
        output.append(f"  Created: {f.created_at}")
        output.append(f"\n  BASIC INFO:")
        output.append(f"    Duration: {f.duration_seconds:.2f} seconds")
        output.append(f"    Sample Rate: {f.sample_rate_hz} Hz")
        output.append(f"\n  SPECTRAL FEATURES:")
        output.append(f"    Spectral Centroid: {f.spectral_centroid_hz:.2f} Hz")
        output.append(f"    Spectral Rolloff: {f.spectral_rolloff_hz:.2f} Hz")
        output.append(f"\n  TEMPORAL FEATURES:")
        output.append(f"    Zero Crossing Rate: {f.zero_crossing_rate:.4f}")
        output.append(f"    RMS Energy: {f.rms_energy:.4f}")
        output.append(f"\n  TEMPO:")
        output.append(f"    Tempo: {f.tempo_bpm:.2f} BPM")
        output.append(f"\n  CHROMA:")
        output.append(f"    Chroma Energy: {f.chroma_energy:.4f}")
        output.append(f"\n  MFCCs:")
        mfcc_line = "    "
        for j in range(13):
            mfcc_val = getattr(f, f"mfcc_{j}")
            mfcc_line += f"MFCC_{j}: {mfcc_val:7.2f}  "
            if (j + 1) % 3 == 0:
                output.append(mfcc_line)
                mfcc_line = "    "
        if mfcc_line.strip():
            output.append(mfcc_line)

    output.append("\n" + "=" * 100)
    return "\n".join(output)


def format_feature_json(features: list[AudioFeatures]) -> str:
    """Format features as JSON."""
    features_dict = []
    for f in features:
        feature_dict = {
            "id": f.id,
            "filename": f.filename,
            "created_at": str(f.created_at),
            "basic_info": {
                "duration_seconds": f.duration_seconds,
                "sample_rate_hz": f.sample_rate_hz,
            },
            "spectral_features": {
                "spectral_centroid_hz": f.spectral_centroid_hz,
                "spectral_rolloff_hz": f.spectral_rolloff_hz,
            },
            "temporal_features": {
                "zero_crossing_rate": f.zero_crossing_rate,
                "rms_energy": f.rms_energy,
            },
            "tempo_bpm": f.tempo_bpm,
            "chroma_energy": f.chroma_energy,
            "mfccs": {f"mfcc_{i}": getattr(f, f"mfcc_{i}") for i in range(13)},
        }
        features_dict.append(feature_dict)

    return json.dumps(features_dict, indent=2)


def format_feature_summary(features: list[AudioFeatures]) -> str:
    """Format features as a summary table."""
    if not features:
        return "No features found."

    output = []
    output.append("=" * 120)
    output.append(
        f"{'ID':<5} {'Filename':<50} {'Duration':<10} {'Tempo':<8} {'Energy':<8} {'Centroid':<10}"
    )
    output.append("=" * 120)

    for f in features:
        output.append(
            f"{f.id:<5} {f.filename[:48]:<50} "
            f"{f.duration_seconds:>8.1f}s {f.tempo_bpm:>6.1f} "
            f"{f.rms_energy:>7.4f} {f.spectral_centroid_hz:>8.1f}Hz"
        )

    output.append("=" * 120)
    output.append(f"Total: {len(features)} files")
    output.append("=" * 120)
    return "\n".join(output)


def get_features(
    limit: Optional[int] = None,
    filename_filter: Optional[str] = None,
) -> list[AudioFeatures]:
    """Query features from database with optional filters."""
    with Session(engine) as session:
        statement = select(AudioFeatures)

        # Apply filename filter if provided
        if filename_filter:
            statement = statement.where(
                AudioFeatures.filename.contains(filename_filter)
            )

        # Apply limit if provided
        if limit:
            statement = statement.limit(limit)

        results = session.exec(statement).all()
        return list(results)


def main():
    """Main function to view audio features."""
    parser = argparse.ArgumentParser(
        description="View extracted audio features from database"
    )
    parser.add_argument(
        "--limit",
        "-l",
        type=int,
        help="Limit number of results to display",
    )
    parser.add_argument(
        "--filename",
        "-f",
        type=str,
        help="Filter by filename (partial match)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON format",
    )
    parser.add_argument(
        "--summary",
        "-s",
        action="store_true",
        help="Show summary table only",
    )

    args = parser.parse_args()

    # Get features from database
    features = get_features(limit=args.limit, filename_filter=args.filename)

    if not features:
        print("No features found in database.")
        return

    # Format and display output
    if args.json:
        print(format_feature_json(features))
    elif args.summary:
        print(format_feature_summary(features))
    else:
        print(format_feature_table(features))


if __name__ == "__main__":
    main()
