"""Build original, editable Cloud course bridges for Weeks 01–18.

These short decks accompany the licensed AWS Academy slide decks in Classroom.
They contain no AWS Academy slides or lab instructions.
"""

from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path
import subprocess

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt


HERE = Path(__file__).resolve().parent
LOGO = HERE.parent / "week07-08-s3-data-protection" / "kosen-kmitl-logo.png"
OUT = HERE / "output"

BG = RGBColor(245, 247, 250)
NAVY = RGBColor(16, 24, 40)
BLUE = RGBColor(0, 122, 194)
DARK_BLUE = RGBColor(0, 90, 145)
ORANGE = RGBColor(227, 82, 5)
GREY = RGBColor(94, 102, 115)
BORDER = RGBColor(213, 220, 228)
WHITE = RGBColor(255, 255, 255)

# Each bridge fills the course-specific gap between the AWS Academy deck and
# our own worksheet. The AWS module/lab remains the main teaching material.
WEEKS = [
    dict(n=1, title="Cloud concepts and responsibility", aws="Cloud Foundations · Modules 1–3", practice="Shared Responsibility discussion", local="Local 01 starts · C5R1 Part 1 / C5R2 Part 2", due="Local 01 due 16 Nov", concept=(
        ("AWS", "Secures the cloud infrastructure and its physical facilities."),
        ("Customer", "Controls data, IAM settings and the EC2 guest operating system."),
        ("Service choice", "Managed services shift some operating tasks to AWS. Check the service boundary.")),
        check="Who installs security updates on an EC2 guest OS?", before="Open the AWS modules and identify the service model.", during="Compare EC2 with a managed service, then begin your assigned Part.", after="Keep your Local 01 evidence and use the Week 02 submission guide."),
    dict(n=2, title="Cloud security and IAM", aws="Cloud Foundations · Module 4", practice="Identity and access check", local="Local 01 submission", due="Local 01 due 16 Nov", concept=(
        ("Implicit deny", "A new IAM user has no permissions until an applicable Allow grants them."),
        ("Scoped allow", "State the action and resource the identity needs for its work."),
        ("Explicit deny", "An applicable Deny overrides an Allow.")),
        check="What can a brand-new IAM user do before a policy grants access?", before="Review shared responsibility, root-user hygiene and MFA.", during="Trace one request through a simple IAM decision.", after="Submit only your assigned Local 01 Part in Classroom."),
    dict(n=3, title="VPC and traffic paths", aws="Cloud Foundations · Module 5", practice="Lab 2 · VPC networking", local="VPC diagram for later Local 07", due="No Local due this week", concept=(
        ("Subnet", "Place an instance in a subnet with a clear public or private purpose."),
        ("Route", "Trace the destination and next hop before claiming a path works."),
        ("Filter", "Check the security group on the instance traffic path.")),
        check="Can a public subnet alone make an instance reachable?", before="Open Module 5 and the Week 02 lab-entry guide.", during="Run the AWS VPC lab and draw one end-to-end traffic path.", after="Keep the diagram. Local 07 will reuse the network model."),
    dict(n=4, title="EC2 roles and URL fetching", aws="Cloud Foundations · Module 6 EC2 portion", practice="Lab 3 · Introduction to Amazon EC2", local="Local 02 starts · C5R1 Part 1 / C5R2 Part 2", due="Local 02 due 30 Nov", concept=(
        ("Instance role", "An EC2 app can receive temporary credentials without a key in its code."),
        ("Unsafe fetch", "A server that fetches any user URL can be asked to reach its own metadata path."),
        ("Control check", "Reject internal targets and confirm an intended fetch still works.")),
        check="Why is blocking only the literal metadata IP insufficient?", before="Open the EC2 slides and prepare Docker if you are assigned Part 2.", during="Complete the EC2 lab. C5R1: discuss Part 1. C5R2: run the local SSRF lab.", after="Submit the assigned Part in Local 02. Keep credentials out of the sheet."),
    dict(n=5, title="Lambda, Beanstalk and events", aws="Cloud Foundations · Module 6 remaining topics", practice="Lambda and Beanstalk formative activities", local="Local 03 preview · S3 lab in Week 06", due="Local 03 due 14 Dec", concept=(
        ("Trigger", "An event invokes a Lambda function when the configured condition occurs."),
        ("Publish", "The function can publish a message to an SNS topic."),
        ("Delivery", "Email subscription must be confirmed; Publish success alone does not prove receipt.")),
        check="Will a subscriber confirmed later receive an earlier SNS message?", before="Open the Lambda and Elastic Beanstalk sections of Module 6.", during="Try the formative activities and trace the Lambda-to-SNS path.", after="Review the Lambda/SNS example. Do the S3 lab and submit Local 03 after Week 06."),
    dict(n=6, title="Storage and S3 public write", aws="Cloud Foundations · Module 7", practice="Lab 4 · EBS", local="Local 03 · C5R1 Part 1 / C5R2 Part 2", due="Local 03 due 14 Dec", concept=(
        ("EBS", "A volume gives an EC2 instance block storage; use the AWS lab for the workflow."),
        ("Public read", "A website policy may permit anonymous reads of intended objects."),
        ("Public write", "An unintended PutObject permission lets an anonymous caller change content.")),
        check="Does a public website need anonymous PutObject?", before="Open Module 7 and the EBS lab. C5R2: prepare Docker.", during="Finish the EBS lab. C5R1: analyze Part 1. C5R2: test S3 policies locally.", after="Submit your Part in Local 03. C5R2 includes GET/PUT results."),
    dict(n=7, title="Databases and object history", aws="Cloud Foundations · Module 8", practice="Lab 5 · RDS; S3 supplement slides 1–3", local="Local 04 starts · C5R1 Part 1 / C5R2 Part 2", due="Local 04 due 28 Dec", concept=(
        ("RDS", "Use the AWS lab to distinguish database service tasks from customer tasks."),
        ("Versioning", "An overwrite creates a new full object version; the old one stays noncurrent."),
        ("Lifecycle", "Current and noncurrent versions need separate transition actions.")),
        check="Does S3 Versioning store a full prior object or only a difference?", before="Open Module 8 and the S3 supplement for Local 04.", during="Complete the RDS lab, then work through Versioning and Lifecycle examples.", after="Begin your assigned Local 04 Part. The recovery case continues in Week 08."),
    dict(n=8, title="Architecture and recovery", aws="Cloud Foundations · Module 9", practice="S3 supplement slide 4 · Replication", local="Local 04 · C5R1 Part 1 / C5R2 Part 2", due="Local 04 due 28 Dec", concept=(
        ("Live rule", "S3 replication handles eligible new and updated objects after configuration."),
        ("Existing data", "Use a separate Batch Replication job for objects that predate the rule."),
        ("Recovery test", "Check destination versions and run a restore, not only the rule settings.")),
        check="Does enabling live replication copy two years of existing objects?", before="Open Module 9 and the S3 supplement's recovery slide.", during="Map a source-to-destination recovery path.", after="Submit the assigned Local 04 Part with a coverage check."),
    dict(n=9, title="Scaling and cost exposure", aws="Cloud Foundations · Module 10", practice="Lab 6 · Load Balancing / Auto Scaling", local="Local 05 starts · C5R1 Part 1 / C5R2 Part 2", due="Local 05 due 11 Jan", concept=(
        ("Traffic", "A public endpoint accepts requests that drive application work."),
        ("Scale", "Unrestricted expensive requests can keep adding capacity up to the configured limit."),
        ("Control", "Limit abusive demand, then verify ordinary requests still succeed.")),
        check="What evidence shows the fix limits load without breaking legitimate use?", before="Open Module 10 and the scaling lab.", during="Run the AWS lab, then compare local load and cost outcomes.", after="Begin your assigned Local 05 Part; keep request and response evidence."),
    dict(n=10, title="Foundations completion", aws="Cloud Foundations · course assessment", practice="Foundations review; assessment outside class", local="Local 05 · C5R1 Part 1 / C5R2 Part 2", due="Local 05 due 11 Jan", concept=(
        ("Review", "Use the AWS modules and graded-lab feedback to find weak topics."),
        ("Assessment", "Complete the Course Assessment in AWS Academy under its LMS rules."),
        ("Record", "Keep the LMS result and submit Local 05 only in Classroom.")),
        check="Which work belongs in AWS Academy, and which belongs in Classroom?", before="Check the LMS assessment window and Local 05 evidence.", during="Use class time for targeted Foundations review.", after="Complete the AWS assessment and submit Local 05 by its due date."),
    dict(n=11, title="Security principles and IAM", aws="Cloud Security Foundations · Modules 1–2", practice="Policy and role reasoning", local="Local 06 preview · C5R1 Part 2 / C5R2 Part 1", due="Local 06 due 25 Jan", concept=(
        ("Principal", "Identify who makes the request and which role session they use."),
        ("Action", "Name the requested operation and resource precisely."),
        ("Decision", "Evaluate applicable Allow and Deny statements in context.")),
        check="What changes when the request runs under an assumed role?", before="Open CSF Modules 1–2; bring one access-control question.", during="Trace an IAM request with the instructor's Module 3 introduction.", after="Keep your policy trace. Complete Local 06 after the Week 12 lab."),
    dict(n=12, title="Effective permissions", aws="Cloud Security Foundations · Module 3", practice="Lab 3.1 · S3 resource policies (60 min)", local="Local 06 · C5R1 Part 2 / C5R2 Part 1", due="Local 06 due 25 Jan", concept=(
        ("Identity", "The user or role policy grants actions to the requesting identity."),
        ("Role", "Trust and assumption determine which role session can make the next request."),
        ("Resource", "A bucket policy can grant resource access; an applicable explicit Deny wins.")),
        check="Can a bucket policy change the result of an implicit identity-policy deny?", before="Open Module 3 and the Week 02 lab-entry guide.", during="Complete Lab 3.1 and trace the user-to-role-to-bucket path.", after="Submit your assigned Local 06 Part with the final permission evidence."),
    dict(n=13, title="VPC security controls", aws="Cloud Security Foundations · Module 4", practice="Lab 4.1 · security groups (90 min)", local="Local 07 preview · C5R1 Part 2 / C5R2 Part 1", due="Local 07 due 8 Feb", concept=(
        ("Security group", "Apply instance-level traffic rules; return traffic is stateful."),
        ("Network ACL", "Apply ordered subnet-level rules in both directions."),
        ("Admin path", "Compare bastion access with Session Manager in the lab.")),
        check="Which control is attached to the subnet, and which to the instance?", before="Open Module 4 and the lab before class; check console access.", during="Use 5 minutes to orient, 90 for the AWS lab and 5 to capture results.", after="Keep your lab notes; begin Local 07 in the Week 14 workshop."),
    dict(n=14, title="NACL first-match reasoning", aws="Local workshop · CSF Module 4 recap", practice="NACL rule-order simulation", local="Local 07 · C5R1 Part 2 / C5R2 Part 1", due="Local 07 due 8 Feb", concept=(
        ("Order", "Read NACL rules from the lowest rule number upward."),
        ("Match", "The first matching allow or deny decides the packet."),
        ("Verify", "Test both the blocked path and an intended permitted path.")),
        check="Can a later deny undo an earlier broad allow?", before="Bring the Week 03 VPC diagram and Week 13 lab notes.", during="Run the local rule-order case and explain each decision.", after="Submit only your assigned Local 07 Part and its requested evidence."),
    dict(n=15, title="KMS and data protection", aws="Cloud Security Foundations · Module 5", practice="Lab 5.1 · KMS (75 min)", local="Local 08 preview · C5R1 Part 2 / C5R2 Part 1", due="Local 08 due 22 Feb", concept=(
        ("Key", "Create and authorize a KMS key for the data-protection workflow."),
        ("Object", "Use the lab to observe S3 server-side encryption with KMS."),
        ("Evidence", "Inspect CloudTrail KMS events and the effect of disabling the key.")),
        check="What evidence distinguishes an encrypted object from usable access to it?", before="Open Module 5 and the KMS lab; check console access.", during="Use 10 minutes to orient, 75 for Lab 5.1 and 15 to capture results.", after="Keep your lab notes; begin Local 08 in the Week 16 workshop."),
    dict(n=16, title="Envelope encryption analysis", aws="CSF Module 5 recap · local workshop", practice="Data-key and key-access reasoning", local="Local 08 · C5R1 Part 2 / C5R2 Part 1", due="Local 08 due 22 Feb", concept=(
        ("Data key", "Use a data key to encrypt the object data."),
        ("KMS key", "Protect the data key with a KMS key and control its use."),
        ("Access", "A later decrypt depends on policy and key state, not only stored ciphertext.")),
        check="Why can ciphertext exist while decryption is unavailable?", before="Bring the Week 15 KMS lab notes; check which Local 08 Part your class does.", during="Trace encrypt, store and decrypt before answering your assigned Part.", after="Submit your assigned Local 08 Part with a reasoned key-state check."),
    dict(n=17, title="Monitoring and alerting", aws="Cloud Security Foundations · Module 6", practice="Lab 6.1 · CloudTrail / CloudWatch (75 min)", local="Local 09 · C5R1 Part 2 / C5R2 Part 1", due="Local 09 due 1 Mar", concept=(
        ("Record", "CloudTrail records the relevant API change."),
        ("Detect", "EventBridge or a CloudWatch metric filter matches the event."),
        ("Notify", "SNS delivery needs a confirmed subscription; inspect alarm and log evidence.")),
        check="Does a CloudTrail trail by itself send an email alert?", before="Open Module 6 and confirm access to an email inbox for the SNS step.", during="Complete Lab 6.1; capture the event, rule and alert evidence.", after="Use the Local 09 slides and lab outside class; submit by 1 Mar.",
        extra=("Outside the Week 17 class", (("Local 09", "Apply the detector model", "Study slides 5–7, then complete only your assigned Part outside class."), ("Module 8", "Bridge work", "Use the assigned LMS material to finish the security course sequence."), ("AWS Academy", "Course Assessment", "Take it under LMS instructions; check the deadline in Classroom.")), "Local 09 due 1 Mar; late submissions close 8 Mar at 23:59.")),
    dict(n=18, title="Config and Lambda remediation", aws="Cloud Security Foundations · Module 7", practice="Lab 7.1 · Config / Lambda (75 min)", local="Local 10 · C5R1 Part 2 / C5R2 Part 1", due="Local 10 closes 8 Mar", concept=(
        ("Observe", "AWS Config records the security-group configuration change."),
        ("Remediate", "A separately configured response invokes Lambda to restore intended inbound rules."),
        ("Prove", "Check the final security group and CloudWatch Logs, not only function success.")),
        check="What proves the dangerous rule was removed?", before="Open Module 7 and the remediation lab.", during="Complete Lab 7.1 and compare before-and-after rules.", after="Use slides 5–7 and complete Local 10 outside class by 8 Mar.",
        extra=("Outside class / course closure", (("Lab evidence", "Verify", "Keep final security-group rules and relevant CloudWatch log events."), ("Local 10", "Submit", "Use the local lab and assigned Part; turn in by 8 Mar at 23:59."), ("Reflection", "Explain", "State what failed, what changed, and how the final state was checked.")), "Local 09 late submissions also close 8 Mar at 23:59.")),
]

