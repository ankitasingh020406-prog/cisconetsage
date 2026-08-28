import streamlit as st
import pandas as pd
from pathlib import Path
from openai import OpenAI

from diagnosis import ai_diagnose, demo_diagnose
from checker import check_diagnosis
st.set_page_config(page_title="NetSage AI", page_icon="🌐", layout="wide")


st.markdown("""
<style>

    /* =========================================================
       NETSAGE AI — BLACK + GREEN THEME
       ========================================================= */

    :root {
    --bg: #030303;
    --bg-soft: #080808;
    --card: #0d0d0d;
    --card-hover: #151515;

    --red: #ff2b2b;
    --red-bright: #ff4b4b;
    --red-dark: #9e1111;
    --red-soft: rgba(255, 43, 43, 0.10);
    --red-border: rgba(255, 43, 43, 0.28);

    --green: #00e676;
    --green-bright: #39ff88;
    --green-dark: #00a844;
    --green-soft: rgba(0, 230, 118, 0.10);
    --green-border: rgba(0, 230, 118, 0.22);

    --text: #f5f5f5;
    --text-soft: #c2c2c2;
    --text-muted: #777777;

    --warning: #ffd166;
}


    /* ---------- GLOBAL APP ---------- */

    .stApp {
        background:
            radial-gradient(
                circle at 15% 5%,
                rgba(0, 255, 102, 0.08),
                transparent 28%
            ),
            radial-gradient(
                circle at 90% 15%,
                rgba(0, 255, 102, 0.045),
                transparent 25%
            ),
            linear-gradient(
                135deg,
                #020402 0%,
                #050805 45%,
                #030603 100%
            );

        color: var(--text);
    }


    /* ---------- MAIN CONTENT ---------- */

    .main .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }


    /* ---------- HEADINGS ---------- */

    h1 {
    font-size: 3rem !important;
    font-weight: 900 !important;
    letter-spacing: -1.5px;

    background: linear-gradient(
        90deg,
        #ffffff 0%,
        #ffffff 35%,
        var(--red-bright) 65%,
        var(--green-bright) 100%
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    text-shadow: 0 0 30px rgba(255, 43, 43, 0.08);
}


    h2 {
        color: #effff4 !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px;
    }


    h3 {
        color: var(--green-bright) !important;
        font-weight: 700 !important;
    }


    p,
    label {
        color: var(--text-soft) !important;
    }


    /* ---------- CAPTION ---------- */

    .stCaption {
        color: #718c7b !important;
        font-size: 1rem !important;
    }


    /* =========================================================
       CARDS / CONTAINERS
       ========================================================= */

    div[data-testid="stVerticalBlock"] > div:has(
        div[data-testid="stMetric"]
    ) {

        background: rgba(7, 12, 8, 0.82);

        border: 1px solid var(--green-border);

        border-radius: 18px;

        backdrop-filter: blur(18px);

        box-shadow:
            0 12px 35px rgba(0, 0, 0, 0.45);
    }


    /* =========================================================
       METRICS
       ========================================================= */

    div[data-testid="stMetric"] {

        background:
            linear-gradient(
                145deg,
                rgba(13, 20, 14, 0.95),
                rgba(5, 10, 6, 0.95)
            );

        border: 1px solid rgba(0, 255, 102, 0.18);

        padding: 18px;

        border-radius: 16px;

        box-shadow:
            inset 0 1px rgba(255,255,255,0.025),
            0 10px 30px rgba(0, 0, 0, 0.35);

        transition: all 0.2s ease;
    }


    div[data-testid="stMetric"]:hover {

        border-color: rgba(0, 255, 102, 0.42);

        box-shadow:
            0 0 25px rgba(0, 255, 102, 0.08),
            0 12px 35px rgba(0, 0, 0, 0.45);

        transform: translateY(-2px);
    }


    div[data-testid="stMetricLabel"] {
        color: #718078 !important;
        font-weight: 600 !important;
    }


    div[data-testid="stMetricValue"] {

        color: var(--green-bright) !important;

        font-weight: 850 !important;

        text-shadow:
            0 0 18px rgba(0, 255, 102, 0.16);
    }


    /* =========================================================
       SIDEBAR
       ========================================================= */

    section[data-testid="stSidebar"] {

        background:
            linear-gradient(
                180deg,
                #070b08 0%,
                #030603 100%
            );

        border-right:
            1px solid rgba(0, 255, 102, 0.16);

        box-shadow:
            8px 0 35px rgba(0, 0, 0, 0.35);
    }


    section[data-testid="stSidebar"] h2 {

        color: var(--green-bright) !important;

        font-weight: 800 !important;
    }


    section[data-testid="stSidebar"] div[data-testid="stMetric"] {

        background: rgba(8, 14, 9, 0.9);

        border:
            1px solid rgba(0, 255, 102, 0.15);
    }


   /* =========================================================
   SELECT BOX — FIXED
   ========================================================= */

/* Main select box */
div[data-baseweb="select"] {
    position: relative !important;
    z-index: 9999 !important;
}

div[data-baseweb="select"] > div {
    background: #ffffff !important;
    border: 1px solid #00ff66 !important;
    border-radius: 12px !important;
    color: #000000 !important;
    min-height: 40px !important;
}


/* Selected value */
div[data-baseweb="select"] span {
    color: #000000 !important;
}


/* Actual input inside select */
div[data-baseweb="select"] input {
    color: #000000 !important;
    caret-color: #000000 !important;
}


/* Dropdown arrow */
div[data-baseweb="select"] svg {
    color: #000000 !important;
    fill: #000000 !important;
}


/* Dropdown container */
div[data-baseweb="popover"] {
    z-index: 999999 !important;
}


/* Dropdown menu */
div[role="listbox"] {
    background: #ffffff !important;
    border: 1px solid #00ff66 !important;
    border-radius: 10px !important;
    z-index: 999999 !important;
    pointer-events: auto !important;
}


/* Individual options */
div[role="option"] {
    background: #ffffff !important;
    color: #000000 !important;
    cursor: pointer !important;
    pointer-events: auto !important;
}


/* Option text */
div[role="option"] * {
    color: #000000 !important;
    pointer-events: none !important;
}


/* Hover */
div[role="option"]:hover {
    background: rgba(0, 255, 102, 0.15) !important;
    color: #000000 !important;
}


/* Selected option */
div[role="option"][aria-selected="true"] {
    background: rgba(0, 255, 102, 0.12) !important;
    color: #000000 !important;
}
    /* =========================================================
       BUTTONS
       ========================================================= */

    .stButton > button {

        width: 100%;

        border-radius: 12px;

        border:
            1px solid rgba(0, 255, 102, 0.22);

        background:
            linear-gradient(
                135deg,
                #0b120d,
                #070c08
            );

        color: #eafff0;

        font-weight: 750;

        padding: 0.75rem 1rem;

        transition:
            all 0.2s ease;

        box-shadow:
            inset 0 1px rgba(255,255,255,0.025);
    }


    .stButton > button:hover {

        border-color:
            rgba(0, 255, 102, 0.65);

        color:
            var(--green-bright);

        background:
            linear-gradient(
                135deg,
                #0d1b11,
                #09120b
            );

        transform:
            translateY(-2px);

        box-shadow:
            0 0 25px rgba(0, 255, 102, 0.12);
    }


    /* ---------- PRIMARY BUTTON ---------- */

    .stButton > button[kind="primary"] {
    background: linear-gradient(
        90deg,
        #8f0e0e,
        var(--red)
    ) !important;

    border: 1px solid var(--red-bright) !important;
    color: white !important;
    font-weight: 850 !important;

    box-shadow:
        0 0 20px rgba(255, 43, 43, 0.20),
        inset 0 1px rgba(255,255,255,0.20);
}

.stButton > button[kind="primary"]:hover {
    background: linear-gradient(
        90deg,
        #b51212,
        #ff4141
    ) !important;

    box-shadow:
        0 0 32px rgba(255, 43, 43, 0.35);

    transform: translateY(-2px);
}
/* =========================================================
   HUMAN REVIEW — SECURITY APPROVAL PANEL
   ========================================================= */

/* Human Review section heading */
h2:has(+ div) {
    letter-spacing: -0.3px;
}

/* Human Review warning */
div[data-testid="stAlert"] {
    border-radius: 12px !important;
}

/* Radio container */
div[role="radiogroup"] {
    background: #080808 !important;
    border: 1px solid #2d2d2d !important;
    border-left: 3px solid #ff2b2b !important;
    padding: 14px 18px !important;
    border-radius: 10px !important;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
}

/* Radio labels */
div[role="radiogroup"] label {
    color: #dddddd !important;
    font-weight: 700 !important;
}

/* Radio hover */
div[role="radiogroup"] label:hover {
    color: #39ff88 !important;
}

/* Selected radio */
div[role="radiogroup"] label[data-checked="true"] {
    color: #39ff88 !important;
}

/* Reviewer notes box */
textarea {
    background: #050505 !important;
    border: 1px solid #292929 !important;
    border-left: 3px solid #ff2b2b !important;
    border-radius: 10px !important;
    color: #f5f5f5 !important;
    font-family: "Segoe UI", sans-serif !important;
}

textarea:focus {
    border-color: #ff2b2b !important;
    box-shadow:
        0 0 0 1px rgba(255, 43, 43, 0.25),
        0 0 20px rgba(255, 43, 43, 0.08) !important;
}

/* Submit Human Review button */
.stButton > button[kind="primary"] {
    background: linear-gradient(
        90deg,
        #8f0e0e,
        #ff2b2b
    ) !important;

    border: 1px solid #ff4b4b !important;
    color: #ffffff !important;

    font-weight: 850 !important;
    letter-spacing: 0.2px;

    box-shadow:
        0 0 18px rgba(255, 43, 43, 0.16),
        inset 0 1px rgba(255,255,255,0.15);
}

.stButton > button[kind="primary"]:hover {
    background: linear-gradient(
        90deg,
        #b51212,
        #ff4141
    ) !important;

    border-color: #ff6b6b !important;

    box-shadow:
        0 0 28px rgba(255, 43, 43, 0.30) !important;

    transform: translateY(-2px);
}

/* Success confirmation */
div[data-testid="stAlert"] {
    box-shadow: 0 8px 22px rgba(0, 0, 0, 0.25);
}

/* Human review info message */
div[data-testid="stAlert"] p {
    font-weight: 600 !important;
}






    /* =========================================================
       CODE / TERMINAL EVIDENCE
       ========================================================= */

    pre {

        background:
            #020603 !important;

        border:
            1px solid rgba(0, 255, 102, 0.18) !important;

        border-radius:
            14px !important;

        padding:
            18px !important;

        box-shadow:
            inset 0 0 35px rgba(0, 255, 102, 0.025);

        position:
            relative;
    }


    code {

        color:
            #7dffa9 !important;

        font-family:
            "Consolas",
            "Courier New",
            monospace !important;
    }


    /* =========================================================
       ALERTS
       ========================================================= */

    div[data-testid="stAlert"] {

        border-radius:
            14px !important;

        border:
            1px solid rgba(0, 255, 102, 0.18);

        background:
            rgba(7, 15, 9, 0.85);

        backdrop-filter:
            blur(12px);
    }


    /* =========================================================
       RADIO BUTTONS
       ========================================================= */

    div[role="radiogroup"] {

        background:
            rgba(7, 13, 8, 0.82);

        border:
            1px solid rgba(0, 255, 102, 0.15);

        padding:
            12px 16px;

        border-radius:
            14px;
    }


    /* =========================================================
       TEXT AREA
       ========================================================= */

    textarea {

        background:
            #060a07 !important;

        border:
            1px solid rgba(0, 255, 102, 0.18) !important;

        border-radius:
            14px !important;

        color:
            #effff4 !important;
    }


    textarea:focus {

        border-color:
            rgba(0, 255, 102, 0.65) !important;

        box-shadow:
            0 0 22px rgba(0, 255, 102, 0.10) !important;
    }


    /* =========================================================
       DATAFRAME
       ========================================================= */

    div[data-testid="stDataFrame"] {

        border-radius:
            14px;

        overflow:
            hidden;

        border:
            1px solid rgba(0, 255, 102, 0.15);

        box-shadow:
            0 10px 30px rgba(0,0,0,0.3);
    }


    /* =========================================================
       DIVIDERS
       ========================================================= */

    hr {

        border-color:
            rgba(0, 255, 102, 0.12) !important;
    }


    /* =========================================================
       SCROLLBAR
       ========================================================= */

    ::-webkit-scrollbar {
        width: 8px;
    }


    ::-webkit-scrollbar-track {
        background:
            #020402;
    }


    ::-webkit-scrollbar-thumb {

        background:
            #12351e;

        border-radius:
            10px;
    }


    ::-webkit-scrollbar-thumb:hover {

        background:
            #00a844;
    }


    /* =========================================================
       STREAMLIT INPUT TEXT
       ========================================================= */

    input {

        color:
            #effff4 !important;
    }


    /* =========================================================
       EXPANDERS
       ========================================================= */

    div[data-testid="stExpander"] {

        background:
            rgba(7, 12, 8, 0.75);

        border:
            1px solid rgba(0, 255, 102, 0.14);

        border-radius:
            14px;
    }


    /* =========================================================
       LINKS
       ========================================================= */

    a {

        color:
            var(--green-bright) !important;
    }


</style>
""", unsafe_allow_html=True)

