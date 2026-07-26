# Lesson Plan — Lesson 10 add-on: VPC Networking (Public/Private Subnets, NAT Gateway, Security Groups vs. NACLs)

*CLOUD add-on. The AWS Academy Learner Lab is the baseline students do **first**; this is the
add-on that attacks and fixes one idea from it locally. **No AWS Academy material is reproduced
anywhere in this plan or in the lab** — the topic is described in our own words only.*

| | |
|---|---|
| **Course** | Cloud Infrastructure & Security · subject code **02005097** (`README.md`, `course-plan.md`; `docs/course-specification.md` still records the course code as ⬚) |
| **AWS lesson this attaches to** | **Lesson 10** — VPC networking: public/private subnets, NAT gateway, security groups, network ACLs (topic named in our own words; the real console work stays in the Learner Lab) |
| **Add-on kind** | **HYBRID** — a small runnable vulnerable/fixed pair with a flag for the NACL rule-ordering bug, plus conceptual material (security-group-vs-NACL comparison and NAT gateway) that stays on the worksheet (`docs/course-specification.md` §6; lab `README.md` header) |
| **Block** | **2** (`docs/course-specification.md` §6). In Block 2 the arms are **reversed** relative to Block 1: **Section A = Conventional, Section B = AIR-Sec** (spec §6: "Section A = Block 1 AIR-Sec / Block 2 Conventional; Section B = the reverse") |
| **Duration of this add-on** | **45–60 min** — the figure the lab's own `README.md` states ("This add-on lab (45–60 min)"). This is *not* a full contact session |
| **Lab folder** | `labs/lesson10-vpc-networking` |
| **Targets** | `vulnerable_app.py` on **:8113** · `fixed_app.py` on **:8114** (`docker-compose.yml`) |
| **Signature exercise** | "The Deny Rule That Never Runs" |
| **Standards** | **CWE-863** (Incorrect Authorization) · **CWE-284** (Improper Access Control) — the lab README's and `lesson.yml`'s own classification |
| **CLOs addressed** | **CLO2** demonstrate · **CLO3** apply the control (schedule row, `docs/course-specification.md` §6). Via §4's alignment table the per-student flag also carries **CLO5**, and the *Audit-the-AI* / *EiPE* tasks carry **CLO1** and **CLO4** |
| **Slides** | ⬚ — `slides/` in this course is deliberately empty (`slides/README.md`); no original deck exists for this lesson |
| **Weekly quiz** | ⬚ — none authored here; knowledge checks for this topic run inside the AWS Learner Lab (`quizzes/README.md`) |
| **Session date / room / section roster / grading scale / PLO list** | ⬚ — institution-specific, recorded nowhere in this repository (`docs/course-specification.md` header, §5, §8) |

> **Naming note.** The lab folder, README and worksheet call this **Lesson 10** — the *AWS lesson
> number* it attaches to. The curriculum monorepo (`courses/cloud-infrastructure-security.yml`)
> lists the same lesson at **slot 7** of 11 total schedule slots — only 10 of which carry an add-on
> (slot 11 is the AWS-graded "Reflection & Wrap-up" review, not an add-on lesson). Both labels refer
> to the same material; use "Lesson 10" with students, since that is what the worksheet header and
> the `Lesson<NN>_<StudentID>.pdf` submission convention use.

---

## 1. Session objectives

By the end of this add-on a student can:

**Knowledge (K)**
- K1 — State the difference between a **security group** (stateful, instance-level, allow-only) and
  a **network ACL** (stateless, subnet-level, allow **and** deny, evaluated in strict rule-number
  order) — the lab README's first objective and worksheet Q1/Q2.
- K2 — Say what "stateless" actually means for a **response packet**, using a concrete example such
  as an inbound rule that allows traffic to a web server on port 443 (worksheet Q1b).
- K3 — Explain precisely why NACL rules are evaluated **in ascending rule-number order, stopping at
  the first match**, and why that makes a broad rule at a low number able to render a narrower,
  more "correct-looking" rule at a higher number **completely unreachable while still being visibly
  present in the rule list** (README objective 2, worksheet Q3).
- K4 — Explain, in general terms, why a **NAT gateway** lets instances in a private subnet initiate
  outbound connections without exposing them to unsolicited inbound connections from the internet,
  and why it sits in a **public** subnet although its users sit in a private one (README objective
  3, worksheet Q4).
