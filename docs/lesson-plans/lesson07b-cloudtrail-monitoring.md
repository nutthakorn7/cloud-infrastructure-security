# Lesson Plan — Lesson 7 (2nd topic): CloudTrail + CloudWatch + EventBridge Monitoring

> **Current delivery policy (2026-11-11):** Week 17's 100-minute class is AWS Academy
> Module 6 and Lab 6.1. Local 09 follows outside class. C5R2 completes Part 1 without
> Docker; C5R1 completes Part 2 using the public Docker lab on each student's machine.
> No personal `.env` or per-student flag is distributed. The marker is shared and earns
> no points by itself. Grade the full evidence, explanation and viva when needed.

*CLOUD add-on. The AWS Academy Learner Lab teaches logging, monitoring and alerting first.
Its security-group event case differs from our local failed-login simulation. No AWS Academy
material is reproduced here; the bridge and simulation are described in our own words.*

| | |
|---|---|
| **Course** | Cloud Infrastructure & Security · subject code **02005097** |
| **Attaches to (AWS lesson)** | AWS Academy Cloud Security Foundations Module 6 and Lab 6.1, *Monitoring and Alerting with CloudTrail and CloudWatch*. The lab covers CloudTrail delivery, SNS subscription, an EventBridge rule for security-group changes, a CloudWatch metric filter/alarm, and Logs Insights. The local failed-login case is a separate transfer exercise. |
| **Kind** | HYBRID — small Docker lab for the aggregation-key concept; EventBridge/SNS subscription mechanics stay conceptual (`course-plan.md`) |
| **Block** | 2 |
| **Delivery** | Week 17 class: 10-minute briefing, 75-minute AWS lab, 15-minute debrief. Local 09: 45–60 minutes outside class after the AWS lab, due Mon 1 Mar 2027 at 23:59. |
| **Lab folder** | `labs/lesson07b-cloudtrail-monitoring` |
| **Slides** | Original [Week 17 course bridge](../../slides/weekly-bridges/output/Week17_Cloud_Course_Bridge.pptx); AWS Module 6 slides remain primary |
| **Analogous bug class** | CWE-778 (Insufficient Logging) **adjacent** / detective-control logic error — "the control exists and runs, but its aggregation key silently excludes the real attack shape" (lab README) |
| **CLOs addressed** | **CLO2** demonstrate the misconfiguration · **CLO3** apply the correct control and verify empirically (course spec §6 row for this lesson) |

> **Assessment:** Local 09 is 6 of the 60 Local points (Technical 5,
> Interdisciplinary 1). AWS-graded work is separate. C5R2 is the Conventional arm;
> C5R1 is the AIR-Sec arm.

> **Plainer worksheet and Step-by-step (owner, 2026-11-04).** KOSEN students come through an
> accelerated high-school track, so the worksheet was reworded into short, concrete questions and
> students may answer in Thai or English (2–4 sentences each) on the **Local09 Answer Sheet** copy
> in Classroom, with no PDF. The change applies to both Parts equally: the same five Part 1
> questions asking for the same points, 2a asking for the same two things, 2b with the same
> meaning, the same point split. The README gained a copy-paste **Step-by-step** (steps 0–6: the
> 20-attempt spray on `:8111` from `203.0.113.20`, the same spray on `:8112`, then the same-username
> control on `:8111` from `198.51.100.7`), run as written on 2026-11-04; its kickoff is now
> `docker compose up -d --build`. Mark the reasoning, not the language.

---

## 1. Session objectives

By the end of this add-on a student can:

**Knowledge (K)**
- K1 — Distinguish a CloudTrail → CloudWatch Logs → metric filter/alarm path from a
  separate EventBridge event-routing path to a target such as SNS. They need not form
  one serial pipeline (worksheet Part 1 Q1).
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
- A2 — Submit reproducible request/response evidence and explain it in the student's
  own words on the Classroom Answer Sheet. A shared marker does not establish identity.
- A3 — Explain the result in plain language and disclose AI use on the Answer Sheet
  (worksheet Part 2b; course spec CLO4).

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

**Students first complete Week 17's AWS work in their own Learner Lab.** Lab 6.1 uses
CloudTrail, CloudWatch Logs, EventBridge, SNS, metric filters/alarms and Logs Insights
for monitoring; its event example is a security-group change, not the local
failed-login case. The AWS module, lab, Week 17 bridge slide 5 and the student
README's concept bridge teach the additional aggregation-key reasoning before
the worksheet is due.

