import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="SupeRR Selector | Pressure Analytics", page_icon="🏏", layout="wide")
DATA = Path(__file__).with_name("analysis.xlsx")

@st.cache_data
def load_data():
    bat = pd.read_excel(DATA, sheet_name="Batting Top 10")
    bowl = pd.read_excel(DATA, sheet_name="Bowling Top 10")
    bat_c = pd.read_excel(DATA, sheet_name="Batting Candidates")
    bowl_c = pd.read_excel(DATA, sheet_name="Bowling Candidates")
    audit = pd.read_excel(DATA, sheet_name="Validation & Audit").fillna("").astype(str)
    sources = pd.read_excel(DATA, sheet_name="Research Sources")
    start = pd.read_excel(DATA, sheet_name="Start Here", header=None)
    return bat, bowl, bat_c, bowl_c, audit, sources, start

bat, bowl, bat_c, bowl_c, audit, sources, start = load_data()

st.title("🏏 SupeRR Selector | Pressure Analytics")
st.caption("Round 1 • Identify the most reliable players under pressure • IPL & T20I, 2022–2026")
st.caption("Explore pressure-performance rankings, player-level evidence, comparisons and the analytical methodology.")

# Topline metrics
def audit_value(key):
    row = audit[audit.iloc[:,0].astype(str).str.contains(key, case=False, na=False)]
    return str(row.iloc[0,1]) if len(row) else "—"

m1,m2,m3,m4=st.columns(4)
m1.metric("Matches in scope", "853")
m2.metric("Matches with ball data", "837")
m3.metric("Legal chase deliveries", "88,093")
m4.metric("High-leverage deliveries", "22,024")

tab1,tab2,tab3,tab4=st.tabs(["Batting leaderboard","Bowling leaderboard","Player comparison","Methodology & audit"])

with tab1:
    st.subheader("Top 10 batters under pressure")
    st.caption("Ordered by the batting composite described in the methodology report.")
    col1,col2=st.columns([1.5,1])
    with col1:
        st.dataframe(bat, width="stretch", hide_index=True)
    with col2:
        metric=st.selectbox("Visualise batting metric",["Impact/100","Runs/100 legal balls","Uplift/100","Positive match %"],key="bat_metric")
        labels={"Impact/100":"Impact/100","Runs/100 legal balls":"Runs/100 legal balls","Uplift/100":"Uplift/100","Positive match %":"Positive match %"}
        fig=px.bar(bat.sort_values("Rank"),x=labels[metric],y="Player",orientation="h",color=labels[metric],color_continuous_scale="RdYlGn",title=metric+" — selected batters")
        fig.update_layout(height=520, yaxis={"categoryorder":"total ascending"}, coloraxis_showscale=False)
        st.plotly_chart(fig,width="stretch")
    chosen=st.selectbox("Inspect a batter",bat["Player"].tolist(),key="bat_detail")
    r=bat[bat["Player"]==chosen].iloc[0]
    st.markdown(f"**{chosen}** · Rank #{int(r['Rank'])} · Player ID `{int(r['Player ID'])}`")
    a,b,c,d=st.columns(4)
    a.metric("Pressure balls",int(r["Pressure balls"]))
    b.metric("Runs",int(r["Runs"]))
    c.metric("Dismissals",int(r["Dismissals"]))
    d.metric("Runs / 100 legal balls",f"{r['Runs/100 legal balls']:.1f}")
    st.write(f"Context-adjusted impact: **{r['Impact/100']:.2f} per 100 balls** · Uplift vs normal: **{r['Uplift/100']:.2f}** · Positive match contribution: **{r['Positive match %']:.1f}%**.")

with tab2:
    st.subheader("Top 10 bowlers under pressure")
    st.caption("Ordered by the bowling composite described in the methodology report.")
    col1,col2=st.columns([1.5,1])
    with col1:
        st.dataframe(bowl, width="stretch", hide_index=True)
    with col2:
        metric=st.selectbox("Visualise bowling metric",["Economy","Wickets/100","Impact/100","Uplift/100","Positive match %"],key="bowl_metric")
        fig=px.bar(bowl.sort_values("Rank"),x=metric,y="Player",orientation="h",color=metric,color_continuous_scale="RdYlGn",title=metric+" — selected bowlers")
        fig.update_layout(height=520, yaxis={"categoryorder":"total ascending"}, coloraxis_showscale=False)
        st.plotly_chart(fig,width="stretch")
    chosen=st.selectbox("Inspect a bowler",bowl["Player"].tolist(),key="bowl_detail")
    r=bowl[bowl["Player"]==chosen].iloc[0]
    st.markdown(f"**{chosen}** · Rank #{int(r['Rank'])} · Player ID `{int(r['Player ID'])}`")
    a,b,c,d=st.columns(4)
    a.metric("Pressure balls",int(r["Pressure balls"]))
    b.metric("Wickets",int(r["Wickets"]))
    c.metric("Runs conceded",int(r["Runs conceded"]))
    d.metric("Economy",f"{r['Economy']:.2f}")
    st.write(f"Wickets per 100 balls: **{r['Wickets/100']:.2f}** · Context-adjusted impact: **{r['Impact/100']:.2f}** · Uplift: **{r['Uplift/100']:.2f}** · Positive match contribution: **{r['Positive match %']:.1f}%**.")

with tab3:
    st.subheader("Compare players")
    role=st.radio("Player role",["Batters","Bowlers"],horizontal=True)
    df=bat_c if role=="Batters" else bowl_c
    options=df["Player"].tolist()
    defaults=options[:min(3,len(options))]
    selected=st.multiselect("Select up to 5 players",options,default=defaults[:2],max_selections=5)
    comp=df[df["Player"].isin(selected)]
    if len(comp):
        st.dataframe(comp,width="stretch",hide_index=True)
        if role=="Batters":
            metric=st.selectbox("Comparison metric",["Runs/100","Impact/100","Uplift/100","Positive %","Composite"],key="bat_comp")
        else:
            metric=st.selectbox("Comparison metric",["Economy","Wickets/100","Impact/100","Uplift/100","Positive %","Composite"],key="bowl_comp")
        fig=px.bar(comp,x="Player",y=metric,color=metric,color_continuous_scale="RdYlGn",title=f"{metric} comparison")
        st.plotly_chart(fig,width="stretch")
    else:
        st.warning("Choose at least one player to compare.")

with tab4:
    st.subheader("Methodology and data audit")
    st.markdown("""
    **Pressure definition:** second-innings delivery leverage, defined as the change in estimated chase win probability between a hypothetical six and a hypothetical wicket. The primary pressure sample is the top quartile of legal chase deliveries.

    **Scope:** IPL competitions and T20I competitions from 2022 onward. Other domestic T20 competitions are excluded.

    **Context controls:** format, innings phase (Powerplay, Middle, Death) and wickets remaining.

    **Eligibility:** at least 50 pressure legal balls across at least 8 matches.

    **Reliability adjustment:** pressure-ball sample size is shrunk using `n / (n + 30)`.

    **Important:** impact and composite scores are relative ranking measures, not probabilities. See the PDF report for full formulas, delivery accounting, references and limitations.
    """)
    st.dataframe(audit,width="stretch",hide_index=True)
    st.subheader("Research sources")
    st.dataframe(sources,width="stretch",hide_index=True)

st.divider()
st.caption("SupeRR Selector Season 2 • Round 1 | Player statistics and rankings are drawn from the accompanying analysis workbook.")
