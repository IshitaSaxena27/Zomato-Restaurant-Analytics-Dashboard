import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "mysql+pymysql://root:RachanaIshita1234#@localhost/zomato_db"
)

df = pd.read_csv(
    "dataset/zomato_cleaned.csv"
)

print("Rows Found:", len(df))

df.to_sql(
    "restaurants",
    engine,
    if_exists="append",
    index=False,
    chunksize=5000
)

print("Import Completed")