- K5 — State the fix as **two changes together**, not one: scope the allow down to the internal CIDR
  that actually needs it (`10.0.1.0/24`, not `0.0.0.0/0`) **and** keep that narrower rule at a lower
  rule number than the broad catch-all deny (README "Why it's exciting"; `nacl_engine.py`
  `NACL_RULES_FIXED` comment). It is *not* "swap allow and deny".

> **Design gap — K1/K2/K4 are Conventional-arm-only in practice.** These five objectives read as if
> every student reaches all of them, but §6's assessment table (checked against `worksheet.md`)
> shows the AIR-Sec arm's own tasks (Part 2a–2c) assess only **K3** and **K5**; K1 (SG vs. NACL), K2
> (statelessness for a response packet) and K4 (NAT gateway) are graded exclusively through Part 1's
> essay questions — and worksheet.md's own instruction is to "complete only the part assigned to you
> this block" (§4b), so a Block 2 AIR-Sec-arm (Section B) student never does Part 1. That student's
> only contact with K1/K2/K4 that block is the 0:00–0:05 framing recall and the AWS Learner Lab
> prerequisite (§3), neither of which is assessed here. This is a worksheet/assessment-design
> question for whoever maintains `worksheet.md`, not something to silently fix by narrowing this
> objective list — flag it alongside the other open design items in §4b and §9.

**Skills (P)**
- P1 — Stand the pair up and read the ordered rule list with `GET /rules` on **both** apps, and say
  which rule numbers exist and in what order.
- P2 — Send `POST /check-access` with the external source IP `203.0.113.55` on port `5432` against
  **:8113**, obtain `{"action": "allow", ...}` **and the flag**, and read `matched_rule_number` back
  as **90**.
- P3 — Send the **identical** request against **:8114**, obtain `{"action": "deny", ...}` with
  `matched_rule_number` **100** and **no flag**, and explain what changed.
- P4 — Point at the exact difference between the two rule lists that produces those two outcomes,
  in the student's own words.
- P5 — Find the planted flaw in the three-rule AI-generated NACL summary in worksheet **2b** and
  state, in plain English, what actually happens both to an external IP and to a request from the
  CIDR the AI claims is allowed.

**Attitude (A)**
- A1 — Attack only the two approved targets — the local Docker labs in `labs/` and the student's own
  assigned Learner Lab sandbox ([ETHICS.md](../../ETHICS.md)). A database port on anything else,
  including "just to look", is out of bounds.
- A2 — Submit evidence that is attributable to themselves — their own flag, with `whoami` / student
  ID / a timestamp visible — and be able to reproduce the capture live on request
  ([SUBMISSION.md](../../SUBMISSION.md)).
- A3 — Treat AI-generated cloud configuration as something to verify against documented behaviour,
  not to trust (worksheet 2b; spec CLO4).

## 2. Key idea (the through-line)

Every rule in this lab's rule list is, read on its own, defensible. `allow` on the database port for
the app tier is what you want. `deny 0.0.0.0/0` on the database port is the secure default you would
hope to find. Nobody wrote a *wrong rule*. The bug is entirely in the relationship between two
rules: how broad each one is, and which rule **number** it was given. Because NACL evaluation walks
the list in ascending rule-number order and **stops at the first match**, a rule that was probably
meant to say "our app tier can reach the database" but was written as `0.0.0.0/0` and placed at #90
decides the outcome for the entire internet — and the deny-all sitting at #100 never executes. It is
dead code that looks like a control. A reviewer scrolling the rule list sees a locked-down database
and is wrong.

That is why the fix has to be two changes at once. Narrowing the allow without moving it, or moving
the deny without narrowing the allow, each leaves a shadowing relationship in place — and a deny-all
placed ahead of *any* allow, however well scoped, shadows that allow in exactly the same way
(`nacl_engine.py`, `NACL_RULES_FIXED` comment). The lesson generalises beyond NACLs: wherever
evaluation is first-match-wins, **specificity has to be ordered ahead of generality**, or the
specific rule is decoration.

## 3. What students must have completed before this add-on

**In the AWS Academy Learner Lab (first, and graded by AWS):**
- That lesson's AWS Academy module and its Knowledge Check ([SUBMISSION.md](../../SUBMISSION.md) —
  AWS first, add-on second; the knowledge checks run inside the Learner Lab, `quizzes/README.md`).
