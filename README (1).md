# Data Modeling with Postgres
## Project Description

<p>Udacity, a startup company, created Sparkify, a music streaming service that imitates the real-world datasets of companies such as Pandora and Spotify. It has millions of users who play their favorite songs on a daily basis.</p>

<p>The goal of this project is to create a database that will allow Sparkify's analytics team to analyze the data collected by its users. They need a simple way to query the data they collect. In order to do so, they will need to store the data in a directory with .Json metadata and raw logs.</p>

### Project Dataset



## Database Schema

<p>We will be using a Star Schema for this project</p>

<p>The Star schema is a standard modeling approach that is commonly used in relational data warehouses. It allows modelers to classify their models as either fact or dimension.</p>

<p>A fact table can be used to store various events and observations, such as sales orders and stock balances. It can also contain dimension key columns that are related to dimension tables. These columns determine the granularity of the table and its dimensionality.</p>

<p>A dimension table can be used to describe various types of business entities, such as people, products, and concepts. The most common table in a star schema is the date dimension table. It can also contain descriptive and unique columns.</p>

<ul>
    <li>Dimension tables support filtering and grouping</li>
    <li>Fact tables support summarization</li>
</ul>

<p>The Sparkify database is not large so it lends itself to be used in a relational database. The datatypes are structured. A RDMS will allow analysts to aggregate the data efficiently which they'll need to use SQL joins for.</p>

Fact Table<br><br>
songplays - records in log data associated with song plays i.e. records with page NextSong<br>
songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent<br>
Dimension Tables<br><br>
users - users in the app<br>
user_id, first_name, last_name, gender, level<br>
songs - songs in music database<br>
song_id, title, artist_id, year, duration<br>
artists - artists in music database<br>
artist_id, name, location, latitude, longitude<br>
time - timestamps of records in songplays broken down into specific units<br>
start_time, hour, day, week, month, year, weekday<br>

## Project template

The data files, the project includes seven files:
1. ***create_tables.py*:** drops and creates your tables. You run this file to reset your tables before each time you run your ETL scripts.
2. ***etl.ipynb*:** reads and processes a single file from *song_data* and *log_data* and loads the data into your tables. This notebook contains detailed instructions on the ETL process for each of the tables.
3. ***etl.py*:** reads and processes files from *song_data* and *log_data* and loads them into your tables. You can fill this out based on your work in the ETL notebook.
4. ***README.md*:** provides discussion on this project.
5. ***sql_queries.py*:** contains all your sql queries, and is imported into the last three files above.
6. ***test.ipynb*:** displays the first few rows of each table to let us check on the database.

## How to Run

1. Run ***create_tables.py*** to create the database and tables.
2. Run ***etl.py*** to process for loading, extracting and inserting the data.
3. Run ***test.ipynb*** to confirm the creation of database and columns.