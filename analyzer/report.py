import pandas as pd


def _pct(val) -> str:
    try:
        return f"{float(val)*100:.1f}%"
    except (TypeError, ValueError):
        return "—"


def print_summary(df: pd.DataFrame) -> None:
    print("\n" + "=" * 60)
    print("  Cold Outreach Analysis")
    print("=" * 60)

    for campaign, group in df.groupby("campaign_name"):
        print(f"\n  {campaign}")
        print(f"  Total sent: {group['sent'].sum():,}")

        if "sequence_step" in group.columns:
            for _, row in group.sort_values("sequence_step").iterrows():
                print(
                    f"    Step {int(row['sequence_step'])} — "
                    f"Sent: {row['sent']:,}  "
                    f"Open: {_pct(row['open_rate'])}  "
                    f"Reply: {_pct(row['reply_rate'])}"
                )
        else:
            for _, row in group.iterrows():
                print(
                    f"    Open: {_pct(row['open_rate'])}  "
                    f"Reply: {_pct(row['reply_rate'])}  "
                    f"Booking: {_pct(row['booking_rate'])}"
                )

    print("\n" + "=" * 60)
    overall_reply = (df["replied"].sum() / df["sent"].sum())
    overall_booking = (df["meetings_booked"].sum() / df["sent"].sum())
    print(f"  Overall reply rate:   {_pct(overall_reply)}")
    print(f"  Overall booking rate: {_pct(overall_booking)}")
    print(f"  Total emails sent:    {df['sent'].sum():,}")
    print("=" * 60 + "\n")


def print_variant_comparison(variant_df: pd.DataFrame) -> None:
    if variant_df.empty:
        return

    print("\n── Variant Comparison ──────────────────────────────────")
    for campaign, group in variant_df.groupby("campaign_name"):
        print(f"\n  {campaign}")
        winner = group["winning_variant"].iloc[0]
        for _, row in group.iterrows():
            tag = "  ← winner" if row["variant"] == winner and len(group) > 1 else ""
            print(
                f"    [{row['variant']}]  "
                f"Reply: {_pct(row['reply_rate'])}  "
                f"Booking: {_pct(row['booking_rate'])}"
                f"{tag}"
            )
    print()
