import pandas as pd


def get_dashboard_stats(df):

    total_restaurants = len(df)

    avg_rating = round(
        df["rate"].mean(),
        2
    )

    total_votes = int(
        df["votes"].sum()
    )

    avg_cost = round(
        df["cost"].mean(),
        2
    )

    top_restaurant = (

        df.sort_values(
            by="rate",
            ascending=False
        )

        ["name"]

        .iloc[0]
    )

    return {

        "total_restaurants":
        total_restaurants,

        "avg_rating":
        avg_rating,

        "total_votes":
        total_votes,

        "avg_cost":
        avg_cost,

        "top_restaurant":
        top_restaurant
    }