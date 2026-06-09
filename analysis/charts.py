import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")


def restaurant_type_chart(df):

    top_types = (
        df["restaurant_type"]
        .value_counts()
        .head(10)
    )

    plt.figure(figsize=(10, 6))

    sns.barplot(
        x=top_types.values,
        y=top_types.index
    )

    plt.title("Top 10 Restaurant Categories")

    plt.tight_layout()

    plt.savefig(
        "static/charts/type_chart.png"
    )

    plt.close()


def rating_distribution(df):

    plt.figure(figsize=(10, 6))

    plt.hist(
        df["rate"],
        bins=20
    )

    plt.title("Rating Distribution")

    plt.xlabel("Rating")
    plt.ylabel("Restaurants")

    plt.tight_layout()

    plt.savefig(
        "static/charts/rating_chart.png"
    )

    plt.close()


def cost_vs_rating(df):

    sample_df = df.sample(
        min(3000, len(df))
    )

    plt.figure(figsize=(10, 6))

    sns.scatterplot(
        x="cost",
        y="rate",
        data=sample_df,
        alpha=0.5
    )

    plt.title("Cost vs Rating")

    plt.tight_layout()

    plt.savefig(
        "static/charts/cost_rating_chart.png"
    )

    plt.close()


def online_order_analysis(df):

    top_df = (
        df.groupby("online_order")["rate"]
        .mean()
        .reset_index()
    )

    plt.figure(figsize=(8, 6))

    sns.barplot(
        x="online_order",
        y="rate",
        data=top_df
    )

    plt.title(
        "Online Order vs Average Rating"
    )

    plt.tight_layout()

    plt.savefig(
        "static/charts/online_order_chart.png"
    )

    plt.close()


def generate_charts(df):

    restaurant_type_chart(df)

    rating_distribution(df)

    cost_vs_rating(df)

    online_order_analysis(df)