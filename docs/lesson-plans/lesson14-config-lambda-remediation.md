# Lesson Plan — Lesson 14 add-on: AWS Config + Lambda Auto-Remediation (Inverted Allowlist)

*CLOUD add-on. The AWS Academy Learner Lab is the baseline students do first; this is the add-on
that attacks and fixes the same idea locally. **No AWS Academy material is reproduced, quoted or
paraphrased from a file anywhere in this plan or in the lab** — the topics are described in our own
words only (`course-plan.md` §"Licensing"; `docs/course-specification.md` §2).*

| | |
|---|---|
| **Course** | Cloud Infrastructure & Security · subject code **02005097** (`README.md`, `course-plan.md`; `docs/course-specification.md` still records the course code as ⬚) |
| **AWS lesson this attaches to** | **Lesson 14** — AWS Config detecting a non-compliant security group, and a Lambda-based remediation action meant to fix it automatically (topic named in our own words; source is Shinya's own troubleshooting notes, per the lab `README.md`) |
| **Add-on kind** | **HYBRID** — small runnable lab plus conceptual material; AWS Config's resource-inventory / compliance-tracking machinery is **concept only**, covered in the worksheet, not simulated in code (`README.md`; `docs/course-specification.md` §6) |
| **Block** | **2** (`docs/course-specification.md` §6, `course-plan.md`). Block 2 = **Conventional for Section A**, **AIR-Sec for Section B** — the reverse of Block 1 (`docs/course-specification.md` §6 "Block assignment"; `course-plan.md`) |
| **Duration of this add-on** | **45–60 min** — the figure the lab's own `README.md` states. This is *not* a full contact session; the AWS Academy Learner Lab is the baseline and comes first |
| **Lab folder** | `labs/lesson14-config-lambda-remediation` |
| **Targets** | `vulnerable_app.py` on **:8115** · `fixed_app.py` on **:8116** (`docker-compose.yml`) |
| **Signature exercise** | "The Inverted Allowlist" (`README.md`) |
| **Standards** | Analogous **CWE-697** (Incorrect Comparison) · **CWE-284** (Improper Access Control) (`README.md`; `lessons/config-lambda-remediation/lesson.yml` in the curriculum monorepo) |
| **CLOs addressed** | **CLO2** demonstrate the misconfiguration · **CLO3** apply the correct control and verify empirically (schedule row, `docs/course-specification.md` §6). Via §4's alignment table the per-student flag also carries **CLO5**, and the *Audit-the-AI* / *EiPE* tasks carry **CLO1** and **CLO4** |
| **Slides** | ⬚ — none. `slides/` in this course is deliberately empty (`slides/README.md`) |
| **Session date / room / section** | ⬚ |

> **⬚ institution-specific, recorded nowhere in this repository:** semester, section, room, date,
> grading scale, the programme's PLO list, and the exact percentage this add-on carries of the
> non-AWS portion of the grade (`docs/course-specification.md` §4, §8). The AWS-graded ~40% is
> scored by AWS and is identical for every student — it is *not* part of this add-on.

> **Naming note.** The lab folder, README and worksheet call this **Lesson 14** — the *AWS lesson
> number* it attaches to. The curriculum monorepo (`courses/cloud-infrastructure-security.yml`)
> lists the same lesson at **slot 10** of 11 slots, because only ten AWS lessons carry an add-on.
> Both labels refer to the same material; use "Lesson 14" with students, since that is what the
> worksheet header and the `Lesson<NN>_<StudentID>.pdf` submission convention use
> ([SUBMISSION.md](../../SUBMISSION.md)).

---

## 1. Session objectives

By the end of this add-on a student can:

**Knowledge (K)**
- K1 — Explain, at a high level, how an AWS Config rule evaluates a resource as **COMPLIANT** or
  **NON_COMPLIANT**, and how a Lambda-based remediation action is *meant* to fit the detect → decide
  → act flow (worksheet Part 1 Q1–Q2; README "Objectives").
- K2 — State the difference between **allowlist** thinking ("deny by default, permit specific
  things") and **denylist** thinking ("permit by default, deny specific things") applied to security
  group inbound rules, and say which is generally safer and why (worksheet Part 1 Q3).
- K3 — Identify an **inverted comparison** (`in` vs `not in` an allowed-ports set) as the bug class,
  and explain why it is a **silent** failure — no exception, no error log, `200 OK` either way
  (README "Objectives"; `remediation_engine.py` docstrings).
- K4 — Explain why "it ran without errors" is not evidence that a remediation function did the right
  thing, and why an inverted-logic bug is worse for an on-call engineer than a crash (worksheet
  Part 1 Q4, Part 2c).
- K5 — Describe a real-world consequence of an inbound rule for SSH (22) or RDP (3389) left open to
  `0.0.0.0/0` on a production security group (worksheet Part 1 Q5).

**Skills (P)**
- P1 — Stand the vulnerable/fixed pair up and read the **seeded baseline**: three inbound rules —
  port 80 (`0.0.0.0/0`), port 443 (`0.0.0.0/0`) and port 22/SSH (`0.0.0.0/0`), the last being what a
  real Config rule such as `restricted-ssh` would flag as NON_COMPLIANT (README signature step 1;
  `remediation_engine.py:seed_rules`).
- P2 — Run the `/reset` → `/remediate` → `/security-group` sequence against **:8115** and show the
  two-part failure: the SSH-from-anywhere rule **survives**, and ports 80/443 are **wrongly
  revoked** — capturing the flag the vulnerable app returns (worksheet 2a; README signature step 4).
- P3 — Run the identical sequence against **:8116** and show only the 80/443 rules remain, the SSH
  rule is correctly revoked, and **no flag** is returned (README signature step 5).
- P4 — Point at the single flipped comparison in `remediation_engine.py` that separates
  `remediate_correct` from `remediate_inverted`, and state which app calls which.
- P5 — Find the planted flaw in the AI-supplied `remediate()` function in worksheet 2b and say in
  plain English what that function actually returns (worksheet 2b).

**Attitude (A)**
- A1 — Attack only the two approved targets — the local Docker labs in `labs/` and their own
  assigned Learner Lab sandbox ([ETHICS.md](../../ETHICS.md) rules 1–3). Never widen, revoke or probe
  a security group that is not in one of those two places.
- A2 — Submit **attributable, reproducible** evidence: their own flag, with `whoami` / student ID /
  timestamp visible, and be able to reproduce the capture live on request
  ([SUBMISSION.md](../../SUBMISSION.md)).
- A3 — Treat AI-generated remediation code as something to verify by tracing it, not to trust
  because it is fluent and well-commented (worksheet 2b; `docs/course-specification.md` CLO4).

## 2. Key idea (the through-line)

Automation that reports success is trusted more than automation that fails. That is the whole lesson.

A Config rule plus a remediation function is a closed loop: something detects that a security group
is non-compliant, something else acts to bring it back into compliance, and a dashboard records the
outcome. Every part of that loop is a *report* about the resource, not the resource itself. When the
remediation function's keep/revoke condition is inverted, the loop still closes — the function
returns, no exception is raised, the response is `200 OK`, and the compliance dashboard would read
"remediation: succeeded". Underneath, the function has done precisely the opposite of its job: it
revoked the two rules that were supposed to stay (80 and 443, so legitimate web traffic breaks) and
kept the one rule that was supposed to go (22 from `0.0.0.0/0`, so the finding that triggered the
whole loop is still there).

This is worse than a remediation function that crashes. A crash pages someone. A one-token inversion
(`not in` where `in` belongs) produces an outage *and* leaves the exposure, and hands both a green
tick. The defence is not "add more automation" — it is to verify the *post-condition* (what rules
actually remain) rather than the *return status*, and to write the allowlist so the safe branch is
the default one.

## 3. What students must have completed before this add-on

**In the AWS Academy Learner Lab (first, and graded by AWS):**
- That lesson's AWS Academy module and its Knowledge Check — AWS grades this part
  ([SUBMISSION.md](../../SUBMISSION.md) — AWS first, add-on second).
- The **real Learner Lab exercise on AWS Config detecting a non-compliant security group and a
  Lambda function remediating it**. The lab README is explicit that this is still where the actual
  console UI is learned — Config rules, the compliance timeline, the Lambda console and CloudWatch
  Logs. Nothing in this add-on re-teaches or replaces any of that, and no AWS Academy file is used.

**On their own machine:**
- **Docker Desktop** working ([SUBMISSION.md](../../SUBMISSION.md) one-time setup).
- A working host Python for `exploit.py` — see §8 risk 1. On a machine where only `python3` exists,
  the README's `pip` / `python` commands need the `python3 -m pip` / `python3` forms.

**Instructor, before the session:**
- **Pre-build the images.** `docker compose up -d --build` in the lab folder pulls
  `python:3.12-slim` and pip-installs `flask>=3.1.3` and `requests>=2.33.0` (`Dockerfile`,
  `requirements.txt`). A whole room doing that at once is the standard way to lose the first
  fifteen minutes of a 45-minute add-on.
- **Mint the per-student flags** — `python3 instructor/seed_flags.py env <STUDENT_ID>` (§7). The
  shim needs the curriculum monorepo as a sibling directory and `CIS_FLAG_SALT` (or the legacy
  `FLAG_SALT`) exported. Do this the day before, not five minutes before class.
- **Re-read the answer key** `instructor/lesson14-config-lambda-remediation-answer-key.md`
  (git-ignored, instructor-held) against the current worksheet.
- **Confirm ports 8115 and 8116 are free** — they are confirmed non-colliding across this repo's
  labs, which allocate 8104–8117 (`course-plan.md`), but another lesson's containers left running
  will still hold their own ports.
- **Decide, and announce, which arm this section is running** — Block 2 is **Conventional for
  Section A** and **AIR-Sec for Section B**. See §8 risk 8 and §9 note 4.

## 4. The add-on session — minute by minute

> **Where these minutes come from.** The task *names and content* below are the worksheet's and
> README's own; the **minute split is this plan's allocation** inside the 45–60 min envelope the lab
> README states. Neither the README, the worksheet nor the code carries a per-task budget — do not
> treat these numbers as fixed course material, and do not edit the lab to make them add up.

**Kickoff commands, exactly as the lab README has them:**

```bash
cd labs/lesson14-config-lambda-remediation
docker compose up -d --build       # vulnerable_app.py on :8115, fixed_app.py on :8116
pip install requests               # once, on the host
python exploit.py
```

(The README's step 2 gives the shorter kickoff `docker compose up -d`; use the `--build` form above
on first run. See §8 risk 1 before the class types the last two lines.)

### 4a. AIR-Sec section (Block 2 = Section B) — 60-minute plan

| Suggested | Task | Student does (task names and content from the lab) | Evidence produced |
|---|---|---|---|
| 0:00–0:05 | **Framing** | Recall what the Learner Lab exercise already did — a Config rule found a non-compliant security group and a remediation function was supposed to fix it. Today's question is not "did it run?" but "what did it actually leave behind?" | — |
| 0:05–0:12 | **Stand the targets up** | `cd labs/lesson14-config-lambda-remediation` → `docker compose up -d --build`; confirm both services answer on `/ping` (`mode` is `vulnerable` on :8115, `fixed` on :8116) | Screenshot of both `/ping` responses |
| 0:12–0:20 | **Baseline (worksheet 2a, step 1)** | `POST /reset` on **:8115** to seed the security group: port 80 (`0.0.0.0/0`), port 443 (`0.0.0.0/0`), port 22 (`0.0.0.0/0`). Name which of the three a Config rule would flag NON_COMPLIANT, and why | The seeded rule list, with the SSH-from-anywhere rule identified |
| 0:20–0:32 | **Run the remediation and read the damage (worksheet 2a, steps 2–3)** | `POST /remediate` then `GET /security-group` on **:8115**. Note **both** halves of the failure: `dangerous_rules_present` is still true (port 22 survived) *and* 80/443 are gone. Capture the flag the response now carries | The exact `/reset` → `/remediate` → `/security-group` sequence, the surviving rule set, and the captured flag |
| 0:32–0:40 | **Confirm the fix (worksheet 2a, step 4)** | The identical sequence against **:8116** → only 80/443 remain, `dangerous_rules_present` is false, and **no flag** appears. Then open `remediation_engine.py` and point at the one-token difference between `remediate_correct` and `remediate_inverted` | The fixed app's post-remediation state + the named comparison (`in` vs `not in` the allowed set `{80, 443}`) |
| 0:40–0:50 | **Worksheet 2b — Audit-the-AI** | Trace the AI-supplied `remediate()` in the worksheet by hand with `allowed_ports = {80, 443}` and rules on 80, 443 and 22; state which ports end up in `remaining_rules` and what the function is really doing | Written answer — the planted flaw named, plus what the function actually returns (start in class, finish as homework) |
| 0:50–0:57 | **Worksheet 2c — EiPE + simplification debrief** | 3–4 sentences a non-technical stakeholder could follow on why a "successful" remediation left the network exposed, and why that is scarier than loud failure; then the instructor walks §6 (where this simulation is *not* AWS Config or Lambda) | Written answer + no one leaves with a wrong model of the real services |
| 0:57–1:00 | **Submit + tear down** | Confirm the submission bundle; `docker compose down` | `Lesson14_<StudentID>.pdf` + the flag → Google Classroom |

**Compressing to 45 minutes.** Keep 0:00–0:40 intact — the 2a sequence against both targets and the
`remediation_engine.py` comparison are the assessed core and the only part that needs the running
containers. Send 2b and 2c home as written work, and replace the 0:50–0:57 debrief with the
two-minute version of §6 (rules are a Python list in process memory; no Config, no Lambda, no AWS
API calls anywhere). If the room is short on time, `python exploit.py` performs the whole
three-request sequence against both targets in one shot and prints two `PASS` lines — but worksheet
2a asks for *the exact request sequence the student ran*, so anyone taking that route must still be
able to state it and reproduce it.

**Optional one-shot check.** `python exploit.py` — expect two `PASS` lines and exit `0`: the
dangerous rule plus flag surviving remediation on :8115, and the dangerous rule correctly removed
with no flag on :8116. *(Re-verified on this machine on 2026-07-26: `docker compose up -d --build`
then `python3 exploit.py` reproduced the README's captured output exactly, exit code 0.)*

**Checks for understanding**
- After the baseline `POST /reset`: cold-call — *"three rules, all open to `0.0.0.0/0`. Which one is
  the finding, and why are the other two fine?"*
- Immediately after `/remediate` on :8115: *"the response said `status: remediated`. Did it work?
  How would you know without looking at the rules?"* — this is the whole lesson in one question.
- After the :8116 run: *"point at the one token that differs between the two functions."*
- Exit ticket (one sentence): *"what would you check, in a monitoring dashboard, that would have
  caught this?"*

### 4b. Conventional section (Block 2 = Section A)

The worksheet's own instruction is *"complete only the part assigned to you this block"*, and Part 1
— five essay questions on what a Config rule does and what COMPLIANT vs NON_COMPLIANT means; how a
Lambda-based auto-remediation fits the detect → decide → act flow; allowlist vs denylist thinking for
security group rules; why an inverted-logic bug is more dangerous than a crash or a no-op; and a
real-world consequence of SSH/RDP open to `0.0.0.0/0` — carries **no flag and no AI-resilience
layer**. That is exactly the manipulation `course-plan.md` describes: a standard take-home worksheet
question on the same concept. Use the slot for guided discussion of those five questions; the
exploit is not run in this arm.

⬚ **Not fixed anywhere in this repository:** whether the Conventional section also stands the local
Docker target up in class. Running the exercise for them would import part of the AIR-Sec treatment
into the control arm; leaving it out means the concept is assessed by writing only. This is a
study-design decision, not a per-lesson one — decide it once, apply it to every Conventional-block
lesson, and record it here.

## 5. What the two targets actually do

Both apps expose the same four endpoints (`vulnerable_app.py`, `fixed_app.py`):

| Endpoint | Method | Behaviour |
|---|---|---|
| `/reset` | POST | Re-seeds the security group to the deterministic starting rule set (80, 443, 22 — all `0.0.0.0/0`) |
| `/remediate` | POST | Runs the remediation function over the current rules; returns `before`, `after` and `mode` |
| `/security-group` | GET | Returns the current rules and `dangerous_rules_present` |
| `/ping` | GET | Liveness; `mode` is `vulnerable` or `fixed` |

The only real difference is one import: `vulnerable_app.py` calls `remediate_inverted`,
`fixed_app.py` calls `remediate_correct`, and both live in `remediation_engine.py` with
`ALLOWED_PORTS = {80, 443}`. `DANGEROUS_PORTS = {22, 3389}` is what `dangerous_rules_present`
tests against.

**The flag gate is deliberate.** The vulnerable app returns the flag from `GET /security-group`
only when a dangerous rule is present **and** `remediation_attempted` is true — the code's own
comment says so, because the dangerous rule is present from the seeded starting state and an
ungated flag could be collected without ever exercising the bug. *(Verified on this machine:
`POST /reset` followed immediately by `GET /security-group` on :8115 returns
`dangerous_rules_present: true` and **no** `flag` field.)* `fixed_app.py` has no flag at all — the
control app is flagless by design, and this course's `CLAUDE.md` records that it once leaked
`FLAG_REMEDIATE` at container startup, which defeated the whole evidence model.

## 6. Where this simulation departs from real AWS — say this out loud

The course specification requires the departures to be named in the same breath as the exercise
(`docs/course-specification.md` §2, §7; this repo's `CLAUDE.md` "Simulations are simulations").
Everything below is visible in the lab's own source.

1. **AWS Config is not simulated at all.** There is no resource inventory, no configuration item, no
   compliance timeline, no rule evaluation and no history — the README and the lesson objectives say
   so explicitly. Nothing in the lab *detects* anything; the student calls `/remediate` by hand where
   Config would have triggered it. That machinery is assessed by essay (Part 1 Q1–Q2) only.
2. **Lambda is not simulated either.** No event source, no invocation, no execution role, no
   CloudWatch Logs, no cold start, no timeout. The "remediation function" is a plain Python function
   called inside a Flask request — `remediation_engine.py`'s own docstring states that no AWS Config
   or Lambda SDK calls happen anywhere in it.
3. **The security group is a Python list in process memory.** `security_group["rules"]` lives in the
   Flask process; restarting the container restores the seeded three rules. There is no VPC, no ENI,
   no instance behind the group, and revoking a rule here breaks nothing real — in AWS, revoking
   80/443 would cut live traffic, which is precisely the consequence students have to *reason* about
   rather than observe.
4. **Nothing in AWS ever returns a flag.** The flag in `GET /security-group` is this course's
   attributable-evidence mechanism, not modelled AWS behaviour.
5. **State is global to the process, not per-student.** `/reset` mutates one shared dictionary. That
   is fine when each student runs their own containers, and wrong the moment the target is shared —
   see §8 risk 6.
6. **Both apps run Flask's built-in development server** (`app.run(host="0.0.0.0", port=5000)`)
   inside the container, published on 8115 and 8116. It is a teaching target, not a hosting stack.
7. **The allowlist is two ports and a rule is a two-field record, `{"port", "cidr"}`.**
   `ALLOWED_PORTS = {80, 443}` and `seed_rules()` produce a deliberately minimal shape for teaching.
   A real inbound rule is richer than that, and this lab states none of the detail — take it from the
   *AWS EC2 — Security group rules* documentation the lab README already cites (§10), not from this
   simulation, before describing it to students. Do not let anyone leave believing a security group
   rule is a port and a CIDR.

## 7. Assessment

| Instrument | Evidence | Outcome | Weight |
|---|---|---|---|
| Worksheet Part 2a (AIR-Sec sections) | The exact `/reset` → `/remediate` → `/security-group` sequence run against the vulnerable app, the captured flag, the surviving rule set it came from, and the same sequence plus resulting state against the fixed app | K3, P1–P4, A2 | Part of the worksheet mark (`docs/course-specification.md` §4) |
| Worksheet Part 2b — *Audit-the-AI* | The planted flaw in the AI-supplied `remediate()` named, with what the function actually returns when traced by hand | K2, K3, P5, A3 · CLO1/CLO4 per §4 | Part of the worksheet mark |
| Worksheet Part 2c — *EiPE* | 3–4 sentences a non-technical stakeholder could follow on why a "successful" run still left the network exposed | K4 · CLO4 | Part of the worksheet mark |
| Worksheet Part 1 (Conventional sections) | Five essay answers — graded on the writing itself | K1, K2, K4, K5 | The Conventional arm's whole submission |
| **Per-student flag** — challenge key `remediate`, injected as `FLAG_REMEDIATE` | The `flag` value the **vulnerable** app returns from `GET /security-group` once `/remediate` has run | A2 · CLO5 | Integrity control that also carries marks (`docs/course-specification.md` §9) |
| Viva / random live check | Live reproduction of the sequence and explanation of the inverted comparison | P2–P4, A2 | Pass / flag for follow-up |

**How the flag control works.** Flags are minted per student from the student ID —
`python3 instructor/seed_flags.py env <STUDENT_ID>`, challenge key `remediate`, salted with this
course's own `CIS_FLAG_SALT` — so a copied flag is traceable to the student it was *issued* to
rather than being a matter of judgement. Without a mint, `FLAG_REMEDIATE` falls back to the public
default baked into `docker-compose.yml`, and it can also be overridden per build with the README's
documented form, `FLAG_REMEDIATE=FLAG{...} docker compose up` (the braces there are the README's own
placeholder, not a value). *(Override path verified on this machine: setting `FLAG_REMEDIATE` in the
environment is reflected in `docker compose config` for both services.)* The fixed app never returns
a flag, so possession of one **is** evidence the student drove the vulnerable path. Submitting
another student's flag is a violation for both parties
([SUBMISSION.md](../../SUBMISSION.md)).

**Deliverable, per the lab README.** The captured flag + the exact request sequence (`/reset`,
`/remediate`, `/security-group`) that produced it + a one-paragraph explanation of why an inverted
allowlist condition is more dangerous than a rule that simply does nothing.

**Submission.** Worksheet exported to PDF with screenshots embedded, named
`Lesson14_<StudentID>.pdf`, plus the captured flag → Google Classroom, before the next class
session; AI-tool disclosure required; late −10%/day up to 3 days
([SUBMISSION.md](../../SUBMISSION.md)).

**Grading scale, and this layer's share of the final grade: ⬚** — an institutional decision,
recorded nowhere in this repository (`docs/course-specification.md` §4, §8).

## 8. Risks and contingencies

| Risk | Mitigation |
|---|---|
| **1. The README's host commands assume `python` and `pip` are on PATH.** Verified on this machine: `python3` and `pip3` exist; `python` and `pip` do not — so `pip install requests` and `python exploit.py` both fail exactly as written | Have students use `python3 -m pip install requests` / `python3 exploit.py`, or a virtual environment if the host Python refuses a global install. Announce this before the class types the block. **Do not edit the lab to fit the room** — escalated as lab content in §9 |
| **2. `exploit.py` cannot be run inside the container.** The `Dockerfile` copies only `remediation_engine.py vulnerable_app.py fixed_app.py`, so the exploit script is not in the image even though `requests` is installed there | Run it from the host as the README says, or skip it — the three requests are short enough to make by hand with `curl` or any HTTP client, and worksheet 2a wants the student's own sequence anyway |
| **3. Ports 8115/8116 already bound** — usually another of this course's labs still running (`course-plan.md` allocates 8104–8117 across the labs; 8115/8116 belong to this one) | `docker compose down` in the other lab folder before starting; or republish the ports in the student's own working copy |
| **4. The flag is captured before `/remediate`, or after a `/reset`, and nothing appears.** The vulnerable app gates the flag on `remediation_attempted`, which `/reset` sets back to false | Enforce the order: `/reset` → `/remediate` → `/security-group`. A student seeing `dangerous_rules_present: true` with no `flag` field has almost always re-`/reset` after remediating |
| **5. A student concludes the bug is "SSH is open".** It is not — SSH-from-anywhere is the *seeded finding*, present before any code runs. The bug is that remediation kept it and revoked 80/443 | Grade both halves of 2a. Require the student to state what happened to ports 80 and 443, not only that port 22 survived. The one-question check in §4a is designed to surface this |
| **6. A shared or hosted instance collides between students.** `security_group` is one module-level dictionary per process, so on a shared target one student's `/reset` wipes another's state mid-capture | Each student runs their own containers locally, which is what the README and [SUBMISSION.md](../../SUBMISSION.md) assume. If this lesson is ever fronted by a shared challenge host, it needs per-student instances — the third challenge-host is listed as not yet provisioned in `course-plan.md` "Open / not yet done" |
| **7. Everyone submits the same flag.** `docker-compose.yml` bakes a default `FLAG_REMEDIATE`, so a cohort whose flags were never seeded produces one identical class-wide flag and the attributability control silently does nothing | Seed per student before the session (§7); spot-check two submissions for distinct values. `seed_flags.py` is a shim that exits with an error unless the curriculum monorepo sits as a sibling directory and `CIS_FLAG_SALT` (or legacy `FLAG_SALT`) is exported — run it the day before |
| **8. Arm mix-up between sections.** In Block 2, Section A runs **Conventional** (Part 1) and Section B runs **AIR-Sec** (Part 2) — the reverse of Block 1, and the worksheet's own header line is ambiguous about this (§9 note 4). A student who completes the wrong part has produced evidence that cannot be graded for their arm, and contaminates the study data | State the assigned part on the board and in the Classroom post at the start of the session. Do not rely on the worksheet header alone for this lesson |
| **9. First `docker compose up -d --build` pulls `python:3.12-slim` and pip-installs for the whole room at once** | Pre-build before the session; keep an offline image copy (`docker save` / `docker load`); or set the build as homework |
| **10. Ethics drift into the Learner Lab or a real account.** A student with the AWS console open in the next tab is one step from revoking or widening a rule on a real security group "to see what happens" | Restate [ETHICS.md](../../ETHICS.md) rules 1–3 at the start and again before students switch back to AWS: the local labs and their own sandbox are the only approved targets, and probing real AWS can suspend the whole class's accounts. Changing inbound rules is a *destructive* action even in a sandbox — it can break the student's own running lab |
| **11. A student finishes 2a in ten minutes** | Extension that needs no new code: have them state the post-condition assertion that would have caught this in review — the check `exploit.py` already makes on the fixed target (`{r["port"] for r in fixed_sg["rules"]} == {80, 443}`) is exactly it. Ask them why a test on the return status could never have caught it |

## 9. Instructor notes escalated from lab content

Recorded here rather than fixed. Student-facing lab material and its curriculum-monorepo copy are
parity-gated and graded, and must not be edited to make this plan tidy
([../../CLAUDE.md](../../CLAUDE.md)).

1. **Host commands.** The README's `pip install requests` / `python exploit.py` fail on a host that
   has only `python3` (verified here — `python` and `pip` are absent from PATH). The
   `python3 -m pip` / `python3` forms would work everywhere the current ones do. This is the same
   defect already escalated in the Lesson 5 plan.
2. **Kickoff command inconsistency.** README step 2 gives `docker compose up -d` while the "Run it"
   block gives `docker compose up -d --build`; on a first run only the second builds the image.
3. **Duration conflict.** The lab README states this add-on is **45–60 min**; the curriculum
   monorepo's `lessons/config-lambda-remediation/lesson.yml` carries `duration_min: 180`. That is not
   a value borrowed from a sibling course — every `lesson.yml` in the monorepo (all three courses,
   including this course's own other lessons) carries the identical unfilled `duration_min: 180`
   default; it was never customized per lesson. This plan follows the README. The real fix is
   populating this course's per-lesson durations in the manifest, not chasing a value that leaked in
   from elsewhere.
4. **The worksheet's arm-assignment line is ambiguous for Section B.** `worksheet.md` opens with
   *"Section is assigned Block 1 = AIR-Sec or Block 2 = Conventional … (Lesson 14 falls in Block 2.)"*
   — which reads as though Block 2 is Conventional for everyone. The design is counterbalanced:
   Section A = Block 1 AIR-Sec / Block 2 Conventional, **Section B is the reverse**
   (`docs/course-specification.md` §6; `course-plan.md`), so Section B students are the **AIR-Sec**
   arm for this lesson and would be told by this header to do Part 1. The Lesson 7b worksheet spells
   the same situation out correctly ("Section A = Block 2 Conventional; Section B = Block 2
   AIR-Sec") — this worksheet should match that wording. Until it does, announce the assignment
   verbally and in Classroom (§8 risk 8).
5. **`docker-compose.yml` injects `FLAG_REMEDIATE` into the `fixed` service.** `fixed_app.py` never
   reads it — it holds no flag constant at all, which is correct — so the variable is inert today.
   But it is the same wiring that once leaked the flag from the control app, a regression this
   repo's `CLAUDE.md` records explicitly. Removing it from the `fixed` service would make the
   flagless-control invariant structural rather than a property of the current code. Related, and
   cosmetic: `fixed_app.py` imports `os` but never uses it.
6. **Stray build artefact in the student-facing folder.** `labs/lesson14-config-lambda-remediation/`
   contains `__pycache__/vulnerable_app.cpython-314.pyc`. The parity gate skips `__pycache__`
   explicitly (`tests/test_parity_cis.py`), so nothing catches it, but it does not belong in a
   student-facing lab directory.

## 10. Materials

- **Lab:** `labs/lesson14-config-lambda-remediation/` — `README.md`, `worksheet.md`,
  `remediation_engine.py`, `vulnerable_app.py` (:8115), `fixed_app.py` (:8116), `exploit.py`,
  `docker-compose.yml`, `Dockerfile`, `requirements.txt` (`flask>=3.1.3`, `requests>=2.33.0`).
- **Instructor-held (git-ignored):** `instructor/lesson14-config-lambda-remediation-answer-key.md` ·
  `instructor/seed_flags.py` · `instructor/check_flag_keys.py`.
- **Course documents:** [course-specification.md](../course-specification.md) ·
  [course-plan.md](../../course-plan.md) · [SUBMISSION.md](../../SUBMISSION.md) ·
  [ETHICS.md](../../ETHICS.md) · [CLAUDE.md](../../CLAUDE.md).
- **Slides:** ⬚ — none; `slides/` is intentionally empty for this course (`slides/README.md`).
- **Reference, as listed in the lab README** (all publicly available; **no AWS Academy file is used,
  quoted or copied**): AWS Config documentation on evaluating resources with rules and remediating
  noncompliant resources; AWS Lambda documentation on the event-driven remediation pattern; AWS EC2
  documentation on security group rules, and why an inbound rule open to `0.0.0.0/0` on a management
  port (22/3389) is treated as a high-severity finding by most cloud security posture tools.
- **Baseline curriculum:** the AWS Academy Learner Lab itself — accessed through AWS, never mirrored
  here.

## 11. Post-teaching reflection

*Complete after the session — this also feeds the course's engagement data.*

- Attendance / completion: ⬚
- Time actually taken per task (vs. the allocation in §4): ⬚
- Did the 45–60 min envelope hold, or did the AWS Learner Lab overrun into it: ⬚
- Where the class got stuck, and what unblocked them: ⬚
- Did anyone report the bug as "SSH is open" rather than "remediation kept the wrong rules"? What
  corrected it: ⬚
- Quality of the *Audit-the-AI* (2b) answers — did students trace the function by hand and catch the
  inverted branch unaided: ⬚
- Did the *EiPE* (2c) answers get to "success was reported, the exposure remained", or stop at "the
  code had a bug": ⬚
- Did any misconception survive the §6 debrief — especially that this lab contains Config or Lambda
  at all: ⬚
- Flags: all distinct? Any duplicate submissions to follow up: ⬚
- Section/arm confusion from the worksheet header (§9 note 4) — did it occur: ⬚
- Anything to change before this add-on runs again: ⬚
