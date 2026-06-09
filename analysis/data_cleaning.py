import pandas as pd


def clean_data(df):

    def handle_rate(value):

        value = str(value)

        value = value.split('/')[0]

        try:
            return float(value)

        except:
            return 0

    df["rate"] = (
        df["rate"]
        .apply(handle_rate)
    )

    return df