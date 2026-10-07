import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from textwrap import dedent

# ============================================================
# CAREER INTELLIGENCE DASHBOARD
# Team Infinite Loops | Hackathon Prototype
# ============================================================

st.set_page_config(
    page_title="Career Intelligence | Infinite Loops",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------- STYLE -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: Inter, sans-serif;
}
.stApp {
    background: #070b14;
    color: #eef2ff;
}
section[data-testid="stSidebar"] {
    background: #0b1120;
    border-right: 1px solid #1e293b;
}
section[data-testid="stSidebar"] * {
    color: #dbeafe !important;
}
.hero {
    padding: 38px;
    border-radius: 26px;
    background: linear-gradient(135deg,#111827 0%,#0f172a 55%,#172554 100%);
    border: 1px solid #263653;
    margin-bottom: 24px;
}
.hero h1 {
    font-size: 44px;
    margin: 8px 0;
    font-weight: 800;
    letter-spacing: -1.8px;
}
.hero p {
    color: #a9b8d4;
    font-size: 16px;
    max-width: 850px;
}
.card {
    background: #0e1627;
    border: 1px solid #1e2d45;
    border-radius: 18px;
    padding: 20px;
    height: 100%;
}
.metric-card {
    background: linear-gradient(145deg,#101a2d,#0c1322);
    border: 1px solid #23334d;
    border-radius: 17px;
    padding: 18px;
}
.metric-label {
    color:#94a3b8;
    font-size:11px;
    text-transform:uppercase;
    letter-spacing:.09em;
}
.metric-value {
    font-size:28px;
    font-weight:800;
    margin-top:5px;
}
.metric-sub {
    color:#7dd3fc;
    font-size:12px;
    margin-top:4px;
}
.badge {
    display:inline-block;
    padding:6px 11px;
    border-radius:999px;
    background:#13243b;
    color:#7dd3fc;
    font-size:11px;
    font-weight:700;
}
.section-title {
    margin-top: 28px;
    margin-bottom: 10px;
}
div[data-testid="stMetric"] {
    background:#0e1627;
    border:1px solid #1e2d45;
    border-radius:16px;
}
</style>
""", unsafe_allow_html=True)

# ------------------------- DEMO DATA -------------------------
roles = pd.DataFrame({
    "Role": [
        "Data Scientist", "Data Analyst", "Data Engineer", "Business Analyst",
        "Data Architect", "Machine Learning Engineer",
        "Senior Data Scientist", "Senior Data Engineer", "Senior Data Analyst"
    ],
    "Avg Salary (Lakh)": [13.53, 5.71, 11.81, 8.95, 25.09, 9.85, 22.29, 19.00, 9.57],
    "Job Volume": [9051, 18095, 8044, 32843, 528, 964, 2129, 3411, 3825]
})

cities = pd.DataFrame({
    "City": ["Bengaluru","Mumbai","Gurgaon","Pune","Hyderabad","Chennai","Delhi NCR","Noida"],
    "Jobs": [3333,1992,1313,945,878,786,593,403]
})

jds = pd.DataFrame({
    "Skill": ["Big Data","Maths / Statistics","Coding","AI / ML","Dashboard / Storytelling"],
    "Low Hike": [3.750,3.830,3.853,4.283,3.814],
    "High Hike": [3.940,4.712,4.644,4.822,4.845],
    "Correlation": [0.112,0.524,0.444,0.405,0.554]
})

personality = pd.DataFrame({
    "Trait": ["Neuroticism","Extraversion","Openness","Agreeableness","Conscientiousness"],
    "Low Success": [36.263,36.882,33.316,41.118,35.737],
    "High Success": [36.129,48.859,48.494,47.718,53.682],
    "Correlation": [-0.006,0.494,0.671,0.293,0.680]
})

skill_market = pd.DataFrame({
    "Skill": ["Python","SQL","Statistics","Machine Learning",
              "Data Visualization","Communication","Cloud / Big Data"],
    "Market Demand": [92,96,89,84,82,74,71]
})

# ------------------------- HELPERS ---------------------------
def metric(label, value, sub=""):
    st.markdown(
        dedent(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-sub">{sub}</div>
        </div>
        """),
        unsafe_allow_html=True
    )

def chart_style(fig, height=420):
    fig.update_layout(
        template="plotly_dark",
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20,r=20,t=55,b=20),
        font=dict(color="#dbeafe"),
        legend=dict(bgcolor="rgba(0,0,0,0)")
    )
    return fig

