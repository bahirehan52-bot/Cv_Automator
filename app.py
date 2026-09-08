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


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="CV Automator Premium",
    page_icon="📄",
    layout="wide"
)


# =========================================================
# GLOBAL CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background: #0b0f16;
}

.block-container {
    max-width: 1500px;
    padding-top: 25px;
}


/* =====================================================
   HEADER
===================================================== */

.hero {
    padding: 32px;
    border-radius: 24px;
    margin-bottom: 25px;

    background:
        radial-gradient(
            circle at 90% 20%,
            rgba(255,193,7,.18),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #111827,
            #1f2937
        );

    border: 1px solid #2d3748;
}

.hero h1 {
    color: white;
    font-size: 42px;
    margin: 0;
}

.hero p {
    color: #9ca3af;
    font-size: 16px;
}


/* =====================================================
   SIDEBAR
===================================================== */

section[data-testid="stSidebar"] {
    background: #10141c;
}


/* =====================================================
   BUTTONS
===================================================== */

.stButton button,
.stDownloadButton button {

    border-radius: 12px;
    min-height: 48px;
    font-weight: 700;
}


/* =====================================================
   SCORE CARD
===================================================== */

.score-card {

    background:
        linear-gradient(
            135deg,
            #151b26,
            #232b3a
        );

    padding: 18px 22px;

    border-radius: 16px;

    border:
        1px solid
        #30394a;

    margin-bottom: 20px;
}


.score-label {

    color: #9ca3af;

    font-size: 11px;

    letter-spacing: 2px;

    font-weight: 700;
}


.score-number {

    color: #ffc107;

    font-size: 34px;

    font-weight: 900;
}


/* =====================================================
   CV WRAPPER
===================================================== */

.cv-wrapper {

    width: 100%;

    min-height: 1120px;

    background: white;

    display: flex;

    position: relative;

    overflow: hidden;

    box-shadow:
        0 25px 80px
        rgba(0,0,0,.55);

    font-family:
        Arial,
        Helvetica,
        sans-serif;
}


/* =====================================================
   LEFT SIDE
===================================================== */

.cv-sidebar {

    width: 36%;

    min-height: 1120px;

    background: #151515;

    color: white;

    padding: 28px 24px;

    position: relative;

    overflow: hidden;
}


.cv-sidebar::before {

    content: "";

    position: absolute;

    top: 0;

    left: 0;

    width: 100%;

    height: 270px;

    background: linear-gradient(
        135deg,
        #ffc107,
        #ff9800
    );

    clip-path:
        polygon(
            0 0,
            100% 0,
            100% 65%,
            45% 100%,
            0 75%
        );

    opacity: .95;
}


.cv-sidebar::after {

    content: "";

    position: absolute;

    bottom: 0;

    left: 0;

    width: 130px;

    height: 180px;

    background: #ffc107;

    clip-path:
        polygon(
            0 35%,
            100% 0,
            100% 100%,
            0 100%
        );
}


/* =====================================================
   PHOTO
===================================================== */

.profile-photo {

    width: 155px;

    height: 155px;

    border-radius: 50%;

    object-fit: cover;

    display: block;

    margin:
        10px auto
        28px auto;

    position: relative;

    z-index: 3;

    border:
        7px solid
        #151515;

    box-shadow:
        0 0 0 5px
        #ffc107;
}


/* =====================================================
   SIDEBAR NAME
===================================================== */

.sidebar-name {

    position: relative;

    z-index: 3;

    text-align: center;

    font-size: 22px;

    font-weight: 900;

    margin-top: 10px;

    color: white;
}


.sidebar-role {

    position: relative;

    z-index: 3;

    text-align: center;

    color: #ffc107;

    font-size: 11px;

    font-weight: 700;

    letter-spacing: 1px;

    margin-bottom: 30px;
}


/* =====================================================
   SIDEBAR SECTION
===================================================== */

.sidebar-section {

    position: relative;

    z-index: 3;

    margin-top: 30px;

    margin-bottom: 14px;

    font-size: 14px;

    font-weight: 900;

    letter-spacing: 1.5px;

    color: #ffc107;

    border-left:
        5px solid
        #ffc107;

    padding-left: 10px;
}


.sidebar-text {

    position: relative;

    z-index: 3;

    font-size: 11px;

    color: #e5e7eb;

    line-height: 1.7;

    margin-bottom: 9px;

    word-break: break-word;
}


/* =====================================================
   SKILLS
===================================================== */

.skill-item {

    position: relative;

    z-index: 3;

    margin-bottom: 15px;
}


.skill-name {

    color: white;

    font-size: 11px;

    margin-bottom: 6px;

    font-weight: 600;
}


.skill-track {

    width: 100%;

    height: 7px;

    background:
        rgba(255,255,255,.15);

    border-radius: 10px;

    overflow: hidden;
}


.skill-bar {

    height: 100%;

    background: #ffc107;

    border-radius: 10px;
}


