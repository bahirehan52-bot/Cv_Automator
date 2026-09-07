import streamlit as st
from PIL import Image
from io import BytesIO
import base64
import html
import re

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image as RLImage
)


# =========================================================
# PAGE
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
    background: #080b12;
}

.block-container {
    max-width: 1500px;
    padding-top: 25px;
}


/* HEADER */

.hero {
    padding: 32px;
    border-radius: 24px;
    margin-bottom: 25px;

    background:
        radial-gradient(
            circle at 90% 20%,
            rgba(245,158,11,.18),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #101827,
            #172033
        );

    border: 1px solid #29354b;
}

.hero h1 {
    color: white;
    font-size: 42px;
    margin: 0;
}

.hero p {
    color: #9ca3af;
}


/* SIDEBAR */

section[data-testid="stSidebar"] {
    background: #0d1119;
}


/* BUTTONS */

.stButton button,
.stDownloadButton button {

    border-radius: 12px;
    min-height: 46px;
    font-weight: bold;
}


/* PREMIUM CARD */

.editor-card {

    background: #111827;

    border: 1px solid #253047;

    padding: 20px;

    border-radius: 18px;

    margin-bottom: 15px;
}


/* CV PREVIEW */

.cv-wrapper {

    background: #ffffff;

    width: 100%;

    min-height: 1100px;

    box-shadow:
        0 25px 80px
        rgba(0,0,0,.45);

    display: flex;

    border-radius: 8px;

    overflow: hidden;

    font-family:
        Arial,
        Helvetica,
        sans-serif;
}


/* LEFT SIDEBAR */

.cv-sidebar {

    width: 34%;

    background: #162132;

    color: white;

    padding: 32px 22px;
}


/* RIGHT SIDE */

.cv-main {

    width: 66%;

    background: #ffffff;

    color: #273142;

    padding: 38px 34px;
}


/* PHOTO */

.profile-photo {

    width: 130px;

    height: 130px;

    border-radius: 50%;

    object-fit: cover;

    display: block;

    margin:
        0 auto
        22px auto;

    border:
        5px solid
        #f59e0b;
}


/* NAME */

.cv-name {

    font-size: 30px;

    font-weight: 900;

    line-height: 1.1;

    color: #111827;

    text-transform: uppercase;
}


/* ROLE */

.cv-role {

    font-size: 13px;

    color: #f59e0b;

    font-weight: 700;

    margin-top: 8px;

    letter-spacing: 1px;
}


/* SIDEBAR NAME */

.sidebar-name {

    text-align: center;

    font-size: 21px;

    font-weight: 800;

    margin-bottom: 4px;
}


.sidebar-role {

    text-align: center;

    color: #f59e0b;

    font-size: 11px;

    margin-bottom: 28px;
}


/* SECTION TITLE */

.sidebar-section {

    margin-top: 28px;

    font-size: 11px;

    font-weight: 900;

    letter-spacing: 2px;

    color: #f59e0b;

    border-bottom:
        1px solid
        rgba(255,255,255,.2);

    padding-bottom: 8px;

    margin-bottom: 12px;
}


.main-section {

    font-size: 13px;

    font-weight: 900;

    letter-spacing: 2px;

    color: #162132;

    border-bottom:
        2px solid
        #f59e0b;

    padding-bottom: 7px;

    margin-top: 25px;

    margin-bottom: 14px;
}


/* TEXT */

.sidebar-text {

    font-size: 10px;

    line-height: 1.7;

    color: #d1d5db;

    margin-bottom: 8px;
}


.main-text {

    font-size: 10px;

    line-height: 1.7;

    color: #475569;
}


/* EXPERIENCE */

.experience-item {

    margin-bottom: 20px;
}


.experience-title {

    font-size: 12px;

    font-weight: 800;

    color: #111827;
}


.experience-meta {

    font-size: 9px;

    color: #f59e0b;

    margin:
        4px 0
        7px 0;

    font-weight: 700;
}


/* SKILLS */

.skill-item {

    margin-bottom: 14px;
}


.skill-name {

    font-size: 10px;

    color: #ffffff;

    margin-bottom: 5px;
}


.skill-track {

    width: 100%;

    height: 5px;

    background:
        rgba(255,255,255,.18);

    border-radius: 5px;

    overflow: hidden;
}


.skill-bar {

    height: 100%;

    background: #f59e0b;

    border-radius: 5px;
}


.score-card {

    background:
        linear-gradient(
            135deg,
            #111827,
            #1f2937
        );

    padding: 16px;

    border-radius: 15px;

    border:
        1px solid
        #29354b;

    margin-bottom: 15px;
}


