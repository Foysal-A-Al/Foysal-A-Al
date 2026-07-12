from pathlib import Path
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import cairosvg

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '_rendered'
OUT.mkdir(exist_ok=True)

FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FONT_B = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

def font(size, bold=False):
    return ImageFont.truetype(FONT_B if bold else FONT, size)

def render_svg(rel, width=1180):
    raw = cairosvg.svg2png(url=str(ROOT/rel), output_width=width)
    return Image.open(BytesIO(raw)).convert('RGB')

def rounded(draw, xy, r, fill, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=width)

def wrap(draw, text, font_obj, max_width):
    words = text.split()
    lines=[]; cur=''
    for w in words:
        test=(cur+' '+w).strip()
        if draw.textbbox((0,0), test, font=font_obj)[2] <= max_width:
            cur=test
        else:
            if cur: lines.append(cur)
            cur=w
    if cur: lines.append(cur)
    return lines

def add_wrapped(draw, xy, text, font_obj, fill, max_width, gap=7):
    x,y=xy
    for line in wrap(draw,text,font_obj,max_width):
        draw.text((x,y),line,font=font_obj,fill=fill)
        y += font_obj.size + gap
    return y

BG='#0d1117'; PANEL='#161b22'; LINE='#30363d'; TEXT='#e6edf3'; MUTED='#8b949e'; CYAN='#22d3ee'; VIOLET='#818cf8'; PINK='#f472b6'
W=1480

hero=render_svg('assets/hero.svg',1120)
research=render_svg('assets/research-ecosystem.svg',1120)
portfolio=render_svg('assets/portfolio-lab.svg',1120)
thesis=render_svg('assets/thesis-dashboard.svg',1120)
metrics=render_svg('github-metrics.svg',1120)
contrib=render_svg('profile-3d-contrib/profile-night-rainbow.svg',1120)
snake=render_svg('dist/github-contribution-grid-snake.svg',1120)
footer=render_svg('assets/footer.svg',1120)

# Full page canvas
sections=[]
# estimated heights and render content functions
H=10550
im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
# top nav
rounded(d,(0,0,W,64),0,'#010409'); d.line((0,63,W,63),fill=LINE)
rounded(d,(24,15,58,49),17,CYAN); d.text((31,21),'GH',font=font(15,True),fill='#071426')
rounded(d,(82,15,410,49),7,'#0d1117',LINE); d.text((96,24),'Search or jump to...',font=font(13),fill=MUTED)
d.text((440,24),'Pull requests    Issues    Marketplace    Explore',font=font(14,True),fill=TEXT)
# shell
left=38; sidebar_w=270; gap=28; main_x=left+sidebar_w+gap; main_w=1120
# sidebar
rounded(d,(left,94,left+220,314),110,'#10182e','#3b4760',3)
d.ellipse((left+18,112,left+202,296),outline='#67e8f9',width=2)
d.text((left+59,153),'AF',font=font(66,True),fill='#a5b4fc')
d.text((left,338),'Abdullah Al Foysal',font=font(25,True),fill=TEXT)
d.text((left,374),'Foysal-A-Al',font=font(18),fill=MUTED)
y=415
y=add_wrapped(d,(left,y),'AI and ML researcher connecting computational psychiatry, clinical AI, psychology, statistical evaluation, and human centered systems.',font(14),TEXT,sidebar_w-15,6)
rounded(d,(left,y+16,left+220,y+54),7,'#21262d',LINE); d.text((left+90,y+25),'Follow',font=font(14,True),fill=TEXT)
y+=78
for line in ['Genoa, Italy','University of Genoa','Casa Paganini InfoMus Lab','meridyn.org','Open to PhD and research roles']:
    d.text((left,y),line,font=font(13),fill=MUTED); y+=27
# tabs
for x,t in [(main_x,'Overview'),(main_x+108,'Repositories 25'),(main_x+245,'Projects'),(main_x+330,'Packages'),(main_x+422,'Stars')]:
    d.text((x,98),t,font=font(14,t=='Overview'),fill=TEXT if t=='Overview' else MUTED)
