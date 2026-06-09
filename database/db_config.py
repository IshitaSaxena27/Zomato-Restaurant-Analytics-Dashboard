from sqlalchemy import create_engine

DB_USER = "root"
DB_PASSWORD = "RachanaIshita1234#"
DB_HOST = "localhost"
DB_NAME = "zomato_db"

DATABASE_URL = (
    f"mysql+pymysql://"
    f"{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}/{DB_NAME}"
)

engine = create_engine(
    DATABASE_URL,
    echo=False
)