/* =====================================================
   RIGHT SIDE
===================================================== */

.cv-main {

    width: 64%;

    min-height: 1120px;

    background:
        linear-gradient(
            135deg,
            #ffffff,
            #f2f3f5
        );

    color: #1b1b1b;

    padding: 55px 45px;

    position: relative;

    overflow: hidden;
}


/* TOP GEOMETRIC */

.cv-main::before {

    content: "";

    position: absolute;

    top: 0;

    right: 0;

    width: 300px;

    height: 110px;

    background: #151515;

    clip-path:
        polygon(
            20% 0,
            100% 0,
            100% 100%,
            0 100%
        );
}


.cv-main::after {

    content: "";

    position: absolute;

    right: 0;

    bottom: 0;

    width: 260px;

    height: 250px;

    background: #151515;

    clip-path:
        polygon(
            100% 0,
            100% 100%,
            0 100%
        );
}


/* =====================================================
   NAME
===================================================== */

.cv-name {

    position: relative;

    z-index: 2;

    font-size: 42px;

    font-weight: 900;

    color: #151515;

    text-transform: uppercase;

    letter-spacing: 1px;

    margin-top: 15px;
}


.cv-role {

    position: relative;

    z-index: 2;

    display: inline-block;

    margin-top: 8px;

    padding:
        7px 15px;

    background: #151515;

    color: #ffc107;

    font-size: 12px;

    font-weight: 800;

    letter-spacing: 1px;

    clip-path:
        polygon(
            0 0,
            100% 0,
            92% 100%,
            0 100%
        );
}


/* =====================================================
   MAIN SECTION
===================================================== */

.main-section {

    position: relative;

    z-index: 2;

    margin-top: 38px;

    margin-bottom: 18px;

    font-size: 22px;

    font-weight: 900;

    color: #151515;

    padding-bottom: 8px;

    border-bottom:
        4px solid
        #ffc107;
}


.main-text {

    position: relative;

    z-index: 2;

    color: #4b5563;

    font-size: 12px;

    line-height: 1.75;

    margin-bottom: 7px;
}


/* =====================================================
   EXPERIENCE
===================================================== */

.experience-item {

    position: relative;

    z-index: 2;

    border-left:
        3px solid
        #ffc107;

    padding-left: 18px;

    margin-bottom: 24px;
}


.experience-title {

    font-size: 14px;

    font-weight: 900;

    color: #151515;
}


.experience-meta {

    color: #b77900;

    font-size: 11px;

    font-weight: 800;

    margin:
        5px 0
        9px 0;
}


/* =====================================================
   SUMMARY
===================================================== */

.summary-box {

    position: relative;

    z-index: 2;

    color: #4b5563;

    font-size: 12px;

    line-height: 1.8;
}


@media (max-width: 850px) {

    .cv-wrapper {
        flex-direction: column;
    }

    .cv-sidebar,
    .cv-main {
        width: 100%;
    }

}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SESSION STATE
# =========================================================

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


# =========================================================
# FUNCTIONS
# =========================================================

def esc(text):

    return html.escape(str(text or ""))


def parse_blocks(text):

    if not text or not text.strip():
        return []

    return [
        [
            line.strip()
            for line in block.splitlines()
            if line.strip()
        ]
        for block in re.split(
            r"\n\s*\n",
            text.strip()
        )
        if block.strip()
    ]


def render_main_section(title, content):

    if not content or not content.strip():
        return ""

    result = f"""
    <div class="main-section">
        {esc(title.upper())}
    </div>
    """

    for block in parse_blocks(content):

        result += """
        <div class="experience-item">
        """

        for i, line in enumerate(block):

            if i == 0:

                result += f"""
                <div class="experience-title">
                    {esc(line)}
                </div>
                """

            elif i == 1:

                result += f"""
                <div class="experience-meta">
                    {esc(line)}
                </div>
                """

            else:

                clean = line.lstrip("-• ").strip()

                result += f"""
                <div class="main-text">
                    • {esc(clean)}
                </div>
                """

        result += "</div>"

    return result


def skill_html(accent):

    skills = st.session_state.skills

    if not skills or not skills.strip():
        return ""

    result = """
    <div class="sidebar-section">
        SKILLS
    </div>
    """

    lines = [
        x.strip()
        for x in skills.splitlines()
        if x.strip()
    ]

    default_levels = [
        90,
        85,
        80,
        75,
        70,
        65
    ]

    for index, skill in enumerate(lines):

        if "|" in skill:

            name, level = skill.split(
                "|",
                1
            )

            name = name.strip()

            numbers = re.sub(
                r"[^0-9]",
                "",
                level
            )

            try:
                percent = int(numbers)
            except:
                percent = 75

        else:

            name = skill

            percent = default_levels[
                index % len(default_levels)
            ]

        percent = max(
            0,
            min(100, percent)
        )

        result += f"""
        <div class="skill-item">

            <div class="skill-name">
                {esc(name)}
            </div>

            <div class="skill-track">

                <div
                    class="skill-bar"
                    style="
                        width:{percent}%;
                        background:{accent};
                    "
                ></div>

            </div>

        </div>
        """

    return result


