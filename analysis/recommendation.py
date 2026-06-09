import pandas as pd


# ==========================
# CALCULATE AI SCORE
# ==========================

def calculate_score(df):

    df = df.copy()

    df["rate"] = pd.to_numeric(
        df["rate"],
        errors="coerce"
    )

    df["votes"] = pd.to_numeric(
        df["votes"],
        errors="coerce"
    )

    df["cost"] = pd.to_numeric(
        df["cost"],
        errors="coerce"
    )

    df = df.dropna(
        subset=[
            "rate",
            "votes",
            "cost"
        ]
    )

    max_votes = max(
        df["votes"].max(),
        1
    )

    df["recommendation_score"] = (

        (df["rate"] * 0.50)

        +

        ((df["votes"] / max_votes) * 3.0)

        +

        (
            df["online_order"]
            .map({
                "Yes": 1,
                "No": 0
            })
            .fillna(0)
            * 0.5
        )
    )

    return df


# ==========================
# TOP RESTAURANTS
# ==========================

def top_restaurants(df):

    df = calculate_score(df)

    return (
        df.sort_values(
            by="recommendation_score",
            ascending=False
        )
        .head(20)
    )


# ==========================
# AI RECOMMENDATION
# ==========================

def recommend_restaurants(
    df,
    budget,
    restaurant_type
):

    df = calculate_score(df)

    filtered = df[

        (df["cost"] <= budget)

    ]

    if restaurant_type:

        filtered = filtered[

            filtered[
                "restaurant_type"
            ]
            .astype(str)
            .str.contains(
                restaurant_type,
                case=False,
                na=False
            )
        ]

    recommendations = (

        filtered.sort_values(
            by="recommendation_score",
            ascending=False
        )

    )

    return recommendations.head(12)


# ==========================
# BEST VALUE
# ==========================

def best_value_restaurants(df):

    df = df.copy()

    df["rate"] = pd.to_numeric(
        df["rate"],
        errors="coerce"
    )

    df["cost"] = pd.to_numeric(
        df["cost"],
        errors="coerce"
    )

    df = df.dropna()

    df["value_score"] = (

        df["rate"]

        /

        (df["cost"] + 1)

    )

    return (

        df.sort_values(
            by="value_score",
            ascending=False
        )

        .head(10)

    )