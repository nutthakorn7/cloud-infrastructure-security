# Lesson Plan — Lesson 11 add-on: S3 Server-Side Encryption with KMS (Envelope Encryption)

| | |
|---|---|
| **Course** | Cloud Infrastructure & Security · subject code **02005097** (`README.md`, `course-plan.md`; `docs/course-specification.md` still records the course code as ⬚) |
| **AWS lesson this attaches to** | **Lesson 11** — S3 server-side encryption with KMS. The lab README names the source topic as Shinya's own notes for the AWS Academy Cloud Security Foundations **Lab 5.1** material (SSE-KMS setup, the CloudTrail `GenerateDataKey` event, and the "instance won't start after the KMS key is disabled" scenario), **described in our own words — no AWS Academy file is copied, quoted or paraphrased into this plan or into the lab** |
| **Add-on kind** | **CONCEPTUAL** — no exploitable target, no Docker, no flag (`docs/course-specification.md` §6; lab README: *"CONCEPTUAL (no exploitable target — this is an architecture/analysis lesson…)"*) |
| **Block** | **2** (`docs/course-specification.md` §6, `course-plan.md`). Block 2 = **Conventional for Section A**, **AIR-Sec for Section B** — the reverse of Block 1. See the callout below |
| **Duration of this add-on** | **45–60 min, no Docker** — the figure the lab's own README states. This is *not* a full contact session: the AWS Academy Learner Lab is the baseline and comes first |
| **Lab folder** | `labs/lesson11-kms-envelope-encryption` — `README.md`, `worksheet.md` only. No code, no `docker-compose.yml`, no `exploit.py`; that is expected for a CONCEPTUAL add-on |
| **Signature exercise** | **"Audit the Envelope"** (lab README) |
| **Standards** | **CWE-320** (Key Management Errors) — named by the lab README and by the curriculum manifest as a *category* describing correct KMS use, not a coding bug in any artefact |
| **CLOs addressed** | **CLO1** shared responsibility · **CLO4** evaluate & communicate (`docs/course-specification.md` §6). Via §4's alignment table the *Audit-the-AI* / *EiPE* tasks carry CLO1 and CLO4, and the per-student **variant** carries **CLO5**. CLO2/CLO3 are **not** claimed here — there is nothing to exploit or remediate in this lesson |
| **Slides / quizzes** | ⬚ — none, deliberately. `slides/` and `quizzes/` are intentionally empty in this course (`slides/README.md`, `quizzes/README.md`) |
| **Session date / section / room** | ⬚ |

> **Which arm is this section in today? Check before the worksheet is opened.**
> This lesson sits in **Block 2**. Under the block table (`docs/course-specification.md` §6,
> `course-plan.md`): **Section A = Block 1 AIR-Sec / Block 2 Conventional**, **Section B = the
> reverse**. So in *this* lesson **Section A does Part 1 (Conventional)** and **Section B does
> Part 2 (AIR-Sec)** — the opposite assignment to the Lessons 1–3 add-on. The worksheet's own
> opening line will mislead a Section B student here; see §8 item 1 and §9 risk 1.

> **Naming note.** The lab folder, README and worksheet call this **Lesson 11** — the *AWS lesson
> number* it attaches to. The curriculum monorepo (`courses/cloud-infrastructure-security.yml`)
> lists the same lesson at **slot 8** of the monorepo's **11 schedule entries** (10 add-on lessons
> plus a final non-add-on "review" slot, Reflection & Wrap-up) — the offset between "Lesson 11" and
> "slot 8" exists because only ten of the AWS lessons carry an add-on. Both labels refer to the same
> material; use "Lesson 11" with students, since that is what the worksheet header and the
> `Lesson<NN>_<StudentID>.pdf` submission convention use.

---

## 1. Session objectives

By the end of this add-on a student can:

**Knowledge (K)**

- K1 — Explain **envelope encryption**: why S3 asks KMS for a *data key* instead of asking KMS to
  encrypt the object directly, and what KMS actually returns — a plaintext copy **and** an
  encrypted copy of that same data key (lab README, Objectives).
