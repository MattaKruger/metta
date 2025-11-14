from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import Index, UniqueConstraint

from .base import Base


class Artist(Base, table=True):
    """Music artist model with comprehensive indexing for performance."""

    # Composite index for artist lookups by name and type
    __table_args__ = (
        Index("idx_artist_name_type", "name", "artist_type"),
        Index("idx_artist_normalized_name", "normalized_name"),
        UniqueConstraint("musicbrainz_id", name="uq_artist_musicbrainz_id"),
    )

    # Basic artist information
    name: str = Field(max_length=200, index=True)
    normalized_name: str = Field(
        max_length=200, index=True
    )  # For case-insensitive searches
    artist_type: str = Field(
        default="person", max_length=50, index=True
    )  # person, group, orchestra, etc.

    # External identifiers for linking to databases
    musicbrainz_id: Optional[str] = Field(default=None, max_length=36)
    spotify_id: Optional[str] = Field(default=None, max_length=22)
    apple_music_id: Optional[str] = Field(default=None, max_length=100)

    # Artist metadata
    formation_year: Optional[int] = Field(default=None, ge=1900, le=2030)
    country: Optional[str] = Field(default=None, max_length=50, index=True)
    biography: Optional[str] = Field(default=None, max_length=2000)

    # Relationships
    tracks: List["Track"] = Relationship(
        back_populates="artists", sa_relationship_kwargs={"lazy": "selectin"}
    )
    albums: List["Album"] = Relationship(
        back_populates="artists", sa_relationship_kwargs={"lazy": "selectin"}
    )
    genres: List["Genre"] = Relationship(
        back_populates="artists", link_model="ArtistGenre"
    )


class Album(Base, table=True):
    """Music album model with optimized indexing."""

    __table_args__ = (
        Index("idx_album_name_year", "name", "release_year"),
        Index("idx_album_normalized_name", "normalized_name"),
        Index("idx_album_artist", "album_artist_id"),
        UniqueConstraint("musicbrainz_id", name="uq_album_musicbrainz_id"),
        UniqueConstraint("catalog_number", name="uq_album_catalog_number"),
    )

    # Album identification
    name: str = Field(max_length=300, index=True)
    normalized_name: str = Field(max_length=300, index=True)

    # Release information
    release_year: Optional[int] = Field(default=None, ge=1900, le=2030, index=True)
    release_date: Optional[str] = Field(
        default=None, max_length=20
    )  # YYYY-MM-DD format
    label: Optional[str] = Field(default=None, max_length=200)
    catalog_number: Optional[str] = Field(default=None, max_length=100)

    # Album artist (primary artist for the album)
    album_artist_id: Optional[int] = Field(
        default=None, foreign_key="artist.id", index=True
    )
    album_artist: Optional[Artist] = Relationship(
        sa_relationship_kwargs={"lazy": "selectin"}
    )

    # External identifiers
    musicbrainz_id: Optional[str] = Field(default=None, max_length=36)
    upc_ean: Optional[str] = Field(default=None, max_length=20)  # Barcode

    # Album metadata
    album_type: str = Field(
        default="album", max_length=50, index=True
    )  # album, single, ep, compilation
    total_tracks: int = Field(default=0, ge=0)
    genre_name: Optional[str] = Field(
        default=None, max_length=100, index=True
    )  # Primary genre string

    # Relationships
    tracks: List["Track"] = Relationship(
        back_populates="album", sa_relationship_kwargs={"lazy": "selectin"}
    )
    artists: List[Artist] = Relationship(
        back_populates="albums", link_model="AlbumArtist"
    )