- The real **VPC networking exercise** — creating public and private subnets, a NAT gateway,
  security groups and a custom network ACL. The lab README is explicit that this is still where the
  actual AWS console UI is learned and where NAT gateway routing is seen live. Nothing in this
  add-on re-teaches or replaces it.

**On their own machine:**
- Docker Desktop working.
- A working host Python for `exploit.py`, plus the `requests` package — see §7 risk 1 before the
  room types the README's command block.

**Instructor, before the session:**
- Pre-build the images so a whole room is not pulling `python:3.12-slim` and running
  `pip install --no-cache-dir -r requirements.txt` at once (`Dockerfile`).
- Mint the per-student flags: `python3 instructor/seed_flags.py env <STUDENT_ID>` — this emits a
  `FLAG_NACL=…` line among the others. The shim needs the curriculum monorepo as a sibling directory
  and `CIS_FLAG_SALT` (or the legacy `FLAG_SALT`) exported. Without it, every student's container
  uses the same public default baked into `docker-compose.yml` and the attributability control is
  void.
- Re-read `instructor/lesson10-vpc-networking-answer-key.md` (git-ignored, instructor-held) against
  the current worksheet, and read §9 of this plan before grading.
- Confirm host ports **8113** and **8114** are free (`course-plan.md` allocates 8104–8117 across the
  labs — confirmed non-colliding, but another lesson's containers may still be running).

## 4. The add-on session — minute by minute

> **Where these minutes come from.** The task *names and content* below are the worksheet's and
> README's own; the **minute split is this plan's allocation** inside the 45–60 min envelope the lab
> README states. Neither the README, the worksheet nor the code carries a per-task budget — do not
> treat these numbers as fixed course material, and do not "correct" the lab to match them.

**Kickoff commands, exactly as the lab README's "Run it" block has them:**

```bash
cd labs/lesson10-vpc-networking
docker compose up -d --build   # vulnerable_app.py on :8113, fixed_app.py on :8114
pip install requests           # once, on the host
python exploit.py
```

(The README's step 2 gives the shorter kickoff `docker compose up -d`; use the `--build` form above
on a first run. See §7 risk 1 before the class types the last two lines — on a host with only
`python3`/`pip3` they fail as written.)

### 4a. AIR-Sec arm — Block 2 = **Section B** — 60-minute plan

| Time | Task | Student does | Evidence produced |
|---|---|---|---|
| 0:00–0:05 | **Framing** | Recall what the Learner Lab exercise already built (subnets, NAT gateway, security groups, a custom NACL); hear today's question — *not* "is this rule right?", but "which rule gets to decide?" | — |
| 0:05–0:10 | **Stand the target up** | `cd labs/lesson10-vpc-networking` then `docker compose up -d --build`; confirm both services answer on `/ping` (`mode` is `vulnerable` on :8113, `fixed` on :8114) | Screenshot of both `/ping` responses |
| 0:10–0:18 | **Worksheet 2a, baseline** | `GET /rules` on **both** apps (worksheet 2a; the README's own signature-exercise step 1 only calls for either app) — write down each rule list in ascending order and note that both apps carry a `deny 0.0.0.0/0` at **#100** | Two rule lists side by side — the deny-all is present on *both* |
| 0:18–0:30 | **Worksheet 2a, the capture** | `POST /check-access` with `source_ip` `203.0.113.55` (a public documentation-range address) and `port` `5432` against **:8113** → `{"action": "allow", …}`, `matched_rule_number` **90**, plus the flag | The exact request (`source_ip`, `port`), the captured flag, and the matched rule number |
| 0:30–0:38 | **Worksheet 2a, confirm the fix** | The **identical** request against **:8114** → `{"action": "deny", …}`, `matched_rule_number` **100**, no flag; then name the one difference between the two `#90` rules | The 2nd response + which rule number matched first in each case, in the student's own words |
| 0:38–0:48 | **Worksheet 2b — Audit-the-AI** | Walk the AI's three-rule summary (#10 / #20 / #30) in ascending order for an external IP **and** for a request from the CIDR the AI claims is the real app tier; decide whether rule #30 ever runs for either | Written answer (start in class, finish as homework) |
| 0:48–0:56 | **Worksheet 2c — EiPE + simplification debrief** | 3–4 sentences a non-technical stakeholder could follow, plus the one-sentence rule of thumb about where a narrow rule goes relative to a broad one; then the instructor walks §5 out loud (what this simulation is *not*) | Written answer + nobody leaves with a wrong model of NACLs or security groups |
| 0:56–1:00 | **Submit + tear down** | Confirm the submission bundle; `docker compose down` | `Lesson10_<StudentID>.pdf` + the flag → Google Classroom |

**Optional one-shot check.** `python exploit.py` (host, `requests` installed) runs `GET /rules` and
the external-IP `POST /check-access` against both targets and prints two `PASS` lines, exiting `0`.
It is a convenience, not the assessment: worksheet 2a asks for *the exact request the student sent*,
so anyone who takes that route must still be able to state and repeat it by hand.

**Compressing to 45 minutes.** Keep 0:00–0:38 intact — the rule-list baseline, the capture and the
fixed-app comparison are the assessed core and the only part that needs the containers running. Send
2b and 2c home as written work and replace the 0:48–0:56 debrief with a two-minute version of §5
(no security groups in the code at all; statefulness not modelled; CIDR matching simplified).

**Checks for understanding**
- After the two rule lists: cold-call — *"both apps deny the whole internet on the database port at
  rule #100. One of them is wide open. How can that be?"*
- After the capture: *"which rule number decided this, and what did it stop the evaluator from ever
  looking at?"*
- The misconception to hunt for explicitly: *"so deny rules should always come first?"* — no. A
  `deny 0.0.0.0/0` placed ahead of a well-scoped allow shadows the allow in exactly the same way and
  locks out the legitimate app tier. The principle is **specific before general**, not "deny first"
  (`nacl_engine.py`, `NACL_RULES_FIXED` comment).
- Exit ticket (one sentence): *"name one rule you could add to the fixed app that would break it
  without changing any existing rule."*

### 4b. Conventional arm — Block 2 = **Section A**

The worksheet's own instruction is *"complete only the part assigned to you this block"*, and Part 1
— five essay questions on security groups vs. network ACLs, the allow/deny expressive-power
difference, why first-match-in-ascending-order evaluation is the rule, the NAT gateway's purpose and
"outbound only", and a real-world consequence of an internal service reachable from the internet —
carries **no flag and no AI-resilience layer**, which is exactly the manipulation `course-plan.md`
describes. Use the slot for guided discussion of those five questions; the exploit is not run in this
arm.

⬚ **Not fixed anywhere in this repository:** whether the Conventional section also stands the local
Docker target up in class. Running the exercise for them would import part of the AIR-Sec treatment
into the control arm; leaving it out means the concept is assessed by writing only. Decide this once,
apply it to every Conventional-block lesson, and record it — it is a study-design decision, not a
per-lesson one. (The same ⬚ is open in the Lesson 5 plan.)

## 5. Where this simulation departs from real AWS — say this out loud

The lab is a pair of small local Flask services standing in for one narrow slice of NACL behaviour,
and the course specification (§2, §7) requires the departures to be named in the same breath as the
exercise. Everything below is visible in the lab's own source.

1. **There are no security groups in the code at all.** The stateful/stateless comparison is
   objective #1 of this lesson and is assessed **by essay only** — nothing in `nacl_engine.py`
   models a security group, and nothing models statefulness. In particular the simulation cannot
   show the thing that makes stateless filtering bite in practice: a real NACL evaluates outbound
   return traffic against its own outbound rules, so an inbound allow without a matching outbound
   rule silently breaks the reply. There is one undirected rule list here and no notion of a
   response packet.
2. **CIDR matching is deliberately simplified and ignores the prefix length.** `_cidr_matches()` —
   whose own docstring says it is "deliberately simplified … for teaching purposes" — treats
   `0.0.0.0/0` as "everything" and otherwise compares only the **first three octets** of the network
   address. Verified consequences on the running fixed app: `10.0.1.999` — not a valid IPv4 address
   at all — is matched by `10.0.1.0/24` and allowed; and a `/16` or `/8` written in a rule would
   *not* behave the way its notation says. Real NACL matching is subnet-mask arithmetic. Say this
   before a student generalises the prefix trick into a mental model.
3. **Port matching is exact integer equality.** There is no protocol field, no port range, and no
   separate inbound/outbound rule sets — a real NACL rule carries all three. Verified: sending
   `"port": "5432"` as a JSON **string** matches nothing and falls through to the implicit deny on
   both apps (see §7 risk 3).
4. **No subnets, no route tables, no NAT gateway, no internet gateway exist in this lab.** The
   public/private subnet split and the NAT gateway are conceptual for this add-on — they are taught
   and seen live in the Learner Lab, and assessed here on the worksheet (Q4 / README objective 3).
5. **The implicit default deny is modelled, but not as a visible rule.** When nothing matches,
   `evaluate()` returns `deny` with `matched_rule_number: null` (verified on both apps with port
   `22`). A real NACL shows this as an explicit `*` row at the bottom of the rule list, which is
   pedagogically useful and is absent here.
6. **The rule numbers are realistic but the set is tiny.** `nacl_engine.py`'s comment notes that
   AWS's real rule-number range is 1–32766 and that the convention is reused "purely for realism";
   this lab uses exactly two rules, #90 and #100.
7. **The two apps' request-handling code is identical.** `vulnerable_app.py` and `fixed_app.py`
   differ only in which rule list they import (`NACL_RULES_VULNERABLE` vs `NACL_RULES_FIXED`). Show
   this — it is the point. The vulnerability is in *configuration data*, not in code, which is what
   makes it survive code review.
8. **Nothing in AWS ever returns a flag.** The flag is this course's attributable-evidence
   mechanism, not modelled AWS behaviour — and see §9(1) for a defect in how it is gated here.
9. **Both apps run Flask's built-in development server** (`app.run(host="0.0.0.0", port=5000)`)
   inside the container, published on 8113 and 8114. A teaching target, not a hosting stack.

## 6. Assessment

| Instrument | Evidence | Outcome | Weight |
|---|---|---|---|
| Worksheet Part 2a (AIR-Sec arm) | The exact request (`source_ip`, `port`) that produced the flag on `:8113`; the captured flag; the identical request against `:8114` and its response; `GET /rules` on both apps with the rule number that matched first in each case | K3, K5, P1–P4, A2 | Part of the worksheet mark (`docs/course-specification.md` §4) |
| Worksheet Part 2b — *Audit-the-AI* | The planted flaw in the three-rule AI summary, named, with what actually happens to an external IP **and** to the CIDR the AI claims is allowed | K3, P5, A3 · CLO1/CLO4 per §4 | Part of the worksheet mark |
| Worksheet Part 2c — *EiPE* | 3–4 sentences a non-technical stakeholder could follow + the one-sentence rule of thumb on placing a narrow rule relative to a broad one | K3, K5 · CLO4 | Part of the worksheet mark |
| Worksheet Part 1 (Conventional arm) | Five essay answers — graded on the writing itself | K1, K2, K3, K4 | The Conventional arm's whole submission |
| **Per-student flag** — challenge key `nacl`, injected as `FLAG_NACL` | The flag value returned by the **vulnerable** app's `/check-access` response for an external IP on port 5432 | A2 · CLO5 | Integrity control that also carries marks (spec §8) |
| Viva / random live check | Live reproduction of the capture and an explanation of why the deny-all at #100 never ran | P1–P4, A2 | Pass / flag for follow-up ([SUBMISSION.md](../../SUBMISSION.md)) |

**How the flag control works — and its limit in this lesson.** Flags are minted per student from the
student ID (`instructor/seed_flags.py`, challenge key `nacl`, salted with `CIS_FLAG_SALT`), so a
copied flag is traceable to the student it was *issued* to rather than being a matter of judgement.
**But in this lab the fixed app is not flagless**: verified on the running containers, a request from
inside the internal CIDR (`{"source_ip": "10.0.1.25", "port": 5432}`) to **:8114** returns
`action: allow` *with the flag attached*, because both apps gate the flag on `action == "allow" and
port == 5432` rather than on the vulnerable rule set. `matched_rule_number` is **90** in that case
too, so it does not discriminate either. See §9(1). **Grade the triple, not the flag string:** the
flag must arrive alongside an **external** `source_ip` in the same response body *and* a `GET /rules`
listing showing `allow 0.0.0.0/0` at #90. Worksheet 2a already asks for exactly those three things,
so this needs no change to the lab.

Be honest about what that buys. The triple catches the **accidental** `:8114` route — the student who
took the internal-CIDR path and reported it truthfully. It does not catch a deliberate one: the
external `source_ip` and the vulnerable app's rule listing are both printed in the lab README's own
captured-output block, so a student holding their own seeded flag from `:8114` can copy both. Stated
precisely: possession of a per-student flag in this lesson proves the student ran a container seeded
for them, **not** that they exercised the vulnerable path. The control that closes the deliberate
route is the **viva / random live check** in the table above — use it here rather than treating the
flag as self-evidencing.

**Deliverable, per the lab README.** The captured flag + the exact request (`source_ip`, `port`) that
produced it + a one-paragraph explanation of why a visibly-present "deny all" rule at a higher rule
number can still be completely unreachable — it is not that the deny rule is wrong, it is that a
broader rule ahead of it already decided the outcome.

**Submission.** Worksheet exported to PDF with screenshots embedded, named
`Lesson10_<StudentID>.pdf`, plus the captured flag → Google Classroom, before the next class session;
AI-tool disclosure required; late −10%/day up to 3 days ([SUBMISSION.md](../../SUBMISSION.md)).
Evidence must show the student's own `whoami` / login / student ID and a timestamp.

**Grading scale, and this layer's share of the final grade: ⬚** — an institutional decision recorded
nowhere in this repository (`docs/course-specification.md` §4, §8). The AWS-graded ~40% is scored by
AWS and is identical for every student; it is not part of this add-on.

## 7. Risks and contingencies

| Risk | Mitigation |
|---|---|
| **1. The README's host commands assume `python`/`pip` are on PATH.** Verified on this machine: only `python3` and `pip3` exist, so `pip install requests` and `python exploit.py` both fail as written | Have students use `python3 -m pip install requests` / `python3 exploit.py`, or a virtual environment if the host Python refuses a global install. Announce it before the room types the block. **Do not edit the lab to fit the room** — escalated in §9(2) |
| **2. Hand-crafted `POST /check-access` without a JSON content type returns `400`.** Verified: `curl -d 'source_ip=…&port=5432'` (form encoding) yields `{"error":"source_ip and port are required"}`, because the app reads `request.get_json(silent=True)`. Students conclude the lab is broken | Show the working shape once on the projector: an explicit `Content-Type: application/json` header (or `curl --json`) with a JSON body. `exploit.py` already sends JSON |
| **3. `"port": "5432"` as a JSON *string* silently denies on the vulnerable app.** Verified: the engine compares `rule["port"] == port`, so a quoted port matches nothing and returns `action: deny`, `matched_rule_number: null`. A student reads that as "the vulnerable app isn't vulnerable" and stops | If a student's request denies on `:8113`, check the payload types first — `5432` unquoted, `"203.0.113.55"` quoted. Escalated as a lab-hardening suggestion in §9(6) |
| **4. The fixed app *does* return the flag** for an internal-CIDR request on port 5432 (verified), so a student can obtain a flag from `:8114` without ever exercising the vulnerable path — and the README's own text tells them `10.0.1.25` is allowed there | Grade the triple described in §6: flag **plus** an external `source_ip` in the same response body **plus** the `#90 allow 0.0.0.0/0` rule listing. `matched_rule_number` is 90 in both cases and cannot be used to tell them apart. Escalated in §9(1) |
| **5. `exploit.py` cannot be run inside the container.** The `Dockerfile` copies only `nacl_engine.py vulnerable_app.py fixed_app.py`, so the script is not in the image even though `requests` is installed there | Run it from the host as the README says, or skip it — the two requests are short enough to make by hand, and worksheet 2a wants the student's own request anyway |
| **6. Ports 8113/8114 already bound** — usually another of this course's labs still running (`course-plan.md` allocates 8104–8117 across the labs) | `docker compose down` in the other lab folder before starting; or a student republishes the ports in their own working copy |
| **7. Everyone submits the same flag.** `docker-compose.yml` bakes a public default `FLAG_NACL` that is also printed in the lab README's captured output, so an unseeded cohort produces one identical flag class-wide and the attributability control silently does nothing | Seed per student before the session (`python3 instructor/seed_flags.py env <STUDENT_ID>`); the README also documents the inline override form `FLAG_NACL=FLAG{...} docker compose up`. Spot-check two submissions for distinct values |
| **8. `seed_flags.py` is a thin shim and can refuse to run.** It exits with an error unless the curriculum monorepo sits as a sibling directory, and it needs `CIS_FLAG_SALT` (or the legacy `FLAG_SALT`) exported | Run the seeding step the day before, not five minutes before class; keep the salt out of the repo, out of Classroom posts and out of screenshots |
| **9. First `docker compose up -d --build` builds `python:3.12-slim` and pip-installs `flask`/`requests` for the whole room at once** | Pre-build before the session; set it as homework on a shared link; keep an offline image copy (`docker save`/`docker load`) |
| **10. Ethics drift into real infrastructure.** This lesson's payload is literally "can I reach a database port from outside?" — the one exercise in the course most likely to tempt a student to try it against something real, including their own Learner Lab's resources or a campus host | Restate ETHICS.md rules 1–2 at the start and again before students switch back to the AWS console: the local labs and the student's own sandbox are the only approved targets, and probing real infrastructure can suspend the whole class's accounts. `203.0.113.55` is a documentation-range address precisely so nothing real is implied |
| **11. Arm mix-up between sections.** This is **Block 2**, where the arms are reversed: Section A runs Conventional (Part 1), Section B runs AIR-Sec (Part 2). A student who completes the wrong part produces evidence that cannot be graded for their arm and contaminates the study data — and this worksheet's header does **not** state the reversal (§9(5)) | State the assigned part on the board and in the Classroom post at the start of the session; the worksheet's first line already says to complete only the assigned part, but say which part that is out loud |
| **12. The "deny first" over-correction.** Students who take away "put the deny at the lowest number" have learned a rule that breaks the fixed app | Handle it in the §4 check-for-understanding while the containers are still up: ask what happens to `10.0.1.25` if `deny 0.0.0.0/0` were renumbered to #80 |

## 8. Materials

- **Lab:** `labs/lesson10-vpc-networking/` — `README.md`, `worksheet.md`, `nacl_engine.py`,
  `vulnerable_app.py` (`:8113`), `fixed_app.py` (`:8114`), `exploit.py`, `docker-compose.yml`,
  `Dockerfile`, `requirements.txt` (`flask>=3.1.3`, `requests>=2.33.0`)
- **Instructor-held (git-ignored):** `instructor/lesson10-vpc-networking-answer-key.md` ·
  `instructor/seed_flags.py` · `instructor/check_flag_keys.py`
- **Course documents:** [course-specification.md](../course-specification.md) ·
  [course-plan.md](../../course-plan.md) · [SUBMISSION.md](../../SUBMISSION.md) ·
  [ETHICS.md](../../ETHICS.md) · [CLAUDE.md](../../CLAUDE.md)
- **Student machine:** Docker Desktop; `requests` on the host Python for `exploit.py`
- **Slides:** ⬚ — none; `slides/` is intentionally empty for this course
- **Reference, as listed in the lab README (all publicly available AWS documentation — no AWS
  Academy file is used, quoted or copied):** AWS VPC documentation *Control subnet traffic with
  network access control lists* (ascending-order, first-match evaluation); *Compare security groups
  and network ACLs* (stateful/allow-only vs. stateless/allow-and-deny); *NAT gateways* (outbound
  connections from a private subnet, no externally initiated inbound)
- **Baseline curriculum:** the AWS Academy Learner Lab itself — accessed through AWS, never mirrored
  here

## 9. Instructor notes escalated from lab content

Recorded here rather than fixed: student-facing lab material and its curriculum-monorepo copy are
parity-gated, and editing graded material so a plan reads tidily is exactly what must not happen.

1. **The fixed app emits the flag — the control app is not flagless.** Verified on the running
   containers: `POST /check-access {"source_ip": "10.0.1.25", "port": 5432}` against **:8114**
   returns `action: allow` with the flag attached, because both apps gate the flag on
   `action == "allow" and port == 5432` (`fixed_app.py` lines 28–29, identical to
   `vulnerable_app.py`) rather than on the vulnerable rule set. The route is *documented to
   students*: the lab README's verification paragraph states that a request from `10.0.1.25` on port
   5432 is allowed on the fixed app. Consequences: (a) it breaks this repo's own standing rule —
   `CLAUDE.md`, "The fixed/control app must never emit a flag", which exists because
   `FLAG_REMEDIATE` once leaked from a control app; (b) it makes `docs/course-specification.md` §9's
   claim — "The control ('fixed') application in each lab never emits a flag — evidence of a flag is
   evidence the student exploited the vulnerable path" — **overstated for this lesson**. The
   answer key's expected 2a evidence does include the external `source_ip` and both `/rules`
   listings, so a careful grader still catches a *careless* `:8114` shortcut — but not a deliberate
   one, since both of those elements are printed in the README's own captured-output block and can
   simply be copied. The flag string alone is not attributable to the vulnerable path. Smallest
   honest fix: gate the flag in `fixed_app.py` on something the fixed rule set can never satisfy, or
   remove the flag branch from `fixed_app.py` entirely. Until that lands, the §6 triple plus the
   viva is the grading workaround — the workaround does not remove the need for the lab-side fix.
2. **Host command forms.** The README's `pip install requests` / `python exploit.py` fail on a host
   that has only `python3`/`pip3` (verified on this machine — `python` and `pip` are absent from
   PATH). The `python3 -m pip install requests` / `python3 exploit.py` forms work everywhere the
   current ones do. Identical to the finding already escalated in the Lesson 5 plan.
3. **Duration conflict — course-wide, verified.** The lab README states this add-on is
   **45–60 min**; the curriculum monorepo's `lessons/vpc-networking/lesson.yml` carries
   `duration_min: 180`, which is the sibling courses' full-lab length, not this course's add-on
   length. This plan follows the README. Checked directly: **all ten** of this course's lessons in
   the monorepo (`aws-fundamentals-intro`, `ec2-lambda-beanstalk`, `s3-static-site-lambda-sns`,
   `load-balancing-autoscaling`, `iam-policy-evaluation`, `cloudtrail-monitoring`, `vpc-networking`,
   `kms-envelope-encryption`, `s3-versioning-lifecycle-replication`, `config-lambda-remediation`)
   carry `duration_min: 180`. It is a course-wide default, not a per-lesson slip, and it means the
   monorepo would schedule three-hour blocks for 45–60-minute add-ons. Worth one fix across all ten
   manifests rather than ten separate ones.
4. **Kickoff command inconsistency.** README step 2 gives `docker compose up -d` while the "Run it"
   block gives `docker compose up -d --build`; on a first run only the second builds the images.
   Same inconsistency as Lesson 5's README.
5. **The worksheet header does not state the Block 2 reversal.** `labs/lesson10-vpc-networking/
   worksheet.md` opens with the generic line "Section is assigned Block 1 = AIR-Sec or Block 2 =
   Conventional per `course-plan.md`'s block table", which describes Section A's assignment only —
   for Section B, Block 2 is the AIR-Sec arm. The other two Block 2 lessons handle this better:
   `lesson07b-cloudtrail-monitoring/worksheet.md` spells the reversal out per section, and
   `lesson14-config-lambda-remediation/worksheet.md` at least adds "(Lesson 14 falls in Block 2.)".
   Aligning this worksheet's header with lesson07b's wording would remove a real chance of a section
   completing the wrong arm.
6. **Type-sensitivity produces a silent false negative.** `evaluate()` compares
   `rule["port"] == port`, so a JSON string `"5432"` matches no rule and returns the implicit deny
   (verified). A student hand-crafting the request in a client that quotes numbers sees the
   *vulnerable* app deny them and may conclude there is nothing to find. A coercion or a 400 on a
   non-integer `port` would turn a silent wrong answer into a visible error. Teaching-content
   change, not a security fix — do not apply it mid-term without updating the answer key.
7. **The prefix-length shortcut is discoverable by students.** `_cidr_matches()` allows
   `10.0.1.999` under `10.0.1.0/24` (verified). The docstring is honest that this is simplified, but
   the README and worksheet do not mention it, so a student who probes it has found a "bug" the
   lesson never acknowledges. Covering it verbally is handled in §5(2); a one-line note in the
   worksheet's 2a would make it a teaching moment instead of a distraction.

## 10. Post-teaching reflection

*Complete after the session — this also feeds the course's engagement data.*

- Attendance / completion: ⬚
- Time actually taken per segment (vs. the allocation in §4): ⬚
- Did the 45–60 min envelope hold, or did the AWS Learner Lab exercise overrun into it: ⬚
- Where the class got stuck, and what unblocked them (JSON content type? quoted `port`? the rule
  lists?): ⬚
- Did anyone take away "put the deny first" rather than "specific before general"? What corrected
  it: ⬚
- Quality of the *Audit-the-AI* (2b) answers — did students spot that the AI's rule #30 never runs,
  and did they work through *both* the external and the internal case: ⬚
- Did any misconception survive the §5 debrief — especially "security groups and NACLs are the same
  thing with different names", or the simplified CIDR matching: ⬚
- Flags: all distinct? Any submitted flag that arrived without an external `source_ip` and the
  `#90 allow 0.0.0.0/0` rule listing (see §6 / §9(1))? Any duplicates to follow up: ⬚
- Anything to change before this add-on runs again: ⬚
