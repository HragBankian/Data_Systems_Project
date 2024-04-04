#-------------------------------------------------------- DDL --------------------------------------------------------------
#parent table
CREATE TABLE media_types (
    media_id INT AUTO_INCREMENT PRIMARY KEY,
    media_type VARCHAR(255) NOT NULL
);

#child table: 'songs' ISA 'media_types'
CREATE TABLE songs (
    song_id INT,
    song_name VARCHAR(255) NOT NULL,
    artist_name VARCHAR(255) NOT NULL,
    album VARCHAR(255),
    duration INT,
    FOREIGN KEY (song_id) REFERENCES media_types(media_id)
);

#child table: 'podcasts' ISA 'media_types'
CREATE TABLE podcasts (
    podcast_id INT,
    podcast_name VARCHAR(255) NOT NULL,
    publisher VARCHAR(255),
    overview VARCHAR(255),
    total_episodes INT,
	FOREIGN KEY (podcast_id) REFERENCES media_types(media_id)
);

#weak entity of 'podcasts'
CREATE TABLE available_markets (
    podcast_id INT,
    market_name VARCHAR(255) NOT NULL,
    PRIMARY KEY (podcast_id, market_name),
    CONSTRAINT fk_podcast_id_available_markets FOREIGN KEY (podcast_id) REFERENCES podcasts(podcast_id)
);

#referential integrity using triggers for 'songs' table
DELIMITER //
CREATE TRIGGER songs_before_insert_trigger
BEFORE INSERT ON songs
FOR EACH ROW
BEGIN
    DECLARE media_type_value VARCHAR(255);
    SELECT media_type INTO media_type_value FROM media_types WHERE media_id = NEW.song_id; -- Corrected to use NEW.song_id instead of NEW.media_id

    IF media_type_value IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Invalid media_type_id for songs';
    END IF;
END//
DELIMITER ;

#referential integrity using triggers for 'podcasts' table
DELIMITER //
CREATE TRIGGER podcasts_before_insert_trigger
BEFORE INSERT ON podcasts
FOR EACH ROW
BEGIN
    DECLARE media_type_value VARCHAR(255);
    SELECT media_type INTO media_type_value FROM media_types WHERE media_id = NEW.podcast_id; -- Corrected to use NEW.podcast_id instead of NEW.media_id

    IF media_type_value IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Invalid media_type_id for podcasts';
    END IF;
END//
DELIMITER ;

#view to display all media items
CREATE OR REPLACE VIEW all_media AS
SELECT
    song_id AS media_id,
    song_name AS media_title,
    'song' AS media_type
FROM
    songs
UNION ALL
SELECT
    podcast_id AS media_id,
    podcast_name AS media_title,
    'podcast' AS media_type
FROM
    podcasts;
    
#-------------------------------------------------------- DML --------------------------------------------------------------
#basic select with simple where clause
SELECT *
FROM songs
WHERE artist_name = 'Coldplay';

#basic select with simple group by clause (without having clause)
SELECT COUNT(song_id), artist_name
FROM songs
GROUP BY artist_name;

#basic select with simple group by clause (with having clause)
SELECT COUNT(podcast_id), publisher
FROM podcasts
GROUP BY publisher
HAVING COUNT(podcast_id) > 10;

#a simple join select query using cartesian product and where clause
SELECT *
FROM podcasts
CROSS JOIN available_markets
WHERE podcasts.podcast_id = available_markets.podcast_id;

#a simple join select query using on
SELECT *
FROM podcasts
JOIN available_markets
ON podcasts.podcast_id = available_markets.podcast_id;

#inner join
SELECT *
FROM podcasts
INNER JOIN available_markets ON podcasts.podcast_id = available_markets.podcast_id;

#outer left join
SELECT *
FROM podcasts
LEFT JOIN available_markets ON podcasts.podcast_id = available_markets.podcast_id;

#outer right join
SELECT *
FROM podcasts
RIGHT JOIN available_markets ON podcasts.podcast_id = available_markets.podcast_id;

#full join 
-- SELECT *
-- FROM podcasts
-- FULL JOIN available_markets ON podcasts.podcast_id = available_markets.podcast_id;
#full join gives an error: " Error Code: 1054. Unknown column 'podcasts.podcast_id' in 'on clause' "
#yet, the same syntax works in the left and right join 
#this might be an engine problem
#the full join can be simulated with the code below:

#full join simulation
SELECT *
FROM podcasts
LEFT JOIN available_markets ON podcasts.podcast_id = available_markets.podcast_id
UNION
SELECT *
FROM podcasts
RIGHT JOIN available_markets ON podcasts.podcast_id = available_markets.podcast_id;

