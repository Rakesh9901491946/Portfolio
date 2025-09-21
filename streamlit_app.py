"""
Portfolio App (Dual-Mode: Streamlit or Static HTML)

This script runs in two modes:
1) If **Streamlit** is available → launches an interactive portfolio app.
2) If **Streamlit is missing** (e.g., restricted/sandboxed env) → generates a static `portfolio.html` you can open in any browser.

Run (interactive):
    streamlit run streamlit_app.py

Run (static fallback if Streamlit isn't installed):
    python streamlit_app.py

NOTE: We intentionally **do not call sys.exit(...)** in the fallback so internal tests can still run.
"""

from datetime import datetime
import sys
import os

# ---------------------------
# CONFIG — EDIT THESE FIELDS
# ---------------------------

WORK_EXPERIENCE = [
    {
        "company": "iiterate Technologies GmbH",
        "title": "AI Development Intern",
        "location": "Koblenz, Germany",
        "duration": "05/2025 – present",
        "details": [
            "Fine-tuned LLMs for summarization, Q&A, and classification using Hugging Face & OpenAI APIs.",
            "Built RAG pipelines with LangChain and vector DBs (FAISS, Pinecone).",
            "Developed YOLOv8 + Deep SORT tracking systems on custom datasets.",
            "Created Streamlit apps for CV/LLM demos tailored to client needs."
        ]
    },
    {
        "company": "KPMG Global Services Private Limited",
        "title": "Analyst",
        "location": "Bengaluru, India",
        "duration": "11/2020 – 08/2023",
        "details": [
            "Built ETL pipelines with Azure Data Factory to ingest from SQL/API to Data Lake.",
            "Used PySpark on Databricks for big data feature engineering (30+ fraud detection features).",
            "Optimized Spark jobs (caching, partitioning, Z-order) improving runtime by 35%.",
            "Built Power BI dashboards using Synapse data for fraud/claims analytics.",
            "Enabled CI/CD and Terraform to automate deployments, reducing manual work by 40%."
        ]
    }
]
PROFILE = {
    "name": "Rakesh Nagaragatta Jayanna",
    "role": "Data Scientist & AI Engineer",
    "location": "Heidelberg, Germany",
    "email": "rakeshnagaragattajayanna@gmail.com",
    "phone": "+4917677026053",
    "photo_url": None,
    "skills": [
    "Python", "PySpark", "SQL", "R", "Transformers", "Computer Vision", "NLP",
    "LLMs", "MLOps", "Airflow", "Databricks", "Azure Data Factory",
    "Azure Synapse", "BigQuery", "GCP", "Docker", "Kubernetes", "CI/CD",
    "Power BI", "Tableau", "Looker Studio", "Flask", "Streamlit", "LangChain",
    "OpenAI API", "ChromaDB", "dbt", "Hugging Face Transformers"
],
    "links": {
        "LinkedIn": "https://www.linkedin.com/in/rakesh-shaiva-06186a14b/",
        "GitHub": "https://github.com/Rakesh9901491946",
        "Projects (Repo List)": "https://github.com/Rakesh9901491946/Projects"
    },
    "resume_url": None,
}

