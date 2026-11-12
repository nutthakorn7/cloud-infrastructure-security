# Lesson Plan — Lesson 6: Load Balancing & Auto-Scaling Under Load

> **Current delivery policy (2026-11-11):** Students update the public repo and run this lab
> without a personal `.env`. Any `FLAG{…}` is a shared demo marker. Grade complete
> request/response evidence, explanation, and a viva spot-check.

| | |
|---|---|
| **Course** | Cloud Infrastructure & Security · 02005097 (`README.md`, `course-plan.md`) |
| **AWS lesson this attaches to** | AWS Academy **Cloud Foundations Lab 6** — load balancing & auto-scaling (topic only; no AWS Academy file is used or copied) |
| **Kind** | **HYBRID** — Part 1 conceptual essay + Part 2 small lab (`labs/lesson06-load-balancing-autoscaling/README.md`) |
| **Block** | Block 1 (`docs/course-specification.md` §6) |
| **Duration** | **45–60 min local work across Weeks 09–10**, started after the AWS lab in the Week 09 class (lab README, "This lesson — what to do") |
| **Lab folder** | `labs/lesson06-load-balancing-autoscaling` |
| **Slides / quiz** | Original [Week 09 course bridge](../../slides/weekly-bridges/output/Week09_Cloud_Course_Bridge.pptx); AWS Module 10 slides and Knowledge Check remain primary |
| **Standards** | **CWE-400** (Uncontrolled Resource Consumption) · OWASP **API4:2023 Unrestricted Resource Consumption** (both named in the lab README) |
| **CLOs addressed** | **CLO2** demonstrate · **CLO3** apply the control (spec §6 row). Task 2b is an *EiPE*, which spec §4 maps to **CLO1/CLO4** — see §9 note |
| **Semester / section / room / grading scale / PLOs** | ⬚ |

> **Cross-reference note.** The curriculum monorepo schedules this lesson as
> **slot 4** (`courses/cloud-infrastructure-security.yml`), rendered "Lesson 4". The renumbering is
> deliberate and documented in `tests/test_parity_cis.py`. In *this* repository it is Lesson 6, after
> the AWS lab it attaches to.

> **Plainer worksheet and Step-by-step (owner, 2026-11-04).** KOSEN students come through an
> accelerated high-school track, so the worksheet was reworded into short, concrete questions, and
> students may answer in Thai or English on the Local05 Answer Sheet (no PDF). The lab README gained
> a copy-paste **Step-by-step** (steps 0–9, every command run as written on 2026-11-04). The change
> applies to both Parts equally: the same five Part 1 questions asking for the same points, 2a
> asking for the same evidence in labelled pieces, 2b and 2c with the same meaning, the same point
> split. Mark the reasoning, not the language.

---

## 1. Session objectives

By the end of this add-on a student can:

**Knowledge (K)**
- K1 — Explain, in their own words, how a **load balancer**, its **target group(s)** and an
  **Auto Scaling Group** work together to keep a fleet sized to demand, and what capability is lost
  if the balancer routes straight to instances with no target group in between.
- K2 — State what an ASG's **minimum** and **maximum** capacity settings each exist for — an
  availability floor and a **cost ceiling** — with one concrete failure scenario for each.
- K3 — Define **"Denial of Wallet"** (economic denial-of-service) and distinguish it from a
  traditional DoS whose goal is unavailability.
- K4 — Explain why a publicly reachable, unauthenticated, unthrottled load-triggering endpoint is a
  **security** problem (CWE-400), and why "just add auth" or "just add rate limiting" is each
  individually insufficient.

**Skills (P)** *(AIR-Sec arm — the arm that runs the container)*
- P1 — Stand both targets up and read baseline state from `GET /status` on each.
- P2 — Drive `current_instances` from the simulated minimum to the simulated maximum with anonymous
  `POST /generate-load` calls against the vulnerable app on `:8109`, and capture the response.
- P3 — Show the identical anonymous request rejected with `401` on the fixed app on `:8110`, then
  show what a *correctly-keyed* caller gets on repeated calls (`429`).
