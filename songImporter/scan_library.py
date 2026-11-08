import os
import sys
from pathlib import Path

import mutagen
import psycopg

AUDIO_EXTS = {".mp3", ".flac", ".m4a", ".ogg", ".opus", ".wav"}
DB_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres:devMusic!@localhost:5432/musiclog",
)

def read_tags(path: Path):
    """Return a dict of tags, or None if the file is unreadable or incomplete."""
    try:
        f = mutagen.File(path, easy=True)
    except Exception:
        return None
    if f is None:
        return None

    def first(key):
        vals = f.get(key)
        return vals[0].strip() if vals else None

    title = first("title")
    artist = first("albumartist") or first("artist")
    album = first("album")

    """Prevents songs with incomplete data from being added"""
    if not (title and artist and album):
        return None

    date = first("date")
    year = int(date[:4]) if date and date[:4].isdigit() else None
    length = getattr(f.info, "length", None)
    duration_ms = int(length * 1000) if length else None

    return {"title": title, "artist": artist, "album": album, "year": year, "duration_ms": duration_ms}

def upsert_artist(cur, name):
    cur.execute(
        """INSERT INTO artist (name) VALUES (%s)
           ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name
           RETURNING id""",
        (name,),
    )
    return cur.fetchone()[0]

def upsert_album(cur, artist_id, title, year):
    cur.execute(
        """INSERT INTO album (artist_id, title, year) VALUES (%s, %s, %s)
           ON CONFLICT (artist_id, title)
           DO UPDATE SET year = COALESCE(album.year, EXCLUDED.year)
           RETURNING id""",
        (artist_id, title, year),
    )
    return cur.fetchone()[0]

def upsert_track(cur, album_id, title, duration_ms):
    cur.execute(
        """INSERT INTO track (album_id, title, duration_ms) VALUES (%s, %s, %s)
           ON CONFLICT (album_id, title)
           DO UPDATE SET duration_ms = EXCLUDED.duration_ms
           RETURNING id""",
        (album_id, title, duration_ms),
    )
    return cur.fetchone()[0]

def main(root: str):
    imported, skipped = 0, []
    with psycopg.connect(DB_URL) as conn, conn.cursor() as cur:
        for path in sorted(Path(root).expanduser().rglob("*")):
            if path.suffix.lower() not in AUDIO_EXTS:
                continue
            tags = read_tags(path)
            if tags is None:
                skipped.append(path)
                continue
            artist_id = upsert_artist(cur, tags["artist"])
            album_id = upsert_album(cur, artist_id, tags["album"], tags["year"])
            upsert_track(cur, album_id, tags["title"], tags["duration_ms"])
            imported += 1
        conn.commit()

    print(f"Imported {imported} tracks, skipped {len(skipped)}")
    for p in skipped:
        print(f"  skipped (missing or unreadable tags): {p}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: python scan_library.py <music folder>")
    main(sys.argv[1])