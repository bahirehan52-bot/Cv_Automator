import streamlit as st
from PIL import Image
from io import BytesIO
import base64
import html
import re

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


st.set_page_config(
    page_title="CV Automator Premium",
    page_icon="📄",
    layout="wide"
)


def esc(value):
    return html.escape(str(value or ""))


def parse_blocks(text):
    if not text or not text.strip():
        return []
    return [
        [line.strip() for line in block.splitlines() if line.strip()]
        for block in re.split(r"\n\s*\n", text.strip())
        if block.strip()
    ]


def parse_skills(text):
    result = []
    defaults = [95, 90, 85, 80, 75, 70]

    for index, line in enumerate((text or "").splitlines()):
        line = line.strip()
        if not line:
            continue

        if "|" in line:
            name, level = line.split("|", 1)
            name = name.strip()
            try:
                percent = int(re.sub(r"[^0-9]", "", level))
            except (ValueError, TypeError):
                percent = defaults[index % len(defaults)]
        else:
            name = line
            percent = defaults[index % len(defaults)]

        result.append((name, max(0, min(100, percent))))

    return result


def render_main_section(title, content, accent):
    if not content or not content.strip():
        return ""

    result = f'''
    <div class="main-section" style="--accent:{accent};">
        {esc(title.upper())}
    </div>
    '''

    for block in parse_blocks(content):
        result += '<div class="timeline-item">'

        if block:
            result += f'''
            <div class="timeline-title">{esc(block[0])}</div>
            '''

        if len(block) > 1:
            result += f'''
            <div class="timeline-meta">{esc(block[1])}</div>
            '''

        for line in block[2:]:
            clean = line.lstrip("-• ").strip()
            if clean:
                result += f'''
                <div class="timeline-text">• {esc(clean)}</div>
                '''

        result += "</div>"

    return result


def render_sidebar_list(title, text, accent):
    if not text or not text.strip():
        return ""

    result = f'''
    <div class="sidebar-section" style="--accent:{accent};">
        {esc(title.upper())}
    </div>
    '''

    for line in text.splitlines():
        if line.strip():
            result += f'''
            <div class="sidebar-text">• {esc(line.strip())}</div>
            '''

    return result


def skill_html(skills, accent):
    parsed = parse_skills(skills)

    if not parsed:
        return ""

    result = f'''
    <div class="sidebar-section" style="--accent:{accent};">
        SKILLS
    </div>
    '''

    for name, percent in parsed:
        result += f'''
        <div class="skill-item">
            <div class="skill-head">
                <span>{esc(name)}</span>
                <span>{percent}%</span>
            </div>
            <div class="skill-track">
                <div class="skill-bar"
                     style="width:{percent}%; background:{accent};">
                </div>
            </div>
        </div>
        '''

    return result


