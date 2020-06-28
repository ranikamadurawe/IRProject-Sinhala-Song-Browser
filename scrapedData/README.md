# sinhala-lyrics-corpus
Sinhala Lyrics corpus for Lyrics SE implementation for CS4642 

## Data Format
Data format of the json file

1. `artist`: List containing the name of Artists
2. `beat`: Beat of the song
3. `composer`: List containing the name of Composers
4. `genre`: List containing Genres
5. `key`: Key of the song
6. `movie` : Movie the song is from, (if any)
7. `shares`: No of time the song was shared in the original site
8. `songLyrics` : Unformatted song lyrics (for displaying)
9. `songLyricsSearchable` : Formatted song list for querying
10. `title`: Title of the song
11. `url`: url of the lyric. Used as the unique for scraping and indexing Data
12. `writer`: List containing the name of Writers
13. `views`: No of time the song was viewed in the original site

> Certain fields which were not available in the scraped site have been marked appropriatly.
