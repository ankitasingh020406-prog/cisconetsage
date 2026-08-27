# 🌐 NetSage AI

**Evidence-first network intelligence • AI-assisted troubleshooting •
Human review**

NetSage AI is an AI-assisted network troubleshooting application built
with **Streamlit**. It is designed for Cisco-style networking labs and
Packet Tracer scenarios. The application takes a predefined
troubleshooting case, displays the symptom, topology information, and
show-command evidence, then uses an AI model to suggest a likely root
cause, confidence score, supporting evidence, next diagnostic command,
fix steps, and verification steps.

A key design principle of NetSage AI is **human-in-the-loop
troubleshooting**: the AI provides a recommendation, but a human
reviewer must accept, edit, or reject the diagnosis before it is
considered approved.

------------------------------------------------------------------------

## 📌 Project Overview

Junior network engineers may know individual Cisco commands but can have
difficulty connecting a network symptom to its actual root cause.

For example:

-   A PC receives an IP address but cannot reach a server.
-   A DHCP scope has no available addresses.
-   DNS resolution fails.
-   OSPF neighbors do not form.
-   An ACL blocks required traffic.
-   NAT translations are missing.
-   A VLAN is not allowed across a trunk.
-   A default gateway is outside the client's subnet.

NetSage AI helps organize this troubleshooting process by combining:

1.  **Case-based network evidence**
2.  **AI-assisted diagnosis**
3.  **Deterministic rule checking**
4.  **Human review**
5.  **Dashboard and responsible-AI logging**

------------------------------------------------------------------------

## ✨ Main Features

### 1. Troubleshooting Case Selection

The sidebar allows the user to select a network troubleshooting case
from `cases.csv`.

For the selected case, the application displays:

-   Case ID
-   Networking concept
-   Symptom
-   Topology note
-   Show-command output
-   Severity
-   Expected OSI layer

------------------------------------------------------------------------

### 2. Evidence-First AI Diagnosis

When **Run AI Diagnosis** is clicked, NetSage AI sends the case
information to the OpenAI API.

The prompt instructs the model to:

-   Use supplied evidence as the primary source
-   Avoid inventing command output
-   Identify one most likely root cause
-   Return a confidence score from 0--100
-   Recommend the next diagnostic command
-   Provide practical fix steps
-   Provide verification steps
-   Admit when evidence is insufficient
-   Never claim that configuration changes were actually performed

The AI response is required to use structured JSON.

Expected structure:

``` json
{
  "root_cause": "string",
  "confidence": 0,
  "evidence": ["string"],
  "osi_layer": "string",
  "next_command": "string",
  "fix_steps": ["string"],
  "verification": "string"
}
```

------------------------------------------------------------------------

### 3. Local Demonstration / Fallback Mode

If the OpenAI API is unavailable because of quota/rate-limit issues,
NetSage AI automatically falls back to a deterministic demonstration
diagnosis.

The fallback engine contains:

-   A command map for common networking concepts
-   A fix map for the 30 demonstration cases
-   Expected faults from the dataset
-   Evidence and verification information

This allows the project to be demonstrated even when an API call cannot
be completed.

------------------------------------------------------------------------

### 4. Deterministic Rule Checker

The application does not rely only on the AI response.

It checks whether:

-   The AI root cause matches the case's expected fault.
-   The AI diagnosis references the supplied show-command evidence.

The results are displayed as:

-   `PASS` when the diagnosis matches
-   `FAIL` when the diagnosis does not match
-   `WARNING` when evidence verification cannot be completed
    automatically

This provides a simple deterministic validation layer around the AI.

------------------------------------------------------------------------

### 5. Human Review

Every AI diagnosis is presented as a recommendation rather than an
automatic configuration change.

The reviewer can select:

-   **Accepted**
-   **Edited**
-   **Rejected**

The reviewer can also enter notes explaining the decision.

The review is stored in the current Streamlit session and displayed in
the Human Review Log.

