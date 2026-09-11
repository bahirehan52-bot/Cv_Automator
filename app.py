import streamlit as st
from PIL import Image
from io import BytesIO
import base64, html, re

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

st.set_page_config(page_title="CV Automator Premium", page_icon="📄", layout="wide")

def esc(x):
    return html.escape(str(x or ""))

def blocks(text):
    return [[x.strip() for x in b.splitlines() if x.strip()]
            for b in re.split(r"\n\s*\n", text or "") if b.strip()]

def skills(text):
    out=[]
    fallback=[95,90,85,80,75,70,65,60]
    for i,line in enumerate((text or "").splitlines()):
        if not line.strip(): continue
        if "|" in line:
            name,p=line.split("|",1)
            try: pct=int(re.sub(r"\D","",p))
            except: pct=fallback[i%len(fallback)]
        else:
            name=line; pct=fallback[i%len(fallback)]
        out.append((name.strip(),max(0,min(100,pct))))
    return out

def wrap(c,text,width,font,size):
    words=str(text).split(); lines=[]; cur=""
    for w in words:
        test=(cur+" "+w).strip()
        if c.stringWidth(test,font,size)<=width: cur=test
        else:
            if cur: lines.append(cur)
            cur=w
    if cur: lines.append(cur)
    return lines

def drawwrap(c,text,x,y,width,font,size,leading,col,max_lines=None):
    ls=wrap(c,text,width,font,size)
    if max_lines: ls=ls[:max_lines]
    c.setFont(font,size); c.setFillColor(col)
    for line in ls:
        c.drawString(x,y,line); y-=leading
    return y

defaults={"name":"","role":"","email":"","phone":"","location":"","linkedin":"",
"website":"","summary":"","experience":"","education":"","projects":"","skills":"",
"languages":"","certifications":"","photo":None}
for k,v in defaults.items():
    if k not in st.session_state: st.session_state[k]=v

st.markdown("""
<style>
.stApp{background:#080b12}.block-container{max-width:1500px}
.hero{padding:28px;border-radius:20px;background:linear-gradient(135deg,#111827,#202938);
border:1px solid #303b50;margin-bottom:20px}.hero h1{color:white;margin:0;font-weight:900}
.hero p{color:#9ca3af}.score{padding:14px 18px;background:#171d28;border:1px solid #303b50;
border-radius:14px;margin-bottom:15px}.score b{font-size:30px}
.cv{width:794px;height:1123px;display:flex;overflow:hidden;background:white;font-family:Arial;
box-shadow:0 20px 70px #0008}.side{width:286px;flex:0 0 286px;background:#151515;color:white;
padding:22px;box-sizing:border-box;position:relative;overflow:hidden}.side:before{content:"";
position:absolute;left:0;top:0;width:100%;height:230px;background:linear-gradient(135deg,var(--a),#ff9800);
clip-path:polygon(0 0,100% 0,100% 62%,45% 100%,0 77%)}.side>*{position:relative;z-index:2}
.main{width:508px;flex:0 0 508px;padding:48px 38px;box-sizing:border-box;overflow:hidden;
position:relative;background:linear-gradient(135deg,#fff,#f4f4f5)}.main:before{content:"";
position:absolute;right:0;top:0;width:220px;height:78px;background:#151515;
clip-path:polygon(28% 0,100% 0,100% 100%,0 100%)}.photo{width:135px;height:135px;object-fit:cover;
border-radius:50%;display:block;margin:8px auto 18px;border:6px solid #151515;box-shadow:0 0 0 4px var(--a)}
.placeholder{width:135px;height:135px;border-radius:50%;margin:8px auto 18px;background:#292929;
display:flex;align-items:center;justify-content:center;font-size:48px;border:6px solid #151515;
box-shadow:0 0 0 4px var(--a)}.sname{text-align:center;font-size:19px;font-weight:900}.role{
text-align:center;color:var(--a);font-size:9px;font-weight:800;letter-spacing:1px;margin:6px 0 18px}
.sh{color:var(--a);font-size:9px;font-weight:900;letter-spacing:1.5px;border-left:3px solid var(--a);
padding-left:7px;margin:14px 0 7px}.st{font-size:8px;line-height:1.4;color: #38BDF8;margin:3px 0;
word-break:break-word}.skill{margin:6px 0}.skillhead{display:flex;justify-content:space-between;
font-size:8px;font-weight:700}.track{height:4px;background:#ffffff22;border-radius:5px;margin-top:3px}
.bar{height:100%;background:var(--a);border-radius:5px}.mn{font-size:31px;font-weight:900;
line-height:1.02;max-width:82%;position:relative;z-index:2}.mr{display:inline-block;background:#151515;
color:var(--a);padding:6px 12px;margin-top:9px;font-size:8px;font-weight:900;letter-spacing:1px;
position:relative;z-index:2}.sec{font-size:13px;font-weight:900;border-bottom:2px solid var(--a);
padding-bottom:5px;margin:19px 0 9px;position:relative;z-index:2}.summary{font-size:8.5px;
line-height:1.5;color:#4b5563;position:relative;z-index:2}.item{border-left:2px solid var(--a);
padding-left:9px;margin-bottom:9px;position:relative;z-index:2}.it{font-size:9.5px;font-weight:900}
.im{font-size:7.5px;font-weight:800;color:#9a6900;margin:2px 0 4px}.itxt{font-size:7.7px;
line-height:1.4;color:#4b5563}
</style>
""",unsafe_allow_html=True)