# Worksheet-specific topics that need explicit teaching before the local
# assessment. Keep these in the teaching week.
SUPPLEMENTS = {
    4: ("Instance role and unsafe fetch", (
        ("Metadata", "On the instance", "The EC2 metadata endpoint is reachable from the instance; an outside caller cannot fetch it directly."),
        ("SSRF", "Borrowed access", "An attacker-controlled URL makes the app fetch an internal target using the instance's network access."),
        ("Fix", "Check destinations", "Allow intended hosts; validate resolved addresses and redirects before each request. Keep the role least-privileged.")),
        "Local 02: a login check alone does not make an unsafe URL safe."),
    9: ("Scaling and the local abuse case", (
        ("Traffic path", "LB → target group → ASG", "The load balancer routes to healthy targets; the Auto Scaling Group adds or removes instances within its limits."),
        ("Cost bound", "Minimum and maximum", "Minimum preserves baseline capacity; maximum limits scale and cost, but a high maximum still permits costly abuse."),
        ("Two controls", "Key + rate limit", "An API key identifies an allowed caller; a rate limit bounds calls even if a valid key is leaked.")),
        "Local 05: check that normal requests still succeed after both controls are applied."),
    12: ("Who a bucket policy can admit", (
        ("Wildcard", "Principal: *", "The policy names every principal, including anonymous callers, before any conditions are evaluated."),
        ("Tag condition", "A narrower match", "A PrincipalTag condition excludes anonymous callers without that tag, but does not name one intended role."),
        ("Scope", "Name the role", "Use the intended role as Principal and check its assumption and resource permissions.")),
        "Local 06: a tag condition is not the same as scoping access to BucketsAccessRole."),
    16: ("SSE-KMS envelope and key states", (
        ("Upload", "Two data-key copies", "S3 requests a data key, uses the plaintext copy for object encryption, and keeps the encrypted copy with the object."),
        ("Read", "KMS on later read", "S3 discards the plaintext data key. In the worksheet's per-object SSE-KMS flow, a later read calls KMS to decrypt its stored copy."),
        ("Key state", "Recover or lose access", "Disabled can be re-enabled; cancelled pending deletion leaves the key disabled; completed deletion is irreversible.")),
        "Local 08 uses per-object SSE-KMS without S3 Bucket Keys; ciphertext alone is not enough."),
    17: ("Choose what the detector counts", (
        ("Pair", "IP + username", "A threshold on each pair can miss a spray that tries many usernames once from one IP."),
        ("Spray", "Group by source", "The local detector groups by source IP to see many usernames from the same origin."),
        ("Brute force", "Group by username", "Counting attempts for one username detects a different pattern. Test both patterns against the rule.")),
        "Local 09 simulates grouping; avoid high-cardinality CloudWatch metric dimensions in production."),
    18: ("Detect, remediate, verify", (
        ("Config", "Evaluate", "A Config rule marks a resource compliant or noncompliant; that result does not itself change the resource."),
        ("Lambda", "Enforce allowlist", "A configured route invokes remediation. Keep ports 80 and 443; remove disallowed inbound rules such as port 22."),
        ("Check", "Inspect final rules", "A successful function run does not prove the rule set is safe. Compare before and after, then inspect logs.")),
        "Local 10: trace each rule through the allowlist code before calling it a fix."),
}