def list_section(title, text):

    if not text or not text.strip():
        return ""

    result = f"""
    <div class="sidebar-section">
        {esc(title)}
    </div>
    """

    for line in text.splitlines():

        if line.strip():

            result += f"""
            <div class="sidebar-text">
                • {esc(line.strip())}
            </div>
            """

    return result


def make_pdf():

    buffer = BytesIO()

    page_width, page_height = A4

    c = canvas.Canvas(
        buffer,
        pagesize=A4
    )

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
    c.setFillColor(
        colors.HexColor("#151515")
    )

    sidebar_width = 70 * mm

    c.rect(
        0,
        0,
        sidebar_width,
        page_height,
        fill=1,
        stroke=0
    )

    # Yellow top shape
    c.setFillColor(
        colors.HexColor("#FFC107")
    )

    c.rect(
        0,
        page_height - 85 * mm,
        sidebar_width,
        85 * mm,
        fill=1,
        stroke=0
    )

    # Main area
    x = sidebar_width + 12 * mm
    y = page_height - 25 * mm

    # Name
    c.setFillColor(
        colors.HexColor("#151515")
    )

    c.setFont(
        "Helvetica-Bold",
        22
    )

    name = (
        st.session_state.name
        or "YOUR NAME"
    ).upper()

    c.drawString(
        x,
        y,
        name[:40]
    )

    y -= 11 * mm

    # Role
    c.setFillColor(
        colors.HexColor("#B77900")
    )

    c.setFont(
        "Helvetica-Bold",
        9
    )

    role = (
        st.session_state.role
        or "PROFESSIONAL TITLE"
    )

    c.drawString(
        x,
        y,
        role[:70]
    )

    y -= 18 * mm

    # Summary
    if st.session_state.summary.strip():

        c.setFillColor(
            colors.HexColor("#151515")
        )

        c.setFont(
            "Helvetica-Bold",
            14
        )

        c.drawString(
            x,
            y,
            "ABOUT ME"
        )

        y -= 8 * mm

        c.setFont(
            "Helvetica",
            8
        )

        c.setFillColor(
            colors.HexColor("#555555")
        )

        text = c.beginText(
            x,
            y
        )

        text.setLeading(12)

        words = st.session_state.summary.split()

        line = ""

        for word in words:

            test = (
                line + " " + word
            ).strip()

            if len(test) > 75:

                text.textLine(line)

                line = word

            else:
                line = test

        if line:
            text.textLine(line)

        c.drawText(text)

        y -= 45 * mm

    # Sections
    sections = [
        (
            "EDUCATION",
            st.session_state.education
        ),
        (
            "EXPERIENCE",
            st.session_state.experience
        ),
        (
            "PROJECTS",
            st.session_state.projects
        )
    ]

    for title, content in sections:

        if not content.strip():
            continue

        if y < 40 * mm:

            c.showPage()

            y = page_height - 25 * mm

        c.setFillColor(
            colors.HexColor("#151515")
        )

        c.setFont(
            "Helvetica-Bold",
            14
        )

        c.drawString(
            x,
            y,
            title
        )

        y -= 8 * mm

        for block in parse_blocks(content):

            for i, line in enumerate(block):

                if y < 25 * mm:

                    c.showPage()

                    y = page_height - 25 * mm

                if i == 0:

                    c.setFont(
                        "Helvetica-Bold",
                        9
                    )

                    c.setFillColor(
                        colors.HexColor("#151515")
                    )

                elif i == 1:

                    c.setFont(
                        "Helvetica-Bold",
                        8
                    )

                    c.setFillColor(
                        colors.HexColor("#B77900")
                    )

                else:

                    c.setFont(
                        "Helvetica",
                        8
                    )

                    c.setFillColor(
                        colors.HexColor("#555555")
                    )

                c.drawString(
                    x + 4 * mm,
                    y,
                    line[:90]
                )

                y -= 5 * mm

            y -= 4 * mm

        y -= 4 * mm

    # =====================================================
    # SIDEBAR CONTENT
    # =====================================================

    side_x = 8 * mm
    side_y = page_height - 100 * mm

    # Photo
    if st.session_state.photo:

        try:

            image = Image.open(
                BytesIO(
                    st.session_state.photo
                )
            )

            image.thumbnail(
                (55 * mm, 55 * mm)
            )

            img_buffer = BytesIO()

            image.save(
                img_buffer,
                format="JPEG"
            )

            img_buffer.seek(0)

            c.drawImage(
                ImageReader(img_buffer),
                8 * mm,
                page_height - 78 * mm,
                width=54 * mm,
                height=54 * mm,
                preserveAspectRatio=True,
                mask="auto"
            )

        except:
            pass

    # Sidebar text
    c.setFillColor(
        colors.white
    )

    c.setFont(
        "Helvetica-Bold",
        9
    )

    sidebar_name = (
        st.session_state.name
        or "YOUR NAME"
    )

    c.drawCentredString(
        sidebar_width / 2,
        side_y,
        sidebar_name[:30]
    )

    side_y -= 7 * mm

    c.setFillColor(
        colors.HexColor("#FFC107")
    )

    c.setFont(
        "Helvetica-Bold",
        7
    )

    c.drawCentredString(
        sidebar_width / 2,
        side_y,
        (
            st.session_state.role
            or "PROFESSIONAL TITLE"
        )[:40]
    )

    side_y -= 16 * mm

    # Contact
    contacts = [
        st.session_state.email,
        st.session_state.phone,
        st.session_state.location,
        st.session_state.linkedin,
        st.session_state.website
    ]

    c.setFillColor(
        colors.HexColor("#FFC107")
    )

    c.setFont(
        "Helvetica-Bold",
        10
    )

    c.drawString(
        side_x,
        side_y,
        "CONTACT"
    )

    side_y -= 7 * mm

    c.setFillColor(
        colors.white
    )

    c.setFont(
        "Helvetica",
        7
    )

    for contact in contacts:

        if contact.strip():

            c.drawString(
                side_x,
                side_y,
                contact[:40]
            )

            side_y -= 6 * mm

    # Skills
    if st.session_state.skills.strip():

        side_y -= 6 * mm

        c.setFillColor(
            colors.HexColor("#FFC107")
        )

        c.setFont(
            "Helvetica-Bold",
            10
        )

        c.drawString(
            side_x,
            side_y,
            "SKILLS"
        )

        side_y -= 7 * mm

        skill_lines = [
            x.strip()
            for x in st.session_state.skills.splitlines()
            if x.strip()
        ]

        for skill in skill_lines:

            if "|" in skill:
                skill_name, skill_level = skill.split(
                    "|",
                    1
                )

                skill_name = skill_name.strip()

            else:
                skill_name = skill.strip()

            if side_y < 20 * mm:
                break

            c.setFillColor(
                colors.white
            )

            c.setFont(
                "Helvetica",
                7
            )

            c.drawString(
                side_x,
                side_y,
                skill_name[:28]
            )

            side_y -= 5 * mm


    # Languages
    if (
        st.session_state.languages
        and st.session_state.languages.strip()
        and side_y > 25 * mm
    ):

        side_y -= 5 * mm

        c.setFillColor(
            colors.HexColor("#FFC107")
        )

        c.setFont(
            "Helvetica-Bold",
            10
        )

        c.drawString(
            side_x,
            side_y,
            "LANGUAGES"
        )

        side_y -= 7 * mm

        c.setFillColor(
            colors.white
        )

        c.setFont(
            "Helvetica",
            7
        )

        for language in (
            st.session_state.languages
            .splitlines()
        ):

            language = language.strip()

            if not language:
                continue

            if side_y < 20 * mm:
                break

            c.drawString(
                side_x,
                side_y,
                language[:30]
            )

            side_y -= 5 * mm


    # Certifications
    if (
        st.session_state.certifications
        and st.session_state.certifications.strip()
        and side_y > 25 * mm
    ):

        side_y -= 5 * mm

        c.setFillColor(
            colors.HexColor("#FFC107")
        )

        c.setFont(
            "Helvetica-Bold",
            10
        )

        c.drawString(
            side_x,
            side_y,
            "CERTIFICATIONS"
        )

        side_y -= 7 * mm

        c.setFillColor(
            colors.white
        )

        c.setFont(
            "Helvetica",
            7
        )

        for certification in (
            st.session_state.certifications
            .splitlines()
        ):

            certification = certification.strip()

            if not certification:
                continue

            if side_y < 20 * mm:
                break

            c.drawString(
                side_x,
                side_y,
                certification[:30]
            )

            side_y -= 5 * mm


    # Save PDF

    c.save()

    buffer.seek(0)

    return buffer.getvalue()


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div class="hero">

        <h1>
            CV Automator
            <span style="color:#ffc107;">
                PREMIUM
            </span>
        </h1>

        <p>
            Professional CV Builder • Live Preview • Profile Photo • PDF Export
        </p>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# DESIGN SETTINGS
