import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { Presentation, PresentationFile } from '@oai/artifact-tool';

const here = path.dirname(fileURLToPath(import.meta.url));
const build = path.join(here, '.build');
const deck = Presentation.create({ slideSize: { width: 1280, height: 720 } });
const C = { bg: '#F5F7FA', navy: '#101828', blue: '#007AC2', darkBlue: '#005A91',
  orange: '#E35205', grey: '#5E6673', border: '#D5DCE4', white: '#FFFFFF' };
const logo = await fs.readFile(path.join(here, 'kosen-kmitl-logo.png'));

function box(slide, x, y, w, h, fill = C.white, stroke = C.border, width = 1) {
  return slide.shapes.add({ geometry: 'rect', position: { left:x, top:y, width:w, height:h },
    fill, line: { style:'solid', fill:stroke, width } });
}
function txt(slide, s, x, y, w, h, size=24, color=C.navy, bold=false) {
  const q = slide.shapes.add({ geometry:'textbox', position:{left:x,top:y,width:w,height:h},
    fill:'none', line:{style:'solid',fill:'none',width:0} });
  q.text = s; q.text.style = { typeface:'Arial', fontSize:size, color, bold }; return q;
}
function base(section, title, number) {
  const slide = deck.slides.add(); slide.background.fill = C.bg;
  box(slide,55,54,8,8,C.blue,C.blue,0);
  txt(slide,`CLOUD / ${section}`,73,46,780,28,18,C.darkBlue,true);
  txt(slide,title,55,103,1120,78,47,C.navy,true);
  slide.images.add({blob:logo,contentType:'image/png',alt:'KOSEN KMITL logo',fit:'contain',
    position:{left:1056,top:35,width:169,height:75}});
  txt(slide,'KOSEN-KMITL | Cloud Infrastructure and Security · Local 04',55,671,1090,23,17,C.grey);
  txt(slide,String(number),1190,671,35,23,17,C.grey);
  return slide;
}
function band(slide, s) { box(slide,55,594,1170,55,C.navy,C.navy,0); txt(slide,s,77,608,1120,31,21,C.white,true); }
function card(slide,x,w,kicker,headline,body,accent=C.blue){
  box(slide,x,231,w,291,C.white,C.border,1);
  box(slide,x,231,w,10,accent,accent,0);
  txt(slide,kicker,x+23,263,w-46,28,17,accent,true);
  txt(slide,headline,x+23,305,w-46,55,26,C.navy,true);
  txt(slide,body,x+23,381,w-46,113,21,C.grey);
}