------------------------------------------------------------------------

### 6. Dashboard

The dashboard provides a quick overview of the troubleshooting dataset
and review activity.

It displays:

-   Total cases
-   Number of issue types
-   Number of reviewed cases
-   AI-human agreement percentage
-   Cases by concept
-   Cases by severity
-   Current-session human review log

------------------------------------------------------------------------

### 7. Responsible AI Log

The application includes a sample Responsible AI Log showing cases where
AI output required human correction or approval.

Example logged cases include:

-   DNS diagnosis requiring additional client-side verification
-   Guest ACL diagnosis accepted based on evidence
-   OSPF diagnosis edited to identify a passive-interface issue
-   Gateway diagnosis accepted
-   OSPF redistribution diagnosis edited to identify a missing `subnets`
    keyword

The purpose is to demonstrate that AI output is reviewed rather than
blindly trusted.

------------------------------------------------------------------------

## 🏗️ Technology Stack

  Technology                     Purpose
  ------------------------------ --------------------------------------
  Python                         Application programming language
  Streamlit                      Web application interface
  Pandas                         Dataset loading and analysis
  OpenAI API                     AI-assisted diagnosis
  JSON                           Structured AI response format
  Pathlib                        File/path management
  CSS                            Custom application styling
  Cisco/Packet Tracer concepts   Networking troubleshooting scenarios

------------------------------------------------------------------------

## 📂 Recommended Project Structure

``` text
NetSage-AI/
│
├── app.py
├── cases.csv
├── README.md
│
├── .streamlit/
│   └── secrets.toml
│
└── requirements.txt
```

### File descriptions

#### `app.py`

Main Streamlit application.

It contains:

-   UI and custom CSS
-   Case loading
-   Case selection
-   AI diagnosis function
-   Demo diagnosis function
-   Rule checker
-   Human review
-   Dashboard
-   Responsible AI log

#### `cases.csv`

The troubleshooting case dataset.

The application expects columns such as:

``` text
case_id
symptom
topology_note
show_outputs
severity
osi_layer
concept_tag
expected_fault
```

The project is intended to contain at least **30 troubleshooting cases**
covering multiple network fault types.

#### `.streamlit/secrets.toml`

Stores the OpenAI API key securely for local Streamlit execution.

------------------------------------------------------------------------

## 🧪 Networking Concepts Covered

The application is designed around a range of common networking
troubleshooting areas, including:

-   VLAN
-   VLAN Trunking
-   Inter-VLAN Routing
-   DHCP
-   DNS
-   OSPF
-   ACL
-   NAT
-   Wireless
-   Wireless/ACL
-   Addressing
-   Static Routing
-   Switching
-   Subnetting
-   VTP
-   Dynamic ARP Inspection
-   Port Security
-   HSRP
-   IPv6
-   CDP

The exact cases and evidence are loaded from `cases.csv`.

------------------------------------------------------------------------

## 🔎 Example Troubleshooting Flow

### Example 1 --- Inter-VLAN Routing

**Symptom:**

A PC receives an IP address but cannot reach a server in another VLAN.

**Possible diagnosis:**

The issue may be related to inter-VLAN routing or an incorrectly
configured sub-interface.

**Next command:**

``` text
show ip interface brief
```

**Human review:**

The reviewer checks the supplied evidence and decides whether to accept,
edit, or reject the AI recommendation.

------------------------------------------------------------------------

### Example 2 --- Guest Network Access

**Symptom:**

A guest Wi-Fi client can reach internal network resources when it should
only have internet access.

**Possible diagnosis:**

Guest isolation or ACL policy may be incorrectly configured.

**Next step:**

Inspect VLAN mapping and ACL rules.

The reviewer verifies that the evidence supports the recommendation
before approving it.

------------------------------------------------------------------------

## 🔐 Responsible AI Design

NetSage AI follows several safety principles.

### Evidence First

The AI is instructed to use the supplied show-command evidence as its
primary source.

### No Fabricated Evidence