#correlated query: find songs longer than average duration
SELECT song_id, song_name, artist_name, album, duration
FROM songs s1
WHERE duration > (
    SELECT AVG(duration)
    FROM songs s2
    WHERE s1.artist_name = s2.artist_name
);

#correlated query: find the podcast with the most total episodes 
SELECT podcast_id, podcast_name, publisher, overview, total_episodes
FROM podcasts p1
WHERE total_episodes > (
    SELECT MAX(total_episodes)
    FROM podcasts p2
    WHERE p1.podcast_id != p2.podcast_id
);

#intersect with set operations 
-- SELECT podcast_id, podcast_name, publisher, overview, total_episodes
-- FROM podcasts
-- INTERSECT
-- SELECT podcast_id, NULL, NULL, NULL, NULL
-- FROM available_markets;
#MySQL does not support INTERSECT
#here is an alternative to the code above:

#alternative code
SELECT podcast_id, podcast_name, publisher, overview, total_episodes
FROM podcasts p
WHERE EXISTS (
    SELECT 1
    FROM available_markets am
    WHERE p.podcast_id = am.podcast_id
);

#intersect equivalence without using set operations
SELECT podcasts.podcast_id, podcast_name, publisher, overview, total_episodes, market_name
FROM podcasts
INNER JOIN available_markets ON podcasts.podcast_id = available_markets.podcast_id;

#union with set operations
SELECT song_id, song_name, artist_name, album, duration
FROM songs
UNION
SELECT podcast_id AS song_id, podcast_name AS song_name, publisher AS artist_name, NULL AS album, NULL AS duration
FROM podcasts;

#union equivalence without set operations
SELECT COALESCE(s.song_id, p.podcast_id) AS song_id,
       COALESCE(s.song_name, p.podcast_name) AS song_name,
       COALESCE(s.artist_name, p.publisher) AS artist_name,
       s.album,
       s.duration
FROM songs s
LEFT JOIN podcasts p ON 1 = 0;

#difference with set operations
#MySQL does not support EXCEPT
-- SELECT song_id, song_name, artist_name, album, duration
-- FROM songs
-- EXCEPT
-- SELECT podcast_id AS song_id, podcast_name AS song_name, publisher AS artist_name, NULL AS album, NULL AS duration
-- FROM podcasts;

#difference equivalence without using set operations
SELECT s.song_id, s.song_name, s.artist_name, s.album, s.duration
FROM songs s
LEFT JOIN podcasts p ON s.song_id = p.podcast_id
WHERE p.podcast_id IS NULL;

#an example of a view that has a hard-coded criteria, by which the content of the view may change upon changing the hard-coded value
create view db_perfect_length as
(select * from songs where duration = 300);
 
#division operator using a) a regular nested query using NOT IN
#finds songs that an artist contributed with other artists
SELECT DISTINCT b.song_name
FROM songs b
WHERE NOT EXISTS (
    SELECT album
    FROM songs a
    WHERE a.artist_name = 'Coldplay'
      AND a.album NOT IN (
          SELECT album
          FROM songs c
          WHERE c.song_id = b.song_id
      )
);

#division operator using b) a correlated nested query using NOT EXISTS and EXCEPT
#finds songs that an artist contributed with other artists
SELECT DISTINCT b.song_name
FROM songs b
WHERE NOT EXISTS (
    SELECT album
    FROM songs a
    WHERE a.artist_name = 'Coldplay'
      AND NOT EXISTS (
          SELECT album
          FROM songs c
          WHERE c.song_id = b.song_id
            AND c.album = a.album
      )
);

#query that demonstrates the overlap constraints
SELECT p1.podcast_id, p1.total_episodes, p2.podcast_id, p2.total_episodes
FROM podcasts p1
JOIN podcasts p2 ON p1.podcast_id <> p2.podcast_id
WHERE p1.total_episodes > 0 AND p2.total_episodes > 0
AND (p1.total_episodes >= p2.total_episodes AND p1.total_episodes <= p2.total_episodes + p2.total_episodes
    OR p2.total_episodes >= p1.total_episodes AND p2.total_episodes <= p1.total_episodes + p1.total_episodes);
#this is overlap because we are comparing every podcast and their total_episodes to every podcast and their total_episodes 

#query that demonstrates the covering constraints
SELECT m.market_name
FROM available_markets m
WHERE NOT EXISTS (
    SELECT 1
    FROM podcasts p
    WHERE p.publisher = m.market_name
);