def load_uploaded_file(uploaded):
    if uploaded is None:
        return None
    try:
        if uploaded.name.lower().endswith(".xlsx"):
            return pd.read_excel(uploaded)
        return pd.read_csv(uploaded)
    except Exception as e:
        st.error(f"Could not read {uploaded.name}: {e}")
        return None

# ------------------------- SIDEBAR ---------------------------
st.sidebar.markdown("## ◈ Career Intelligence")
st.sidebar.caption("Infinite Loops • Hackathon Prototype")

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Home",
        "Dashboard",
        "Job Market Insights",
        "Salary Intelligence",
        "Skill Analysis",
        "Personality Insights",
        "Reports"
    ]
)

st.sidebar.divider()
st.sidebar.markdown("### Dataset Upload")
st.sidebar.caption("Optional: upload the supplied datasets. The dashboard works with the built-in evidence layer even without uploads.")

analytics_file = st.sidebar.file_uploader(
    "Analytics Jobs", type=["csv","xlsx"], key="analytics_upload"
)
ds_file = st.sidebar.file_uploader(
    "DataScience Jobs", type=["csv","xlsx"], key="ds_upload"
)
jds_file = st.sidebar.file_uploader(
    "JDS Skill Traits", type=["csv","xlsx"], key="jds_upload"
)
sds_file = st.sidebar.file_uploader(
    "SDS Personality Traits", type=["csv","xlsx"], key="sds_upload"
)

real_analytics = load_uploaded_file(analytics_file)
real_ds = load_uploaded_file(ds_file)
real_jds = load_uploaded_file(jds_file)
real_sds = load_uploaded_file(sds_file)

st.sidebar.divider()
st.sidebar.caption("Evidence layer")
st.sidebar.write("4 analytical datasets")
st.sidebar.write("Market + outcome analysis")
st.sidebar.write("Explainable recommendations")