The prompt explicitly tells the model not to invent show-command output.

### Human Approval Required

AI output is not treated as an automatic configuration change.

The reviewer must:

-   Accept the diagnosis
-   Edit the diagnosis
-   Or reject the diagnosis

### Deterministic Validation

The application compares the AI root cause against the expected fault
stored in the dataset.

### Verification

The application recommends rerunning the relevant command and testing
the original connectivity problem after a proposed fix.

------------------------------------------------------------------------

## ⚙️ Installation

### 1. Clone or create the project

Place the following files in the same project directory:

``` text
app.py
cases.csv
README.md
```

### 2. Create a virtual environment

Windows:

``` bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:

``` bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

Create `requirements.txt`:

``` text
streamlit
pandas
openai
```

Then run:

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

## 🔑 Configure the OpenAI API Key

Create the following file:

``` text
.streamlit/secrets.toml
```

Add:

``` toml
OPENAI_API_KEY = "your-openai-api-key"
```

Do **not** commit your API key to GitHub or place it directly inside
`app.py`.

The application reads the key using Streamlit secrets.

------------------------------------------------------------------------

## ▶️ Run the Application

From the project directory:

``` bash
streamlit run app.py
```

Streamlit will start the application and provide a local URL, normally
similar to:

``` text
http://localhost:8501
```

Open the URL in a browser.

------------------------------------------------------------------------

## 🖥️ Application Workflow

The normal workflow is:

``` text
Select Case
    ↓
Review Symptom + Topology
    ↓
Inspect Show-Command Evidence
    ↓
Run AI Diagnosis
    ↓
Display Root Cause + Confidence
    ↓
Review Evidence
    ↓
Check Next Diagnostic Command
    ↓
Review Suggested Fix
    ↓
Run Deterministic Rule Checker
    ↓
Human Review
    ↓
Accept / Edit / Reject
    ↓
Dashboard + Responsible AI Log
```

------------------------------------------------------------------------

## 📊 Expected Dataset Coverage

For the project requirements, the dataset should contain at least **30
troubleshooting cases** across multiple network fault types.

A suitable case dataset should include evidence such as:

-   Symptoms
-   Topology notes
-   Show-command output
-   Expected fault
-   OSI layer
-   Networking concept
-   Severity

The application uses these fields both for AI diagnosis and
deterministic validation.

------------------------------------------------------------------------

## 🧠 AI Prompt Strategy

The application uses a structured prompt instead of asking the model an
unrestricted question.

The prompt provides:

``` text
Case ID
Symptom
Topology
Show-command evidence
Expected OSI layer
Concept
Severity
```

The model is then instructed to return only the expected JSON fields.

This makes the output easier for the application to parse and display.

------------------------------------------------------------------------

## 🧩 AI vs Rule-Based Diagnosis

NetSage AI uses two complementary approaches.

### AI Diagnosis

Useful for:

-   Interpreting symptoms
-   Connecting evidence to likely causes
-   Generating diagnostic reasoning
-   Suggesting practical next commands
-   Producing human-readable fix steps

### Deterministic Checker

Useful for:

-   Checking the expected root cause
-   Verifying that supplied evidence was referenced
-   Reducing dependence on AI correctness

Together, they demonstrate an **AI-assisted rather than AI-controlled**
troubleshooting workflow.

------------------------------------------------------------------------

## 📝 Human Review Data

During a session, every submitted review records:

``` text
case_id
decision
notes
expected_fault
ai_root_cause
```

The review data is displayed in the dashboard.

> Note: The current implementation stores review records in
> `st.session_state`, so they are session-based and are not a permanent
> database.

------------------------------------------------------------------------

## ⚠️ Limitations

This project is intended as an educational/demo troubleshooting
assistant.

Current limitations include:

1.  The dataset is loaded from a local CSV file.
2.  Human-review records are stored only for the current Streamlit
    session.
