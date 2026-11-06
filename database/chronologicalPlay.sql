-- Finds and lists all play events in chronological order
SELECT 
  play.played_at, --timestamp 
  track.title  AS track_title, 
  album.title  AS album_title, 
  artist.name  AS artist_name
FROM play_event play
JOIN track  ON play.track_id = track.id
JOIN album  ON track.album_id = album.id
JOIN artist ON album.artist_id = artist.id
ORDER BY play.played_at;