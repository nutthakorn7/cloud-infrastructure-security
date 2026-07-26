# Lesson Plan — Lesson 5 add-on: S3 Static Website Hosting + Lambda/SNS Event-Driven Email

| | |
|---|---|
| **Course** | Cloud Infrastructure & Security · subject code **02005097** (`README.md`, `course-plan.md`; `docs/course-specification.md` still records the course code as ⬚) |
| **AWS lesson this attaches to** | **Lesson 5** — S3 static website hosting, plus the Lambda + SNS event-driven email pattern (topic named in our own words; **no AWS Academy material is reproduced anywhere in this plan or in the lab**) |
| **Add-on kind** | **LAB** — runnable vulnerable/fixed pair with a flag (`docs/course-specification.md` §6) |
| **Block** | **1** (`docs/course-specification.md` §6). Block 1 = AIR-Sec for Section A, Conventional for Section B (`course-plan.md`) |
| **Duration of this add-on** | **45–60 min** — the figure the lab's own README states. This is *not* a full contact session; the AWS Academy Learner Lab is the baseline and comes first |
| **Lab folder** | `labs/lesson05-s3-static-site-lambda-sns` |
| **Targets** | `vulnerable_app.py` on **:8105** · `fixed_app.py` on **:8106** |
| **Signature exercise** | "Deface the Site" |
| **Standards** | **CWE-284** (Improper Access Control) · **CWE-668** (Exposure of Resource to Wrong Sphere) |
| **CLOs addressed** | **CLO2** demonstrate · **CLO3** apply the control (schedule row, `docs/course-specification.md` §6). Via §4's alignment table the per-student flag also carries **CLO5**, and the *Audit-the-AI* / *EiPE* tasks carry **CLO1** and **CLO4** |
| **Slides** | ⬚ — `slides/` in this course is deliberately empty (`slides/README.md`); no original deck exists for this lesson |
| **Session date / room / section** | ⬚ |

> **Naming note.** The lab folder, README and worksheet call this **Lesson 5** — the *AWS lesson number* it attaches to. The curriculum monorepo (`courses/cloud-infrastructure-security.yml`) lists the same lesson at **slot 3** of 11 schedule slots (10 of which carry an add-on; slot 11 is a non-add-on "Reflection & Wrap-up" review entry). Both labels refer to the same material; use "Lesson 5" with students, since that is what the worksheet header and the submission filename convention use.

---

## 1. Session objectives

By the end of this add-on a student can:

**Knowledge (K)**
- K1 — State why a bucket policy granting `Principal: "*"` the `s3:GetObject` action is the **correct, intended** configuration for static website hosting, not a security mistake in itself.
- K2 — Explain what changes when that same public statement **also** lists `s3:PutObject`: any anonymous caller, with no credentials and no assumed role, can overwrite objects in the hosted site, including `index.html`.
- K3 — State what least privilege means for a resource policy whose entire purpose is to be publicly readable — precision about *which actions* are public, not the absence of public access.
- K4 — Explain why a Lambda function publishing to an SNS topic can complete and return without the subscriber's inbox being reachable, read, or even subscribed yet, and how that differs from a synchronous request-response call.

**Skills (P)**
- P1 — Issue an anonymous `GET /bucket/website/index.html` against **both** targets and show that public read works identically on `:8105` and `:8106`.
- P2 — Deface the homepage with an anonymous `PUT /bucket/website/index.html` sent with **no `Authorization` header at all**, capture the flag the vulnerable app returns, and re-`GET` the object to show the overwrite persisted.
- P3 — Fire the identical anonymous `PUT` at `:8106` and obtain `403` `AccessDenied` with no flag, while the anonymous `GET` on `:8106` still returns `200`.
- P4 — Read the `BUCKET_POLICY` list in each app and name the single difference that produces those two outcomes.
- P5 — Find the planted flaw in the AI-supplied bucket policy in Worksheet 2b and say in plain English what it actually grants.

