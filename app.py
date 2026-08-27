import streamlit as st
import pandas as pd
from pathlib import Path
from openai import OpenAI

from diagnosis import ai_diagnose, demo_diagnose
from checker import check_diagnosis
st.set_page_config(page_title="NetSage AI", page_icon="🌐", layout="wide")


st.markdown("""
<style>

    /* ---------- GLOBAL ---------- */

    .stApp {
        background:
            radial-gradient(circle at 10% 10%, rgba(0, 180, 255, 0.10), transparent 30%),
            radial-gradient(circle at 90% 20%, rgba(100, 80, 255, 0.10), transparent 30%),
            linear-gradient(135deg, #050914 0%, #08111f 50%, #050914 100%);
        color: #e8f1ff;
    }

    .main .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* ---------- HEADINGS ---------- */

    h1 {
        font-size: 3rem !important;
        font-weight: 800 !important;
        letter-spacing: -1px;
        background: linear-gradient(90deg, #ffffff, #69d9ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    h2 {
        color: #f2f7ff !important;
        font-weight: 750 !important;
    }

    h3 {
        color: #bfe9ff !important;
        font-weight: 650 !important;
    }

    p, label {
        color: #b8c7dc !important;
    }

    /* ---------- TOP CAPTION ---------- */

    .stCaption {
        color: #7f9bb8 !important;
        font-size: 1rem !important;
    }

    /* ---------- GLASS CONTAINERS ---------- */

    div[data-testid="stVerticalBlock"] > div:has(
        div[data-testid="stMetric"]
    ) {
        background: rgba(15, 27, 48, 0.55);
        border: 1px solid rgba(130, 190, 255, 0.14);
        border-radius: 18px;
        backdrop-filter: blur(18px);
    }

    /* ---------- METRICS ---------- */

    div[data-testid="stMetric"] {
        background: rgba(15, 28, 48, 0.72);
        border: 1px solid rgba(100, 190, 255, 0.18);
        padding: 18px;
        border-radius: 18px;
        box-shadow: 0 10px 35px rgba(0, 0, 0, 0.25);
    }

    div[data-testid="stMetricLabel"] {
        color: #7895b5 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #eaf7ff !important;
        font-weight: 800 !important;
    }

    /* ---------- SIDEBAR ---------- */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                rgba(9, 18, 34, 0.96),
                rgba(5, 12, 24, 0.98)
            );
        border-right: 1px solid rgba(100, 190, 255, 0.12);
    }

    section[data-testid="stSidebar"] h2 {
        color: #dff6ff !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stMetric"] {
        background: rgba(16, 31, 52, 0.65);
    }

    /* ---------- SELECT BOX ---------- */

    div[data-baseweb="select"] > div {
        background: rgba(17, 31, 53, 0.75) !important;
        border: 1px solid rgba(90, 180, 255, 0.22) !important;
        border-radius: 12px !important;
        color: white !important;
    }

    /* ---------- BUTTONS ---------- */

    .stButton > button {
        width: 100%;
        border-radius: 14px;
        border: 1px solid rgba(90, 200, 255, 0.25);
        background: rgba(25, 55, 82, 0.65);
        color: #e9f8ff;
        font-weight: 700;
        padding: 0.75rem 1rem;
        transition: all 0.2s ease;
        backdrop-filter: blur(12px);
    }

    .stButton > button:hover {
        border-color: rgba(80, 210, 255, 0.7);
        background: rgba(25, 85, 120, 0.75);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 180, 255, 0.18);
    }

    /* ---------- PRIMARY BUTTON ---------- */

    .stButton > button[kind="primary"] {
        background: linear-gradient(
            90deg,
            #087ea4,
            #2563c9
        ) !important;
        border: 1px solid rgba(110, 220, 255, 0.45) !important;
        box-shadow:
            0 0 20px rgba(0, 180, 255, 0.18),
            inset 0 1px rgba(255,255,255,0.15);
    }

    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(
            90deg,
            #0a9bc8,
            #3476df
        ) !important;
        box-shadow:
            0 0 30px rgba(0, 190, 255, 0.30);
    }

    /* ---------- CODE / EVIDENCE ---------- */

    pre {
        background: rgba(3, 12, 24, 0.78) !important;
        border: 1px solid rgba(80, 170, 255, 0.16) !important;
        border-radius: 14px !important;
        padding: 18px !important;
        box-shadow: inset 0 0 30px rgba(0, 100, 180, 0.05);
    }

    code {
        color: #9ee8ff !important;
    }

    /* ---------- SUCCESS / INFO / WARNING ---------- */

    div[data-testid="stAlert"] {
        border-radius: 14px !important;
        border: 1px solid rgba(100, 200, 255, 0.18);
        background: rgba(20, 40, 65, 0.60);
        backdrop-filter: blur(12px);
    }

    /* ---------- RADIO ---------- */

    div[role="radiogroup"] {
        background: rgba(14, 27, 46, 0.60);
        border: 1px solid rgba(100, 180, 255, 0.15);
        padding: 12px 16px;
        border-radius: 14px;
    }

    /* ---------- TEXT AREA ---------- */

    textarea {
        background: rgba(10, 22, 38, 0.72) !important;
        border: 1px solid rgba(90, 180, 255, 0.18) !important;
        border-radius: 14px !important;
        color: white !important;
    }

    textarea:focus {
        border-color: rgba(70, 200, 255, 0.65) !important;
        box-shadow: 0 0 20px rgba(0, 180, 255, 0.12) !important;
    }

    /* ---------- DATAFRAME ---------- */

    div[data-testid="stDataFrame"] {
        border-radius: 14px;
        overflow: hidden;
        border: 1px solid rgba(100, 190, 255, 0.14);
    }

    /* ---------- DIVIDERS ---------- */

    hr {
        border-color: rgba(100, 180, 255, 0.10) !important;
    }

    /* ---------- SCROLLBAR ---------- */

    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #050914;
    }

    ::-webkit-scrollbar-thumb {
        background: #183b58;
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #24658d;
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
        border-radius:20px;
        background:linear-gradient(
            135deg,
            rgba(18,40,66,.72),
            rgba(10,24,42,.48)
        );
        border:1px solid rgba(100,190,255,.16);
        backdrop-filter:blur(18px);
        box-shadow:0 15px 40px rgba(0,0,0,.20);
    ">
        <div style="
            color:#61d7ff;
            font-size:14px;
            font-weight:700;
            letter-spacing:1px;
            text-transform:uppercase;
        ">
            ACTIVE TROUBLESHOOTING CASE
        </div>

        <div style="
            color:#f3f8ff;
            font-size:30px;
            font-weight:800;
            margin-top:5px;
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

    