st.markdown(
    '''
<style>
.stApp {
    background: #080b12;
}
.block-container {
    max-width: 1550px;
    padding-top: 24px;
    padding-bottom: 50px;
}
section[data-testid="stSidebar"] {
    background: #0d1119;
}
.hero {
    position: relative;
    overflow: hidden;
    padding: 34px;
    margin-bottom: 24px;
    border: 1px solid #283348;
    border-radius: 24px;
    background:
        radial-gradient(circle at 90% 15%, rgba(255,193,7,.20), transparent 30%),
        linear-gradient(135deg, #101827, #1b2435);
}
.hero h1 {
    margin: 0;
    color: #ffffff;
    font-size: 42px;
    font-weight: 900;
}
.hero p {
    margin: 8px 0 0;
    color: #9ca3af;
    font-size: 15px;
}
.score-card {
    padding: 18px 22px;
    margin-bottom: 18px;
    border-radius: 16px;
    border: 1px solid #2d3748;
    background: linear-gradient(135deg, #151b26, #232b3a);
}
.score-label {
    color: #9ca3af;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 2px;
}
.score-number {
    color: #ffc107;
    font-size: 34px;
    font-weight: 900;
}
.cv-wrapper {
    width: 100%;
    min-height: 1120px;
    display: flex;
    overflow: hidden;
    position: relative;
    background: #ffffff;
    box-shadow: 0 25px 80px rgba(0,0,0,.55);
    font-family: Arial, Helvetica, sans-serif;
}
.cv-sidebar {
    width: 36%;
    min-height: 1120px;
    position: relative;
    overflow: hidden;
    padding: 30px 25px;
    color: #ffffff;
    background: #151515;
}
.cv-sidebar::before {
    content: "";
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 285px;
    background: linear-gradient(135deg, var(--accent), #ff9800);
    clip-path: polygon(0 0, 100% 0, 100% 64%, 44% 100%, 0 77%);
}
.cv-sidebar::after {
    content: "";
    position: absolute;
    right: -40px;
    bottom: -50px;
    width: 190px;
    height: 190px;
    border: 28px solid var(--accent);
    transform: rotate(45deg);
    opacity: .9;
}
.cv-sidebar > * {
    position: relative;
    z-index: 2;
}
.cv-main {
    width: 64%;
    min-height: 1120px;
    position: relative;
    overflow: hidden;
    padding: 58px 48px;
    color: #171717;
    background: linear-gradient(135deg, #ffffff, #f3f4f6);
}
.cv-main::before {
    content: "";
    position: absolute;
    top: 0;
    right: 0;
    width: 320px;
    height: 115px;
    background: #151515;
    clip-path: polygon(25% 0, 100% 0, 100% 100%, 0 100%);
}
.cv-main::after {
    content: "";
    position: absolute;
    right: -40px;
    bottom: -70px;
    width: 280px;
    height: 280px;
    background: var(--accent);
    opacity: .12;
    transform: rotate(45deg);
}
.profile-photo, .photo-placeholder {
    width: 158px;
    height: 158px;
    display: block;
    margin: 8px auto 25px;
    object-fit: cover;
    border-radius: 50%;
    border: 7px solid #151515;
    box-shadow: 0 0 0 5px var(--accent);
}
.photo-placeholder {
    display: flex;
    align-items: center;
    justify-content: center;
    background: #292929;
    font-size: 58px;
}
.sidebar-name {
    text-align: center;
    color: #ffffff;
    font-size: 22px;
    font-weight: 900;
    line-height: 1.15;
}
.sidebar-role {
    margin-top: 7px;
    margin-bottom: 28px;
    text-align: center;
    color: var(--accent);
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.4px;
    text-transform: uppercase;
}
.sidebar-section {
    margin-top: 24px;
    margin-bottom: 12px;
    padding-left: 10px;
    border-left: 4px solid var(--accent);
    color: var(--accent);
    font-size: 11px;
    font-weight: 900;
    letter-spacing: 1.8px;
}
.sidebar-text {
    margin-bottom: 8px;
    color: #e5e7eb;
    font-size: 9.5px;
    line-height: 1.55;
    word-break: break-word;
}
.skill-item {
    margin-bottom: 12px;
}
.skill-head {
    display: flex;
    justify-content: space-between;
    gap: 8px;
    margin-bottom: 5px;
    color: #ffffff;
    font-size: 9.5px;
    font-weight: 700;
}
.skill-track {
    height: 5px;
    overflow: hidden;
    border-radius: 10px;
    background: rgba(255,255,255,.16);
}
.skill-bar {
    height: 100%;
    border-radius: 10px;
}
.cv-name {
    position: relative;
    z-index: 2;
    max-width: 78%;
    margin-top: 12px;
    color: #151515;
    font-size: 39px;
    font-weight: 900;
    line-height: 1.02;
    letter-spacing: .5px;
    text-transform: uppercase;
}
.cv-role {
    position: relative;
    z-index: 2;
    display: inline-block;
    margin-top: 11px;
    padding: 7px 16px;
    color: var(--accent);
    background: #151515;
    font-size: 10px;
    font-weight: 900;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    clip-path: polygon(0 0, 100% 0, 92% 100%, 0 100%);
}
.main-section {
    position: relative;
    z-index: 2;
    margin-top: 30px;
    margin-bottom: 15px;
    padding-bottom: 7px;
    border-bottom: 3px solid var(--accent);
    color: #151515;
    font-size: 17px;
    font-weight: 900;
    letter-spacing: 1.5px;
}
.summary-box {
    position: relative;
    z-index: 2;
    color: #4b5563;
    font-size: 10.5px;
    line-height: 1.7;
}
.timeline-item {
    position: relative;
    z-index: 2;
    margin-bottom: 17px;
    padding-left: 15px;
    border-left: 3px solid var(--accent);
}
.timeline-title {
    color: #151515;
    font-size: 11.5px;
    font-weight: 900;
}
.timeline-meta {
    margin: 4px 0 6px;
    color: #9a6900;
    font-size: 9px;
    font-weight: 800;
}
.timeline-text {
    color: #4b5563;
    font-size: 9.5px;
    line-height: 1.6;
}
@media (max-width: 900px) {
    .cv-wrapper {
        flex-direction: column;
    }
    .cv-sidebar, .cv-main {
        width: 100%;
    }
    .cv-name {
        max-width: 100%;
    }
}
</style>
    ''',
    unsafe_allow_html=True
)