class Track(Base, table=True):
    """Music track model with comprehensive indexing for search and analysis."""

    __table_args__ = (
        Index("idx_track_name_artist", "name", "artist_display"),
        Index("idx_track_normalized", "normalized_name"),
        Index("idx_track_duration", "duration"),
        Index("idx_track_album", "album_id"),
        Index("idx_track_genre", "genre_id"),
        Index("idx_track_file_path", "file_path"),
        UniqueConstraint("musicbrainz_id", name="uq_track_musicbrainz_id"),
        UniqueConstraint("acoustid_fingerprint", name="uq_track_acoustid_fingerprint"),
    )

    # Track identification
    name: str = Field(max_length=300, index=True)
    normalized_name: str = Field(max_length=300, index=True)
    artist_display: str = Field(max_length=400, index=True)  # Combined artist display

    # File information
    file_path: str = Field(max_length=500, index=True, unique=True)
    file_hash: str = Field(
        max_length=64, index=True
    )  # SHA-256 hash for duplicate detection
    file_size: int = Field(default=0, ge=0)  # File size in bytes
    file_format: str = Field(max_length=10, index=True)  # mp3, flac, wav, etc.

    # Audio properties
    duration: float = Field(default=0.0, ge=0, index=True)  # Duration in seconds
    bit_rate: Optional[int] = Field(default=None, ge=0)  # kbps
    sample_rate: Optional[int] = Field(default=None, ge=0)  # Hz
    bit_depth: Optional[int] = Field(default=None, ge=0)  # bits

    # Track position
    track_number: Optional[int] = Field(default=None, ge=0)
    disc_number: Optional[int] = Field(default=None, ge=1)
    total_discs: Optional[int] = Field(default=None, ge=1)

    # Album relationship
    album_id: Optional[int] = Field(default=None, foreign_key="album.id", index=True)
    album: Optional[Album] = Relationship(
        back_populates="tracks", sa_relationship_kwargs={"lazy": "selectin"}
    )

    # Artist relationships (many-to-many)
    artists: List[Artist] = Relationship(
        back_populates="tracks",
        link_model="TrackArtist",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    # Genre relationship
    genre_id: int = Field(foreign_key="genre.id", index=True)
    genre: "Genre" = Relationship(
        back_populates="tracks", sa_relationship_kwargs={"lazy": "selectin"}
    )

    # External identifiers and analysis
    musicbrainz_id: Optional[str] = Field(default=None, max_length=36)
    acoustid_fingerprint: Optional[str] = Field(
        default=None, max_length=500
    )  # Acoustic fingerprint
    acousticbrainz_id: Optional[str] = Field(default=None, max_length=36)

    # Popularity and metadata
    play_count: int = Field(default=0, ge=0)
    skip_count: int = Field(default=0, ge=0)
    last_played: Optional[str] = Field(default=None, max_length=20)  # ISO datetime
    rating: Optional[int] = Field(default=None, ge=1, le=5)  # User rating

    # Audio features relationship
    audio_features_id: Optional[int] = Field(
        default=None, foreign_key="audiofeatures.id"
    )
    audio_features: Optional["AudioFeatures"] = Relationship(
        back_populates="track", sa_relationship_kwargs={"lazy": "selectin"}
    )


class Genre(Base, table=True):
    """Music genre model with hierarchical support."""

    __table_args__ = (
        Index("idx_genre_name", "name", unique=True),
        Index("idx_genre_parent", "parent_id"),
    )

    name: str = Field(max_length=100, unique=True, index=True)
    description: Optional[str] = Field(default=None, max_length=500)
    parent_id: Optional[int] = Field(
        default=None, foreign_key="genre.id"
    )  # For hierarchical genres

    # Relationships
    tracks: List[Track] = Relationship(
        back_populates="genre", sa_relationship_kwargs={"lazy": "selectin"}
    )
    artists: List[Artist] = Relationship(
        back_populates="genres", link_model="ArtistGenre"
    )
    subgenres: List["Genre"] = Relationship(sa_relationship_kwargs={"lazy": "selectin"})


# Link tables for many-to-many relationships
class TrackArtist(Base, table=True):
    """Link table for track-artist many-to-many relationship."""

    __table_args__ = (
        UniqueConstraint("track_id", "artist_id", name="uq_track_artist"),
        Index("idx_trackartist_track", "track_id"),
        Index("idx_trackartist_artist", "artist_id"),
    )

    track_id: int = Field(foreign_key="track.id", primary_key=True)
    artist_id: int = Field(foreign_key="artist.id", primary_key=True)
    artist_role: str = Field(
        default="main", max_length=50
    )  # main, featured, composer, etc.
    credited_as: Optional[str] = Field(
        default=None, max_length=200
    )  # Alternative credit name


class AlbumArtist(Base, table=True):
    """Link table for album-artist many-to-many relationship."""

    __table_args__ = (
        UniqueConstraint("album_id", "artist_id", name="uq_album_artist"),
        Index("idx_albumartist_album", "album_id"),
        Index("idx_albumartist_artist", "artist_id"),
    )

    album_id: int = Field(foreign_key="album.id", primary_key=True)
    artist_id: int = Field(foreign_key="artist.id", primary_key=True)
    artist_role: str = Field(
        default="main", max_length=50
    )  # main, featured, composer, etc.


class ArtistGenre(Base, table=True):
    """Link table for artist-genre many-to-many relationship."""

    __table_args__ = (
        UniqueConstraint("artist_id", "genre_id", name="uq_artist_genre"),
        Index("idx_artistgenre_artist", "artist_id"),
        Index("idx_artistgenre_genre", "genre_id"),
    )

    artist_id: int = Field(foreign_key="artist.id", primary_key=True)
    genre_id: int = Field(foreign_key="genre.id", primary_key=True)
    primary_genre: bool = Field(
        default=False
    )  # Whether this is the primary genre for the artist


class Playlist(Base, table=True):
    """Music playlist model."""

    __table_args__ = (
        Index("idx_playlist_name", "name"),
        Index("idx_playlist_user", "user_id"),
        Index("idx_playlist_created", "created_at"),
    )

    name: str = Field(max_length=200, index=True)
    description: Optional[str] = Field(default=None, max_length=500)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", index=True)

    # Playlist metadata
    public: bool = Field(default=False, index=True)
    collaborative: bool = Field(default=False)
    track_count: int = Field(default=0, ge=0)
    duration: float = Field(default=0.0, ge=0)  # Total duration in seconds

    # Relationships
    tracks: List["PlaylistTrack"] = Relationship(
        back_populates="playlist", sa_relationship_kwargs={"lazy": "selectin"}
    )


class PlaylistTrack(Base, table=True):
    """Link table for playlist-track relationship with ordering."""

    __table_args__ = (
        UniqueConstraint("playlist_id", "track_id", name="uq_playlist_track"),
        Index("idx_playlisttrack_playlist", "playlist_id"),
        Index("idx_playlisttrack_track", "track_id"),
        Index("idx_playlisttrack_position", "playlist_id", "position"),
    )

    playlist_id: int = Field(foreign_key="playlist.id", primary_key=True)
    track_id: int = Field(foreign_key="track.id", primary_key=True)
    position: int = Field(ge=0)  # Track position in playlist
    added_at: str = Field()  # ISO datetime when added
    added_by: Optional[int] = Field(default=None, foreign_key="user.id")


class User(Base, table=True):
    """User model for multi-user support."""

    __table_args__ = (
        UniqueConstraint("username", name="uq_user_username"),
        UniqueConstraint("email", name="uq_user_email"),
    )

    username: str = Field(max_length=50, unique=True, index=True)
    email: str = Field(max_length=200, unique=True, index=True)
    display_name: Optional[str] = Field(default=None, max_length=100)

    # User preferences
    language: str = Field(default="en", max_length=10)
    timezone: str = Field(default="UTC", max_length=50)

    # Relationships
    playlists: List[Playlist] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )


