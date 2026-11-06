-- Groups all plays and displays top artists in descending order
SELECT
  artist.name AS artist_name,
  count(*) AS play_count
FROM play_event play
JOIN track ON play.track_id = track.id
JOIN album ON track.album_id = album.id
JOIN artist ON album.artist_id = artist.id
GROUP BY artist.id, artist.name
ORDER BY play_count DESC;