# --------------------------------
# DATA — EDIT YOUR CONTENT BELOW
# --------------------------------
PROJECTS = [
    {
        "title": "Radiology Report Generation from Chest X-rays (ViT + GPT-2)",
        "summary": "End-to-end pipeline generating radiology reports from chest X-rays using a VisionEncoderDecoderModel.",
        "tech": ["Python", "PyTorch", "Transformers", "ViT", "GPT-2", "Streamlit"],
        "repo_url": "https://github.com/Rakesh9901491946/Vision-to-Text-Generation-for-Chest-X-rays-using-ViT-GPT2-A-Deep-Learning-Approach-for-Radiology-Re"
    },
    {
        "title": "Twin-Solar: PV Production Forecasting",
        "summary": "Forecasting photovoltaic (PV) output using weather-dependent and independent approaches with LSTM.",
        "tech": ["Python", "LSTM", "Time Series", "ML"],
        "repo_url": "https://github.com/Rakesh9901491946/Twin-Solar"
    },
    {
        "title": "Azure End-to-End Data Engineering Project",
        "summary": "Complete Azure pipeline using Data Factory, Databricks, Synapse Analytics, and Power BI with Medallion Architecture.",
        "tech": ["Azure Data Factory", "Data Lake Gen2", "Databricks", "Synapse", "Power BI"],
        "repo_url": "https://github.com/Rakesh9901491946/Projects/tree/main/Azure%20End-to-End%20Data%20Engineering%20Project%20%7C%20AdventureWorks%20Dataset"
    },
    {
        "title": "Cold Email Generation using Generative AI",
        "summary": "Automated cold email generator using Flask, Llama 3.1, LangChain, and ChromaDB with contextual retrieval.",
        "tech": ["Python", "Flask", "Llama 3.1", "LangChain", "ChromaDB"],
        "repo_url": "https://github.com/Rakesh9901491946/Projects/tree/main/Cold%20Email%20Generator%20using%20Generative%20AI"
    },
    {
        "title": "Azure AI-Powered Document Extraction Pipeline",
        "summary": "Pipeline using Azure Durable Functions and GPT-4 Vision to extract structured data from scanned documents.",
        "tech": ["Azure Functions", "GPT-4 Vision", "Azure Container Apps", "Prompt Engineering"],
        "repo_url": "https://github.com/Rakesh9901491946/Projects/tree/main/Azure%20AI-Powered%20Document%20Extraction%20Pipeline"
    },
    {
        "title": "Speechain – Joint ASR-TTS Research Toolkit",
        "summary": "End-to-end machine speech chain integrating ASR and TTS using PyTorch on LibriSpeech dataset.",
        "tech": ["PyTorch", "Speech Processing", "ASR", "TTS", "Speechain"],
        "repo_url": "https://github.com/Rakesh9901491946/Projects/tree/main/hushhush_project"
    },
    {
        "title": "ESPnet – End-to-End Speech Processing Toolkit",
        "summary": "Trained ASR and TTS models using ESPnet with LibriSpeech/LJSpeech, including Voice Activity Detection (VAD).",
        "tech": ["ESPnet", "Transformer ASR", "TTS", "Speech Translation"],
        "repo_url": ""
    },
    {
        "title": "Spotify Data Analysis Using SQL",
        "summary": "Advanced SQL queries on simulated Spotify DB for customer behavior, trends, and music preference analysis.",
        "tech": ["SQL", "Data Analysis", "Window Functions"],
        "repo_url": "https://github.com/Rakesh9901491946/Projects/tree/main/Spotify%20Data%20Analysis%20Using%20SQL"
    },
    {
        "title": "SmartRecruit: AI-Powered Recruitment Automation Tool",
        "summary": "Python + Flask app to automate candidate evaluation using scraping, clustering, and OpenAI feedback generation.",
        "tech": ["Flask", "Web App", "OpenAI API", "Clustering"],
        "repo_url": "https://github.com/Rakesh9901491946/Projects/tree/main/hushhush_project"
    }
]

DASHBOARDS = [
    {
        "title": "King County House Sales Dashboard",
        "platform": "Tableau/BI",
        "link_url": "https://github.com/Rakesh9901491946/Projects/tree/main/King%20County%20House%20Sales%20Dashboard",
    },
    {
        "title": "Olympics Data Analysis",
        "platform": "Power BI",
        "link_url": "https://github.com/Rakesh9901491946/Projects/tree/main/Olympics_Data_Analysis%20using%20Power%20BI",
    },
]

PUBLICATIONS = [
    {
        "title": "Automated Chest X-ray Report Generation Using Vision-Language Models",
        "venue": "Case Study (2025)",
        "pdf_url": "https://drive.google.com/file/d/1Vw0_aZSvZAZRt1VBNNX-CqYl1ugRkW6j/view?usp=sharing",
        "summary": "End-to-end pipeline, dataset curation, metrics (BLEU/ROUGE/METEOR), and clinical evaluation."
    },
]

# Separate sections for Case Studies and Master Thesis
CASE_STUDIES = [
    {
        "title": "Automated Chest X-ray Report Generation Using Vision-Language Models",
        "venue": "Case Study (2025)",
        "pdf_url": "https://drive.google.com/file/d/1Vw0_aZSvZAZRt1VBNNX-CqYl1ugRkW6j/view?usp=sharing",
        "summary": "End-to-end pipeline, dataset curation, metrics (BLEU/ROUGE/METEOR), and clinical evaluation."
    }
]

