# How to Do & Submit Work

**Platforms:** **AWS Academy Learner Lab** (the AWS modules + Knowledge Checks — provided through
Classroom) + **Google Classroom** (our worksheets, flags, grades). All offensive work is on the two
approved sandboxes only — see [ETHICS.md](ETHICS.md).

> **How this course is graded (read once):** ~40% of your grade is AWS Academy's own auto-graded
> Learner Lab activities + Knowledge Checks — identical for everyone, run on AWS's machinery. The
> layer *we* author and grade on top is the **local Docker labs + worksheets + Audit-the-AI** in this
> repo. Both matter; this page covers how to submit **our** layer.

---

## One-time setup (Lesson 1)
1. Join the **Google Classroom** (code given in class) and accept the **AWS Academy Learner Lab**
   invite posted there.
2. Install **Docker Desktop** + Git, then get this course's repo — the local add-on
   labs all begin with `cd labs/lessonNN-…`, so you need it on your own machine:
   ```bash
   git clone https://github.com/nutthakorn7/cloud-infrastructure-security.git
   cd cloud-infrastructure-security
   ```
   Each add-on lab is then `docker compose up`.
3. Confirm you can start your Learner Lab and reach the AWS console.

---

## Per-lesson — how to do & submit

**Do it (in order):**
1. **AWS first:** complete that lesson's real **AWS Academy module + Knowledge Check** in your
   Learner Lab (this is where you learn the actual AWS console/service). AWS grades this part.
2. **Then the local add-on lab:** stand up the week's target (`cd labs/lesson<NN>-…` → `docker compose
   up`, per that lab's README) and work the **worksheet** (`labs/lesson<NN>…/worksheet.md`): for each
   task record the **payload/command**, a **screenshot** of the result, and a short **mitigation**.
   Conceptual lessons (no Docker target) center the **Audit-the-AI** exercise instead of an exploit.
3. Capture your lab's **flag** where the lab mints one (LAB/HYBRID lessons).

**Submit → Google Classroom:**
| Part | What |
|------|------|
| Worksheet | the completed worksheet exported to **PDF** (screenshots embedded) |
| Flag | the captured `FLAG{…}` for that lesson (LAB/HYBRID lessons) |

**File name:** `LocalNN_StudentID.pdf` (e.g. `Local04_65123456.pdf`). `NN` is the number of the
**Local** assignment in Classroom, which is not the lesson folder number (see the table below).
**Deadline:** before the start of the next week's class. The exact date and time is the due date
on the Classroom assignment.
**Grading:** the rubric in each worksheet; the AWS Knowledge Checks are graded by AWS.

**Which Local is which lab:**
| Classroom assignment | Lab folder |
|---|---|
| Local 01 | `labs/lesson01-03-aws-fundamentals-intro` |
| Local 02 | `labs/lesson04-ec2-lambda-beanstalk` |
| Local 03 | `labs/lesson05-s3-static-site-lambda-sns` |
| Local 04 | `labs/lesson13-s3-versioning-lifecycle-replication` |
| Local 05 | `labs/lesson06-load-balancing-autoscaling` |
| Local 06 | `labs/lesson07-iam-policy-evaluation` |
| Local 07 | `labs/lesson10-vpc-networking` |
| Local 08 | `labs/lesson11-kms-envelope-encryption` |
| Local 09 | `labs/lesson07b-cloudtrail-monitoring` |
| Local 10 | `labs/lesson14-config-lambda-remediation` |

---

## Knowledge Checks & quizzes
- Weekly **knowledge checks run inside the AWS Academy Learner Lab** (part of the licensed
  curriculum) — there is no separate quiz file to submit for those.
- Any additional in-class quiz is posted in Classroom at quiz time; the form **is** the submission.

## Term work / capstone
- If a capstone or write-up is assigned, submit it via **Google Classroom** with an **AI-tool usage
  disclosure** (state how you used any AI tool — search, code, translate — "None" is valid).

---

## Rules for every submission
- **Name + Student ID** on every file; labs are individual unless a task says otherwise.
- **AI-tool disclosure** on worksheets/reports.
- **Late:** 10% of the score you earned is taken off for every 24 hours (or part of 24 hours)
  after the due time, down to 0 after 10 days. Submit what you have.
- **Late work needs a viva:** the answers are walked through in the class right after the
  deadline, so a late worksheet is marked only after you explain it to the instructor in a short
  viva.
- **Local 10**, the last worksheet, closes on the date the instructor announces; nothing is
  accepted after it.
- **Extensions:** for illness or a documented technical failure, tell the instructor (before the
  deadline if you can). Extensions are decided case by case.
- These rules cover the local worksheets only. AWS Academy items follow the LMS due dates and the
  first-attempt rule.

---

## Academic Integrity & Anti-Cheating

This is a security course — we practice the same rigor on your own work. Assume your submission is checked.

- **Your flags are unique to you.** Each student receives **personalized lab flags** derived from
  your student ID. A flag is traceable to the person it was issued to — submitting someone else's
  flag is detected automatically and counts as a violation for **both** parties.
- **Your screenshots must show you.** Evidence must include a terminal running `printf '%s | %s | ' "$(whoami)" '<YOUR-STUDENT-ID>'; date '+%F %T %Z'` **in
  the same image as the evidence**. When the evidence is a browser page, a DevTools panel or a
  rendered response, put that terminal **beside the browser and capture the whole screen** — a
  cropped window carries nothing that identifies you, and the lab's own output is
  byte-identical for the whole cohort *by design*, so the stamp is the only thing that makes
  the shot yours. Generic or borrowed screenshots are not accepted.
- **Random live checks.** You may be asked to **reproduce a task or explain your fix live**. Answers
  you can't explain in your own words score zero.
- **Explain, don't copy.** Reflection and Audit-the-AI questions are graded on *your* reasoning about
  *your* results.

**Allowed:** discussing concepts, helping a classmate debug their *own* setup, using AI tools **if disclosed**.
**Not allowed:** sharing flags/answers/screenshots, copying a write-up, touching anyone else's Learner Lab.

Violations follow the [ethics & academic-integrity policy](ETHICS.md), the AWS Academy terms, and
KOSEN's conduct process.
