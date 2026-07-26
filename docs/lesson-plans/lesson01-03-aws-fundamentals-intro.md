# Lesson Plan — Lessons 1–3 Add-on: AWS Fundamentals (Shared Responsibility & IAM Basics)

| | |
|---|---|
| **Course** | Cloud Infrastructure & Security (⬚ course code) |
| **AWS lesson this attaches to** | AWS Academy **Modules 1–3** — Cloud Foundations intro, security fundamentals, IAM/access-securing concepts — and their Knowledge Checks |
| **Kind** | **CONCEPTUAL** — no exploitable target, no Docker, no flag |
| **Block** | 1 |
| **Duration** | **45–60 min, no Docker** (the lab README's own figure) — the add-on only; the AWS Academy Learner Lab work is the separate, prior baseline |
| **Lab folder** | `labs/lesson01-03-aws-fundamentals-intro` (`README.md`, `worksheet.md` — no code files this lesson) |
| **Slides / quizzes** | None authored here, deliberately — see §6 |
| **Analogous CWE** | CWE-269 (Improper Privilege Management) / CWE-287 (Improper Authentication) — as categories describing the *misconceptions* this lesson corrects, not a coding bug in any artefact |
| **CLOs addressed** | **CLO1** shared responsibility · **CLO4** evaluate & communicate (course specification §6) |
| **Date / section / room** | ⬚ |

> **Which arm is this section in today?** This lesson sits in **Block 1**. Under the block table
> (course specification §6, `course-plan.md`), **Section A = Block 1 AIR-Sec** → Part 2;
> **Section B = the reverse**, so Section B does **Part 1 (Conventional)** in this same lesson.
> Announce this before the worksheet is opened — see §8 and §9.

---

## 1. Session objectives

By the end of this add-on a student can:

**Knowledge (K)**
- K1 — State the Shared Responsibility Model's split precisely for an IaaS service like EC2: AWS
  secures the infrastructure (host hardware, hypervisor, physical facilities, the network fabric
  underneath); the customer secures everything placed on top — guest-OS patching, application
  software, IAM configuration, and data.
- K2 — Explain why that split moves for a fully-managed service (a managed relational database, a
  serverless function runtime), and why EC2 specifically does *not* get guest-OS patching from AWS.
- K3 — Explain IAM's **default-deny** evaluation model: a principal with no attached policy has
  **no** access, not broad access that must be manually narrowed.
- K4 — Explain why day-to-day administrative work uses an ordinary administrative IAM identity
  rather than the account root user, and why MFA on the root user is a second factor added *to*, not
  a replacement *for*, a strong password.

**Skills (P)**

*AIR-Sec arm (worksheet Part 2):*
- P1 — Compute their own variant with `variant = (last digit of your student ID) mod 4` and read
  only that passage.
- P2 — Identify the single planted factual error in their own assigned passage, quote the exact
  sentence, and state what actually happens instead.
- P3 — Write the corrected sentence.
- P4 — (2b, EiPE) Explain in 3–4 sentences a non-technical stakeholder could follow why "AWS runs
  the cloud" does not mean AWS keeps your servers patched, using the EC2 guest-OS example.
- P5 — (2c, viva) Answer the viva prompt without notes.

*Conventional arm (worksheet Part 1):*
- P6 — Answer the four essay questions in their own words: the EC2 responsibility line; guest-OS
  patching and how the answer changes for a fully-managed service; what IAM "default-deny" means and
  what a brand-new IAM user can do; why routine administration does not use the root user.

**Attitude (A)**
- A1 — Work only within the two approved targets in [ETHICS.md](../../ETHICS.md) — the local Docker
  labs in `labs/` and the student's own assigned AWS Academy Learner Lab sandbox — and treat Learner
  Lab credentials as secrets.
- A2 — Treat a fluent, confident AI explanation of an AWS concept as something to verify against
  AWS's own documentation, not to trust.
- A3 — Answer **their own** variant: the lab README states that describing someone else's variant's
  error does not satisfy the task.

## 2. Key ideas (the through-line)

Responsibility in AWS tracks **control**, not branding. AWS "running the cloud" settles who owns the
building, the hardware and the hypervisor; it says nothing about the operating system a customer
chose to boot on an EC2 instance, because AWS deliberately never reaches inside it. Move up the
managed-service ladder and the line moves with it — the further a customer is from shell access, the
more of the stack AWS takes over. IAM is the same principle approached from the other end: nothing is
permitted until something explicitly permits it, so a new identity starts with nothing rather than
with everything-minus-restrictions.

The teaching move this lesson makes is deliberately awkward: the four passages in the worksheet
*sound* right. They are fluent, confident and structurally correct, and each carries exactly one false
claim. Vocabulary alone will not catch it; only a student who has internalised who is responsible for
what will. That is the point of the exercise, and it is also the CLO4 skill — evaluating someone
else's confident cloud-security claim against AWS's documented behaviour.

## 3. What students must have done first (AWS Learner Lab baseline)

The AWS Academy lab is the baseline and comes **first**; this add-on assesses the same concept
afterwards, and does not re-teach it.

- **Before this session** — complete the real AWS Academy **Modules 1–3** in the Learner Lab sandbox:
  intro to cloud concepts, security fundamentals, and the IAM Knowledge Checks (lab README, step 1).
  AWS grades that portion; nothing here alters it.
- **From Lesson 1's one-time setup** ([SUBMISSION.md](../../SUBMISSION.md)) — joined the Google
  Classroom, accepted the AWS Academy Learner Lab invite, installed Docker Desktop + Git, and
  confirmed they can start their Learner Lab and reach the AWS console.
- **Signed** the ETHICS.md acknowledgment (ETHICS.md states this is signed in Lesson 1).

**Instructor, before the session**
- Confirm and be ready to state which arm this section is in for Block 1 (§8 explains why this cannot
  be left to the worksheet's own opening line).
- Post the worksheet in Classroom; have the lab README's References list to hand — the AWS Shared
  Responsibility Model page and the IAM User Guide pages are the authoritative sources students are
  expected to check their correction against.
- Nothing to pull, build or start: this add-on has no Docker target.

## 4. Add-on run sheet — 45–60 min

> The per-row minutes below are **this plan's allocation** inside the 45–60 min envelope the lab
> README states; the lab states the envelope, not the split. The tables are built to the **45-minute
> floor** so they still fit on a short day — §4.3 says what the extra 15 minutes buys.
>
> The two arms are **alternatives, not a sequence**. A student does 4.1 *or* 4.2, never both.

### 4.1 AIR-Sec arm — worksheet Part 2 (Section A in Block 1)

| Time | Task | Student does | Evidence produced |
|---|---|---|---|
| 0:00–0:05 | **Frame the add-on** | Hears which arm this section is in, that Modules 1–3 are the prerequisite, and that today assesses that concept rather than adding AWS content; notes that no Docker or console access is needed | — |
| 0:05–0:10 | **Compute the variant** | `variant = (last digit of your student ID) mod 4`; writes the variant number and the ID's last digit at the top of the sheet; reads **only** that passage | Variant number recorded before reading |
| 0:10–0:25 | **Part 2a — "Audit the AI" (personalized)** | Finds the single planted error in their own passage; records the exact sentence, why it is wrong (what actually happens instead), and the corrected sentence | Variant no. + quoted error sentence + explanation + correction |
| 0:25–0:35 | **Part 2b — EiPE** | Writes 3–4 sentences for a non-technical stakeholder: why "AWS runs the cloud" ≠ "AWS keeps your servers patched", via the EC2 guest-OS example | Short written answer |
| 0:35–0:45 | **Part 2c — viva spot-check + close** | 3–4 rotating students answer the viva prompt (what a customer running a deliberately old OS version or custom kernel implies about who needs control) without notes; the class then closes on *method* — how to test a confident claim against AWS's own documentation | Oral answers noted against the student |

> **Do not walk the four variants' planted errors in this session.** Part 2a is a marked deliverable
> and, under SUBMISSION.md, is not due until before the next class session — revealing any variant's
> error now marks the exercise for everyone still holding it. The four-variant walk-through belongs
> at the start of the following add-on, after the deadline has passed.

### 4.2 Conventional arm — worksheet Part 1 (Section B in Block 1)

No personalised artefact and no AI-resilience layer here — that absence *is* the manipulated
variable (`course-plan.md`), so do not add the viva or a variant to this arm.

| Time | Task | Student does | Evidence produced |
|---|---|---|---|
| 0:00–0:05 | **Frame the add-on** | As above; confirms this section answers Part 1 only | — |
| 0:05–0:15 | **Part 1 Q1** | Draws or describes the responsibility line the model draws for an EC2 instance — what specifically is AWS's, what specifically is the customer's | Written answer / diagram |
| 0:15–0:25 | **Part 1 Q2** | Guest-OS patching on EC2: whose job, and why the answer changes for a fully-managed relational database or a serverless function runtime | Written answer |
| 0:25–0:35 | **Part 1 Q3** | What "default-deny" means in IAM, and what access a brand-new IAM user has before any policy is attached | Written answer |
| 0:35–0:45 | **Part 1 Q4** | Why day-to-day administration uses an ordinary IAM identity rather than root, and what root is for instead | Written answer |

### 4.3 If the session runs to the full 60 minutes

Spend the extra 15 minutes on, in this order: (1) more viva coverage in the AIR-Sec arm — sample at
least one student per variant, which the skew in §9 makes non-automatic; (2) a worked demonstration
of the *method*, checking one confident-sounding claim against the AWS pages in the lab README's
References — use a claim that appears in none of the four passages, so nothing is given away;
(3) a Docker Desktop + Git check against SUBMISSION.md's Lesson 1 setup list, so the next add-on
(`labs/lesson04-ec2-lambda-beanstalk`, which does need `docker compose up`) does not lose its first
twenty minutes to installation.

**Checks for understanding.** Cold-call mid-session: *"who has control of the guest OS on an EC2
instance, and why does that settle who patches it?"* Before the debrief, a one-minute paper: *"what
access does a brand-new IAM user have?"* — the second one surfaces the default-deny misconception
directly, and is worth collecting even in the Conventional arm.

## 5. Assessment for this lesson

| Instrument | Evidence | Outcome | Weight |
|---|---|---|---|
| Worksheet Part 2a — "Audit the AI" (AIR-Sec arm) | Variant number, the exact error sentence, why it is wrong, the corrected sentence | K1–K4, P1–P3, CLO4 | Part of the add-on worksheet mark — this layer's share of the grade is ⬚ |
| Worksheet Part 2b — EiPE (AIR-Sec arm) | 3–4 sentence plain-English explanation | K1–K2, P4, CLO1/CLO4 | Part of the worksheet mark |
| Worksheet Part 2c — viva spot-check (AIR-Sec arm, in class) | Live answer without notes | P5, CLO4/CLO5 | Pass / flag for follow-up |
| Worksheet Part 1 — four essay questions (Conventional arm) | Written answers, graded on the writing itself | K1–K4, P6, CLO1 | Part of the worksheet mark |
| **Per-student attributable artefact** | **No flag this lesson (CONCEPTUAL)** — the attributable artefact is *which planted-error variant the student was assigned*, and identifying their own variant's error is what is attributable | A3, CLO5 | Integrity control that also carries marks (specification §8) |
| AWS Academy Modules 1–3 Knowledge Checks | Graded inside the Learner Lab | AWS's own objectives | ~40% shared AWS-graded baseline — **not** part of this layer, and identical for every section |

Marking detail (the point split and the model answers) lives in the instructor-held key,
`instructor/lesson01-03-aws-fundamentals-answer-key.md`, which is git-ignored and is not reproduced
here. The exact weight of this repository's layer within the final grade is ⬚ (specification §4
and §8).

**Submission** (SUBMISSION.md): worksheet exported to PDF → Google Classroom, named
`Lesson<NN>_<StudentID>.pdf`, with an AI-tool usage disclosure; due before the next class session
unless told otherwise; late −10%/day up to 3 days. ⬚ — SUBMISSION.md does not state which `NN` a
single add-on covering Modules 1–3 should use; fix a convention in Classroom before hand-out.

## 6. Materials

- Lab: `labs/lesson01-03-aws-fundamentals-intro/` — `README.md`, `worksheet.md`. There is no code,
  no `docker-compose.yml` and no `exploit.py` for this lesson; that is expected for a CONCEPTUAL
  add-on.
- Instructor key: `instructor/lesson01-03-aws-fundamentals-answer-key.md` (git-ignored, never
  committed).
- **Slides — none, on purpose.** `slides/` is deliberately empty: the lecture baseline is AWS
  Academy's own licensed modules, delivered through the Learner Lab and never mirrored here
  (`slides/README.md`). Any original, non-AWS slide would go in `slides/lesson01.md`.
- **Quizzes — none, on purpose.** The weekly knowledge checks run inside the Learner Lab as part of
  the licensed curriculum (`quizzes/README.md`).
- Public references named by the lab README (publicly available AWS material — no AWS Academy file
  used or copied): AWS — *Shared Responsibility Model*
  (aws.amazon.com/compliance/shared-responsibility-model); AWS IAM User Guide — *Security best
  practices in IAM*, *Policy evaluation logic*, *Root user best practices for your AWS account*.
- [SUBMISSION.md](../../SUBMISSION.md) · [ETHICS.md](../../ETHICS.md) ·
  [course specification](../course-specification.md) · [course-plan.md](../../course-plan.md)

## 7. Where this departs from real AWS behaviour — say it aloud

The repository's standing rule is that any simplification in a local simulation is labelled in the
same breath as the simulation. **This lesson has no simulation to label** — no Flask app, no Docker
target, no stand-in service. What still has to be said aloud is this:

- The four passages in `worksheet.md` Part 2a are **synthetic, AI-style text written for this
  exercise**. They are not real AWS documentation, and — per the licensing constraint that governs
  this whole repository — they are not AWS Academy material either. Each contains exactly one
  deliberate false claim.
- Students must not screenshot a passage and later cite it as an AWS statement. Point them at the
  lab README's References list for the authoritative source, and require the *corrected* sentence
  to be defensible against it.
- The lesson describes AWS's topics in our own words throughout. Nothing here is a substitute for
  the Learner Lab modules, which remain the place the actual console and its guard-rails are learnt.

## 8. Known issues in the source material — do not patch the worksheet mid-term

Both of these are defects in student-facing or shared content that this plan deliberately does not
edit; they are reported upward instead. Handle them in delivery:

1. **The worksheet's opening line conflates block with arm.** `worksheet.md` opens with *"Section is
   assigned Block 1 = AIR-Sec or Block 2 = Conventional per `course-plan.md`'s block table"*. Read
   literally, that says Block 1 is always the AIR-Sec arm — which is false for Section B, and this
   lesson is Block 1 for **both** sections. A Section B student who self-selects from that line will
   do the wrong Part. **In delivery:** state the section's arm aloud and in Classroom *before* the
   worksheet is opened, and do not let students choose their own Part.
2. **The curriculum monorepo's manifest for this lesson says `duration_min: 180`**
   (`../KOSEN69 - curriculum/lessons/aws-fundamentals-intro/lesson.yml`), which contradicts the lab
   README's *"45–60 min, no Docker"* and the course specification §1's *"45–60 min each; one 60–90
   min"*. The same 180 appears on all ten cloud lessons, so it looks like an unadjusted default
   carried over from the 3-hour sibling courses rather than a claim about this lesson. **In
   delivery:** teach to the README's 45–60 min. Do not schedule a 3-hour room from the manifest.

## 9. Risks and contingencies

| Risk | Mitigation |
|---|---|
| **Variant skew is built into the formula.** `(last digit of student ID) mod 4` maps three digits to variants 0 and 1 (0/4/8 and 1/5/9) but only two to variants 2 and 3 (2/6 and 3/7) — roughly a 30/30/20/20 split. Fewer students will have actually worked variants 2 and 3 | When choosing viva subjects, deliberately sample across all four variants rather than relying on volunteers, or variants 0 and 1 dominate the oral evidence. Hold the four-variant walk-through until the following add-on, after the Part 2a deadline — see §4.1 |
| A student computes the wrong variant, or answers a passage that is not theirs — the lab README states describing someone else's variant's error does not satisfy the task | Have every student write their variant number **and** their ID's last digit at the top of the sheet in the 0:05–0:10 slot, and check them then, not at marking time. A visible mismatch is a viva follow-up, not an automatic accusation — arithmetic slips look identical to copying at first glance |
| A student pastes their passage into an AI assistant, which confidently confirms the planted claim, or invents a different "error" | Repo policy permits AI use **with disclosure** (SUBMISSION.md), so this is not automatically misconduct — but what is graded is the student's own reasoning. Require the corrected sentence to be justified against the AWS pages in the lab README's References, and use the Part 2c viva as the tiebreak. ⬚ — the worksheet does not state whether Part 2a is closed-book on AI; fix that instruction in Classroom before hand-out if you want it closed-book |
| The passages are deliberately-false text sitting in a **public** repository; one can be screenshotted and later quoted as AWS guidance | Say at hand-out that every passage contains exactly one false claim and none of them is an AWS statement; make the corrected sentence, not the passage, the thing students keep |
| A student arrives without having completed Modules 1–3, or cannot start their Learner Lab | This add-on needs no console and no Docker, so they can still do it — run the session, and route the Learner Lab problem to the AWS-side channel and Lesson 1's one-time setup list in SUBMISSION.md. Do not spend add-on minutes debugging AWS sandbox access for one student |
| Section/arm confusion in Block 1 (see §8, item 1) | Announce the arm before the worksheet opens; post it in Classroom in writing so a late arrival cannot guess wrong |
| The temptation to "even things up" by giving the Conventional arm the viva or a variant | Do not. The absence of the personalised artefact and the AI-resilience layer *is* the manipulated variable for this block (`course-plan.md`); adding them contaminates the comparison for the whole block |
| The session runs short because there is nothing to install and nothing to exploit | Use §4.3's list in order — extra viva coverage first, then the worked method demonstration (on a claim from none of the four passages), then the Docker Desktop + Git check that `labs/lesson04-ec2-lambda-beanstalk` will need |

## 10. Post-teaching reflection

*Complete after the session — this also feeds the course's engagement data.*

- Attendance / completion: ⬚
- Which arm this section actually ran, and whether anyone did the wrong Part: ⬚
- Time actually taken per task (vs. the 45-minute floor above): ⬚
- Variant distribution as it fell out in the room, vs. the expected 30/30/20/20: ⬚
- Detection rate per variant — which planted error went uncaught most often: ⬚
- Misconception that showed up in the EiPE answers: ⬚
- Whether any student justified a correction from an AI answer rather than AWS documentation: ⬚
- Anything to change before this add-on runs again: ⬚
