INSERT INTO artist (name) VALUES ('Eir Aoi'), ('LiSA'), ('DECO*27');

-- On a fresh database these artists get ids 1, 2, 3 in that order
INSERT INTO album (artist_id, title, year) VALUES
  (1, 'I will... - EP', 2020),
  (2, 'LEO-NiNE', 2020),
  (3, 'Undercover - Single', 2021);

-- Albums get ids 1, 2, 3 likewise
INSERT INTO track (album_id, title, duration_ms) VALUES
  (1, 'I will...', 274000),
  (2, 'Gurenge', 238000),
  (3, 'UNDERCOVER', 204000);

INSERT INTO play_event (track_id, played_at, source) VALUES
  (1, '2026-11-01 08:15+09', 'manual'),
  (1, '2026-11-02 08:20+09', 'manual'),
  (2, '2026-11-02 18:05+09', 'manual'),
  (3, '2026-11-03 21:30+09', 'manual'),
  (1, '2026-11-04 23:10+09', 'manual'),
  (1, '2026-11-05 08:10+09', 'manual');
