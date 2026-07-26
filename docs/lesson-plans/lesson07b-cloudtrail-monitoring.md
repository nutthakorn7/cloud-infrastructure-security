# Lesson Plan — Lesson 7 (2nd topic): CloudTrail + CloudWatch + EventBridge Monitoring

*CLOUD add-on. The AWS Academy Learner Lab is the baseline students do first; this is the
add-on that attacks and fixes the same idea locally. No AWS Academy material is reproduced here —
topics are described in our own words only.*

| | |
|---|---|
| **Course** | Cloud Infrastructure & Security · subject code **02005097** (`README.md`, `course-plan.md`; `docs/course-specification.md` still records the course code as ⬚) |
| **Attaches to (AWS lesson)** | AWS Academy Cloud Security Foundations — failed-console-login alerting: CloudTrail event recording → CloudWatch metric filter/alarm → EventBridge rule → SNS notification (course spec "AWS lesson 7 (2nd topic)"; the lab README places it as Lab 3.2-class material) |
| **Kind** | HYBRID — small Docker lab for the aggregation-key concept; EventBridge/SNS subscription mechanics stay conceptual (`course-plan.md`) |
| **Block** | 2 |
| **Add-on duration** | 45–60 min (per the lab's own `README.md`) |
| **Lab folder** | `labs/lesson07b-cloudtrail-monitoring` |
| **Slides** | ⬚ (no `lesson07b` deck in the repo — `slides/` holds only `README.md`) |
| **Analogous bug class** | CWE-778 (Insufficient Logging) **adjacent** / detective-control logic error — "the control exists and runs, but its aggregation key silently excludes the real attack shape" (lab README) |
| **CLOs addressed** | **CLO2** demonstrate the misconfiguration · **CLO3** apply the correct control and verify empirically (course spec §6 row for this lesson) |

> **⬚ institution-specific:** section, room, date, grading scale, PLO list, and the exact
> percentage this add-on carries of the non-AWS 60% (course specification §4). The AWS-graded
> ~40% is scored by AWS and is identical for every student — it is *not* part of this add-on.

---

## 1. Session objectives

By the end of this add-on a student can:

**Knowledge (K)**
- K1 — State the distinct role each stage plays in a real failed-login alerting pipeline —
  **CloudTrail** recording the sign-in event, **CloudWatch** metric filters/alarms counting and
  thresholding it, **EventBridge** routing to a target such as **SNS** (worksheet Part 1 Q1).
- K2 — Define an **aggregation key** for a metric that counts failed-login events, and explain how
  two different key choices over the *same* raw log data produce metrics that count different
  things (worksheet Part 1 Q2).
- K3 — Distinguish a **password-spray** pattern (many usernames, one source, 1–2 failures each)
  from a **classic brute-force** pattern (one username, many failures, one source), and say why
  both look like "many failed logins" in the raw log yet need different aggregation logic
  (worksheet Part 1 Q3; README "Why it's exciting").
- K4 — Explain why a wrong aggregation key is a **security** bug rather than a tuning or
  false-positive-rate issue — the control runs on every request, never crashes, never errors, and
  still cannot see the attack (worksheet Part 1 Q5).

**Skills (P)**
- P1 — Stand the vulnerable/fixed pair up and read the response shape of
  `POST /login-attempt` — `alert`, `count_for_key`, `note` (README "Endpoint").
- P2 — Run the rotating-username spray from one `source_ip` against the vulnerable app on `:8111`
  and confirm, attempt by attempt, that `count_for_key` never rises above 1 and no alert fires
  across 20 attempts (worksheet 2a).
- P3 — Run the **negative control** — the same username three times from the same IP against the
  *vulnerable* app — and show it *does* alert, proving the counter mechanics work and that the key
  choice is the defect (README "The vulnerability").
- P4 — Run the identical spray against the fixed app on `:8112`, identify the attempt number the
  alert fires on, and capture the emitted flag (worksheet 2a).
- P5 — State the general defender's principle: choose what you group log events by to match the
  threat's shape, not the record's shape (worksheet 2b).

**Attitude (A)**
- A1 — Attack only the two approved targets — the local Docker lab and the student's own assigned
  Learner Lab sandbox ([ETHICS.md](../../ETHICS.md)).
- A2 — Submit **attributable, reproducible** evidence: the student's own request/response
  sequences, with `whoami` / student ID / timestamp visible ([SUBMISSION.md](../../SUBMISSION.md)).
- A3 — Treat AI-generated cloud-security explanations as something to verify, not trust
  (worksheet 2b; course spec CLO4).

## 2. The through-line

Detective controls fail quietly. A missing alarm is obvious; an alarm that runs, counts correctly
and never fires is not. In this lab both services record every login event and both increment a
failure counter on every failed attempt — the only difference is **what the counter is keyed by**.
Key it by `(source_ip, username)` and a password-spray attacker, who deliberately tries each
username only once or twice, never pushes any single counter to the threshold no matter how many
total attempts they make. Key it by `source_ip` alone and the same traffic trips the same threshold
on the third attempt, because from a detection standpoint "one IP, many failed usernames" and "one
IP, many failed attempts at one username" are the same underlying event: somebody at that address
is guessing credentials. The lesson is that an aggregation key encodes a threat model, and if the
key does not match the threat, the control is decorative.

## 3. Prerequisites — before this add-on runs

**Students must have completed, in order:**
1. The real **AWS Academy failed-console-login alerting lab content** (CloudTrail → CloudWatch
   metric filter/alarm → EventBridge → SNS) in their own Learner Lab sandbox — that is where the
   AWS console UI, the actual metric-filter syntax and EventBridge rule configuration are learned,
   and that portion is AWS-graded (lab README step 1; [SUBMISSION.md](../../SUBMISSION.md)).
2. **Docker Desktop** working on their own machine.

**Instructor, before the session:**
- Pre-build the images (`docker compose up -d --build` in the lab folder) so a room of students is
  not pulling `python:3.12-slim` and running `pip install` at once.
- Mint per-student flags for the cohort (see §6).
- Confirm host ports **8111** (vulnerable) and **8112** (fixed) are free. No other lab in this
  repository binds them; a collision means this lab is already up, or an unrelated host process
  holds the port.
- Have `requests` available on the host for `exploit.py`, **or** be ready to run the whole flow by
  hand with `curl` — see §9.

## 4. Minute-by-minute add-on (AIR-Sec arm — Section B this block)

> **Pacing note.** The repo states one budget — **45–60 min for the whole add-on** (README). The
> per-segment minutes below are *suggested instructor pacing* within that envelope, not budgets
> prescribed by the worksheet; adjust freely. Task names, ports, bodies and commands are copied
> from the lab. The section assigned the **Conventional** arm this block (Section A) runs §5
> instead of this table.

Kick-off, exactly as the README's "Run it" block has it:

```bash
cd labs/lesson07b-cloudtrail-monitoring
docker compose up -d --build     # vulnerable_app.py on :8111, fixed_app.py on :8112
pip install requests             # once, on the host
python3 exploit.py
```

| Suggested | Task | Student does (exact from lab) | Evidence produced |
|---|---|---|---|
| 0:00–0:06 | **Stand it up** | `cd labs/lesson07b-cloudtrail-monitoring` → `docker compose up -d --build`. Vulnerable on `:8111`, fixed on `:8112`; both containers listen on `5000` internally | `GET /ping` on both — `{"mode":"vulnerable",…}` and `{"mode":"fixed",…}` |
| 0:06–0:12 | **Read the endpoint** | One `POST /login-attempt` by hand with the README's documented body `{"username": "admin7", "success": false, "source_ip": "203.0.113.20"}`; note the response fields `alert`, `count_for_key`, `note` and the threshold of 3 | The request/response pair and the value of `note` on each app |
| 0:12–0:25 | **The spray that never alerts (vulnerable, `:8111`)** | Send the rotating-username spray from **one** `source_ip` — `exploit.py` uses usernames `admin1`…`admin20` and a `source_ip` drawn once per run from `203.0.113.1`–`203.0.113.254`. Watch `count_for_key` stay at **1** on every attempt | Worksheet 2a: the exact request sequence, and confirmation that after **20** attempts the app still had not alerted and returned no flag |
| 0:25–0:33 | **Negative control (still `:8111`)** | Send the **same** username three times from the same `source_ip`. The vulnerable app *does* alert (`"alert": true`) — but returns **no** flag | The three responses; a one-line statement that the counter works and the *key* is the defect |
| 0:33–0:42 | **Confirm the fix (`:8112`)** | Replay the identical rotating-username spray against the fixed app. `count_for_key` now climbs 1 → 2 → 3 and the alert fires on the **3rd** attempt, `reason` naming the `source_ip` "(usernames vary)" | Worksheet 2a: the attempt number the alert fired on + the captured flag |
| 0:42–0:47 | **One-shot check (optional)** | `python3 exploit.py` — expect two `PASS` lines and exit `0`. Read §9 first if the containers have already served this `source_ip` | The two PASS lines |
| 0:47–0:60 | **EiPE + submit** | Draft worksheet **2b**: 3–4 sentences a non-technical stakeholder could follow on why per-`(source_ip, username)` counting lets a spray attacker hide in plain sight, and the general grouping principle beyond this lab | Worksheet 2a request/response pairs + 2b answer → Classroom |

**Formative checkpoints.**
- A student whose vulnerable-app run alerts (or whose fixed-app run alerts on attempt 1 or 2) is
  almost always re-using a `source_ip` the still-running container has already counted. The
  counters are plain in-memory dictionaries with no evaluation window and no reset endpoint — see
  §9 for the two recoveries.
- A student who gets `400 {"error": "username and source_ip are required"}` has omitted one of the
  two required body fields; `success` is optional and is treated as false when absent.
- A student who concludes "the vulnerable app's alerting is broken" has missed the point of the
  negative control. Send them back to 0:25–0:33: it alerts perfectly well — for the wrong attack.

## 5. Conventional-arm variant (same slot, no flag) — Section A this block

Per the worksheet header, Block 2 reverses Block 1's assignment: **Section A = Conventional**,
**Section B = AIR-Sec**. The Conventional arm does **worksheet Part 1 only** — five essay questions
on the same concepts: the stage-by-stage role of CloudTrail / CloudWatch / EventBridge; what an
aggregation key is and how two choices over the same log data change what is counted; password
spray versus classic brute force and why both need different aggregation logic; whether a control
keyed on *username* alone would catch a one-IP/20-username spray and whether it would catch
credential stuffing of one username from 20 IPs; and why an aggregation-key choice is a security
bug rather than a tuning issue. No Docker target, no per-student flag, no AI-resilience layer —
graded on the writing itself. Use the slot for guided discussion of those five questions; the
exploit is not run in this arm.

## 6. Assessment

| Instrument | Evidence | Outcome | Notes |
|---|---|---|---|
| Worksheet Part 2a (AIR-Sec arm) | The exact `POST /login-attempt` sequence against `:8111` + confirmation of no alert after 20 attempts; then the `:8112` sequence, the alert attempt number, and the flag | K3, P2, P4, A2 | Part of the worksheet mark |
| Worksheet Part 2b — **EiPE** (AI-resilient) | 3–4 plain-English sentences on hiding in plain sight + the general grouping principle | K2, K4, A3, CLO4 | The AI-resilient task for this lesson |
| Worksheet Part 1 (Conventional arm) | Five essays | K1–K4 | The Conventional arm's whole submission |
| **Per-student flag** | The `flag` value returned once the **fixed** app's alert fires | A2 | Integrity control (also carries marks) — but see the caution below |
| Live check (optional) | Reproduce the negative control and explain why it alerts while the 20-attempt spray does not | P3, K4 | Under SUBMISSION.md "Random live checks"; there is no worksheet viva part in this lesson |

**Per-student flag.** Mint with `python3 instructor/seed_flags.py env <STUDENT_ID>` — verified
working from this repo; this course's shim forwards to the curriculum monorepo's shared
`tools/seed_flags.py`, whose challenge-key vocabulary comes from the course manifest rather than a
hand-maintained list, and it emits this lesson's `FLAG_MONITOR`. Without a mint, `docker-compose.yml`
supplies a public default placeholder to the **fixed** service only, overridable per build
(`FLAG_MONITOR=FLAG{...} docker compose up`). Flags are per student and salted, so a copied flag is
traceable to the student it was issued to.

> **⚠ Instructor caution — the flag is weaker evidence here than in the other labs.** Unlike every
> other lab in this course, the flag in lesson 07b is emitted by **`fixed_app.py`**, and
> `vulnerable_app.py` never emits one (the vulnerable service simply receives no `FLAG_MONITOR` in
> `docker-compose.yml`; both files read the same `os.environ.get("FLAG_MONITOR")`). That inverts
> the convention asserted in course specification §9 and in this repo's `CLAUDE.md`. The practical
> consequence: any three `success: false` POSTs sharing one self-chosen `source_ip` (any value, any
> usernames) sent to `:8112` yield the flag, without the student ever touching the vulnerable app —
> the fixed app keys its counter by `source_ip` alone, so three POSTs spread across *different*
> `source_ip` values each stay at `count_for_key: 1` and never alert. **Grade the vulnerable-side
> evidence** — the 20-attempt sequence with `count_for_key` pinned at 1, and the negative control —
> not the flag on its own. See §11.

**Deliverable (worksheet).** The captured flag + the attempt number it appeared on + a
one-paragraph explanation of why `(source_ip, username)` is the wrong aggregation key for detecting
a password spray, while `source_ip` alone correctly catches it.

## 7. Materials

- Lab folder `labs/lesson07b-cloudtrail-monitoring/`: `README.md`, `worksheet.md`,
  `vulnerable_app.py` (`:8111`), `fixed_app.py` (`:8112`), `exploit.py`, `docker-compose.yml`,
  `Dockerfile` (`python:3.12-slim`), `requirements.txt` (`flask>=3.1.3`, `requests>=2.33.0`).
- Docker Desktop; `pip install requests` on the host for `exploit.py`.
- `exploit.py` knobs, if you want to vary the exercise: `VULN_URL`, `FIXED_URL`, `ATTEMPTS`
  (default `20`), `SOURCE_IP`.
- Instructor: `instructor/seed_flags.py` (git-ignored) and the answer key
  `instructor/lesson07b-cloudtrail-monitoring-answer-key.md`.
- Rules of engagement: [ETHICS.md](../../ETHICS.md) · Submission: [SUBMISSION.md](../../SUBMISSION.md)
- Slides: ⬚ (none in repo).
- References the lab cites (all publicly available, no AWS Academy file used or copied): AWS
  CloudTrail docs *Logging AWS API and console sign-in events*; AWS CloudWatch docs *Creating
  metric filters and alarms for log data* (specifically the aggregation/dimension-key concept for a
  custom metric); AWS EventBridge docs *Event patterns and rules for routing to a target*.

## 8. Where the simulation departs from real AWS (say this out loud)

- **Reset-on-success is a lab simplification, and it is the one most likely to mislead.** Here a
  `{"success": true}` POST clears that key's failure streak. A real CloudWatch metric filter is a
  *stateless* counter of matching failure events, and its alarm sums those over a fixed evaluation
  window: a success simply produces no datapoint — it does not zero or pause the count, so failures
  on either side of an intervening success inside the same window still add up. Real
  reset-on-success would need custom logic, for example an EventBridge → Lambda rule (README; both
  app files carry the same note in comments).
- **There is no evaluation window at all in this lab.** The counters are module-level Python dicts
  that persist for the container's lifetime, so "3 failures" means three failures *ever*, not three
  within a period. A real alarm's threshold is inseparable from its period — that pairing is absent
  here.
- **`source_ip` is self-asserted in the JSON body.** The client tells the service which address it
  is coming from. Real CloudTrail records the source IP address itself as part of the event; an
  attacker cannot simply declare it. Do not let students leave thinking the aggregation key is
  attacker-controlled input.
- **EventBridge and SNS subscription mechanics stay conceptual** in this add-on — nothing is routed
  or delivered anywhere; the "alert" is a field in an HTTP response (`course-plan.md`). The routing
  and notification stages are exercised in the Learner Lab, not here.

## 9. Risks and contingencies

| Risk | Mitigation |
|---|---|
| **Re-running `exploit.py` against still-running containers can fail its own assertions.** Verified on this machine: with the same `source_ip` a second time, the fixed app alerts on attempt **1** and `assert fixed_alerted_at == 3` fails; a third time, the vulnerable app alerts on attempt **1** and `assert vuln_alerted_at is None` fails | State lives in in-memory dicts for the container's lifetime. Either `docker compose down` then `docker compose up -d --build` again, or send a `{"success": true}` POST for that `source_ip` first (one per `(ip, username)` pair on the vulnerable app, one per IP on the fixed app). Do **not** pin `SOURCE_IP` for repeat demos |
| The randomised `source_ip` is drawn from only 254 values, so repeated runs on one machine can collide by chance and trigger the failure above | Tear the containers down between demo runs rather than relying on the draw; set a deliberately fresh `SOURCE_IP` if you must keep them up |
| `pip install requests` fails on an externally-managed host Python (no venv) | `exploit.py` is optional. The whole worksheet flow is reachable by hand — `curl -s -X POST http://localhost:8111/login-attempt -H 'Content-Type: application/json' -d '{"username":"admin7","success":false,"source_ip":"203.0.113.20"}'` — verified working against both ports |
| Slow/failed pull of `python:3.12-slim` or `pip install` during `docker compose up -d --build` in class | Pre-build before the session; keep an offline image copy (`docker save`/`docker load`) |
| Ports `8111`/`8112` already bound | Nothing else in `labs/` uses them; `docker compose down` this lab if it is already up, or free the unrelated host process |
| A student "captures" the flag without doing the exercise — three failed POSTs to `:8112` sharing one self-chosen `source_ip` suffice | Grade the **vulnerable**-side evidence (20 attempts, `count_for_key` never above 1) plus the negative control; per-student salted flags still make a *shared* flag traceable. See §6's caution and §11 |
| A student concludes the vulnerable app's detection code is simply broken | Run the negative control with them: same username ×3 from one IP on `:8111` returns `"alert": true`. The mechanics are sound; the key is wrong |
| A student mistakes the lab's reset-on-success for real CloudWatch behaviour | Address it explicitly at the point it is observed — §8, first bullet |
| A student wants to test spray detection against real infrastructure | Out of bounds — only the local lab and the student's own Learner Lab are approved targets (ETHICS.md). Attempted logins against real AWS endpoints can suspend the whole class's Learner Lab access |

## 10. Post-teaching reflection

*Complete after the session — this also feeds the course's engagement data.*

- Attendance / completion: ⬚
- Time actually taken per segment (vs. the 45–60 min envelope): ⬚
- Where the class got stuck (stale counter state from a re-run? the meaning of `count_for_key`?
  the negative control?) and what unblocked them: ⬚
- Misconception that showed up in the **EiPE (2b)** answers — did students reach the general
  grouping principle, or only restate this lab's fix?: ⬚
- Did anyone leave believing real CloudWatch resets on success, or that CloudTrail takes the source
  IP from the client?: ⬚
- Anything to change before this add-on runs again: ⬚

## 11. Instructor notes — content issues to raise, not to patch here

These are defects in lab/spec content, recorded here rather than edited, because lab files are
under a byte-parity gate with the curriculum monorepo and changing graded material to suit a
lesson plan is not an acceptable fix.

1. **`labs/lesson07b-cloudtrail-monitoring/exploit.py` comment and README claim state isolation
   that does not hold.** The comment says the randomised per-run IP means "repeated local runs
   against the same containers don't accumulate state across runs". Reproduced on this machine:
   with a colliding or pinned `SOURCE_IP`, run 2 fails `assert fixed_alerted_at == 3` and run 3
   fails `assert vuln_alerted_at is None`. Until the lab gains a reset route or per-run isolation,
   teach the tear-down workaround in §9.
2. **The README's `FLAG_MONITOR` paragraph (≈ lines 119–122) is misleading.** It implies the flag
   must be set explicitly to exercise the fixed app's alert-then-flag path; `docker-compose.yml`
   already supplies a public default to the `fixed` service, and the path works with nothing set.
   The two apps' code is identical on this point — the difference is purely which service receives
   the environment variable.
3. **Course specification §9 and `CLAUDE.md` both assert that the control ("fixed") app never emits
   a flag. That is false for this lesson by design** — here the fixed app is the one that alerts,
   so it is the one that emits. The design is coherent (the finding is the *absence* of an alert on
   the vulnerable side), but the blanket rule needs an explicit exception, and the assessment
   consequence in §6 needs to be honoured in grading.