- K2 — State precisely what S3 **keeps** and what it **discards** after encrypting an object with
  SSE-KMS: the encrypted data key goes into the object's metadata; the plaintext copy does not
  persist.
- K3 — Distinguish the **blast radius** of *disabling* a KMS key from *deleting* it. Disabling makes
  every object ever encrypted under that key unreadable **while it stays disabled**, and is
  *reversible* — re-enabling restores access. Deleting it, after the mandatory **7–30-day waiting
  period**, is irreversible and makes those objects **permanently** unreadable, because the
  encrypted data key stored in each object's metadata can then never be decrypted (lab README,
  Objectives).
- K4 — Explain why envelope encryption uses a separate data key per object/operation rather than
  encrypting every object directly with the customer master key (CMK) itself (worksheet Part 1 Q4).

**Skills (P)**

*AIR-Sec arm — worksheet Part 2 (Section B in Block 2):*

- P1 — Compute their own variant with `variant = (last digit of your student ID) mod 4` and read
  **only** that passage.
- P2 — Identify the single planted factual error in their own assigned passage and quote the exact
  sentence containing it.
- P3 — State why it is wrong — what actually happens instead — and write the corrected sentence.
- P4 — (2b, EiPE) Write 3–4 sentences a non-technical stakeholder could follow on why disabling a
  KMS key makes old data unreadable *until the key is re-enabled* even though the encrypted objects
  are still sitting in the bucket; contrast that with disabling one database user account; and say
  how *deleting* the key differs from disabling it.
- P5 — (2c, viva) Answer the worksheet's viva prompt without notes: what keeping the plaintext data
  key after encryption would defeat.

*Conventional arm — worksheet Part 1 (Section A in Block 2):*

- P6 — Answer the four essay questions in their own words: the step-by-step path from "click Upload
  on an object in an SSE-KMS bucket" to "the object is stored encrypted"; what S3 stores in the
  object's metadata and what it deliberately discards; what happens to objects already stored when
  the KMS key is disabled or scheduled for deletion, and why; and why a separate data key is used
  per object/operation instead of the CMK directly.

**Attitude (A)**

- A1 — Work only within the two approved targets in [ETHICS.md](../../ETHICS.md) — the local Docker
  labs in `labs/` and the student's own assigned AWS Academy Learner Lab sandbox — and treat Learner
  Lab credentials as secrets. This add-on needs neither, which is exactly why the rule is worth
  restating before students switch back to the console.
- A2 — Treat a fluent, confident AI explanation of an AWS mechanism as something to verify against
  AWS's own public documentation, not to trust.
- A3 — Answer **their own** variant: the lab README states that describing someone else's variant's
  error does not satisfy the task.

## 2. Key idea (the through-line)

The object is encrypted by a key that is itself encrypted. That one sentence carries the whole
lesson. When an object is written to an SSE-KMS bucket, the bulk encryption happens with a fresh
symmetric data key, and what travels with the ciphertext is not that key but a *locked copy* of it —
locked under a key that never leaves KMS. The ciphertext and its own wrapped key sit together in the
bucket, and neither is any use without a service call to the one place that can unwrap it.

Two consequences follow, and both are what the worksheet actually assesses. First, **what is kept
and what is thrown away is the entire security property.** If the plaintext data key were retained
next to the object "for speed", anyone who could read the object's metadata could decrypt it with no
call to KMS, no permission check and no audit record — which is the viva prompt in 2c. Second,
**revocability is the feature, and it cuts both ways.** Because every read needs KMS to unwrap the
stored data key, control over that key is control over the data — so disabling the key locks
*existing* data, not just new writes. That is the property an organisation buys, and it is the same
property that turns a key deletion into permanent data loss. The pedagogically important line is the
one students most often collapse: **disable is a pause, delete is a shred.** The AWS Academy Lab 5.1
topic the README names — a workload that stops working once its KMS key is disabled — is the same
idea observed from the operations side.

