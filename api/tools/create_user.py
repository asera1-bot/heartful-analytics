import getpass
from sqlalchemy import text
from passlib.context import CryptContext
from db_config import get_engine
from app.models.base import Base
from app.core.db import engine

Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def main():
    username = input("username: ").strip()
    password = getpass.getpass("password: ").strip()
    password_hash = pwd_context.hash(password)

    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO users (username, password_hash)
                VALUES (:u, :p)
            """),
            {"u": username, "p": password_hash},
        )

    print("OK: user created")

if __name__ == "__main__":
    main()
