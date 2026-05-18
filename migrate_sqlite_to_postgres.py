from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Log  # ✅ correct model

# SQLite (source)
SQLITE_URL = "sqlite:///./data/diary.db"

# PostgreSQL (destination)
POSTGRES_URL = "REMOVED_SECRET"

# Engines
sqlite_engine = create_engine(SQLITE_URL)
postgres_engine = create_engine(POSTGRES_URL)

# Sessions
SQLiteSession = sessionmaker(bind=sqlite_engine)
PostgresSession = sessionmaker(bind=postgres_engine)

sqlite_db = SQLiteSession()
postgres_db = PostgresSession()

# Fetch all data from SQLite
logs = sqlite_db.query(Log).all()

print(f"Found {len(logs)} records")

# (Optional but recommended) clear Postgres before inserting
postgres_db.query(Log).delete()
postgres_db.commit()

# Insert into Postgres
for log in logs:
    new_log = Log(
        food=log.food,
        calories=log.calories,
        protein=log.protein,
        fiber=log.fiber,
        date=log.date
    )
    postgres_db.add(new_log)

postgres_db.commit()

print("Migration complete ✅")

sqlite_db.close()
postgres_db.close()