st.markdown("""<div class="hero"><h1>CV Automator <span style="color:#FFC107">PREMIUM</span></h1>
<p>Professional single-page A4 CV — photo, skills, languages and certificates stay on Page 1.</p></div>""",unsafe_allow_html=True)

with st.sidebar:
    st.header("Design")
    accent=st.color_picker("Accent","#FFC107")
    sidebar=st.color_picker("Sidebar","#151515")

left,right=st.columns([.82,1.18],gap="large")
with left:
    t=st.tabs(["Personal","Profile","Experience","Education","Projects","Skills","More"])
    with t[0]:
        f=st.file_uploader("Profile Picture",type=["jpg","jpeg","png","webp"])
        if f:
            im=Image.open(f).convert("RGB"); b=BytesIO(); im.save(b,"JPEG",quality=95)
            st.session_state.photo=b.getvalue()
        if st.session_state.photo:
            st.image(st.session_state.photo,width=120)
        st.session_state.name=st.text_input("Full Name",st.session_state.name)
        st.session_state.role=st.text_input("Professional Title",st.session_state.role)
        st.session_state.email=st.text_input("Email",st.session_state.email)
        st.session_state.phone=st.text_input("Phone",st.session_state.phone)
        st.session_state.location=st.text_input("Location",st.session_state.location)
        st.session_state.linkedin=st.text_input("LinkedIn",st.session_state.linkedin)
        st.session_state.website=st.text_input("Portfolio / Website",st.session_state.website)
    with t[1]:
        st.session_state.summary=st.text_area("Professional Summary",st.session_state.summary,height=180)
    with t[2]:
        st.session_state.experience=st.text_area("Experience",st.session_state.experience,height=270,
        placeholder="""Junior Web Developer — Freelance
2025 - 2026
Developed responsive websites using HTML, CSS, JavaScript and Python.
Built small web applications according to client requirements.
Improved performance and user experience.""")
    with t[3]:
        st.session_state.education=st.text_area("Education",st.session_state.education,height=220,
        placeholder="""FSc Pre-Engineering — 1st Year
Punjab Board
2026 - Present

Matriculation (Science)
Punjab Board
Completed 2026""")
    with t[4]:
        st.session_state.projects=st.text_area("Projects",st.session_state.projects,height=260,
        placeholder="""AI Study Assistant
Python / AI
Developed an AI-based study planning application.
Generates personalized schedules and MCQs.

CV Automator
Python / Streamlit
Built a professional CV generation application with PDF export.

Personal Portfolio Website
HTML / CSS / JavaScript
Created a responsive portfolio website.""")
    with t[5]:
        st.session_state.skills=st.text_area("Skills",st.session_state.skills,height=220,
        placeholder="""Python | 95
Streamlit | 90
HTML | 90
CSS | 85
JavaScript | 75
Git & GitHub | 80
C++ | 70""")
    with t[6]:
        st.session_state.languages=st.text_area("Languages",st.session_state.languages,height=110,
        placeholder="""English — Intermediate
Urdu — Native
Punjabi — Fluent""")
        st.session_state.certifications=st.text_area("Certificates",st.session_state.certifications,height=110,
        placeholder="""Python Programming Certificate
Web Development Certificate
AI Fundamentals Certificate""")

