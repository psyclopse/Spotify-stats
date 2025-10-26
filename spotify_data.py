import json
import pandas as pd

# Load JSON data from file
with open('spotify_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

df = pd.DataFrame(data)
df['minutes_played'] = df['ms_played'] / 1000 / 60

# Ask user how many items to display
while True:
    try:
        top_n = int(input("Display top how many artists and song? (e.g. 10, 15): "))
        if top_n > 0:
            break
        else:
            print("do you not know what a positve number is?")
    except ValueError:
        print("do you not know what a positve number is?.")

# Top artists
top_artists = (
    df.groupby('master_metadata_album_artist_name')['minutes_played']
    .sum()
    .sort_values(ascending=False)
    .head(top_n)
)

print(f"\nTop Artists")
for i, (artist, minutes) in enumerate(top_artists.items(), start=1):
    print(f"{i}. {artist}: {minutes:.2f} min")

# Top songs 
top_songs = (
    df.groupby('master_metadata_track_name')['minutes_played']
    .sum()
    .sort_values(ascending=False)
    .head(top_n)
)

print(f"\nTop Songs:")
for i, (song, minutes) in enumerate(top_songs.items(), start=1):
    print(f"{i}. {song}: {minutes:.2f} min")

# Total minutes listened
total_minutes = df['minutes_played'].sum()
print(f"\nTotal Minutes Listened: {total_minutes:.2f} min")

#Search for artist or song
def search_artist(df):
    artist_query = input("Enter artist's name: ").strip().lower()
    matches = df[df['master_metadata_album_artist_name'].str.lower().str.contains(artist_query, na=False)]
    if matches.empty:
        print(f"No songs found for artists matching '{artist_query}'.")
        return
    # Find best matched artist
    artist_stats = (
        matches.groupby('master_metadata_album_artist_name')['minutes_played']
        .sum()
        .sort_values(ascending=False)
    )
    print("\nMatched artists:")
    for i, (artist, minutes) in enumerate(artist_stats.items(), start=1):
        print(f"{i}. {artist}: {minutes:.2f} min")
    # Show stats for matched artist
    best_artist = artist_stats.index[0]
    artist_df = matches[matches['master_metadata_album_artist_name'] == best_artist]
    total_artist_minutes = artist_df['minutes_played'].sum()
    num_songs = artist_df['master_metadata_track_name'].nunique()
    print(f"\nStats for artist '{best_artist}':")
    print(f"- Total number of songs listened to by artist: {num_songs}")
    print(f"- Total minutes listened: {total_artist_minutes:.2f} min")
    print("\nSongs played and their minutes listened:")
    song_stats = (
        artist_df.groupby('master_metadata_track_name')['minutes_played']
        .sum()
        .sort_values(ascending=False)
    )
    for song, minutes in song_stats.items():
        print(f"  {song}: {minutes:.2f} min")

def search_song(df):
    song_query = input("Enter song's name: ").strip().lower()
    matches = df[df['master_metadata_track_name'].str.lower().str.contains(song_query, na=False)]
    if matches.empty:
        print(f"No songs found matching '{song_query}'.")
        return
    song_stats = (
        matches.groupby('master_metadata_track_name')['minutes_played']
        .sum()
        .sort_values(ascending=False)
    )
    print("\nMatched songs:")
    for i, (song, minutes) in enumerate(song_stats.items(), start=1):
        print(f"{i}. {song}: {minutes:.2f} min")
    # Show stats for top match
    best_song = song_stats.index[0]
    song_df = matches[matches['master_metadata_track_name'] == best_song]
    print(f"\nStats for song '{best_song}':")
    print(f"- Total minutes listened: {song_stats[best_song]:.2f} min")
    # Optionally, show artists who performed this song
    artists = song_df['master_metadata_album_artist_name'].unique()
    print(f"- Artist(s): {', '.join(artists)}")

# Main search loop
while True:
    search_choice = input("\ndo you want to search for anything else or exit? (artist/song/exit): ").strip().lower()
    if search_choice == 'artist':
        search_artist(df)
    elif search_choice == 'song':
        search_song(df)
    elif search_choice == 'exit':
        print("Goodbye!")
        break
    else:
        print("input 'artist', 'song', or 'exit'.")
