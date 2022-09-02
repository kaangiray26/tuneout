import re
import requests


class Services:
    def __init__(self):
        # self.amazon_music = Amazon_Music()
        # self.apple_music = Apple_Music()
        self.deezer = Deezer()
        # self.deezer_short = Deezer_Short()
        # self.qobuz = Qobuz()
        # self.soundcloud = SoundCloud()
        # self.spotify = Spotify()
        # self.tidal = Tidal()
        # self.youtube_music = YouTube_Music()
        # self.youtube_short = YouTube_Short()
        # self.youtube = YouTube()

    def get(self, domain, url):
        # if (domain == "music.amazon.com"):
        #     return self.deezer.gather(url)

        # if (domain == "music.apple.com"):
        #     return self.deezer.gather(url)

        if (domain == "www.deezer.com"):
            return self.deezer.gather(url)

        # if (domain == "deezer.page.link"):
        #     return self.deezer.gather(url)

        # if (domain == "open.qobuz.com"):
        #     return self.deezer.gather(url)

        # if (domain == "soundcloud.com"):
        #     return self.deezer.gather(url)

        # if (domain == "open.spotify.com"):
        #     return self.deezer.gather(url)

        # if (domain == "tidal.com"):
        #     return self.deezer.gather(url)

        # if (domain == "music.youtube.com"):
        #     return self.deezer.gather(url)

        # if (domain == "youtu.be"):
        #     return self.deezer.gather(url)

        # if (domain == "www.youtube.com"):
        #     return self.deezer.gather(url)

        return {"Error": "Couldn't find anything."}


class Deezer:
    def __init__(self):
        self.endpoint = "https://api.deezer.com"
        self.artist_regex = r"\/artist\/([0-9]+)"
        self.album_regex = r"\/album\/([0-9]+)"
        self.track_regex = r"\/track\/([0-9]+)"

    def gather(self, url):
        artist_match = re.split(self.artist_regex, url)
        if (artist_match and len(artist_match)) > 1:
            data = self.get_artist(artist_match[1])
            output = {
                "type": 'Artist',
                "artist": data['name'],
                "album": None,
                "track": None,
                "image": data['picture_xl'],
                "service": 'Deezer',
                "link": data['link']
            }
            return output

        album_match = re.split(self.album_regex, url)
        if (album_match and len(album_match)) > 1:
            data = self.get_album(album_match[1])
            output = {
                "type": 'Album',
                "artist": data['artist']['name'],
                "album": data['title'],
                "track": None,
                "image": data['cover_xl'],
                "service": 'Deezer',
                "link": data['link']
            }
            return output

        track_match = re.split(self.track_regex, url)
        if (track_match and len(track_match)) > 1:
            data = self.get_track(track_match[1])
            output = {
                "type": 'Track',
                "artist": data['artist']['name'],
                "album": data['album']['title'],
                "track": data['title'],
                "image": data['album']['cover_xl'],
                "service": 'Deezer',
                "link": data['link']
            }
            return output

        return {"Error": "Couldn't find anything."}

    def get_artist(self, id):
        response = requests.get(self.endpoint + "/artist/" + id)
        if not response.ok:
            return None
        return response.json()

    def get_album(self, id):
        response = requests.get(self.endpoint + "/album/" + id)
        if not response.ok:
            return None
        return response.json()

    def get_track(self, id):
        response = requests.get(self.endpoint + "/track/" + id)
        if not response.ok:
            return None
        return response.json()