**Attitude (A)**
- A1 — Attack only the two approved targets — the local Docker labs in `labs/` and their own assigned Learner Lab sandbox — under [ETHICS.md](../../ETHICS.md). Never send this request at a real S3 bucket.
- A2 — Submit a flag that is attributable to themselves, and be able to reproduce the capture live on request.
- A3 — Treat AI-generated cloud configuration as something to verify against documented behaviour, not to trust.

## 2. Key idea (the through-line)

Public read and public write are not two points on one scale — they are different kinds of decision. Static website hosting *requires* that anonymous browsers can read the objects, so `Principal: "*"` on `GetObject` is the feature working as designed. The bug this lab teaches sits on top of that correct pattern: someone widened the same public statement to `PutObject` as well, most plausibly by reusing a read/write template written for an authenticated deploy role. From that moment the bucket's own policy hands write access to the entire internet, and there is no credential, password or role for an attacker to obtain first. Least privilege on a deliberately public resource therefore means being exact about *which actions* the wildcard principal gets — not refusing to have a wildcard principal at all.

The second topic of this AWS lesson — Lambda publishing to an SNS topic that fans a message out to a subscribed email address — carries the complementary idea: in a pub/sub architecture the publisher's job is finished once the message is accepted by the topic, whatever the subscriber is doing. That decoupling is the whole point, and it is why the two topics sit in one lesson.

## 3. What students must have completed before this add-on

**In the AWS Academy Learner Lab (first, and graded by AWS):**
- That lesson's AWS Academy module and its Knowledge Check ([SUBMISSION.md](../../SUBMISSION.md) — AWS first, add-on second).
- The real Learner Lab exercise on **S3 static website hosting**, and the **Lambda + SNS email exercise** — the lab README is explicit that this is still where the actual console UI, bucket creation and SNS topic wiring are learned. Nothing in this add-on re-teaches or replaces it.

**On their own machine:**
- Docker Desktop working.
- A working host Python for `exploit.py` — see §7 risk 1; on a machine where only `python3` exists, the README's commands need the `python3 -m pip` / `python3` forms.

**Instructor, before the session:**
- Build the images ahead of time so a whole room is not pulling `python:3.12-slim` and pip-installing at once.
- Mint the per-student flags: `python3 instructor/seed_flags.py env <STUDENT_ID>` (the shim needs the curriculum monorepo as a sibling directory and `CIS_FLAG_SALT`, or the legacy `FLAG_SALT`, exported). Without this every student gets the same default `FLAG_S3SITE` baked into `docker-compose.yml` and the attributability control is void.
- Re-read `instructor/lesson05-s3-static-site-lambda-sns-answer-key.md` (git-ignored, instructor-held) against the current worksheet.

## 4. The add-on session — minute by minute

> **Where these minutes come from.** The task *names and content* below are the worksheet's and README's own; the **minute split is this plan's allocation** inside the 45–60 min envelope the lab README states. Neither the README, the worksheet nor the code carries a per-task budget — do not treat these numbers as fixed course material.

**Kickoff commands, exactly as the lab README has them:**

```bash
cd labs/lesson05-s3-static-site-lambda-sns
docker compose up -d --build   # vulnerable_app.py on :8105, fixed_app.py on :8106
pip install requests           # once, on the host
python exploit.py
```

