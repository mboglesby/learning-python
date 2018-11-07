##########################################################################
## importItunesTracks.py - v1.0 				    	##
## Created by Michael Oglesby for 'Using Python to Access Web Data'	##
##	class offered by University of Michigan on Coursera		##
## Usage: python3 importItunesTracks.py     				##
## Description: Prompts user for a filename (file specified should be   ##
##      in iTunes track export XML format). XML is parsed, and data is  ##
##      loaded into a simple SQLite database.                           ##
##########################################################################

import sys
import sqlite3
import xml.etree.ElementTree as xmlElementTree

# Function that accepts an iTunes XML format track and a key value as input,
# returns the value corresponding to the key
def extractValueForKey(track, key) :
    keyFound = False
    for entry in track :
        if keyFound :
            return entry.text
        if entry.tag == 'key' and entry.text == key :
            keyFound = True
    return None

# Open database connection and initialize cursor
dbConnection = sqlite3.connect('trackdb.sqlite')
dbCursor = dbConnection.cursor()

# Drop tables if they already exist
dbCursor.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Genre;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track''')

# Create tables
dbCursor.executescript('''
CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT UNIQUE
);

CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY 
        AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    genre_id  INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
)''')

# Prompt user for file name
fileName = input('Enter file name: ')

# Open file
try :
    fileHandle = open(fileName)
except :
    print("Error opening file")
    sys.exit(0)

# Create XML tree from file
xmlTree = xmlElementTree.parse(fileHandle)
xmlTreeRoot = xmlTree.getroot()

# Load all tracks into a list
tracks = xmlTreeRoot.findall('./dict/dict/dict')
print("Track count:", len(tracks))

# Iterate through each track and load into database
for track in tracks :
    trackName = extractValueForKey(track, "Name")
    albumName = extractValueForKey(track, "Album")
    artistName = extractValueForKey(track, "Artist")
    genre = extractValueForKey(track, "Genre")
    length = extractValueForKey(track, "Total Time")
    rating = extractValueForKey(track, "Rating")
    count = extractValueForKey(track, "Play Count")

    if not trackName :
        continue

    # Insert Genre
    if genre :
        dbCursor.execute('''
        INSERT OR IGNORE INTO Genre (name)
            VALUES (?)''', (genre,))
        dbCursor.execute('''
        SELECT id
            FROM Genre
            WHERE name = ?''', (genre,))
        genreId = dbCursor.fetchone()[0]
    else :
        genreId = None

    # Insert Artist
    if artistName :
        dbCursor.execute('''
        INSERT OR IGNORE INTO Artist (name)
            VALUES (?)''', (artistName,))
        dbCursor.execute('''
        SELECT id
            FROM Artist
            WHERE name = ?''', (artistName,))
        artistId = dbCursor.fetchone()[0]
    else :
        artistId = None

    # Insert Album
    if albumName :
        dbCursor.execute('''
        INSERT OR IGNORE INTO Album (artist_id, title)
            VALUES (?, ?)''', (artistId, albumName))
        dbCursor.execute('''
        SELECT id
            FROM Album
            WHERE title = ?''', (albumName,))
        albumId = dbCursor.fetchone()[0]
    else :
        albumId = None

    # Insert Track
    dbCursor.execute('''
    INSERT OR IGNORE INTO Track (title, album_id, genre_id, len, rating, count)
        VALUES (?, ?, ?, ?, ?, ?)''', (trackName, albumId, genreId, length, rating, count))
    dbConnection.commit()

# Run test query and print results
sql = '''
SELECT Track.title, Artist.name, Album.title, Genre.name
    FROM Track, Artist, Album, Genre
    WHERE Track.album_id = Album.id
    AND Track.genre_id = Genre.id
    AND Album.artist_id = Artist.id
    ORDER BY Artist.name, Track.title LIMIT 3'''

print("First 3 tracks in database:")
for row in dbCursor.execute(sql) :
    print(row)

dbCursor.close()
