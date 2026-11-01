# CRYPTEX isolated paper relay smoke test — 1 November 2026

## Actual verified test

- Workflow: [CRYPTEX - free disposable paper-engine relay test](https://github.com/maingame6/TEst-work/actions/runs/41299185723)
- Run ID: `41299185723`; result **success** after correcting two initial sandbox path errors in the workflow setup.
- Real completed Kraken 5-minute candle: new candle processed, from timestamp `1793529600` to `1793529900`.
- Account integrity: **21/21 agents** preserved, **13/13 audit checks passed**.
- PAPER_ONLY baseline and isolated-after balance: **$208.899241**, with zero new realized profit in this one cycle.
- Missing observations: **2** before and **2** after; no synthetic backfill.
- Production write: **none**. The sandbox discarded its local changes. Permissions were `contents: read` with checkout credentials not persisted.
- Dedicated DigitalOcean instances: **not contacted, created, resized, rebooted or altered**; CSGORisky untouched.
- Runner memory address-space capped to 768 MB; CPU time capped to 105 seconds.
- Source: `cryptex/ops/relay_canary.py`, workflow `.github/workflows/cryptex-relay-canary.yml`.
- No separate VPS purchased. Public standard GitHub-hosted Actions compute is free per GitHub documentation, subject to normal usage/Terms limits.

## Precisely what this does not prove

This was one successful disposable cloud-runner engine cycle. It did **not** establish
an independent always-on machine, guaranteed five-minute scheduling,
profitability, sustained 768 MB performance over seven days, or that a
separate $6/month DigitalOcean droplet is required. Never present the
canary's one correctly processed candle as a 99% continuity pass.

The existing GitHub Actions paper workflow remains the **only** writer
to the $210 paper journal. Do not activate another continuous writer
without an atomic lease/fence, production safety audit, and verified
handover. The CSGORisky relay droplet ID `612199466` must never host
CRYPTEX; only the existing Codex droplet ID `610231290` is the
preliminarily approved *candidate*, subject to on-host capacity review.

## If truly independent hosting is later needed

Do not provision a new paid server under the existing zero-additional-cost
constraint. GitHub's public-repository standard runners are free but
not an independent continuously running VPS. The previously observed
DigitalOcean 1 vCPU / 1 GB plan is around **$6/month** before any
applicable taxes. Cost approval and server host audit would be needed
before creating or enabling a new VPS.