- P4 — Record the exact request pattern — endpoint, method, headers-or-lack-thereof, approximate
  call count — as attributable evidence.
- P5 — Reason about the blast radius of **one** leaked API key against this fixed design.

**Attitude (A)**
- A1 — Attack only the two approved targets: the local Docker labs in `labs/`, and their own AWS
  Academy Learner Lab sandbox ([ETHICS.md](../../ETHICS.md) rule 1).
- A2 — Submit their own complete request/response evidence and explanation, and be able to
  reproduce and explain the result in a viva spot-check. The shared demo flag is not identity
  evidence ([SUBMISSION.md](../../SUBMISSION.md), "Academic Integrity & Anti-Cheating").
- A3 — Treat a cloud bill as an attack surface: "it scaled, so it worked" is not a security verdict.

## 2. Key idea (the through-line)

Nothing in this lab is a code bug. `POST /generate-load` does exactly what it was built to do — the
vulnerability is entirely in what it **does not check** before doing expensive work. Every accepted
request buys the caller a little more of someone else's capacity, and the fleet obediently grows to
its configured maximum. That makes the interesting question not "where is the flaw in the code?" but
"who is allowed to spend this money, and how fast?" — which is why the fix has to be *two* controls
(identity **and** rate), not a cleverer one.

## 3. What students must have completed first

1. **Before the Week 09 class:** study Cloud Foundations Module 10 and complete its Knowledge
   Check. During that class, run the assigned AWS load-balancing / auto-scaling lab in the Learner
   Lab before starting the local work. This matches the Classroom 10 + 30 + 45 + 15 minute flow.
2. **Docker Desktop working** on the student's own machine (SUBMISSION.md, one-time setup).
3. **Signed ethics acknowledgment** from Lesson 1 (ETHICS.md).

**Instructor, before class**
- Preflight the instructor demonstration on the instructor machine with
  `docker compose up -d --build` in the lab folder, then `docker compose down`. Students build
  their own local copy; allow for a first-time image download during the Week 09 local slot.
- Announce **which worksheet Part this section is doing** before the local work starts — see
  §8, risk 1. Do not send a personal `.env` or seed individual flags for Local 05.
- Read the instructor key: `instructor/lesson06-load-balancing-autoscaling-answer-key.md`
  (`instructor/` is git-ignored; never paste it into a public file).

## 4. Local 05 work plan — 55 min across Weeks 09–10

> The minute split below is **this plan's own allocation** for 55 minutes of local work. Start
> this sequence after
> the AWS lab in Week 09, using that week's 45-minute local-work slot; finish the remaining
> writing and submission in Week 10. This table is the **AIR-Sec** delivery; §5 covers the
> Conventional delivery of the same Local.

