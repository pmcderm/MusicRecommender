#!/usr/bin/env python3
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import string
import random
from IPython.display import display
import pandas as pd
import os
import numpy as np

# Authorization
def authentication():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="f84481c403ec4569a9ee6ab6959629e6",
                                               client_secret=os.environ["SPOTIFY_DEV_CLIENT_SECRET"],
                                               redirect_uri="http://localhost:8888/callback/",
                                               state=''.join(random.choices(string.ascii_uppercase +
                             string.digits, k=16)),
                                               scope="user-library-read"))
    return sp # ALSO SHOULD RETURN USER ID FOR SCALING

# Get's all of user's saved tracks with artist name and track id
def grab_saved_tracks(sp):
    # Retrieve ALL saved tracks, 50 at a time
    retrieve_tracks = sp.current_user_saved_tracks(50,0,None)
    saved_tracks = retrieve_tracks['items']
    while retrieve_tracks['next']:
        retrieve_tracks = sp.next(retrieve_tracks)
        saved_tracks.extend(retrieve_tracks['items'])

    # initialize empty dataframe to be filled with tracks
    col_track_id = 'track_id'
    col_track_name = 'track_name'
    col_artist_name = 'artist_name'
    df_saved_tracks = pd.DataFrame(columns=[col_track_id,col_track_name,col_artist_name])

    # fill data frame with saved tracks
    for item in saved_tracks:
        artist_names = list(map(lambda x: x['name'], item['track']['artists']))
        data = {col_track_id : item['track']['id'], col_track_name :item['track']['name'], col_artist_name : artist_names}
        to_be_added_item = pd.DataFrame(data=data, columns=[col_track_id,col_track_name,col_artist_name])
        df_saved_tracks = pd.concat([df_saved_tracks,to_be_added_item])

    return df_saved_tracks

sp_user = authentication()
df_saved_tracks = grab_saved_tracks(sp_user)

# save dataframe into local file
df_saved_tracks.to_csv('savedtracks.csv', index=False)

#for id in list(df_saved_tracks[col_track_id])
test_a_analysis = sp_user.audio_analysis('5u3MTOeVsXAiqFFLKve52k')
print(test_a_analysis['track']['tempo'])