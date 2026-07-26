# Course Specification — Cloud Infrastructure & Security

Outcome-based (OBE) specification for **this repository's teaching layer**, which sits on top of a
licensed AWS Academy curriculum. Read §2 before anything else: this course is structurally unlike
its two sibling courses, and the specification has to be honest about which part of the grade this
repository actually controls.

> **Fill before submission.** Fields marked ⬚ are institution-specific and are not recorded here:
> course code, semester/academic year, section, room, grading scale, and the programme's PLO list.

---

## 1. Course identification

| Field | Value |
|---|---|
| Course title | Cloud Infrastructure & Security |
| Course code | ⬚ |
| Credits | 1 |
| Level | Undergraduate |
| Baseline curriculum | AWS Academy **Cloud Foundations** + **Cloud Security Foundations** (~15 lessons), delivered through AWS's own Learner Lab sandboxes, Knowledge Checks and auto-graded assessments |
| This repository | 10 original add-on lessons (45–60 min each; one 60–90 min) layered onto specific AWS lesson topics |
| Instructors | Nutthakorn Chalaemwongwan · Shinya Oyama (co-taught) |
| Semester / Year | ⬚ |
| Programme | ⬚ |

## 2. How this course is put together — and what this specification covers

Roughly **40% of the final grade is AWS-graded** (6 Cloud Foundations items + 7 Cloud Security
Foundations items), identical for every student in every section. That portion is the *shared
baseline*: AWS teaches it, AWS grades it, and nothing in this repository alters it.

What this repository adds is an **assessment layer bolted onto specific lesson topics**, written
entirely from scratch:

- a per-student attributable artefact — a flag, a seeded misconfiguration, or a personalised
  parameter, and
- at least one AI-resilient task (*Audit the AI*, *Explain-in-Plain-English*, or *Prompt Problem*).

**Licensing constraint (confirmed, not inferred).** The AWS Academy materials carry an explicit
no-reproduction footer. **No AWS Academy file is ever copied into this repository.** The lessons
here describe the same *topics* — IAM, S3, KMS, VPC, CloudTrail, security-group remediation — in
our own words, with our own runnable simulations. This is a legal boundary, not a style preference;
see [course-plan.md](../course-plan.md) §"Licensing".

**Simulation, not emulation.** The add-on labs are small local Flask services that stand in for AWS
behaviour so students can exploit and fix something without an account. Where a simulation
simplifies a service, the lesson says so explicitly, so that no one leaves with a wrong model of
the real service.

## 3. Course learning outcomes (CLOs)

These are the outcomes of **this repository's layer**. The AWS Academy baseline carries its own
objectives, which this specification does not restate or claim.

| # | Outcome | Bloom |
|---|---|---|
| **CLO1** | **Apply the shared-responsibility model** to a named AWS service: state precisely what AWS secures, what the customer must secure, and how that split shifts between IaaS and managed services. | Analyse |
| **CLO2** | **Demonstrate** the misconfiguration classes this course covers — instance-role credential theft via SSRF, public bucket policy, identity-vs-resource policy evaluation gaps, blind monitoring, network ACL vs security-group confusion, key-management blast radius, non-compliant security groups — against a controlled local target, and explain the mechanism. | Apply / Analyse |
| **CLO3** | **Apply the correct control** for each — least-privilege policy, Block Public Access, KMS envelope encryption, subnet segmentation, CloudTrail/CloudWatch alerting keyed to the real threat shape, Config rules with remediation — and verify empirically that the original attack fails. | Create / Evaluate |
| **CLO4** | **Evaluate** cloud-security advice and configuration produced by others, including AI-generated answers, against AWS's documented behaviour, and communicate the finding plainly. | Evaluate |
| **CLO5** | **Practise** within the ethical and account boundaries of the sandbox, and produce evidence of their own work that withstands scrutiny. | Apply / Value |

## 4. CLO → assessment alignment

| Assessment | Owner | Weight | CLO1 | CLO2 | CLO3 | CLO4 | CLO5 |
|---|---|---|:--:|:--:|:--:|:--:|:--:|
| AWS Academy graded items (Knowledge Checks, labs, exams) | AWS | ~40% | ● | | ● | | |
| Add-on lesson worksheets (this repository, 10 lessons) | Us | ⬚ | ● | ● | ● | ● | ● |
| Per-student artefact — flag / seeded misconfiguration / personalised variant | Us | part of the worksheet mark | | ● | ● | | ● |
| *Audit the AI* / *EiPE* / *Prompt Problem* | Us | part of the worksheet mark | ● | | | ● | |

⬚ The split between the AWS-graded 40% and this layer's share of the remaining 60% is an
institutional decision and is not fixed anywhere in this repository — record it here once set.

## 5. CLO → PLO mapping

⬚ Replace with the programme's outcomes. **I** = Introduced, **R** = Reinforced, **M** = Mastered.

| CLO | ⬚ PLO1 | ⬚ PLO2 | ⬚ PLO3 | ⬚ PLO4 |
|---|:--:|:--:|:--:|:--:|
| CLO1 Shared responsibility | R | I | | |
| CLO2 Misconfiguration exploitation | M | R | | |
| CLO3 Applying the control | M | M | | R |
| CLO4 Evaluation & communication | | | M | |
| CLO5 Ethics & evidence | | | R | M |