BASE = Path(__file__).parent
cases = pd.read_csv(BASE / "cases.csv")
# OpenAI client
client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)
st.title("🌐 NetSage AI")
st.caption(
    "Evidence-first network intelligence • "
    "AI-assisted troubleshooting • Human review"
)


# Sidebar
st.sidebar.header("Case Selection")

case_id = st.sidebar.selectbox(
    "Choose a troubleshooting case",
    cases["case_id"].tolist()
)

case = cases[cases["case_id"] == case_id].iloc[0]

# Session state
if "diagnosis" not in st.session_state:
    st.session_state.diagnosis = None

if "reviewed" not in st.session_state:
    st.session_state.reviewed = []

# Reset diagnosis when user changes the case
if "last_case" not in st.session_state:
    st.session_state.last_case = case_id

if st.session_state.last_case != case_id:
    st.session_state.diagnosis = None
    st.session_state.last_case = case_id

st.sidebar.divider()

st.sidebar.metric("Total Cases", len(cases))
st.sidebar.metric("Issue Types", cases["concept_tag"].nunique())
# Case
st.markdown(
    f"""
    <div style="
        margin-top:28px;
        margin-bottom:20px;
        padding:22px 26px;
        border-radius:18px;

        background:
            linear-gradient(
                135deg,
                rgba(40,8,8,.92),
                rgba(12,12,12,.96)
            );

        border:1px solid rgba(255,43,43,.32);

        box-shadow:
            0 15px 40px rgba(0,0,0,.45),
            inset 3px 0 0 #ff2b2b;
    ">

        <div style="
            color:#ff4b4b;
            font-size:13px;
            font-weight:800;
            letter-spacing:1.5px;
            text-transform:uppercase;
        ">
            ● ACTIVE TROUBLESHOOTING CASE
        </div>

        <div style="
            color:#f5f5f5;
            font-size:30px;
            font-weight:850;
            margin-top:7px;
        ">
            {case['case_id']} — {case['concept_tag']}
        </div>

    </div>
    """,
    unsafe_allow_html=True
)
c1, c2 = st.columns(2)
with c1:
    st.markdown("### 🐛 Symptom")
    st.write(case["symptom"])
    st.markdown("### 🗺️ Topology")
    st.write(case["topology_note"])