The teaching move is deliberately awkward. The four passages in the worksheet *sound* right: fluent,
confident, structurally correct, correct in vocabulary, and each carrying exactly one false claim
that is a one-word or one-clause swap. Vocabulary alone will not catch it; only a student who has
internalised the *data flow* will. That is the point of the exercise, and it is the CLO4 skill.

## 3. What students must have completed before this add-on

The AWS Academy lab is the baseline and comes **first**; this add-on assesses the same concept
afterwards and does not re-teach it ([SUBMISSION.md](../../SUBMISSION.md) — AWS first, add-on
second).

**In the AWS Academy Learner Lab (graded by AWS):**

- The real **AWS Academy Lab 5.1** work in their own Learner Lab sandbox, which the lab README lists
  as: SSE-KMS setup, uploading and viewing an encrypted object, and the CloudTrail `GenerateDataKey`
  event (lab README, step 1). That is where the actual console, the key policy UI and the CloudTrail
  event view are learned. Nothing in this add-on re-teaches or replaces it.

**From Lesson 1's one-time setup** ([SUBMISSION.md](../../SUBMISSION.md)):

- Joined Google Classroom, accepted the AWS Academy Learner Lab invite, and signed the ETHICS.md
  acknowledgment (ETHICS.md states this is signed in Lesson 1).

**On their own machine:**

- **Nothing.** This add-on has no Docker target, no code, no host Python and no console requirement —
  the README says *"no Docker"* explicitly.

**Instructor, before the session:**

- Confirm, and be ready to state aloud, which arm this section is in for **Block 2** — Section A
  Conventional, Section B AIR-Sec. §8 item 1 explains why this cannot be left to the worksheet's own
  opening line.
- Post the worksheet in Classroom with the assigned Part named **in writing**.
- Re-read the instructor-held key `instructor/lesson11-kms-envelope-encryption-answer-key.md`
  (git-ignored, never committed, not reproduced here) against the current worksheet.
- Have the lab README's References list open: AWS KMS documentation on how envelope encryption
  works, AWS's page on S3 encryption with AWS KMS (SSE-KMS), and AWS's page on deleting KMS keys —
  all publicly available AWS material, no AWS Academy file. These are the authoritative sources a
  student's *corrected sentence* has to survive.
- Nothing to pull, build, start or seed. See §9 risk 8 on flags.

## 4. The add-on session — minute by minute

> **Where these minutes come from.** The task *names and content* below are the worksheet's and the
> README's own. The **minute split is this plan's allocation** inside the 45–60 min envelope the lab
> README states — neither the README nor the worksheet carries a per-task budget, so do not treat
> these numbers as fixed course material. Both tables are built to the **45-minute floor** so they
> still fit on a short day; §4.3 says what the extra 15 minutes buys.
>
> The two arms are **alternatives, not a sequence.** A student does 4.1 *or* 4.2, never both — the
> worksheet's own instruction is *"complete only the part assigned to you this block"*.

### 4.1 AIR-Sec arm — worksheet Part 2 (Section B in Block 2)

| Time | Task | Student does | Evidence produced |
|---|---|---|---|
| 0:00–0:05 | **Frame the add-on** | Hears which arm this section is in; that Lab 5.1 is the prerequisite and today assesses that concept rather than adding AWS content; notes that no Docker, no console and no credentials are needed | — |
| 0:05–0:10 | **Compute the variant** | `variant = (last digit of your student ID) mod 4`; writes the variant number **and** the ID's last digit at the top of the sheet; reads **only** that passage | Variant number recorded before reading |
| 0:10–0:27 | **Part 2a — "Audit the Envelope" (personalised)** | Finds the single planted error in their own passage; records the exact sentence, why it is wrong (what actually happens instead), and the corrected sentence | Variant no. + quoted error sentence + explanation + corrected sentence |
| 0:27–0:37 | **Part 2b — EiPE** | Writes 3–4 sentences for a non-technical stakeholder: why disabling the KMS key makes objects still sitting in the bucket unreadable, why disabling one database user account does not do the same thing to a database, and how *deleting* the key differs from disabling it | Short written answer covering all three halves of the question |
| 0:37–0:45 | **Part 2c — viva spot-check + close** | 3–4 rotating students answer the viva prompt without notes — what keeping the plaintext data key around after encrypting would defeat; the class then closes on *method*: how to test a confident claim against AWS's own documentation | Oral answers noted against the student |

