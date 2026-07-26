# Lesson Plan — Lesson 7: IAM Policy Evaluation (Privilege Escalation)

*CLOUD add-on. The AWS Academy Learner Lab is the baseline students do first; this is the
add-on that attacks and fixes the same idea locally. No AWS Academy material is reproduced here —
topics are described in our own words only.*

| | |
|---|---|
| **Course** | Cloud Infrastructure & Security (02005097) |
| **Attaches to (AWS lesson)** | AWS Academy **Cloud Security Foundations Lab 3.1** — the identity-vs-resource IAM policy topic (lab `README.md` header); course specification §6 row **"AWS lesson 7"** |
| **Kind** | LAB — runnable vulnerable/fixed pair with a per-student flag (course specification §6; lab `README.md` header) |
| **Block** | 1 — "the IAM topic anchors Block 1's LAB week" (`course-plan.md`) |
| **Add-on duration** | **60–90 min** (per the lab's own `README.md`) — this is the single 60–90 min add-on the course specification §1 refers to; every other add-on is 45–60 min |
| **Lab folder** | `labs/lesson07-iam-policy-evaluation` |
| **Slides** | ⬚ (no deck in the repo — `slides/` holds only `README.md`; so does `quizzes/`) |
| **Analogous CWE** | CWE-284 (Improper Access Control) · CWE-668 (Exposure of Resource to Wrong Sphere) |
| **CLOs addressed** | **CLO1** shared responsibility · **CLO2** demonstrate the misconfiguration · **CLO3** apply the correct control and verify the attack fails (course specification §6) |

> **⬚ institution-specific:** section, room, date, grading scale, PLO list, and the exact
> percentage this add-on carries of the non-AWS 60% (course specification §4). The AWS-graded
> ~40% is scored by AWS and is identical for every student — it is *not* part of this add-on.

> **⬚ CLO1 coverage note (instructor).** The course specification's §6 row claims CLO1 for this
> lesson, but neither `README.md` nor `worksheet.md` carries a shared-responsibility item. CLO1 is
> therefore carried by **instructor framing** in §2 below — "AWS runs the policy evaluator; *you*
> write the `Principal`" — not by a graded task. Either say it out loud in the slot or record the
> gap. Do not fabricate a worksheet question for it.

---

## 1. Session objectives

By the end of this add-on a student can:

**Knowledge (K)**
- K1 — Distinguish an **identity-based** policy (attached to a principal) from a **resource-based**
  policy (attached to the resource) and give one example of each (worksheet Q1).
- K2 — Explain why a caller with **no identity-based grant at all** can still reach a resource,
  purely because of that resource's **own** policy (README "Objectives"; worksheet Q2).
- K3 — State what `Principal: "*"` on a resource-based policy actually grants, and why it is **not**
  shorthand for "any principal in our account" (README "Objectives"; worksheet Q3).
- K4 — Say what **least privilege** means for a resource-based policy *specifically*, as opposed to
  an identity-based one — a resource policy also decides **who**, which is an extra dimension an
  identity policy never has (worksheet Q5).

**Skills (P)**
- P1 — Establish the baseline: `POST /assume-role {"role": "BucketsAccessRole"}` → token, then show
  that token **can** `PUT bucket2` (its resource policy allows get and put) but **cannot** `PUT
  bucket1` (bucket1's policy is get-only) (README signature step 1).
- P2 — Execute the exploit — `PUT /bucket/bucket3/object/<name>` with **no `Authorization` header at
  all** against `:8107` — and capture the flag the vulnerable app returns (README signature steps
  2–3; worksheet 2a).
- P3 — Show the fixed app on `:8108` rejects the **identical** anonymous `PUT` with `403`, *and*
  rejects the same `PUT` from a validly-assumed `BucketsAccessRole` token, because fixed bucket3 is
  get-only for everyone (README signature step 4).
- P4 — Point at the one-statement difference between `BUCKETS_VULNERABLE["bucket3"]` and
  `BUCKETS_FIXED["bucket3"]` in `policy_engine.py` and describe it as an application of least
  privilege — scoping the `Principal` — not as "adding a check" (README "Objectives", third bullet).

**Attitude (A)**
- A1 — Attack only the two approved targets — the local Docker lab and the student's own assigned
  Learner Lab sandbox ([ETHICS.md](../../ETHICS.md)).
- A2 — Submit **attributable, reproducible** evidence: their own flag *plus* the exact request that
  produced it ([SUBMISSION.md](../../SUBMISSION.md); README "Evidence artifact").
- A3 — Treat an AI-generated bucket policy as something to verify against documented behaviour, not
  trust because it reads as confident (worksheet 2b; course specification CLO4).

## 2. The through-line

In IAM there are two places a grant can come from, and students who have only met identity policies
assume there is one. A principal's identity policy can grant nothing whatsoever and the principal
can still read and write a bucket, because the **bucket's own** policy names it. That is the whole
of worksheet Q2, and it is the setup for the bug: once you accept that a resource policy grants on
its own authority, the `Principal` field in that policy becomes a load-bearing security control. Set
it to `*` — an easy mistake, because it *reads* like "anyone in our account" — and the resource has
just granted itself to every caller on the internet, including one holding no credentials at all.
This is where the shared-responsibility split bites (CLO1): AWS operates the policy evaluator
faithfully; the customer writes the `Principal`, and the evaluator will honour a wildcard exactly as
written. The fix is not authentication — the requests here were never *missing* authentication, the
policy simply declared everyone acceptable. The fix is to name the one legitimate role and scope the
actions it may take.

## 3. Prerequisites — before this add-on runs

**Students must have completed, in order:**
1. The real **AWS Academy Lab 3.1** in their own Learner Lab sandbox — that is still where the
   actual AWS console UI is learned, and that portion is AWS-graded (README "This lesson" step 1;
   [SUBMISSION.md](../../SUBMISSION.md)).
2. **Docker Desktop** working on their own machine.

**Instructor, before the session:**
- Pre-build the images — `docker compose up -d --build` in the lab folder — so a room of students is
  not pulling `python:3.12-slim` and running `pip install` simultaneously. (The README's own
  verification transcript was captured with the `--build` form; the student-facing "Run it" block
  says `docker compose up -d`, which is correct only once an image exists — see §9.)
- Mint per-student flags for the cohort (see §6).
- Confirm host ports **8107** (vulnerable) and **8108** (fixed) are free. Verified: each of
  `8104`–`8117` is published exactly once across `labs/*/docker-compose.yml`, so these two do not
  collide with another lesson — but another lesson's stack left running still holds its own ports.
- Have the answer key open: `instructor/lesson07-iam-policy-evaluation-answer-key.md` (git-ignored).

## 4. Minute-by-minute add-on (AIR-Sec arm)

> **Pacing note.** The repo states one budget — **60–90 min for the whole add-on** (README). The
> per-segment minutes below are *suggested instructor pacing* within that envelope, not budgets
> prescribed by the worksheet; adjust freely. Task names, requests, ports and commands are copied
> from the lab. The section assigned the **Conventional** arm this block runs §5 instead of this
> table.
>
> **If the slot is 60 rather than 90 min:** run to 0:50, then set worksheet **2b** and **2c** as
> homework. Segments up to 0:50 are the ones that need the containers running.

| Suggested | Task | Student does (exact from lab) | Evidence produced |
|---|---|---|---|
| 0:00–0:08 | **Stand it up** | `cd labs/lesson07-iam-policy-evaluation` → `docker compose up -d`; `pip install requests` (once, on the host). Vulnerable on `:8107`, fixed on `:8108` | Both apps reachable — `/ping` reports `"mode": "vulnerable"` and `"mode": "fixed"` respectively |
| 0:08–0:20 | **Baseline — assume the role** | `POST /assume-role {"role": "BucketsAccessRole"}` → token. With that token: `PUT bucket2` succeeds (its resource policy allows get and put); `PUT bucket1` is refused `403 AccessDenied` (bucket1's policy is get-only) | The two responses, side by side — the grant came from the *bucket's* policy, not from the role's own |
| 0:20–0:35 | **The real question — drop the credentials** | `PUT /bucket/bucket3/object/<name>` against `:8107` with **no `Authorization` header at all** — no assumed role, no identity policy, nothing. It succeeds and the response carries the flag | The exact request (method, URL, and the *absence* of the header) + the captured flag |
| 0:35–0:50 | **Confirm the fix** | The identical anonymous `PUT` against `:8108` → `403`. Then the *same* `PUT` on `:8108` **with** a validly-assumed `BucketsAccessRole` token → also `403`, because fixed bucket3 is get-only | Both rejected requests and their `403 AccessDenied` bodies — the empirical proof that scoping `Principal` is what closed the hole, not "adding auth" |
| 0:50–0:57 | **One-shot check (optional)** | `python exploit.py` — expect two `PASS` lines and exit `0` (anonymous write + flag on `:8107`; rejection, no flag, on `:8108`) | The two PASS lines |
| 0:57–1:05 | **Read the one-line diff** | Open `policy_engine.py` and compare `BUCKETS_VULNERABLE["bucket3"]` with `BUCKETS_FIXED["bucket3"]`: `principal` goes `"*"` → `"BucketsAccessRole"`, and `actions` goes `["get", "put"]` → `["get"]` | One sentence naming that change as least privilege on *both* dimensions — who, and what |
| 1:05–1:20 | **Audit-the-AI (2b)** | Work worksheet **2b**: the AI-supplied bucket policy that claims to be "scoped to only our internal application role." Find the planted flaw and say, in plain English, what it actually grants. Use the worksheet's own hint about `Principal: "*"` plus a `Condition` on a tag | Written answer (2b) |
| 1:20–1:30 | **EiPE (2c) + submit** | Worksheet **2c**: 3–4 sentences a non-technical stakeholder could follow on why scoping `Principal` to `BucketsAccessRole` fixed the vulnerability *without removing any legitimate access*; then submit | Flag + 2a request/response pair + 2b/2c answers → Classroom |

**Formative checkpoints.**
- A student who reports `403` on the *vulnerable* app's anonymous `bucket3` write has usually sent
  the request to `:8108`. The two apps differ only in which policy table they import and in the
  vulnerable app's extra flag-emission block on `bucket3` writes (§9) — the URL (or `/ping`'s `mode`
  field) is the reliable way to tell them apart, not a source-level identity claim.
- A student who cannot explain *why* the baseline `PUT bucket1` failed has skipped the point of the
  slot. Send them back to `policy_engine.py`: bucket1 grants `["get"]` and `IDENTITY_POLICY` grants
  the role nothing, so there is no statement anywhere that permits a put.
- A student whose baseline suddenly starts returning `403` mid-session has almost certainly had the
  container recreated — tokens are held in memory (see §9). Re-assume the role.

## 5. Conventional-arm variant (same slot, no flag)

The section assigned the **Conventional** arm for Block 1 does **worksheet Part 1 only** — five
essay questions on the same concepts: identity-based vs resource-based policy with an example of
each; why `devuser` (via `BucketsAccessRole`) can still read bucket1 and write bucket2 when its
identity policy grants neither; what `"Principal": "*"` actually grants and whether that equals "any
AWS user in our account"; one real-world consequence of an over-broad bucket policy; and what least
privilege means for a resource-based policy specifically. No Docker target, no per-student flag, no
AI-resilience layer — graded on the writing itself (worksheet Part 1). Use the slot for guided
discussion of those five; the exploit is not run in this arm.

## 6. Assessment

| Instrument | Evidence | Outcome | Notes |
|---|---|---|---|
| Worksheet Part 2a (AIR-Sec arm) | The exact request (method, URL, headers-or-lack-thereof) that got the flag on `:8107`, the captured flag, and the request tried against `:8108` with the response it returned instead | K2, K3, P2, P3, A2 | Part of the worksheet mark |
| Worksheet Part 2b — **Audit-the-AI** (AI-resilient) | The planted flaw in the supplied bucket policy, and a plain-English statement of what that policy actually grants | K3, A3, CLO4 | The AI-resilient task for this lesson. Model answer and the common wrong answers are in the git-ignored answer key — do not circulate |
| Worksheet Part 2c — **EiPE** | 3–4 stakeholder-readable sentences on why scoping `Principal` fixed it without removing legitimate access | K4, A3 | Part of the worksheet mark |
| Worksheet Part 1 (Conventional arm) | Five essays | K1–K4 | The Conventional arm's whole submission |
| **Per-student flag** | The `flag` value returned by the **vulnerable** app's write to bucket3 | A2 | Integrity control that also carries marks; the fixed app never emits it |
| Viva spot-check (optional) | Verbal, <2 min: which policy granted the access, and why adding authentication alone would not have closed it | P4, A2 | Sourced to `course-plan.md`'s AIR-Sec taxonomy ("+ a viva spot-check"), **not** to the worksheet — this worksheet defines no viva item |

**Per-student flag.** Mint with `python3 instructor/seed_flags.py env <STUDENT_ID>` — this course's
`seed_flags.py` already mints this lesson's `iam` flag (its vocabulary now comes from the curriculum
monorepo's course manifest, not a hand-maintained list). Without a mint, `FLAG_IAM` falls back to a
public default placeholder that can be overridden per build (`FLAG_IAM=FLAG{...} docker compose
up`). Flags are per student and salted, so a copied flag is traceable to the student it was issued
to; the control app is deliberately flagless, so possession of a flag *is* evidence the student
exploited the vulnerable path (SUBMISSION.md integrity rules; [../../CLAUDE.md](../../CLAUDE.md)
"The fixed/control app must never emit a flag").

> **Grading caution (verified by running the lab).** On `:8107` the flag is returned on **any**
> successful `PUT` to bucket3, including one made with a validly-assumed `BucketsAccessRole` token —
> not only the anonymous one. So the flag alone does not evidence that the student did the
> credential-free request the worksheet asks for. Mark **2a's request evidence** (the absent
> `Authorization` header), which the README's own Deliverable already demands, rather than the flag
> on its own. See §9 and the escalation note at the end of this plan.

**Deliverable (worksheet).** The captured flag + the exact request that produced it (bucket, method,
headers-or-lack-thereof) + a one-paragraph explanation of why a wildcard `Principal` on a
resource-based policy is a different thing from "no authentication."

## 7. Materials

- Lab folder `labs/lesson07-iam-policy-evaluation/`: `README.md`, `worksheet.md`,
  `policy_engine.py` (the shared policy tables and `is_allowed`), `vulnerable_app.py` (`:8107`),
  `fixed_app.py` (`:8108`), `exploit.py`, `docker-compose.yml`, `Dockerfile`, `requirements.txt`
  (`flask>=3.1.3`, `requests>=2.33.0`).
- Docker Desktop; `pip install requests` on the host for `exploit.py`.
- Instructor: `instructor/seed_flags.py` and the answer key
  `instructor/lesson07-iam-policy-evaluation-answer-key.md` (both git-ignored).
- Rules of engagement: [ETHICS.md](../../ETHICS.md) · Submission: [SUBMISSION.md](../../SUBMISSION.md)
- Slides: ⬚ (none in repo). Weekly quiz item: ⬚ (`quizzes/` holds only `README.md`).
- References the lab cites (all publicly available, no AWS Academy file used or copied): AWS IAM
  documentation — *Identity-based policies and resource-based policies*, *Policy evaluation logic*;
  AWS S3 documentation — *Bucket policy examples*, specifically why `"Principal": "*"` should almost
  always be paired with a `Condition` block or avoided entirely.

## 8. Where the simulation departs from real AWS (say this out loud)

`policy_engine.py` says it in its own docstring — it models "exactly the one concept this lesson is
about" and is "an original simplification for teaching, not AWS code." Five departures are worth
naming in the room, because a student who does not hear them will leave with a wrong model:

1. **`/assume-role` requires no credentials.** The endpoint checks only that the requested role is in
   `KNOWN_ROLES` and hands back a token to anyone who asks. Real STS `AssumeRole` requires the caller
   to already hold credentials **and** requires the role's own trust policy to permit that caller.
   This is the largest departure, and it cuts both ways pedagogically: in this lab even the
   "legitimately assumed role" path is unauthenticated, so the contrast the exercise draws is
   between *named* and *wildcard* principals, not between authenticated and anonymous callers.
2. **There is no explicit `Deny`, and no evaluation order.** `is_allowed()` walks the resource
   policy's Allow statements, then falls back to the principal's identity actions. Real IAM
   evaluation is default-deny with **explicit Deny overriding any Allow**; nothing in this engine
   models a Deny at all. Do not let students generalise "either policy grants it" into a complete
   statement of AWS policy evaluation.
3. **No account boundary and no organisation-level controls.** The engine's "identity *or* resource
   policy suffices" union is shaped like same-account S3 access. Real cross-account access needs
   both sides to allow, and real accounts also have SCPs, permissions boundaries, session policies
   and S3 Block Public Access — none of which exist here. Block Public Access in particular would
   have blunted this exact misconfiguration on a real bucket.
4. **Two different policy notations inside one lesson.** The engine uses bare `get`/`put` action
   strings and has no `Version`, `Sid`, `Effect`, `Resource` or `Condition` element whatsoever;
   worksheet 2b then presents a full-shape bucket policy with `s3:GetObject`/`s3:PutObject`, a
   `Resource` ARN and a `Condition` block. Flag the crossing explicitly — the engine's shape is a
   teaching reduction, and 2b's shape is the real one.
5. **`IDENTITY_POLICY` zeroes out both principals.** `devuser` *and* `BucketsAccessRole` are given
   empty action lists, so in this simulation **all** access comes from resource policies. That
   isolation is the point of the exercise (it is what makes Q2 answerable), but it is not what the
   role looks like in the real Lab 3.1 setup.

## 9. Risks and contingencies

| Risk | Mitigation |
|---|---|
| A student captures the flag from the **role-assumed** `PUT` and believes they performed the anonymous exploit | `vulnerable_app.py`'s `put_object` emits `FLAG_IAM` whenever the bucket is `bucket3`, whatever the principal — verified by running the lab. Grade the 2a **request evidence** (no `Authorization` header), not the flag alone; the viva spot-check in §6 separates the two in about a minute |
| Assumed-role tokens are held **in memory** (`ISSUED_TOKENS = {}`); a `docker compose` restart or container recreate silently invalidates a student's saved token, producing unexplained `403`s | Re-run `POST /assume-role` after any restart. Tell the class this before the baseline segment, not after the first confused hand goes up |
| Student runs the README's `docker compose up -d` on a machine with no image built yet | The README's verified transcript used `docker compose up -d --build`; pre-build in class (§3), or have students add `--build` on first run |
| Slow/failed pull of `python:3.12-slim`, or `pip install --no-cache-dir -r requirements.txt` failing during the image build, with a room-full of students building at once | Pre-build before the session; keep an offline image copy (`docker save`/`docker load`) |
| `pip install requests` on the host fails (managed Python / no venv) | `exploit.py` is optional — the whole worksheet flow is reachable by hand with any HTTP client: `POST /assume-role`, then `PUT /bucket/bucket3/object/<name>` with and without an `Authorization` header |
| Ports `8107`/`8108` already bound by another lesson's containers | `docker compose down` the other lab first; ports 8104–8117 are each published once across the repo's lab compose files, so the only collisions are self-inflicted |
| Student sends the exploit to `:8108` and concludes the lab is broken because they got `403` | `:8107` is the vulnerable target and `:8108` the fixed one; `/ping` reports `"mode": "vulnerable"` / `"mode": "fixed"` so the target is checkable in one request |
| A student "captures" the flag from the fixed app or from a classmate | `fixed_app.py`'s `put_object` has no flag code path at all, and fixed bucket3 is get-only — doubly impossible. Per-student salted flags make a shared flag traceable to its issuee; viva-spot-check the pair (SUBMISSION.md) |
| A student generalises "`Principal: "*"` plus a `Condition` is safe" from worksheet 2b, or wants to test a wildcard policy against real AWS to find out | 2b is precisely the trap; keep the discussion on documented behaviour. Testing outside the local lab and the student's own Learner Lab is out of bounds (ETHICS.md rules 1–2) — a boundary probe against real AWS infrastructure can get the whole class's Learner Lab access suspended |

## 10. Post-teaching reflection

*Complete after the session — this also feeds the course's engagement data.*

- Attendance / completion: ⬚
- Time actually taken per segment (vs. the 60–90 min envelope): ⬚
- Did the baseline segment (role can `PUT bucket2`, cannot `PUT bucket1`) land before the exploit, or
  did students jump straight to bucket3?: ⬚
- Where the class got stuck (wrong port? stale token after a restart? reading `policy_engine.py`?)
  and what unblocked them: ⬚
- Misconception in the **Audit-the-AI (2b)** answers — did students catch the planted flaw, or accept
  the `Condition` block as sufficient scoping?: ⬚
- Quality of the **EiPE (2c)** answers — could students explain the fix without reaching for
  "we added authentication"?: ⬚
- How many students submitted a flag whose 2a request evidence did **not** show the credential-free
  request?: ⬚
- Anything to change before this add-on runs again: ⬚

---

> **Instructor note — defects observed in lab content while writing this plan (not fixed here;
> lab content was left untouched):**
> 1. `vulnerable_app.py` returns the flag on *any* successful `PUT` to bucket3, including one made
>    with a validly-assumed role token — so the flag is not gated on the exploited (anonymous)
>    condition the README's Deliverable and worksheet 2a ask for. This is in tension with
>    `CLAUDE.md`'s own rule, "Gate flags behind the exploited condition."
> 2. The README's "Verified" transcript shows only 2 of the 4 lines `exploit.py` actually prints for
>    the FIXED target (the `GET bucket1 → 404` and `PUT bucket2 → 200` lines are omitted). Students
>    diffing their output line by line will think something is wrong.
> 3. The README's student-facing "Run it" block says `docker compose up -d`, while its own verified
>    run used `docker compose up -d --build`; a first run on a clean machine needs the build.
>
> Any change to the lab must move together with the curriculum monorepo copy and the git-ignored
> answer key (`CLAUDE.md`). This plan file lives in `docs/` and is **outside** the parity gate.
