# Lesson Plan — Lesson 13 add-on: S3 Data Protection (Versioning, Lifecycle, Cross-Region Replication)

| | |
|---|---|
| **Course** | Cloud Infrastructure & Security · subject code **02005097** (`course-plan.md` line 1; `docs/course-specification.md` §1 still records the course code as ⬚) |
| **AWS lesson this attaches to** | **AWS Academy Lesson 13** — the challenge lab that exercises S3 versioning, lifecycle rules and cross-region replication (topic named in our own words; **no AWS Academy file, scenario, character name or lab wording is reproduced in this plan or in the lab** — lab `README.md`) |
| **Add-on kind** | **CONCEPTUAL** — no exploitable target, no Docker, no flag (`docs/course-specification.md` §6; lab `README.md`) |
| **Block** | **2** (`docs/course-specification.md` §6). Block 2 = **Conventional for Section A**, **AIR-Sec for Section B** — the reverse of this course's Block 1 lessons (`course-plan.md`; specification §6) |
| **Duration of this add-on** | **45–60 min, no Docker** — the figure the lab's own README states. This is *not* a full contact session: the AWS Academy Learner Lab is the baseline and comes first |
| **Lab folder** | `labs/lesson13-s3-versioning-lifecycle-replication` (`README.md`, `worksheet.md` — no code files this lesson) |
| **Signature exercise** | "Audit the Backup Plan" (lab `README.md`) |
| **Analogous CWE** | **CWE-1188-adjacent** (Insecure Default Initialization of a Resource), *applied loosely* — the lab README is explicit that this lesson is about correct configuration assumptions, not a coding bug; general data-protection misconfiguration category |
| **CLOs addressed** | **CLO1** shared responsibility · **CLO4** evaluate & communicate (schedule row, `docs/course-specification.md` §6). Via §4 of the specification the per-student planted-error variant also carries **CLO5** |
| **Slides / quizzes** | ⬚ — none authored, deliberately; `slides/` and `quizzes/` in this course are intentionally empty (`slides/README.md`, `quizzes/README.md`) |
| **Date / section / room** | ⬚ |

> **Which arm is this section in today?** This lesson sits in **Block 2**. Under the block table
> (specification §6, `course-plan.md`): **Section A = Block 1 AIR-Sec / Block 2 Conventional**, and
> **Section B = the reverse**. So *in this lesson* **Section A does Part 1 (Conventional)** and
> **Section B does Part 2 (AIR-Sec)** — the opposite way round from Lessons 1–3, 4 and 5. Announce
> it before the worksheet is opened; §8 explains why this cannot be left to the worksheet's own
> opening line, which in this lesson points the wrong way for Section B.

> **Naming note.** The lab folder, README, worksheet and the submission filename all call this
> **Lesson 13** — the *AWS lesson number* it attaches to. The curriculum monorepo
> (`../KOSEN69 - curriculum/courses/cloud-infrastructure-security.yml`) lists the same lesson at
> **slot 9** of 11 schedule slots (ten add-ons plus a wrap-up). Use "Lesson 13" with students: it is
> what the worksheet header and `Lesson<NN>_<StudentID>.pdf` require.

---

## 1. Session objectives

By the end of this add-on a student can:

**Knowledge (K)**
- K1 — Explain why enabling **versioning** on a bucket protects against accidental delete *and*
  accidental overwrite, and state what actually happens to an object's prior contents when a new
  version is uploaded or a "delete" is issued (lab README, Objectives).
- K2 — Explain what a **lifecycle rule** does — transitioning older object versions to a colder,
  cheaper storage class and permanently expiring versions after a retention window — and say which
  lifecycle actions apply to the *current* version versus *noncurrent* versions.
- K3 — Explain **cross-region replication (CRR)** as a disaster-recovery strategy, including the
  precise scope of what gets replicated automatically versus what requires a separate one-time
  action.
- K4 — State precisely why enabling CRR on a bucket that already contains objects does **not** by
  itself back-copy those pre-existing objects to the destination region, and name the AWS feature
  that closes that gap.

**Skills (P)**

