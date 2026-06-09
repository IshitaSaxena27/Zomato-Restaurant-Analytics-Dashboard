import pandas as pd
from sqlalchemy import text
from database.db_config import engine

# ==========================
# LOAD CSV
# ==========================

df = pd.read_csv(
    "dataset/zomato.csv"
)

# ==========================
# CLEAN RATINGS
# ==========================

def handle_rate(value):

    value = str(value)

    if '/' in value:
        value = value.split('/')[0]

    try:
        return float(value)

    except:
        return 0


df["rate"] = df["rate"].apply(
    handle_rate
)

# ==========================
# CLEAN COST COLUMN
# ==========================

df["approx_cost(for two people)"] = (

    df["approx_cost(for two people)"]

    .astype(str)

    .str.replace(",", "")

)

# ==========================
# INSERT DATA
# ==========================

insert_query = """
INSERT INTO restaurants
(
name,
online_order,
book_table,
rate,
votes,
cost,
restaurant_type
)

VALUES

(
:name,
:online_order,
:book_table,
:rate,
:votes,
:cost,
:restaurant_type
)
"""

with engine.begin() as conn:

    for _, row in df.iterrows():

        conn.execute(
            text(insert_query),
            {

                "name":
                row["name"],

                "online_order":
                row["online_order"],

                "book_table":
                row["book_table"],

                "rate":
                row["rate"],

                "votes":
                int(row["votes"]),

                "cost":
                int(float(
                    row[
                        "approx_cost(for two people)"
                    ]
                )),

                "restaurant_type":
                row[
                    "listed_in(type)"
                ]
            }
        )

print(
    f"{len(df)} records imported successfully."
)