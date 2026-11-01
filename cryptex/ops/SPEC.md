# CRYPTEX · SPEC.md — Evidence-only reconstruction / parity process

Adapted from the user-supplied "GPT SOL 6.1 — REA rebuilder + verifier" image. This project is **not** a reconstruction of third-party proprietary software and does **not** use an unverified REA tool. The useful engineering rule is **confirmed observations first, then small changes, then independent checks**.

## Ownership and safety

**Authoritative owner:** GitHub `cryptex-paper-trading-preview` is the sole paper-ledger writer until an actual on-host DigitalOcean handover has been proven, independently verified, fenced and approved. No new VPS or costs. `612199466` is the protected CSGORisky relay and must never be accessed or modified by this work.

**Scope:** Read-only verification; no orders, key material, host commands, strategy changes, backfilling, ledger resets, or inferred future fills. Account balances are simulated. A GitHub workflow success cannot establish server process status or strategy profitability.

## The confirmed-only workflow

1. **Evidence map.** Read unchanged GitHub reports from `cryptex-paper-trading-preview`, `cryptex-wide-market-research` and the main-branch writer authority. Record their paths and their real timestamps. Missing fields remain UNKNOWN.
2. **Clean-room specification.** Describe the expected behaviour and unambiguous tests in this SPEC. Do not infer secret functionality from a screenshot, historical outcomes, or unavailable server logs.
3. **Small verified changes.** Make isolated improvements, preferably in the separate evidence collector or verifier, without modifying live paper accounts.
4. **Challenge report.** Run unit tests with deliberately corrupted inputs, including a real-order flag, a false 99% coverage assertion, 20/21 accounts, a mismatched virtual balance, stale timestamps, forged profits and wrong writer/host IDs.
5. **Parity matrix.** Create `PARITY_MATRIX.md` with the expected condition, actual measured observation, explicit source reference and one of CONFIRMED, NOT_MET or UNKNOWN. This matrix **does not become complete merely because CI passes**.
6. **Delivery.** Publish `SPEC.md` (this file), `TEST_REPORT.md`, `PARITY_MATRIX.md`, `RUN.md` and `verification.json` in a downloadable GitHub Actions artifact. The result must say what still fails and exactly how it was tested.

## What is required for actual completion

| ID | Required test | Evidence |
|---|---|---|
| paper_only | All reports PAPER_ONLY and zero real orders | All input reports |
| accounts | 21 paper accounts, initial $210, each reconciliation check true | Integrity report |
| ledger | Exact same publication time, candle and paper equity | State + continuity + portfolio + integrity |
| owner | Approved owner GitHub until proven handover, separate protected CSGORisky host | Writer-authority policy (not live process proof) |
| recent | State less than 15 minutes old | Paper state |
| candles | Genuine observed + missed = expected | Continuity |
| five_venues | 5 exchanges, 4,000+ actual historical catalogue attempts | Wide scan + forward report |
| depth | 15 spot markets, at least 10 usable orderbooks, latest <=45 min | Microstructure |
| fee_model | Explicit per-side modeled fee+slippage, no assumed fill receipts | Entry-study |
| seven_days | >=7 real days and >=99% genuine 5-min coverage | Continuity |
| v4_samples | >=30 V4 completed closes for EACH of 21 strategies | Continuity |
| profits | Valid prespecified held-out after-fee result beating matched cash/buy-hold with meaningful uncertainty | Not yet independently available |
| server | At least six consecutive 5-min processed observations **on actual Codex machine**, safe RAM/CPU proof | Not available from GitHub |
| venue_fills | Executable, synchronized 5-venue prospective fills rather than later snapshots | Not yet proven |

**Interpretation:** VERIFIED and SAFE is not the same as PROFITABLE or FULLY DEPLOYED. Goals labelled UNKNOWN remain open. Goal NOT_MET means existing evidence demonstrates the requirement is presently unsatisfied. A missing report does not count as a passing test.

## Use

Open GitHub Actions workflow `CRYPTEX - confirmed evidence parity verifier` or inspect the parity artifact attached to the existing heartbeat watchdog. No exchange credentials or paid tools are required. Inspect `TEST_REPORT.md` and `PARITY_MATRIX.md` to see what is proven and what is not.

A future version may integrate REA tools **only if their actual availability, permissions and behaviour are verified**. The screenshot itself is not proof of an installed tool.