# Plain-language add-on for Week 03 (original wording; no AWS Academy material).
# Teacher notes hold the answers. NACL and NAT stay for Weeks 13-14 and Local 07.
WEEK3_PLAIN = (
    ('PLAIN WORDS', 'What is a VPC?', (
        ('Think of', 'VPC = a fenced compound', 'Your own logically separate network in AWS. Access rules decide who can reach what.'),
        ('Inside it', 'Subnet = a section', 'A VPC is split into subnets. Each subnet sits in one Availability Zone.'),
        ('In the subnet', 'Instance = a server', 'Your EC2 server sits in one subnet, like a person in one room.')),
     'A new custom VPC has no internet connection until you add one.',
     "TEACHER NOTE (plain-language add-on for Week 03). Use the compound analogy: the fence is the VPC, the sections are subnets, the person in a room is the EC2 instance. Be precise on three points. (1) A VPC is logically isolated, not magically private: who can reach what depends on routes and security rules. (2) A newly created custom VPC has no internet connection until an internet gateway and routes are added; the default VPC already has internet connectivity configured; traffic inside the VPC still depends on routing and security rules. (3) Say 'section' or 'subnet', not 'zone': a subnet lives in one Availability Zone, and 'zone' already means something in AWS. Do not copy AWS Academy slides; this is our own wording. Ask: where would you put a database, and where a website?"),
    ('PUBLIC OR PRIVATE', 'What makes a subnet public?', (
        ('Public subnet', 'Has a route to the internet', 'Its route table sends internet traffic to an internet gateway.'),
        ('Private subnet', 'No direct route to the internet', 'Used for things like a database. Access comes only through paths you set up.'),
        ('Security group', 'A firewall on the server', 'It lists the traffic allowed in and out. Replies to allowed traffic are let through.')),
     'Can a public subnet alone make an instance reachable?',
     "TEACHER NOTE. Answer to the question on the band: NO. A public subnet is not enough. This is a simplified checklist for a server reached directly from the internet, and it assumes an internet gateway is attached to the VPC, the network ACLs allow the traffic, and an application is listening: (1) the subnet's route table sends internet traffic to the internet gateway (that route is what makes a subnet public), (2) the instance has a public address, and (3) its security group allows that port. Three short cases to try: a subnet with no route to the gateway is not a public subnet; no public address; port not allowed. A private subnet has no direct route to the internet gateway, but outsiders can still reach things in it through paths someone configures, such as a load balancer or a VPN. Keep NACLs and NAT for Week 13-14 and Local 07."),
    ('DRAW YOUR PATH', 'Draw one traffic path', (
        ('Step 1', 'Draw the subnet and server', 'Draw the VPC, a subnet inside it, and the web server inside the subnet.'),
        ('Step 2', 'Add the path and the checks', "Draw the internet gateway at the VPC edge. Mark the subnet's route and the server's security group."),
        ('Step 3', 'Find the missing piece', 'Remove one piece. Say what breaks. That is the skill you will reuse.')),
     'Keep your drawing. Local 07 (Week 14) builds on it with network ACLs and NAT.',
     "TEACHER NOTE. This is the in-class drawing task, with an example format so students know what to draw. Model drawing: a box for the VPC; inside it a public subnet box; inside that the web server with its security group attached (allowing 443); the subnet's route table with 0.0.0.0/0 pointing to the internet gateway; the internet gateway drawn on the VPC edge; an arrow from the Internet through the gateway to the server. The route table and security group are settings that the traffic is checked against, not boxes the traffic travels through. Accept a hand drawing or a photo. Local 07 does not ask for a diagram, so say only that the drawing helps them think about Weeks 13-14, not that it is required."),
)