defaults = {
    "name": "",
    "role": "",
    "email": "",
    "phone": "",
    "location": "",
    "linkedin": "",
    "website": "",
    "summary": "",
    "experience": "",
    "education": "",
    "projects": "",
    "skills": "",
    "languages": "",
    "certifications": "",
    "photo": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


st.markdown(
    '''
    <div class="hero">
        <h1>CV Automator <span style="color:#ffc107;">PREMIUM</span></h1>
        <p>Modern geometric CV • Photo • Live preview • A4 PDF export</p>
    </div>
    ''',
    unsafe_allow_html=True
)


with st.sidebar:
    st.header("🎨 Design")

    accent = st.color_picker(
        "Accent Color",
        "#FFC107"
    )

    sidebar_color = st.color_picker(
        "Sidebar Color",
        "#151515"
    )

    st.divider()
    st.caption("Premium geometric A4 template")


editor, preview = st.columns(
    [0.86, 1.14],
    gap="large"
)


with editor:

    tabs = st.tabs([
        "👤 Personal",
        "🧠 Profile",
        "💼 Experience",
        "🎓 Education",
        "🚀 Projects",
        "🛠 Skills",
        "📜 More"
    ])

    with tabs[0]:

        st.markdown("### 📸 Profile Picture")

        uploaded = st.file_uploader(
            "Upload Picture",
            type=["jpg", "jpeg", "png", "webp"]
        )

        if uploaded is not None:
            try:
                image = Image.open(uploaded).convert("RGB")
                image_buffer = BytesIO()
                image.save(
                    image_buffer,
                    format="JPEG",
                    quality=95
                )
                st.session_state.photo = image_buffer.getvalue()
            except Exception as exc:
                st.error(f"Image error: {exc}")

        if st.session_state.photo:

            st.image(
                st.session_state.photo,
                width=150
            )

            if st.button("Remove Picture"):
                st.session_state.photo = None
                st.rerun()

        st.divider()

        st.session_state.name = st.text_input(
            "Full Name",
            value=st.session_state.name,
            placeholder="Muhammad Rehan Ahmed"
        )

        st.session_state.role = st.text_input(
            "Professional Title",
            value=st.session_state.role,
            placeholder="Software Engineer"
        )

        st.session_state.email = st.text_input(
            "Email",
            value=st.session_state.email,
            placeholder="you@example.com"
        )

        st.session_state.phone = st.text_input(
            "Phone",
            value=st.session_state.phone,
            placeholder="+92 300 1234567"
        )

        st.session_state.location = st.text_input(
            "Location",
            value=st.session_state.location,
            placeholder="Faisalabad, Pakistan"
        )

        st.session_state.linkedin = st.text_input(
            "LinkedIn",
            value=st.session_state.linkedin,
            placeholder="linkedin.com/in/username"
        )

        st.session_state.website = st.text_input(
            "Portfolio / Website",
            value=st.session_state.website,
            placeholder="yourwebsite.com"
        )

    with tabs[1]:

        st.session_state.summary = st.text_area(
            "Professional Summary",
            value=st.session_state.summary,
            height=190,
            placeholder="Write a concise professional summary..."
        )

    with tabs[2]:

        st.session_state.experience = st.text_area(
            "Experience",
            value=st.session_state.experience,
            height=280,
            placeholder='''Software Developer | ABC Company
2025 - 2026
Developed automation tools
Built web applications
Improved system performance

Freelance Developer | Self Employed
2024 - Present
Created websites
Worked with clients'''
        )

    with tabs[3]:

        st.session_state.education = st.text_area(
            "Education",
            value=st.session_state.education,
            height=230,
            placeholder='''BS Software Engineering
ABC University
2024 - 2028

Intermediate
XYZ College
2022 - 2024'''
        )

    with tabs[4]:

        st.session_state.projects = st.text_area(
            "Projects",
            value=st.session_state.projects,
            height=250,
            placeholder='''CV Automator
Python / Streamlit
Built a premium CV generation application
Created A4 PDF export

AI Study Assistant
Python / AI
Built an AI-powered study planner'''
        )

    with tabs[5]:

        st.info("One skill per line. Optional format: Python | 90")

        st.session_state.skills = st.text_area(
            "Skills",
            value=st.session_state.skills,
            height=230,
            placeholder='''Python | 95
Streamlit | 90
HTML | 90
CSS | 85
JavaScript | 75
Git | 80'''
        )

    with tabs[6]:

        st.session_state.languages = st.text_area(
            "Languages",
            value=st.session_state.languages,
            height=130,
            placeholder='''English
Urdu
Punjabi'''
        )

        st.session_state.certifications = st.text_area(
            "Certifications",
            value=st.session_state.certifications,
            height=130,
            placeholder='''Python Certificate
Web Development Certificate'''
        )


with preview:

    st.markdown("### 👁️ Premium Live Preview")

    score_fields = [
        st.session_state.name,
        st.session_state.role,
        st.session_state.email,
        st.session_state.summary,
        st.session_state.experience,
        st.session_state.education,
        st.session_state.projects,
        st.session_state.skills
    ]

    completed = sum(
        bool(str(field).strip())
        for field in score_fields
    )

    score = round(
        completed / len(score_fields) * 100
    )

    st.markdown(
        f'''
        <div class="score-card">
            <div class="score-label">CV COMPLETENESS</div>
            <div class="score-number" style="color:{accent};">
                {score}/100
            </div>
        </div>
        ''',
        unsafe_allow_html=True
    )

    if st.session_state.photo:

        encoded = base64.b64encode(
            st.session_state.photo
        ).decode("utf-8")

        photo_html = f'''
        <img
            class="profile-photo"
            src="data:image/jpeg;base64,{encoded}"
            style="--accent:{accent};"
        >
        '''

    else:

        photo_html = f'''
        <div class="photo-placeholder" style="--accent:{accent};">
            &#128100;
        </div>
        '''

    contact_html = ""

    contacts = [
        ("Email", st.session_state.email),
        ("Phone", st.session_state.phone),
        ("Location", st.session_state.location),
        ("LinkedIn", st.session_state.linkedin),
        ("Website", st.session_state.website)
    ]

    for label, value in contacts:

        if value and value.strip():

            contact_html += f'''
            <div class="sidebar-text">
                <strong>{esc(label)}:</strong><br>
                {esc(value)}
            </div>
            '''

    languages_html = render_sidebar_list(
        "Languages",
        st.session_state.languages,
        accent
    )

    certifications_html = render_sidebar_list(
        "Certifications",
        st.session_state.certifications,
        accent
    )

    summary_html = ""

    if st.session_state.summary.strip():

        summary_html = f'''
        <div class="main-section" style="--accent:{accent};">
            ABOUT ME
        </div>
        <div class="summary-box">
            {esc(st.session_state.summary)}
        </div>
        '''

    education_html = render_main_section(
        "Education",
        st.session_state.education,
        accent
    )

    experience_html = render_main_section(
        "Experience",
        st.session_state.experience,
        accent
    )

    projects_html = render_main_section(
        "Projects",
        st.session_state.projects,
        accent
    )

    cv_html = f'''
    <style>
    .cv-wrapper {{
        --accent: {accent};
    }}

    .cv-sidebar {{
        background: {sidebar_color};
    }}
    </style>

    <div class="cv-wrapper">

        <div class="cv-sidebar">

            {photo_html}

            <div class="sidebar-name">
                {esc(st.session_state.name) or "YOUR NAME"}
            </div>

            <div class="sidebar-role" style="--accent:{accent};">
                {esc(st.session_state.role) or "PROFESSIONAL TITLE"}
            </div>

            <div class="sidebar-section" style="--accent:{accent};">
                CONTACT
            </div>

            {contact_html}

            {skill_html(st.session_state.skills, accent)}

            {languages_html}

            {certifications_html}

        </div>

        <div class="cv-main">

            <div class="cv-name">
                {esc(st.session_state.name) or "YOUR NAME"}
            </div>

            <div class="cv-role" style="--accent:{accent};">
                {esc(st.session_state.role) or "PROFESSIONAL TITLE"}
            </div>

            {summary_html}
            {education_html}
            {experience_html}
            {projects_html}

        </div>

    </div>
    '''

    st.markdown(
        cv_html,
        unsafe_allow_html=True
    )


def draw_wrapped(c, text, x, y, max_width, font_name, font_size,
                 leading, color_value, max_lines=None):

    if not text:
        return y

    words = str(text).split()
    line = ""
    lines = []

    for word in words:

        test = (line + " " + word).strip()

        if c.stringWidth(
            test,
            font_name,
            font_size
        ) <= max_width:

            line = test

        else:

            if line:
                lines.append(line)

            line = word

    if line:
        lines.append(line)

    if max_lines:
        lines = lines[:max_lines]

    c.setFillColor(color_value)
    c.setFont(font_name, font_size)

    for item in lines:

        c.drawString(
            x,
            y,
            item
        )

        y -= leading

    return y


def draw_pdf_section(
    c,
    title,
    content,
    x,
    y,
    width,
    accent_color
):

    if not content or not content.strip():
        return y

    if y < 45 * mm:

        c.showPage()

        y = A4[1] - 22 * mm

    c.setFillColor(
        colors.HexColor("#151515")
    )

    c.setFont(
        "Helvetica-Bold",
        12
    )

    c.drawString(
        x,
        y,
        title.upper()
    )

    y -= 3 * mm

    c.setStrokeColor(
        accent_color
    )

    c.setLineWidth(2)

    c.line(
        x,
        y,
        x + width,
        y
    )

    y -= 7 * mm

    for block in parse_blocks(content):

        if not block:
            continue

        if y < 32 * mm:

            c.showPage()

            y = A4[1] - 22 * mm

        c.setFillColor(
            colors.HexColor("#151515")
        )

        y = draw_wrapped(
            c,
            block[0],
            x + 3 * mm,
            y,
            width - 3 * mm,
            "Helvetica-Bold",
            9,
            4 * mm,
            colors.HexColor("#151515"),
            2
        )

        if len(block) > 1:

            y = draw_wrapped(
                c,
                block[1],
                x + 3 * mm,
                y - 1 * mm,
                width - 3 * mm,
                "Helvetica-Bold",
                7.5,
                3.5 * mm,
                colors.HexColor("#9A6900"),
                2
            )

        for line in block[2:]:

            clean = line.lstrip("-• ").strip()

            if clean:

                y = draw_wrapped(
                    c,
                    "• " + clean,
                    x + 3 * mm,
                    y - 1 * mm,
                    width - 3 * mm,
                    "Helvetica",
                    7.5,
                    3.5 * mm,
                    colors.HexColor("#555555"),
                    3
                )

        y -= 4 * mm

    return y


def make_pdf():

    buffer = BytesIO()

    page_width, page_height = A4

    c = canvas.Canvas(
        buffer,
        pagesize=A4
    )

    accent = colors.HexColor("#FFC107")
    dark = colors.HexColor("#151515")

    sidebar_width = 70 * mm

    # Background
    c.setFillColor(colors.white)

    c.rect(
        0,
        0,
        page_width,
        page_height,
        fill=1,
        stroke=0
    )

    # Sidebar
    c.setFillColor(dark)

    c.rect(
        0,
        0,
        sidebar_width,
        page_height,
        fill=1,
        stroke=0
    )

    # Yellow geometric sidebar header
    path = c.beginPath()

    path.moveTo(
        0,
        page_height
    )

    path.lineTo(
        sidebar_width,
        page_height
    )

    path.lineTo(
        sidebar_width,
        page_height - 58 * mm
    )

    path.lineTo(
        31 * mm,
        page_height - 86 * mm
    )

    path.lineTo(
        0,
        page_height - 68 * mm
    )

    path.close()

    c.setFillColor(accent)

    c.drawPath(
        path,
        fill=1,
        stroke=0
    )

    # Main geometric top
    path2 = c.beginPath()

    path2.moveTo(
        page_width - 42 * mm,
        page_height
    )

    path2.lineTo(
        page_width,
        page_height
    )

    path2.lineTo(
        page_width,
        page_height - 30 * mm
    )

    path2.lineTo(
        page_width - 58 * mm,
        page_height - 30 * mm
    )

    path2.close()

    c.setFillColor(dark)

    c.drawPath(
        path2,
        fill=1,
        stroke=0
    )

    main_x = sidebar_width + 12 * mm

    main_width = (
        page_width
        - main_x
        - 12 * mm
    )

    y = page_height - 25 * mm

    name = (
        st.session_state.name.strip()
        or "YOUR NAME"
    ).upper()

    role = (
        st.session_state.role.strip()
        or "PROFESSIONAL TITLE"
    )

    c.setFillColor(dark)

    y = draw_wrapped(
        c,
        name,
        main_x,
        y,
        main_width,
        "Helvetica-Bold",
        21,
        9 * mm,
        dark,
        2
    )

    c.setFillColor(accent)

    c.setFont(
        "Helvetica-Bold",
        8.5
    )

    c.drawString(
        main_x,
        y - 2 * mm,
        role[:70]
    )

    y -= 16 * mm

    if st.session_state.summary.strip():

        c.setFillColor(dark)

        c.setFont(
            "Helvetica-Bold",
            12
        )

        c.drawString(
            main_x,
            y,
            "ABOUT ME"
        )

        y -= 3 * mm

        c.setStrokeColor(accent)

        c.setLineWidth(2)

        c.line(
            main_x,
            y,
            main_x + main_width,
            y
        )

        y -= 7 * mm

        y = draw_wrapped(
            c,
            st.session_state.summary,
            main_x,
            y,
            main_width,
            "Helvetica",
            7.5,
            3.6 * mm,
            colors.HexColor("#555555"),
            8
        )

        y -= 5 * mm

    y = draw_pdf_section(
        c,
        "Education",
        st.session_state.education,
        main_x,
        y,
        main_width,
        accent
    )

    y -= 2 * mm

    y = draw_pdf_section(
        c,
        "Experience",
        st.session_state.experience,
        main_x,
        y,
        main_width,
        accent
    )

    y -= 2 * mm

    y = draw_pdf_section(
        c,
        "Projects",
        st.session_state.projects,
        main_x,
        y,
        main_width,
        accent
    )

    # Sidebar content
    side_x = 8 * mm
    side_center = sidebar_width / 2

    photo_size = 47 * mm
    photo_x = side_center - photo_size / 2
    photo_y = page_height - 59 * mm

    if st.session_state.photo:

        try:

            img = Image.open(
                BytesIO(
                    st.session_state.photo
                )
            ).convert("RGB")

            img_buffer = BytesIO()

            img.save(
                img_buffer,
                format="JPEG",
                quality=95
            )

            img_buffer.seek(0)

            c.drawImage(
                ImageReader(img_buffer),
                photo_x,
                photo_y,
                width=photo_size,
                height=photo_size,
                preserveAspectRatio=True,
                anchor="c",
                mask="auto"
            )

        except Exception:
            pass

    side_y = page_height - 70 * mm

    c.setFillColor(colors.white)

    c.setFont(
        "Helvetica-Bold",
        9
    )

    c.drawCentredString(
        side_center,
        side_y,
        (
            st.session_state.name
            or "YOUR NAME"
        )[:28]
    )

    side_y -= 6 * mm

    c.setFillColor(accent)

    c.setFont(
        "Helvetica-Bold",
        6.8
    )

    c.drawCentredString(
        side_center,
        side_y,
        (
            st.session_state.role
            or "PROFESSIONAL TITLE"
        )[:38]
    )

    side_y -= 13 * mm

    c.setFillColor(accent)

    c.setFont(
        "Helvetica-Bold",
        8.5
    )

    c.drawString(
        side_x,
        side_y,
        "CONTACT"
    )

    side_y -= 6 * mm

    for value in [
        st.session_state.email,
        st.session_state.phone,
        st.session_state.location,
        st.session_state.linkedin,
        st.session_state.website
    ]:

        if value and value.strip():

            side_y = draw_wrapped(
                c,
                value,
                side_x,
                side_y,
                sidebar_width - 16 * mm,
                "Helvetica",
                6.5,
                3.2 * mm,
                colors.HexColor("#E5E7EB"),
                2
            )

            side_y -= 2 * mm

    parsed_skills = parse_skills(
        st.session_state.skills
    )

    if parsed_skills:

        side_y -= 4 * mm

        c.setFillColor(accent)

        c.setFont(
            "Helvetica-Bold",
            8.5
        )

        c.drawString(
            side_x,
            side_y,
            "SKILLS"
        )

        side_y -= 6 * mm

        track_width = sidebar_width - 16 * mm

        for skill_name, percent in parsed_skills[:8]:

            c.setFillColor(colors.white)

            c.setFont(
                "Helvetica",
                6.8
            )

            c.drawString(
                side_x,
                side_y,
                skill_name[:25]
            )

            c.setFillColor(
                colors.HexColor("#777777")
            )

            c.drawRightString(
                sidebar_width - 8 * mm,
                side_y,
                f"{percent}%"
            )

            side_y -= 3.5 * mm

            c.setFillColor(
                colors.HexColor("#444444")
            )

            c.roundRect(
                side_x,
                side_y,
                track_width,
                1.3 * mm,
                .7 * mm,
                fill=1,
                stroke=0
            )

            c.setFillColor(accent)

            c.roundRect(
                side_x,
                side_y,
                track_width * percent / 100,
                1.3 * mm,
                .7 * mm,
                fill=1,
                stroke=0
            )

            side_y -= 6 * mm

    if st.session_state.languages.strip():

        side_y -= 2 * mm

        c.setFillColor(accent)

        c.setFont(
            "Helvetica-Bold",
            8.5
        )

        c.drawString(
            side_x,
            side_y,
            "LANGUAGES"
        )

        side_y -= 6 * mm

        for line in st.session_state.languages.splitlines():

            if line.strip():

                side_y = draw_wrapped(
                    c,
                    "• " + line.strip(),
                    side_x,
                    side_y,
                    sidebar_width - 16 * mm,
                    "Helvetica",
                    6.8,
                    3.2 * mm,
                    colors.HexColor("#E5E7EB"),
                    2
                )

                side_y -= 1.5 * mm

    if st.session_state.certifications.strip():

        side_y -= 2 * mm

        c.setFillColor(accent)

        c.setFont(
            "Helvetica-Bold",
            8.5
        )

        c.drawString(
            side_x,
            side_y,
            "CERTIFICATIONS"
        )

        side_y -= 6 * mm

        for line in st.session_state.certifications.splitlines():

            if line.strip():

                side_y = draw_wrapped(
                    c,
                    "• " + line.strip(),
                    side_x,
                    side_y,
                    sidebar_width - 16 * mm,
                    "Helvetica",
                    6.8,
                    3.2 * mm,
                    colors.HexColor("#E5E7EB"),
                    2
                )

                side_y -= 1.5 * mm

    c.save()

    buffer.seek(0)

    return buffer.getvalue()


# =========================================================
# PDF DOWNLOAD
# =========================================================

st.divider()

st.markdown("### 📥 Download")

if st.button(
    "Generate Professional PDF",
    use_container_width=True
):

    try:

        pdf_data = make_pdf()

        filename = (
            st.session_state.name.strip()
            .replace(" ", "_")
            or "CV"
        ) + ".pdf"

        st.download_button(
            "⬇️ Download CV PDF",
            data=pdf_data,
            file_name=filename,
            mime="application/pdf",
            use_container_width=True
        )

    except Exception as exc:

        st.error(
            f"PDF generation failed: {exc}"
        )


st.markdown(
    '''
    <div style="
        text-align:center;
        color:#6b7280;
        padding:30px 0 10px;
        font-size:12px;
    ">
        CV Automator Premium • Modern Geometric CV Builder
    </div>
    ''',
    unsafe_allow_html=True
)
