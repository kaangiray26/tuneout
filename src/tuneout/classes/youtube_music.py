import re
import json
from ytmusicapi import YTMusic

class YouTube_Music:
    def __init__(self):
        self.ytmusic = YTMusic()
        self.artist_regex = r"\/channel\/(\S+)"
        self.album_regex = r"\/playlist\?list=(\S+)&|\/playlist\?list=(\S+)"
        self.track_regex = r"\/watch\?v=(\S+)&|\/watch\?v=(\S+)"

    def find(self, data):
        if data['service'] == 'YouTube Music':
            return data['origin']

        if data['type'] == 'Artist':
            search = self.find_artist([data['artist']])

            if not len(search):
                return {"Error": "Couldn't find anything."}

            return f"https://music.youtube.com/channel/{search[0]['browseId']}"

        if data['type'] == 'Album':
            search = self.find_album([data['artist'], data['album']])

            if not len(search):
                return {"Error": "Couldn't find anything."}
            
            return f"https://music.youtube.com/browse/{search[0]['browseId']}"

        if data['type'] == 'Track':
            search = self.find_track(
                [data['artist'], data['album'], data['track']])

            if not len(search):
                return {"Error": "Couldn't find anything."}

            with open('data.json', 'w') as f:
                json.dump(search, f)

            return f"https://music.youtube.com/watch/?v={search[0]['videoId']}"

        return {"Error": "Couldn't find anything."}

    def gather(self, url):
        artist_match = re.split(self.artist_regex, url.split("?")[0])
        if (artist_match and len(artist_match)) > 1:
            data = self.get_artist(artist_match[1])

            if not data:
                return {"Error": "Couldn't retrieve information."}

            output = {
                "type": 'Artist',
                "artist": data['name'],
                "album": None,
                "track": None,
                "image": data['thumbnails'][-1]['url'],
                "service": 'YouTube Music',
                "origin": f"https://music.youtube.com/channel/{data['channelId']}"
            }
            return output

        album_match = re.split(self.album_regex, url)
        if (album_match and len(album_match)) > 1:
            data = self.get_album(album_match[1])

            if not data:
                return {"Error": "Couldn't retrieve information."}

            output = {
                "type": 'Album',
                "artist": data['artists'][0]['name'],
                "album": data['title'],
                "track": None,
                "image": data['thumbnails'][-1]['url'],
                "service": 'YouTube Music',
                "origin": f"https://music.youtube.com/playlist?list={data['audioPlaylistId']}"
            }
            return output

        track_match = re.split(self.track_regex, url)
        if (track_match and len(track_match)) > 1:
            data = self.get_track(track_match[1])

            if not data:
                return {"Error": "Couldn't retrieve information."}

            output = {
                "type": 'Track',
                "artist": data['videoDetails']['author'],
                "album": None,
                "track": data['videoDetails']['title'],
                "image": data['videoDetails']['thumbnail']['thumbnails'][-1]['url'],
                "service": 'YouTube Music',
                "origin": f"https://music.youtube.com/playlist?list={data['videoDetails']['videoId']}"
            }
            return output

        return {"Error": "Couldn't find anything."}

    def find_artist(self, data):
        query = " ".join(list(filter(None, data)))
        response = self.ytmusic.search(query, filter='artists', limit=5, ignore_spelling=True)
        return response

    def find_album(self, data):
        query = " ".join(list(filter(None, data)))
        response = self.ytmusic.search(query, filter='albums', limit=5, ignore_spelling=True)
        return response

    def find_track(self, data):
        query = " ".join(list(filter(None, data)))
        response = self.ytmusic.search(query, filter='songs', limit=5, ignore_spelling=True)
        return response

    def get_artist(self, id):
        try:
            response = self.ytmusic.get_artist(id)
            return response
        except:
            return None

    def get_album(self, id):
        try:
            album_id = self.ytmusic.get_album_browse_id(id)
            response = self.ytmusic.get_album(album_id)
            return response
        except:
            return None

    def get_track(self, id):
        try:
            response = self.ytmusic.get_song(id)
            return response
        except:
            return None