# Plain-language add-on for Week 04 (original wording; no AWS Academy material).
# Teacher notes hold the answers and link to Local 02 Part 1 Q1, Q2, Q4, Q5 and Q6.
WEEK4_PLAIN = (
    ('PLAIN WORDS', 'What does an instance role do?', (
        ('Think of', 'Role = what it may do', 'A role is a set of permissions. AWS gives the server temporary credentials (a badge) to use it.'),
        ('Where from', 'IMDS = the badge desk', 'The instance metadata service (IMDS) hands the server its badge. Internet users cannot reach it directly.'),
        ('Why it is good', 'No key in the code', 'No long-lived key sits in GitHub. But a badge can still be stolen, so protect it.')),
     'Safer than an access key in the code, but the temporary badge must still be protected.',
     'TEACHER NOTE (plain-language add-on for Week 04, links to Local 02 Part 1 Q1, Q2 and Q5). Keep three ideas apart: the role is the set of permissions; the temporary credentials are the badge the server uses; the instance metadata service (IMDS, at 169.254.169.254) is the instance-local service that supplies metadata and, when a role is attached, its temporary credentials. Internet clients cannot reach that address directly, but vulnerable software running on the instance can relay a request to it. Temporary credentials still must be protected: a stolen badge works until it expires, so give the role only the permissions it needs (least privilege) to limit the damage. Own wording; no AWS Academy slides copied.'),
    ('PLAIN WORDS', 'What is SSRF?', (
        ('A normal feature', 'Preview this link', 'You type a URL. The server downloads that page and shows it to you.'),
        ('The trick', 'Ask for its own desk', 'In our lab the attacker types the metadata address and the weak app fetches its own badge.'),
        ('The name', 'SSRF', 'Server-Side Request Forgery: the server is tricked into making a request for the attacker.')),
     'The attacker never touches the badge desk. The trusted server does it for them.',
     "TEACHER NOTE. SSRF = Server-Side Request Forgery. Walk through the local lab in words only: the vulnerable app's /fetch-preview does a plain requests.get(url) on whatever URL it is given, so a URL that points at the app's own metadata route returns the fake credentials. Say clearly that this is a local simulation of an IMDSv1-style attack. In real AWS, IMDSv2 asks for a session token first, so a simple relayed GET does not return credentials; requiring IMDSv2 is one real control, and the app should still be fixed. Do not ask students to probe real metadata endpoints or other systems; use only the supplied local scenario."),
    ('CHECK THE FIX', 'How do we check the fix?', (
        ('Check 1', 'A normal request', 'Name one request that should still work after the fix. What should happen?'),
        ('Check 2', 'An attack request', 'Name one request that should be refused after the fix. What should happen?'),
        ('Why both', 'Why do we need both?', 'What does each check prove? Answer in your own words.')),
     'Use only the supplied local scenario. Never probe real metadata endpoints or other systems.',
     'TEACHER NOTE. The slide poses the questions only; the model answers are in this note and not on the slide, so Local 02 Part 1 Q6 stays an assessed answer. These are the two checks Q6 asks for. In the local lab the fixed app (:8117) returns 403 {"error":"blocked","reason":"internal/metadata URL not allowed"} for both the localhost form and the 169.254.169.254 form, and 200 \'fetched\' for an ordinary URL; it also rejects a redirect that points at an internal target. The fixed app blocks internal targets (loopback, link-local, the metadata path, redirects); it is not a strict allowlist, so say \'block internal destinations\', and mention that an allowlist of intended hosts is the stronger design. For Q4 (\'name two ways to stop the attack\'), accept two preventive controls such as: validate the destination and any redirects before fetching (block loopback, link-local and metadata addresses, or use an allowlist); require IMDSv2 or otherwise limit access to the metadata service. Least privilege (giving the role only the permissions it needs) limits the damage if credentials are stolen but does not stop the attack, so credit it under Q5, not as a preventive control for Q4.'),
)