# =========================================================

with st.sidebar:

    st.header(
        "🎨 Design Settings"
    )

    accent = st.color_picker(
        "Accent Color",
        "#FFC107"
    )

    sidebar_color = st.color_picker(
        "Sidebar Color",
        "#151515"
    )

    st.divider()

    st.markdown(
        "### 📄 CV Style"
    )

    st.caption(
        "Modern Professional Geometric Template"
    )


# =========================================================
# MAIN LAYOUT
# =========================================================

editor, preview = st.columns(
    [0.9, 1.1],
    gap="large"
)


# =========================================================
# EDITOR
# =========================================================

with editor:

    st.markdown(
        "## ✏️ CV Editor"
    )

    tabs = st.tabs([
        "👤 Personal",
        "🧠 Profile",
        "💼 Experience",
        "🎓 Education",
        "🚀 Projects",
        "🛠 Skills",
        "📜 More"
    ])


    # =====================================================
    # PERSONAL
    # =====================================================

    with tabs[0]:

        st.markdown(
            "### 📸 Profile Picture"
        )

        uploaded = st.file_uploader(
            "Upload Profile Picture",
            type=[
                "jpg",
                "jpeg",
                "png",
                "webp"
            ]
        )

        if uploaded:

            try:

                image = Image.open(
                    uploaded
                ).convert(
                    "RGB"
                )

                buffer = BytesIO()

                image.save(
                    buffer,
                    format="JPEG",
                    quality=95
                )

                st.session_state.photo = (
                    buffer.getvalue()
                )

            except Exception as error:

                st.error(
                    f"Image Error: {error}"
                )


        if st.session_state.photo:

            st.image(
                st.session_state.photo,
                width=160
            )

            if st.button(
                "🗑 Remove Picture"
            ):

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
            placeholder="example@email.com"
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
            value=st.session_state.linkedin
        )


        st.session_state.website = st.text_input(
            "Portfolio / Website",
            value=st.session_state.website
        )


    # =====================================================
    # PROFILE
    # =====================================================

    with tabs[1]:

        st.session_state.summary = st.text_area(
            "Professional Summary",
            value=st.session_state.summary,
            height=220,
            placeholder=(
                "Write a short professional introduction "
                "about yourself, your skills and your goals..."
            )
        )


    # =====================================================
    # EXPERIENCE
    # =====================================================

    with tabs[2]:

        st.info(
            "Format: First line = Job Title, "
            "Second line = Date/Company, "
            "Remaining lines = Details. "
            "Separate jobs with an empty line."
        )

        st.session_state.experience = st.text_area(
            "Experience",
            value=st.session_state.experience,
            height=320,
            placeholder="""Software Developer | ABC Company
2025 - Present
Developed automation tools
Built web applications
Improved system performance

Freelance Developer
2024 - Present
Created websites
Worked with clients"""
        )


    # =====================================================
    # EDUCATION
    # =====================================================

    with tabs[3]:

        st.info(
            "Separate each education entry "
            "with an empty line."
        )

        st.session_state.education = st.text_area(
            "Education",
            value=st.session_state.education,
            height=260,
            placeholder="""BS Software Engineering
2025 - Present
University Name
Relevant coursework and achievements"""
        )


    # =====================================================
    # PROJECTS
    # =====================================================

    with tabs[4]:

        st.session_state.projects = st.text_area(
            "Projects",
            value=st.session_state.projects,
            height=280,
            placeholder="""CV Automator
2026
Built a professional CV generator
Added live preview and PDF export

AI Study Assistant
2026
Created an AI based student helper"""
        )


    # =====================================================
    # SKILLS
    # =====================================================

    with tabs[5]:

        st.info(
            "One skill per line.\n\n"
            "Optional percentage format:\n"
            "Python | 90"
        )

        st.session_state.skills = st.text_area(
            "Skills",
            value=st.session_state.skills,
            height=260,
            placeholder="""Python | 90
C++ | 80
HTML | 95
CSS | 90
JavaScript | 75"""
        )


    # =====================================================
    # MORE
    # =====================================================

    with tabs[6]:

        st.session_state.languages = st.text_area(
            "Languages",
            value=st.session_state.languages,
            height=150,
            placeholder="""English
Urdu"""
        )


        st.session_state.certifications = st.text_area(
            "Certifications",
            value=st.session_state.certifications,
            height=150,
            placeholder="""Python Certification
Web Development Certificate"""
        )


