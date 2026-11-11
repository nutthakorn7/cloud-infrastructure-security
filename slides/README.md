# Cloud Infrastructure and Security slides

Each of the 18 teaching weeks has an original **course bridge** in [`weekly-bridges/output/`](weekly-bridges/output/). Weeks 01–16 have three slides; Weeks 17–18 have an additional outside-class or closure slide. Use the assigned AWS Academy module slides and lab as the main lesson. The bridge supplies the course-specific concept link, local worksheet handoff and class flow. It is not a replacement for the AWS deck.

The AWS Academy PPTX/PDF files remain in the authorized Classroom/AWS Academy locations. Their licensing notice prohibits copying them into this repository. No AWS Academy slide or lab instruction is reproduced in these bridges.

| Week | Editable bridge | PDF | Main AWS / local content |
|---|---|---|---|
| 01 | [PPTX](weekly-bridges/output/Week01_Cloud_Course_Bridge.pptx) | [PDF](weekly-bridges/output/Week01_Cloud_Course_Bridge.pdf) | Cloud Foundations Modules 1–3; Local 01 starts |
| 02 | [PPTX](weekly-bridges/output/Week02_Cloud_Course_Bridge.pptx) | [PDF](weekly-bridges/output/Week02_Cloud_Course_Bridge.pdf) | Cloud Foundations Module 4; Local 01 |
| 03 | [PPTX](weekly-bridges/output/Week03_Cloud_Course_Bridge.pptx) | [PDF](weekly-bridges/output/Week03_Cloud_Course_Bridge.pdf) | Cloud Foundations Module 5; VPC lab |
| 04 | [PPTX](weekly-bridges/output/Week04_Cloud_Course_Bridge.pptx) | [PDF](weekly-bridges/output/Week04_Cloud_Course_Bridge.pdf) | Cloud Foundations Module 6 EC2 and Lab 3; Local 02 |
| 05 | [PPTX](weekly-bridges/output/Week05_Cloud_Course_Bridge.pptx) | [PDF](weekly-bridges/output/Week05_Cloud_Course_Bridge.pdf) | Cloud Foundations Module 6 Lambda/Beanstalk; Local 03 starts |
| 06 | [PPTX](weekly-bridges/output/Week06_Cloud_Course_Bridge.pptx) | [PDF](weekly-bridges/output/Week06_Cloud_Course_Bridge.pdf) | Cloud Foundations Module 7 and EBS lab; Local 03 |
| 07 | [PPTX](weekly-bridges/output/Week07_Cloud_Course_Bridge.pptx) | [PDF](weekly-bridges/output/Week07_Cloud_Course_Bridge.pdf) | Cloud Foundations Module 8 and RDS lab; [S3 supplement](week07-08-s3-data-protection/README.md) slides 1–3 |
| 08 | [PPTX](weekly-bridges/output/Week08_Cloud_Course_Bridge.pptx) | [PDF](weekly-bridges/output/Week08_Cloud_Course_Bridge.pdf) | Cloud Foundations Module 9; [S3 supplement](week07-08-s3-data-protection/README.md) slide 4; Local 04 |
| 09 | [PPTX](weekly-bridges/output/Week09_Cloud_Course_Bridge.pptx) | [PDF](weekly-bridges/output/Week09_Cloud_Course_Bridge.pdf) | Cloud Foundations Module 10 and Lab 6; Local 05 starts |
| 10 | [PPTX](weekly-bridges/output/Week10_Cloud_Course_Bridge.pptx) | [PDF](weekly-bridges/output/Week10_Cloud_Course_Bridge.pdf) | Foundations completion and Course Assessment; Local 05 |
| 11 | [PPTX](weekly-bridges/output/Week11_Cloud_Course_Bridge.pptx) | [PDF](weekly-bridges/output/Week11_Cloud_Course_Bridge.pdf) | Cloud Security Foundations Modules 1–2; Local 06 starts |
| 12 | [PPTX](weekly-bridges/output/Week12_Cloud_Course_Bridge.pptx) | [PDF](weekly-bridges/output/Week12_Cloud_Course_Bridge.pdf) | Cloud Security Foundations Module 3 and Lab 3.1; Local 06 |
| 13 | [PPTX](weekly-bridges/output/Week13_Cloud_Course_Bridge.pptx) | [PDF](weekly-bridges/output/Week13_Cloud_Course_Bridge.pdf) | Cloud Security Foundations Module 4 and Lab 4.1; Local 07 starts |
| 14 | [PPTX](weekly-bridges/output/Week14_Cloud_Course_Bridge.pptx) | [PDF](weekly-bridges/output/Week14_Cloud_Course_Bridge.pdf) | Local NACL workshop; Local 07 |
| 15 | [PPTX](weekly-bridges/output/Week15_Cloud_Course_Bridge.pptx) | [PDF](weekly-bridges/output/Week15_Cloud_Course_Bridge.pdf) | Cloud Security Foundations Module 5 and Lab 5.1; Local 08 starts |
| 16 | [PPTX](weekly-bridges/output/Week16_Cloud_Course_Bridge.pptx) | [PDF](weekly-bridges/output/Week16_Cloud_Course_Bridge.pdf) | Local KMS workshop; Local 08 |
| 17 | [PPTX](weekly-bridges/output/Week17_Cloud_Course_Bridge.pptx) | [PDF](weekly-bridges/output/Week17_Cloud_Course_Bridge.pdf) | Cloud Security Foundations Module 6 and Lab 6.1; Local 09 |
| 18 | [PPTX](weekly-bridges/output/Week18_Cloud_Course_Bridge.pptx) | [PDF](weekly-bridges/output/Week18_Cloud_Course_Bridge.pdf) | Cloud Security Foundations Module 7 and Lab 7.1; Local 10 |

The generator is [`weekly-bridges/build.py`](weekly-bridges/build.py). It uses the current PBL4 Week 03 deck as the visual reference: 16:9, pale background, navy headings, blue/orange accents, KOSEN KMITL logo, rectangular cards and dark bottom band. The related [Week 07–08 S3 supplement](week07-08-s3-data-protection/README.md) supplies the additional technical teaching needed for Local 04.

Technical cross-checks: the current Cloud worksheets and lesson plans, the assigned AWS Academy LMS lab pages, and the official AWS documentation for [IAM evaluation](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html), [S3 Batch Replication](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-batch-replication-batch.html), [instance metadata](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html) and [network ACL rules](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-network-acls.html). Check the current LMS instructions before teaching a lab because AWS can revise them.
