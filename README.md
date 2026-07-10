# Cloud Infrastructure & Security

A hands-on Year-5 course (subject code **02005097**) wrapping AWS Academy's Cloud Foundations +
Cloud Security Foundations curriculum with an original AIR-Sec assessment layer. Co-taught with
Shinya Oyama. Third arm of the same preregistered study as
[`software-security`](../KOSEN69%20-%20software-security/) and
[`security-cryptography`](../KOSEN69%20-%20security-cryptography/) — same pedagogy, same
research design, structurally different course (see below).

> ⚠️ **Status: DRAFT.** All 10 lesson topics built and Docker-verified (see
> [course-plan.md](course-plan.md)). `seed_flags.py`/CTFd wiring and the research instruments
> (H1–H4, adapted to this course's shared-AWS-baseline structure) are done. Not yet built: the
> third challenge-host and the deployable Docker images — do not use this for a live course yet.

> ⚠️ **This repo never contains AWS Academy's official material.** The underlying curriculum
> (Cloud Foundations, Cloud Security Foundations, all Learner Lab instructions) is Shinya's own
> AWS Academy Educator deployment and is explicitly licensed — *"may not be reproduced or
> redistributed... without prior written permission from Amazon Web Services, Inc."* (confirmed
> from the source material itself). Everything in this repo is an **original assessment layer**
> bolted onto those lesson topics, never a copy of AWS's content. See
> [course-plan.md](course-plan.md) for exactly what that means and why.

---

## Quick start

```bash
git clone <this-repo-url>
cd cloud-infrastructure-security
cd labs/lesson07-iam-policy-evaluation
cat README.md
docker compose up
```

**Base requirements:** Docker Desktop, Git. The AWS-side hands-on labs themselves run in AWS
Academy's own Learner Lab sandboxes (separate from this repo, provided through Classroom) — this
repo only holds the assessment layer we control.

## Course at a glance

Full topic map, block assignment, and design rationale: [course-plan.md](course-plan.md).

| Lesson | Topic | Kind | Block | Status |
|---|---|---|---|---|
| 1–3 | AWS Academy Modules 1–3 (intro, security fundamentals, access) | Conceptual | 1 | ✅ built |
| 4 | EC2 / Lambda / Elastic Beanstalk (SSRF → instance-role credential theft) | Hybrid | 1 | ✅ built |
| 5 | S3 static website hosting; Lambda + SNS (public-write bucket policy) | Lab | 1 | ✅ built |
| 6 | Load balancing & auto-scaling (Denial-of-Wallet) | Hybrid | 1 | ✅ built |
| 7 | IAM policy evaluation (wildcard-principal privilege escalation) | **Lab** | 1 | ✅ built |
| 7b | CloudTrail/CloudWatch monitoring (wrong aggregation key) | Hybrid | 2 | ✅ built |
| 10 | VPC networking (NACL rule-ordering) | Hybrid | 2 | ✅ built |
| 11 | KMS envelope encryption (Audit-the-AI) | **Conceptual** | 2 | ✅ built |
| 13 | S3 versioning / lifecycle / cross-region replication (Audit-the-AI) | Conceptual | 2 | ✅ built |
| 14 | Config + Lambda auto-remediation (inverted allowlist logic) | Hybrid | 2 | ✅ built |
| 15 | Reflection (existing AWS-graded mock exams) | — | — | n/a |

Every LAB/HYBRID lesson is a real Docker vulnerable/fixed pair, independently built and
Docker-verified (`docker compose up` → `exploit.py` → both PASS lines captured for real, then torn
down). Every CONCEPTUAL lesson is a worksheet-only Audit-the-AI exercise with 3–4 personalized
variants per student, each fact-checked against AWS's own public documentation.
