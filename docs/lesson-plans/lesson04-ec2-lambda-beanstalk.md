# Lesson Plan — Lesson 4: EC2 Instance Roles, Lambda Basics, Elastic Beanstalk

*CLOUD add-on. The AWS Academy Learner Lab is the baseline students do first; this is the
add-on that attacks and fixes the same idea locally. No AWS Academy material is reproduced here —
topics are described in our own words only.*

| | |
|---|---|
| **Course** | Cloud Infrastructure & Security (02005097) |
| **Attaches to (AWS lesson)** | AWS Academy Cloud Foundations — EC2 instance management, Lambda basics, Elastic Beanstalk (course spec "AWS lesson 4") |
| **Kind** | HYBRID — small Docker lab for the EC2 instance-role / SSRF concept; Lambda and Elastic Beanstalk stay conceptual (worksheet Part 1) |
| **Block** | 1 |
| **Add-on duration** | 45–60 min (per the lab's own `README.md`) |
| **Lab folder** | `labs/lesson04-ec2-lambda-beanstalk` |
| **Slides** | ⬚ (no `slides/week04`/`lesson04` deck in the repo — `slides/` holds only `README.md`) |
| **Analogous CWE** | CWE-918 (Server-Side Request Forgery) |
| **CLOs addressed** | **CLO2** demonstrate the misconfiguration · **CLO3** apply the correct control and verify the attack fails |

> **⬚ institution-specific:** section, room, date, grading scale, PLO list, and the exact
> percentage this add-on carries of the non-AWS 60% (course specification §4). The AWS-graded
> ~40% is scored by AWS and is identical for every student — it is *not* part of this add-on.

---

## 1. Session objectives

By the end of this add-on a student can:

**Knowledge (K)**
- K1 — Explain what an **EC2 instance role** is and how software on the instance obtains
  **temporary credentials** from the Instance Metadata Service (IMDS) without any long-lived key
  in the code (worksheet Q1–Q2).
- K2 — State why a server-side "fetch this URL for me" feature turns into credential theft, and
  name the class: **Server-Side Request Forgery** (CWE-918) (worksheet Q3, README "Why this
  concept matters").
- K3 — Explain why the bug lives in `/fetch-preview`, **not** in the metadata endpoint — the
  metadata route behaves exactly as an instance's IMDS is supposed to for on-instance callers
  (worksheet 2c).

**Skills (P)**
- P1 — Stand the vulnerable/fixed pair up and run the **benign baseline** fetch, showing the
  feature itself is legitimate (README signature step 1).
- P2 — Execute the **self-SSRF** against the vulnerable app and capture the leaked instance-role
  credentials and flag from the fetched metadata body (worksheet 2a).
- P3 — Show the **fixed** app rejects the identical request (`403`) and the literal
  `169.254.169.254` IMDS form, while an ordinary URL still fetches — proof the fix is a targeted
  block, not a blanket failure (README signature step 4).
- P4 — Name at least **two concrete defences** beyond blocking the literal string
  `169.254.169.254` (worksheet Q4).

**Attitude (A)**
- A1 — Attack only the two approved targets — the local Docker lab and the student's own assigned
  Learner Lab sandbox ([ETHICS.md](../../ETHICS.md)).
- A2 — Submit **attributable, reproducible** evidence: the student's own flag, with `whoami` /
  student ID / timestamp visible ([SUBMISSION.md](../../SUBMISSION.md)).
- A3 — Treat AI-generated cloud-security explanations as something to verify, not trust
  (worksheet 2b, course spec CLO4).

## 2. The through-line

A real EC2 instance can carry an IAM instance role, and code on it reads *temporary* credentials
from a link-local address (`169.254.169.254`) rather than holding a long-lived key. That design is
good — until the same instance runs a feature that fetches a **user-supplied URL** server-side with
no restriction on *which* URL. An attacker who cannot reach the metadata service from the internet
just asks the vulnerable feature to fetch it *for* them; the request originates from the trusted
instance, so IMDS answers. The fix is structural: the feature must decide *which* internal targets
it will never fetch, **before** the outbound request — not fetch first and hope.

## 3. Prerequisites — before this add-on runs

**Students must have completed, in order:**
1. The real **AWS Academy EC2 / Lambda / Elastic Beanstalk lab content** in their own Learner Lab
   sandbox (this is where the AWS console and its guard-rails are learned), and its Knowledge
   Check — that portion is AWS-graded (README step 1; [SUBMISSION.md](../../SUBMISSION.md)).
2. **Docker Desktop** working on their own machine.

**Instructor, before the session:**
- Pre-build the images (`docker compose up -d --build` in the lab folder) so a room of students is
  not pulling `python:3.12-slim` and running `pip install` at once — the single most common way to
  lose the first 15 minutes.
- Mint per-student flags for the cohort (see §6).
- Confirm host ports **8104** (vulnerable) and **8117** (fixed) are free — the lab uses these two
  because `:8105` is taken by `lesson05` (README "Port note").

## 4. Minute-by-minute add-on (AIR-Sec arm)

> **Pacing note.** The repo states one budget — **45–60 min for the whole add-on** (README). The
> per-segment minutes below are *suggested instructor pacing* within that envelope, not budgets
> prescribed by the worksheet; adjust freely. Task names, payloads, ports and commands are copied
> from the lab. Section assigned the **Conventional** arm this block runs §5 instead of this table.

| Suggested | Task | Student does (exact from lab) | Evidence produced |
|---|---|---|---|
| 0:00–0:08 | **Stand it up** | `cd labs/lesson04-ec2-lambda-beanstalk` → `docker compose up -d --build`; `pip install requests` (once, on host). Vulnerable on `:8104`, fixed on `:8117` | Both apps reachable |
| 0:08–0:15 | **Baseline (benign)** | `POST /fetch-preview {"url": "http://vulnerable:5000/ping"}` — works on both apps; the feature is legitimate, the bug is the *lack of restriction* | Note that the benign fetch succeeds |
| 0:15–0:30 | **The self-SSRF (capture)** | `POST /fetch-preview {"url": "http://localhost:5000/latest/meta-data/iam/security-credentials/AppRole"}` against `:8104` — the app fetches its own metadata route on your behalf and returns the fake `AccessKeyId`/`SecretAccessKey`/`Token` **and the flag** in the fetched body | The exact request body + the captured flag from the vulnerable app's response |
| 0:30–0:40 | **Confirm the fix** | The identical request against `:8117` → `403` *before* any outbound fetch; so is the literal `http://169.254.169.254/latest/meta-data/iam/security-credentials/AppRole`; an ordinary URL still returns `200` | The rejected request + its `403` response; note the ordinary URL still works |
| 0:40–0:45 | **One-shot check (optional)** | `python exploit.py` — expect two `PASS` lines and exit `0` (leak on `:8104`, rejection on `:8117`) | The two PASS lines |
| 0:45–0:60 | **EiPE + viva prep + submit** | Draft worksheet **2b** (plain-English: why "fetch a URL for me" leaks cloud credentials, and why blocking the literal `169.254.169.254` string is not a full fix — think `localhost`); ready the **2c** viva answers; submit | Worksheet 2a request/response pair + 2b answer → Classroom; 2c is a live spot-check |

**Formative checkpoints.**
- A student whose self-SSRF returns a fetch error (`502`) has almost always put the *host* port
  (`8104`/`8117`) in the JSON body. The URL is what the **server** fetches from its own network
  namespace, so it must be the in-container address — `http://localhost:5000/...`, port **5000**.
- A student who cannot see why `:8117` refuses the request should re-read `is_blocked()` in
  `fixed_app.py`: the block is on the *host* (`localhost`/`127.0.0.1`/`0.0.0.0`/`169.254.169.254`)
  and on any path under `/latest/meta-data`, decided before the outbound call.

## 5. Conventional-arm variant (same slot, no flag)

The section assigned the **Conventional** arm for Block 1 does **worksheet Part 1 only** — six essay
questions on the same concepts (instance role vs long-lived key; what IMDS is and why it is
on-instance-only; how the URL-fetch feature is abused and what the class is called; ≥2 defences
beyond the literal-string block; the EC2→Lambda operational/security shift; why the
misconfiguration is *more* consequential across an auto-scaling group). No Docker target, no
per-student flag, no AI-resilience layer — graded on the writing itself (worksheet Part 1). Use the
slot for guided discussion of those questions; the exploit is not run in this arm.

## 6. Assessment

| Instrument | Evidence | Outcome | Notes |
|---|---|---|---|
| Worksheet Part 2a (AIR-Sec arm) | The `POST /fetch-preview` body that leaked the flag, the captured flag, and the fixed-app request/response | K2, P2, P3, A2 | Part of the worksheet mark |
| Worksheet Part 2b — **EiPE** (AI-resilient) | 3–4 plain-English sentences on the credential-theft path and why a literal-string block is insufficient | K2, A3, CLO4 | The AI-resilient task for this lesson |
| Worksheet Part 2c — **viva** spot-check | Verbal, <2 min: why the metadata route "works correctly"; the one-line fix and its check category (allowlist vs blocklist vs auth); why adding login alone would not fix it | K3, P4 | Live during lab/office hours, not a written submission |
| Worksheet Part 1 (Conventional arm) | Six essays | K1–K2, P4 | The Conventional arm's whole submission |
| **Per-student flag** | The `flag` value inside the fetched metadata body from the **vulnerable** app | A2 | Integrity control (also carries marks); the fixed app never emits it |

**Per-student flag.** Mint with `python3 instructor/seed_flags.py env <STUDENT_ID>` — this course's
`seed_flags.py` already mints this lesson's `ec2` flag (its vocabulary now comes from the
curriculum monorepo's course manifest, not a hand-maintained list). Without a mint, `FLAG_EC2`
falls back to a public default placeholder that can be overridden per build
(`FLAG_EC2=FLAG{...} docker compose up`). Flags are per student and salted, so a copied flag is
traceable to the student it was issued to; the control app is deliberately flagless, so possession
of a flag *is* evidence the student exploited the vulnerable path (SUBMISSION.md integrity rules;
[../../CLAUDE.md](../../CLAUDE.md) "fixed/control app must never emit a flag").

**Deliverable (worksheet).** The captured flag + the exact `POST /fetch-preview` body that produced
it + a one-paragraph explanation of why this is SSRF and not "a bug in the metadata endpoint."

## 7. Materials

- Lab folder `labs/lesson04-ec2-lambda-beanstalk/`: `README.md`, `worksheet.md`,
  `vulnerable_app.py` (`:8104`), `fixed_app.py` (`:8117`), `exploit.py`, `docker-compose.yml`,
  `Dockerfile`, `requirements.txt` (`flask>=3.1.3`, `requests>=2.33.0`).
- Docker Desktop; `pip install requests` on the host for `exploit.py`.
- Instructor: `instructor/seed_flags.py` (git-ignored) and its answer key
  `instructor/lesson04-ec2-lambda-beanstalk-answer-key.md`.
- Rules of engagement: [ETHICS.md](../../ETHICS.md) · Submission: [SUBMISSION.md](../../SUBMISSION.md)
- Slides: ⬚ (none in repo).
- References the lab cites (all publicly available, no AWS Academy file used): AWS EC2 docs
  *Instance metadata and user data* / *IAM roles for Amazon EC2*; OWASP *SSRF Prevention Cheat
  Sheet*; public SSRF-to-cloud-metadata incident write-ups.

## 8. Where the simulation departs from real AWS (say this out loud)

- On a real instance, `169.254.169.254` is **link-local — reachable only from processes running on
  that instance**, not routable from the internet or another host. Plain Docker Compose cannot
  reproduce that boundary, so the "metadata service" here is **just another route on the same Flask
  app** (`/latest/meta-data/iam/security-credentials/AppRole`), and the exploit **always goes
  through** `/fetch-preview` — never a direct hit on the metadata route from the host. That
  preserves the real attack shape (the attacker never talks to IMDS directly) while being runnable
  without an AWS account (README "Simulation limits").
- The `/fetch-preview` payload targets the app's **own in-container address**
  (`http://localhost:5000/...`), because the server fetches from its own network namespace — not
  the host-mapped port (`exploit.py` comment).
- The shipped fix in `fixed_app.py` is a **blocklist** (`BLOCKED_HOSTS` + a `/latest/meta-data`
  path prefix). That is deliberate teaching material, not the last word: worksheet 2c asks students
  to critique blocklist vs allowlist, and Q4 asks for stronger defences. Do not present the
  blocklist as a complete solution — it is exactly what the viva interrogates.

## 9. Risks and contingencies

| Risk | Mitigation |
|---|---|
| The self-SSRF is a **nested request into the same process** (`/fetch-preview` → `/latest/meta-data`). A single-threaded server deadlocks on it | Both apps already run `app.run(..., threaded=True)`; if a student edits the app, keep `threaded=True` or the request hangs (`vulnerable_app.py` comment) |
| Student puts the **host port** (`8104`/`8117`) in the JSON body and gets a `502` fetch error | The URL is what the *server* fetches from inside its container — it must be `http://localhost:5000/...`, port **5000** (see §4 checkpoint) |
| Slow/failed pull of `python:3.12-slim` or `pip install` during `docker compose up -d --build` in class | Pre-build before the session; keep an offline image copy (`docker save`/`docker load`) |
| `pip install requests` on the host fails (managed Python / no venv) | `exploit.py` is optional — the worksheet flow is reachable by hand with `curl`/an HTTP client; run the request/response manually |
| Ports `8104`/`8117` already bound by another lesson's containers | `docker compose down` the other lab first; these two ports are confirmed non-colliding across the repo (README "Port note") |
| A student "captures" the flag from the **fixed** app or a classmate | The fixed app never returns the flag; per-student salted flags make a shared flag traceable to its issuee — viva-spot-check the pair (SUBMISSION.md) |
| A student wants to try the real IMDS string against real infrastructure | Out of bounds — only the local lab and the student's own Learner Lab are approved targets (ETHICS.md); the literal `169.254.169.254` form is exercised **only** against the local `:8117`/`:8104` apps |

## 10. Post-teaching reflection

*Complete after the session — this also feeds the course's engagement data.*

- Attendance / completion: ⬚
- Time actually taken per segment (vs. the 45–60 min envelope): ⬚
- Where the class got stuck (host-port-in-payload? the `threaded` nested request? blocklist vs
  allowlist?) and what unblocked them: ⬚
- Misconception that showed up in the **EiPE (2b)** answers — did students grasp why `localhost`
  defeats a literal-string block?: ⬚
- Quality of the **viva (2c)** answers — could students place the bug in `/fetch-preview` rather
  than the metadata endpoint?: ⬚
- Anything to change before this add-on runs again: ⬚
