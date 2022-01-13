import requests
import json

def autentication():
    CLIENT_ID = 'dcfe12fe9a444597983372226fb6b9f6'
    CLIENT_SECRET = '58cc390d911b402f9b9644ccbc25327c'
    AUTH_URL = 'https://accounts.spotify.com/api/token'

    auth_response = requests.post(AUTH_URL, {
    #'grant_type': 'client_credentials',
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    })
    auth_response_data = auth_response.json()

    access_token = auth_response_data['access_token']

    headers = {
        'Authorization': 'Bearer '+str(access_token),
        'Content-Type': 'application/json'
    }
    return headers

def top_tracks_artist(name):
    search_item = 'https://api.spotify.com/v1/search?q=' + name + '&type=artist&market=ES&limit=1&offset=0'
    headers = autentication()
    search_response = requests.get(search_item, headers=headers)
    search_response = search_response.json()

    #comprobar si existe respuesta
    top_tracks_info = []
    if not search_response["artists"]["items"]:

        return top_tracks_info, name, ''

    id = search_response["artists"]["items"][0]["id"]

    top_tracks_url = 'https://api.spotify.com/v1/artists/' + str(id) + '/top-tracks?market=ES'
    top_tracks = requests.get(top_tracks_url, headers=headers)
    top_tracks = top_tracks.json()

    sequence = range(0,len(top_tracks["tracks"]))

    for i in sequence:
        top_tracks_info.append([ json.dumps(top_tracks["tracks"][i]["name"], ensure_ascii=False),
                                 json.dumps(top_tracks["tracks"][i]["popularity"]),
                                 json.dumps(top_tracks["tracks"][i]["preview_url"]),
                                 json.dumps(top_tracks["tracks"][i]["album"]["images"][2]["url"])

                                ])

    return top_tracks_info, name, id


def playlist_info(name):
    search_item = 'https://api.spotify.com/v1/search?q=' + name + '&type=playlist&market=ES&limit=2&offset=0'
    headers=autentication()
    search_response = requests.get(search_item, headers=headers)
    search_response = search_response.json()

    if search_response["playlists"]["total"]==0:
        return "null", 'null'
    else:

        id = search_response["playlists"]["items"][0]["id"]

        playlist_url = 'https://api.spotify.com/v1/playlists/' + str(id)
        playlist = requests.get(playlist_url, headers=headers)
        playlist = playlist.json()

        playlist_info = [json.dumps(playlist["name"],ensure_ascii=False), json.dumps(playlist["description"],ensure_ascii=False), json.dumps(playlist["owner"]["display_name"],ensure_ascii=False), json.dumps(playlist["followers"]["total"]), json.dumps(playlist["tracks"]["total"])]

        playlist_image_url = 'null'
        if playlist['images']:
            playlist_image_url = playlist['images'][0]['url']

        return playlist_info, playlist_image_url



def artist_info(name):
    search_item = 'https://api.spotify.com/v1/search?q=' + name + '&type=artist&market=ES&limit=1&offset=0'
    search_response = requests.get(search_item, headers=autentication())
    search_response = search_response.json()

    if search_response["artists"]["total"]==0:
        return "null",'null'
    else:

        artist = search_response["artists"]["items"][0]
        artist_info = [json.dumps(artist["name"], ensure_ascii=False), json.dumps(artist["followers"]["total"]), json.dumps(artist["popularity"]), json.dumps(artist["genres"], ensure_ascii=False)]

        artist_image_url = artist['images'][1]['url']

        return artist_info, artist_image_url


def album_info(name):
    search_item = 'https://api.spotify.com/v1/search?q=' + name + '&type=album&market=ES&limit=1&offset=0'
    search_response = requests.get(search_item, headers=autentication())
    search_response = search_response.json()

    if search_response["albums"]["total"]==0:
        return "null",'null'
    else:

        album = search_response["albums"]["items"][0]

        artists = []
        sequence = range(0,len(album["artists"]))
        for i in sequence:
            artists.append(json.dumps(album["artists"][i]["name"],ensure_ascii=False))

        album_info = [json.dumps(album["name"],ensure_ascii=False), artists, json.dumps(album["album_type"], ensure_ascii=False), json.dumps(album["release_date"]), json.dumps(album["total_tracks"])]

        album_image_url = album['images'][1]['url']

        return album_info, album_image_url