# =========================================================
# PREVIEW
# =========================================================

with preview:

    st.markdown(
        "## 👁️ Live CV Preview"
    )


    # =====================================================
    # COMPLETENESS SCORE
    # =====================================================

    score_fields = [
        st.session_state.name,
        st.session_state.role,
        st.session_state.email,
        st.session_state.summary,
        st.session_state.education,
        st.session_state.experience,
        st.session_state.projects,
        st.session_state.skills
    ]

    completed = sum(
        1
        for item in score_fields
        if item and item.strip()
    )

    score = round(
        completed
        /
        len(score_fields)
        *
        100
    )


    st.markdown(
        f"""
        <div class="score-card">

            <div class="score-label">
                CV COMPLETENESS
            </div>

            <div class="score-number">
                {score}%
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # =====================================================
    # PHOTO HTML
    # =====================================================

    if st.session_state.photo:

        encoded = base64.b64encode(
            st.session_state.photo
        ).decode()

        photo_html = f"""
        <img
            class="profile-photo"
            src="data:image/jpeg;base64,{encoded}"
            style="
                box-shadow:
                    0 0 0 5px {accent};
            "
        >
        """

    else:

        photo_html = f"""
        <div
            class="profile-photo"
            style="
                background:#2b2b2b;
                display:flex;
                align-items:center;
                justify-content:center;
                font-size:60px;
                color:white;
                box-shadow:
                    0 0 0 5px {accent};
            "
        >
            👤
        </div>
        """


    # =====================================================
    # CONTACT
    # =====================================================

    contact_html = ""

    contacts = [
        ("✉", st.session_state.email),
        ("☎", st.session_state.phone),
        ("⌖", st.session_state.location),
        ("in", st.session_state.linkedin),
        ("◉", st.session_state.website)
    ]

    for icon, value in contacts:

        if value and value.strip():

            contact_html += f"""
            <div class="sidebar-text">
                <b>{icon}</b> {esc(value)}
            </div>
            """


    # =====================================================
    # FULL HTML
    # =====================================================

    cv_html = f"""

    <style>

        .cv-sidebar {{
            background:{sidebar_color};
        }}

        .cv-sidebar::before {{
            background:
                linear-gradient(
                    135deg,
                    {accent},
                    #ff9800
                );
        }}

        .cv-sidebar::after {{
            background:{accent};
        }}

        .profile-photo {{
            box-shadow:
                0 0 0 5px {accent};
        }}

        .sidebar-role {{
            color:{accent};
        }}

        .sidebar-section {{
            color:{accent};
            border-left-color:{accent};
        }}

        .skill-bar {{
            background:{accent};
        }}

        .main-section {{
            border-bottom-color:{accent};
        }}

        .experience-item {{
            border-left-color:{accent};
        }}

        .cv-role {{
            color:{accent};
        }}

    </style>


    <div class="cv-wrapper">


        <!-- SIDEBAR -->

        <div class="cv-sidebar">

            {photo_html}


            <div class="sidebar-name">

                {esc(st.session_state.name) or "YOUR NAME"}

            </div>


            <div class="sidebar-role">

                {esc(st.session_state.role) or "PROFESSIONAL TITLE"}

            </div>


            <div class="sidebar-section">

                CONTACT

            </div>


            {contact_html}


            {skill_html(accent)}


            {list_section(
                "LANGUAGES",
                st.session_state.languages
            )}


            {list_section(
                "CERTIFICATIONS",
                st.session_state.certifications
            )}


        </div>


        <!-- MAIN -->

        <div class="cv-main">


            <div class="cv-name">

                {esc(st.session_state.name) or "YOUR NAME"}

            </div>


            <div
                class="cv-role"
                style="
                    color:{accent};
                "
            >

                {esc(st.session_state.role) or "PROFESSIONAL TITLE"}

        c.drawString(
            side_x,
            side_y,
            "SKILLS"
        )

        side_y -= 7 * mm

        c.setFillColor(colors.white)
        c.setFont(
            "Helvetica",
            8
        )

        skill_lines = [
            x.strip()
            for x in st.session_state.skills.splitlines()
            if x.strip()
        ]

        for skill in skill_lines:

            if "|" in skill:
                skill_name = skill.split(
                    "|",
                    1
                )[0].strip()
            else:
                skill_name = skill.strip()

            if side_y < 20 * mm:
                break

            c.drawString(
                side_x,
                side_y,
                skill_name[:35]
            )

            side_y -= 6 * mm


    # Languages
    if st.session_state.languages.strip():

        side_y -= 6 * mm

        if side_y > 30 * mm:

            c.setFillColor(
                colors.HexColor("#FFC107")
            )

            c.setFont(
                "Helvetica-Bold",
                10
            )

            c.drawString(
                side_x,
                side_y,
                "LANGUAGES"
            )

            side_y -= 7 * mm

            c.setFillColor(
                colors.white
            )

            c.setFont(
                "Helvetica",
                8
            )

            for language in st.session_state.languages.splitlines():

                language = language.strip()

                if not language:
                    continue

                if side_y < 20 * mm:
                    break

                c.drawString(
                    side_x,
                    side_y,
                    language[:35]
                )

                side_y -= 6 * mm


    # Certifications
    if st.session_state.certifications.strip():

        side_y -= 6 * mm

        if side_y > 30 * mm:

            c.setFillColor(
                colors.HexColor("#FFC107")
            )

            c.setFont(
                "Helvetica-Bold",
                10
            )

            c.drawString(
                side_x,
                side_y,
                "CERTIFICATIONS"
            )

            side_y -= 7 * mm

            c.setFillColor(
                colors.white
            )

            c.setFont(
                "Helvetica",
                8
            )

            for certification in (
                st.session_state.certifications
                .splitlines()
            ):

                certification = certification.strip()

                if not certification:
                    continue

                if side_y < 20 * mm:
                    break

                c.drawString(
                    side_x,
                    side_y,
                    certification[:35]
                )

                side_y -= 6 * mm


    c.save()

    buffer.seek(0)

    return buffer.getvalue()


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="hero">'
    '<h1>CV Automator <span style="color:#ffc107;">PREMIUM</span></h1>'
    '<p>Modern geometric CV - Profile photo - Live preview - Professional PDF export</p>'
    '</div>',
    unsafe_allow_html=True
)

