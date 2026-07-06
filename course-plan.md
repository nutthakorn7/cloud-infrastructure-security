# Cloud Infrastructure & Security (02005097) — Course Plan

> **Status: DRAFT — all 10 lesson topics built and Docker-verified.** This is the third arm of the
> preregistered study (`software-security/instructor/research/preregistration.md` §3, where this
> course is named "Cloud Infra & Security"). Read this whole file before touching any lesson —
> the shape of this course is genuinely different from its two sibling repos and the usual
> 19-week LAB/HYBRID/CONCEPTUAL template does not transfer directly. Remaining before this is
> usable for a live course: `seed_flags.py`/CTFd wiring, research instruments (H1–H4) — see
> [Open / not yet done](#open--not-yet-done).

## Why this course is structurally different from its two siblings

`software-security` and `security-cryptography` are both from-scratch, fully-owned 19-week
courses: every lab, every assessment, every line of teaching material is ours. This course is
not that. It **wraps AWS Academy's official, licensed Cloud Foundations + Cloud Security
Foundations curriculum** — 1 credit, ~15 lessons, run mostly through AWS's own Learner Lab
sandboxes, Knowledge Checks, and exams. Per the existing course's own reflection notes
(`Lesson 15 ~ reflection.pdf`, read from the source Drive folder), **40% of the final grade is
AWS-graded assignments** (6 Cloud Foundations items + 7 Cloud Security Foundations items),
identical in content for every student regardless of section.

Two facts settle how this course has to be built:

1. **Licensing (confirmed, not inferred).** The AWS Academy challenge-lab PDF
   (`Lesson13~Challenge (Cafe) lab...pdf`) carries an explicit footer: *"This work may not be
   reproduced or redistributed, in whole or in part, without prior written permission from
   Amazon Web Services, Inc."* — so **no AWS Academy file (pptx/pdf/zip) is ever copied into this
   repo**, public or private. This restricts AWS's own expression only, not our right to teach
   the same topics (IAM, S3, KMS, VPC, CloudTrail, security-group remediation) or write original
   assessments about them. If any AWS Academy source file is ever needed for instructor reference,
   it stays in the source Google Drive folder — never in `instructor/` or anywhere in this repo.
2. **Co-ownership.** The course is co-taught with Shinya Oyama (owner of the source material);
   he has agreed to the full controlled crossover protocol as preregistered (2 sections,
   counterbalanced AIR-Sec/Conventional blocks, student data collected under the study's IRB).
   The user teaches both sections solo this term, so **instructor is not confounded with
   treatment condition** — no `(1|instructor)` term needed in the analysis beyond what's already
   in `preregistration.md` §6.

## The shared-baseline resolution

Because ~40% of the grade runs on AWS's own auto-graded machinery, that portion **cannot** be the
manipulated variable — it's identical for every student in every section already. So:

- **Shared baseline (same for both sections, both blocks, untouched):** the AWS Academy Learner
  Lab activities themselves, their Knowledge Checks, and their auto-grading. This is "the full
  teaching" every student gets, matching preregistration §3's framing ("both sections get the
  full teaching — only the assessment format ... differs").
- **The manipulated layer (this is what AIR-Sec vs Conventional actually varies):** an
  **assessment artifact bolted onto specific lesson topics**, built entirely by us, never touching
  an AWS file:
  - **AIR-Sec condition:** a per-student attributable artifact (flag, seeded misconfiguration
    instance, or personalized parameter) + at least one of Audit-the-AI / EiPE / Prompt Problem +
    a viva spot-check — same taxonomy as the other two courses.
  - **Conventional condition:** a standard take-home worksheet question on the same topic, no
    per-student flag, no AI-resilience layer.
  - Both arms assess the **same underlying concept** the AWS lab already taught that lesson —
    we are not re-teaching AWS's content, we are adding an assessment layer on top of it.

This means the DV story stays clean: `learning gain`, `planted-error detection`, etc. are measured
against **our** layer, and the shared AWS-graded 40% is a controlled-equal covariate, not part of
the IV. Worth flagging explicitly in the paper/analysis as a documented deviation from a
fully-authored course (see `preregistration.md` §8 — anything not preregistered in this much
detail is exploratory unless amended).

## Lesson topic map (confirmed from source material, not copied)

Read directly from Shinya's own troubleshooting/correction notes for each AWS lab (not the AWS
files themselves) — these are the *topics*, described in our own words:

| Lesson | AWS topic (ours to assess, not to copy) | Kind | Block | Dir |
|---|---|---|---|---|
| 1–3 | AWS Academy Modules 1–3 (Intro, security fundamentals, IAM/access-securing concepts) + Knowledge Checks | **CONCEPTUAL ✅** | 1 | `lesson01-03-aws-fundamentals-intro` |
| 4 | EC2 instance roles, Lambda basics, Elastic Beanstalk (SSRF → instance-role credential theft) | **HYBRID ✅** | 1 | `lesson04-ec2-lambda-beanstalk` |
| 5 | S3 static website hosting; Lambda + SNS (public-write bucket-policy misconfig) | **LAB ✅** | 1 | `lesson05-s3-static-site-lambda-sns` |
| — | Load balancing & auto-scaling under load (Cloud Foundations Lab 6) | **HYBRID ✅** | 1 | `lesson06-load-balancing-autoscaling` |
| 7 | IAM privilege escalation — identity-based vs. resource-based policy conflicts (assume-role to reach a bucket the identity policy alone doesn't permit) | **LAB ✅** | 1 | `lesson07-iam-policy-evaluation` |
| 7 (same lesson, 2nd topic) | CloudTrail + CloudWatch + EventBridge monitoring/alerting on failed logins | **HYBRID ✅** | 2 | `lesson07b-cloudtrail-monitoring` |
| 10 | VPC networking — public/private subnets, NAT gateway, security groups vs. network ACLs | **HYBRID ✅** | 2 | `lesson10-vpc-networking` |
| 11 | S3 server-side encryption with KMS — envelope encryption, key-disable blast radius | **CONCEPTUAL ✅** | 2 | `lesson11-kms-envelope-encryption` |
| 13 | "Cafe" challenge lab — S3 versioning, lifecycle rules, cross-region replication (official AWS Academy Cloud Architect lab; topic only, never the file) | **CONCEPTUAL ✅** | 2 | `lesson13-s3-versioning-lifecycle-replication` |
| 14 | AWS Config + Lambda auto-remediation of a non-compliant security group | **HYBRID ✅** | 2 | `lesson14-config-lambda-remediation` |
| 15 | Reflection / wrap-up (existing AWS-graded mock exams) | — | — | n/a |

All 10 topics are built and Docker-verified where applicable (every LAB/HYBRID lesson has a real
`docker compose up` → `exploit.py` run captured in its own README; every CONCEPTUAL lesson has
personalized Audit-the-AI variants fact-checked against AWS's own public documentation). Ports
8104–8117 are allocated across the LAB/HYBRID labs — confirmed non-colliding.

Block assignment follows `preregistration.md` §3's table for this course: **Section A = Block 1
AIR-Sec / Block 2 Conventional; Section B = reversed.** Lessons 1–5 + Lab6/Load-Balancing = Block
1; Lessons 7(monitoring)/10/11/13/14 = Block 2. (Lesson 7's *two* topics split across blocks
deliberately — the IAM topic anchors Block 1's LAB week, the monitoring topic is Block 2 HYBRID.)

## All 10 lesson topics — built and verified

- **CONCEPTUAL — "AWS Fundamentals Audit-the-AI"** (`lesson01-03-aws-fundamentals-intro/`):
  worksheet-only, 4 personalized variants on Shared Responsibility Model / IAM default-deny /
  root-user hygiene / MFA, each fact-checked against AWS's own public docs.
- **HYBRID — "SSRF → Instance-Role Credential Theft"** (`lesson04-ec2-lambda-beanstalk/`): a
  simulated EC2 instance-metadata endpoint leaked via an unrestricted URL-fetch feature
  (CWE-918); fixed version blocks internal/metadata-shaped URLs. Elastic Beanstalk
  auto-scaling stays conceptual (worksheet only).
- **LAB — "Public-Write Bucket Policy"** (`lesson05-s3-static-site-lambda-sns/`): a static-site
  bucket policy that mistakenly grants `PutObject` to `Principal: "*"` alongside the intended
  `GetObject`, letting anonymous callers deface the site. Lambda+SNS stays conceptual.
- **HYBRID — "Load Balancing & Auto-Scaling Under Load"**
  (`lesson06-load-balancing-autoscaling/`): an unauthenticated, unthrottled "generate load"
  endpoint that forces a simulated Auto Scaling Group to max capacity — a Denial-of-Wallet
  attack (CWE-400). ALB/target-group concepts stay conceptual.
- **LAB — "IAM Policy Evaluation"** (`lesson07-iam-policy-evaluation/`): the identity-based-vs-
  resource-based policy conflict Shinya's own Lab 3.1 notes describe (devuser can't reach
  bucket3 via identity policy alone; an overly-broad **resource-based** policy with an unscoped
  `Principal` grants it anyway). CWE-284/CWE-668-class misconfiguration.
- **HYBRID — "Wrong Aggregation Key Defeats Alerting"** (`lesson07b-cloudtrail-monitoring/`): a
  failed-login monitor that keys its counter by `(source_ip, username)` instead of `source_ip`
  alone, so a password-spray attack (rotating usernames from one IP) never triggers an alert.
  EventBridge/SNS subscription mechanics stay conceptual.
- **HYBRID — "NACL Rule-Ordering Shadow"** (`lesson10-vpc-networking/`): a broad allow-all rule
  at a low rule-number shadows an intended deny-all at a higher number (NACLs evaluate in
  ascending rule-number order, first match wins — confirmed against AWS's own VPC docs). NAT
  gateway / security-group-vs-NACL comparison stays conceptual.
- **CONCEPTUAL — "KMS Envelope Encryption Audit-the-AI"** (`lesson11-kms-envelope-encryption/`):
  4 personalized variants on S3 SSE-KMS envelope encryption and key-disable blast radius, each
  fact-checked word-for-word against AWS's own SSE-KMS documentation.
- **CONCEPTUAL — "S3 Replication Misconception Audit-the-AI"**
  (`lesson13-s3-versioning-lifecycle-replication/`): 4 personalized variants, including the
  confirmed-false claim that enabling cross-region replication auto-backfills pre-existing
  objects (it only applies to new objects/versions going forward).
- **HYBRID — "Inverted Allowlist Auto-Remediation"** (`lesson14-config-lambda-remediation/`): a
  security-group auto-remediation function with an inverted allowlist condition that revokes the
  *allowed* ports and leaves a dangerous port (e.g. SSH from `0.0.0.0/0`) open — a silent,
  no-error failure mode.

Every LAB/HYBRID lesson was independently Docker-built, exploited, and torn down for real
(`docker compose up -d --build` → `exploit.py` → captured PASS output → `docker compose down`);
several builds caught and fixed a real bug in their own first draft during this verification
step (documented in each lesson's own README). No AWS Academy file content was referenced or
copied in any of the ten.

## Research instruments — status

- **`instructor/seed_flags.py` + `check_flag_keys.py` + `platform-build/` wiring — done and
  verified.** 7 challenge keys, own `FLAG_SALT`, drift guard passes, a generated flag confirmed
  to flow through a real lab end-to-end. Carries over the sibling repo's recommendation for a
  **third, separate challenge-host** (not yet provisioned — needs the user's budget sign-off).
- **`instructor/research/pre-post-test.md` (H3) and `planted-error-bank.md` (H2) — built.** Same
  methodology as the sibling instruments (parallel forms, proctoring protocol, scoring formulas)
  ported verbatim; only item content differs, mapped to this course's 10 lesson topics. Every
  technical claim in every item was verified against AWS's own public documentation (see each
  file's own Verification log) — not one is untested assertion. Still needs, before OSF lock: a
  pilot (3–5 students), Shinya's review, item statistics, and a cross-course difficulty-
  equivalence check (flagged in both files' verification logs as an open risk unique to having
  three parallel instruments).
- **H4 (engagement/motivation) survey + engagement telemetry + integrity instrument — reused
  as-is from `software-security/instructor/research/{surveys.md, engagement-telemetry.md,
  integrity-instrument.md}`.** These are genuinely course-agnostic (no lesson-specific content) —
  confirmed `security-cryptography` does not duplicate them either. No course-specific file
  needed here.

## ⚠️ The "dose" problem — needs a decision before this arm is confirmatory, not just built

Raised to the user directly, recorded here so it isn't lost: in the other two courses, the
AIR-Sec vs. Conventional manipulation covers the **entire** assessment for a block. Here, ~40% of
the grade (AWS's auto-graded labs/knowledge-checks) is **identical across both conditions** — only
the assessment layer this repo builds varies. That means:

1. **The treatment dose is a smaller fraction of total assessment here than in the other two
   arms** — this arm's effect size is likely attenuated relative to a uniform-dose design, and
   `preregistration.md` §5's power analysis was not computed separately for this structure.
2. **This is currently undocumented in the actual preregistration** — it's a note in this file,
   not an amendment to `preregistration.md` itself. If this arm is meant to be a full confirmatory
   arm (as agreed), the OSF registration needs an explicit amendment describing the shared-baseline
   structure *before* data collection — otherwise it's an undisclosed deviation discovered after
   the fact, which is exactly what §8's confirmatory/exploratory distinction exists to prevent.

**This does not block anything already built** — the instruments and lessons are correct
regardless of how this gets resolved. It changes the *analysis framing* for this arm's results,
not their content. **Not resolved here — the user's call.**

## Open / not yet done

- The third challenge-host itself (provisioning, not the wiring) — needs budget/approval.
- The OSF amendment for the dose problem above — needs the user's decision.
- The Docker images (`airsec-cloud/*:dev`) referenced by the now-built
  `challenges-import.csv`/`ctfd/challenges.yml` deployment catalog aren't built/pushed yet.

## Repo visibility — decided: public

Same as `software-security` and `security-cryptography` — no AWS content will ever be in this
repo (see the licensing section above), so there's no blocker to matching the other two courses'
convention. **Not yet actually created on GitHub** — this repo exists only locally so far; making
it public is the user's own action once a remote is created.
