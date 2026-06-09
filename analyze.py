import argparse
from analyzer.parser import parse
from analyzer.metrics import compute, flag_underperformers, compare_variants
from analyzer.report import print_summary, print_variant_comparison


def main():
    parser = argparse.ArgumentParser(description="Analyze cold outreach campaign exports.")
    parser.add_argument("--input", required=True, help="Path to campaign export CSV")
    parser.add_argument("--compare-variants", action="store_true", help="Compare A/B variants within campaigns")
    parser.add_argument("--benchmark-reply", type=float, default=None, help="Flag campaigns below this reply rate (e.g. 0.05)")
    parser.add_argument("--output", default=None, help="Save enriched data to CSV")
    args = parser.parse_args()

    df = parse(args.input)
    df = compute(df)

    print_summary(df)

    if args.compare_variants:
        variants = compare_variants(df)
        print_variant_comparison(variants)

    if args.benchmark_reply:
        under = flag_underperformers(df, args.benchmark_reply)
        if not under.empty:
            print(f"\nCampaigns below {args.benchmark_reply*100:.0f}% reply rate benchmark:")
            for _, row in under.iterrows():
                print(f"  - {row['campaign_name']} ({row['avg_reply_rate']*100:.1f}%)")
        else:
            print(f"\nAll campaigns above {args.benchmark_reply*100:.0f}% reply rate benchmark.")

    if args.output:
        df.to_csv(args.output, index=False)
        print(f"\nSaved to {args.output}")


if __name__ == "__main__":
    main()