(The README's step 2 gives the shorter kickoff `docker compose up -d`; use the `--build` form above on first run. See §7 risk 1 before the class types the last two lines.)

### 4a. AIR-Sec section (Block 1 = Section A) — 60-minute plan

| Time | Task | Student does | Evidence produced |
|---|---|---|---|
| 0:00–0:05 | **Framing** | Recall what the Learner Lab exercise already did; hear today's question — *not* "is a public bucket bad", but "which actions did the public statement grant" | — |
| 0:05–0:12 | **Stand the target up** | `cd labs/lesson05-s3-static-site-lambda-sns` then `docker compose up -d --build`; confirm both services answer on `/ping` (`mode` is `vulnerable` on :8105, `fixed` on :8106) | Screenshot of both `/ping` responses |
| 0:12–0:20 | **Worksheet 2a, baseline** | Anonymous `GET /bucket/website/index.html` on **both** :8105 and :8106, with no headers at all; confirm both return the site homepage | Two `200` responses — public read is identical on both apps |
| 0:20–0:32 | **Worksheet 2a, the defacement** | Anonymous `PUT /bucket/website/index.html` with **no `Authorization` header at all** against :8105; capture the flag from the response; re-`GET` the object to prove the overwrite persisted | Exact request (method, URL, headers-or-lack-thereof, body) + captured flag + the re-`GET` showing attacker HTML |
| 0:32–0:40 | **Worksheet 2a, confirm the fix** | The identical anonymous `PUT` against :8106 → `403` `AccessDenied`, no flag; then the identical anonymous `GET` on :8106 → still `200`; open both apps' `BUCKET_POLICY` and name the one difference | 403 response + the still-working GET + the policy diff in the student's own words |
| 0:40–0:50 | **Worksheet 2b — Audit-the-AI** | Examine the AI-supplied "standard static-website-hosting policy" in the worksheet; find the planted flaw and state what the statement actually grants | Written answer (start in class, finish as homework) |
| 0:50–0:57 | **Worksheet 2c — EiPE + simplification debrief** | 3–4 sentences for a non-technical stakeholder on why removing `PutObject` while keeping `GetObject` fixes the bug without breaking the site; then the instructor walks §5 (where the simulation is *not* real S3) | Written answer + no one leaves with a wrong model of the service |
| 0:57–1:00 | **Submit + tear down** | Confirm the submission bundle; `docker compose down` | `Lesson05_<StudentID>.pdf` → Google Classroom |

**Compressing to 45 minutes.** Keep 0:00–0:40 intact — the four 2a steps and the policy comparison are the assessed core and the only part that needs the running targets. Send 2b and 2c home as written work, and replace the 0:50–0:57 debrief with the two-minute version of §5 (in-memory bucket; no Block Public Access; no identity policies). If the room is short on time to run the requests by hand, `python exploit.py` performs the whole GET/PUT/GET sequence against both targets in one shot — but the worksheet asks for *the exact request the student sent*, so anyone who takes that route must still be able to state it.

### 4b. Conventional section (Block 1 = Section B)

The worksheet's own instruction is *"complete only the part assigned to you this block"*, and Part 1 — five essay questions on the intended public-read pattern, the `PutObject` escalation, least privilege on a deliberately public resource, a real-world defacement consequence, and the Lambda/SNS decoupling question — carries **no flag and no AI-resilience layer**, which is exactly the manipulation `course-plan.md` describes. Part 1 is a take-home worksheet question on the same concept.

⬚ **Not fixed anywhere in this repository:** whether the Conventional section also stands the local Docker target up in class. Running the exploit for them would import part of the AIR-Sec treatment into the control arm; leaving it out means the concept is assessed by writing only. Decide this once, apply it to every Conventional-block lesson, and record it here — it is a study-design decision, not a per-lesson one.

**Checks for understanding**
- After the baseline GETs: cold-call — *"both apps just returned 200 to an anonymous request. Which one is misconfigured, and why can this request not tell you?"*
- After the 403: *"point at the one line that differs between the two apps."*
- Exit ticket (one sentence): *"why does the fix not break the website?"*
- For the pub/sub topic, which the AIR-Sec arm's Part 2 never asks about (see §9): a 2-minute verbal cold-call — *"the Lambda returned successfully. Has anyone received the email yet? Do you know?"*

## 5. Where this simulation departs from real AWS — say this out loud

The lab is a small local Flask pair standing in for S3 behaviour, and the course specification requires the departures to be named in the same breath as the exercise. Everything below is visible in the lab's own source.

1. **The bucket is a Python dictionary.** `WEBSITE_FILES` lives in process memory; restarting the container restores the original homepage. A real defacement persists until someone restores the object — recovery, versioning and lifecycle are the Lesson 13 topic, not this one.
2. **Policy evaluation is a deliberate stub.** `is_allowed()` — the code's own docstring calls it a *"minimal stand-in for S3 bucket-policy evaluation"* — returns true if any statement has principal `"*"` and lists the action. There are no identity-based policies, no explicit `Deny`, no evaluation order, no conditions, no ACLs or object ownership, and **no S3 Block Public Access layer** — the account-and-bucket-level control that CLO3 names. In this simulation the bucket policy really is the only thing between the object and the public, which is precisely why the lab is instructive and precisely what makes it simpler than AWS. Identity-vs-resource policy evaluation is Lesson 7's lab; do not let students conclude they have already seen it.
3. **The interface is a JSON API, not an S3 endpoint.** Objects are addressed at `/bucket/website/<filename>`, the `PUT` body is JSON with a `content` field, and responses are JSON. A real static-website endpoint serves the object's bytes to a browser and a real `PUT` carries the raw object body. The error shapes — `403` `AccessDenied`, `404` `NoSuchKey` — do mirror S3's names on purpose.
4. **Nothing in AWS ever returns a flag.** The vulnerable app returns the flag in the `PUT` response for `index.html`; that is the course's attributable-evidence mechanism, not a modelled S3 behaviour.
5. **Lambda and SNS are not simulated at all.** There is no event notification, no topic and no subscription anywhere in this lab — the README says so explicitly. The pub/sub topic is assessed by essay only.
6. **Both apps run Flask's built-in development server** (`app.run(host="0.0.0.0", port=5000)`) inside the container, published on 8105 and 8106. It is a teaching target, not a hosting stack: single process, no TLS, no CDN, no request logging.

## 6. Assessment

| Instrument | Evidence | Outcome | Weight |
|---|---|---|---|
| Worksheet Part 2a (AIR-Sec sections) | The exact request that produced the flag, the flag itself, the fixed app's response to the identical request, and confirmation that anonymous `GET` still succeeds on **both** apps | K1–K3, P1–P4, A2 | Part of the worksheet mark (`docs/course-specification.md` §4) |
| Worksheet Part 2b — *Audit-the-AI* | The planted flaw in the AI-supplied policy, named, with what the statement actually grants | K1, K2, P5, A3 · CLO1/CLO4 per §4 | Part of the worksheet mark |
| Worksheet Part 2c — *EiPE* | 3–4 sentences a non-technical stakeholder could follow | K1, K3 · CLO4 | Part of the worksheet mark |
| Worksheet Part 1 (Conventional sections) | Five essay answers — graded on the writing itself, in the worksheet's own words | K1–K4 | Part of the worksheet mark |
| **Per-student flag** — challenge key `s3site`, injected as `FLAG_S3SITE` | The flag value the *vulnerable* app returns on the anonymous write to `index.html` | A2 · CLO5 | Integrity control that also carries marks (§8) |
| Viva / random live check | Live reproduction of the capture and explanation of the policy difference | P1–P4, A2 | Pass / flag for follow-up |

**How the flag control works.** Flags are minted per student from the student ID (`instructor/seed_flags.py`, challenge key `s3site`), so a copied flag is traceable to the student it was *issued* to rather than being a matter of judgement. The **fixed app never returns a flag** — possession of one is itself evidence the student drove the vulnerable path. Submitting another student's flag is a violation for both parties ([SUBMISSION.md](../../SUBMISSION.md)).

**Deliverable, per the lab README.** The captured flag + the exact request (method, path, headers-or-lack-thereof, body) that produced it + a one-paragraph explanation of why granting `Principal: "*"` the `PutObject` action is a fundamentally different and much worse mistake than granting it `GetObject` on a website-hosting bucket.

**Submission.** Worksheet exported to PDF with screenshots embedded, named `Lesson05_<StudentID>.pdf`, plus the captured flag → Google Classroom, before the next class session; AI-tool disclosure required; late −10%/day up to 3 days ([SUBMISSION.md](../../SUBMISSION.md)).

**Grading scale, and this layer's share of the final grade: ⬚** — an institutional decision, recorded nowhere in this repository (`docs/course-specification.md` §4, §8).

## 7. Risks and contingencies

| Risk | Mitigation |
|---|---|
| **1. The README's host commands assume `python`/`pip` are on PATH.** Verified on this machine: `python3` exists, `python` and `pip` do not — so `pip install requests` and `python exploit.py` both fail as written | Have students use the `python3 -m pip install requests` / `python3 exploit.py` forms, or a virtual environment if the host Python refuses a global install. Announce this before the class types the block. **Do not edit the lab to fit the room** — this is escalated as a lab-content fix (§9) |
| **2. `exploit.py` cannot be run inside the container.** The `Dockerfile` copies only `vulnerable_app.py fixed_app.py`, so although the image installs `requests`, the exploit script is not in it | Run it from the host as the README says, or skip it entirely — the two requests are short enough to make by hand, and the worksheet wants the student's own request anyway |
| **3. Ports 8105/8106 already bound** — usually another of this course's labs still running (`course-plan.md` allocates 8104–8117 across the labs) | `docker compose down` in the other lab folder before starting; or a student may republish the ports in their own working copy |
| **4. Order-of-operations wrecks the baseline evidence.** The bucket is an in-memory dict that the `PUT` mutates, so a student who defaces before capturing the baseline `GET` will screenshot "PWNED" as the site's homepage | Baseline `GET` on both apps first — it is step 1 of the worksheet for this reason. To reset, restart the vulnerable service |
| **5. A `PUT` sent without a JSON body still returns the flag.** `request.get_json(silent=True)` yields nothing when the request is not JSON, so `content` becomes empty — status `200`, flag returned, but the "defacement" is a blank page | Grade the **re-`GET`**, not the flag alone: the evidence must show the attacker's HTML being served back. `exploit.py` sends the body as JSON; students working by hand must do the same |
| **6. Everyone submits the same flag.** `docker-compose.yml` bakes a default `FLAG_S3SITE`, so a cohort whose flags were never seeded produces one identical flag class-wide and the attributability control silently does nothing | Seed per student before the session (`python3 instructor/seed_flags.py env <STUDENT_ID>`); the flag can also be overridden inline with the README's documented form, `FLAG_S3SITE=FLAG{...} docker compose up` (the braces there are the README's own placeholder, not a value). Spot-check two submissions for distinct values |
| **7. `seed_flags.py` is a shim and can refuse to run.** It exits with an error unless the curriculum monorepo sits as a sibling directory, and it needs `CIS_FLAG_SALT` (or the legacy `FLAG_SALT`) exported | Run the seeding step the day before, not five minutes before class; keep the salt out of the repo and out of screenshots |
| **8. First `docker compose up -d --build` builds `python:3.12-slim` and pip-installs for the whole room at once** | Pre-build before the session; students on a shared link should build in advance as homework |
| **9. Ethics drift into the Learner Lab.** A student with the AWS console open in the next tab is one step from trying an anonymous `PUT` against a real bucket to "see if it works" | Restate ETHICS.md rules 1–2 at the start and again before students switch back to AWS: the local labs and their own sandbox are the only approved targets, and probing real AWS can suspend the whole class's accounts |
| **10. Arm mix-up between sections.** In Block 1, Section A runs AIR-Sec (Part 2) and Section B runs Conventional (Part 1); a student who completes the wrong part has produced evidence that cannot be graded for their arm — and contaminates the study data | State the assigned part on the board and in the Classroom post at the start of the session; the worksheet's first line already says to complete only the assigned part |