*AIR-Sec arm — worksheet Part 2 (Section B in Block 2):*
- P1 — Compute their own variant with `variant = (last digit of your student ID) mod 4` and read
  **only** that passage.
- P2 — Identify the single planted factual error in their own assigned passage, quote the exact
  sentence(s), and state what actually happens instead.
- P3 — Write the corrected sentence.
- P4 — (2b, EiPE) Explain in 3–4 sentences a non-technical stakeholder could follow why switching
  on cross-region replication is not an instant, one-time backup of everything already in the
  bucket, and what would actually be needed to protect years of old data the same way as new
  uploads.
- P5 — (2c, viva) Answer the viva prompt without notes: what happens to the pre-existing objects
  when the primary region is lost, and whose assumption was wrong.

*Conventional arm — worksheet Part 1 (Section A in Block 2):*
- P6 — Answer the four essay questions in their own words: recovering an accidentally overwritten
  object in a versioning-enabled bucket (and how the outcome differs without versioning); what a
  30-day transition rule does to the *current* versus *noncurrent* versions and whether those are
  the same action; whether a destination bucket holds two years of pre-existing objects the day
  after CRR is switched on, and what would be required to get them there; and whether a bucket can
  be returned to its original unversioned state, or only to the one other available state.

**Attitude (A)**
- A1 — Work only within the two approved targets in [ETHICS.md](../../ETHICS.md) — the local Docker
  labs in `labs/` and the student's own assigned AWS Academy Learner Lab sandbox — and treat Learner
  Lab credentials as secrets.
- A2 — Treat a fluent, confident AI explanation of an AWS data-protection feature as something to
  verify against AWS's own documentation, not to trust.
- A3 — Answer **their own** variant: the lab README states that describing someone else's variant's
  error does not satisfy the task.

## 2. Key ideas (the through-line)

Versioning, lifecycle rules and replication look like one feature — "backup" — and are three
different guarantees with three different scopes. Versioning is about *time*: a new upload does not
overwrite the old bytes and a delete does not destroy them, so recovery is a matter of retrieving a
version rather than restoring from elsewhere. Lifecycle is about *cost over time*, and it draws a
line the vocabulary hides — the actions that apply to the version currently being served are not the
same actions that apply to the older versions sitting behind it. Replication is about *place*, and
its scope is the one most people assume wrongly.

That last point is the lesson. A disaster-recovery plan is not a switch; it is a claim about which
objects exist in the second region and when they got there. If the claim is inherited from a
confident summary rather than checked against what the service actually does, the gap is invisible
until the day the primary region is gone — which is the only day it matters. The exercise is
deliberately awkward for that reason: the four passages in `worksheet.md` Part 2a read like a
capable assistant explaining a feature, they are fluent and structurally correct, and each carries
exactly one false claim of the kind the lab README describes as something "a rushed engineer could
genuinely believe and act on". Vocabulary alone will not catch it. That is the CLO4 skill.

## 3. What students must have done first (AWS Learner Lab baseline)

The AWS Academy lab is the baseline and comes **first**; this add-on assesses the same concepts
afterwards and does not re-teach them.

- **Before this session** — complete the real AWS Academy Lesson 13 challenge lab in their own
  Learner Lab sandbox: the challenge lab that exercises S3 versioning, lifecycle rules and
  cross-region replication (lab README, step 1). That work sits on the AWS side of the course and
  nothing here alters it — but do not tell students it carries AWS-graded weight until §5's ⬚ is
  settled.
- **From Lesson 1's one-time setup** ([SUBMISSION.md](../../SUBMISSION.md)) — joined the Google
  Classroom, accepted the AWS Academy Learner Lab invite, installed Docker Desktop + Git, and
  confirmed they can start their Learner Lab and reach the AWS console. (Docker is not needed
  *today*; it is needed for the next add-on — see §4.3.)
- **Signed** the ETHICS.md acknowledgment (ETHICS.md states this is signed in Lesson 1).

**Instructor, before the session**
- Confirm and be ready to state which arm this section is in **for Block 2** — see the header note
  and §8 item 1. This is the lesson where the worksheet's own opening line is most likely to send a
  student to the wrong Part.
