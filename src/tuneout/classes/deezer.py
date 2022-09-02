from copyreg import constructor
import re
import requests


class Deezer:
    def __init__(self):
        self.endpoint = "https://api.deezer.com"
        self.artist_regex = r"\/artist\/([0-9]+)"
        self.album_regex = r"\/album\/([0-9]+)"
        self.track_regex = r"\/track\/([0-9]+)"

    def shortlink(self, url):
        response = requests.head(url, allow_redirects=True)
        if not response.ok:
            return {"Error": "Couldn't retrieve information."}

        return self.gather(response.url)

    def find(self, data):
        if data['service'] == 'Deezer':
            return data['origin']

        if data['type'] == 'Artist':
            search = self.find_artist(data['artist'])

            if not len(search['data']):
                return {"Error": "Couldn't find anything."}

            return f"https://www.deezer.com/en/artist/{search['data'][0]['artist']['id']}"

        if data['type'] == 'Album':
            search = self.find_album(data['artist'], data['album'])

            if not len(search['data']):
                return {"Error": "Couldn't find anything."}

            return f"https://www.deezer.com/en/album/{search['data'][0]['album']['id']}"

        if data['type'] == 'Track':
            search = self.find_track(
                data['artist'], data['album'], data['track'])

            if not len(search['data']):
                return {"Error": "Couldn't find anything."}

            return f"https://www.deezer.com/en/track/{search['data'][0]['id']}"

        return {"Error": "Couldn't find anything."}

    def gather(self, url):
        artist_match = re.split(self.artist_regex, url)
        if (artist_match and len(artist_match)) > 1:
            data = self.get_artist(artist_match[1])

            if not data:
                return {"Error": "Couldn't retrieve information."}

            output = {
                "type": 'Artist',
                "artist": data['name'],
                "album": None,
                "track": None,
                "image": data['picture_xl'],
                "service": 'Deezer',
                "origin": data['link']
            }
            return output

        album_match = re.split(self.album_regex, url)
        if (album_match and len(album_match)) > 1:
            data = self.get_album(album_match[1])

            if not data:
                return {"Error": "Couldn't retrieve information."}

            output = {
                "type": 'Album',
                "artist": data['artist']['name'],
                "album": data['title'],
                "track": None,
                "image": data['cover_xl'],
                "service": 'Deezer',
                "origin": data['link']
            }
            return output

        track_match = re.split(self.track_regex, url)
        if (track_match and len(track_match)) > 1:
            data = self.get_track(track_match[1])

            if not data:
                return {"Error": "Couldn't retrieve information."}

            output = {
                "type": 'Track',
                "artist": data['artist']['name'],
                "album": data['album']['title'],
                "track": data['title'],
                "image": data['album']['cover_xl'],
                "service": 'Deezer',
                "origin": data['link']
            }
            return output

        return {"Error": "Couldn't find anything."}

    def find_artist(self, artist):
        query = ''

        if artist:
            query += f'artist:"{artist}" '

        if not len(query):
            return None
        
        response = requests.get(self.endpoint + "/search/", params={
            "q": f'artist:"{artist}"'
        })
        if not response.ok:
            return None
        return response.json()

    def find_album(self, artist, album):
        query = ''

        if artist:
            query += f'artist:"{artist}" '
        if album:
            query += f'album:"{album}"'

        if not len(query):
            return None
        
        response = requests.get(self.endpoint + "/search/", params={
            "q": query
        })
        if not response.ok:
            return None
        return response.json()

    def find_track(self, artist, album, track):
        query = ''

        if artist:
            query += f'artist:"{artist}" '
        if album:
            query += f'album:"{album}"'
        if track:
            query += f'track:"{track}"'

        if not len(query):
            return None

        response = requests.get(self.endpoint + "/search/", params={
            "q": query
        })
        if not response.ok:
            return None
        return response.json()

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