d.line((main_x,128,main_x+main_w,128),fill=LINE)
# repo card
card_top=150
rounded(d,(main_x,card_top,main_x+main_w,card_top+10180),10,PANEL,LINE)
d.text((main_x+18,card_top+13),'Foysal-A-Al / README.md',font=font(14,True),fill=TEXT)
d.line((main_x,card_top+44,main_x+main_w,card_top+44),fill=LINE)
y=card_top+66
# hero
im.paste(hero,(main_x,y)); y+=hero.height+22
# badges
labels=['EMAIL','LINKEDIN','GOOGLE SCHOLAR','PORTFOLIO','PROFILE VIEWS']
bx=main_x+150
for label in labels:
    bw=150 if label!='GOOGLE SCHOLAR' else 190
    rounded(d,(bx,y,bx+bw,y+38),8,'#071426','#27364e')
    d.text((bx+15,y+10),label,font=font(12,True),fill=TEXT); bx+=bw+10
y+=64
# profile intro blocks
rounded(d,(main_x,y,main_x+300,y+310),14,'#101827',LINE)
rounded(d,(main_x+330,y,main_x+main_w,y+310),14,'#101827',LINE)
rounded(d,(main_x+75,y+24,main_x+225,y+174),75,'#11162d','#3b4760',2)
d.text((main_x+117,y+65),'AF',font=font(48,True),fill='#a5b4fc')
d.text((main_x+53,y+195),'Abdullah Al Foysal',font=font(18,True),fill=TEXT)
d.text((main_x+75,y+230),'AI / ML Researcher',font=font(14,True),fill=CYAN)
d.text((main_x+57,y+260),'University of Genoa',font=font(13),fill=MUTED)
d.text((main_x+50,y+284),'Casa Paganini InfoMus Lab',font=font(13),fill=MUTED)
d.text((main_x+355,y+25),'Research profile',font=font(24,True),fill=TEXT)
intro='I build machine learning systems for questions where prediction alone is not enough. My work combines computational psychiatry, clinical and multimodal AI, psychology, human behaviour, explainable machine learning, Bayesian evaluation, and research engineering.'
ny=add_wrapped(d,(main_x+355,y+72),intro,font(15),TEXT,main_w-380,8)
d.text((main_x+355,ny+8),'scientific question → data design → modelling → statistical evaluation',font=font(14,True),fill='#c4b5fd')
d.text((main_x+355,ny+34),'→ explanation → uncertainty → usable research software',font=font(14,True),fill='#c4b5fd')
rounded(d,(main_x+355,ny+78,main_x+main_w-24,ny+154),10,'#11192a',VIOLET,1)
add_wrapped(d,(main_x+373,ny+92),'Research principle: high accuracy is only one part of a credible system. Human centred AI also requires calibration, interpretability, reproducibility, ethical framing, and clear limits.',font(13),TEXT,main_w-425,5)
y+=345

def heading(text):
    global y
    d.text((main_x,y),text,font=font(25,True),fill=TEXT)
    d.line((main_x,y+39,main_x+main_w,y+39),fill=LINE)
    y+=58

def paste(img, margin=18):
    global y
    im.paste(img,(main_x,y)); y+=img.height+margin

heading('Research ecosystem'); paste(research)
heading('Research programmes')
programs=[('Computational psychiatry','Bipolar disorder, rapid cycling, treatment response, temporal models, symptom graphs, and digital phenotyping.'),('Clinical and multimodal AI','Clinical, pharmacological, imaging, EEG, speech, wearable, and behavioural variables for risk forecasting.'),('Explainable and safe ML','LIME, SHAP, calibration, uncertainty, abstention, fairness, subgroup evaluation, and documentation.'),('Statistical evaluation','Bayesian correlated tests, NHST, ROPE, repeated validation, equivalence, and uncertainty.'),('Multimodal HCI','Computer vision, movement, social signals, behavioural computing, and interactive research systems.'),('Research engineering','FastAPI, Streamlit, PyQt6, Docker, GitHub Actions, testing, databases, and reproducible pipelines.')]
for i,(title,body) in enumerate(programs):
    col=i%3; row=i//3; x=main_x+col*373; yy=y+row*155
    rounded(d,(x,yy,x+350,yy+135),12,'#101827',LINE)
    d.text((x+16,yy+15),title,font=font(16,True),fill=TEXT)
    add_wrapped(d,(x+16,yy+48),body,font(13),MUTED,318,5)
