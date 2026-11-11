# Week 07–08: S3 Data Protection supplement

This four-slide instructor supplement closes a demonstrated gap for Local 04. The assigned AWS Academy Cloud Foundations modules and lab remain the primary lesson. The attached Module 9 deck introduces storage but does not teach S3 Versioning, lifecycle actions for noncurrent versions, or replication coverage in enough detail to answer Local 04. Use slides 1–3 with Week 07 and slide 4 with Week 08, after the AWS material.

- [Editable PowerPoint](output/Week07-08_S3_Data_Protection_Supplement.pptx)
- [PDF handout](output/Week07-08_S3_Data_Protection_Supplement.pdf)

The layout and branding follow the current PBL course deck `../KOSEN69 - PBL/slides/pbl4/week03-sprint1/PBL4_W03_Sprint1.pptx`. The explanations and diagrams are original. Source links are in the PowerPoint speaker notes:

`build.mjs` and `kosen-kmitl-logo.png` are the editable generation source. The PowerPoint itself also remains editable. The build script uses the course's Codex presentation runtime; `.build/` contains temporary render checks and is excluded from version control.

- [S3 Versioning](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html)
- [S3 Lifecycle configuration elements](https://docs.aws.amazon.com/AmazonS3/latest/userguide/intro-lifecycle-rules.html)
- [Batch Replication for existing objects](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-batch-replication-batch.html)

Do not treat replication as a verified backup until the destination versions and restore path have been checked.