> **Do not walk the four variants' planted errors in this session.** Part 2a is a marked deliverable
> and, under SUBMISSION.md, is not due until before the next class session — revealing any variant's
> error now marks the exercise for everyone still holding it. Hold the four-variant walk-through
> until the start of the following add-on, after the deadline has passed.

### 4.2 Conventional arm — worksheet Part 1 (Section A in Block 2)

No personalised artefact and no AI-resilience layer here — that absence **is** the manipulated
variable (`course-plan.md`), so do not add the viva or a variant to this arm.

| Time | Task | Student does | Evidence produced |
|---|---|---|---|
| 0:00–0:05 | **Frame the add-on** | As above; confirms this section answers **Part 1 only** | — |
| 0:05–0:17 | **Part 1 Q1** | Walks through, step by step, what happens between clicking Upload on an object in an SSE-KMS bucket and the object being stored encrypted: what S3 asks KMS for, and what KMS sends back | Written answer / sequence diagram |
| 0:17–0:25 | **Part 1 Q2** | States specifically what S3 stores in the object's metadata after encryption, and what it deliberately discards | Written answer |
| 0:25–0:35 | **Part 1 Q3** | What happens to objects already stored when the organisation disables — or schedules deletion of — the KMS key used to encrypt that bucket's objects, and why | Written answer |
| 0:35–0:45 | **Part 1 Q4** | Why envelope encryption uses a separate data key per object/operation instead of asking KMS to encrypt every object directly with the CMK | Written answer |

⬚ **Not fixed anywhere in this repository:** whether the Conventional section runs this in class at
all or takes Part 1 home. This is a study-design decision, not a per-lesson one — decide it once,
apply it to every Conventional-block lesson, and record it here. (The same ⬚ is open in the Lesson 5
plan for the Docker labs.)

### 4.3 If the session runs to the full 60 minutes

Spend the extra 15 minutes on, in this order:

1. **More viva coverage in the AIR-Sec arm** — deliberately sample at least one student per variant.
   The skew in §9 risk 2 makes this non-automatic.
2. **A worked demonstration of the *method***: take one confident-sounding claim about SSE-KMS that
   appears in **none** of the four passages, and check it live against the AWS pages in the lab
   README's References. Nothing is given away, and the transferable skill is the point.
3. **Close the loop to the Learner Lab scenario the README names** — the workload that stops working
   once its KMS key is disabled. Neither Part asks about it in writing, so if you want it covered it
   has to be covered verbally (see §8 item 3).

**Checks for understanding.**

- Mid-session cold-call: *"the encrypted object and its wrapped key are both sitting in the bucket.
  What is missing, and where does it live?"*
- One-minute paper, worth collecting in **both** arms: *"the key was disabled on Monday and
  re-enabled on Friday. What state are Tuesday's objects in on Saturday?"* — this surfaces the
  disable-vs-delete collapse directly (§9 risk 6).
- Follow-up for a fast group: *"the key is scheduled for deletion but the waiting period has not
  expired yet. Can the objects be read today?"* Check your answer against AWS's own "Deleting AWS
  KMS keys" page — the README lists it as a reference precisely because AWS publishes the
  irreversibility warnings itself.

## 5. Where this departs from real AWS — say it aloud

The repository's standing rule is that any simplification is named in the same breath as the
exercise (`docs/course-specification.md` §7). **This lesson has no simulation to label** — no Flask
app, no Docker target, no stand-in service. What still has to be said aloud is this:

1. **The four passages in `worksheet.md` Part 2a are synthetic, AI-style text written for this
   exercise.** They are not real AWS documentation, and — per the licensing constraint governing this
   whole repository — they are not AWS Academy material either. Each contains exactly one deliberate
   false claim.
2. **Nothing here is a substitute for Lab 5.1.** No `GenerateDataKey` call is made, no CloudTrail
   event is viewed, no key is created, disabled or scheduled for deletion in this add-on. Students
   who skipped the Learner Lab work will be able to complete the worksheet and will still not have
   seen the console — say so, rather than letting the worksheet stand in for the lab.
3. **Students must not screenshot a passage and later cite it as an AWS statement.** Point them at
   the README's References list, and require the *corrected* sentence — not the passage — to be the
   thing they keep.
4. **The passages compress real service behaviour, and a well-read student may push on the
   compression.** The worksheet's passages are written at concept level; AWS's own S3 and KMS pages
   document options and edge cases none of the four passages mention. Do not improvise an answer
   from memory when that happens — pose the question back, open the pages in the README's References
   with the class, and let the documentation settle it. That exchange *is* the CLO4 skill being
   modelled, and it costs two minutes.
5. **Numbers age.** The README states the mandatory waiting period before a scheduled KMS key
   deletion takes effect as **7–30 days**. Teach students to check the current AWS page rather than
   memorise a number from a worksheet; that habit is the CLO4 skill this lesson exists to build.

## 6. Assessment for this lesson

| Instrument | Evidence | Outcome | Weight |
|---|---|---|---|
| Worksheet Part 2a — *"Audit the Envelope"* (AIR-Sec arm) | Variant number, the exact sentence containing the error, why it is wrong, the corrected sentence | K1–K3, P1–P3 · CLO4 | Part of the add-on worksheet mark — this layer's share of the final grade is ⬚ |
| Worksheet Part 2b — *EiPE* (AIR-Sec arm) | 3–4 sentences a non-technical stakeholder could follow, covering unreadability, the database-account contrast, and disable vs. delete | K2–K3, P4 · CLO1/CLO4 | Part of the worksheet mark |
| Worksheet Part 2c — viva spot-check (AIR-Sec arm, in class) | Live answer without notes | K2, P5 · CLO4/CLO5 | Pass / flag for follow-up |
| Worksheet Part 1 — four essay questions (Conventional arm) | Written answers, graded on the writing itself | K1–K4, P6 · CLO1 | Part of the worksheet mark |
| **Per-student attributable artefact** | **No flag this lesson (CONCEPTUAL).** The attributable artefact is *which planted-error variant the student was assigned* — correctly identifying **their own** variant's specific error is what is attributable; describing someone else's variant's error does not satisfy the task (lab README) | A3 · CLO5 | Integrity control that also carries marks (`docs/course-specification.md` §8) |
| AWS Academy Lab 5.1 + its Knowledge Check | Graded inside the Learner Lab | AWS's own objectives | part of the ~40% AWS-graded aggregate across all ~13 Learner Lab / Knowledge-Check items course-wide (`docs/course-specification.md` §2: 6 Cloud Foundations + 7 Cloud Security Foundations items) — this one lab's individual share is not broken out anywhere in this repository; **not** part of this layer, and identical for every section |

**Why there is no flag here, and why that is correct.** `docs/course-specification.md` §7 states that
CONCEPTUAL lessons issue per-student planted-error variants *instead of* flags, and the curriculum
manifest for this lesson carries `flag_keys: []`
(`../KOSEN69 - curriculum/lessons/kms-envelope-encryption/lesson.yml`). There is nothing for
`instructor/seed_flags.py` to mint. A submission with no `FLAG{…}` in it is complete for this lesson.

**Marking detail** — the point split and model answers — lives in
`instructor/lesson11-kms-envelope-encryption-answer-key.md`, which is git-ignored and is deliberately
**not** reproduced here: this repository is public.

