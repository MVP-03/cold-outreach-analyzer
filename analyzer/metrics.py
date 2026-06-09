import pandas as pd


def compute(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["open_rate"] = (df["opened"] / df["sent"]).round(4)
    df["reply_rate"] = (df["replied"] / df["sent"]).round(4)
    df["booking_rate"] = (df["meetings_booked"] / df["sent"]).round(4)

    if "positive_replies" in df.columns:
        safe_replied = df["replied"].replace(0, 1)
        df["positive_reply_rate"] = (df["positive_replies"] / safe_replied).round(4)

    return df


def flag_underperformers(df: pd.DataFrame, benchmark_reply: float) -> pd.DataFrame:
    agg = df.groupby("campaign_name").agg(
        total_sent=("sent", "sum"),
        avg_reply_rate=("reply_rate", "mean"),
    ).reset_index()
    agg["underperforming"] = agg["avg_reply_rate"] < benchmark_reply
    return agg[agg["underperforming"]]


def compare_variants(df: pd.DataFrame) -> pd.DataFrame:
    if "variant" not in df.columns:
        return pd.DataFrame()

    agg = df.groupby(["campaign_name", "variant"]).agg(
        sent=("sent", "sum"),
        replied=("replied", "sum"),
        meetings_booked=("meetings_booked", "sum"),
    ).reset_index()

    agg["reply_rate"] = (agg["replied"] / agg["sent"]).round(4)
    agg["booking_rate"] = (agg["meetings_booked"] / agg["sent"]).round(4)

    winners = (
        agg.sort_values("booking_rate", ascending=False)
        .groupby("campaign_name")
        .first()
        .rename(columns={"variant": "winning_variant"})
        [["winning_variant"]]
        .reset_index()
    )

    return agg.merge(winners, on="campaign_name")

