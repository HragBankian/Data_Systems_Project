use sys;

#parent table
CREATE TABLE media_types (
    media_id INT AUTO_INCREMENT PRIMARY KEY,
    media_type VARCHAR(255) NOT NULL #a media can only be of type 'MUSIC_VIDEO_TYPE_ATV' (song) or 'show' (podcast)
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
    CONSTRAINT fk_podcast_id_available_markets 
        FOREIGN KEY (podcast_id) 
        REFERENCES podcasts(podcast_id)
);


#referential integrity using triggers for 'songs' table
DELIMITER //
CREATE TRIGGER songs_before_insert_trigger
BEFORE INSERT ON songs
FOR EACH ROW
BEGIN
    DECLARE media_type_value ENUM('MUSIC_VIDEO_TYPE_ATV', 'show');
    SELECT media_type INTO media_type_value FROM media_types WHERE media_id = NEW.media_type_id;
    
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
    DECLARE media_type_value ENUM('MUSIC_VIDEO_TYPE_ATV', 'show');
    SELECT media_type INTO media_type_value FROM media_types WHERE media_id = NEW.media_type_id;
    
    IF media_type_value IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Invalid media_type_id for podcasts';
    END IF;
END//
DELIMITER ;

#view to display all media items
CREATE VIEW all_media AS
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