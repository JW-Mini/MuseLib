-- Table for artists
CREATE TABLE artist (
  id    BIGSERIAL PRIMARY KEY,
  name  TEXT NOT NULL UNIQUE
);

-- Table for artist albums; references artist id
CREATE TABLE album (
  id         BIGSERIAL PRIMARY KEY,
  artist_id  BIGINT NOT NULL REFERENCES artist(id),
  title      TEXT NOT NULL,
  year       SMALLINT,
  UNIQUE (artist_id, title)
);

-- Table for album tracs; references album id
CREATE TABLE track (
  id           BIGSERIAL PRIMARY KEY,
  album_id     BIGINT NOT NULL REFERENCES album(id),
  title        TEXT NOT NULL,
  duration_ms  INTEGER CHECK (duration_ms > 0),
  UNIQUE (album_id, title)
);

-- Table for tracking when track is played; references track id
CREATE TABLE play_event (
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  track_id   BIGINT NOT NULL REFERENCES track(id),
  played_at  TIMESTAMPTZ NOT NULL,
  source     TEXT NOT NULL,
  -- prevents duplicate listening events
  UNIQUE (source, track_id, played_at)
);

-- creates indicies to find specific play times/track ids faster
CREATE INDEX ON play_event (played_at);
CREATE INDEX ON play_event (track_id);

-- creates a saved SQL query for monthly play stats
CREATE VIEW play_stats_monthly AS
SELECT track_id,
       date_trunc('month', played_at)::date AS month,
       count(*) AS play_count
FROM play_event
GROUP BY track_id, date_trunc('month', played_at);