- Post the worksheet in Classroom with the arm stated in writing.
- Have the lab README's References list to hand — the AWS S3 user-guide pages on what live
  replication covers, on S3 Batch Replication, on retaining multiple versions with S3 Versioning,
  and on lifecycle configuration elements. Those are the authoritative sources a correction has to
  survive.
- Read §8 item 2 before hand-out: one of the four variants' corrections is already stated in
  material students can see, which changes how that variant should be marked.
- Nothing to pull, build or start: this add-on has no Docker target and needs no AWS console.

## 4. Add-on run sheet — 45–60 min

> The per-row minutes below are **this plan's allocation** inside the 45–60 min envelope the lab
> README states; the lab states the envelope, not the split. The tables are built to the
> **45-minute floor** so they still fit on a short day — §4.3 says what the extra 15 minutes buys.
>
> The two arms are **alternatives, not a sequence**. A student does 4.1 *or* 4.2, never both.

### 4.1 AIR-Sec arm — worksheet Part 2 (Section B in Block 2)

| Time | Task | Student does | Evidence produced |
|---|---|---|---|
| 0:00–0:05 | **Frame the add-on** | Hears which arm this section is in, that the AWS Lesson 13 challenge lab is the prerequisite, and that today assesses those concepts rather than adding AWS content; notes that no Docker and no console access is needed | — |
| 0:05–0:10 | **Compute the variant** | `variant = (last digit of your student ID) mod 4`; writes the variant number and the ID's last digit at the top of the sheet; reads **only** that passage | Variant number recorded before reading |
| 0:10–0:25 | **Part 2a — "Audit the Backup Plan" (personalised)** | Finds the single planted error in their own passage; records the exact sentence(s), why it is wrong (what actually happens instead), and the corrected sentence | Variant no. + quoted error sentence + explanation + correction |
| 0:25–0:35 | **Part 2b — EiPE** | Writes 3–4 sentences for a non-technical stakeholder: why switching on cross-region replication is not an instant backup of everything already in the bucket, and what would actually be needed so years of old data are protected like new uploads | Short written answer |
| 0:35–0:45 | **Part 2c — viva spot-check + close** | 3–4 rotating students answer the viva prompt without notes — CRR enabled six months ago, no Batch Replication job ever run for the pre-existing objects, primary region destroyed today: what happens to those older objects, and whose assumption was wrong; the class then closes on *method* — how to test a confident claim against AWS's own documentation | Oral answers noted against the student |

> **Do not walk the four variants' planted errors in this session.** Part 2a is a marked deliverable
> and, under SUBMISSION.md, is not due until before the next class session — revealing any variant's
> error now marks the exercise for everyone still holding it. The four-variant walk-through belongs
> at the start of the following add-on, after the deadline has passed. The one thing you *may* say
> at hand-out is the general instruction in §7: every passage contains exactly one false claim, and
> none of them is an AWS statement.

> **Sequencing warning.** Part 2b sits *after* 2a in the worksheet, and its question restates the
> correction to one of the four variants (§8 item 2). Keep the room on 2a until 0:25 and do not
> preview 2b's wording — a student who reads ahead has been handed that variant's answer.

### 4.2 Conventional arm — worksheet Part 1 (Section A in Block 2)

No personalised artefact and no AI-resilience layer here — that absence *is* the manipulated
variable (`course-plan.md`), so do not add the viva or a variant to this arm.

| Time | Task | Student does | Evidence produced |
|---|---|---|---|
| 0:00–0:05 | **Frame the add-on** | As above; confirms this section answers Part 1 only | — |
| 0:05–0:15 | **Part 1 Q1 — accidental overwrite** | Walks through what actually happened to the original object's data in a versioning-enabled bucket, how the teammate recovers it, and whether the outcome would differ had versioning never been enabled | Written answer |
| 0:15–0:25 | **Part 1 Q2 — lifecycle, current vs noncurrent** | States what a "transition to a colder tier after 30 days" rule does to (a) the current version and (b) the noncurrent versions, and whether those are the same action or two different lifecycle actions | Written answer |
| 0:25–0:35 | **Part 1 Q3 — CRR on a bucket with existing data** | Answers whether the destination bucket holds the two years of pre-existing objects the day after CRR is enabled, justifies it, and states what would be needed for a complete copy | Written answer |
| 0:35–0:45 | **Part 1 Q4 — reversing versioning** | States whether a bucket can be returned to its original unversioned state, names the only other state change available, and explains how it differs from a true "undo" | Written answer |

