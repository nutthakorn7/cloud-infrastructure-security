# Lesson plan — Local 06: IAM policy evaluation

Cloud Infrastructure and Security (02005097), Block 2, Weeks 11–12. AWS Academy Cloud
Security Foundations is the primary source. This local simulation is an original add-on;
it does not reproduce Academy lab instructions.

| Item | Plan |
|---|---|
| Week 11 | Security Foundations Modules 1–2; instructor-led introduction to Module 3 policy and role concepts |
| Week 12 | Module 3 and Lab 3.1, Using Resource-Based Policies to Secure an S3 Bucket |
| Local 06 | C5R1: Part 2 AIR-Sec; C5R2: Part 1 Conventional |
| Due | Monday 25 January 2027, 23:59 Bangkok time, in the Week 12 Classroom Assignment |
| Score | 8 points within the 60-point Local Coursework category |
| Submission | Local06 Answer Sheet, copied for each student in Classroom; no PDF required |

## Learning outcomes

- Distinguish identity-based policy, resource-based policy, and role trust policy.
- Trace which principal makes a request after AssumeRole. A successful role assumption
  does not itself grant every S3 action.
- Explain how a bucket resource policy can grant access when an identity policy has no
  relevant Allow, subject to other applicable controls and explicit Deny.
- Show how a broad Principal and unnecessary PutObject permission create an unsafe
  policy; verify a fixed policy against both unwanted and intended requests.
- Explain why the local engine is a simplified simulation, not AWS IAM.

## Week 11: 100-minute class

1. 10 min — Review shared responsibility from Modules 1–2. AWS evaluates requests;
   the customer configures identity, trust, bucket policy and storage controls.
2. 25 min — Introduce IAM users, roles, trust boundaries, and the difference between
   assuming a role and receiving resource permissions. Use the supplied Module 3
   introduction for these concepts only.
3. 45 min — Give a guided policy trace. Students identify the request principal,
   resource, action, relevant identity/resource statements, and provisional decision.
   Use instructor-provided examples taught in this slot.
4. 20 min — Debrief and correct mistaken claims about wildcard Principal and role
   assumptions. Students preview their assigned Local 06 part, but do not answer
   Lab 3.1-dependent questions or submit the worksheet.

Week 11 has no Local 06 submission. The Classroom Week 11 Material and the source
worksheet both state that Lab 3.1 and the assessed work follow in Week 12.

## Week 12: 100-minute class and follow-up

1. 10 min — Brief Module 3 and the Academy lab.
2. 60 min — Students complete the official Lab 3.1 in their assigned AWS Academy
   sandbox. Use current LMS instructions; Academy records its own result.
3. 20 min — Compare identity and resource policy outcomes in the lab with the
   local IAM case. Briefly teach how Conditions and S3 Block Public Access
   can change a wildcard policy's effective result before students answer
   Part 1 Q3 or Part 2b. Part 2 students can start their downloaded Docker lab on
   their own computers. The full local add-on takes approximately 60–90 min,
   so they finish outside this 20-minute slot before the deadline.
4. 10 min — Evidence and viva debrief.

C5R2 answers Part 1, including the Lab 3.1 role/bucket question. C5R1 does
Part 2: an anonymous write on the vulnerable local app, the identical request
on the fixed app, an audit of a suggested policy, and a plain-language explanation.
Students do only their assigned part.

The instructor does not host a shared target. Students download or update the
public repository and run ports 8107 and 8108 on their own machines with Docker
Desktop. No personal .env or per-student flag is required. Any FLAG marker in
the response is shared demo data and receives no score by itself. Mark the full
request, both responses, the student's explanation, and a live spot-check when
needed. Do not ask the owner to provide a Windows machine or run the tests.

## What the local experiment proves

The vulnerable bucket3 policy allows get and put for Principal "*". In this
simulation an anonymous PUT succeeds. The fixed policy names
BucketsAccessRole and allows get only, so both anonymous and role-based PUTs
return 403. These two policy dimensions change together. A before/after PUT
result cannot isolate Principal scoping as the sole cause of the denial.

The role can still PUT bucket2 on the fixed app. A role-based GET of an absent
bucket3 object returns 404 NoSuchKey rather than 403 AccessDenied: read was
authorized, but that object does not exist. This is the intended-access
control check students should be able to explain.

The Audit-the-AI question uses a wildcard Principal with a
PrincipalTag/team=backend condition. The tag condition does not mean "only
BucketsAccessRole"; another authenticated principal with the matching tag
can satisfy it. An anonymous request has no principal tag and does not meet
this StringEquals condition. Do not claim this particular statement grants
anonymous access. AWS S3 Block Public Access can also override a broad bucket
policy; the local simulation omits it.

## Simulation limits to say aloud

- The local /assume-role endpoint issues a token for a known role without
  authenticating the caller or evaluating a trust policy. Real STS does both.
- The engine has no explicit Deny, permissions boundary, session policy, SCP,
  account boundary, S3 Block Public Access, or full IAM evaluation order.
- It uses get/put strings rather than full AWS actions and ARNs.
- It gives both devuser and BucketsAccessRole empty identity action lists,
  isolating resource policy behavior. The Academy lab may differ.
- Tokens are in memory. After a container restart students must assume the
  role again. A token from one target does not work on the other.
- The public demo marker can be returned by any successful vulnerable
  bucket3 PUT, including one with a role token. It does not prove the
  required anonymous request; inspect the submitted command.

## Instructor checks

- Week 11 Material covers only Modules 1–2 plus the taught Module 3
  introduction; Lab 3.1 is in Week 12.
- Week 12 Material and Local 06 Assignment use the same due date and the
  correct Part assignment for each section.
- The answer sheet remains set to "Make a copy for each student" and the
  Assignment has 8 points and the six-criterion rubric.
- Ask students to keep credentials and signed URLs out of evidence.
- Test the local Docker targets independently on an available machine.
  Windows-specific behavior remains unverified until evidence from an
  actual Windows environment exists; it is not a request for the owner to
  run anything.

## References

- AWS IAM User Guide: Policy evaluation logic; Principal policy element;
  controlling access using principal tags.
- AWS S3 User Guide: Block Public Access.
- Source worksheet and README in labs/lesson07-iam-policy-evaluation.
- Classroom Week 11 and Week 12 Draft Materials and Local 06 Assignment.
