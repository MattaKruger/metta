from typing import Annotated, List

from fastapi import APIRouter, Depends
from pylast import LastFMNetwork, PlayedTrack, md5

from ..dependencies.last_fm import get_lastfm_network
from ..settings import Settings

settings = Settings()

router = APIRouter(
    prefix="/last_fm",
    tags=["last_fm"],
    dependencies=[Depends(get_lastfm_network)],
    responses={404: {"Description": "Not found"}},
)


def get_lastfm_network() -> LastFMNetwork:
    return LastFMNetwork(
        api_key=settings.last_fm_api_key,
        api_secret=settings.last_fm_secret,
        username=settings.last_fm_user,
        password_hash=(md5(settings.last_fm_pass)),
    )


@router.get("/current")
def get_current_track(last_fm: LastFMNetwork = Depends(get_lastfm_network)):
    pass


@router.get("/recent")
def get_recent_tracks(last_fm: LastFMNetwork = Depends(get_lastfm_network)):
    played_tracks: List[PlayedTrack] = last_fm.get_user(
        settings.last_fm_user
    ).get_recent_tracks()
    tags = {}
    for played_track in played_tracks:
        # print(played_track.track.artist, played_track.track.title)
        tags[played_track.track.artist] = played_track.track.get_top_tags(5)
    print(tags)
    return played_tracks


@router.get("/tag")
def get_track(
    artist: str, title: str, last_fm: LastFMNetwork = Depends(get_lastfm_network)
):
    print(last_fm.get_track(artist, title))
