# Challenge Task – Monthly Price Output & Trading Optimization

## Overview
This repository contains two independent solutions based on the provided case study:

- reconstruct_output: Reconstruction of monthly OUTPUT table from historical share price data.
- trading_strategy: Maximum wealth calculation using at most 3 trades under a simplified trading model.

The goal is reproducibility and clarity rather than production-grade generalization.

---

## Input Data

Expected Excel structure:

Sheet: SHARE_PRICE_HIST
- COMPANY
- CURRENCY
- SHARE_PRICE
- S_FROM

Sheet: SHARE_PRICE
- COMPANY
- CURRENCY
- SHARE_PRICE
- S_FROM

Default input file name used in scripts:
ChallengeTask_data.xlsx

---

## How to Run

reconstruct_output:
python "reconstruct_output.py"

Output:
OUTPUT.xlsx

trading_strategy:
python "trading_strategy_dp.py"

Console output:
- Max wealth
- Max profit

---

## Solution Logic

### reconstruct_output.py (Monthly OUTPUT Reconstruction)
For each month boundary:
- Take price at start of month T
- Take price at start of month T+1
- If price difference ≠ 0 → write record into OUTPUT

Records are generated only when a full month price change exists.

---

### trading_strategy (Trading Optimization)
Dynamic programming solution computing maximum achievable wealth using:
- Initial capital = 1
- Maximum = 3 trades (buy + sell pairs)
- Chronological trade ordering

Note: The implementation assumes standard time-ordered trading, not literal unrestricted time travel.

---

## Assumptions

- Input data are internally consistent.
- Price timestamps represent valid effective-from dates.
- Missing months imply no valid OUTPUT record.
- Dataset used here contains a single company and currency.

---

## Known Limitations / TODO

Deduplication:
Currently deduplicates by pairs of timestamp and company name only.

Multi-Entity Support:
Scripts are not fully generalized for multiple companies or currencies in one run.
For multi-currency datasets it should choose one and convert, or group by currencies and deduplicate by triple of timestamp, company name and currency.

Current point-in-time price selection uses the latest row with `S_FROM <= T` (ignores `S_TO` / `TS_TO`). This is only safe if intervals are gap-free and non-overlapping. Future: select rows by validity window (`S_FROM <= T < S_TO`, optionally `TS_FROM <= ts < TS_TO`) and add gap/overlap validation.

Input Configurability:
Input filename is currently hardcoded.

---

## Dependencies

Typical environment:
pandas
openpyxl

---

## Reproducibility

Run scripts in directory containing the input Excel file.
