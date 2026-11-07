## MuseLib

PostgreSQL command-line based music library detailer. Runs on Docker for portability.

Import music libraries, track plays, find what you love.

### Setup

Download the repo as .ZIP, then unzip, open a CLI and move to the folder directory.

Before starting, you'll need a file named .env (no extension). This holds your password, which Postgres needs to start.
Copy the example .env into the directory.

Windows:
cp .envExample.txt .env

Make sure to manually change the password before continuing.
Now open Docker Desktop, then build the container.

Windows:
docker compose up -d
docker compose exec db psql -U postgres -d musiclog

Confirm the database is up with the following commmand:
\i searches/topArtistPlays.sql

You should see three artists.
Now, open the Python virtual environment and execute the song importer.

Windows: 
.venv/Scripts/activate
py scan_library.py Path/To/Your/Library

The importer looks through every audio file in the provided path and adds it to the database if all song info is present.
Finally, move back to the Docker container and run these two SQL commands:

SELECT count(*) FROM track;

SELECT art.name, trk.title AS song_name
FROM track trk
JOIN album alb  ON trk.album_id = alb.id
JOIN artist art ON alb.artist_id = art.id
GROUP BY art.name, trk.title
ORDER BY song_name DESC
LIMIT 10;

The count of songs should be increased by the number of songs the importer was able to import, and you should see some of the songs you imported. This import is idempotent, meaning running it multiple times with the same songs doesn't add extra files.