| Time | Task | Student does | Evidence produced |
|---|---|---|---|
| 0:00–0:05 | **Bridge from the AWS lab** | Recall from the Learner Lab: what the target group held, where min/max/desired capacity was set. Frame today's question: who may trigger scaling, and how often? | — |
| 0:05–0:12 | **Stand up the targets** | README Step-by-step steps 0–3: no personal `.env`; `docker compose up -d --build` (vulnerable on `:8109`, fixed on `:8110`); `GET /status` on both — `current_instances` 2, `load_units` 0 | Baseline response |
| 0:12–0:27 | **Worksheet 2a (i) — the attack** | Loop anonymous `POST /generate-load` against the vulnerable app until `current_instances` reaches the simulated maximum. Step-by-step step 4: a 40-call `curl` loop (`exploit.py` is an optional self-check) | Complete request pattern, call count and vulnerable response; any flag is a shared marker |
| 0:27–0:37 | **Worksheet 2a (ii) — the control** | Same anonymous request against `:8110` → `401`. Then repeat with the correct `X-Api-Key` (value is in the lab's own `docker-compose.yml`; Step-by-step steps 6–8) until the response changes to `429`, and re-check `GET /status` | Both responses + the fixed app's `/status` afterwards |
| 0:37–0:45 | **Week 09: compare and stop** | Check that the fixed fleet did not scale like the vulnerable one, record the responses, and run `docker compose down` before leaving | Complete trace; local containers stopped |
| 0:45–0:50 | **Week 10: worksheet 2b — EiPE** | Explain why an API key alone and "just add more instances" are insufficient, in 3–4 short sentences a nontechnical reader can follow | Written answer |
| 0:50–0:53 | **Week 10: worksheet 2c — blast radius** | One valid key leaks: state the maximum accepted calls before cutoff and why that bounds damage | Written answer |
| 0:53–0:55 | **Week 10: submit** | Fill in the Local05 Answer Sheet copy in Classroom and Turn in by 11 Jan 2027, 23:59; no PDF | Submission |

**Checks for understanding**
- After 2a(i), cold-call: *"nothing crashed and no error was returned — so what exactly did the
  attacker take?"* (Answer to steer towards: capacity and money, not availability.)
- After 2a(ii), before anyone writes 2b: *"the fixed app rejected you at call 1. Which of the two
  controls did that, and would the other one alone have stopped you?"*

**Do not put the keyed call-count on the projector.** Worksheet 2c asks students to derive the
worst-case number of calls a leaked key buys; that number is `RATE_LIMIT_MAX_CALLS` and students are
meant to read it off **their own terminal** in 2a(ii). Demonstrate the mechanism at the front only
after 2c is written, or answer it for them.

## 5. Conventional delivery of the same slot

The counterbalanced section does **Part 1 only** — five short-answer questions (2–4 sentences each,
Thai or English), no container, no flag
(worksheet, "Submit"). Spread the local writing across Weeks 09–10:

- 0:00–0:10 — bridge from the AWS lab; the load balancer / target group / ASG relationship (Q1) and
  min-vs-max capacity (Q2, Q3) discussed at the board.
- 0:10–0:20 — instructor demonstrates the anonymous hammer on the projector so the concept is
  concrete; students do not run containers in this arm.
- 0:20–0:45 in Week 09 — students start Q1–Q5.
- Week 10 — finish and submit the Local05 Answer Sheet by 11 Jan 2027, 23:59.

Marking is on the writing itself; there is no AI-resilience layer and no flag in this arm.

## 6. Where the simulation departs from real AWS behaviour

Say each of these out loud — CLAUDE.md makes it a house rule, so that no one leaves with a wrong
model of the real service.

| The simulation | The reality it stands in for |
|---|---|
| `scaler.py` is, in its own words, "deterministic, synchronous, no timers, no real AWS calls". A request returns the *already-scaled* state. | Real scaling is asynchronous — an alarm fires, an instance launches, warms up and passes health checks before it serves traffic. Cooldowns and health checks have no representation here. |
| There is no load balancer and no target group in the code at all — a single Flask process holds a counter that plays the role of `current_instances`. | The ALB / target-group registration and de-registration behaviour is learned in the AWS Learner Lab, not here. |
| The scaler only ever counts **up**: `generate_load()` increments, and there is no decrement path and no reset endpoint. `MIN_INSTANCES` is only ever the starting value. | A real ASG also **scales in** when load drops; the minimum is a floor that is genuinely exercised, not just an initial value. |
| The throttle in `fixed_app.py` is, per its own comment, a "fixed lifetime call-count cap per API key, tracked in memory" — once a key's budget is spent it is refused until the process restarts. | Real API throttling is time-windowed / refilling. A student must not leave believing that a rate limiter permanently bricks a credential. |
| `MIN_INSTANCES`, `MAX_INSTANCES` and `UNITS_PER_INSTANCE` are module constants in `scaler.py`. | An ASG's min/max/desired are per-deployment configuration, changeable without touching code. |
| A single static shared key in an environment variable is the whole identity model. | Choosing the actual production control set is out of scope for this simulation and belongs to the AWS baseline. |
| "Expensive" is asserted, never computed — no instance-hour price appears anywhere in the lab. | The cost argument in the worksheet is qualitative by design. |

## 7. Assessment for this lesson

| Instrument | Evidence | Outcome | Weight |
|---|---|---|---|
| Worksheet Part 2a (AIR-Sec) | Request pattern, call count, vulnerable response, both fixed-app responses | P1–P4, K4 | Part of this layer's worksheet mark — ⬚ (spec §4) |
| Worksheet Part 2b — *EiPE* | Written 3–4 sentence explanation | K4, CLO4 | as above |
| Worksheet Part 2c — blast radius | Written answer | P5, K4 | as above |
| Worksheet Part 1 (Conventional arm) | Five short answers | K1–K4 | as above |
| **Shared demo marker** | A `FLAG{…}` may appear in the vulnerable response at maximum simulated capacity | — | Not identity evidence and not graded by itself |
| Viva / random live check | Live reproduction and explanation | P1–P4, A2 | Pass / flag for follow-up (SUBMISSION.md) |

**How the marker works here.** The public `docker-compose.yml` supplies a shared demonstration
`FLAG_SCALING` value. Only the vulnerable app emits it after `current_instances` reaches the
configured maximum. Any student can read that value in the public repository, so possession of
it proves nothing about who ran the lab. Mark the complete request/response trace, explanation
and viva spot-check; do not send or require a personal `.env`.

Grading detail lives in the worksheet's own submission rules and the instructor key. Partial credit
where the mechanism is explained correctly but the run was not completed.

## 8. Risks and contingencies

| Risk | Mitigation |
|---|---|
| **Arm confusion.** The worksheet header now states the Block 1 arms both ways (Section A = AIR-Sec, Section B = Conventional) and the README's "This lesson" step 3 now agrees (fixed 2026-11-04, §9 notes 1–2), but a student can still do the wrong Part in good faith. | Announce, in class and in the Classroom post, which Part **this section** is doing today. Do not let students infer it from the worksheet header. |
| **Scaler state is cumulative and in-process.** Any exploration before the timed run inflates `load_units`, and a second run returns the shared marker on call 1 rather than ~40. Nothing resets it from outside. | Verified on this machine: `docker compose restart vulnerable` returns `/status` to `current_instances` 2, `load_units` 0. Restart before a demo or a re-attempt, and mark the *reasoning*, not the exact call count. |
| **The fixed app's key budget is a lifetime counter.** A student who spends it while poking about gets `429` on every later keyed call, including the one they meant to screenshot. | `docker compose restart fixed` (same mechanism as above). |
| **Optional Python self-check needs `requests`.** Installing it into the host Python can fail under PEP 668. | The README now uses a Git-ignored `.venv/` for macOS/Linux and Windows Git Bash. The required Step-by-step uses only Docker and `curl`; skip `exploit.py` if Python setup is unavailable. |
| **Host ports 8109 / 8110 already bound.** | `exploit.py` reads `VULN_URL` and `FIXED_URL` from the environment, so a student who remaps published ports can point it at the new ones without editing the script. Prefer that to editing `docker-compose.yml` — the lab files are covered by the monorepo parity gate. |
| **First-time image build inside a 45–60 min slot** (`python:3.12-slim` pull + Flask install) eats the lab. | Pre-build during the AWS Learner Lab portion, or ask students to run `docker compose up -d --build` the night before. |
| **The AWS Learner Lab overruns** and swallows the add-on. | Fall back to the §5 shape: demonstrate the anonymous hammer at the front, set 2b and 2c as homework, and have students run 2a on their own machines before the next session. |
| **Copied marker or trace.** The shared marker is public, and a student could copy another response. | Require the full command and vulnerable/fixed responses, check the explanation, and spot-check with a live reproduction or viva. Do not treat the marker alone as evidence. |
| **Someone points the loop at a real endpoint.** The technique is trivially portable and would be a genuine offence. | Re-state ETHICS.md rules 1–2 at the start: local labs and the student's own Learner Lab only — "not even to 'look'". |

## 9. Instructor notes on lab-content issues (do not fix inside a worksheet mid-term)

Three inconsistencies in this lesson's own materials were flagged rather than edited (notes 1 and 2 were fixed on 2026-11-04, with the plainer worksheet). Keep any student-facing lab edit aligned
with the curriculum monorepo copy; changes to assessed answers also require the instructor key
to be updated (repo CLAUDE.md). The monorepo copy carries the documented renumbering substitutions
in `tests/test_parity_cis.py`.

1. **Fixed 2026-11-04 — who does Part 1.** The lab README said "Part 1 essay for everyone; Part 2
   AIR-Sec students also submit the flag", which contradicted the worksheet's "complete only the
   part assigned to you this block". README step 3 now says the Conventional room does Part 1 and
   the AIR-Sec room does Part 2, matching the worksheet. The public flag is a shared demo marker.
2. **Fixed — block → arm.** This note quoted an older worksheet header that stated the
   block→arm mapping as fixed for every section. The header now reads "Section A = Block 1 AIR-Sec;
   Section B = Block 1 Conventional", which is right for this Block 1 lesson.
3. **Fixed declared duration.** `lesson.yml` in the monorepo now records `duration_min: 60` for
   this local add-on, matching the lab README's 45–60 minutes. The complete weekly meeting remains
   100 minutes.

Also noted: spec §6 assigns this row CLO2 and CLO3, while spec §4 maps *EiPE* tasks to CLO1/CLO4 —
task 2b is an EiPE, so the row understates its own CLO coverage.

## 10. Materials

- Lab: `labs/lesson06-load-balancing-autoscaling/` — `README.md`, `worksheet.md`, `scaler.py`,
  `vulnerable_app.py`, `fixed_app.py`, `exploit.py`, `docker-compose.yml`, `Dockerfile`,
  `requirements.txt`
- Instructor key: `instructor/lesson06-load-balancing-autoscaling-answer-key.md` (git-ignored)
- Shared demonstration marker: `FLAG_SCALING` in the public `docker-compose.yml`; no personal
  `.env` is distributed or needed for Local 05.
- Optional macOS/Linux self-check after standing up the targets (students follow the README's Step-by-step; Windows Git Bash commands are in that README):
  ```bash
  cd labs/lesson06-load-balancing-autoscaling
  docker compose up -d --build
  python3 -m venv .venv
  .venv/bin/python -m pip install requests
  .venv/bin/python exploit.py
  ```
- References the lab itself cites: AWS Elastic Load Balancing documentation (*What is a target
  group?*, *Application Load Balancer components*); AWS Auto Scaling documentation (*Auto Scaling
  group concepts* — minimum, maximum, desired capacity, scaling policies); OWASP *API4:2023
  Unrestricted Resource Consumption*. All publicly available; **no AWS Academy file is used.**
- Rules of engagement: [ETHICS.md](../../ETHICS.md) · Submission: [SUBMISSION.md](../../SUBMISSION.md)

**Reproduced on 2026-07-26** on the instructor machine, from a freshly built stack: the anonymous
loop drove `current_instances` to the maximum on call 40 and the response carried the shared marker; the same
anonymous request against the fixed app was refused at call 1 with `401`; `exploit.py` printed both
`PASS` lines and exited `0`. Separately confirmed: a correctly-keyed caller gets exactly
`RATE_LIMIT_MAX_CALLS` accepted calls — `current_instances` never leaves 2 — and then `429`.

## 11. Post-teaching reflection

*Complete after the session — this also feeds the course's engagement data.*

- Attendance / completion: ⬚
- Which arm this section ran, and whether anyone did the wrong Part: ⬚
- Time actually taken per task (vs. the allocation in §4): ⬚
- How many students had to restart a container mid-task, and why: ⬚
- Whether the *EiPE* answers separated "authentication" from "rate limiting", or blurred them: ⬚
- Did anyone argue the endpoint "isn't really a vulnerability because nothing broke"? How was it
  resolved?: ⬚
- Misconceptions about real ASG behaviour traceable to the simulation (§6): ⬚
- Anything to change before this lesson runs again: ⬚