## 8. Materials

- **Lab:** `labs/lesson05-s3-static-site-lambda-sns/` — `README.md`, `worksheet.md`, `vulnerable_app.py`, `fixed_app.py`, `exploit.py`, `docker-compose.yml`, `Dockerfile`, `requirements.txt`
- **Instructor-held (git-ignored):** `instructor/lesson05-s3-static-site-lambda-sns-answer-key.md` · `instructor/seed_flags.py` · `instructor/check_flag_keys.py`
- **Course documents:** [course-specification.md](../course-specification.md) · [course-plan.md](../../course-plan.md) · [SUBMISSION.md](../../SUBMISSION.md) · [ETHICS.md](../../ETHICS.md)
- **Slides:** ⬚ — none; `slides/` is intentionally empty for this course
- **Reference, as listed in the lab README:** AWS's own public S3 documentation on hosting a static website, bucket policy examples, and the difference between `s3:GetObject` and `s3:PutObject` in a public `Principal: "*"` statement; AWS's public SNS and Lambda-with-S3 documentation for the event-driven concepts. **No AWS Academy file is used, quoted or copied.**
- **Baseline curriculum:** the AWS Academy Learner Lab itself — accessed through AWS, never mirrored here

## 9. Instructor notes escalated from lab content

Recorded here rather than fixed, because student-facing lab material and the curriculum monorepo copy are byte-parity-gated and must not be edited to make this plan tidy.

