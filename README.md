<div align="center">

# Cold Outreach Analyzer

**Parse campaign exports. Surface what's working. Kill what isn't.**

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)

</div>

---

## What it does

Takes CSV exports from Instantly (or any sequencer with similar output) and gives you a clear picture of what's happening across your campaigns — open rates, reply rates, booking rates, step-level drop-off, and A/B variant winners. Also flags campaigns that fall below a benchmark you set.

---

## Table of Contents

- [Quickstart](#quickstart)
- [Metrics Computed](#metrics-computed)
- [Input Format](#input-format)
- [Sample Output](#sample-output)
- [Variant Comparison](#variant-comparison)
- [Benchmark Flagging](#benchmark-flagging)
- [CLI Reference](#cli-reference)
- [Project Structure](#project-structure)
- [Contributing](#contributing)

---

## Quickstart

```bash
git clone https://github.com/MVP-03/cold-outreach-analyzer.git
cd cold-outreach-analyzer
pip install -r requirements.txt

# Basic analysis
python analyze.py --input data/sample_campaign_export.csv

# With variant comparison and benchmark flagging
python analyze.py --input data/sample_campaign_export.csv --compare-variants --benchmark-reply 0.05
```

---

## Metrics Computed

| Metric | Formula | Signal |
|---|---|---|
| Open Rate | Opened / Sent | Deliverability + subject line |
| Reply Rate | Replied / Sent | Message resonance |
| Positive Reply Rate | Positive / Replied | Tone and targeting |
| Booking Rate | Meetings / Sent | Actual pipeline created |

---

## Input Format

Export your campaign from Instantly as a CSV. Expected columns:

```csv
campaign_name,sequence_step,variant,sent,opened,replied,positive_replies,meetings_booked,send_date
Q2 Series B Outbound,1,A,400,176,37,14,4,2026-06-09
Q2 Series B Outbound,2,A,364,113,15,5,2,2026-06-11
Q2 Series B Outbound,1,B,400,168,41,18,7,2026-06-09
```

`sequence_step`, `variant`, `positive_replies`, and `send_date` are optional but unlock additional analysis when present.

---

## Sample Output

```
════════════════════════════════════════════════════════════
  Cold Outreach Analysis
════════════════════════════════════════════════════════════

  Q2 Series B Outbound
  Total sent: 1,913
    Step 1 — Sent: 800   Open: 43.0%  Reply: 9.8%
    Step 2 — Sent: 723   Open: 29.7%  Reply: 4.4%
    Step 3 — Sent: 390   Open: 17.2%  Reply: 1.8%

  Founder Cold - DevTools
  Total sent: 472
    Step 1 — Sent: 250   Open: 48.8%  Reply: 11.2%
    Step 2 — Sent: 222   Open: 33.3%  Reply: 4.1%

════════════════════════════════════════════════════════════
  Overall reply rate:    7.1%
  Overall booking rate:  1.0%
  Total emails sent:     2,385
════════════════════════════════════════════════════════════
```

---

## Variant Comparison

When your export includes a `variant` column, the analyzer compares A/B variants within each campaign and flags the winner by booking rate:

```
── Variant Comparison ──────────────────────────────────────

  Q2 Series B Outbound
    [A]  Reply: 6.8%  Booking: 0.8%
    [B]  Reply: 7.9%  Booking: 1.1%  ← winner
```

---

## Benchmark Flagging

Set a minimum reply rate. Any campaign averaging below that threshold gets flagged:

```bash
python analyze.py --input campaigns.csv --benchmark-reply 0.05
```

```
Campaigns below 5% reply rate benchmark:
  - Reactivation - Churned (4.4%)
```

---

## CLI Reference

```bash
# Basic summary
python analyze.py --input campaigns.csv

# Add variant comparison
python analyze.py --input campaigns.csv --compare-variants

# Flag campaigns below 5% reply rate
python analyze.py --input campaigns.csv --benchmark-reply 0.05

# Save enriched data with computed metrics
python analyze.py --input campaigns.csv --output enriched.csv

# All flags together
python analyze.py --input campaigns.csv --compare-variants --benchmark-reply 0.05 --output enriched.csv
```

---

## Project Structure

```
cold-outreach-analyzer/
├── analyze.py              # Entry point and argument parsing
├── analyzer/
│   ├── parser.py           # CSV loader and column validation
│   ├── metrics.py          # Metric computation, benchmarking, variant comparison
│   └── report.py           # Formatted terminal output
├── data/
│   └── sample_campaign_export.csv
└── requirements.txt
```

---

## Contributing

Good next additions:

- Day-of-week reply rate analysis
- Trend view across multiple exports over time
- HTML report export for sharing with stakeholders

---

## License

MIT