with right:
    vals=[st.session_state[k] for k in ["name","role","email","summary","experience","education",
    "projects","skills","languages","certifications"]]
    score=round(sum(bool(str(x).strip()) for x in vals)/len(vals)*100)
    st.markdown(f'<div class="score">CV COMPLETENESS<br><b style="color:{accent}">{score}%</b></div>',
                unsafe_allow_html=True)

    if st.session_state.photo:
        enc=base64.b64encode(st.session_state.photo).decode()
        ph=f'<img class="photo" src="data:image/jpeg;base64,{enc}">'
    else: ph='<div class="placeholder">👤</div>'

    contact="".join(f'<div class="st">{esc(x)}</div>' for x in
                    [st.session_state.email,st.session_state.phone,st.session_state.location,
                     st.session_state.linkedin,st.session_state.website] if x.strip())
    sk=""
    for n,p in skills(st.session_state.skills)[:7]:
        sk+=f'<div class="skill"><div class="skillhead"><span>{esc(n)}</span><span>{p}%</span></div><div class="track"><div class="bar" style="width:{p}%"></div></div></div>'

    def side_text(title,text):
        a=[x.strip() for x in (text or "").splitlines() if x.strip()]
        return (f'<div class="sh">{title}</div>'+''.join(f'<div class="st">• {esc(x)}</div>' for x in a[:5])) if a else ""

    def main_sec(title,text):
        if not text.strip(): return ""
        z=f'<div class="sec">{title}</div>'
        for b in blocks(text):
            z+='<div class="item"><div class="it">'+esc(b[0])+'</div>'
            if len(b)>1:z+=f'<div class="im">{esc(b[1])}</div>'
            for x in b[2:]:z+=f'<div class="itxt">• {esc(x.lstrip("-• ").strip())}</div>'
            z+='</div>'
        return z

    summary=(f'<div class="sec">ABOUT ME</div><div class="summary">{esc(st.session_state.summary)}</div>'
             if st.session_state.summary.strip() else "")

    st.markdown(f"""<div class="cv" style="--a:{accent}">
    <aside class="side" style="background:{sidebar}">{ph}
    <div class="sname">{esc(st.session_state.name) or "YOUR NAME"}</div>
    <div class="role">{esc(st.session_state.role) or "PROFESSIONAL TITLE"}</div>
    <div class="sh">CONTACT</div>{contact}
    <div class="sh">SKILLS</div>{sk}
    {side_text("LANGUAGES",st.session_state.languages)}
    {side_text("CERTIFICATIONS",st.session_state.certifications)}
    </aside>
    <main class="main"><div class="mn">{esc(st.session_state.name) or "YOUR NAME"}</div>
    <div class="mr">{esc(st.session_state.role) or "PROFESSIONAL TITLE"}</div>
    {summary}{main_sec("EDUCATION",st.session_state.education)}
    {main_sec("EXPERIENCE",st.session_state.experience)}
    {main_sec("PROJECTS",st.session_state.projects)}
    </main></div>""",unsafe_allow_html=True)