### 4.3 If the session runs to the full 60 minutes

Spend the extra 15 minutes on, in this order: (1) more viva coverage in the AIR-Sec arm — sample at
least one student per variant, which the skew in §9 makes non-automatic, and deliberately sample the
variant identified in §8 item 2 *last*, since its answer is the one already in circulation; (2) a
worked demonstration of the *method* — take one confident-sounding data-protection claim that
appears in **none** of the four passages and check it against the AWS pages in the lab README's
References, so nothing is given away; (3) a Docker Desktop + Git check against SUBMISSION.md's
Lesson 1 setup list, because the next add-on in this block —
`labs/lesson14-config-lambda-remediation`, a HYBRID lesson (specification §6) — does need a running
Docker target and should not lose its first twenty minutes to installation.

**Checks for understanding.** Cold-call mid-session: *"a lifecycle rule transitions objects after 30
days — which versions of the object does that sentence actually cover?"* Before the debrief, a
one-minute paper: *"you enabled replication this morning; which of your objects are now in the other
region?"* — the second surfaces the scope misconception directly and is worth collecting in **both**
arms.

## 5. Assessment for this lesson

| Instrument | Evidence | Outcome | Weight |
|---|---|---|---|
| Worksheet Part 2a — "Audit the Backup Plan" (AIR-Sec arm) | Variant number, the exact error sentence(s), why it is wrong, the corrected sentence | K1–K4, P1–P3, CLO4 | Part of the add-on worksheet mark — this layer's share of the grade is ⬚ |
| Worksheet Part 2b — EiPE (AIR-Sec arm) | 3–4 sentence plain-English explanation | K3–K4, P4, CLO1/CLO4 | Part of the worksheet mark |
| Worksheet Part 2c — viva spot-check (AIR-Sec arm, in class) | Live answer without notes | P5, CLO4/CLO5 | Pass / flag for follow-up |
| Worksheet Part 1 — four essay questions (Conventional arm) | Written answers, graded on the writing itself | K1–K4, P6, CLO1 | Part of the worksheet mark |
| **Per-student attributable artefact** | **No flag this lesson (CONCEPTUAL)** — the lab README states the attributable artefact is *which planted-error variant the student was assigned*; identifying **their own** variant's specific error is what is attributable, and describing someone else's does not satisfy the task | A3, CLO5 | Integrity control that also carries marks (specification §8) |
| AWS Academy Lesson 13 challenge lab | Graded inside the Learner Lab | AWS's own objectives | ⬚ — **not** part of this layer either way. Whether this particular lab sits inside the ~40% AWS-graded baseline is **not established by the repository**: `course-plan.md` attributes it to AWS Academy *Cloud Architect*, while specification §1's baseline is Cloud Foundations + Cloud Security Foundations and §2 pins the ~40% to 6 + 7 items from those two. Confirm with the AWS-side gradebook before telling students it counts |

Marking detail (the point split and the model answers) lives in the instructor-held key,
`instructor/lesson13-s3-versioning-lifecycle-replication-answer-key.md`, which is git-ignored and is
not reproduced here. The exact weight of this repository's layer within the final grade is ⬚
(specification §4 and §8).

**Marking adjustment required this lesson.** Because the correction to one variant is stated
verbatim in material every student can read (§8 item 2), a bare correct answer on that variant is
weaker evidence than the same answer on the other three. Mark it on the *explanation* — what
actually happens instead, and what closes the gap — not on the identification alone, and record the
variant number against the score so the per-variant detection rate stays interpretable (§10).

