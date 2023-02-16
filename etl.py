import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *

def process_song_file(cur, filepath):
    """
    Purpose: 
    process_song_file function parses and processes a JSON formatted song file
    Function uses Pandas module to read song file and create DataFrame
    Artist and Song data is extracted from the DataFrame and Inserted into respective Sparkify database tables
    
    Arg: 
    cur - PostgreSQL connection cursor
    filepath - path where JSON formatted song file is stored
    """    
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']].values[0].tolist()
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values[0].tolist()
    cur.execute(artist_table_insert, artist_data)

def process_log_file(cur, filepath):
    
    """
    Purpose: 
    process_log_file function parses and processes a JSON formatted log file
    Function uses Pandas module to read log file and create DataFrame
    Function derives various date and time attributes using Pandas dt method on timestamp field in log file
    User and Time tables are updated using data from log file
    Songplay table is updated using data from log file along with song_id and artist_id queried from song and
    artist tables, respectively
    
    Arg: 
    cur - PostgreSQL connection cursor
    filepath - path where JSON formatted log file is stored
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df.loc[df['page'] == 'NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit='ms')
    
    # insert time data records
    time_data = [df.ts.values, t.dt.hour.values, t.dt.day.values, t.dt.week.values, t.dt.month.values, t.dt.year.values, t.dt.dayofweek.values]

    column_labels = column_labels = ('start_time','hour', 'day', 'week', 'month', 'year', 'weekday')
    time_df = time_df = pd.DataFrame(dict(zip(column_labels, time_data)))

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (pd.to_datetime(row.ts, unit='ms'), row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent) 
        cur.execute(songplay_table_insert, songplay_data) 

def process_data(cur, conn, filepath, func):
    """
    Purpose: 
    process_data function builds a list of JSON files stored in the given filepath
    Itereates over list of files one at a time to process song and log data
    Calls process_song_file or process_log_file functions based on the user provided parameter
    
    Arg: 
    cur - PostgreSQL connection cursor
    conn - PostgreSQL connection
    filepath - path where JSON formatted file is stored
    func - function (song or log) to be called to process the files in the given filepath
    """ 
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))

def main():
    
    """
    Purpose: 
    Connect to PostgreSQL module (psycopg2) and get the Cursor to interact with PostgreSQL database using
    Python
    Call process_data function with filename defaulted to paths containing song and log data
    Func is defaulted for functions to be called along with respective data
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()