y+=330
heading('Flagship project laboratory'); paste(portfolio)
heading('Selected public systems')
projects=[('PsychoGraph-Net','Graph augmented Transformer for psychiatric prediction using symptom topology and longitudinal dynamics.','GCN / TRANSFORMER / NEO4J / LIME'),('NeuroFusion','Uncertainty aware mental health platform with calibrated probabilities, API, dashboard, and tests.','CALIBRATION / FASTAPI / STREAMLIT / DOCKER'),('Optical Flow Cluster Analyzer','Real time movement quality analysis with detection, optical flow, clustering, validation, and export.','YOLOV8 / OPTICAL FLOW / PYQT6'),('PyEyesWeb','Python toolkit for expressive movement analysis across research, health, arts, and interactive systems.','PACKAGE / FEATURES / DOCS / INTEGRATION'),('Psychological Analytics and Blockchain','Predictive psychological analytics with a lightweight auditable data integrity layer.','RANDOM FOREST / HASH LINKED RECORDS'),('Student Stress Analysis','Multi factor study of psychological, physiological, academic, social, and environmental stress.','EDA / FEATURE IMPORTANCE / VISUALISATION')]
for i,(title,body,tag) in enumerate(projects):
    col=i%2; row=i//2; x=main_x+col*560; yy=y+row*180
    rounded(d,(x,yy,x+535,yy+160),12,'#101827',LINE)
    d.text((x+17,yy+16),title,font=font(17,True),fill=TEXT)
    add_wrapped(d,(x+17,yy+48),body,font(13),MUTED,500,5)
    d.text((x+17,yy+132),tag,font=font(11,True),fill=CYAN)
y+=560
heading('MSc thesis'); paste(thesis)
rounded(d,(main_x,y,main_x+main_w,y+250),14,'#101827',LINE)
d.text((main_x+22,y+22),'Statistically Sound Model Selection',font=font(20,True),fill=TEXT)
items=['54 datasets','5 classifiers','Repeated 10 x 10 CV','NHST','Bayesian correlated test','ROPE decisions']
for i,t in enumerate(items):
    col=i%3; row=i//3; x=main_x+22+col*360; yy=y+68+row*78
    rounded(d,(x,yy,x+335,yy+58),9,'#0b1526','#34415a')
    d.text((x+14,yy+18),t,font=font(14,True),fill='#c4b5fd')
y+=285
heading('Experience and education')
entries=[('Research Assistant, Casa Paganini InfoMus Lab','Multimodal HCI, expressive and social behaviour, behavioural analytics, research interfaces, and reproducible software.'),('MSc Computer Engineering, Artificial Intelligence','University of Genoa. Machine learning, deep learning, advanced data systems, and statistical model evaluation.'),('Information Engineering','Jiangxi University of Science and Technology. Computing, programming, information systems, and engineering foundations.'),('Applied engineering in safety critical projects','Inspection, compliance, risk identification, quality monitoring, and technical reporting.')]
for title,body in entries:
    rounded(d,(main_x,y,main_x+main_w,y+92),10,'#101827',LINE)
    d.ellipse((main_x+18,y+20,main_x+32,y+34),fill=CYAN)
    d.text((main_x+48,y+15),title,font=font(15,True),fill=TEXT)
    add_wrapped(d,(main_x+48,y+44),body,font(13),MUTED,main_w-80,4)
    y+=106
heading('Technical stack')
stacks=[('ML and deep learning','PyTorch, TensorFlow, scikit learn, XGBoost, GNNs, Transformers'),('Statistics and XAI','Bayesian inference, NHST, ROPE, LIME, SHAP, bootstrap uncertainty'),('Vision and HCI','OpenCV, YOLO, optical flow, PyQt6, Streamlit, behavioural signals'),('Data systems','pandas, NumPy, SQL, MongoDB, Cassandra, Neo4j'),('Deployment','FastAPI, Docker, GitHub Actions, Terraform, testing and linting'),('Research quality','Calibration, leakage control, model cards, data cards, ethics framing')]
for i,(title,body) in enumerate(stacks):
    col=i%3; row=i//3; x=main_x+col*373; yy=y+row*125
    rounded(d,(x,yy,x+350,yy+105),10,'#101827',LINE)
    d.text((x+16,yy+14),title,font=font(14,True),fill='#c4b5fd')
    add_wrapped(d,(x+16,yy+43),body,font(12),MUTED,318,4)
y+=270
heading('Live GitHub intelligence'); paste(metrics)
heading('3D contribution landscape'); paste(contrib)
heading('Contribution stream'); paste(snake)
paste(footer,0)
# crop to used height
im=im.crop((0,0,W,min(H,y+60)))
im.save(ROOT/'profile-preview-full.png',quality=92)
# top crop
im.crop((0,0,W,min(1500,im.height))).save(ROOT/'profile-preview-top.png',quality=94)
# research crop around ecosystem and projects
research_top=1250
im.crop((0,research_top,W,min(research_top+2200,im.height))).save(ROOT/'profile-preview-research.png',quality=94)
print('Created', im.size)
