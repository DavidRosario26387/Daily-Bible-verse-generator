import psycopg2
from datetime import date

schema = """
CREATE TABLE IF NOT EXISTS daily_verses (
    id SERIAL PRIMARY KEY,
    day DATE UNIQUE NOT NULL,
    reference TEXT NOT NULL,
    verse TEXT NOT NULL,
    prompt_general TEXT,
    prompt_bible TEXT,
    img1 BYTEA,
    img2 BYTEA,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT,
    error_message TEXT
);
"""
success_query = """
INSERT INTO daily_verses
(day, reference, verse, prompt_general, prompt_bible, img1, img2, status)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s);
"""

error_query = """
INSERT INTO daily_verses
(day, reference, verse, status, error_message)
VALUES (%s,%s,%s,%s,%s);
"""

def insert_success(conn, reference, verse, prompt1, prompt2, img1, img2):

    with conn.cursor() as cur:
        cur.execute(
            success_query,
            (
                date.today(),
                reference,
                verse,
                prompt1,
                prompt2,
                psycopg2.Binary(img1),
                psycopg2.Binary(img2),
                "success"
            )
        )

    conn.commit()


def insert_error(conn, reference, verse, error):

    with conn.cursor() as cur:
        cur.execute(
            error_query,
            (
                date.today(),
                reference,
                verse,
                "failed",
                str(error)
            )
        )

    conn.commit()