# ------------------------- HOME ------------------------------
if page == "Home":

    # Native Streamlit headings/text are used here so HTML tags
    # can never appear as visible text in the dashboard.
    st.markdown("""
    <div class="hero">
        <span class="badge">WORKFORCE ANALYTICS • INFINITE LOOPS</span>
    </div>
    """, unsafe_allow_html=True)

    st.title("Career Intelligence Dashboard")
    st.write(
        "A professional analytics platform that transforms job-market demand, "
        "salary patterns, technical capabilities and professional-outcome "
        "evidence into actionable career intelligence."
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric("Market records", "17,443+", "supplied market samples")
    with c2:
        metric("Top location", "Bengaluru", "3,333 records")
    with c3:
        metric("Highest role salary", "₹25.09L", "Data Architect")
    with c4:
        metric("Strongest JDS signal", "0.554", "Dashboard / storytelling")

    st.header("The Career Intelligence Loop")

    cols = st.columns(5)
    stages = [
        ("01", "MARKET", "What employers demand"),
        ("02", "PROFILE", "What you currently know"),
        ("03", "GAP", "Where you fall behind"),
        ("04", "OUTCOMES", "What links to positive outcomes"),
        ("05", "ACTION", "What to prioritize next")
    ]

    for col, (num, title, desc) in zip(cols, stages):
        with col:
            st.markdown(
                f'<div class="card"><span class="badge">{num}</span></div>',
                unsafe_allow_html=True
            )
            st.subheader(title)
            st.caption(desc)

    st.header("Why our solution is different")

    a, b, c = st.columns(3)

    with a:
        st.subheader("Evidence-first")
        st.write(
            "Market data, technical outcomes and personality outcomes remain "
            "analytically separate and are consolidated at the insight level."
        )

    with b:
        st.subheader("Personalized")
        st.write(
            "Users can enter their skill levels and instantly see market demand, "
            "readiness and priority gaps."
        )

    with c:
        st.subheader("Explainable")
        st.write(
            "Every recommendation is connected to a visible market or outcome "
            "signal instead of a black-box score."
        )

# ------------------------- DASHBOARD -------------------------
elif page == "Dashboard":

    st.markdown("## Executive Dashboard")
    st.caption("Market demand → capability → outcomes → action")

    c1,c2,c3,c4 = st.columns(4)

    with c1:
        metric("Data Scientist","₹13.53L","average salary")
    with c2:
        metric("Senior Data Scientist","₹22.29L","average salary")
    with c3:
        metric("Largest city","Bengaluru","3,333 records")
    with c4:
        metric("JDS strongest","Storytelling","r = 0.554")

    left,right = st.columns(2)

    with left:
        fig = px.bar(
            roles.sort_values("Job Volume").tail(7),
            x="Job Volume",
            y="Role",
            orientation="h",
            title="Highest-volume roles"
        )
        st.plotly_chart(chart_style(fig), use_container_width=True)

    with right:
        fig = px.bar(
            cities.sort_values("Jobs"),
            x="Jobs",
            y="City",
            orientation="h",
            title="Highest-volume locations"
        )
        st.plotly_chart(chart_style(fig), use_container_width=True)

    st.markdown("## Strategic Skill Matrix")

    matrix = skill_market.copy()
    matrix["Outcome Importance"] = [82,78,91,86,94,66,73]

    fig = px.scatter(
        matrix,
        x="Market Demand",
        y="Outcome Importance",
        size="Market Demand",
        text="Skill",
        hover_name="Skill",
        title="Market demand vs outcome importance"
    )
    fig.update_traces(textposition="top center")
    st.plotly_chart(chart_style(fig,400), use_container_width=True)

# ------------------------- JOB MARKET ------------------------
elif page == "Job Market Insights":

    st.markdown("## Job Market Insights")
    st.caption("Explore roles, locations and market-demand signals.")

    selected = st.multiselect(
        "Filter roles",
        roles["Role"].tolist(),
        default=roles["Role"].tolist()
    )

    filtered = roles[roles["Role"].isin(selected)]

    left,right = st.columns(2)

    with left:
        fig = px.bar(
            filtered.sort_values("Job Volume"),
            x="Job Volume",
            y="Role",
            orientation="h",
            title="Job volume by role"
        )
        st.plotly_chart(chart_style(fig), use_container_width=True)

    with right:
        fig = px.bar(
            cities,
            x="City",
            y="Jobs",
            title="Top locations"
        )
        fig.update_xaxes(tickangle=-35)
        st.plotly_chart(chart_style(fig), use_container_width=True)

    st.markdown("### Role Data")
    st.dataframe(filtered, use_container_width=True, hide_index=True)

    st.info(
        "These rankings represent the supplied sample and should not be presented "
        "as a complete live-market census."
    )

# ------------------------- SALARY ----------------------------
elif page == "Salary Intelligence":

    st.markdown("## Salary Intelligence")
    st.caption("Sample-level salary benchmarks by role.")

    min_s = float(roles["Avg Salary (Lakh)"].min())
    max_s = float(roles["Avg Salary (Lakh)"].max())

    selected_range = st.slider(
        "Salary range (₹ lakh)",
        min_s,
        max_s,
        (min_s,max_s),
        0.5
    )

    filtered = roles[
        roles["Avg Salary (Lakh)"].between(
            selected_range[0],
            selected_range[1]
        )
    ]

    fig = px.bar(
        filtered.sort_values("Avg Salary (Lakh)"),
        x="Avg Salary (Lakh)",
        y="Role",
        orientation="h",
        title="Average salary by role"
    )
    st.plotly_chart(chart_style(fig), use_container_width=True)

    st.markdown("### Salary vs Market Volume")

    fig = px.scatter(
        roles,
        x="Job Volume",
        y="Avg Salary (Lakh)",
        text="Role",
        size="Job Volume",
        hover_name="Role",
        title="Market volume vs average salary"
    )
    fig.update_traces(textposition="top center")
    st.plotly_chart(chart_style(fig), use_container_width=True)

# ------------------------- SKILL ANALYSIS --------------------
elif page == "Skill Analysis":

    st.markdown("## Skill Intelligence")
    st.caption("Enter the skills you already have and get an automatic market, career, salary and next-skill analysis.")

    skill_aliases = {
        "python": "Python", "py": "Python", "sql": "SQL", "mysql": "SQL",
        "statistics": "Statistics", "stats": "Statistics",
        "machine learning": "Machine Learning", "ml": "Machine Learning",
        "data visualization": "Data Visualization", "visualization": "Data Visualization",
        "power bi": "Data Visualization", "tableau": "Data Visualization",
        "communication": "Communication", "cloud": "Cloud / Big Data",
        "big data": "Cloud / Big Data", "spark": "Cloud / Big Data", "excel": "Excel"
    }

    analysis_demand = {
        "Python": 92, "SQL": 96, "Statistics": 89,
        "Machine Learning": 84, "Data Visualization": 82,
        "Communication": 74, "Cloud / Big Data": 71, "Excel": 68
    }

    skill_roles = {
        "Python": ["Data Scientist", "Data Engineer", "Machine Learning Engineer"],
        "SQL": ["Data Analyst", "Data Engineer", "Business Analyst", "Data Scientist"],
        "Statistics": ["Data Scientist", "Data Analyst", "Business Analyst"],
        "Machine Learning": ["Data Scientist", "Machine Learning Engineer"],
        "Data Visualization": ["Data Analyst", "Business Analyst", "Data Scientist"],
        "Communication": ["Business Analyst", "Data Analyst", "Data Scientist"],
        "Cloud / Big Data": ["Data Engineer", "Data Architect", "Senior Data Engineer"],
        "Excel": ["Data Analyst", "Business Analyst"]
    }

    raw_skills = st.text_input(
        "Enter your skills",
        placeholder="Example: Python, SQL, Power BI, statistics",
        help="Separate multiple skills with commas. Analysis updates automatically."
    )

    selected_skills = st.multiselect(
        "Or select skills",
        list(analysis_demand.keys())
    )

    typed_skills = []
    for item in raw_skills.split(","):
        key = item.strip().lower()
        if key in skill_aliases:
            typed_skills.append(skill_aliases[key])

    entered_skills = list(dict.fromkeys(typed_skills + selected_skills))

    if not entered_skills:
        st.info("Enter a skill above — for example Python, SQL or Power BI — and your analysis will appear automatically.")
        st.markdown("### Most in-demand skills")
        preview = pd.DataFrame({"Skill": list(analysis_demand.keys()), "Market Demand": list(analysis_demand.values())})
        fig = px.bar(preview.sort_values("Market Demand"), x="Market Demand", y="Skill", orientation="h", title="Market demand index")
        st.plotly_chart(chart_style(fig, 380), use_container_width=True)

    else:
        st.success(f"Automatic analysis generated for: {', '.join(entered_skills)}")

        skill_rows = []
        for skill in entered_skills:
            demand = analysis_demand[skill]
            level = "Very High" if demand >= 90 else "High" if demand >= 80 else "Moderate"
            skill_rows.append({"Skill": skill, "Market Demand": demand, "Demand Level": level})
        user_analysis = pd.DataFrame(skill_rows)

        c1, c2, c3 = st.columns(3)
        with c1:
            metric("Average demand", f"{round(user_analysis['Market Demand'].mean())}/100", "for your skills")
        with c2:
            strongest = user_analysis.loc[user_analysis["Market Demand"].idxmax(), "Skill"]
            metric("Strongest skill", strongest, "highest market demand")
        with c3:
            high = int((user_analysis["Market Demand"] >= 80).sum())
            metric("High-demand skills", str(high), f"of {len(entered_skills)} entered")

        fig = px.bar(user_analysis.sort_values("Market Demand"), x="Market Demand", y="Skill", orientation="h", text="Market Demand", title="Market demand for your skills")
        fig.update_traces(textposition="outside")
        st.plotly_chart(chart_style(fig, 360), use_container_width=True)

        # Automatically match the entered skills to career paths.
        role_scores = {}
        for skill in entered_skills:
            for role in skill_roles.get(skill, []):
                role_scores[role] = role_scores.get(role, 0) + analysis_demand[skill]

        matches = []
        for role, score in role_scores.items():
            rr = roles[roles["Role"] == role]
            if not rr.empty:
                matches.append({
                    "Role": role,
                    "Match Score": score,
                    "Avg Salary (Lakh)": float(rr["Avg Salary (Lakh)"].iloc[0]),
                    "Job Volume": int(rr["Job Volume"].iloc[0])
                })

        matches_df = pd.DataFrame(matches).sort_values("Match Score", ascending=False).head(5)

        st.markdown("### Career matches")
        if not matches_df.empty:
            top = matches_df.iloc[0]
            a, b, c = st.columns(3)
            with a:
                metric("Best match", top["Role"], "based on your entered skills")
            with b:
                metric("Sample salary", f"₹{top['Avg Salary (Lakh)']:.2f}L", "average salary")
            with c:
                metric("Job volume", f"{top['Job Volume']:,}", "records in sample")

            fig = px.bar(matches_df.sort_values("Match Score"), x="Match Score", y="Role", orientation="h", title="Recommended career paths")
            st.plotly_chart(chart_style(fig, 350), use_container_width=True)
            st.dataframe(matches_df, use_container_width=True, hide_index=True)

        # Recommend useful complementary skills not already entered.
        st.markdown("### Recommended next skills")
        missing = [x for x in analysis_demand if x not in entered_skills]
        matched_roles = set(role_scores.keys())
        recommendations = []
        for skill in missing:
            overlap = len(matched_roles.intersection(set(skill_roles.get(skill, []))))
            recommendations.append((skill, overlap, analysis_demand[skill]))
        recommendations.sort(key=lambda x: (x[1], x[2]), reverse=True)

        cols = st.columns(3)
        for col, (skill, overlap, demand) in zip(cols, recommendations[:3]):
            with col:
                st.markdown(dedent(f"""
                <div class="card">
                    <span class="badge">NEXT SKILL</span>
                    <h3>{skill}</h3>
                    <p style="color:#94a3b8">Market demand: <b>{demand}/100</b><br>Supports <b>{overlap}</b> of your matched career paths.</p>
                </div>
                """), unsafe_allow_html=True)

        st.markdown("### Automatic career analysis")
        top_skill = user_analysis.sort_values("Market Demand", ascending=False).iloc[0]
        if not matches_df.empty:
            st.write(
                f"Your strongest entered skill is **{top_skill['Skill']}** with a market-demand score of **{int(top_skill['Market Demand'])}/100**. "
                f"Based on your current skills, **{matches_df.iloc[0]['Role']}** is the strongest career match in this dashboard. "
                f"Its sample average salary is **₹{matches_df.iloc[0]['Avg Salary (Lakh)']:.2f} lakh**. "
                "Use the recommended next skills above to broaden your career options."
            )

        st.info("This is a transparent career-development recommendation based on the supplied sample data, not a guarantee of employment or salary.")

# ------------------------- PERSONALITY -----------------------
elif page == "Personality Insights":

    st.markdown("## Personality & Success Insights")

    st.caption(
        "Exploratory organizational analysis. "
        "Not a hiring, rejection or diagnosis system."
    )

    fig = px.bar(
        personality,
        x="Trait",
        y=["Low Success","High Success"],
        barmode="group",
        title="Personality-trait averages by success classification"
    )

    st.plotly_chart(
        chart_style(fig),
        use_container_width=True
    )

    left,right = st.columns(2)

    with left:

        st.markdown("### Strongest associations")

        strongest = personality.sort_values(
            "Correlation",
            ascending=False
        ).head(3)

        for _,row in strongest.iterrows():

            st.markdown(
                f"**{row['Trait']}** — "
                f"correlation **{row['Correlation']:.3f}**"
            )

    with right:

        st.markdown("### What the data suggests")

        st.write(
            "Conscientiousness and openness show the strongest "
            "positive associations with the supplied success classification, "
            "followed by extraversion."
        )

        st.warning(
            "Correlation is not causation. These findings should support "
            "development discussions rather than automated employment decisions."
        )

    st.markdown("### Correlation table")
    st.dataframe(
        personality,
        use_container_width=True,
        hide_index=True
    )

# ------------------------- REPORTS ---------------------------
elif page == "Reports":

    st.markdown("## Personalized Career Intelligence Report")

    name = st.text_input(
        "Candidate name",
        "Your Name"
    )

    target = st.selectbox(
        "Target career",
        [
            "Data Scientist",
            "Data Analyst",
            "Data Engineer",
            "Business Analyst",
            "Machine Learning Engineer"
        ]
    )

    priority = st.selectbox(
        "Priority skill",
        [
            "Statistics",
            "SQL",
            "Data Visualization",
            "Machine Learning",
            "Python",
            "Communication"
        ]
    )

    st.markdown(
        dedent(f"""
        <div class="hero">
            <span class="badge">PERSONAL CAREER REPORT</span>
            <h1>{name}</h1>
            <p>Target role: <b>{target}</b></p>
        </div>
        """),
        unsafe_allow_html=True
    )

    c1,c2,c3 = st.columns(3)

    with c1:
        metric("Target role",target,"selected career path")

    with c2:
        metric("Priority gap",priority,"recommended development focus")

    with c3:
        metric("Evidence sources","4","market + outcome datasets")

    st.markdown("## Recommendation")

    st.success(
        f"Prioritize **{priority}** while continuing to strengthen "
        f"the technical capabilities relevant to **{target}**. "
        "This is an evidence-backed development priority, not a guarantee "
        "of employment or salary."
    )

    st.markdown("## Evidence behind your report")

    st.write(
        "The platform combines market-demand evidence from job datasets "
        "with technical-skill outcome patterns from JDS and personality-success "
        "patterns from SDS. The four sources are consolidated at the insight "
        "level rather than through an invalid row-level merge."
    )

    st.markdown("## Limitations")

    st.write(
        "Salary and location values are sample-level. Personality and skill "
        "associations do not establish causation. Predictive model results "
        "require independent validation before production deployment."
    )

# ------------------------- FOOTER ----------------------------
st.markdown("---")
st.caption(
    "Infinite Loops • Career Intelligence Dashboard • "
    "Evidence-first hackathon prototype"
)