{
 const s=base('WEEKS 07–08 · SUPPLEMENT','S3 data protection',1);
 txt(s,'AWS Academy modules remain the main lesson. Use this short guide for Local 04.',55,179,1120,35,25,C.grey);
 card(s,55,365,'WEEK 07','Versioning','Keep prior object versions after an overwrite or ordinary delete.');
 card(s,457,365,'WEEK 07','Lifecycle','Current and noncurrent versions need different transition actions.',C.orange);
 card(s,860,365,'WEEK 08','Replication','Live replication covers new or updated objects; existing data needs a separate job.');
 band(s,'Local 04: use your assigned Part only · No extra AWS lab');
 s.speakerNotes.text='Original instructor supplement. AWS Academy Cloud Foundations Modules 8 and 9 remain the primary weekly content. Source: https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html ; https://docs.aws.amazon.com/AmazonS3/latest/userguide/intro-lifecycle-rules.html ; https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-batch-replication-batch.html';
}
{
 const s=base('WEEK 07 · OBJECT HISTORY','Versioning keeps prior versions',2);
 const xs=[55,457,860],labels=['T0 · ORIGINAL','T1 · OVERWRITE','T2 · DELETE'];
 const heads=['report.pdf · v1','report.pdf · v2','Delete marker becomes current'];
 const bodies=['The first upload is the current version.','The new upload becomes current. v1 remains noncurrent.','An ordinary delete hides the object. Earlier versions can still be restored.'];
 xs.forEach((x,i)=>card(s,x,365,labels[i],heads[i],bodies[i],i===2?C.orange:C.blue));
 band(s,'After enabling versioning, you can suspend it; you cannot return the bucket to unversioned.');
 s.speakerNotes.text='Source: AWS S3 User Guide, Retaining multiple versions of objects with S3 Versioning: https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html . Each stored version is the entire object, not a small diff. Ordinary DELETE without a version ID creates a delete marker; permanently deleting a specific version is different. This slide addresses Local 04 Part 1 Q1/Q4 and AIR-Sec variants 2/3.';
}
{
 const s=base('WEEK 07 · RETENTION','Lifecycle needs two actions',3);
 box(s,55,225,565,298,C.white,C.border,1);box(s,660,225,565,298,C.white,C.border,1);
 box(s,55,225,565,10,C.blue,C.blue,0);box(s,660,225,565,10,C.orange,C.orange,0);
 txt(s,'CURRENT VERSION',83,257,500,28,19,C.blue,true);
 txt(s,'Transition',83,306,500,45,34,C.navy,true);
 txt(s,'Example: move the current object to a colder storage class after its age reaches 30 days.',83,378,505,113,23,C.grey);
 txt(s,'NONCURRENT VERSION',688,257,500,28,19,C.orange,true);
 txt(s,'NoncurrentVersionTransition',688,306,500,48,30,C.navy,true);
 txt(s,'Separate action: count from when a version became noncurrent. A current-version rule does not cover it.',688,378,505,113,23,C.grey);
 band(s,'A lifecycle rule never restores a version that was permanently deleted.');
 s.speakerNotes.text='Source: AWS S3 User Guide, Lifecycle configuration elements: https://docs.aws.amazon.com/AmazonS3/latest/userguide/intro-lifecycle-rules.html . Transition applies to current versions in a versioned bucket; NoncurrentVersionTransition is a distinct action with its own age calculation. This slide addresses Local 04 Part 1 Q2 and AIR-Sec variant 1. Avoid implying an exact execution time: lifecycle actions are asynchronous.';
}
{
 const s=base('WEEK 08 · RECOVERY','Replication does not backfill old data',4);
 box(s,55,225,530,280,C.white,C.border,1);box(s,660,225,565,280,C.white,C.border,1);
 box(s,55,225,530,10,C.orange,C.orange,0);box(s,660,225,565,10,C.blue,C.blue,0);
 txt(s,'BEFORE THE RULE',83,254,450,28,19,C.orange,true);
 txt(s,'Existing objects',83,301,450,48,34,C.navy,true);
 txt(s,'Live replication does not automatically copy objects already in the source bucket.',83,373,460,103,23,C.grey);
 txt(s,'AFTER THE RULE',688,254,470,28,19,C.blue,true);
 txt(s,'New and updated objects',688,301,480,48,34,C.navy,true);
 txt(s,'Live replication copies eligible new writes. Use S3 Batch Replication for existing objects.',688,373,493,103,23,C.grey);
 txt(s,'Recovery check: verify which versions exist at the destination, then test the restore path.',55,533,1160,41,23,C.darkBlue,true);
 band(s,'Local 04 Q3: a replication rule alone is not a full backup of two years of old objects.');
 s.speakerNotes.text='Source: AWS S3 User Guide, Create a Batch Replication job for new replication rules or destinations: https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-batch-replication-new-config.html ; Replicating existing objects with Batch Replication: https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-batch-replication-batch.html . Live replication applies to eligible new and updated objects after configuration; Batch Replication can copy existing objects on demand. This slide addresses Local 04 Part 1 Q3 and Part 2b. Replication has configuration and eligibility details; verify actual coverage before calling it a recovery copy.';
}

await fs.mkdir(build,{recursive:true});
for (let i=0;i<deck.slides.items.length;i++) {
  const blob=await deck.export({slide:deck.slides.items[i],format:'png',scale:1});
  await fs.writeFile(path.join(build,`slide-${i+1}.png`),new Uint8Array(await blob.arrayBuffer()));
}
const out=path.join(build,'candidate.pptx');
await (await PresentationFile.exportPptx(deck)).save(out);
console.log(out);