# Plain-language add-on for Week 05 (original wording; no AWS Academy material).
# Slide 3 poses the Local 03 Q5 questions only; the answers stay in the teacher notes.
WEEK5_PLAIN = (
    ("PLAIN WORDS", "What does Lambda do?", (
        ("Think of", "Lambda = a helper on call", "A small piece of code that runs only when something happens. No server to keep on."),
        ("What wakes it", "An event", "A file is uploaded, a timer ticks, or a message arrives. Then your code runs."),
        ("The cost idea", "Pay while it runs", "You pay for the time the code runs, not for the time it waits.")),
     "Lambda is code that waits for an event, runs, then stops.",
     "TEACHER NOTE (plain-language add-on for Week 05, links to Local 03 Part 1 Q5). Helper-on-call analogy: nobody pays the "
     "helper to sit and wait; they are called when there is a job. Keep it to the idea of an event-driven function. The AWS "
     "Academy Lambda activity is the hands-on part; this slide only supplies the plain words. Own wording; no AWS Academy "
     "slides copied."),
    ("PLAIN WORDS", "What is SNS?", (
        ("Think of", "Topic = a notice board", "Lambda posts a message to the topic. The topic does not send email by itself."),
        ("Who gets it", "Subscription = a name on the list", "An email address that asked for the notices. It must confirm by clicking a link first."),
        ("The action", "Publish = pinning a notice", "A successful Publish means SNS accepted the message. It does not prove the email arrived.")),
     "Topic, subscription and publish are three different things.",
     "TEACHER NOTE. In the Local 03 scenario a Lambda function publishes a message to an SNS Standard topic that has an email "
     "subscription. Roles: Lambda publishes; the topic receives and fans the message out; each confirmed subscription gets a "
     "copy. Why confirm: it shows the owner of the address wants the emails, so nobody can sign someone else up and spam "
     "them. A successful Publish response only shows SNS accepted the message; delivery to a mailbox can still fail or "
     "land in spam."),
    ("CHECK YOURSELF", "Three questions for Local 03 Q5", (
        ("Question 1", "Who does what?", "Say in one line what Lambda, the topic and the subscription each do."),
        ("Question 2", "Why confirm?", "Why must an email subscription be confirmed? Does a successful Publish prove the email arrived?"),
        ("Question 3", "A late subscriber?", "Someone subscribes after a message was sent. Will they get it? Say why.")),
     "Answer in your own words. The answers are not on this slide.",
     "TEACHER NOTE. The slide poses the questions only; the model answers are below and are not on the slide, so Q5 stays an assessed answer. These are the parts Local 03 Part 1 Q5 asks for (model answers: Lambda publishes, the topic receives, each confirmed subscription gets a copy; confirmation shows the address owner wants the emails; a successful Publish proves only that SNS accepted the message; a Standard topic does not replay old messages): the roles of Lambda, the topic and the subscription; why "
     "the email subscription must be confirmed; whether a successful Publish proves the email reached the recipient (no); and "
     "why a subscriber added later should not expect past messages (a Standard topic does not replay). Accept answers in Thai "
     "or English; mark the reasoning, not the length. Keep AWS names in English."),
)


