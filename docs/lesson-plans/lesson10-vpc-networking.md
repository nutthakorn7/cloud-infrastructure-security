# Lesson plan — Local 07: VPC and NACL rule ordering

Cloud Infrastructure and Security (02005097), Block 2, Weeks 13–14. AWS Academy
Cloud Security Foundations Module 4 and Lab 4.1 are the primary course material.
This local NACL simulation is an original follow-up, not a copy of Academy content.

| Item | Plan |
|---|---|
| Prior foundation | Week 03 Cloud Foundations Module 5 VPC lab and traffic-path diagram |
| Week 13 | Cloud Security Foundations Module 4 and Lab 4.1, Securing VPC Resources by Using Security Groups |
| Week 14 | Local NACL workshop, then Local 07 submission |
| Local 07 arms | C5R1: Part 2 AIR-Sec; C5R2: Part 1 Conventional |
| Due | Monday 8 February 2027, 23:59 Bangkok time, Week 14 Classroom Assignment |
| Score | 7 points: Technical 6 + Interdisciplinary 1 within Local Coursework |
| Submission | Local07 Answer Sheet copied for each student in Classroom |

## Objectives

- Explain security groups as instance-level, stateful, allow-only controls and
  network ACLs as subnet-level, stateless, ordered allow/deny controls.
- Trace source, destination port and return path through a VPC diagram.
- Predict which NACL rule matches first. A later deny cannot undo an earlier
  broad allow, regardless of how sensible the later rule looks.
- Explain the role of a public NAT gateway for outbound connections from a
  private subnet, assuming correct routes and other controls.
- Compare the vulnerable and fixed local rule sets and confirm both external
  denial and legitimate internal access.

## Week 13: 100-minute class

1. 5 min — Brief the assigned AWS Academy Lab 4.1 and verify console access.
2. 90 min — Students complete the official Lab 4.1 in their assigned sandbox.
   Use the current LMS instructions, which remain authoritative for the
   practical steps and Academy grading.
3. 5 min — Record security-group and NACL observations for Week 14.

Module 4 student slides cover VPC routing, NAT gateways, security groups,
NACLs, and stateful/stateless return traffic. The class has no local Docker
investigation or Local 07 submission. Students preview the worksheet only.

## Week 14: 100-minute local workshop

1. 10 min — Recall the Week 03 diagram and Week 13 lab. Mark where a subnet
   NACL and an instance security group apply.
2. 25 min — Trace first-match decisions for intended and unwanted sources.
   Teach the difference between HTTP response status and the decision
   carried in the simulator's JSON action field.
3. 45 min — C5R1 runs the downloaded local vulnerable/fixed pair on each
   student's own computer and records GET /rules plus request/response
   evidence for Part 2. C5R2 writes Part 1, using the supplied teaching
   scenarios and AWS module, without an assessed Docker requirement.
4. 20 min — Compare decisions, check legitimate traffic, discuss the
   simulation limits below, and give feedback.

The local add-on takes about 45–60 minutes. Students can finish their
assigned written explanation before the Monday deadline. The instructor
does not host a target; ports 8113 and 8114 bind only to each student's
localhost. No personal .env or per-student flag is required. The flag is a
shared demo marker and is not graded by itself.

The Week 03 VPC diagram and Week 13 lab notes are study aids. The Local 07
worksheet defines the actual deliverables. Part 1 is Q1–Q5. Part 2 is
GET /rules output, the exact POST request, vulnerable/fixed results,
Audit-the-AI and EiPE explanations. Do not require a separate diagram or
rule-evaluation table unless it appears in the assigned worksheet.

## What the local experiment proves

Both apps have an allow at rule #90 and a deny at #100 for destination port
5432. The vulnerable #90 allows 0.0.0.0/0, so an external request matches
before the deny. The fixed #90 allows 10.0.1.0/24, so an external request
falls through to deny #100 while 10.0.1.25 still matches allow #90.
Only the CIDR of rule #90 changes; the rule numbers do not change. This is
not an experiment that isolates the effect of renumbering.

The /check-access endpoint reports a simulated decision. HTTP 200 means the
API answered; the JSON action says allow or deny. Invalid JSON shape, source
IP or port returns HTTP 400. The engine uses actual IPv4 CIDR membership,
then sorts NACL rules by number and stops at the first match.

## Limits to explain in class

- The simulator models one inbound IPv4 source and one exact destination
  port. It does not send packets, attach a subnet or evaluate protocol,
  port ranges, separate outbound rules, or return traffic.
- There is no security-group engine, route table, NAT gateway, internet
  gateway, or AWS default-network-ACL behavior in this code. These are
  taught in the Academy material and Week 14 supplement instead.
- The model returns deny when no listed rule matches, analogous to the
  final AWS NACL default-deny row. It does not display a * row.
- A shared FLAG marker only signals a vulnerable allow response. It does
  not identify a student or prove the required request was submitted.
  Grade request, response, reasoning and an optional viva check.

## Instructor readiness checks

- The Week 13 bridge and Classroom Material say Local 07 starts in Week 14;
  the AWS lab occupies the Week 13 class.
- Week 14 Material includes the seven-slide NACL workshop supplement and
  the Classroom Assignment has the correct due date, arms, answer-sheet
  copy setting, six-criterion rubric and 7-point maximum.
- Students use only their own permitted Academy sandbox and downloaded
  local Docker pair. Keep credentials and signed URLs out of evidence.
- Verify the local pair on an available machine. No Windows machine or
  test execution is expected from the course owner.

## References

- AWS Academy Module 4 and Lab 4.1 in the enrolled LMS.
- AWS VPC User Guide: Network ACL rules; compare security groups and
  network ACLs; NAT gateway.
- Source README and worksheet in labs/lesson10-vpc-networking.
- Classroom Week 13 and Week 14 Draft Materials and Local 07 Assignment.