**Submission** (SUBMISSION.md): worksheet exported to PDF → Google Classroom, named
`Lesson13_<StudentID>.pdf`, with an AI-tool usage disclosure; due before the next class session
unless told otherwise; late −10%/day up to 3 days. There is **no flag to submit** — SUBMISSION.md
asks for a captured flag on LAB/HYBRID lessons only, and this add-on is CONCEPTUAL.

## 6. Materials

- Lab: `labs/lesson13-s3-versioning-lifecycle-replication/` — `README.md`, `worksheet.md`. There is
  no code, no `docker-compose.yml` and no `exploit.py` for this lesson; that is expected for a
  CONCEPTUAL add-on.
- Instructor key: `instructor/lesson13-s3-versioning-lifecycle-replication-answer-key.md`
  (git-ignored, never committed).
- **Slides — none, on purpose.** `slides/` is deliberately empty: the lecture baseline is AWS
  Academy's own licensed curriculum, delivered through the Learner Lab and never mirrored here
  (`slides/README.md`). Any original, non-AWS slide would go in `slides/lesson13.md`.
- **Quizzes — none, on purpose.** The knowledge checks run inside the Learner Lab as part of the
  licensed curriculum (`quizzes/README.md`).
- Public references named by the lab README (publicly available AWS S3 user-guide material — no AWS
  Academy course file was used or copied): *What does Amazon S3 replicate?* (the scope of live
  replication); *Replicating existing objects with S3 Batch Replication* (the separate, one-time
  job); *Retaining multiple versions of objects with S3 Versioning* (the unversioned /
  versioning-enabled / versioning-suspended states); *Lifecycle configuration elements* and the
  lifecycle-actions/versioning-state table.
- [SUBMISSION.md](../../SUBMISSION.md) · [ETHICS.md](../../ETHICS.md) ·
  [course specification](../course-specification.md) · [course-plan.md](../../course-plan.md)

## 7. Where this departs from real AWS behaviour — say it aloud

The repository's standing rule is that any simplification in a local simulation is labelled in the
same breath as the simulation. **This lesson has no simulation to label** — no Flask app, no Docker
target, no stand-in service (`README.md`: CONCEPTUAL, no exploitable target). What still has to be
said aloud is this:

- The four passages in `worksheet.md` Part 2a are **synthetic, AI-style text written for this
  exercise**. They are not real AWS documentation, and — per the licensing constraint that governs
  this whole repository — they are not AWS Academy material either. Each contains exactly one
  deliberate false claim.
- Students must not screenshot a passage and later cite it as an AWS statement. Point them at the
  lab README's References list for the authoritative source, and require the *corrected* sentence to
  be defensible against it.
- **Vocabulary mismatch to warn about before they open the docs.** The worksheet uses the shorthand
  "cross-region replication (CRR)". The AWS pages the README cites frame the same behaviour as *live
  replication* — whose scope is objects created or updated after the replication configuration is
  added — with *S3 Batch Replication* as the separate one-time job for objects that already existed.
  A student checking their correction will meet that vocabulary, not the worksheet's shorthand; mark
  the substance, not the label. Nothing beyond what the README's References describe should be
  asserted in class about replication behaviour.
- The lesson describes AWS's topics in our own words throughout, and never by the AWS Academy lab's
  own scenario name. Nothing here is a substitute for the Learner Lab challenge lab, which remains
  the place the actual console and its guard-rails are learnt.

## 8. Known issues in the source material — do not patch the worksheet mid-term

These are defects in student-facing or shared content that this plan deliberately does **not** edit;
they are reported upward instead. Handle them in delivery.

1. **The worksheet's opening line points the wrong way in this lesson.** `worksheet.md` opens with
   *"Section is assigned Block 1 = AIR-Sec or Block 2 = Conventional per `course-plan.md`'s block
   table"*. Read literally that says Block 2 is always the Conventional arm — and this is a **Block
   2** lesson, so a Section B student self-selecting from that line will do **Part 1 instead of
   their assigned Part 2**, producing evidence that cannot be graded for their arm and contaminating
   the block's comparison. The same line was already reported from Lesson 1–3's plan (§8 there); it
   is a standing worksheet defect, not a new one, but this is the lesson where it does damage. **In
   delivery:** state the section's arm aloud *and* in Classroom before the worksheet is opened, and
   do not let students choose their own Part.