def rect(slide, x, y, w, h, fill=WHITE, line=BORDER, line_pt=0.8):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    if line_pt:
        shape.line.color.rgb = line
        shape.line.width = Pt(line_pt)
    else:
        shape.line.fill.background()
    return shape


def text(slide, value, x, y, w, h, size=22, color=NAVY, bold=False, align=PP_ALIGN.LEFT):
    shape = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = shape.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0)
    tf.margin_top = tf.margin_bottom = Inches(0)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = value
    run.font.name = "Arial"
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    return shape


def base(prs, week, section, title, page):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = BG
    rect(slide, .58, .55, .08, .08, BLUE, BLUE, 0)
    text(slide, f"CLOUD / WEEK {week['n']:02d} · {section}", .78, .45, 9.2, .35, 15, DARK_BLUE, True)
    text(slide, title, .58, 1.02, 11.1, .7, 37, NAVY, True)
    slide.shapes.add_picture(str(LOGO), Inches(10.97), Inches(.35), width=Inches(1.75))
    day = date(2026, 11, 3) + timedelta(weeks=week["n"] - 1)
    text(slide, f"KOSEN-KMITL | 02005097 Cloud Infrastructure and Security · {day.strftime('%d %b %Y')}", .58, 7.12, 11.5, .2, 10.5, GREY)
    text(slide, str(page), 12.7, 7.12, .2, .2, 10.5, GREY, align=PP_ALIGN.RIGHT)
    return slide