**For Local 09 after class:** C5R2 needs the README and Answer Sheet only. C5R1
needs Docker Desktop and `curl` on each student's own computer; the student
downloads or updates the public repo. No instructor-hosted target, pre-built
instructor container, personal `.env`, or private flag distribution is needed.
The optional `exploit.py` requires `requests` on the host; the assessed steps
use only `curl`. Students should check that ports 8111 and 8112 are free locally.

## 4. Minute-by-minute add-on (AIR-Sec arm — Section B this block)

> **Pacing note.** The 45–60 minutes below are a suggested self-paced Local 09
> sequence **outside** the 100-minute Week 17 AWS class. C5R2 uses §5 instead.

Kick-off: students follow the README's **Step-by-step** (steps 0–6), which starts with
`docker compose up -d --build` and gives every command with the output to expect. The optional
self-check is the README's "Run it" block (`python3 -m pip install requests`, then
`docker compose restart vulnerable fixed` and `python3 exploit.py`).

| Suggested | Task | Student does (exact from lab) | Evidence produced |
|---|---|---|---|
| 0:00–0:08 | **Start locally** | Update the repo, enter the lab folder, run `docker compose up -d --build`, then `GET /ping` on ports 8111 and 8112. No `.env` is required. | Both apps return HTTP 200. |
| 0:08–0:23 | **Vulnerable spray** | README step 3: 20 rotating usernames from one `source_ip` to `:8111`. | All 20 responses have `alert:false` and `count_for_key:1`. |
| 0:23–0:35 | **Fixed spray** | README step 4: the same sequence to `:8112`. | The first alert is on attempt 3; keep its complete response. The flag is a shared marker. |
| 0:35–0:43 | **Negative control** | README step 5: repeat username `alice` three times from one IP to `:8111`. | The third request alerts, showing the counter works but the grouping misses the spray. |
| 0:43–1:00 | **Explain and submit** | Answer Part 2a and 2b on the Local09 Answer Sheet; clean up with `docker compose down`. | Commands, relevant responses and an explanation; no extra PDF. |

**Formative checkpoints.**
- A student whose vulnerable-app run alerts (or whose fixed-app run alerts on attempt 1 or 2) is
  almost always re-using a `source_ip` the still-running container has already counted. The
  counters are plain in-memory dictionaries with no evaluation window and no reset endpoint — see
  §9 for the two recoveries.
- A student who gets `400 {"error": "username and source_ip are required"}` has omitted one of the
  two required body fields; `success` is optional and is treated as false when absent.
- A student who concludes "the vulnerable app's alerting is broken" has missed the point of the
  negative control. Send them back to 0:35–0:43: it alerts for repeated attempts against one pair.

## 5. Conventional arm (outside class, no Docker) — C5R2

Per the worksheet header, Block 2 reverses Block 1's assignment: **Section A = Conventional**,
**Section B = AIR-Sec**. The Conventional arm does **worksheet Part 1 only** — five short-answer questions (2–4 sentences each, Thai or English)
on the same concepts: the roles of CloudTrail, CloudWatch Logs metric filters and alarms, and EventBridge across log-to-metric and event-routing paths; what an
aggregation key is and how two choices over the same log data change what is counted; password
spray versus classic brute force and why both need different aggregation logic; whether a control
keyed on *username* alone would catch a one-IP/20-username spray and whether it would catch
20 failed attempts for one username from 20 IPs (without inferring stolen credentials); and why an aggregation-key choice is a security
bug rather than a tuning issue. No Docker target or AI-resilience layer is assigned to this
arm; grade its writing. The same-week concept bridge supplies the failed-login case after
AWS Lab 6.1, and students complete this Part outside class before the Local 09 deadline.

## 6. Assessment

| Instrument | Evidence | Outcome | Notes |
|---|---|---|---|
| Worksheet Part 2a (AIR-Sec arm) | The exact `POST /login-attempt` sequence against `:8111` + confirmation of no alert after 20 attempts; then the `:8112` sequence, the alert attempt number, and its complete response | K3, P2, P4, A2 | Part of the worksheet mark |
| Worksheet Part 2b — **EiPE** (AI-resilient) | 3–4 plain-English sentences on hiding in plain sight + the general grouping principle | K2, K4, A3, CLO4 | The AI-resilient task for this lesson |
| Worksheet Part 1 (Conventional arm) | Five short answers | K1–K4 | The Conventional arm's whole submission |
| Shared demo marker | The `flag` field appears only when the **fixed** app's alert fires | P4 | No standalone marks; it does not prove identity or completion |
| Live check (optional) | Reproduce the negative control and explain why it alerts while the 20-attempt spray does not | P3, K4 | Under SUBMISSION.md "Random live checks"; there is no worksheet viva part in this lesson |

