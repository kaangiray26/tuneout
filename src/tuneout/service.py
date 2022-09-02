from classes import *


class Service:
    def __init__(self):
        # self.amazon_music = Amazon_Music()
        # self.apple_music = Apple_Music()
        self.deezer = deezer.Deezer()
        # self.qobuz = Qobuz()
        # self.soundcloud = SoundCloud()
        # self.spotify = Spotify()
        # self.tidal = Tidal()
        self.youtube_music = youtube_music.YouTube_Music()

    def extract(self, domain, url):
        # if (domain == "music.amazon.com"):
        #     return self.deezer.gather(url)

        # if (domain == "music.apple.com"):
        #     return self.deezer.gather(url)

        if (domain == "www.deezer.com"):
            return self.deezer.gather(url)

        if (domain == "deezer.page.link"):
            return self.deezer.shortlink(url)

        # if (domain == "open.qobuz.com"):
        #     return self.deezer.gather(url)

        # if (domain == "soundcloud.com"):
        #     return self.deezer.gather(url)

        # if (domain == "open.spotify.com"):
        #     return self.deezer.gather(url)

        # if (domain == "tidal.com"):
        #     return self.deezer.gather(url)

        if (domain == "music.youtube.com"):
            return self.youtube_music.gather(url)

        return {"Error": "Couldn't find anything."}

    def construct(self, data):
        output = {
            "amazon_music": None,
            "apple_music": None,
            "deezer": self.deezer.find(data),
            "qobuz": None,
            "soundcloud": None,
            "spotify": None,
            "tidal": None,
            "youtube_music": self.youtube_music.find(data)
        }
        return output