with c2:
    st.subheader("🔎 Show-command evidence")
    st.code(case["show_outputs"])
    st.write(f"**Severity:** {case['severity']}")
    st.write(f"**Expected OSI layer:** {case['osi_layer']}")


if st.button(
    "🤖 Run AI Diagnosis",
    type="primary",
    use_container_width=True
):
    try:
        with st.spinner("Analyzing network evidence..."):
            st.session_state.diagnosis = ai_diagnose(case, client)

        st.success("AI diagnosis generated successfully.")

    except Exception as e:
        if "insufficient_quota" in str(e) or "429" in str(e):
            st.warning(
                "OpenAI API quota is unavailable. "
                "Running NetSage in local demonstration mode."
            )

            st.session_state.diagnosis = demo_diagnose(case)

        else:
            st.error(f"AI diagnosis failed: {e}")
    

if st.session_state.diagnosis:
    d = st.session_state.diagnosis

    st.divider()
    st.header("🤖 AI Diagnosis")

    a, b = st.columns([3, 1])
    with a:
        st.subheader("Root Cause")
        st.success(d["root_cause"])
    with b:
        st.subheader("Confidence")
        st.metric("Confidence", f"{d['confidence']}%")

    st.subheader("Evidence")
    for e in d["evidence"]:
        st.code(e)

    st.subheader("Next Diagnostic Command")
    st.code(d["next_command"])

    st.subheader("Suggested Fix")
    for step in d["fix_steps"]:
        st.write("• " + step)

    st.subheader("Verification")
    st.info(d["verification"])

    st.divider()
    st.header("🔐 Deterministic Rule Checker")

    check = check_diagnosis(d, case)

    if check["root_cause_match"]:
        st.success("✓ PASS — AI root cause matches the case's expected fault.")
    else:
        st.error("✗ FAIL — AI root cause does not match expected fault.")

    if check["evidence_referenced"]:
        st.success("✓ PASS — AI referenced supplied show-command evidence.")
    else:
        st.warning("⚠ Evidence reference could not be verified automatically.")
    st.divider()
    
    st.header("👤 Human Review")

    st.warning(
        "⚠️ Human approval required: AI output is a recommendation, "
        "not an automatic configuration change."
    )

    decision = st.radio(
        "Reviewer decision",
        ["Accepted", "Edited", "Rejected"],
        horizontal=True
    )

    notes = st.text_area(
        "Reviewer notes",
        placeholder="Explain why the diagnosis was accepted, edited, or rejected."
    )

    if st.button("Submit Human Review", type="primary"):
        review_record = {
            "case_id": case_id,
            "decision": decision,
            "notes": notes,
            "expected_fault": case["expected_fault"],
            "ai_root_cause": d["root_cause"]
        }

        st.session_state.reviewed.append(review_record)

        st.success(
            f"✓ Human review recorded successfully: {decision}"
        )

        st.info(
            f"Case {case_id} has been reviewed and added to the session review log."
        )

        st.success(
            f"✓ Human review recorded successfully: {decision}"
        )

        st.info(
            f"Case {case_id} has been reviewed and added to the session review log."
        )