def pdf():
    buf=BytesIO(); pw,ph=A4; c=canvas.Canvas(buf,pagesize=A4)
    a=colors.HexColor(accent); s=colors.HexColor(sidebar); sw=70*mm
    c.setFillColor(colors.white);c.rect(0,0,pw,ph,fill=1,stroke=0)
    c.setFillColor(s);c.rect(0,0,sw,ph,fill=1,stroke=0)
    p=c.beginPath();p.moveTo(0,ph);p.lineTo(sw,ph);p.lineTo(sw,ph-55*mm);p.lineTo(31*mm,ph-82*mm);p.lineTo(0,ph-65*mm);p.close()
    c.setFillColor(a);c.drawPath(p,fill=1,stroke=0)
    cx=sw/2; ps=43*mm; px=cx-ps/2; py=ph-62*mm
    if st.session_state.photo:
        c.drawImage(ImageReader(BytesIO(st.session_state.photo)),px,py,width=ps,height=ps,
                    preserveAspectRatio=True,anchor="c",mask="auto")
    else:
        c.setFillColor(colors.HexColor("#292929"));c.circle(cx,py+ps/2,ps/2,fill=1,stroke=0)
    sy=ph-69*mm;c.setFillColor(colors.white);c.setFont("Helvetica-Bold",8.5)
    for x in wrap(c,st.session_state.name or "YOUR NAME",sw-20*mm,"Helvetica-Bold",8.5)[:2]:
        c.drawCentredString(cx,sy,x);sy-=4*mm
    c.setFillColor(a);c.setFont("Helvetica-Bold",6.5);c.drawCentredString(cx,sy-1*mm,
        (st.session_state.role or "PROFESSIONAL TITLE")[:42]);sy-=10*mm
    sx=10*mm;tw=sw-20*mm
    def sh(t):
        nonlocal sy
        c.setFillColor(a);c.setFont("Helvetica-Bold",7.5);c.drawString(sx,sy,t);sy-=5*mm
    sh("CONTACT")
    for x in [st.session_state.email,st.session_state.phone,st.session_state.location,st.session_state.linkedin,st.session_state.website]:
        if x.strip(): sy=drawwrap(c,x,sx,sy,tw,"Helvetica",6.1,2.8*mm,colors.HexColor("#eee"),2)-1.2*mm
    if skills(st.session_state.skills):
        sh("SKILLS")
        for n,pct in skills(st.session_state.skills)[:7]:
            c.setFillColor(colors.white);c.setFont("Helvetica",6.2);c.drawString(sx,sy,n[:25])
            c.drawRightString(sx+tw,sy,f"{pct}%");sy-=3*mm
            c.setFillColor(colors.HexColor("#444"));c.rect(sx,sy,tw,1.1*mm,fill=1,stroke=0)
            c.setFillColor(a);c.rect(sx,sy,tw*pct/100,1.1*mm,fill=1,stroke=0);sy-=5*mm
    for title,text in [("LANGUAGES",st.session_state.languages),("CERTIFICATIONS",st.session_state.certifications)]:
        arr=[x.strip() for x in text.splitlines() if x.strip()]
        if arr:
            sh(title)
            for x in arr[:5]:sy=drawwrap(c,"• "+x,sx,sy,tw,"Helvetica",6.1,2.8*mm,colors.HexColor("#eee"),2)-1*mm
    mx=sw+10*mm;mw=pw-mx-10*mm;y=ph-20*mm
    y=drawwrap(c,(st.session_state.name or "YOUR NAME").upper(),mx,y,mw,"Helvetica-Bold",19,8*mm,colors.HexColor("#151515"),2)
    c.setFillColor(a);c.setFont("Helvetica-Bold",7.5);c.drawString(mx,y-1*mm,(st.session_state.role or "PROFESSIONAL TITLE")[:65]);y-=12*mm
    if st.session_state.summary.strip():
        c.setFillColor(colors.HexColor("#151515"));c.setFont("Helvetica-Bold",10);c.drawString(mx,y,"ABOUT ME");y-=2.5*mm
        c.setStrokeColor(a);c.line(mx,y,mx+mw,y);y-=5*mm
        y=drawwrap(c,st.session_state.summary,mx,y,mw,"Helvetica",7,3.2*mm,colors.HexColor("#555"),6)-2*mm
    def section(title,text):
        nonlocal y
        if not text.strip():return
        c.setFillColor(colors.HexColor("#151515"));c.setFont("Helvetica-Bold",9.5);c.drawString(mx,y,title);y-=2.5*mm
        c.setStrokeColor(a);c.line(mx,y,mx+mw,y);y-=5*mm
        for b in blocks(text):
            if y<18*mm:return
            c.setStrokeColor(a);c.setLineWidth(1);c.line(mx,y+1*mm,mx,y-9*mm)
            c.setFillColor(colors.HexColor("#151515"));c.setFont("Helvetica-Bold",7.8);c.drawString(mx+3*mm,y,b[0][:70]);y-=3.2*mm
            if len(b)>1:
                c.setFillColor(colors.HexColor("#9a6900"));c.setFont("Helvetica-Bold",6.5);c.drawString(mx+3*mm,y,b[1][:65]);y-=3.2*mm
            for x in b[2:]:
                y=drawwrap(c,"• "+x.lstrip("-• ").strip(),mx+3*mm,y,mw-3*mm,"Helvetica",6.5,2.8*mm,colors.HexColor("#555"),2)
            y-=2*mm
    section("EDUCATION",st.session_state.education)
    section("EXPERIENCE",st.session_state.experience)
    section("PROJECTS",st.session_state.projects)
    c.setFillColor(colors.HexColor("#888"));c.setFont("Helvetica",5);c.drawRightString(pw-10*mm,5*mm,"CV Automator Premium")
    c.showPage();c.save();buf.seek(0);return buf.getvalue()

if st.button("📄 Generate Professional PDF",use_container_width=True):
    try:
        data=pdf()
        st.download_button("⬇️ Download CV PDF",data=data,
            file_name=(st.session_state.name.strip().replace(" ","_") or "CV")+".pdf",
            mime="application/pdf",use_container_width=True)
        st.success("Single-page A4 PDF created.")
    except Exception as e: st.error(f"PDF generation failed: {e}")