**Submission** ([SUBMISSION.md](../../SUBMISSION.md)): worksheet exported to PDF → Google Classroom,
named `Lesson11_<StudentID>.pdf`, with Name + Student ID on the file and an AI-tool usage disclosure
("None" is a valid disclosure); due before the next class session unless told otherwise; late
−10%/day up to 3 days. The worksheet's own Submit line asks the AIR-Sec arm for variant + error +
correction + Parts 2b/2c, and the Conventional arm for Part 1 only.

**Grading scale, and this layer's share of the final grade: ⬚** — an institutional decision recorded
nowhere in this repository (`docs/course-specification.md` §4, §8).

## 7. Materials

- **Lab:** `labs/lesson11-kms-envelope-encryption/` — `README.md`, `worksheet.md`. No code, no
  `docker-compose.yml`, no `exploit.py`; expected for a CONCEPTUAL add-on.
- **Instructor-held (git-ignored, never committed):**
  `instructor/lesson11-kms-envelope-encryption-answer-key.md`. The H3 pre/post instrument
  (`instructor/research/pre-post-test.md`) and the H2 planted-error bank
  (`instructor/research/planted-error-bank.md`) both carry items drawn from this lesson's content.
  Neither is reproduced or summarised here — see §9 risk 10.
- **Slides — none, on purpose.** `slides/` is deliberately empty: the lecture baseline is AWS
  Academy's own licensed modules, delivered through the Learner Lab and never mirrored here
  (`slides/README.md`). Any original, non-AWS slide would go in `slides/lesson11.md`.
- **Quizzes — none, on purpose.** Knowledge checks run inside the Learner Lab as part of the licensed
  curriculum (`quizzes/README.md`).
- **Public references named by the lab README** (publicly available AWS material — no AWS Academy
  file used or copied): AWS KMS documentation on *how envelope encryption works* and on *Amazon S3
  encryption with AWS KMS (SSE-KMS)*; AWS's documentation on *deleting AWS KMS keys*, which carries
  AWS's own blast-radius and irreversibility warnings.
- **Baseline curriculum:** the AWS Academy Learner Lab itself — accessed through AWS, never mirrored
  here.
- **Course documents:** [course-specification.md](../course-specification.md) ·
  [course-plan.md](../../course-plan.md) · [SUBMISSION.md](../../SUBMISSION.md) ·
  [ETHICS.md](../../ETHICS.md)

## 8. Known issues in the source material — do not patch the worksheet mid-term

These are defects in student-facing or shared content that this plan deliberately does **not** edit.
Lab content and its curriculum-monorepo copy are parity-gated, and editing graded material so a
lesson plan reads tidily is exactly the failure mode that gate exists to catch. Handle them in
delivery; fix them between cohorts.

1. **The worksheet's opening line conflates block with arm, and this lesson is where it bites.**
   `worksheet.md` opens with *"Section is assigned Block 1 = AIR-Sec or Block 2 = Conventional per
   `course-plan.md`'s block table"*. Read literally, that says Block 2 is always the Conventional
   arm — which is true for Section A and **false for Section B**, whose Block 2 is AIR-Sec. This
   lesson is Block 2 for both sections, so a Section B student who self-selects from that line will
   write four essays instead of auditing their variant, and produce evidence that cannot be graded
   for their arm. **In delivery:** state the section's arm aloud *and* in the Classroom post before
   the worksheet is opened; do not let students choose their own Part. (The same line is flagged in
   the Lessons 1–3 plan §8; there it was a latent risk, here it points the wrong way for a whole
   section.)
2. **The README undercounts the Conventional questions.** The lab README's Deliverable says *"plus
   the two Part 1 essay-style questions if you're in the Conventional block instead"* — the worksheet
   Part 1 has **four** numbered questions, and the instructor key marks four. A Section A student who
   reads only the README will answer half the paper. **In delivery:** hand out the worksheet, not the
   README, as the authoritative task list, and say "four questions" out loud.