# Dashboard
st.divider()
st.header("📊 Dashboard")

reviewed = pd.DataFrame(st.session_state.reviewed)

m1, m2, m3, m4 = st.columns(4)

m1.metric(
    "Total Cases",
    len(cases)
)

m2.metric(
    "Issue Types",
    cases["concept_tag"].nunique()
)

m3.metric(
    "Reviewed",
    len(reviewed)
)

if len(reviewed) > 0:
    accepted = (reviewed["decision"] == "Accepted").sum()
    agreement = round((accepted / len(reviewed)) * 100)
else:
    agreement = 0

m4.metric(
    "AI-Human Agreement",
    f"{agreement}%"
)



left, right = st.columns(2)
with left:
    st.subheader("Cases by Concept")
    st.bar_chart(cases["concept_tag"].value_counts())

with right:
    st.subheader("Cases by Severity")
    st.bar_chart(cases["severity"].value_counts())

if len(reviewed):
    st.subheader("Human Review Log — Current Session")
    st.dataframe(reviewed, use_container_width=True)
st.divider()

st.header("🛡️ Responsible AI Log")

st.write(
    "AI diagnoses are treated as recommendations. "
    "A human reviewer must approve, edit, or reject every diagnosis."
)

responsible_cases = pd.DataFrame([
    {
        "Case": "NET-003",
        "AI Issue": "DNS service disabled",
        "Human Action": "Edited",
        "Reason": "Client DNS configuration also requires verification"
    },
    {
        "Case": "NET-007",
        "AI Issue": "Guest ACL too permissive",
        "Human Action": "Accepted",
        "Reason": "Evidence directly supports the diagnosis"
    },
    {
        "Case": "NET-012",
        "AI Issue": "OSPF adjacency problem",
        "Human Action": "Edited",
        "Reason": "Passive interface was the specific cause"
    },
    {
        "Case": "NET-020",
        "AI Issue": "Gateway configuration problem",
        "Human Action": "Accepted",
        "Reason": "Gateway is outside the client subnet"
    },
    {
        "Case": "NET-021",
        "AI Issue": "OSPF redistribution problem",
        "Human Action": "Edited",
        "Reason": "Missing 'subnets' keyword identified"
    }
])

st.dataframe(
    responsible_cases,
    use_container_width=True,
    hide_index=True
)

    
