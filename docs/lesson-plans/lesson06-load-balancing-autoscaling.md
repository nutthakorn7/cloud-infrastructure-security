# Lesson Plan — Lesson 6: Load Balancing & Auto-Scaling Under Load

| | |
|---|---|
| **Course** | Cloud Infrastructure & Security · 02005097 (`README.md`, `course-plan.md`) |
| **AWS lesson this attaches to** | AWS Academy **Cloud Foundations Lab 6** — load balancing & auto-scaling (topic only; no AWS Academy file is used or copied) |
| **Kind** | **HYBRID** — Part 1 conceptual essay + Part 2 small lab (`labs/lesson06-load-balancing-autoscaling/README.md`) |
| **Block** | Block 1 (`docs/course-specification.md` §6) |
| **Duration** | **45–60 min add-on**, run *after* the AWS Learner Lab (lab README, "This lesson — what to do") |
| **Lab folder** | `labs/lesson06-load-balancing-autoscaling` |
| **Slides / quiz** | None, by design — `slides/README.md` and `quizzes/README.md` are deliberately empty; the lecture baseline and the Knowledge Check are AWS's |
| **Standards** | **CWE-400** (Uncontrolled Resource Consumption) · OWASP **API4:2023 Unrestricted Resource Consumption** (both named in the lab README) |
| **CLOs addressed** | **CLO2** demonstrate · **CLO3** apply the control (spec §6 row). Task 2b is an *EiPE*, which spec §4 maps to **CLO1/CLO4** — see §9 note |
| **Semester / section / room / grading scale / PLOs** | ⬚ |

> **Cross-reference note.** The curriculum monorepo and the CTFd/flag tooling schedule this lesson as
> **slot 4** (`courses/cloud-infrastructure-security.yml`), rendered "Lesson 4". The renumbering is
> deliberate and documented in `tests/test_parity_cis.py`. In *this* repository it is Lesson 6, after
> the AWS lab it attaches to.

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
  `POST /generate-load` calls against the vulnerable app on `:8109`, and capture the returned flag.
- P3 — Show the identical anonymous request rejected with `401` on the fixed app on `:8110`, then
  show what a *correctly-keyed* caller gets on repeated calls (`429`).
- P4 — Record the exact request pattern — endpoint, method, headers-or-lack-thereof, approximate
  call count — as attributable evidence.
- P5 — Reason about the blast radius of **one** leaked API key against this fixed design.

**Attitude (A)**
- A1 — Attack only the two approved targets: the local Docker labs in `labs/`, and their own AWS
  Academy Learner Lab sandbox ([ETHICS.md](../../ETHICS.md) rule 1).
- A2 — Submit evidence that is identifiably their own — own flag, own screenshots showing
  `whoami`/student ID and a timestamp — and be able to reproduce it live on request
  ([SUBMISSION.md](../../SUBMISSION.md), "Academic Integrity & Anti-Cheating").
- A3 — Treat a cloud bill as an attack surface: "it scaled, so it worked" is not a security verdict.

## 2. Key idea (the through-line)

Nothing in this lab is a code bug. `POST /generate-load` does exactly what it was built to do — the
vulnerability is entirely in what it **does not check** before doing expensive work. Every accepted
request buys the caller a little more of someone else's capacity, and the fleet obediently grows to
its configured maximum. That makes the interesting question not "where is the flaw in the code?" but
"who is allowed to spend this money, and how fast?" — which is why the fix has to be *two* controls
(identity **and** rate), not a cleverer one.

## 3. What students must have completed first

1. **The AWS Learner Lab, first.** The lab README is explicit: complete the real AWS Academy
   load-balancing / auto-scaling lab in the Learner Lab sandbox *before* this add-on — "that's still
   where you learn the actual ALB/target-group/ASG console UI". [SUBMISSION.md](../../SUBMISSION.md)
   states the same order for every lesson: AWS module + Knowledge Check first, local add-on second.
2. **Docker Desktop working** on the student's own machine (SUBMISSION.md, one-time setup).
3. **Signed ethics acknowledgment** from Lesson 1 (ETHICS.md).

**Instructor, before class**
- Pre-build the two images so a room full of students is not pulling `python:3.12-slim` at once.
  Verified command: `docker compose up -d --build` in the lab folder, then `docker compose down`.
- Mint per-student flags: `python3 instructor/seed_flags.py env <STUDENT_ID>` (lab README). Decide
  and announce **which worksheet Part this section is doing** before the session — see §8, risk 1.
- Read the instructor key: `instructor/lesson06-load-balancing-autoscaling-answer-key.md`
  (`instructor/` is git-ignored; never paste it into a public file).

## 4. The add-on session — 55 min

> The minute split below is **this plan's own allocation** inside the 45–60 min envelope the lab
> README states; the repository does not prescribe per-task budgets. Tasks are the worksheet's own
> (Part 2a / 2b / 2c). This table is the **AIR-Sec** delivery; §5 covers the Conventional delivery
> of the same slot.

