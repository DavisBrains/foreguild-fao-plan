# Foreguild local demo (T0 harness + FIP→mandate)

No chain. No wallet. Python 3 stdlib only.

## What it shows
1. A sample task with three acceptance tests (file exists, no blank `amount`, min rows).
2. A **bad** agent submission that leaves a blank → T0 **REJECT**.
3. A **good** submission that fills blanks with `0.00` → T0 **ACCEPT**.
4. A passed FIP (`FIP-03`) compiled into an active mandate (categories, spend caps, take bps).
5. Mandate enforcement: in-category job allowed; marketing-copy blocked; over-cap spend blocked.

## Run
```bash
cd demo
python3 run_demo.py
```

## Captured output
See `captured-output.txt` (recaptured from the commands above).

## Files
- `run_demo.py` — harness + mandate compiler/enforcer
- `sample_task/task.json` — task + tests
- `fixtures/good|bad/out/costs_clean.csv` — submissions
- `mandates/fip-03-passed.json` — passed FIP input
- `mandates/active_mandate.json` — written on each run