3.  The application does not directly configure Cisco devices.
4.  The AI cannot independently verify a live network.
5.  The fallback diagnosis is based on predefined case mappings.
6.  AI responses depend on the availability and behavior of the
    configured OpenAI model/API.
7.  The Responsible AI Log currently contains predefined demonstration
    records rather than a persistent audit database.

------------------------------------------------------------------------

## 🚀 Possible Future Improvements

Future versions could add:

-   Persistent review history using SQLite, PostgreSQL, or Supabase
-   User authentication
-   Upload of Packet Tracer evidence
-   Automatic parsing of Cisco command output
-   More troubleshooting cases
-   Network topology visualization
-   Multi-model AI comparison
-   Confidence thresholds requiring mandatory human review
-   Exportable diagnosis reports
-   Search and filtering of historical cases
-   Automatic before/after verification
-   Admin dashboard
-   Deployment to Streamlit Community Cloud or another hosting platform

------------------------------------------------------------------------

## 🎯 Project Goals

NetSage AI demonstrates how AI can assist network engineers without
removing human responsibility from troubleshooting.

The project focuses on:

-   **Network troubleshooting**
-   **Evidence-based diagnosis**
-   **AI-assisted reasoning**
-   **Deterministic validation**
-   **Human oversight**
-   **Responsible AI**
-   **Clear verification steps**

The central principle is:

> **AI suggests. Evidence supports. Rules check. Humans decide.**

------------------------------------------------------------------------

## 👩‍💻 Project Deliverables

The project can be submitted with:

  -----------------------------------------------------------------------
  Deliverable                         Description
  ----------------------------------- -----------------------------------
  `cases.csv`                         At least 30 network troubleshooting
                                      cases

  `app.py`                            Streamlit application and diagnosis
                                      engine

  `README.md`                         Project documentation

  Prompt documentation                Structured AI prompt and output
                                      format

  Python checker                      Deterministic validation logic

  Dashboard                           Issue types, severity, review and
                                      agreement information

  Responsible AI log                  Examples of corrected/approved AI
                                      responses

  Demo video                          Demonstration of case selection, AI
                                      diagnosis, human review, fix and
                                      verification
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 📹 Suggested Demo Video Flow

A 5--10 minute demonstration can follow this sequence:

### 1. Introduction

Briefly explain:

> NetSage AI is an evidence-first AI troubleshooting assistant for
> Cisco-style networking labs.

### 2. Select a Broken Case

Choose a case from the sidebar.

Show:

-   Symptom
-   Topology
-   Show-command evidence
-   Severity
-   OSI layer

### 3. Run AI Diagnosis

Click:

``` text
🤖 Run AI Diagnosis
```

Show:

-   Root cause
-   Confidence
-   Evidence
-   Next diagnostic command
-   Suggested fix
-   Verification

### 4. Demonstrate Rule Checker

Show whether the AI diagnosis matches the expected fault.

### 5. Human Review

Choose:

``` text
Accepted
```

or:

``` text
Edited
```

or:

``` text
Rejected
```

Add reviewer notes.

### 6. Dashboard

Show:

-   Total cases
-   Issue types
-   Reviewed cases
-   AI-human agreement
-   Concept chart
-   Severity chart
-   Review log

### 7. Responsible AI

Explain that the AI recommendation is not automatically applied and
requires human approval.

------------------------------------------------------------------------

---

## 👩‍💻 Created & Coded By

**Shubhangi Verma**  
*Designed, developed, and coded with ❤️ for network troubleshooting and Responsible AI.*

---

## 📄 License

This project is intended for educational, academic, and demonstration
purposes. Add an appropriate license if the project is published or
distributed publicly.

------------------------------------------------------------------------

## ⭐ Conclusion

**NetSage AI** combines networking knowledge, structured evidence, AI
assistance, deterministic validation, and human oversight into one
troubleshooting workflow.

It demonstrates a practical responsible-AI pattern for network
engineering:

**Observe → Diagnose → Validate → Review → Fix → Verify**