| Time | Task | Student does | Evidence produced |
|---|---|---|---|
| 0:00–0:05 | **Bridge from the AWS lab** | Recall from the Learner Lab: what the target group held, where min/max/desired capacity was set. Frame today's question: who may trigger scaling, and how often? | — |
| 0:05–0:12 | **Stand up the targets** | `cd labs/lesson06-load-balancing-autoscaling` → `docker compose up -d` (vulnerable on `:8109`, fixed on `:8110`); `GET /status` on both — `current_instances` 2, `load_units` 0 | Baseline screenshot |
| 0:12–0:27 | **Worksheet 2a (i) — the attack** | Loop anonymous `POST /generate-load` against the vulnerable app until `current_instances` reaches the simulated maximum; the response then carries the flag. Either `python exploit.py` or a hand-rolled loop | Request pattern + approximate call count + **the flag** |
| 0:27–0:37 | **Worksheet 2a (ii) — the control** | Same anonymous request against `:8110` → `401`. Then repeat with the correct `X-Api-Key` (value is in the lab's own `docker-compose.yml`) until the response changes to `429`, and re-check `GET /status` | Both responses + the fixed app's `/status` afterwards |
| 0:37–0:47 | **Worksheet 2b — EiPE** | Answer the teammate who says an API key alone is enough, in 3–4 sentences a non-technical stakeholder would follow; and why "just add more instances" is not a security fix | Written answer |
| 0:47–0:53 | **Worksheet 2c — blast radius** | One valid key leaks to a public repository: worst-case scaling-relevant calls before cut-off, and why that number bounds the damage | Written answer |
| 0:53–0:55 | **Submit + tear down** | Export the worksheet to PDF as `Lesson06_<StudentID>.pdf`, submit worksheet + flag to Classroom; `docker compose down` | Submission |

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

The counterbalanced section does **Part 1 only** — five essay questions, no container, no flag
(worksheet, "Submit"). Same 45–60 min envelope:

- 0:00–0:10 — bridge from the AWS lab; the load balancer / target group / ASG relationship (Q1) and
  min-vs-max capacity (Q2, Q3) discussed at the board.
- 0:10–0:20 — instructor demonstrates the anonymous hammer on the projector so the concept is
  concrete; students do not run containers in this arm.
- 0:20–0:50 — students write Q1–Q5.
- 0:50–0:55 — submit.

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
| Worksheet Part 2a (AIR-Sec) | Request pattern, call count, captured flag, both fixed-app responses | P1–P4, K4 | Part of this layer's worksheet mark — ⬚ (spec §4) |
| Worksheet Part 2b — *EiPE* | Written 3–4 sentence explanation | K4, CLO4 | as above |
| Worksheet Part 2c — blast radius | Written answer | P5, K4 | as above |
| Worksheet Part 1 (Conventional arm) | Five essay answers | K1–K4 | as above |
| **Per-student flag** | The `scaling` flag returned by the *vulnerable* app once the fleet reaches maximum | A2 | Integrity control that also carries marks (spec §8) |
| Viva / random live check | Live reproduction and explanation | P1–P4, A2 | Pass / flag for follow-up (SUBMISSION.md) |

**How the flag works here.** Flags are minted per student — `python3 instructor/seed_flags.py env
<STUDENT_ID>` — and injected through `FLAG_SCALING`, which `docker-compose.yml` passes to both
services. The lab README gives the override form as `FLAG_SCALING=FLAG{...} docker compose up`. Only
the **vulnerable** app can ever emit it, and only once `current_instances` has reached the maximum:
the fixed app is flagless by construction, so possession of a flag is evidence the student drove the
exploit themselves. A student who starts the stack without their own value gets the repository
default — that submission is not attributable, and is worth catching at collection time rather than
at grading time.

Grading detail lives in the worksheet's own submission rules and the instructor key. Partial credit
where the mechanism is explained correctly but the run was not completed.

## 8. Risks and contingencies

| Risk | Mitigation |
|---|---|
| **Arm confusion.** The worksheet tells the student to complete only their assigned Part, but its block→arm sentence does not hold for the counterbalanced section, and the lab README says something different again (see §9). A student can do the wrong Part in good faith. | Announce, in class and in the Classroom post, which Part **this section** is doing today. Do not let students infer it from the worksheet header. |
| **Scaler state is cumulative and in-process.** Any exploration before the timed run inflates `load_units`, and a second run returns the flag on call 1 rather than ~40. Nothing resets it from outside. | Verified on this machine: `docker compose restart vulnerable` returns `/status` to `current_instances` 2, `load_units` 0. Restart before a demo or a re-attempt, and mark the *reasoning*, not the exact call count. |
| **The fixed app's key budget is a lifetime counter.** A student who spends it while poking about gets `429` on every later keyed call, including the one they meant to screenshot. | `docker compose restart fixed` (same mechanism as above). |
| **`pip install requests` is refused** with *externally-managed-environment* (PEP 668) on Homebrew and Debian-packaged Python — the README's host-side install then fails. | Verified fallback: `python3 -m venv .venv && .venv/bin/pip install requests && .venv/bin/python exploit.py` (`.venv/` is already git-ignored). Or skip `exploit.py` and drive the endpoint with `curl` — the exercise needs no Python. |
| **`python exploit.py` fails** on machines where only `python3` exists. | Run `python3 exploit.py`; that is what was used to reproduce the README's captured output. |
| **Host ports 8109 / 8110 already bound.** | `exploit.py` reads `VULN_URL` and `FIXED_URL` from the environment, so a student who remaps published ports can point it at the new ones without editing the script. Prefer that to editing `docker-compose.yml` — the lab files are covered by the monorepo parity gate. |
| **First-time image build inside a 45–60 min slot** (`python:3.12-slim` pull + Flask install) eats the lab. | Pre-build during the AWS Learner Lab portion, or ask students to run `docker compose up -d --build` the night before. |
| **The AWS Learner Lab overruns** and swallows the add-on. | Fall back to the §5 shape: demonstrate the anonymous hammer at the front, set 2b and 2c as homework, and have students run 2a on their own machines before the next session. |
| **Copied flags.** The default value is printed in the public lab README, so a student who never ran anything can quote it. | Per-student flags via `seed_flags.py`; `seed_flags.py verify` resolves any submitted flag back to the student it was issued to. Spot-check with a live reproduction. |
| **Someone points the loop at a real endpoint.** The technique is trivially portable and would be a genuine offence. | Re-state ETHICS.md rules 1–2 at the start: local labs and the student's own Learner Lab only — "not even to 'look'". |

## 9. Instructor notes on lab-content issues (do not fix inside a worksheet mid-term)

Three inconsistencies in this lesson's own materials are flagged rather than edited — any change has
to move `labs/`, the curriculum monorepo copy and the instructor key together (repo CLAUDE.md), and
the monorepo copy carries the documented renumbering substitutions in `tests/test_parity_cis.py`.

1. **Who does Part 1.** The lab README says "Part 1 essay for everyone; Part 2 AIR-Sec students also
   submit the flag"; the worksheet says "complete only the part assigned to you this block" and its
   Submit line reads "Part 1 (Conventional) or Part 2a/2b/2c (AIR-Sec)". These cannot both hold.
   Teach the worksheet's version and say so explicitly.
2. **Block → arm.** The worksheet's opening line ("Section is assigned Block 1 = AIR-Sec or Block 2
   = Conventional per `course-plan.md`'s block table") is byte-identical boilerplate copied into
   every lesson worksheet, not conditioned on section — so it states the mapping as fixed. It holds
   for Section A but is reversed for Section B (`course-plan.md`: "Section A = Block 1 AIR-Sec /
   Block 2 Conventional; Section B = reversed"; `docs/course-specification.md` §6: "Section B = the
   reverse"). The citation is also imprecise: `course-plan.md`'s actual "Lesson topic map" table
   gives only lesson→block (1 or 2); the block→arm rule is the section-conditional prose sentence
   beneath that table, not the table itself. This is a Block-1 lesson, so a Section B student
   following the worksheet header verbatim would join the wrong arm.
3. **Declared duration.** `lesson.yml` in the monorepo records `duration_min: 180` for this lesson —
   as it does for all ten cloud lessons, a template default carried over from the 19-week sibling
   courses. The authoritative figure for teaching is the lab README's 45–60 min.

Also noted: spec §6 assigns this row CLO2 and CLO3, while spec §4 maps *EiPE* tasks to CLO1/CLO4 —
task 2b is an EiPE, so the row understates its own CLO coverage.

## 10. Materials

- Lab: `labs/lesson06-load-balancing-autoscaling/` — `README.md`, `worksheet.md`, `scaler.py`,
  `vulnerable_app.py`, `fixed_app.py`, `exploit.py`, `docker-compose.yml`, `Dockerfile`,
  `requirements.txt`
- Instructor key: `instructor/lesson06-load-balancing-autoscaling-answer-key.md` (git-ignored)
- Flag tooling: `instructor/seed_flags.py` (challenge key `scaling`, salt env `CIS_FLAG_SALT`)
- Run block, quoted from the lab README:
  ```bash
  cd labs/lesson06-load-balancing-autoscaling
  docker compose up -d          # vulnerable_app.py on :8109, fixed_app.py on :8110
  pip install requests          # once, on the host
  python exploit.py
  ```
- References the lab itself cites: AWS Elastic Load Balancing documentation (*What is a target
  group?*, *Application Load Balancer components*); AWS Auto Scaling documentation (*Auto Scaling
  group concepts* — minimum, maximum, desired capacity, scaling policies); OWASP *API4:2023
  Unrestricted Resource Consumption*. All publicly available; **no AWS Academy file is used.**
- Rules of engagement: [ETHICS.md](../../ETHICS.md) · Submission: [SUBMISSION.md](../../SUBMISSION.md)

**Reproduced on 2026-07-26** on the instructor machine, from a freshly built stack: the anonymous
loop drove `current_instances` to the maximum on call 40 and the response carried the flag; the same
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