MASTER_THESIS = [
    {
        "title": "Radiology Report Generation from Chest X-rays (ViT + GPT-2)",
        "summary": "End-to-end pipeline generating radiology reports from chest X-rays using a VisionEncoderDecoderModel.",
        "tech": ["Python", "PyTorch", "Transformers", "ViT", "GPT-2", "Streamlit"],
        "repo_url": "https://github.com/Rakesh9901491946/Vision-Language-Modeling-for-Chest-X-ray-Report-Generation"
    }
]

# Keep PUBLICATIONS for backward-compatibility/tests (alias of case studies)
PUBLICATIONS = CASE_STUDIES

# ---------------------------
# RENDERING FUNCTIONS
# ---------------------------

def _render_streamlit():
    import streamlit as st
    st.set_page_config(page_title=f"{PROFILE['name']} | Portfolio", page_icon="💼", layout="wide")

    # Header
    st.title(PROFILE["name"])
    st.subheader(PROFILE["role"])

    # Sidebar profile
    with st.sidebar:
        if PROFILE.get("photo_url"):
            st.image(PROFILE["photo_url"], use_container_width=True)
        st.markdown(f"**Location:** {PROFILE['location']}")
        if PROFILE.get("email"): st.markdown(f"**Email:** {PROFILE['email']}")
        if PROFILE.get("phone"): st.markdown(f"**Phone:** {PROFILE['phone']}")
        st.markdown("---")
        st.markdown("**Links**")
        for label, url in PROFILE["links"].items():
            st.markdown(f"- [{label}]({url})")
        if PROFILE.get("resume_url"):
            st.markdown("---")
            st.markdown(f"[Open Résumé (PDF)]({PROFILE['resume_url']})")

    # Tabs
    exp_tab, proj_tab, dash_tab, thesis_tab, case_tab = st.tabs(["💼 Experience", "📁 Projects", "📊 Dashboards", "📖 Master Thesis", "📚 Case Studies"])

    with proj_tab:
        for p in PROJECTS:
            st.markdown(f"### {p['title']}")
            st.write(p["summary"])
            tech = ", ".join(p.get("tech", []))
            if tech:
                st.caption(f"Tech: {tech}")
            if p.get("repo_url"):
                st.markdown(f"[Repository ↗]({p['repo_url']})")
            st.markdown("---")

    with dash_tab:
        for d in DASHBOARDS:
            st.markdown(f"### {d['title']} ({d['platform']})")
            if d.get("link_url"):
                st.markdown(f"[Open dashboard repo ↗]({d['link_url']})")
            st.markdown("---")

    with thesis_tab:
        for thesis in MASTER_THESIS:
            st.markdown(f"### {thesis['title']}")
            st.write(thesis['summary'])
            tech = ", ".join(thesis.get("tech", []))
            if tech:
                st.caption(f"Tech: {tech}")
            if thesis.get("repo_url"):
                st.markdown(f"[Repository ↗]({thesis['repo_url']})")
            st.markdown("---")

    with case_tab:
        for pub in CASE_STUDIES:
            st.markdown(f"### {pub['title']}")
            if pub.get("venue"): st.caption(pub["venue"])
            if pub.get("summary"): st.markdown(pub["summary"])
            if pub.get("pdf_url"): st.markdown(f"[Open PDF ↗]({pub['pdf_url']})")
            if pub.get("repo_url"): st.markdown(f"[Repository ↗]({pub['repo_url']})")
            st.markdown("---")

    st.success("✅ Streamlit app running.")

    with exp_tab:
        for exp in WORK_EXPERIENCE:
            st.markdown(f"### {exp['title']} at {exp['company']}")
            st.caption(f"{exp['location']} | {exp['duration']}")
            for line in exp['details']:
                st.markdown(f"- {line}")
            st.markdown("---")


