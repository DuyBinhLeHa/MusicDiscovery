# pylint: disable = E0401

"""
Provides functions to get data from Spotify.
"""
import os
import base64
import random
import requests

MARKET = "US"


def get_access_token():
    """
    Based on SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET for authentication with Spotify
    and return access_token variable.
    """
    auth = base64.standard_b64encode(
        bytes(
            f"{os.getenv('SPOTIFY_CLIENT_ID')}:{os.getenv('SPOTIFY_CLIENT_SECRET')}",
            "utf-8",
        )
    ).decode("utf-8")
    response = requests.post(
        "https://accounts.spotify.com/api/token",
        headers={"Authorization": f"Basic {auth}"},
        data={"grant_type": "client_credentials"},
    )
    json_response = response.json()
    return json_response["access_token"]


def get_song_data(artist_id, access_token):
    """
    Given a artist id and access token (authenticated), query Spotify using the artists API
    and return song data of that artist id.
    """
    response = requests.get(
        f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks",
        headers={"Authorization": f"Bearer {access_token}"},
        params={"market": MARKET},
    )
    json_response = response.json()
    track_json = random.choice(json_response["tracks"])  # choose random track
    song_name = track_json["name"]
    song_artist = ", ".join([artist["name"] for artist in track_json["artists"]])
    song_image_url = track_json["album"]["images"][0]["url"]
    preview_url = track_json["preview_url"]
    return (song_name, song_artist, song_image_url, preview_url)


def check_artist_id(artist_id, access_token):
    """
    Given a artist id and access token (authenticated), query Spotify using the artists API
    and return True if artist id already exists and vice versa.
    """
    response = requests.get(
        f"https://api.spotify.com/v1/artists/{artist_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    if response.status_code == 200:
        return True
    return False
