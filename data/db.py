import sqlite3

class DB:
    def __init__(self):
        self.db = sqlite3.connect("data.db")
        self.cursor = self.db.cursor()

    def __enter__(self):
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.commit()
        self.db.close()

def create_tables():
    with DB() as cursor:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS reddit_posts (
                id TEXT PRIMARY KEY,
                type, 
                selftext, 
                over_18,
                created_utc,
                title, 
                author,
                rating,
                upvote_ratio,
            )
            """
        )

create_tables()