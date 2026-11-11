# Cloud workshop teaching supplements

These are original, editable teaching slides for the two weeks whose main in-class activity is a local workshop. The assigned AWS Academy slide deck and lab remain the primary source. No licensed AWS Academy slide or lab instruction is copied here.

| Week | Classroom topic | Editable deck | PDF | Worksheet gap covered |
|---|---|---|---|---|
| 14 | NACL rule-order workshop after Cloud Security Foundations Module 4 | [PPTX](output/Week14_Cloud_Workshop_Supplement_v3.pptx) | [PDF](output/Week14_Cloud_Workshop_Supplement_v3.pdf) | Security group versus NACL, stateful return traffic, first-match rule order, NAT route, and evidence for Local 07 |
| 16 | SSE-KMS workshop after Cloud Security Foundations Module 5 and Lab 5.1 | [PPTX](output/Week16_Cloud_Workshop_Supplement_v4.pptx) | [PDF](output/Week16_Cloud_Workshop_Supplement_v4.pdf) | Upload/read envelope flow, data-key copies, disabled/pending-deletion/deleted key states, and evidence for Local 08 |

The Week 14 example uses rule numbers and CIDRs different from the graded worksheet's planted rule set. Its fixed local app changes rule #90's CIDR while preserving rule order. The Week 16 slides teach the mechanism without displaying any of the worksheet's planted-error passages. For Local 07 and Local 08, C5R1 completes Part 2 and C5R2 completes Part 1. Students submit only their assigned Part.

The source is [`build.mjs`](build.mjs). It uses the PBL4 Week 03 visual reference: 16:9 pale background, navy titles, blue/orange accents, KOSEN KMITL logo, rectangular cards, and a dark bottom band. The two final PPTX files passed package, layout, font and first-party import validation; their PDF renders were visually reviewed slide by slide. The source cites the local lesson plans and worksheets plus official AWS documentation in speaker notes. To regenerate, use the bundled Codex presentation runtime and change the revision suffix before finalization, which will not overwrite an existing final output.