.score-label {

    font-size: 10px;

    color: #9ca3af;

    letter-spacing: 1px;
}


.score-number {

    font-size: 30px;

    color: #f59e0b;

    font-weight: 900;
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

    return html.escape(text or "")


def parse_blocks(text):

    if not text.strip():

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

    if not content.strip():

        return ""

    result = f"""

    <div class="main-section">

        {title.upper()}

    </div>

    """


    for block in parse_blocks(content):

        result += '<div class="experience-item">'


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


def skill_html():

    if not st.session_state.skills.strip():

        return ""


    result = """

    <div class="sidebar-section">

        SKILLS

    </div>

    """


    lines = [

        x.strip()

        for x in st.session_state.skills.splitlines()

        if x.strip()
    ]


    for index, skill in enumerate(lines):

        # Example:
        # Python
        # Python | 90

        if "|" in skill:

            name, level = skill.split(
                "|",
                1
            )

            try:

                percent = int(
                    re.sub(
                        r"[^0-9]",
                        "",
                        level
                    )
                )

            except:

                percent = 75

        else:

            name = skill

            levels = [
                90,
                85,
                80,
                75,
                70,
                65
            ]

            percent = levels[
                index % len(levels)
            ]


        percent = max(
            0,
            min(
                100,
                percent
            )
        )


        result += f"""

        <div class="skill-item">

            <div class="skill-name">

                {esc(name)}

            </div>

            <div class="skill-track">

                <div
                    class="skill-bar"
                    style="width:{percent}%"
                ></div>

            </div>

        </div>

        """


    return result


# =========================================================
# HEADER
# =========================================================

st.markdown("""

<div class="hero">

    <h1>

        CV Automator
        <span style="color:#f59e0b">
            PREMIUM
        </span>

    </h1>

    <p>

        Premium dark sidebar •
        Profile photo •
        Live preview •
        PDF export

    </p>

</div>

""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR SETTINGS
# =========================================================

with st.sidebar:

    st.header("🎨 Premium Design")

    accent = st.color_picker(
        "Accent Color",
        "#F59E0B"
    )

    sidebar_color = st.color_picker(
        "Sidebar Color",
        "#162132"
    )

    st.divider()

    st.caption(
        "Premium Sidebar Template"
    )


# =========================================================
# LAYOUT
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

        "🧠 Profile",

        "💼 Experience",

        "🎓 Education",

        "🚀 Projects",

        "🛠 Skills",

        "📜 More"
    ])


    # -----------------------------------------------------
    # PERSONAL
    # -----------------------------------------------------

    with tabs[0]:

        st.markdown("### 📸 Profile Picture")

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


        if st.session_state.photo:

            st.image(

                st.session_state.photo,

                width=160
            )


            if st.button(
                "Remove Picture"
            ):

                st.session_state.photo = None

                st.rerun()


        st.divider()


        st.session_state.name = st.text_input(

            "Full Name",

            st.session_state.name,

            placeholder=
            "Muhammad Rehan Ahmed"
        )


        st.session_state.role = st.text_input(

            "Professional Title",

            st.session_state.role,

            placeholder=
            "Software Engineer"
        )


        st.session_state.email = st.text_input(

            "Email",

            st.session_state.email
        )


        st.session_state.phone = st.text_input(

            "Phone",

            st.session_state.phone
        )


        st.session_state.location = st.text_input(

            "Location",

            st.session_state.location
        )


        st.session_state.linkedin = st.text_input(

            "LinkedIn",

            st.session_state.linkedin
        )


        st.session_state.website = st.text_input(

            "Portfolio / Website",

            st.session_state.website
        )


    # -----------------------------------------------------
    # PROFILE
    # -----------------------------------------------------

    with tabs[1]:

        st.session_state.summary = st.text_area(

            "Professional Summary",

            st.session_state.summary,

            height=220,

            placeholder=
            "Motivated software engineering student..."
        )


    # -----------------------------------------------------
    # EXPERIENCE
    # -----------------------------------------------------

    with tabs[2]:

        st.session_state.experience = st.text_area(

            "Experience",

            st.session_state.experience,

            height=300,

            placeholder="""Software Developer | ABC Company | 2025-2026
2025 - 2026
Developed automation tools
Built web applications
Improved system performance

Freelance Developer | Self Employed
2024 - Present
Created websites
Worked with clients"""
        )


    # -----------------------------------------------------
    # EDUCATION
    # -----------------------------------------------------

    with tabs[3]:

        st.session_state.education = st.text_area(

            "Education",

            st.session_state.education,

            height=240
        )


    # -----------------------------------------------------
    # PROJECTS
    # -----------------------------------------------------

    with tabs[4]:

        st.session_state.projects = st.text_area(

            "Projects",

            st.session_state.projects,

            height=260
        )


    # -----------------------------------------------------
    # SKILLS
    # -----------------------------------------------------

    with tabs[5]:

        st.info(

            "Write one skill per line. "
            "Optional: Python | 90"
        )


        st.session_state.skills = st.text_area(

            "Skills",

            st.session_state.skills,

            height=250,

            placeholder="""Python | 90
C++ | 80
HTML | 95
CSS | 90
JavaScript | 75"""
        )


    # -----------------------------------------------------
    # MORE
    # -----------------------------------------------------

    with tabs[6]:

        st.session_state.languages = st.text_area(

            "Languages",

            st.session_state.languages,

            height=140
        )


        st.session_state.certifications = st.text_area(

            "Certifications",

            st.session_state.certifications,

            height=140
        )


# =========================================================
# PREVIEW
# =========================================================

with preview:

    st.markdown(
        "### 👁️ Premium Live Preview"
    )


    score_fields = [

        st.session_state.name,

        st.session_state.role,

        st.session_state.email,

        st.session_state.summary,

        st.session_state.skills,

        st.session_state.education,

        st.session_state.experience,

        st.session_state.projects
    ]


    score = round(

        sum(
            bool(
                x.strip()
            )

            for x in score_fields
        )

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

                {score}/100

            </div>

        </div>

        """,

        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # PHOTO
    # -----------------------------------------------------

    if st.session_state.photo:

        encoded = base64.b64encode(

            st.session_state.photo

        ).decode()


        photo_html = f"""

        <img
            class="profile-photo"
            src="data:image/jpeg;base64,{encoded}"
            style="border-color:{accent};"
        >

        """

    else:

        photo_html = f"""

        <div
            class="profile-photo"
            style="
                background:#27364d;
                border-color:{accent};
                display:flex;
                align-items:center;
                justify-content:center;
                font-size:50px;
            "
        >

            👤

        </div>

        """


    # -----------------------------------------------------
    # CONTACT
    # -----------------------------------------------------

    contact_html = ""


    contacts = [

        ("📧", st.session_state.email),

        ("📱", st.session_state.phone),

        ("📍", st.session_state.location),

        ("🔗", st.session_state.linkedin),

        ("🌐", st.session_state.website)
    ]


    for icon, value in contacts:

        if value.strip():

            contact_html += f"""

            <div class="sidebar-text">

                {icon}
                {esc(value)}

            </div>

            """


    # -----------------------------------------------------
    # LANGUAGES
    # -----------------------------------------------------

    languages_html = ""


    if st.session_state.languages.strip():

        languages_html = f"""

        <div class="sidebar-section">

            LANGUAGES

        </div>

        """


        for line in (
            st.session_state.languages
            .splitlines()
        ):

            if line.strip():

                languages_html += f"""

                <div class="sidebar-text">

                    {esc(line)}

                </div>

                """


    # -----------------------------------------------------
    # CERTIFICATIONS
    # -----------------------------------------------------

    cert_html = ""


    if st.session_state.certifications.strip():

        cert_html = f"""

        <div class="sidebar-section">

            CERTIFICATIONS

        </div>

        """


        for line in (
            st.session_state.certifications
            .splitlines()
        ):

            if line.strip():

                cert_html += f"""

                <div class="sidebar-text">

                    {esc(line)}

                </div>

                """


    # -----------------------------------------------------
    # FULL CV HTML
    # -----------------------------------------------------

    st.markdown(

        f"""

        <style>

        .cv-sidebar {{

            background:
            {sidebar_color};

        }}

        .skill-bar {{

            background:
            {accent};

        }}

        .sidebar-section {{

            color:
            {accent};

        }}

        .main-section {{

            border-color:
            {accent};

        }}

        .experience-meta {{

            color:
            {accent};

        }}

        .cv-role {{

            color:
            {accent};

        }}

        </style>


        <div class="cv-wrapper">


            <!-- LEFT -->

            <div class="cv-sidebar">


                {photo_html}


                <div class="sidebar-name">

                    {esc(st.session_state.name)
                    or "YOUR NAME"}

                </div>


                <div class="sidebar-role">

                    {esc(st.session_state.role)
                    or "PROFESSIONAL TITLE"}

                </div>


                <div class="sidebar-section">

                    CONTACT

                </div>


                {contact_html}


                {skill_html()}


                {languages_html}


                {cert_html}


            </div>


            <!-- RIGHT -->

            <div class="cv-main">


                <div class="cv-name">

                    {esc(st.session_state.name)
                    or "YOUR NAME"}

                