def track_info(name):
    search_item = 'https://api.spotify.com/v1/search?q=' + name + '&type=track&market=ES&limit=1&offset=0'
    search_response = requests.get(search_item, headers=autentication())
    search_response = search_response.json()

    if search_response["tracks"]["total"]==0:
        return "null",'null'
    else:

        track = search_response["tracks"]["items"][0]
        track_image_url = track["album"]["images"][1]["url"]
        artists = []
        sequence = range(0,len(track["artists"]))
        for i in sequence:
            artists.append(json.dumps(track["artists"][i]["name"],ensure_ascii=False))


        track_info = [json.dumps(track["name"],ensure_ascii=False), artists, json.dumps(track["album"]["name"],ensure_ascii=False), json.dumps(track["popularity"])]
        return track_info, track_image_url

def track_audio_features(name):
    search_item = 'https://api.spotify.com/v1/search?q=' + name + '&type=track&market=ES&limit=1&offset=0'
    headers = autentication()
    search_response = requests.get(search_item, headers=headers)
    search_response = search_response.json()

    if search_response["tracks"]["total"]==0:
        return "null"
    else:

        id = search_response["tracks"]["items"][0]["id"]

        track_audio_features_url = 'https://api.spotify.com/v1/audio-features/' + str(id)
        all_features = requests.get(track_audio_features_url, headers=headers)
        all_features = all_features.json()

        track_features = [all_features["acousticness"], all_features["danceability"], all_features["energy"],
                        all_features["instrumentalness"], all_features["speechiness"], all_features["valence"]]

        return track_features

def track_preview(name):
    search_item = 'https://api.spotify.com/v1/search?q=' + name + '&type=track&market=ES&limit=1&offset=0'
    search_response = requests.get(search_item, headers=autentication())
    search_response = search_response.json()

    track_preview_info = []
    if search_response["tracks"]["total"]==0:
        return track_preview_info, "null"
    else:

        #track_preview = search_response["tracks"]["items"][0]["preview_url"]
        track = search_response['tracks']['items'][0]

        track_preview_info.append([ json.dumps(track['name'], ensure_ascii = False),
                                 json.dumps(track['popularity']),
                                 json.dumps(track['preview_url']),
                                 json.dumps(track['album']['images'][2]['url'])

                                ])

        artist_name = json.dumps(track['album']['artists'][0]['name'], ensure_ascii = False)

        return track_preview_info, artist_name


def playlist_popularity_vs_feature(name):

    search_item = 'https://api.spotify.com/v1/search?q=' + name + '&type=playlist&market=ES&limit=1&offset=0'
    headers=autentication()
    search_response = requests.get(search_item, headers=headers)
    search_response = search_response.json()

    if search_response["playlists"]["total"]==0:
        return "null",'null'

    else:

        id = search_response["playlists"]["items"][0]["id"]

        playlist_url = 'https://api.spotify.com/v1/playlists/' + str(id)
        playlist = requests.get(playlist_url, headers=headers)
        playlist_tracks = (playlist.json())["tracks"]["items"]

        popularities = []
        features = []
        sequence = range(0, len(playlist_tracks))

        for i in sequence:
            popularities.append(playlist_tracks[i]["track"]["popularity"])
            features.append([track_audio_features(json.dumps(playlist_tracks[i]["track"]["name"], ensure_ascii=False)), json.dumps(playlist_tracks[i]["track"]["name"], ensure_ascii=False)])
        return popularities, features


def album_popularity_vs_feature(name):
    search_item = 'https://api.spotify.com/v1/search?q=' + name + '&type=album&market=ES&limit=1&offset=0'
    headers = autentication()
    search_response = requests.get(search_item, headers=headers)
    search_response = search_response.json()

    if search_response["albums"]["total"]==0:
        return "null", "null"

    else:

        id = search_response["albums"]["items"][0]["id"]

        album_url = 'https://api.spotify.com/v1/albums/' + str(id) + '/tracks?market=ES&l&offset=0'
        album = requests.get(album_url, headers=headers)
        album_tracks = (album.json())["items"]

        popularities = []
        features = []
        sequence = range(0, len(album_tracks))

        for i in sequence:

            info, url = track_info(json.dumps(album_tracks[i]["name"], ensure_ascii=False))
            popularities.append(int(info[3]))

            features.append([track_audio_features(json.dumps(album_tracks[i]["name"], ensure_ascii=False)), json.dumps(album_tracks[i]["name"], ensure_ascii=False)])

        return popularities, features
