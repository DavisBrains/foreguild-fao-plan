# FIP-04d, a live test proposal on Seer [Demo]

FIP-04d is a test Foreguild Improvement Proposal. It asks one small question. When the pilot intake opens, which task category should it accept first, CSV cleanup or CI patch?

Foreguild has no revenue yet and nothing here measures revenue. The point of this stage is to show the governance path working end to end on real contracts. The proposal is written as conditional markets on Seer, each market resolves through Reality.eth with Kleros as arbitrator, and this rules file is public and timestamped by its commit before any market opens for answers.

## The markets

All three live on Gnosis. They were created through the Seer MarketFactory at `0x83183DA839Ce8228E31Ae41222EaD9EDBb5cDcf1`. Each has a minimum Reality.eth bond of 1 xDAI and the standard 3.5 day answer timeout.

1. The decision market asks which category FIP-04d adopts. Its outcomes are CSV cleanup and CI patch, and it opens for answers on 12 Nov 2026 at 6 pm UTC.
2. Branch A applies if CSV cleanup wins. It asks how many outside accounts request a pilot task, on a scale of 0 to 40, and opens for answers on 20 Nov 2026 at midnight UTC.
3. Branch B asks the same question for CI patch and opens at the same time.

The exact question texts are below, word for word as they appear on chain.

```
[Demo] Which pilot task category will the Foreguild test proposal FIP-04d adopt, according to the decision file demo/fip-04d-decision.json published in github.com/DavisBrains/foreguild-fao-plan on or before 12 Nov 2026 18:00 UTC?

[Demo] If FIP-04d adopts CSV cleanup, how many distinct GitHub accounts other than DavisBrains, created before 1 Nov 2026, will open an issue labelled pilot-task in github.com/DavisBrains/foreguild-fao-plan between 13 Nov 2026 00:00 UTC and 20 Nov 2026 00:00 UTC? [accounts]

[Demo] If FIP-04d adopts CI patch, how many distinct GitHub accounts other than DavisBrains, created before 1 Nov 2026, will open an issue labelled pilot-task in github.com/DavisBrains/foreguild-fao-plan between 13 Nov 2026 00:00 UTC and 20 Nov 2026 00:00 UTC? [accounts]
```

## Live addresses

The three markets went live on Gnosis on 6 Nov 2026, about ten minutes after this file was first committed. All three were sent from 0x5De2bE433465d02304d43AF8F10b792b068d219B to the MarketFactory, and each receipt has status 1.

| Market | Address | Creation tx | Reality.eth question |
|---|---|---|---|
| Decision | [0xd1ccddfb0684a93f9bbb9a7dda0918a62ba3e4c7](https://app.seer.pm/markets/100/0xd1ccddfb0684a93f9bbb9a7dda0918a62ba3e4c7) | [0x9b7aa347…](https://gnosisscan.io/tx/0x9b7aa347fdedb1b18dd0446422f5880a8ad3b49c639e282f90100ea994544631) | `0x2112dd6cc57417e66f02f439861de7b8c83dd8e7c831e4009206b0bf4b1e921d` |
| Branch A, CSV cleanup | [0x1f93d14169a966f624e2f86162a1a5dfcffdb8d8](https://app.seer.pm/markets/100/0x1f93d14169a966f624e2f86162a1a5dfcffdb8d8) | [0x06d42842…](https://gnosisscan.io/tx/0x06d42842a6ef8bc19f67c6c9dad4d2900eff2351b1b90100c5aed7c60d6acaee) | `0xcaacdf394526a5c40ad09cd2da7852ff7df1e568113c894a06a231b0db312073` |
| Branch B, CI patch | [0x9d713f713de42887cf0a32a80e228711b299902f](https://app.seer.pm/markets/100/0x9d713f713de42887cf0a32a80e228711b299902f) | [0x7d10909e…](https://gnosisscan.io/tx/0x7d10909ee9a252a22c89c109b5bdee6d82c1f9cd4a3254da8f159ccbcb6dfff9) | `0x95a2903aca56a1b276c287a9e9c76ee2b49113c3760cb34abc4b7bb21cbeb91e` |

Read back on chain, branch A points to the decision market with parent outcome 0 and branch B with parent outcome 1. Both branches run from 0 to 40. The decision market opens for answers at Unix time 1794506400 and the branches at 1795132800. Every question has a minimum bond of 1 xDAI, a timeout of 302400 seconds, and the Kleros arbitrator at 0x68154EA682f95BF582b80Dd6453FA401737491Dc. Screenshots of the Seer pages are in `assets/fip-04d/`.

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
