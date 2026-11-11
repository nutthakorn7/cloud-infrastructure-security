# Lesson Plan — Local 03 across Weeks 5–6: Lambda/SNS concept and S3 public-write investigation

> **Current delivery policy (2026-11-11):** Students update the public repo and run this lab
> without a personal `.env`. Any `FLAG{…}` is a shared demo marker. Grade complete
> request/response evidence, explanation, and viva. Older per-student flag and seeding notes
> below document the original design and are not instructions for this cohort.

| | |
|---|---|
| **Course** | Cloud Infrastructure & Security · subject code **02005097** (`README.md`, `course-plan.md`; `docs/course-specification.md` still records the course code as ⬚) |
| **AWS lessons this attaches to** | **Week 5:** Cloud Foundations Module 6 Lambda/Elastic Beanstalk activities, plus the instructor's Lambda/SNS notification reference. **Week 6:** Module 7 storage and the AWS EBS lab, plus the instructor's S3 website reference. No AWS Academy material is reproduced here. |
| **Add-on kind** | **LAB** — runnable vulnerable/fixed pair with a flag (`docs/course-specification.md` §6) |
| **Block** | **1** (`docs/course-specification.md` §6). Block 1 = AIR-Sec for Section A, Conventional for Section B (`course-plan.md`) |
| **Duration of this add-on** | **45–60 min in Week 6**, after the estimated 30-minute AWS EBS lab. The S3-site case and notification scenario are introduced in Week 5. |
| **Lab folder** | `labs/lesson05-s3-static-site-lambda-sns` |
| **Targets** | `vulnerable_app.py` on **:8105** · `fixed_app.py` on **:8106** |
| **Signature exercise** | "Deface the Site" |
| **Standards** | **CWE-284** (Improper Access Control) · **CWE-668** (Exposure of Resource to Wrong Sphere) |
| **CLOs addressed** | **CLO2** demonstrate · **CLO3** apply the control (schedule row, `docs/course-specification.md` §6). Via §4's alignment table the per-student flag also carries **CLO5**, and the *Audit-the-AI* / *EiPE* tasks carry **CLO1** and **CLO4** |
| **Slides** | AWS Cloud Foundations Module 6 (Week 5) and Module 7 (Week 6) decks are primary; the instructor's Lambda/SNS and S3 website references support the local case. Original [Week 05–06 course bridges](../../slides/README.md) connect them to Local 03. AWS files are not copied into this repo. |
| **Session date / room / section** | ⬚ |

> **Naming note.** The folder and worksheet retain the existing **Lesson 5** label. In the current syllabus, Local 03 starts with Week 5 concepts and is completed and submitted after the Week 6 S3 investigation. Do not treat the folder number as an AWS Academy lab number.

---

## 1. Session objectives

By the end of this add-on a student can:

**Knowledge (K)**
- K1 — State why a bucket policy granting `Principal: "*"` the `s3:GetObject` action is the **correct, intended** configuration for static website hosting, not a security mistake in itself.
- K2 — Explain what changes when that same public statement **also** lists `s3:PutObject`: any anonymous caller, with no credentials and no assumed role, can overwrite objects in the hosted site, including `index.html`.
- K3 — State what least privilege means for a resource policy whose entire purpose is to be publicly readable — precision about *which actions* are public, not the absence of public access.
- K4 — Explain Lambda, SNS Standard topic and confirmed email-subscription roles; why confirmation is required, why `Publish` success does not prove email delivery, and why a later subscriber does not receive old messages by replay.

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

The Week 5 instructor notification scenario shows Lambda publishing to an SNS Standard topic with a confirmed email subscription. The publisher can receive a successful `Publish` response without proof of inbox delivery; an unconfirmed or later subscriber does not receive previous messages. SNS Standard has no built-in replay. This concept is introduced before the Week 6 S3 policy investigation, and neither the notification scenario nor a real S3 bucket is simulated in the Docker lab.

## 3. What students must have completed before this add-on

**Assigned weekly sequence:**
- **Week 5:** prepare Module 6 theory, complete the assigned Lambda and Elastic Beanstalk activities (formative, zero course points), then discuss the instructor's Lambda/SNS reference and introduce S3 website read/write permissions. Complete the Module 6 Knowledge Check after the module work.
- **Week 6:** prepare Module 7 storage theory, complete the assigned AWS EBS lab, then use the instructor's S3 website reference and this local README before answering the S3 policy questions and performing the local Docker investigation. Local 03 is due after Week 6. The syllabus does not assign a separate AWS Academy S3 website or SNS email lab for these weeks.

