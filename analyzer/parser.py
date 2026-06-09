import pandas as pd


REQUIRED = {"campaign_name", "sent", "opened", "replied", "meetings_booked"}


def parse(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    if "send_date" in df.columns:
        df["send_date"] = pd.to_datetime(df["send_date"], errors="coerce")

    for col in ["sent", "opened", "replied", "meetings_booked"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

    if "positive_replies" in df.columns:
        df["positive_replies"] = pd.to_numeric(df["positive_replies"], errors="coerce").fillna(0).astype(int)

    df = df[df["sent"] > 0].reset_index(drop=True)
    return df
