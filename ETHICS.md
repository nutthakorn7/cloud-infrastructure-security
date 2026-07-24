# Ethics & Authorized-Use Policy

This course teaches cloud attack-and-misconfiguration techniques **so that students can architect and
defend cloud infrastructure correctly**. Misusing these techniques is both an academic-integrity
violation and, in most jurisdictions, a crime.

## Rules

1. **Only attack approved targets.** Two, and only two, are approved:
   - the intentionally vulnerable **local Docker labs** in `labs/` in this repository, and
   - **your own assigned AWS Academy Learner Lab sandbox** (provided through Google Classroom).

   Anything else is off-limits.
2. **Never touch real AWS resources you don't own.** Never test, scan, or attack AWS's own
   services/endpoints, another student's Learner Lab, any production AWS account, the university
   network, or any third-party cloud service — **not even to "look."** AWS's Acceptable Use Policy
   and the Learner Lab terms are binding; a boundary probe against real AWS infrastructure can get
   your account (and the class's) suspended and may be a criminal offense.
3. **Keep exploits in the sandbox.** The SSRF, IAM-privilege-escalation, public-bucket, and
   auto-remediation-bypass techniques here run **only** against the provided local labs. Do not
   deploy them, run them over the campus network, or exfiltrate real data.
4. **Handle Learner Lab credentials as secrets.** The temporary AWS keys/console access in your
   Learner Lab are secrets — never paste them into chat/screenshots, never commit them to Git, never
   share them. Use the provided `.gitignore` / `.env` patterns. (This is CWE-798 — the very failure
   the IAM and S3 lessons teach.)
5. **Practice responsible / coordinated disclosure.** If you incidentally discover a real
   vulnerability (in AWS, the university, anywhere), do not exploit it. Report it privately to the
   owner and to the instructor.

## Acknowledgment

Every student signs an acknowledgment of this policy in Lesson 1. Violations are handled under the
university's academic-integrity and student-conduct procedures, the AWS Academy terms, and may carry
legal consequences.

## Reference

- AWS Acceptable Use Policy: https://aws.amazon.com/aup/
- Responsible disclosure basics: https://cheatsheetseries.owasp.org/cheatsheets/Vulnerability_Disclosure_Cheat_Sheet.html