# =========================================================
# SIDEBAR SETTINGS
# =========================================================

with st.sidebar:

    st.header(
        "🎨 CV Design"
    )

    accent = st.color_picker(
        "Accent Color",
        "#FFC107"
    )

    sidebar_color = st.color_picker(
        "Sidebar Color",
        "#151515"
    )

    st.divider()

    st.caption(
        "Modern Professional Template"
    )


# =========================================================
# MAIN LAYOUT
# =========================================================

editor, preview = st.columns(
    [0.85, 1.15],
    gap="large"
)


# =========================================================
# EDITOR
# =========================================================

with editor:

    tabs = st.tabs([
        "👤 Personal",
        "🧠 About",
        "💼 Experience",
        "🎓 Education",
        "🚀 Projects",
        "🛠 Skills",
        "📜 More"
    ])


    # PERSONAL
    with tabs[0]:

        st.subheader(
            "Profile Picture"
        )

        uploaded = st.file_uploader(
            "Upload Picture",
            type=[
                "jpg",
                "jpeg",
                "png",
                "webp"
            ]
        )

        if uploaded:

            try:

                image = Image.open(
                    uploaded
                ).convert(
                    "RGB"
                )

                buffer = BytesIO()

                image.save(
                    buffer,
                    format="JPEG",
                    quality=95
                )

                st.session_state.photo = (
                    buffer.getvalue()
                )

            except Exception as e:

                st.error(
                    f"Image error: {e}"
                )


        if st.session_state.photo:

            st.image(
                st.session_state.photo,
                width=160
            )

            if st.button(
                "🗑 Remove Picture"
            ):

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
            value=st.session_state.email
        )


        st.session_state.phone = st.text_input(
            "Phone",
            value=st.session_state.phone
        )


        st.session_state.location = st.text_input(
            "Location",
            value=st.session_state.location
        )


        st.session_state.linkedin = st.text_input(
            "LinkedIn",
            value=st.session_state.linkedin
        )


        st.session_state.website = st.text_input(
            "Portfolio / Website",
            value=st.session_state.website
        )


    # ABOUT
    with tabs[1]:

        st.session_state.summary = st.text_area(
            "Professional Summary",
            value=st.session_state.summary,
            height=250,
            placeholder=(
                "Write a short professional introduction "
                "about yourself..."
            )
        )


    # EXPERIENCE
    with tabs[2]:

        st.caption(
            "Separate each experience with a blank line."
        )

        
    st.session_state.experience = st.text_area(
    "Experience",
    value=st.session_state.experience,
    height=350,
    placeholder=(
        "Software Developer | ABC Company\n"
        "2025 - Present\n"
        "Developed automation tools\n"
        "Built modern web applications\n"
        "Improved system performance\n"
        "\n"
        "Freelance Developer\n"
        "2024 - Present\n"
        "Created professional websites\n"
        "Worked with multiple clients"
    )
)


    # EDUCATION
    with tabs[3]:

        st.caption(
            "Separate each education entry with a blank line."
        )

        st.session_state.education = st.text_area(
            "Education",
            value=st.session_state.education,
            height=300,
            placeholder=(
    "BS Software Engineering | University Name\n"
    "2025 - Present\n"
    "Relevant coursework and achievements\n"
    "\n"
    "FSc Pre-Medical | College Name\n"
    "2023 - 2025\n"
    "Science and academic achievements"
)


    # PROJECTS
    with tabs[4]:

        st.caption(
            "Separate each project with a blank line."
        )

        st.session_state.projects = st.text_area(
            "Projects",
            value=st.session_state.projects,
            height=320,
            placeholder=(
    "CV Automator\n"
    "Python | Streamlit\n"
    "Built an automated professional CV generator\n"
    "\n"
    "AI Study Assistant\n"
    "Python | AI\n"
    "Created a personalized student study planner"
)


    # SKILLS
    with tabs[5]:

        st.info(
            "One skill per line. "
            "Optional format: Python | 90"
        )

        st.session_state.skills = st.text_area(
            "Skills",
            value=st.session_state.skills,
            height=280,
            placeholder=(
    "Python | 90\n"
    "C++ | 80\n"
    "HTML | 95\n"
    "CSS | 90\n"
    "JavaScript | 75"
)
        )


    # MORE
    with tabs[6]:

        st.session_state.languages = st.text_area(
            "Languages",
            value=st.session_state.languages,
            height=150,
            placeholder="""English
Urdu"""
        )


        st.session_state.certifications = st.text_area(
            "Certifications",
            value=st.session_state.certifications,
            height=150,
            placeholder="Python Programming\n"
"Web Development"
        )


# =========================================================
# PREVIEW
# =========================================================

with preview:

    st.markdown(
        "### 👁️ Live CV Preview"
    )


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
        bool(
            field.strip()
        )
        for field in score_fields
    )


    score = round(
        completed
        /
        len(score_fields)
        *
        100
    )


    st.markdown(
    f"""
    <div class="score-card">

        <div class="score-label">
            CV COMPLETENESS
        </div>

        <div
            class="score-number"
            style="color:{accent};"
        >
            {score}/100
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


    # PHOTO
    # =========================================================
# PHOTO
# =========================================================

if st.session_state.photo:

    encoded = base64.b64encode(
        st.session_state.photo
    ).decode("utf-8")

    photo_html = f'''
    <img
        class="profile-photo"
        src="data:image/jpeg;base64,{encoded}"
        style="box-shadow: 0 0 0 5px {accent};"
    >
    '''

else:

    photo_html = f'''
    <div
        class="profile-photo"
        style="
            background: #2a2a2a;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 55px;
            box-shadow: 0 0 0 5px {accent};
        "
    >
        &#128100;
    </div>
    '''


contact_html = ''

contacts = [
    ('Email:', st.session_state.email),
    ('Phone:', st.session_state.phone),
    ('Location:', st.session_state.location),
    ('LinkedIn:', st.session_state.linkedin),
    ('Website:', st.session_state.website)
]

for icon, value in contacts:

    if value and value.strip():

        contact_html += f'''
        <div class="sidebar-text">
            <strong>{esc(icon)}</strong>
            {esc(value)}
        </div>
        '''


    # MAIN SECTIONS
    summary_html = ""

    if st.session_state.summary.strip():

        summary_html = f"""
        <div class="main-section">
            ABOUT ME
        </div>

        <div class="summary-box">
            {esc(st.session_state.summary)}
        </div>
        """


    education_html = render_main_section(
        "Education",
        st.session_state.education
    )


    experience_html = render_main_section(
        "Experience",
        st.session_state.experience
    )


    projects_html = render_main_section(
        "Projects",
        st.session_state.projects
    )


    languages_html = list_section(
        "Languages",
        st.session_state.languages
    )


    certifications_html = list_section(
        "Certifications",
        st.session_state.certifications
    )

# FULL CV
cv_html = f"""
<style>

.cv-sidebar {{
    background: {sidebar_color};
}}

.cv-sidebar::before {{
    background: linear-gradient(
        135deg,
        {accent},
        #ff9800
    );
}}

.cv-sidebar::after {{
    background: {accent};
}}

.sidebar-role,
.sidebar-section {{
    color: {accent};
}}

.sidebar-section {{
    border-left-color: {accent};
}}

.skill-bar {{
    background: {accent};
}}

.main-section {{
    border-bottom-color: {accent};
}}

.experience-item {{
    border-left-color: {accent};
}}

.experience-meta {{
    color: {accent};
}}

.cv-role {{
    color: {accent};
}}

</style>

<div class="cv-wrapper">

    <!-- LEFT SIDEBAR -->

    <div class="cv-sidebar">

        {photo_html}

        <div class="sidebar-name">
            {esc(st.session_state.name) or "YOUR NAME"}
        </div>

        <div class="sidebar-role">
            {esc(st.session_state.role) or "PROFESSIONAL TITLE"}
        </div>

        <div class="sidebar-section">
            CONTACT
        </div>

        {contact_html}

        {skill_html(accent)}

        {languages_html}

        {certifications_html}

    </div>

    <!-- RIGHT SIDE -->

    <div class="cv-main">

        <div class="cv-name">
            {esc(st.session_state.name) or "YOUR NAME"}
        </div>

        <div class="cv-role">
            {esc(st.session_state.role) or "PROFESSIONAL TITLE"}
        </div>

        {summary_html}

        {education_html}

        {experience_html}

        {projects_html}

    </div>

</div>
"""

st.markdown(
    cv_html,
    unsafe_allow_html=True
)

st.divider()
    # =====================================================
    # PDF DOWNLOAD
    # =====================================================

    st.markdown(
        "### 📥 Download"
    )


    if st.button(
        "Generate Professional PDF",
        use_container_width=True
    ):

        try:

            pdf_data = make_pdf()

            st.download_button(
                label="⬇️ Download CV PDF",
                data=pdf_data,
                file_name=(
                    st.session_state.name
                    .strip()
                    .replace(" ", "_")
                    or "CV"
                ) + ".pdf",
                mime="application/pdf",
                use_container_width=True
            )

        except Exception as e:

            st.error(
                f"PDF generation failed: {e}"
            )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div style="
        text-align:center;
        color:#6b7280;
        padding:30px 0 10px 0;
        font-size:13px;
    ">
        CV Automator Premium
        • Modern CV Builder
    </div>
    """,
    unsafe_allow_html=True
)
