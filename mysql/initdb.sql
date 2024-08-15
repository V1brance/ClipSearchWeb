USE ClipCache;

CREATE TABLE Broadcasters (
    broadcaster_id      BIGINT          PRIMARY KEY NOT NULL,
    broadcaster_name    VARCHAR(128)    NOT NULL,
    last_cached         DATETIME        NOT NULL DEFAULT "1970-01-01 00:00:00"
);

CREATE TABLE Games (
    game_id             BIGINT          PRIMARY KEY NOT NULL,
    game_name           VARCHAR(128)    NOT NULL,
    FULLTEXT(game_name)
);

CREATE TABLE Clips (
    clip_id             VARCHAR(512)    PRIMARY KEY NOT NULL,
    broadcaster_id      BIGINT          NOT NULL,
    clip_date           DATETIME        NOT NULL,
    clip_url            VARCHAR(512)    NOT NULL,
    creator_id          BIGINT          NOT NULL,
    creator_name        VARCHAR(128)    NOT NULL,
    game_id             BIGINT          NOT NULL,
    title               VARCHAR(256)    NOT NULL,
    view_count          INT             NOT NULL,
    thumbnail_url       VARCHAR(512)    NOT NULL,
    duration            INT             NOT NULL,
    CONSTRAINT fk_broadcaster
        FOREIGN KEY (broadcaster_id) REFERENCES Broadcasters(broadcaster_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_game
        FOREIGN KEY (game_id) REFERENCES Games(game_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FULLTEXT(title, creator_name)
);

INSERT INTO Games VALUES (0, "NULL");