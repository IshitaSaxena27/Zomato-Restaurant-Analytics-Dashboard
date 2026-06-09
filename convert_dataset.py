import pandas as pd

df = pd.read_csv("dataset/zomato_restaurants_in_India.csv")

new_df = pd.DataFrame()

new_df["name"] = df["name"]

new_df["online_order"] = df["delivery"].apply(
    lambda x: "Yes" if x == 1 else "No"
)

new_df["book_table"] = "No"

new_df["rate"] = df["aggregate_rating"]

new_df["votes"] = df["votes"]

new_df["cost"] = df["average_cost_for_two"]

new_df["restaurant_type"] = df["cuisines"]

# Remove bad records
new_df = new_df[
    (new_df["rate"] > 0)
]

new_df = new_df.dropna()

new_df.to_csv(
    "dataset/zomato_cleaned.csv",
    index=False
)

print("Rows:", len(new_df))
print(new_df.head())