2. **The correction to one of the four Part 2a variants is already published to every student.** The
   passage whose planted claim is that switching on cross-region replication auto-backfills a
   bucket's pre-existing objects is contradicted, in plain words, by material students can see
   before they start: the lab README's Objectives bullet on why enabling CRR does not back-copy
   pre-existing objects and what feature closes the gap; the README's "Why it's exciting" paragraph,
   which names that same claim as its illustrative example; worksheet Part 2b, which asks **all**
   AIR-Sec students the question whose answer is that correction; and the Part 2c viva prompt, which
   names the remedy outright. (Naming the affected claim here adds no disclosure: `course-plan.md`
   already states it in this same public repository.) Two consequences: that variant is materially
   easier than the other three, and under `(last digit of student ID) mod 4` it falls into one of
   the two *larger* buckets, so the leak lands on roughly 30% of the cohort — which distorts the
   per-variant planted-error detection rate the research layer measures. **In delivery:** do not
   edit the worksheet mid-term; apply §5's marking adjustment, keep the room on 2a until 0:25, and
   record the variant number against every score.
3. **The curriculum monorepo's manifest for this lesson says `duration_min: 180`**
   (`../KOSEN69 - curriculum/lessons/s3-versioning-lifecycle-replication/lesson.yml`), which
   contradicts the lab README's *"45–60 min, no Docker"* and specification §1's *"45–60 min each;
   one 60–90 min"*. The same 180 appears on the other cloud lessons, so it reads as an unadjusted
   default carried over from the 3-hour sibling courses. **In delivery:** teach to the README's
   45–60 min; do not schedule a 3-hour room from the manifest.
4. **The specification's schedule row labels this lesson with the AWS Academy scenario name in
   quotes** (`docs/course-specification.md` §6). The lab README's own rule is that no AWS Academy
   scenario or character name is referenced anywhere in this lesson, and `course-plan.md` treats the
   licensing boundary as legal rather than stylistic. **In delivery:** refer to it only as the AWS
   Academy Lesson 13 challenge lab, in class and in Classroom, as this plan does.
5. **Which AWS course this lab belongs to is inconsistent across shared content.** `course-plan.md`'s
   lesson map calls it an official AWS Academy **Cloud Architect** lab, but specification §1 states
   the baseline curriculum as Cloud Foundations + Cloud Security Foundations, and §2 pins the ~40%
   AWS-graded share to 6 Cloud Foundations items + 7 Cloud Security Foundations items. Nothing in
   the repository says whether this lab is one of those 13. **In delivery:** do not assert to
   students that this challenge lab carries AWS-graded weight; check the AWS-side gradebook and
   record the answer in §5 (see also §10).

## 9. Risks and contingencies

