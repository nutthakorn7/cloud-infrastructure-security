import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { Presentation, PresentationFile } from '@oai/artifact-tool';

// Original course-specific teaching slides. AWS Academy remains the primary
// slide deck; its licensed slides are not reproduced here.
const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../..');
const out = path.join(here, 'output');
const staging = path.join(here, '.build');
const logo = path.join(root, 'slides/week07-08-s3-data-protection/kosen-kmitl-logo.png');
const logoBytes = await fs.readFile(logo);
const skill = process.env.CLOUD_PRESENTATIONS_SKILL_DIR;
const python = process.env.RUNTIME_PYTHON;
if (!skill || !python || !process.env.RUNTIME_NODE_MODULES) {
  throw new Error('Set CLOUD_PRESENTATIONS_SKILL_DIR, RUNTIME_PYTHON and RUNTIME_NODE_MODULES from the bundled presentation runtime.');
}
const C = { bg:'#F5F7FA', navy:'#101828', blue:'#007AC2', dark:'#005A91', orange:'#E35205', grey:'#5E6673', border:'#D5DCE4', white:'#FFFFFF', pale:'#EAF4FA' };

const decks = [
  {
    n:14, title:'NACL first-match reasoning', subtitle:'Local 07 · 45–60 minute add-on after the AWS VPC lesson',
    source:'labs/lesson10-vpc-networking/worksheet.md; docs/lesson-plans/lesson10-vpc-networking.md; https://docs.aws.amazon.com/vpc/latest/userguide/vpc-network-acls.html',
    slides:[
      {k:'START',t:'The question: which rule decides?',kind:'cards',cards:[
        ['Recall','Security group','Instance-level, stateful, allow rules only.'],
        ['Focus','Network ACL','Subnet-level, stateless, ordered allow and deny rules.'],
        ['Evidence','Explain the path','Name the first matching rule for both an intended and an unwanted packet.']],
       band:'AWS Module 4 supplies the VPC baseline · This add-on supplies Local 07 reasoning.'},
      {k:'COMPARE',t:'One request, two filters',kind:'flow',steps:[
        ['Client','203.0.113.55 → port 443'],['Subnet NACL','Check inbound rule by number'],['Security group','Check allowed inbound flow'],['Server','Return traffic takes the reverse path']],
       callouts:[['Security group','Stateful: an allowed request permits its response without a separate outbound rule.'],['NACL','Stateless: check the return packet against outbound rules too.']],
       band:'A successful inbound rule does not prove the stateless return path works.'},
      {k:'WORKED EXAMPLE',t:'Trace the first match',kind:'rules',rules:[
        ['#80','ALLOW','10.0.1.0/24','5432'],['#100','DENY','0.0.0.0/0','5432']],
       probes:[['10.0.1.25','Matches #80 → allow'],['203.0.113.55','Skips #80; matches #100 → deny']],
       band:'Read from the lowest rule number. Stop after the first match.'},
      {k:'FAILURE MODE',t:'A visible deny may never run',kind:'rules',rules:[
        ['#70','ALLOW','0.0.0.0/0','5432'],['#90','DENY','0.0.0.0/0','5432']],
       probes:[['External source','Matches broad #70 → allow'],['Internal source','Also matches #70 → allow']],
       band:'Fix both scope and order: narrow the allow to the intended CIDR, then put it before the catch-all deny.'},
      {k:'NETWORK PATH',t:'What the NAT gateway changes',kind:'flow',steps:[
        ['Private instance','Initiates an update request'],['Private route','Default route → NAT gateway'],['Public subnet','NAT gateway → internet gateway'],['Internet','Response returns to the initiated flow']],
       callouts:[['Allowed direction','The private instance can initiate outbound traffic when routes and rules permit.'],['Boundary','An unsolicited inbound internet connection is not forwarded to that private instance by NAT.']],
       band:'The NAT gateway sits in a public subnet; its users stay in a private subnet.'},
      {k:'LOCAL 07',t:'Use one method for every answer',kind:'cards',cards:[
        ['1 · Identify','Packet and boundary','State source IP, destination port, direction and the control being checked.'],
        ['2 · Walk','Rule order','Read each NACL rule in ascending order; stop at the first match.'],
        ['3 · Verify','Before and after','Compare vulnerable and fixed results, including an intended path that still works.']],
       band:'Section A: Part 1 · Section B: Part 2 · Submit only the assigned Part in Classroom.'},
    ]
  },
  {
    n:16, title:'SSE-KMS envelope encryption', subtitle:'Local 08 · 45–60 minute conceptual add-on after AWS Lab 5.1',
    source:'labs/lesson11-kms-envelope-encryption/worksheet.md; docs/lesson-plans/lesson11-kms-envelope-encryption.md; https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingKMSEncryption.html; https://docs.aws.amazon.com/kms/latest/developerguide/deleting-keys.html',
    slides:[
      {k:'START',t:'Trace the key, not just the object',kind:'cards',cards:[
        ['Baseline','AWS Lab 5.1','Observe S3 encryption with KMS and relevant KMS events.'],
        ['Today','Envelope flow','Separate the KMS key, plaintext data key and encrypted data key.'],
        ['Question','Later read','What must still be available to decrypt an old object?']],
       band:'Scenario: per-object SSE-KMS without S3 Bucket Keys.'},
      {k:'UPLOAD',t:'Two copies of a data key',kind:'flow',steps:[
        ['S3','Requests GenerateDataKey'],['KMS','Returns plaintext + encrypted copies'],['S3','Encrypts object with plaintext copy'],['Store','Ciphertext + encrypted data key']],
       callouts:[['Use now','The plaintext data key encrypts this object.'],['Keep later','S3 stores the encrypted copy and discards the plaintext copy.']],
       band:'The KMS key protects the data key; it does not directly encrypt the whole object.'},
      {k:'READ',t:'Why an old object needs KMS again',kind:'flow',steps:[
        ['Stored object','Ciphertext + encrypted data key'],['S3','Sends encrypted data key to KMS'],['KMS','Decrypts it if key state and permissions allow'],['S3','Uses plaintext data key for this read']],
       callouts:[['No plaintext cache','In this lesson scenario, S3 does not keep a plaintext data key between requests.'],['Access condition','Stored ciphertext alone does not grant a usable read.']],
       band:'Check the request path and key state when a read fails.'},
      {k:'KEY STATES',t:'Reversible and irreversible outcomes',kind:'cards',cards:[
        ['Disabled','Temporarily unavailable','Existing ciphertext remains. Reads needing KMS fail until the key is re-enabled.'],
        ['Pending deletion','Cancel before deadline','Cancellation stops deletion but leaves the key disabled; enable it again for use.'],
        ['Deleted','Cannot recover key','Completed deletion is irreversible; ciphertext that depends on that key is unusable.']],
       band:'A key state change affects access; it does not erase the stored encrypted object.'},
      {k:'WHY ENVELOPE?',t:'One key for control, data keys for data',kind:'cards',cards:[
        ['KMS key','Protects keys','A managed control point for authorization, audit and key state.'],
        ['Data key','Encrypts content','A fresh per-operation data key handles object data efficiently.'],
        ['Stored copy','Supports future reads','Only the encrypted data key is retained with the object.']],
       band:'Do not confuse one KMS key with one reusable plaintext data key for every object.'},
      {k:'LOCAL 08',t:'Audit a claim by tracing the flow',kind:'cards',cards:[
        ['1 · Name','Which key?','Identify whether the claim concerns the KMS key or a data key.'],
        ['2 · Trace','Upload or read?','Walk through the actual request and note what is stored or discarded.'],
        ['3 · Correct','One precise sentence','Explain the key state and replace the false claim in your own words.']],
       band:'Section A: Part 1 · Section B: Part 2 · No flag is required for this conceptual task.'},
    ]
  }
];

