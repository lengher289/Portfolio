import requests
from bs4 import BeautifulSoup
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time


# Scrape data from billboard website

def scrape_billboard_year(year):
    """Scrape Billboard Hot 100 for a specific year
    
    Args:
        year (int): Year we want to extract data from

    Returns:
        temp_df (pandas.DataFrame): Dataframe containing the stripped information from the website, namely:
            Rank,Song,Artist
    """
    print(f"\nScraping year {year}...")
    
    url = f'https://www.billboard.com/charts/year-end/{year}/hot-100-songs/'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }


    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Reference: https://stackoverflow.com/questions/71461576/beautiful-soup-find-function-returning-none-even-though-element-exists-and-fin
    entries = soup.find_all('div', class_='o-chart-results-list-row-container')
    
    ranks = []
    songs = []
    artists = []

    for entry in entries:
        try:
            #rank from first span with class c-label
            rank = entry.find('span', class_='c-label').text.strip()
            
            #song title
            song_element = entry.find('h3', class_='c-title')
            song = song_element.text.strip() if song_element else "N/A"
            
            # looking specifically for the artist span
            # Updated to find the correct span for artist
            artist_element = entry.find('span', class_='c-label', 
                                     attrs={'for': 'chart-element-artist'})
            if not artist_element:
                artist_element = entry.select('li.o-chart-results-list__item span.c-label:not([for])')[1]
            artist = artist_element.text.strip() if artist_element else "N/A"
            
            #clean extra whitespace and formatting
            rank = ''.join(filter(str.isdigit, rank)) #make sure rank is a digit
            song = ' '.join(song.split())
            artist = ' '.join(artist.split())
            
            ranks.append(rank)
            songs.append(song)
            artists.append(artist)
            
        except AttributeError as e:
            print(f"Error processing entry: {e}")
            continue
        except IndexError as e:
            print(f"Error finding artist: {e}")
            continue

    temp_df = pd.DataFrame({
        'Rank': ranks,
        'Song': songs,
        'Artist': artists,
        'Year': year
    })

    temp_df['Rank'] = pd.to_numeric(temp_df['Rank'])
    temp_df = temp_df.sort_values('Rank')
    
    print(f"Found {len(temp_df)} songs for year {year}")

    return temp_df


def clean_artist_name(artist):
    """Extract only the first artist name before any collaborator indicators, this will reduce errors when searching for the songs via Spotify API
    This will serve as a helper function that will be applied to each row of the Artist column
    
    Args:
        artist (str): Artist of the song

    Returns:
        artist (str): Returns only the first artist
    """
    # collaboration indicators
    separators = [' Featuring ', ' X ', ' x ', ' & ', ' With ', ' Duet With ', ' + ']
    
    for sep in separators:
        if sep in artist:
            artist = artist.split(sep)[0]
    
    return artist.strip()



#scrape Billboard
print("Part 1: Scraping Billboard charts...")
years = [2020, 2019, 2018] # Change this later only handle 300 rows at a time
all_dfs = []

for year in years:
    try:
        year_df = scrape_billboard_year(year)
        all_dfs.append(year_df)
        
        if year != years[-1]:
            print("Waiting 3 seconds before next request...")
            time.sleep(3)
            
    except Exception as e:
        print(f"Error processing year {year}: {e}")
        continue

# Combine all years and clean up
billboard_df = pd.concat(all_dfs, ignore_index=True)
billboard_df = billboard_df.sort_values(['Year', 'Rank'])

# remove dataframes we dont need anymore for better memory allocation
del all_dfs
del year_df


###### Now we begin using Spotify API, more information can be found in thier documentation:
###### https://developer.spotify.com/documentation/web-api\
###### https://developer.spotify.com/documentation/web-api/reference/get-several-audio-features
###### We are opting to search for the songs via the song title and Artist, but there are API requests limits so we will need to implement wait times
###### There is another method of using Track ID of the song and making 1 request for every 100 tracks so we do not meet out limit however it will be
###### manual work or we can use the song and artist method to get the track ids first but for simplicity we will use the song and artist method to get
###### our data. For future enhancements we can read from data with Spotify IDs already intergrated to stay under the requests limit.
###### This method may take longer as we will implement longer wait times to requests (e.g. 5-10secs per request)


# Initialize Spotify client
CLIENT_ID = "" # enter your information here more information on how this is created can be found in the documentation mentioned above.
CLIENT_SECRET= ""

print("Initializing Spotify client...")
sp = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET
    ),
    requests_timeout=10
)

print("\nBillboard data collected. Starting Spotify feature extraction...")

# Initialize columns
spotify_columns = ['spotify_id', 'spotify_name', 'spotify_artist', 'spotify_album', 
                  'release_date', 'danceability', 'energy', 'key', 'loudness', 
                  'mode', 'speechiness', 'acousticness', 'instrumentalness', 
                  'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature']

for col in spotify_columns:
    billboard_df[col] = None

billboard_df['spotify_error'] = False # indicate if there was an error; intialize to False

#process each song
print("\nPart 2: Getting Spotify features...")
total_songs = len(billboard_df)

for idx, row in billboard_df.iterrows():
    try:
        print(f"Processing {row['Song']} by {row['Artist']} ({idx + 1}/{total_songs})") # TODO: Fix indexing of this since its not showing up properly starts at 200 not 1; Maybe reset index first

        # Clean artist name to get only the first artist
        main_artist = clean_artist_name(row['Artist']) # Previously without clean 78% success rate now 98% success rate with clean
        print("New Artist Query: ", main_artist)
        # Search for the track
        query = f"track:{row['Song']} artist:{main_artist}" # Only grab main artist to avoid errors
        results = sp.search(q=query, type='track', limit=1)

        if results['tracks']['items']:
            track_id = results['tracks']['items'][0]['id']
            track = results['tracks']['items'][0]
            features = sp.audio_features(track_id)[0]
            
            # Update DataFrame with Spotify data
            billboard_df.at[idx, 'spotify_id'] = track_id
            billboard_df.at[idx, 'spotify_name'] = track['name']
            billboard_df.at[idx, 'spotify_artist'] = track['artists'][0]['name']
            billboard_df.at[idx, 'spotify_album'] = track['album']['name']
            billboard_df.at[idx, 'release_date'] = track['album']['release_date']
            
            # Add audio features
            for feature in ['danceability', 'energy', 'key', 'loudness', 'mode',
                          'speechiness', 'acousticness', 'instrumentalness',
                          'liveness', 'valence', 'tempo', 'duration_ms',
                          'time_signature']:
                billboard_df.at[idx, feature] = features[feature]
                
        else:
            billboard_df.at[idx, 'spotify_error'] = True
            
    except Exception as e:
        print(f"Error processing {row['Song']}: {str(e)}")
        billboard_df.at[idx, 'spotify_error'] = True
    
    # Sleep to respect rate limits
    time.sleep(10)

# Final cleanup
final_df = billboard_df.copy()
del billboard_df

# get summary of dataset:

print("\nFinal Dataset Summary:")
print(f"Total songs: {len(final_df)}")
print("\nSongs per year:")
print(final_df['Year'].value_counts().sort_index())
print("\nSpotify match rate:")
print(f"Successfully matched: {sum(~final_df['spotify_error'])} songs")
print(f"Failed to match: {sum(final_df['spotify_error'])} songs")


# save this to csv so we can concat the datasets later on if we want more data
final_df.to_csv('new_billboard_spotify_data_part2.csv', index=False)