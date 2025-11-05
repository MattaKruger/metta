import pylast

from settings import Settings

settings = Settings()

lastfm_network = pylast.LastFMNetwork(
    api_key=settings.last_fm_api_key,
    api_secret=settings.last_fm_secret,
    username=settings.last_fm_user,
    password_hash=(pylast.md5(settings.last_fm_pass)),
)


def parse_played_tracks(played_tracks):
    """Parse Last.fm played tracks into a readable format.

    Args:
        played_tracks: List of PlayedTrack objects from pylast

    Returns:
        List of dictionaries with formatted track information
    """
    parsed_tracks = []

    for played_track in played_tracks:
        track_info = {
            "artist": str(played_track.track.artist),
            "title": str(played_track.track.title),
            "album": str(played_track.album),
            "played_at": played_track.playback_date,
            "timestamp": played_track.timestamp,
        }
        parsed_tracks.append(track_info)

    return parsed_tracks


def print_formatted_tracks(played_tracks):
    """Print tracks in a readable format.

    Args:
        played_tracks: List of PlayedTrack objects from pylast
    """
    parsed_tracks = parse_played_tracks(played_tracks)

    print(f"{'Artist':<30} {'Title':<40} {'Album':<35} {'Played At':<20}")
    print("=" * 125)

    for track in parsed_tracks:
        artist = track["artist"][:29]  # Truncate if too long
        title = track["title"][:39]
        album = track["album"][:34]
        played_at = track["played_at"]

        print(f"{artist:<30} {title:<40} {album:<35} {played_at:<20}")


def get_recent_tracks_formatted(limit=10):
    """Get and format recent tracks from Last.fm.

    Args:
        limit: Number of recent tracks to retrieve

    Returns:
        List of formatted track dictionaries
    """
    recent_tracks = lastfm_network.get_user("ackrite187").get_recent_tracks(limit=limit)
    return parse_played_tracks(recent_tracks)


# Get recent tracks and display them in a readable format
if __name__ == "__main__":
    recent_tracks = lastfm_network.get_user("ackrite187").get_recent_tracks()
    print_formatted_tracks(recent_tracks)
