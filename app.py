import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Tamil Nadu Election Results",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

h1, h2, h3 {
    font-family: 'Averia Libre', sans-serif !important;
}

.block-container { padding-top: 2rem; padding-bottom: 2rem; }

/* Metric cards */
[data-testid="metric-container"] {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    color: white;
}
[data-testid="metric-container"] label {
    color: #94a3b8 !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #f1f5f9 !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0f172a;
    border-right: 1px solid #1e293b;
}
section[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stRadio label {
    color: #94a3b8 !important;
    font-size: 0.7rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

/* Page title banner */
.page-banner {
    background: linear-gradient(135deg, #0f172a 0%, #1a1040 50%, #0f172a 100%);
    border: 1px solid #7c3aed33;
    border-radius: 16px;
    padding: 1.5rem 2rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.page-banner::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, #7c3aed22 0%, transparent 70%);
    pointer-events: none;
}
.page-banner h1 {
    font-family: 'Syne', sans-serif;
    font-size: 1.9rem;
    font-weight: 800;
    color: #f8fafc;
    margin: 0 0 0.3rem 0;
    letter-spacing: -0.02em;
}
.page-banner p {
    color: #94a3b8;
    font-size: 0.875rem;
    margin: 0;
}
.accent { color: #a78bfa; }

/* Chart container */
.chart-card {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 1rem;
    margin-bottom: 1rem;
}

/* Divider */
hr { border-color: #1e293b; }
</style>
""", unsafe_allow_html=True)

# ── Data Loading ───────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("Election_Results_Clean.csv")
    df["SEX"] = df["SEX"].fillna("UNKNOWN")
    df["CATEGORY"] = df["CATEGORY"].fillna("UNKNOWN")
    return df

df = load_data()

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🗳️ TN Elections")
    st.markdown("---")
    page = st.radio(
        "NAVIGATE",
        ["Overview", "Party Analysis", "Constituency Deep Dive", "Candidate Explorer", "Voter Demographics"],
        label_visibility="visible",
    )
    st.markdown("---")
    st.markdown("### Filters")
    parties = sorted(df["PARTY"].unique())
    selected_parties = st.multiselect("Filter by Party", parties, default=[], placeholder="All parties")
    cat_options = sorted(df["CATEGORY"].dropna().unique())
    selected_cats = st.multiselect("Filter by Category", cat_options, default=[], placeholder="All categories")

    filtered_df = df.copy()
    if selected_parties:
        filtered_df = filtered_df[filtered_df["PARTY"].isin(selected_parties)]
    if selected_cats:
        filtered_df = filtered_df[filtered_df["CATEGORY"].isin(selected_cats)]

    st.markdown("---")
    st.caption(f"Showing **{len(filtered_df):,}** of **{len(df):,}** records")

# ── PLOTLY THEME ───────────────────────────────────────────────────────────────
PLOT_THEME = dict(
    paper_bgcolor="#0f172a",
    plot_bgcolor="#0f172a",
    font=dict(family="DM Sans", color="#94a3b8", size=12),
    title_font=dict(family="Syne", color="#f1f5f9", size=15),
    legend=dict(bgcolor="#1e293b", bordercolor="#334155", borderwidth=1),
    colorway=["#a78bfa", "#34d399", "#60a5fa", "#f472b6", "#fb923c", "#facc15", "#2dd4bf", "#c084fc"],
)

COLOR_SEQ = ["#a78bfa", "#34d399", "#60a5fa", "#f472b6", "#fb923c", "#facc15", "#2dd4bf", "#818cf8"]

def apply_theme(fig):
    fig.update_layout(**PLOT_THEME)
    fig.update_xaxes(gridcolor="#1e293b", zerolinecolor="#334155")
    fig.update_yaxes(gridcolor="#1e293b", zerolinecolor="#334155")
    return fig

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
if page == "Overview":
    st.markdown("""
    <div class="page-banner">
        <h1>Tamil Nadu <span class="accent">Election Results</span></h1>
        <p>Comprehensive breakdown of candidate performance across all constituencies</p>
    </div>
    """, unsafe_allow_html=True)

    # KPI row
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Candidates", f"{len(filtered_df['CANDIDATE_NAME'].unique()):,}")
    col2.metric("Constituencies", f"{filtered_df['AC_NO'].nunique():,}")
    col3.metric("Parties", f"{filtered_df['PARTY'].nunique():,}")
    total_votes = filtered_df["TOTAL_VOTES"].sum()
    col4.metric("Total Votes Cast", f"{total_votes/1e6:.2f}M")
    avg_turnout = filtered_df.drop_duplicates("AC_NO")["VOTES_POLLED_PCT"].mean()
    col5.metric("Avg Turnout %", f"{avg_turnout:.1f}%")

    st.markdown("<br>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        # Top 10 parties by total votes
        party_votes = (
            filtered_df.groupby("PARTY")["TOTAL_VOTES"].sum()
            .sort_values(ascending=False).head(10).reset_index()
        )
        fig = px.bar(
            party_votes, x="TOTAL_VOTES", y="PARTY", orientation="h",
            title="Top 10 Parties by Total Votes",
            labels={"TOTAL_VOTES": "Total Votes", "PARTY": ""},
            color="TOTAL_VOTES", color_continuous_scale=["#1e293b", "#7c3aed", "#a78bfa"],
        )
        fig.update_layout(yaxis=dict(autorange="reversed"), coloraxis_showscale=False, height=420)
        apply_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        # Turnout distribution
        turnout_df = filtered_df.drop_duplicates("AC_NO")[["AC_NAME", "VOTES_POLLED_PCT"]].dropna()
        fig = px.histogram(
            turnout_df, x="VOTES_POLLED_PCT", nbins=30,
            title="Constituency Turnout Distribution",
            labels={"VOTES_POLLED_PCT": "Voter Turnout %", "count": "Constituencies"},
            color_discrete_sequence=["#a78bfa"],
        )
        fig.update_traces(marker_line_color="#7c3aed", marker_line_width=1)
        fig.update_layout(height=420)
        apply_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

    # Candidates per party (top 20)
    cand_count = filtered_df[~filtered_df["PARTY"].isin(["NOTA", "IND"])].groupby("PARTY")["CANDIDATE_NAME"].count().sort_values(ascending=False).head(15).reset_index()
    cand_count.columns = ["PARTY", "CANDIDATES"]
    fig = px.bar(
        cand_count, x="PARTY", y="CANDIDATES",
        title="Number of Candidates Fielded — Top 15 Parties",
        color="CANDIDATES", color_continuous_scale=["#1e293b", "#0ea5e9", "#60a5fa"],
        labels={"CANDIDATES": "Candidates", "PARTY": "Party"},
    )
    fig.update_layout(coloraxis_showscale=False, height=350)
    apply_theme(fig)
    st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: PARTY ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Party Analysis":
    st.markdown("""
    <div class="page-banner">
        <h1>Party <span class="accent">Analysis</span></h1>
        <p>Vote share, candidate counts, and performance metrics by political party</p>
    </div>
    """, unsafe_allow_html=True)

    top_n = st.slider("Show Top N Parties", min_value=5, max_value=20, value=10)

    party_stats = (
        filtered_df.groupby("PARTY")
        .agg(
            Total_Votes=("TOTAL_VOTES", "sum"),
            Candidates=("CANDIDATE_NAME", "count"),
            Avg_Votes=("TOTAL_VOTES", "mean"),
            Constituencies=("AC_NO", "nunique"),
        )
        .sort_values("Total_Votes", ascending=False)
        .head(top_n)
        .reset_index()
    )

    col1, col2 = st.columns(2)

    with col1:
        fig = px.pie(
            party_stats, values="Total_Votes", names="PARTY",
            title=f"Vote Share — Top {top_n} Parties",
            color_discrete_sequence=COLOR_SEQ,
            hole=0.45,
        )
        fig.update_traces(textposition="outside", textinfo="percent+label", textfont_size=11)
        fig.update_layout(height=440, showlegend=False)
        apply_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.scatter(
            party_stats, x="Candidates", y="Total_Votes",
            size="Avg_Votes", color="PARTY", text="PARTY",
            title="Candidates Fielded vs. Total Votes Won",
            labels={"Total_Votes": "Total Votes", "Candidates": "# Candidates"},
            color_discrete_sequence=COLOR_SEQ,
        )
        fig.update_traces(textposition="top center", textfont_size=9)
        fig.update_layout(height=440, showlegend=False)
        apply_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

    # Average votes per candidate
    fig = px.bar(
        party_stats.sort_values("Avg_Votes", ascending=False),
        x="PARTY", y="Avg_Votes",
        title=f"Average Votes per Candidate — Top {top_n} Parties",
        color="Avg_Votes", color_continuous_scale=["#1e293b", "#10b981", "#34d399"],
        labels={"Avg_Votes": "Avg Votes", "PARTY": "Party"},
    )
    fig.update_layout(coloraxis_showscale=False, height=350)
    apply_theme(fig)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Party Stats Table")
    st.dataframe(
        party_stats.rename(columns={
            "PARTY": "Party", "Total_Votes": "Total Votes",
            "Candidates": "Candidates", "Avg_Votes": "Avg Votes/Candidate",
            "Constituencies": "Constituencies Contested"
        }).style.format({"Total Votes": "{:,.0f}", "Avg Votes/Candidate": "{:,.0f}"}),
        use_container_width=True, hide_index=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: CONSTITUENCY DEEP DIVE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Constituency Deep Dive":
    st.markdown("""
    <div class="page-banner">
        <h1>Constituency <span class="accent">Deep Dive</span></h1>
        <p>Explore candidate-level results for any constituency</p>
    </div>
    """, unsafe_allow_html=True)

    constituencies = sorted(filtered_df["AC_NAME"].unique())
    selected_ac = st.selectbox("Select Constituency", constituencies)

    ac_df = filtered_df[filtered_df["AC_NAME"] == selected_ac].sort_values("TOTAL_VOTES", ascending=False)

    if not ac_df.empty:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("AC Number", int(ac_df["AC_NO"].iloc[0]))
        col2.metric("Total Candidates", len(ac_df))
        col3.metric("Total Votes Cast", f"{ac_df['TOTAL_VOTES'].sum():,}")
        col4.metric("Voter Turnout", f"{ac_df['VOTES_POLLED_PCT'].max():.1f}%")

        col_a, col_b = st.columns([3, 2])

        with col_a:
            fig = px.bar(
                ac_df, x="TOTAL_VOTES", y="CANDIDATE_NAME", orientation="h",
                color="PARTY", title=f"Vote Count by Candidate — {selected_ac}",
                labels={"TOTAL_VOTES": "Total Votes", "CANDIDATE_NAME": ""},
                color_discrete_sequence=COLOR_SEQ,
                text="TOTAL_VOTES",
            )
            fig.update_traces(texttemplate="%{text:,}", textposition="outside")
            fig.update_layout(yaxis=dict(autorange="reversed"), height=max(300, len(ac_df) * 38), showlegend=True)
            apply_theme(fig)
            st.plotly_chart(fig, use_container_width=True)

        with col_b:
            fig = px.pie(
                ac_df, values="TOTAL_VOTES", names="CANDIDATE_NAME",
                title="Vote Share",
                color_discrete_sequence=COLOR_SEQ, hole=0.4,
            )
            fig.update_traces(textinfo="percent+label", textfont_size=10)
            fig.update_layout(height=max(300, len(ac_df) * 38), showlegend=False)
            apply_theme(fig)
            st.plotly_chart(fig, use_container_width=True)

        # General vs Postal votes
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name="General Votes", x=ac_df["CANDIDATE_NAME"], y=ac_df["GENERAL_VOTES"],
            marker_color="#a78bfa",
        ))
        fig.add_trace(go.Bar(
            name="Postal Votes", x=ac_df["CANDIDATE_NAME"], y=ac_df["POSTAL_VOTES"],
            marker_color="#34d399",
        ))
        fig.update_layout(
            barmode="stack", title="General vs Postal Votes Split",
            xaxis_title="", yaxis_title="Votes", height=350,
        )
        apply_theme(fig)
        st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: CANDIDATE EXPLORER
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Candidate Explorer":
    st.markdown("""
    <div class="page-banner">
        <h1>Candidate <span class="accent">Explorer</span></h1>
        <p>Search, rank, and analyse individual candidate performance</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        search = st.text_input("Search Candidate Name", placeholder="Type name...")
    with col2:
        top_n_cand = st.slider("Top N Candidates", 10, 50, 20)

    result_df = filtered_df.copy()
    if search:
        result_df = result_df[result_df["CANDIDATE_NAME"].str.contains(search, case=False, na=False)]

    top_candidates = result_df.nlargest(top_n_cand, "TOTAL_VOTES")[
        ["CANDIDATE_NAME", "PARTY", "AC_NAME", "SEX", "AGE", "CATEGORY", "TOTAL_VOTES", "VOTES_POLLED_PCT"]
    ]

    fig = px.bar(
        top_candidates.sort_values("TOTAL_VOTES"),
        x="TOTAL_VOTES", y="CANDIDATE_NAME", orientation="h",
        color="PARTY", title=f"Top {top_n_cand} Candidates by Votes",
        labels={"TOTAL_VOTES": "Total Votes", "CANDIDATE_NAME": ""},
        color_discrete_sequence=COLOR_SEQ, text="TOTAL_VOTES",
    )
    fig.update_traces(texttemplate="%{text:,}", textposition="outside")
    fig.update_layout(height=max(350, top_n_cand * 28), showlegend=True)
    apply_theme(fig)
    st.plotly_chart(fig, use_container_width=True)

    # Age distribution of top candidates
    age_df = filtered_df.dropna(subset=["AGE"])
    col_a, col_b = st.columns(2)
    with col_a:
        fig = px.histogram(
            age_df, x="AGE", nbins=25, color="SEX",
            title="Age Distribution of All Candidates",
            labels={"AGE": "Age", "count": "Candidates"},
            color_discrete_map={"MALE": "#60a5fa", "FEMALE": "#f472b6", "UNKNOWN": "#94a3b8", "THIRD": "#34d399"},
        )
        fig.update_layout(height=350, barmode="overlay")
        fig.update_traces(opacity=0.75)
        apply_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        sex_counts = filtered_df["SEX"].value_counts().reset_index()
        sex_counts.columns = ["SEX", "COUNT"]
        fig = px.pie(
            sex_counts, values="COUNT", names="SEX",
            title="Gender Distribution of Candidates",
            color_discrete_map={"MALE": "#60a5fa", "FEMALE": "#f472b6", "UNKNOWN": "#94a3b8", "THIRD": "#34d399"},
            hole=0.5,
        )
        fig.update_layout(height=350)
        apply_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Candidate Table")
    st.dataframe(
        top_candidates.reset_index(drop=True)
        .rename(columns={"CANDIDATE_NAME": "Name", "PARTY": "Party", "AC_NAME": "Constituency",
                         "SEX": "Gender", "AGE": "Age", "CATEGORY": "Category",
                         "TOTAL_VOTES": "Total Votes", "VOTES_POLLED_PCT": "Turnout %"})
        .style.format({"Total Votes": "{:,.0f}", "Turnout %": "{:.2f}"}),
        use_container_width=True, hide_index=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: VOTER DEMOGRAPHICS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Voter Demographics":
    st.markdown("""
    <div class="page-banner">
        <h1>Voter <span class="accent">Demographics</span></h1>
        <p>Turnout patterns, reservation categories, and electoral participation insights</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        cat_votes = filtered_df.groupby("CATEGORY")["TOTAL_VOTES"].sum().reset_index()
        fig = px.pie(
            cat_votes, values="TOTAL_VOTES", names="CATEGORY",
            title="Total Votes by Reservation Category",
            color_discrete_map={"GENERAL": "#a78bfa", "SC": "#34d399", "ST": "#60a5fa", "UNKNOWN": "#94a3b8"},
            hole=0.45,
        )
        fig.update_layout(height=380)
        apply_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Turnout scatter: Total Electors vs Total Votes
        ac_summary = filtered_df.drop_duplicates("AC_NO")[["AC_NAME", "TOTAL_ELECTORS", "VOTES_POLLED_PCT"]].dropna()
        fig = px.scatter(
            ac_summary, x="TOTAL_ELECTORS", y="VOTES_POLLED_PCT",
            title="Electorate Size vs Voter Turnout",
            labels={"TOTAL_ELECTORS": "Total Electors", "VOTES_POLLED_PCT": "Turnout %"},
            color="VOTES_POLLED_PCT", color_continuous_scale=["#0f172a", "#7c3aed", "#a78bfa"],
            hover_data=["AC_NAME"],
        )
        fig.update_layout(height=380, coloraxis_showscale=False)
        apply_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

    # Top and bottom turnout constituencies
    ac_turnout = filtered_df.drop_duplicates("AC_NO")[["AC_NAME", "VOTES_POLLED_PCT", "TOTAL_ELECTORS"]].dropna()
    col_a, col_b = st.columns(2)

    with col_a:
        top10 = ac_turnout.nlargest(10, "VOTES_POLLED_PCT")
        fig = px.bar(
            top10.sort_values("VOTES_POLLED_PCT"),
            x="VOTES_POLLED_PCT", y="AC_NAME", orientation="h",
            title="Top 10 Highest Turnout Constituencies",
            color="VOTES_POLLED_PCT", color_continuous_scale=["#065f46", "#34d399"],
            labels={"VOTES_POLLED_PCT": "Turnout %", "AC_NAME": ""},
        )
        fig.update_layout(coloraxis_showscale=False, height=350)
        apply_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        bot10 = ac_turnout.nsmallest(10, "VOTES_POLLED_PCT")
        fig = px.bar(
            bot10.sort_values("VOTES_POLLED_PCT", ascending=False),
            x="VOTES_POLLED_PCT", y="AC_NAME", orientation="h",
            title="Top 10 Lowest Turnout Constituencies",
            color="VOTES_POLLED_PCT", color_continuous_scale=["#7f1d1d", "#f87171"],
            labels={"VOTES_POLLED_PCT": "Turnout %", "AC_NAME": ""},
        )
        fig.update_layout(coloraxis_showscale=False, height=350)
        apply_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

    # Candidate count per constituency
    cand_per_ac = filtered_df.groupby("AC_NAME")["CANDIDATE_NAME"].count().reset_index()
    cand_per_ac.columns = ["AC_NAME", "CANDIDATES"]
    fig = px.histogram(
        cand_per_ac, x="CANDIDATES", nbins=20,
        title="Distribution of Candidates per Constituency",
        labels={"CANDIDATES": "# Candidates", "count": "Constituencies"},
        color_discrete_sequence=["#fb923c"],
    )
    fig.update_traces(marker_line_color="#ea580c", marker_line_width=1)
    fig.update_layout(height=300)
    apply_theme(fig)
    st.plotly_chart(fig, use_container_width=True)