3. **The README's Deliverable omits Parts 2b and 2c**, which the worksheet's own Submit line requires
   ("Your variant + error + correction + Part 2b/2c"). Same mitigation: the worksheet is the
   authoritative list. Related: the Learner Lab scenario the README names as part of the source topic
   — a workload that stops once its KMS key is disabled — is not asked about in writing in either
   Part, so do not claim it as assessed; cover it verbally (§4.3 item 3).
4. **The 2c viva prompt is malformed.** The worksheet asks: *"If S3 kept the plaintext data key
   around after encrypting, what would that defeat the entire point of envelope encryption?"* — the
   sentence has an interrogative missing. Students will parse it, but read it aloud in its intended
   form ("*why* would that defeat…") so nobody loses time deciding what is being asked, and do not
   penalise an answer that responds to either reading.
5. **The curriculum monorepo's manifest for this lesson says `duration_min: 180`**
   (`../KOSEN69 - curriculum/lessons/kms-envelope-encryption/lesson.yml`), contradicting the lab
   README's *"45–60 min, no Docker"* and `docs/course-specification.md` §1's *"45–60 min each; one
   60–90 min"*. The same 180 appears across the cloud lessons, so it reads as an unadjusted default
   inherited from the 3-hour sibling courses. **In delivery:** teach to the README's 45–60 min; do
   not book a three-hour room from the manifest.

## 9. Risks and contingencies