**On their own machine:**
- Docker Desktop working.
- A working host Python for the optional `exploit.py` — see §7 risk 1. The README's Step-by-step uses only `curl`, so a student without a working Python can still do the whole lab.

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
python3 -m pip install requests           # once, on the host
python3 exploit.py
```

(The last two lines are an optional one-shot check. Students work through the README's **Step-by-step**, which uses `curl` only. See §7 risk 1.)

> **Plainer worksheet (owner, 2026-11-02).** KOSEN students come through an accelerated high-school
> track, so the worksheet was reworded into short, concrete questions in Part 1, 2a and 2c, students
> may answer in Thai or English, and the lab README now has a copy-paste **Step-by-step** (curl
> commands with the expected output, run and checked). Same concepts, same flag, same point split.
> **2b (Audit-the-AI) is unchanged word for word**, including the planted policy and its hint. 2a
> now also asks for the re-`GET` that shows the defacement persisted (Step-by-step step 5; see risk
> 5). Mark the reasoning, not the language. If a curl prints only `HTTP 000`, the apps are still
> starting: wait a few seconds and rerun.
>
> **Answer Sheet (owner, 2026-11-02).** Students answer on the English *Local03 Answer Sheet*, a
> Google Doc that Classroom copies for each student, and turn that copy in. No PDF is needed. The
> sheet has both Parts, the 2a fields (curl command, flag, re-`GET` result, fixed-app HTTP code and
> error, public read on both apps) and an AI-use box.

### 4a. AIR-Sec section (Block 1 = Section A) — 60-minute plan

| Time | Task | Student does | Evidence produced |
|---|---|---|---|
| 0:00–0:05 | **Framing** | Recall the Week 5 S3-site case and Week 6 storage/reference material; ask which actions the public statement grants | — |
| 0:05–0:12 | **Stand the target up** | `cd labs/lesson05-s3-static-site-lambda-sns` then `docker compose up -d --build`; confirm both services answer on `/ping` (`mode` is `vulnerable` on :8105, `fixed` on :8106) | Screenshot of both `/ping` responses |
| 0:12–0:20 | **Worksheet 2a, baseline** | Anonymous `GET /bucket/website/index.html` on **both** :8105 and :8106, with no headers at all; confirm both return the site homepage | Two `200` responses — public read is identical on both apps |
| 0:20–0:32 | **Worksheet 2a, the defacement** | Anonymous `PUT /bucket/website/index.html` with **no `Authorization` header at all** against :8105; capture the flag from the response; re-`GET` the object to prove the overwrite persisted | Exact request (method, URL, headers-or-lack-thereof, body) + captured flag + the re-`GET` showing attacker HTML |
| 0:32–0:40 | **Worksheet 2a, confirm the fix** | The identical anonymous `PUT` against :8106 → `403` `AccessDenied`, no flag; then the identical anonymous `GET` on :8106 → still `200`; open both apps' `BUCKET_POLICY` and name the one difference | 403 response + the still-working GET + the policy diff in the student's own words |
| 0:40–0:50 | **Worksheet 2b — Audit-the-AI** | Examine the AI-supplied "standard static-website-hosting policy" in the worksheet; find the planted flaw and state what the statement actually grants | Written answer (start in class, finish as homework) |
| 0:50–0:57 | **Worksheet 2c — EiPE + simplification debrief** | 3–4 sentences for a non-technical stakeholder on why removing `PutObject` while keeping `GetObject` fixes the bug without breaking the site; then the instructor walks §5 (where the simulation is *not* real S3) | Written answer + no one leaves with a wrong model of the service |
| 0:57–1:00 | **Submit + tear down** | Confirm the submission bundle; `docker compose down` | The student's copy of the *Local03 Answer Sheet* → Turn in on Google Classroom |

**Compressing to 45 minutes.** Keep 0:00–0:40 intact — the four 2a steps and the policy comparison are the assessed core and the only part that needs the running targets. Send 2b and 2c home as written work, and replace the 0:50–0:57 debrief with the two-minute version of §5 (in-memory bucket; no Block Public Access; no identity policies). If the room is short on time to run the requests by hand, `python3 exploit.py` performs the whole GET/PUT/GET sequence against both targets in one shot — but the worksheet asks for *the exact request the student sent*, so anyone who takes that route must still be able to state it.

### 4b. Conventional section (Block 1 = Section B)

The worksheet's own instruction is *"complete only the part assigned to you this block"*, and Part 1 — five short-answer questions on the intended public-read pattern, the `PutObject` escalation, least privilege on a deliberately public resource, a real-world defacement consequence, and the Week 5 Lambda/SNS Standard-topic scenario — carries **no flag and no AI-resilience layer**, which is exactly the manipulation `course-plan.md` describes. Q5 requires subscription confirmation, delivery-vs-publish distinction and the absence of built-in replay; teach these from the local README before asking it. Submit the worksheet after Week 6.

⬚ **Not fixed anywhere in this repository:** whether the Conventional section also stands the local Docker target up in class. Running the exploit for them would import part of the AIR-Sec treatment into the control arm; leaving it out means the concept is assessed by writing only. Decide this once, apply it to every Conventional-block lesson, and record it here — it is a study-design decision, not a per-lesson one.

**Checks for understanding**
- After the baseline GETs: cold-call — *"both apps just returned 200 to an anonymous request. Which one is misconfigured, and why can this request not tell you?"*
- After the 403: *"point at the one line that differs between the two apps."*
- Exit ticket (one sentence): *"why does the fix not break the website?"*
- For the pub/sub topic, which the AIR-Sec arm's Part 2 never asks about (see §9): a Week 5 verbal check — *"The Lambda got a successful Publish response. Has the email arrived? Would a subscriber added tomorrow receive this message?"*

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
| Worksheet Part 2a (AIR-Sec sections) | The exact request that produced the flag, the flag itself, the re-`GET` showing the attacker's HTML, the fixed app's response to the identical request, and confirmation that anonymous `GET` still succeeds on **both** apps | K1–K3, P1–P4, A2 | Part of the worksheet mark (`docs/course-specification.md` §4) |
| Worksheet Part 2b — *Audit-the-AI* | The planted flaw in the AI-supplied policy, named, with what the statement actually grants | K1, K2, P5, A3 · CLO1/CLO4 per §4 | Part of the worksheet mark |
| Worksheet Part 2c — *EiPE* | 3–4 sentences a non-technical stakeholder could follow | K1, K3 · CLO4 | Part of the worksheet mark |
| Worksheet Part 1 (Conventional sections) | Five short answers — graded on the writing itself, in the worksheet's own words | K1–K4 | Part of the worksheet mark |
| **Per-student flag** — challenge key `s3site`, injected as `FLAG_S3SITE` | The flag value the *vulnerable* app returns on the anonymous write to `index.html` | A2 · CLO5 | Integrity control that also carries marks (§8) |
| Viva / random live check | Live reproduction of the capture and explanation of the policy difference | P1–P4, A2 | Pass / flag for follow-up |

**How the flag control works.** Flags are minted per student from the student ID (`instructor/seed_flags.py`, challenge key `s3site`), so a copied flag is traceable to the student it was *issued* to rather than being a matter of judgement. The **fixed app never returns a flag** — possession of one is itself evidence the student drove the vulnerable path. Submitting another student's flag is a violation for both parties ([SUBMISSION.md](../../SUBMISSION.md)).

**Deliverable, per the lab README.** The captured flag + the exact request (method, path, headers-or-lack-thereof, body) that produced it + a one-paragraph explanation of why granting `Principal: "*"` the `PutObject` action is a fundamentally different and much worse mistake than granting it `GetObject` on a website-hosting bucket.

**Submission.** Answers, including the captured flag, on the student's copy of the English *Local03 Answer Sheet* (Classroom makes the copy) → Turn in on Google Classroom, before the next class session; the sheet's AI-use box is required; late −10% of the earned score per day down to 0, marked only after a viva ([SUBMISSION.md](../../SUBMISSION.md)).

**Grading scale, and this layer's share of the final grade: ⬚** — an institutional decision, recorded nowhere in this repository (`docs/course-specification.md` §4, §8).

## 7. Risks and contingencies

| Risk | Mitigation |
|---|---|
| **1. Host Python for `exploit.py`.** The README now uses the `python3 -m pip install requests` / `python3 exploit.py` forms (a host may have `python3` but no `python` or `pip`), but a managed host Python can still refuse a global install | `exploit.py` is optional: the Step-by-step uses `curl` only. Use a virtual environment if a student wants the one-shot check |
| **2. `exploit.py` cannot be run inside the container.** The `Dockerfile` copies only `vulnerable_app.py fixed_app.py`, so although the image installs `requests`, the exploit script is not in it | Run it from the host as the README says, or skip it entirely — the two requests are short enough to make by hand, and the worksheet wants the student's own request anyway |
| **3. Ports 8105/8106 already bound** — usually another of this course's labs still running (`course-plan.md` allocates 8104–8117 across the labs) | `docker compose down` in the other lab folder before starting; or a student may republish the ports in their own working copy |
| **4. Order-of-operations wrecks the baseline evidence.** The bucket is an in-memory dict that the `PUT` mutates, so a student who defaces before capturing the baseline `GET` will screenshot "PWNED" as the site's homepage | Baseline `GET` on both apps first — it is step 1 of the worksheet for this reason. To reset, restart the vulnerable service |
| **5. A `PUT` sent without a JSON body still returns the flag.** `request.get_json(silent=True)` yields nothing when the request is not JSON, so `content` becomes empty — status `200`, flag returned, but the "defacement" is a blank page | Grade the **re-`GET`**, not the flag alone: the evidence must show the attacker's HTML being served back. Worksheet 2a asks for it (Step-by-step step 5), and the Step-by-step `curl` sends the body as JSON, as `exploit.py` does |
| **6. Everyone submits the same flag.** `docker-compose.yml` bakes a default `FLAG_S3SITE`, so a cohort whose flags were never seeded produces one identical flag class-wide and the attributability control silently does nothing | Seed per student before the session (`python3 instructor/seed_flags.py env <STUDENT_ID>`); the flag can also be overridden inline with the README's documented form, `FLAG_S3SITE=FLAG{...} docker compose up` (the braces there are the README's own placeholder, not a value). Spot-check two submissions for distinct values |
| **7. `seed_flags.py` is a shim and can refuse to run.** It exits with an error unless the curriculum monorepo sits as a sibling directory, and it needs `CIS_FLAG_SALT` (or the legacy `FLAG_SALT`) exported | Run the seeding step the day before, not five minutes before class; keep the salt out of the repo and out of screenshots |
| **8. First `docker compose up -d --build` builds `python:3.12-slim` and pip-installs for the whole room at once** | Pre-build before the session; students on a shared link should build in advance as homework |
| **9. Ethics drift into the Learner Lab.** A student with the AWS console open in the next tab is one step from trying an anonymous `PUT` against a real bucket to "see if it works" | Restate ETHICS.md rules 1–2 at the start and again before students switch back to AWS: the local labs and their own sandbox are the only approved targets, and probing real AWS can suspend the whole class's accounts |
| **10. Arm mix-up between sections.** In Block 1, Section A runs AIR-Sec (Part 2) and Section B runs Conventional (Part 1); a student who completes the wrong part has produced evidence that cannot be graded for their arm — and contaminates the study data | State the assigned part on the board and in the Classroom post at the start of the session; the worksheet's first line already says to complete only the assigned part |

## 8. Materials

- **Lab:** `labs/lesson05-s3-static-site-lambda-sns/` — `README.md`, `worksheet.md`, `vulnerable_app.py`, `fixed_app.py`, `exploit.py`, `docker-compose.yml`, `Dockerfile`, `requirements.txt`
- **Instructor-held (git-ignored):** `instructor/lesson05-s3-static-site-lambda-sns-answer-key.md` · `instructor/seed_flags.py` · `instructor/check_flag_keys.py`
- **Course documents:** [course-specification.md](../course-specification.md) · [course-plan.md](../../course-plan.md) · [SUBMISSION.md](../../SUBMISSION.md) · [ETHICS.md](../../ETHICS.md)
- **Slides:** Assigned AWS Module 6 and 7 decks and the instructor's Week 5 Lambda/SNS and Week 6 S3 website reference decks (held in the course Drive; not copied into this repo).
- **Reference, as listed in the lab README:** AWS's own public S3 documentation on hosting a static website, bucket policy examples, and the difference between `s3:GetObject` and `s3:PutObject` in a public `Principal: "*"` statement; AWS's public SNS and Lambda-with-S3 documentation for the event-driven concepts. **No AWS Academy file is used, quoted or copied.**
- **Baseline curriculum:** the AWS Academy Learner Lab itself — accessed through AWS, never mirrored here

## 9. Instructor notes escalated from lab content

Maintain these notes against the paired student-facing lab and curriculum copy; rendered parity is checked before publication.

1. **Host commands.** *Fixed:* the README now uses the `python3 -m pip` / `python3` forms, and the Step-by-step (2026-11-02) needs no host Python at all.
2. **Duration alignment.** The lab README states **45–60 min** and the current curriculum `lesson.yml` states `duration_min: 60`. Week 6 allocates this within the 70 minutes after the estimated AWS EBS lab.
3. **The Lambda/SNS topic is unassessed for the AIR-Sec arm.** The README says the pub/sub topic is *"covered in Worksheet Part 1 as an essay question"*, but the worksheet tells each student to complete only their assigned part — so an AIR-Sec-block section never answers a Lambda/SNS question at all, while the specification's schedule row pairs the S3 and Lambda/SNS topics in this lesson. Until the worksheet is amended, cover it verbally (see the §4 check-for-understanding) and do not claim it as assessed.
4. **Kickoff command inconsistency.** *Fixed 2026-11-02:* README step 2 and the Step-by-step both use `docker compose up -d --build`.
5. **Flag capture is weaker than the defacement claim.** Because the vulnerable app returns the flag for `index.html` regardless of whether a usable body was parsed (risk 5), the flag on its own does not evidence a real overwrite. *Addressed 2026-11-02:* worksheet 2a now asks for the re-`GET` (Step-by-step step 5), so grade it together with the flag.

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
