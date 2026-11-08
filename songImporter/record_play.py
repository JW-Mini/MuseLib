import argparse
from datetime import datetime, timezone

import psycopg

from scan_library import DB_URL, upsert_artist, upsert_album, upsert_track


def record_play(cur, artist, album, title, played_at, source):
    """Record one play. Returns True if new, False if it was a duplicate."""
    artist_id = upsert_artist(cur, artist)
    album_id = upsert_album(cur, artist_id, album, None)
    track_id = upsert_track(cur, album_id, title, None)
    cur.execute(
        """INSERT INTO play_event (track_id, played_at, source)
           VALUES (%s, %s, %s)
           ON CONFLICT (source, track_id, played_at) DO NOTHING
           RETURNING id""",
        (track_id, played_at, source),
    )
    return cur.fetchone() is not None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--artist", required=True)
    parser.add_argument("--album", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--at", help="ISO timestamp with offset; default: now")
    parser.add_argument("--source", default="manual")
    args = parser.parse_args()

    played_at = datetime.fromisoformat(args.at) if args.at else datetime.now(timezone.utc)
    if played_at.tzinfo is None:
        raise SystemExit("--at needs args UTC offset, e.g. 2026-11-07T08:15:00+09:00")

    with psycopg.connect(DB_URL) as conn, conn.cursor() as cur:
        is_new = record_play(cur, args.artist, args.album, args.title, played_at, args.source)
        conn.commit()
    print("recorded" if is_new else "duplicate, ignored")


if __name__ == "__main__":
    main()