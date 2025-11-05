from pylast import LastFMNetwork, md5

from ..settings import Settings

settings = Settings()


def get_lastfm_network() -> LastFMNetwork:
    return LastFMNetwork(
        api_key=settings.last_fm_api_key,
        api_secret=settings.last_fm_secret,
        username=settings.last_fm_user,
        password_hash=(md5(settings.last_fm_pass)),
    )
