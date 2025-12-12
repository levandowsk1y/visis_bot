import json
import psycopg2
import os

conn = psycopg2.connect(
    host=os.getenv("DB_HOST", "localhost"),
    database="visisdb",
    user="zikres",
    password="123"
)
cursor = conn.cursor()

with open("data/videos.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for video in data["videos"]:
    cursor.execute("""
        INSERT INTO videos (
            id, creator_id, video_created_at,
            views_count, likes_count, comments_count, reports_count,
            created_at
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET
            views_count = EXCLUDED.views_count,
            likes_count = EXCLUDED.likes_count,
            comments_count = EXCLUDED.comments_count,
            reports_count = EXCLUDED.reports_count,
            updated_at = NOW();
    """, (
        video["id"],
        video["creator_id"],
        video["video_created_at"],
        video["views_count"],
        video["likes_count"],
        video["comments_count"],
        video["reports_count"],
        video["created_at"]
    ))

for video in data["videos"]:
    for snap in video.get("snapshots", []):
        cursor.execute("""
            INSERT INTO video_snapshots (
                video_id,
                views_count, likes_count, comments_count, reports_count,
                delta_views_count, delta_likes_count, delta_comments_count, delta_reports_count,
                created_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, (
            video["id"],
            snap["views_count"],
            snap["likes_count"],
            snap["comments_count"],
            snap["reports_count"],
            snap["delta_views_count"],
            snap["delta_likes_count"],
            snap["delta_comments_count"],
            snap["delta_reports_count"],
            snap["created_at"]
        ))
conn.commit()
conn.close()
print("✅ Данные из videos.json успешно загружены в PostgreSQL")