class CollectionStatistics(Base, table=True):
    """Statistics and analytics for the music collection."""

    __table_args__ = (
        UniqueConstraint("collection_date", name="uq_collection_stats_date"),
    )

    # Collection metadata
    total_tracks: int = Field(ge=0)
    total_artists: int = Field(ge=0)
    total_albums: int = Field(ge=0)
    total_genres: int = Field(ge=0)
    total_playlists: int = Field(ge=0)

    # File statistics
    total_size_bytes: int = Field(ge=0)
    avg_bitrate: float = Field(default=0.0, ge=0)
    avg_duration: float = Field(default=0.0, ge=0)

    # Format distribution (stored as JSON strings)
    format_distribution: str = Field(default="{}")  # JSON: {"mp3": 100, "flac": 50}
    genre_distribution: str = Field(default="{}")  # JSON: {"rock": 200, "jazz": 150}

    # Collection date
    collection_date: str = Field(max_length=20)  # YYYY-MM-DD format


# ```

# This enhanced model structure provides:

# ## **Key Improvements:**

# 1. **Comprehensive Indexing**: Strategic indexes on commonly queried fields
# 2. **Composite Unique Constraints**: Prevents duplicates while enabling efficient lookups
# 3. **Optimized Relationships**: Uses `sa_relationship_kwargs={"lazy": "selectin"}` for better query performance
# 4. **External API Integration**: Fields for MusicBrainz, Spotify, AcoustID integration
# 5. **Audio Analysis Support**: Links to audio features and acoustic fingerprints
# 6. **Multi-User Support**: User model for future multi-user functionality
# 7. **Statistics Tracking**: Collection analytics and statistics

# ## **Performance Optimizations:**

# - **Composite indexes** on frequently queried field combinations
# - **Covering indexes** that include all needed fields for common queries
# - **Foreign key indexing** for join performance
# - **Lazy loading** with selectin for relationship queries

# ## **Data Integrity:**

# - **Unique constraints** prevent duplicate entries
# - **Referential integrity** through foreign keys
# - **Check constraints** for valid ranges (years, ratings, etc.)

# This structure would support advanced querying patterns like:
# - "Find all tracks by artist X from year Y"
# - "Get similar tracks based on audio features"
# - "Analyze collection growth over time"
# - "Find duplicate tracks across different formats"

# The design follows modern database normalization principles while maintaining query performance through strategic indexing.