| Risk | Mitigation |
|---|---|
| **Arm/section mix-up in Block 2** (§8 item 1) — this lesson reverses the arm assignment relative to every Block 1 add-on already taught, and the worksheet's opening line reinforces the wrong answer for Section B | Announce the arm before the worksheet opens and post it in Classroom in writing, so a late arrival cannot guess wrong. Do not rely on students remembering "we're the AIR-Sec section" from Block 1 — for one of the two sections that is now false |
| **The leaked variant** (§8 item 2) compounds the built-in skew | Apply §5's marking adjustment on that variant; sample it *last* in the viva (§4.3) so the earlier oral answers do not repeat the correction to the room; record variant numbers against scores for §10 |
| **Variant skew is built into the formula.** `(last digit of student ID) mod 4` maps three digits to variants 0 and 1 (0/4/8 and 1/5/9) but only two to variants 2 and 3 (2/6 and 3/7) — roughly a 30/30/20/20 split | When choosing viva subjects, deliberately sample across all four variants rather than relying on volunteers, or the two larger buckets dominate the oral evidence. Hold the four-variant walk-through until the following add-on, after the Part 2a deadline (§4.1) |
| A student computes the wrong variant, or answers a passage that is not theirs — the lab README states describing someone else's variant's error does not satisfy the task | Have every student write their variant number **and** their ID's last digit at the top of the sheet in the 0:05–0:10 slot, and check them then, not at marking time. A visible mismatch is a viva follow-up, not an automatic accusation — arithmetic slips look identical to copying at first glance |
| A student pastes their passage into an AI assistant, which confidently confirms the planted claim — the failure mode this lesson is *about* — or invents a different "error" | Repo policy permits AI use **with disclosure** (SUBMISSION.md), so this is not automatically misconduct; what is graded is the student's own reasoning. Require the corrected sentence to be justified against the AWS pages in the lab README's References, and use the Part 2c viva as the tiebreak. ⬚ — the worksheet does not state whether Part 2a is closed-book on AI; fix that instruction in Classroom before hand-out if you want it closed-book |
| The four deliberately-false passages sit in a **public** repository and can be screenshotted and later quoted as AWS guidance about backups | Say at hand-out that every passage contains exactly one false claim and none is an AWS statement; make the corrected sentence, not the passage, the thing students keep (§7) |
| A student proposes to settle a claim by demonstrating it in their Learner Lab — enabling versioning, creating a second-region bucket, running a replication job | The add-on needs no console at all and the whole envelope is 45–60 min. Route them to the README's References for today; a console demonstration is Learner Lab time, not add-on time, and versioning in particular cannot be undone once enabled (the subject of Part 1 Q4) |
| A student arrives without having completed the AWS Lesson 13 challenge lab, or cannot start their Learner Lab | This add-on needs no console and no Docker, so they can still do it — run the session, and route the Learner Lab problem to the AWS-side channel and Lesson 1's one-time setup list in SUBMISSION.md. Do not spend add-on minutes debugging AWS sandbox access for one student |
| Students check their correction against AWS's docs and meet different vocabulary — *live replication*, *S3 Batch Replication* — than the worksheet's "CRR" shorthand, and conclude they have the wrong page | Warn them at hand-out (§7) and mark on substance rather than label. Do not extend the discussion to replication behaviour the README's References do not cover |
| The temptation to "even things up" by giving the Conventional arm the viva or a variant | Do not. The absence of the personalised artefact and the AI-resilience layer *is* the manipulated variable for this block (`course-plan.md`); adding them contaminates the comparison for the whole block |
| A 3-hour room or 3-hour expectation is scheduled from the monorepo manifest's `duration_min: 180` (§8 item 3) | Schedule to the README's 45–60 min; if the slot is already long, use §4.3's list in order rather than stretching the worksheet |
| The session runs short — there is nothing to install and nothing to exploit | Use §4.3's list in order: extra viva coverage first (leaked variant last), then the worked method demonstration on a claim from none of the four passages, then the Docker Desktop + Git check that `labs/lesson14-config-lambda-remediation` will need |

## 10. Post-teaching reflection

*Complete after the session — this also feeds the course's engagement data.*

- Attendance / completion: ⬚
- Which arm this section actually ran, and whether anyone did the wrong Part (the Block 2 reversal is
  the specific risk this time): ⬚
- Time actually taken per task (vs. the 45-minute floor above): ⬚
- Variant distribution as it fell out in the room, vs. the expected 30/30/20/20: ⬚
- Detection rate **per variant** — which planted error went uncaught most often, and whether the
  variant identified in §8 item 2 scored conspicuously higher than the rest (evidence for the
  leak) or the same (evidence students did not read the README): ⬚
- Whether any variant's passage was caught for the wrong reason — implausible phrasing rather than
  the factual claim: ⬚
- Misconception that showed up in the EiPE answers — especially the difference between "replication
  is on" and "the old objects are there": ⬚
- Whether any student justified a correction from an AI answer rather than AWS documentation: ⬚
- Settled from the AWS-side gradebook: does this challenge lab carry AWS-graded weight (§5, §8 item
  5)? Record it here so the next run of this plan can drop the ⬚: ⬚
- Anything to change before this add-on runs again: ⬚
