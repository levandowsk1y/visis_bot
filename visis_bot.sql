CREATE TABLE json_raw (
    data JSONB
);


INSERT INTO json_raw (data)
SELECT pg_read_file('C:\Users\Никита\Desktop\videos.json')::jsonb;


CREATE TABLE videos (
    id TEXT PRIMARY KEY,
    creator_id TEXT NOT NULL,
    video_created_at TIMESTAMP WITH TIME ZONE,
    views_count BIGINT DEFAULT 0,
    likes_count BIGINT DEFAULT 0,
    comments_count BIGINT DEFAULT 0,
    reports_count BIGINT DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE video_snapshots (
    id TEXT PRIMARY KEY,
    video_id TEXT REFERENCES videos(id) ON DELETE CASCADE,
    views_count BIGINT DEFAULT 0,
    likes_count BIGINT DEFAULT 0,
    comments_count BIGINT DEFAULT 0,
    reports_count BIGINT DEFAULT 0,
    delta_views_count BIGINT DEFAULT 0,
    delta_likes_count BIGINT DEFAULT 0,
    delta_comments_count BIGINT DEFAULT 0,
    delta_reports_count BIGINT DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
);

INSERT INTO videos (
    id,
    creator_id,
    video_created_at,
    views_count,
    likes_count,
    comments_count,
    reports_count,
    created_at,
    updated_at
)
SELECT
    v.value->>'id' AS id,
    v.value->>'creator_id' AS creator_id,
    (v.value->>'video_created_at')::TIMESTAMP WITH TIME ZONE AS video_created_at,
    (v.value->>'views_count')::BIGINT AS views_count,
    (v.value->>'likes_count')::BIGINT AS likes_count,
    (v.value->>'comments_count')::BIGINT AS comments_count,
    (v.value->>'reports_count')::BIGINT AS reports_count,
    (v.value->>'created_at')::TIMESTAMP WITH TIME ZONE AS created_at,
    (v.value->>'updated_at')::TIMESTAMP WITH TIME ZONE AS updated_at
FROM
    json_raw,
    JSONB_ARRAY_ELEMENTS(data->'videos') AS v;

INSERT INTO video_snapshots (
    id,
    video_id,
    views_count,
    likes_count,
    comments_count,
    reports_count,
    delta_views_count,
    delta_likes_count,
    delta_comments_count,
    delta_reports_count,
    created_at,
    updated_at
)
SELECT
    s.value->>'id' AS id,
    v.value->>'id' AS video_id,
    (s.value->>'views_count')::BIGINT,
    (s.value->>'likes_count')::BIGINT,
    (s.value->>'comments_count')::BIGINT,
    (s.value->>'reports_count')::BIGINT,
    (s.value->>'delta_views_count')::BIGINT,
    (s.value->>'delta_likes_count')::BIGINT,
    (s.value->>'delta_comments_count')::BIGINT,
    (s.value->>'delta_reports_count')::BIGINT,
    (s.value->>'created_at')::TIMESTAMP WITH TIME ZONE,
    (s.value->>'updated_at')::TIMESTAMP WITH TIME ZONE
FROM
    json_raw,
    JSONB_ARRAY_ELEMENTS(data->'videos') AS v,
    JSONB_ARRAY_ELEMENTS(v.value->'snapshots') AS s;
проверка

-- Сколько видео загружено?
SELECT COUNT(*) FROM videos;

-- Сколько снапшотов?
SELECT COUNT(*) FROM video_snapshots;

-- Пример видео и его снапшоты
SELECT id, views_count, likes_count FROM videos LIMIT 1;

SELECT video_id, created_at, views_count, delta_views_count
FROM video_snapshots
LIMIT 5;