function shape(slide, geometry, x,y,w,h, fill='none', stroke='none', lineWidth=0) {
  return slide.shapes.add({geometry,position:{left:x,top:y,width:w,height:h},fill,line:{style:'solid',fill:stroke,width:lineWidth}});
}
function txt(slide, value,x,y,w,h,size=24,color=C.navy,bold=false,align='left') {
  const s=shape(slide,'textbox',x,y,w,h);
  s.text=value;
  s.text.style={typeface:'Arial',fontSize:size,color,bold,alignment:align,verticalAlignment:'middle',wrap:'square',autoFit:'shrinkText',insets:0};
  return s;
}
function rect(slide,x,y,w,h,fill=C.white,stroke=C.border,lw=1) {return shape(slide,'rect',x,y,w,h,fill,stroke,lw);}
function chrome(slide,deck,kicker,title,page){
  slide.background.fill=C.bg;
  rect(slide,56,48,8,8,C.blue,C.blue,0);
  txt(slide,`CLOUD / WEEK ${deck.n} · ${kicker}`,76,38,890,35,15,C.dark,true);
  txt(slide,title,56,96,1080,72,39,C.navy,true);
  slide.images.add({blob:logoBytes,contentType:'image/png',alt:'KOSEN KMITL logo',fit:'contain',position:{left:1060,top:31,width:164,height:76}});
  txt(slide,`KOSEN-KMITL | 02005097 Cloud Infrastructure and Security`,56,687,1030,20,11,C.grey);
  txt(slide,String(page),1200,687,24,20,11,C.grey,false,'right');
  slide.speakerNotes.text=`Original course add-on. Primary AWS Academy slides and lab remain in the LMS. Sources: ${deck.source}. Do not display the worksheet's planted-error wording as a teaching example.`;
}
function band(slide,message){rect(slide,56,612,1168,52,C.navy,C.navy,0);txt(slide,message,78,620,1124,36,17,C.white,true);}
function card(slide,x,y,w,h,k,head,body,accent=C.blue){
  rect(slide,x,y,w,h);rect(slide,x,y,w,7,accent,accent,0);
  txt(slide,k.toUpperCase(),x+24,y+22,w-48,28,15,accent,true);
  txt(slide,head,x+24,y+62,w-48,54,24,C.navy,true);
  txt(slide,body,x+24,y+128,w-48,h-144,19,C.grey);
}
function render(slide,s){
  if(s.kind==='cards'){
    s.cards.forEach((v,i)=>card(slide,56+i*400,205,368,370,...v,i===1?C.orange:C.blue));
  } else if(s.kind==='flow'){
    s.steps.forEach((v,i)=>{
      const x=56+i*300;card(slide,x,205,268,193,`0${i+1}`,v[0],v[1],i===1?C.orange:C.blue);
      if(i<3)txt(slide,'→',x+271,274,25,45,30,C.orange,true,'center');
    });
    s.callouts.forEach((v,i)=>{
      const x=56+i*600;rect(slide,x,430,568,145,C.white,C.border,1);rect(slide,x,430,8,145,i?C.orange:C.blue,i?C.orange:C.blue,0);
      txt(slide,v[0],x+24,448,520,35,21,C.navy,true);txt(slide,v[1],x+24,487,520,68,18,C.grey);
    });
  } else if(s.kind==='rules'){
    rect(slide,56,205,568,336,C.white,C.border,1);
    txt(slide,'Rule',80,224,70,30,16,C.dark,true);txt(slide,'Action',166,224,115,30,16,C.dark,true);
    txt(slide,'Source CIDR',300,224,190,30,16,C.dark,true);txt(slide,'Port',520,224,60,30,16,C.dark,true);
    s.rules.forEach((v,i)=>{const y=270+i*111;rect(slide,80,y,520,82,i?C.pale:'#FFF2EA','none',0);v.forEach((cell,j)=>txt(slide,cell,[95,166,300,520][j],y+22,[60,115,190,60][j],38,20,j===1?(cell==='DENY'?C.orange:C.blue):C.navy,j<2));});
    rect(slide,656,205,568,336,C.white,C.border,1);txt(slide,'Trace the packet',680,224,520,40,23,C.navy,true);
    s.probes.forEach((v,i)=>{const y=286+i*112;txt(slide,v[0],680,y,210,40,20,C.dark,true);txt(slide,v[1],888,y,306,58,20,C.grey);});
  }
  band(slide,s.band);
}
async function build(deck){
  const pres=Presentation.create({slideSize:{width:1280,height:720}});
  let slide=pres.slides.add();chrome(slide,deck,'WORKSHOP',deck.title,1);
  txt(slide,deck.subtitle,56,173,1135,52,23,C.grey);
  card(slide,56,250,568,290,'Primary lesson','AWS Academy',deck.n===14?'Cloud Security Foundations Module 4 · VPC security controls':'Cloud Security Foundations Module 5 · Protecting data',C.blue);
  card(slide,656,250,568,290,'Course add-on',`Local ${deck.n===14?'07':'08'}`,deck.n===14?'Trace subnet rules, return traffic and the NAT route.':'Trace upload, read and KMS key-state effects.',C.orange);
  band(slide,'Use the assigned AWS module and lab first; work on only your assigned Local Part.');
  deck.slides.forEach((s,i)=>{slide=pres.slides.add();chrome(slide,deck,s.k,s.t,i+2);render(slide,s);});
  await fs.mkdir(staging,{recursive:true});await fs.mkdir(out,{recursive:true});
  const stem=`Week${deck.n}_Cloud_Workshop_Supplement_v2`;
  const candidate=path.join(staging,`${stem}.candidate.pptx`);
  await (await PresentationFile.exportPptx(pres)).save(candidate);
  const {finalizePresentation}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
  const finalPath=path.join(out,`${stem}.pptx`);
  const result=await finalizePresentation({workspaceDir:root,candidatePath:candidate,finalPath,
    pythonExecutable:python,integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),
    layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),
    layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-heading-fit'],
    fontPolicy:{basis:'design',families:['Arial']},verifyArtifactToolImport:true,
    receiptPath:path.join(staging,`${stem}.validation.json`)});
  console.log(JSON.stringify({deck:stem,slides:pres.slides.items.length,result}));
}
for(const d of decks)await build(d);
