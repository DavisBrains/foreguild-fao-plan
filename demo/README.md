# Foreguild local demo (T0 harness and FIP to mandate)

No chain. No wallet. Python 3 stdlib only.

## What it shows

1. A sample task with three acceptance tests. The output file must exist, the `amount` column can have no blanks, and there must be at least three rows.
2. A **bad** agent submission that leaves a blank gets a T0 **REJECT**.
3. A **good** submission that fills blanks with `0.00` gets a T0 **ACCEPT**.
4. A passed FIP (`FIP-03`) is compiled into an active mandate with allowed categories, spend caps and take in basis points.
5. The mandate is enforced. An in category job is allowed, a marketing copy job is blocked, and a job over the daily spend cap is blocked.

## Run

```bash
cd demo
python3 run_demo.py
```

## Captured output

The file `captured-output.txt` holds a fresh capture from the commands above.

## Files

`run_demo.py` is the harness plus the mandate compiler and enforcer. `sample_task/task.json` holds the task and its tests. The two submissions live in `fixtures/good/out/costs_clean.csv` and `fixtures/bad/out/costs_clean.csv`. The passed FIP input is `mandates/fip-03-passed.json`, and each run writes `mandates/active_mandate.json`.
