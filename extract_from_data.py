#!/usr/bin/env python3
"""
Extract Audio Features from Data Directory

This script extracts audio features from all audio files in the /data directory
and stores them in the SQLite database.

Usage:
    python extract_from_data.py

    # Or with custom directory path:
    python extract_from_data.py --directory ./custom_data
"""

import argparse
from pathlib import Path
from typing import List

from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine, select

from extract_features import extract_features_from_directory
from models.features import AudioFeatures

# Database configuration
DATABASE_URL = "sqlite:///./audio_features.db"

# Create engine with SQLite-specific configuration
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


def create_db_and_tables():
    """Create database tables if they don't exist."""
    SQLModel.metadata.create_all(engine)
    print("✓ Database tables initialized")


def check_existing_features(session: Session, filename: str) -> bool:
    """Check if features for a given filename already exist in the database."""
    statement = select(AudioFeatures).where(AudioFeatures.filename == filename)
    result = session.exec(statement).first()
    return result is not None


def save_features_to_db(
    features_list: List[AudioFeatures], skip_duplicates: bool = True
):
    """
    Save extracted features to the database.

    Args:
        features_list: List of AudioFeatures to save
        skip_duplicates: If True, skip files that already have features in DB
    """
    with Session(engine) as session:
        saved_count = 0
        skipped_count = 0

        for features in features_list:
            # Check if features already exist
            if skip_duplicates and check_existing_features(session, features.filename):
                print(f"  ⊘ Skipped (already exists): {features.filename}")
                skipped_count += 1
                continue

            # Save to database
            session.add(features)
            saved_count += 1
            print(f"  ✓ Saved: {features.filename}")

        # Commit all changes
        session.commit()

        print(f"\n{'=' * 60}")
        print(f"Summary:")
        print(f"  • Saved: {saved_count} files")
        print(f"  • Skipped: {skipped_count} files")
        print(f"  • Total processed: {len(features_list)} files")
        print(f"{'=' * 60}")


def main():
    """Main function to extract and save audio features."""
    parser = argparse.ArgumentParser(
        description="Extract audio features from directory and save to database"
    )
    parser.add_argument(
        "--directory",
        "-d",
        type=str,
        default="./data",
        help="Directory containing audio files (default: ./data)",
    )
    parser.add_argument(
        "--skip-duplicates",
        action="store_true",
        default=True,
        help="Skip files that already have features in database (default: True)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force re-extraction even if features already exist",
    )

    args = parser.parse_args()

    # Resolve directory path
    data_dir = Path(args.directory).resolve()

    if not data_dir.exists():
        print(f"❌ Error: Directory not found: {data_dir}")
        return

    if not data_dir.is_dir():
        print(f"❌ Error: Path is not a directory: {data_dir}")
        return

    print("=" * 60)
    print("Audio Feature Extraction")
    print("=" * 60)
    print(f"Directory: {data_dir}")
    print(f"Database: {DATABASE_URL}")
    print("=" * 60)
    print()

    # Create database tables
    create_db_and_tables()
    print()

    # Extract features from all audio files
    print(f"🎵 Extracting features from: {data_dir}")
    print()

    try:
        features_list = extract_features_from_directory(str(data_dir))

        if not features_list:
            print(f"⚠️  No audio files found in directory: {data_dir}")
            return

        print(f"\n✓ Successfully extracted features from {len(features_list)} files")
        print()

        # Save to database
        print("💾 Saving features to database...")
        print()
        skip_duplicates = not args.force and args.skip_duplicates
        save_features_to_db(features_list, skip_duplicates=skip_duplicates)

        print("\n✅ Feature extraction complete!")

    except Exception as e:
        print(f"\n❌ Error during feature extraction: {str(e)}")
        raise


if __name__ == "__main__":
    main()