def card(slide, x, width, kicker, headline, body, accent=BLUE, y=2.15, h=3.25):
    rect(slide, x, y, width, h)
    rect(slide, x, y, width, .09, accent, accent, 0)
    text(slide, kicker.upper(), x + .23, y + .25, width - .46, .28, 14, accent, True)
    text(slide, headline, x + .23, y + .72, width - .46, .77, 22, NAVY, True)
    text(slide, body, x + .23, y + 1.68, width - .46, h - 1.9, 18, GREY)


def band(slide, message):
    rect(slide, .58, 6.3, 12.16, .52, NAVY, NAVY, 0)
    text(slide, message, .83, 6.36, 11.65, .4, 16, WHITE, True)


def notes(slide, week):
    try:
        slide.notes_slide.notes_text_frame.text = (
            "Original course bridge. Use the AWS Academy module and lab named on slide 1 as the "
            "primary teaching source. This bridge links that content to the course's local worksheet. "
            f"Week {week['n']:02d} Classroom Material and the Cloud course plan define the weekly sequence. "
            "For technical details, follow the current AWS Academy LMS instructions and the local worksheet."
        )
    except AttributeError:
        pass


def build_week(week):
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    number = week["n"]

    slide = base(prs, week, "COURSE BRIDGE", week["title"], 1)
    text(slide, "AWS Academy is the main lesson. This short deck connects it to our class work.", .58, 1.7, 11.9, .35, 19, GREY)
    card(slide, .58, 3.78, "Primary", "AWS Academy", week["aws"])
    card(slide, 4.77, 3.78, "In class", "Practice", week["practice"], ORANGE)
    card(slide, 8.96, 3.78, "Course work", "Local task", week["local"])
    band(slide, week["due"] + (" · Use only your assigned Part" if not week["due"].startswith("No Local") else ""))
    notes(slide, week)

    slide = base(prs, week, "CONCEPT LINK", "One path through the topic", 2)
    for i, (headline, body) in enumerate(week["concept"]):
        card(slide, .58 + i * 4.19, 3.78, f"Step {i+1}", headline, body, ORANGE if i == 1 else BLUE)
    band(slide, week["check"])
    notes(slide, week)

    slide = base(prs, week, "CLASS FLOW", "What to do this week", 3)
    for i, (kicker, headline, body) in enumerate((("Before class", "Prepare", week["before"]),
                                                  ("In class", "Work", week["during"]),
                                                  ("After class", "Record", week["after"]))):
        card(slide, .58 + i * 4.19, 3.78, kicker, headline, body, ORANGE if i == 1 else BLUE)
    band(slide, "AWS work stays in AWS Academy · Local work stays in Classroom")
    notes(slide, week)

    if extra := week.get("extra"):
        title, items, message = extra
        slide = base(prs, week, "OUTSIDE CLASS / CLOSURE", title, 4)
        for i, (kicker, headline, body) in enumerate(items):
            card(slide, .58 + i * 4.19, 3.78, kicker, headline, body, ORANGE if i == 1 else BLUE)
        band(slide, message)
        notes(slide, week)

    if supplement := SUPPLEMENTS.get(number):
        title, items, message = supplement
        slide = base(prs, week, "LOCAL WORKSHEET LINK", title, len(prs.slides) + 1)
        for i, (kicker, headline, body) in enumerate(items):
            card(slide, .58 + i * 4.19, 3.78, kicker, headline, body, ORANGE if i == 1 else BLUE)
        band(slide, message)
        notes(slide, week)

    if number == 3:
        for section, title, cards, message, note in WEEK3_PLAIN:
            slide = base(prs, week, section, title, len(prs.slides) + 1)
            for i, (kicker, headline, body) in enumerate(cards):
                card(slide, .58 + i * 4.19, 3.78, kicker, headline, body, ORANGE if i == 1 else BLUE)
            band(slide, message)
            slide.notes_slide.notes_text_frame.text = note

    if number == 4:
        for section, title, cards, message, note in WEEK4_PLAIN:
            slide = base(prs, week, section, title, len(prs.slides) + 1)
            for i, (kicker, headline, body) in enumerate(cards):
                card(slide, .58 + i * 4.19, 3.78, kicker, headline, body, ORANGE if i == 1 else BLUE)
            band(slide, message)
            slide.notes_slide.notes_text_frame.text = note

    if number == 5:
        for section, title, cards, message, note in WEEK5_PLAIN:
            slide = base(prs, week, section, title, len(prs.slides) + 1)
            for i, (kicker, headline, body) in enumerate(cards):
                card(slide, .58 + i * 4.19, 3.78, kicker, headline, body, ORANGE if i == 1 else BLUE)
            band(slide, message)
            slide.notes_slide.notes_text_frame.text = note

    if number == 17:
        slide = base(prs, week, "LOCAL 09 · EVENT PATHS", "Two ways to turn an event into an alert", len(prs.slides) + 1)
        card(slide, .58, 3.78, "Event route", "CloudTrail → EventBridge", "A rule matches a relevant event and sends it to a target such as SNS.")
        card(slide, 4.77, 3.78, "Metric route", "Logs → metric → alarm", "A CloudWatch Logs filter counts matching events; an alarm evaluates the metric and can notify.", ORANGE)
        card(slide, 8.96, 3.78, "Compare", "Separate paths", "CloudTrail records the action. EventBridge and a metric alarm need not be one serial pipeline.")
        band(slide, "Use the AWS lab for the real service setup; Local 09 studies the counting choice.")
        notes(slide, week)

        slide = base(prs, week, "LOCAL 09 · COUNTING", "The same events, different counts", len(prs.slides) + 1)
        card(slide, .58, 3.78, "Spray", "20 names · one IP", "One failure per name: pair and username counters stay at 1; a source-IP counter reaches 20.")
        card(slide, 4.77, 3.78, "Distributed guesses", "One name · 20 IPs", "One failure per IP: pair and source-IP counters stay at 1; a username counter reaches 20.", ORANGE)
        card(slide, 8.96, 3.78, "Scope", "A simulation", "The local app resets a streak on success. A real metric filter counts matching events in an alarm window.")
        band(slide, "A running detector can miss an attack when its grouping key does not match the threat.")
        notes(slide, week)

    if number == 18:
        slide = base(prs, week, "LOCAL 10 · TRACE", "Which rules survive the condition?", len(prs.slides) + 1)
        card(slide, .58, 3.78, "Input", "80 · 443 · 22", "The intended allowlist is {80, 443}; port 22 is open to everyone in the local starting state.")
        card(slide, 4.77, 3.78, "Inverted test", "Keep port NOT in list", "The vulnerable function keeps 22 and removes 80/443. It can report success while leaving danger.", ORANGE)
        card(slide, 8.96, 3.78, "Correct test", "Keep port IN list", "The fixed function keeps 80/443 and removes 22. Compare actual rules after the run.")
        band(slide, "Trace the worksheet's supplied code by hand before answering Part 2b.")
        notes(slide, week)

        slide = base(prs, week, "LOCAL 10 · VERIFY", "A successful run is only one signal", len(prs.slides) + 1)
        card(slide, .58, 3.78, "Detection", "Config evaluation", "A NON_COMPLIANT result reports a state; a separately configured path must invoke remediation.")
        card(slide, 4.77, 3.78, "Safety", "Port 22 removed?", "Inspect the final security-group rules; a 200 response or Lambda log alone cannot prove this.", ORANGE)
        card(slide, 8.96, 3.78, "Service", "80/443 still work?", "Check the intended access too. Removing safe rules while retaining SSH is a failed security outcome.")
        band(slide, "Local Flask targets model rule logic; AWS Config inventory and timing are not simulated.")
        notes(slide, week)

    OUT.mkdir(exist_ok=True)
    target = OUT / f"Week{number:02d}_Cloud_Course_Bridge.pptx"
    prs.save(target)
    return target


def main():
    if not LOGO.exists():
        raise SystemExit(f"Missing template logo: {LOGO}")
    import sys
    requested = {int(arg) for arg in sys.argv[1:]}
    selected = [week for week in WEEKS if not requested or week["n"] in requested]
    if requested and len(selected) != len(requested):
        raise SystemExit(f"Unknown week number: {sorted(requested - {week['n'] for week in selected})}")
    paths = []
    for week in selected:
        path = build_week(week)
        paths.append(path)
        print(path)
    subprocess.run([
        "soffice", "-env:UserInstallation=file:///tmp/lo-cloud-weekly-bridges", "--headless",
        "--convert-to", "pdf", "--outdir", str(OUT),
        *[str(p) for p in paths],
    ], check=True)


if __name__ == "__main__":
    main()