def _render_static_html(outfile: str = "portfolio.html") -> str:
    """Generate a very simple static HTML page with the portfolio content."""
    html_content = f"""
    <html>
    <head>
      <meta charset='utf-8'/>
      <title>{PROFILE['name']} Portfolio</title>
      <style>
        body {{ font-family: Arial, sans-serif; max-width: 900px; margin: 40px auto; padding:0 16px; }}
        h1 {{ margin-bottom: 0; }}
        .section {{ margin-top: 28px; }}
        .item {{ margin-bottom: 12px; }}
        .meta {{ color: #666; font-size: 0.95em; }}
      </style>
    </head>
    <body>
      <h1>{PROFILE['name']}</h1>
      <h2 class="meta">{PROFILE['role']}</h2>

      <div class="section">
        <h3>Projects</h3>
        <ul>
          {''.join([f'<li class="item"><a href="{p.get("repo_url", "#")}"><strong>{p["title"]}</strong></a> — {p["summary"]}</li>' for p in PROJECTS])}
        </ul>
      </div>

      <div class="section">
        <h3>Dashboards</h3>
        <ul>
          {''.join([f'<li class="item"><a href="{d.get("link_url", "#")}"><strong>{d["title"]}</strong></a> ({d["platform"]})</li>' for d in DASHBOARDS])}
        </ul>
      </div>

      <div class="section">
        <h3>Publications</h3>
        <ul>
          {''.join([f'<li class="item"><a href="{pub.get("pdf_url", "#")}"><strong>{pub["title"]}</strong></a>{" — " + pub.get("venue", "") if pub.get("venue") else ""}</li>' for pub in PUBLICATIONS])}
        </ul>
      </div>

      <p class="meta">Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
    </body>
    </html>
    """
    with open(outfile, "w", encoding="utf-8") as f:
        f.write(html_content)
    return outfile

# ---------------------------
# MAIN ENTRY (dual-mode)
# ---------------------------
try:
    import streamlit  # only to check availability; not used directly below
    _render_streamlit()
except ModuleNotFoundError:
    # Fallback: static HTML output (NO sys.exit here; allow tests to run)
    outfile = _render_static_html("portfolio.html")
    print(f"⚠️ Streamlit not available. Static HTML generated: {outfile}")

# ---------------------------
# TESTS (keep existing; add more)
# ---------------------------
if __name__ == "__main__":
    # --- Existing test (UNCHANGED) ---
    assert PROFILE["name"] in (open("portfolio.html").read() if 'streamlit' not in sys.modules else PROFILE["name"])
    print("✅ Basic test passed.")

    # --- Additional tests ---
    def _looks_like_url(u: str) -> bool:
        return isinstance(u, str) and u.startswith(("http://", "https://"))

    # Test 1: Profile has a non-empty name
    assert isinstance(PROFILE["name"], str) and PROFILE["name"].strip(), "Profile name must be non-empty"

    # Test 2: Projects contain required keys and titles are unique
    titles = set()
    for p in PROJECTS:
        assert "title" in p and p["title"].strip(), "Every project needs a title"
        assert "summary" in p and p["summary"].strip(), "Every project needs a summary"
        assert p["title"] not in titles, "Project titles must be unique"
        titles.add(p["title"])

    # Test 3: Links look like URLs
    for _, url in PROFILE["links"].items():
        assert _looks_like_url(url), f"Bad link URL: {url}"
    for p in PROJECTS:
        if p.get("repo_url"):
            assert _looks_like_url(p["repo_url"]), f"Bad repo URL: {p['repo_url']}"
    for d in DASHBOARDS:
        if d.get("link_url"):
            assert _looks_like_url(d["link_url"]), f"Bad dashboard URL: {d['link_url']}"
    for pub in PUBLICATIONS:
        if pub.get("pdf_url"):
            assert _looks_like_url(pub["pdf_url"]), f"Bad publication URL: {pub['pdf_url']}"

    # Test 4: Fallback created a file with at least one project title when Streamlit is absent
    if 'streamlit' not in sys.modules:
        assert os.path.exists("portfolio.html"), "portfolio.html should be created in fallback mode"
        html = open("portfolio.html", encoding="utf-8").read()
        assert any(p['title'] in html for p in PROJECTS), "portfolio.html should list project titles"

    # Test 5: Static generator returns the outfile path and writes non-empty contents
    out = _render_static_html("_test_portfolio.html")
    assert os.path.exists(out), "Static generator must create the output file"
    assert os.path.getsize(out) > 0, "Generated HTML must not be empty"
    os.remove(out)

    print("✅ All additional tests passed.")