1. **Host commands.** The README's `pip install requests` / `python exploit.py` fail on a host that has only `python3` (verified on this machine — `python` and `pip` are absent from PATH). The `python3 -m pip` / `python3` forms would work everywhere the current ones do.
2. **Duration conflict.** The lab README states this add-on is **45–60 min**; the curriculum monorepo's `lessons/s3-static-site-lambda-sns/lesson.yml` carries `duration_min: 180`, which is the sibling-course lab length, not this course's. This plan follows the README. One of the two needs correcting so the monorepo does not schedule a three-hour block.
3. **The Lambda/SNS topic is unassessed for the AIR-Sec arm.** The README says the pub/sub topic is *"covered in Worksheet Part 1 as an essay question"*, but the worksheet tells each student to complete only their assigned part — so an AIR-Sec-block section never answers a Lambda/SNS question at all, while the specification's schedule row pairs the S3 and Lambda/SNS topics in this lesson. Until the worksheet is amended, cover it verbally (see the §4 check-for-understanding) and do not claim it as assessed.
4. **Kickoff command inconsistency.** README step 2 gives `docker compose up -d` while the Run-it block gives `docker compose up -d --build`; on a first run only the second builds the image.
5. **Flag capture is weaker than the defacement claim.** Because the vulnerable app returns the flag for `index.html` regardless of whether a usable body was parsed (risk 5), the flag on its own does not evidence a real overwrite. The worksheet asks for the request and the flag, not for the re-`GET`; graders should require the re-`GET` anyway, or the worksheet should ask for it.

## 10. Post-teaching reflection

*Complete after the session — this also feeds the course's engagement data.*

- Attendance / completion: ⬚
- Time actually taken per task (vs. the allocation in §4): ⬚
- Did the 45–60 min envelope hold, or did the AWS Learner Lab overrun into it: ⬚
- Where the class got stuck, and what unblocked them: ⬚
- Did anyone conclude that "public bucket = bug" rather than "public *write* = bug"? What corrected it: ⬚
- Quality of the *Audit-the-AI* answers — did students catch the planted flaw unaided: ⬚
- Did any misconception survive the §5 simplification debrief (especially Block Public Access, or persistence of the defacement): ⬚
- Flags: all distinct? Any duplicate submissions to follow up: ⬚
- Anything to change before this lesson runs again: ⬚