| Risk | Mitigation |
|---|---|
| **1. Arm inversion in Block 2 (see §8 item 1).** Section B is AIR-Sec here, but the worksheet's first line reads as "Block 2 = Conventional". A whole section can do the wrong Part, which is unmarkable for their arm *and* contaminates the study data | Announce the arm before the worksheet opens and post it in writing in Classroom so a late arrival cannot guess wrong. Spot-check in the first five minutes that Section B students have written a variant number at the top of the sheet — that is the visible tell that they are on the right Part |
| **2. Variant skew is built into the formula.** `(last digit of student ID) mod 4` maps three digits to variants 0 and 1 (0/4/8 and 1/5/9) but only two to variants 2 and 3 (2/6 and 3/7) — roughly a 30/30/20/20 split, so fewer students will actually have worked variants 2 and 3 | Choose viva subjects by deliberately sampling across all four variants rather than taking volunteers, or variants 0 and 1 dominate the oral evidence — and the two under-represented variants are not interchangeable with the other two, so a skewed viva sample leaves part of the concept unexamined |
| **3. A student computes the wrong variant, or answers a passage that is not theirs** — the README states that describing someone else's variant's error does not satisfy the task | Have every student write the variant number **and** their ID's last digit at the top of the sheet in the 0:05–0:10 slot, and check them then, not at marking time. A visible mismatch is a viva follow-up, not an accusation — an arithmetic slip and a copied answer look identical at first glance |
| **4. AI assistants are unusually fluent on this exact topic.** "Envelope encryption" is heavily represented in general-purpose model training data, so pasting a passage in may produce a confident confirmation of the planted claim, or the invention of a different "error" | Repo policy permits AI use **with disclosure** (SUBMISSION.md), so this is not automatically misconduct — what is graded is the student's own reasoning. Require the corrected sentence to be defensible against the AWS pages in the README's References, and use the 2c viva as the tiebreak. ⬚ — the worksheet does not state whether Part 2a is closed-book on AI; fix that instruction in Classroom before hand-out if you want it closed-book |
| **5. The deliberately-false passages sit in a public repository** and can be screenshotted and later quoted as AWS guidance about how SSE-KMS works | Say at hand-out that every passage contains exactly one false claim and none of them is an AWS statement; make the *corrected* sentence, not the passage, the artefact students keep (§5 item 3) |
| **6. Disable-vs-delete collapse — the predictable wrong answer.** One of the four passages concerns the effect of disabling a key, and a student who over-corrects from it lands on "disabling destroys your data forever", which is equally wrong. Part 1 Q3 and Part 2b both hinge on this distinction | Use the one-minute paper in §4 (*disabled Monday, re-enabled Friday — what state are Tuesday's objects in on Saturday?*) in both arms; it forces the reversibility answer out into the open before marking. Part 2b already asks for the disable-vs-delete difference explicitly — grade it as a required half, not a bonus |
| **7. A student arrives without having done Lab 5.1, or cannot start their Learner Lab** | This add-on needs no console, no credentials and no Docker, so they can still complete it. Run the session; route the sandbox problem to the AWS-side channel and Lesson 1's one-time setup list in SUBMISSION.md. Do not spend add-on minutes debugging one student's Learner Lab access |
| **8. Someone looks for the flag that does not exist.** Every LAB/HYBRID lesson in this course mints one; the three CONCEPTUAL lessons (Lessons 1–3, this lesson, and Lesson 13) do not | State at the start that this lesson has no flag and nothing to seed — this lesson's manifest carries `flag_keys: []` and `instructor/seed_flags.py` has no key for it. A submission with no `FLAG{…}` is complete. Do not "add" one for parity: the variant *is* the attributable artefact |
| **9. Pattern-matching across two consecutive Audit-the-AI lessons.** Block 2 runs this lesson and then Lesson 13, both CONCEPTUAL Audit-the-AI with the same four-variant format; students start hunting for the *shape* of a planted error ("the boldest sentence") instead of reasoning about the mechanism | Grade the *explanation* and the corrected sentence, not the underline. The 2c viva is the check that separates a student who found the swapped clause from one who understands the data flow — it is worth running even if the room is short on time |
| **10. Contaminating the research instruments.** Both the H3 pre/post test and the H2 planted-error bank carry items drawn from this lesson's content (`instructor/research/`, git-ignored) | Teach the concept, not the item wording, and never project or hand out either instrument. In particular, do not drill the four variants' sentences verbatim as a revision exercise; the four-variant walk-through belongs in the following session (§4.1 callout) and should be run on the *mechanism*, not on the phrasing |
| **11. Ethics drift back into the Learner Lab.** A student with the AWS console open in the next tab is one step from disabling or scheduling deletion of a KMS key "to see what happens" — and in a sandbox with real objects, the deletion path is the one this lesson has just described as irreversible | Restate ETHICS.md rules 1–2 before students switch back to AWS: their own sandbox is an approved target, but a scheduled key deletion is not a reversible experiment, and probing anything outside the two approved targets can suspend the whole class's accounts |
| **12. The temptation to "even things up"** by giving the Conventional arm the viva or a variant so nobody misses out | Do not. The absence of the personalised artefact and the AI-resilience layer *is* the manipulated variable for this block (`course-plan.md`); adding them contaminates the comparison for the entire block, not just this lesson |
| **13. The session runs short — there is nothing to install, stand up or exploit** | Use §4.3's list in order: viva coverage across all four variants, then the worked method demonstration on a claim that appears in none of the passages, then the verbal close-back to the Learner Lab key-disable scenario |

## 10. Post-teaching reflection

*Complete after the session — this also feeds the course's engagement data.*

- Attendance / completion: ⬚
- Which arm this section actually ran, and whether anyone did the wrong Part (§8 item 1): ⬚
- Time actually taken per task, against the 45-minute floor in §4: ⬚
- Variant distribution as it fell out in the room, vs. the expected 30/30/20/20: ⬚
- Detection rate per variant — which planted error went uncaught most often: ⬚
- Did the disable-vs-delete distinction hold up in the EiPE answers, or did students collapse the
  two (§9 risk 6): ⬚
- Whether any student justified a correction from an AI answer rather than from AWS documentation: ⬚
- Did anyone leave believing the worksheet had replaced Lab 5.1 (§5 item 2): ⬚
- Did the 45–60 min envelope hold, or did the AWS Learner Lab work overrun into it: ⬚
- Anything to change before this add-on runs again: ⬚
