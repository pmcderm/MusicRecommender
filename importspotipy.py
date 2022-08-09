import spotipy
from spotipy.oauth2 import SpotifyOAuth
import string
import random
from IPython.display import display
import pandas as pd
import numpy as np

# Authorization
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="f84481c403ec4569a9ee6ab6959629e6",
                                               client_secret="4997dd3a43ee41adbf7b3d87c1e9479a",
                                               redirect_uri="http://localhost:8888/callback/",
                                               state=''.join(random.choices(string.ascii_uppercase +
                             string.digits, k=16)),
                                               scope="user-library-read"))

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


display(df_saved_tracks)