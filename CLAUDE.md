# Working rules for this repo

## When you change lesson content, three things must move together

1. **`labs/lessonNN-<slug>/`** — the student-facing worksheet / README / code.
2. **The curriculum monorepo** (`../KOSEN69 - curriculum/lessons/<slug>/`) holds a
   byte-identical copy, enforced by a parity gate:
   `cd "../KOSEN69 - curriculum" && .venv/bin/python -m pytest tests/ -q`
   Apply the *same* edit to both — don't `cp` the `.md` files, the monorepo copies
   carry template tokens (`{{ slot_label }}`, `{{ labpath }}`).
3. **`instructor/lessonNN-<slug>-answer-key.md`** — what grades that lesson.
   **`instructor/` is git-ignored**, so neither CI nor the diff will remind you. A
   worksheet fix that leaves its key stale means students get marked wrong for
   correct answers.

## This course wraps a licensed AWS Academy curriculum

Lessons describe the AWS Academy labs *in our own words* and add a local, from-scratch
simulation. Never copy AWS Academy material into this repo.

## Simulations are simulations — say so

The Flask apps stand in for AWS services; they are not faithful models. Where a lab
simplifies a service's real behaviour, label it explicitly (e.g. lesson07b's
reset-on-success failure counter is a lab simplification — a real CloudWatch metric
filter is a stateless, time-windowed counter). Students should not learn a wrong
mental model of the actual AWS service from a convenience in our code.

## AWS facts worth double-checking, because we got them wrong once

- **Disabling** a KMS key is reversible (re-enabling restores decrypt); only
  **deleting** it, after the 7–30 day waiting period, is permanent.
- Trivy's `config` scanner does **not** parse standalone IAM policy JSON.
- A `trivy image` command running inside a container cannot see a locally built image.

## The fixed/control app must never emit a flag

Evidence flags prove the student exploited the *vulnerable* app. `fixed_app.py` had
once leaked `FLAG_REMEDIATE` at container startup, which defeated the whole evidence
model. Gate flags behind the exploited condition, and keep the control app flagless.

## Verify by running, not by reading

Payloads, expected output and line-number citations are executed literally by
students. Run the command before claiming it works.
