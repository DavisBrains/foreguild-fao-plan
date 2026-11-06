# FIP-04d, a live test proposal on Seer [Demo]

FIP-04d is a test Foreguild Improvement Proposal. It asks one small question. When the pilot intake opens, which task category should it accept first, CSV cleanup or CI patch?

Foreguild has no revenue yet and nothing here measures revenue. The point of this stage is to show the governance path working end to end on real contracts. The proposal is written as conditional markets on Seer, each market resolves through Reality.eth with Kleros as arbitrator, and this rules file is public and timestamped by its commit before any market opens for answers.

## The markets

All three live on Gnosis and were created through the Seer MarketFactory at `0x83183DA839Ce8228E31Ae41222EaD9EDBb5cDcf1`. Each has a minimum Reality.eth bond of 1 xDAI and the standard 3.5 day answer timeout.

1. The decision market asks which category FIP-04d adopts. Its outcomes are CSV cleanup and CI patch, and it opens for answers on 12 Nov 2026 at 6 pm UTC.
2. Branch A applies if CSV cleanup wins. It asks how many outside accounts request a pilot task, on a scale of 0 to 40, and opens for answers on 20 Nov 2026 at midnight UTC.
3. Branch B asks the same question for CI patch and opens at the same time.

The exact question texts are below, word for word as they appear on chain.

```
[Demo] Which pilot task category will the Foreguild test proposal FIP-04d adopt, according to the decision file demo/fip-04d-decision.json published in github.com/DavisBrains/foreguild-fao-plan on or before 12 Nov 2026 18:00 UTC?

[Demo] If FIP-04d adopts CSV cleanup, how many distinct GitHub accounts other than DavisBrains, created before 1 Nov 2026, will open an issue labelled pilot-task in github.com/DavisBrains/foreguild-fao-plan between 13 Nov 2026 00:00 UTC and 20 Nov 2026 00:00 UTC? [accounts]

[Demo] If FIP-04d adopts CI patch, how many distinct GitHub accounts other than DavisBrains, created before 1 Nov 2026, will open an issue labelled pilot-task in github.com/DavisBrains/foreguild-fao-plan between 13 Nov 2026 00:00 UTC and 20 Nov 2026 00:00 UTC? [accounts]
```

The market addresses and Seer links will be added to this file once the markets exist.

## How the decision is made

Liquidity is a separate and later step. It gets added when a real pilot budget is at stake, so the prices carry information from people with money on the line. Until then the markets hold the question and the resolution path, and a clear default decides.

**The default.** FIP-04d adopts CSV cleanup.

**The price rule.** It switches on only if both UP pools have depth. An UP pool pairs a branch UP token with the parent outcome token for that branch on Swapr, and anyone can create one. Every hour from 11 Nov 2026 at 6 pm UTC to 12 Nov 2026 at 6 pm UTC, a script reads both pools, giving 24 reads per branch. If both pools hold at least 5 parent tokens on each side at every read, the expected count for a branch is 40 times the average UP price, and the branch with the higher count wins. A tie falls back to the default.

**Publishing.** By 12 Nov 2026 at 6 pm UTC the file `demo/fip-04d-decision.json` goes into this repository. It names the adopted category, says whether the price rule was on, and includes every read if it was.

## How each market resolves

**Decision market.** The correct answer is the category named in `demo/fip-04d-decision.json`. If that file is missing at 6 pm UTC on 12 Nov 2026, the correct answer is CSV cleanup.

**The winning branch.** Count distinct GitHub accounts that opened an issue in this repository with the label pilot-task, created from 13 Nov 2026 at midnight UTC up to 20 Nov 2026 at midnight UTC. Leave out the account DavisBrains and any account created on or after 1 Nov 2026. Count each account once. The number can be checked with the GitHub issue search for `label:pilot-task created:2026-11-13..2026-11-19` and each author profile. A count above 40 is reported as 40.

**The other branch.** Its parent outcome lost, so its tokens carry no value whatever answer it gets. It may stay unanswered.

## The intake form

The issue form in `.github/ISSUE_TEMPLATE/pilot-task.yml` adds the pilot-task label. Once the decision file is published, the form keeps only the adopted category.

This proposal is a demonstration. It moves no treasury funds and commits Foreguild to nothing beyond the pilot intake order described here.