## 6. Lesson schedule

Each row is an add-on session that follows the corresponding AWS Academy lesson. **Kind** follows
the repository's own classification: LAB = runnable vulnerable/fixed pair with a flag; HYBRID =
smaller demonstrable exploit plus conceptual material; CONCEPTUAL = analysis, no flag.

| AWS lesson | Add-on topic | Kind | Block | Lab folder | CLOs |
|---|---|---|:--:|---|---|
| 1–3 | AWS fundamentals, security basics, IAM access concepts | CONCEPTUAL | 1 | `labs/lesson01-03-aws-fundamentals-intro` | 1, 4 |
| 4 | EC2 instance roles, Lambda, Elastic Beanstalk — SSRF → instance-role credential theft | HYBRID | 1 | `labs/lesson04-ec2-lambda-beanstalk` | 2, 3 |
| 5 | S3 static hosting + Lambda/SNS — public-write bucket policy | LAB | 1 | `labs/lesson05-s3-static-site-lambda-sns` | 2, 3 |
| Lab 6 | Load balancing & auto-scaling under load | HYBRID | 1 | `labs/lesson06-load-balancing-autoscaling` | 2, 3 |
| 7 | IAM privilege escalation — identity vs. resource policy evaluation | LAB | 1 | `labs/lesson07-iam-policy-evaluation` | 1, 2, 3 |
| 7 (2nd topic) | CloudTrail + CloudWatch + EventBridge alerting on failed logins | HYBRID | 2 | `labs/lesson07b-cloudtrail-monitoring` | 2, 3 |
| 10 | VPC networking — subnets, NAT, security groups vs. network ACLs | HYBRID | 2 | `labs/lesson10-vpc-networking` | 2, 3 |
| 11 | S3 SSE-KMS — envelope encryption and key-disable blast radius | CONCEPTUAL | 2 | `labs/lesson11-kms-envelope-encryption` | 1, 4 |
| 13 | "Cafe" challenge — S3 versioning, lifecycle, cross-region replication | CONCEPTUAL | 2 | `labs/lesson13-s3-versioning-lifecycle-replication` | 1, 4 |
| 14 | AWS Config + Lambda auto-remediation of a non-compliant security group | HYBRID | 2 | `labs/lesson14-config-lambda-remediation` | 2, 3 |
| 15 | AWS-graded reflection / wrap-up | — | — | *(no add-on)* | — |

Block assignment follows the preregistration: **Section A** = Block 1 AIR-Sec / Block 2
Conventional; **Section B** = the reverse.

## 7. Teaching and learning methods

- **AWS Academy lab first, add-on second.** Students complete the real Learner Lab — that is where
  the AWS console, its UI and its guard-rails are learned. The add-on then attacks and fixes the
  same idea locally, without an account, so the security reasoning is exercised rather than the
  click-path.
- **Per-student attributable artefacts.** Flags are minted per student (`instructor/seed_flags.py`),
  and CONCEPTUAL lessons issue per-student planted-error variants instead of flags.
- **AI-resilient assessment.** Every add-on carries at least one of *Audit the AI*, *EiPE* or
  *Prompt Problem* — cloud security is a domain where AI answers are fluent and frequently wrong
  about specifics such as policy-evaluation order or what a scanner can actually parse.
- **Explicit simplification notices.** Where a local simulation departs from real AWS behaviour,
  the lesson says so in the same paragraph.

## 8. Assessment criteria and grading

The AWS-graded portion is scored by AWS. This layer's worksheets are graded against the rubric in
each lesson's worksheet; the per-student artefact is an integrity control that also carries marks.
Grading scale and the exact weight of this layer: ⬚.

## 9. Verification of student achievement

- Every add-on lesson has an instructor-held answer key, reviewed against the published worksheet
  whenever lesson content changes.
- Flags and planted-error variants are per student, so duplicate submissions are detectable rather
  than a matter of judgement.
- The control ("fixed") application in each lab never emits a flag — evidence of a flag is evidence
  the student exploited the vulnerable path themselves.
- Attainment is reviewed at the end of term by mapping this layer's scores back to §4; the
  AWS-graded 40% is reported separately, as it is identical for all sections by construction.

## 10. Resources

- This repository: 10 add-on lessons with runnable local targets.
- AWS Academy Learner Lab (the baseline curriculum) — accessed through AWS, never mirrored here.
- Docker Desktop on the student's own machine for every add-on lab.
- Rules of engagement: [ETHICS.md](../ETHICS.md) · Submission: [SUBMISSION.md](../SUBMISSION.md)

## 11. Academic integrity and AI policy

AI assistants are permitted and are assessed directly through the *Audit the AI* tasks. What is
graded is the student's own understanding, which is why artefacts are per-student and why the
control app is flagless. Submitting a configuration or explanation a student cannot reproduce is an
academic-integrity matter under ⬚ (institutional policy).

---

*Lesson plans that instantiate this specification: [`docs/lesson-plans/`](lesson-plans/).*