**Evidence rule.** The fixed service deliberately emits a public marker when its alert
fires; the vulnerable service never emits one. Any three failures sharing a supplied
`source_ip` can obtain the fixed marker, so it is not proof that a student tested the
vulnerable case. Grade the command/response sequences, reasoning and a live spot-check
when attribution is in doubt. This follows [SUBMISSION.md](../../SUBMISSION.md) and
course specification §9.

**Deliverable (worksheet).** C5R2 answers Part 1 only. C5R1 supplies the vulnerable
and fixed loop commands, the final vulnerable response, the fixed alert attempt and
complete response, plus Part 2b's plain-language explanation. Both use the
**Local09 Answer Sheet** copy in Classroom and click Turn in (no PDF).

## 7. Materials

- Lab folder `labs/lesson07b-cloudtrail-monitoring/`: `README.md`, `worksheet.md`,
  `vulnerable_app.py` (`:8111`), `fixed_app.py` (`:8112`), `exploit.py`, `docker-compose.yml`,
  `Dockerfile` (`python:3.12-slim`), `requirements.txt` (`flask>=3.1.3`, `requests>=2.33.0`).
- Docker Desktop and `curl`. `python3 -m pip install requests` on the host only for the optional
  `exploit.py`.
- `exploit.py` knobs, if you want to vary the exercise: `VULN_URL`, `FIXED_URL`, `ATTEMPTS`
  (default `20`), `SOURCE_IP`.
- Instructor: the private, git-ignored answer key
  `instructor/lesson07b-cloudtrail-monitoring-answer-key.md`; no seeding step.
- Rules of engagement: [ETHICS.md](../../ETHICS.md) · Submission: [SUBMISSION.md](../../SUBMISSION.md)
- Slides: [Week 17 course bridge](../../slides/weekly-bridges/output/Week17_Cloud_Course_Bridge.pptx), after the primary AWS Academy slides.
- References the lab cites (all publicly available, no AWS Academy file used or copied): AWS
  CloudTrail docs *Logging AWS API and console sign-in events*; AWS CloudWatch docs *Creating
  metric filters and alarms for log data* (specifically the aggregation/dimension-key concept for a
  custom metric); AWS EventBridge docs *Event patterns and rules for routing to a target*.

## 8. Where the simulation departs from real AWS (say this out loud)

- **Per-IP or per-username dimensions can be costly in CloudWatch Logs.** The local lab teaches
  the threat-model choice of what to group. In production, CloudWatch Logs warns against
  high-cardinality fields such as IP address as metric-filter dimensions because each distinct
  value creates a separate custom metric and can incur charges; choose an implementation and
  cost guardrails for the actual traffic volume. See [AWS metric-filter dimension guidance](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntaxForMetricFilters.html).
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
| Slow/failed pull of `python:3.12-slim` or `pip install` while a student builds locally outside class | Ask the student to keep the error output and arrange an equivalent local trace or short viva; do not provide an instructor-hosted target |
| Ports `8111`/`8112` already bound | Nothing else in `labs/` uses them; `docker compose down` this lab if it is already up, or free the unrelated host process |
| A student "captures" the shared marker without doing the exercise — three failed POSTs to `:8112` sharing one self-chosen `source_ip` suffice | Grade the **vulnerable**-side evidence (20 attempts, `count_for_key` never above 1), fixed response, explanation and a spot-check when needed; the marker proves nothing about identity. See §6 |
| A student concludes the vulnerable app's detection code is simply broken | Run the negative control with them: same username ×3 from one IP on `:8111` returns `"alert": true`. The mechanics are sound; the key is wrong |
| A student mistakes the lab's reset-on-success for real CloudWatch behaviour | Address it explicitly at the point it is observed — §8, second bullet |
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

## 11. Instructor checks before release

- Check that the Week 17 Classroom material names AWS Module 6/Lab 6.1, reserves the
  100-minute class for AWS work, and assigns Local 09 after class. The attached older
  logging companion must not instruct students to submit in Week 19; the course has
  only 18 scheduled meetings.
- Check that the Local 09 Assignment has 6 maximum points, the six-criterion rubric,
  the correct due date and Answer Sheet copy, and stays Draft until approved.
- On a fresh local Docker run, the vulnerable spray should produce 20 non-alerts;
  the fixed spray should alert first on attempt 3; the vulnerable negative control
  should alert on attempt 3. Stop containers after the check.
- A repeated `exploit.py` run can collide with remembered counters. Restart both
  containers before rerunning or use a fresh address. The lab's IP is supplied in
  JSON and its counters have no time window; neither behavior models real CloudTrail
  or CloudWatch precisely. Real per-IP metric dimensions also have cost and
  cardinality limits.
