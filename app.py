import streamlit as st
import json
from collections import Counter

st.set_page_config(page_title="AJIO Wishlist Discovery Engine", page_icon="🛍️", layout="wide")

@st.cache_data
def load_data():
    with open("ajio_data.json", "r") as f:
        return json.load(f)

data = load_data()
insights = data["insights"]
ranking = data["opportunity_ranking"]

st.markdown("""
<style>
    .main-header { font-size: 2.2rem; font-weight: 700; color: #ffffff; margin-bottom: 0.3rem; }
    .sub-header { font-size: 1rem; color: #a0a0b0; margin-bottom: 2rem; }
    .brand-tag { color: #feca57; font-weight: 600; font-size: 0.9rem; }
    .metric-card {
        background: #1a1d29;
        border-radius: 12px;
        padding: 20px;
        border-top: 3px solid #feca57;
        text-align: left;
    }
    .metric-card-alt {
        background: #1a1d29;
        border-radius: 12px;
        padding: 20px;
        border-top: 3px solid #ff6b6b;
        text-align: left;
    }
    .metric-number {
        font-size: 2rem;
        font-weight: 700;
        color: #ffffff;
    }
    .metric-label-card {
        font-size: 0.85rem;
        color: #8888a0;
        margin-top: 4px;
    }
    .insight-card { 
        background: #1a1d29; 
        border-left: 4px solid #667eea; 
        padding: 1rem; 
        margin-bottom: 0.8rem; 
        border-radius: 0 8px 8px 0; 
        color: #e0e0e0; 
    }
    .opportunity-high { border-left: 4px solid #ff6b6b; }
    .opportunity-medium { border-left: 4px solid #feca57; }
    .opportunity-low { border-left: 4px solid #1dd1a1; }
    .theme-badge { 
        display: inline-block; 
        padding: 4px 12px; 
        border-radius: 20px; 
        font-size: 0.75rem; 
        font-weight: 600; 
        margin-right: 8px; 
    }
    .stage-badge { background: #2d3561; color: #74b9ff; }
    .sentiment-negative { background: #3d1f1f; color: #ff7675; }
    .sentiment-positive { background: #1f3d1f; color: #55efc4; }
    .sentiment-neutral { background: #3d331f; color: #fdcb6e; }
    a { color: #74b9ff !important; }
    .source-grid {
        background: #1a1d29;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
    }
    .source-number {
        font-size: 1.8rem;
        font-weight: 700;
        color: #ffffff;
    }
    .source-name {
        font-size: 0.8rem;
        color: #8888a0;
        margin-top: 4px;
    }
</style>
""", unsafe_allow_html=True)

st.sidebar.title("🛍️ AJIO Discovery")
st.sidebar.markdown("---")
st.sidebar.markdown("""
**Goal:** Increase % of users who purchase at least 1 wishlist item within 30 days.

**Approach:** AI-powered analysis of public user feedback mapped to the wishlist-to-purchase journey.
""")

view = st.sidebar.radio("Select View", [
    "📊 Executive Dashboard",
    "🔍 Thematic Analysis",
    "🏆 Opportunity Ranker",
    "🧪 Live Analyzer",
    "📖 Methodology"
])

st.markdown('<div class="brand-tag">AJIO · Wishlist Insights</div>', unsafe_allow_html=True)
st.markdown('<div class="main-header">Wishlist-to-Purchase Discovery Engine</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-classified themes from Play Store, App Store, Reddit, Trustpilot, Medium, and YouTube — surfacing why users do not convert wishlisted items into purchases on AJIO.</div>', unsafe_allow_html=True)

def get_theme_color(theme):
    colors = {
        "FIT_UNCERTAINTY": "#ff6b6b", "QUALITY_DOUBT": "#feca57", "TRUST_DEFICIT": "#a29bfe",
        "INFO_GAP": "#74b9ff", "RETURN_NIGHTMARE": "#ff6b6b", "APP_FRICTION": "#dfe6e9",
        "PRICE_SATISFACTION": "#1dd1a1", "FORGOTTEN_WISHLIST": "#fd79a8", "EXTERNAL_COMPARISON": "#00cec9"
    }
    return colors.get(theme, "#667eea")

def get_opp_class(score):
    if score >= 80: return "opportunity-high"
    elif score >= 60: return "opportunity-medium"
    else: return "opportunity-low"

if view == "📊 Executive Dashboard":

    st.markdown("### 📊 Data Overview")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="metric-card"><div class="metric-number">{len(insights)}</div><div class="metric-label-card">Items Analyzed</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><div class="metric-number">{len(insights)}</div><div class="metric-label-card">Items Classified</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card-alt"><div class="metric-number">{len(set(i["theme"] for i in insights))}</div><div class="metric-label-card">Themes Identified</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="metric-card-alt"><div class="metric-number">{len(set(i["source"] for i in insights))}</div><div class="metric-label-card">Sources</div></div>', unsafe_allow_html=True)

    st.markdown("### 📡 Source Breakdown")
    source_counts = Counter([i["source"] for i in insights])
    source_items = list(source_counts.items())
    cols = st.columns(len(source_items))

    for idx, (src, cnt) in enumerate(source_items):
        with cols[idx]:
            src_key = src.lower().replace(" ", "_")
            st.markdown(f'<div class="source-grid"><div class="metric-number">{cnt}</div><div class="source-name">{src_key}</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🎯 Theme Distribution Across Feedback")
    theme_counts = Counter([i["theme_label"] for i in insights])
    st.bar_chart(dict(theme_counts))

    st.markdown("---")
    st.subheader("🛤️ Where in the Wishlist Journey Do Problems Occur?")
    journey_counts = Counter([i["journey_label"] for i in insights])
    st.bar_chart(dict(journey_counts))

    st.info("""
    **How to read this:** PRE_PURCHASE issues are direct conversion blockers — users are actively considering 
    a wishlist item but something stops them. POST_DELIVERY issues are trust eroders — they make users 
    hesitant to buy from their wishlist in the future.
    """)

elif view == "🔍 Thematic Analysis":
    st.subheader("🔍 Deep Dive: Feedback Themes")
    f1, f2, f3 = st.columns(3)
    with f1: sel_theme = st.selectbox("Filter by Theme", ["All"] + sorted(list(set(i["theme_label"] for i in insights))))
    with f2: sel_stage = st.selectbox("Filter by Journey Stage", ["All"] + sorted(list(set(i["journey_label"] for i in insights))))
    with f3: sel_source = st.selectbox("Filter by Source", ["All"] + sorted(list(set(i["source"] for i in insights))))

    filtered = insights
    if sel_theme != "All": filtered = [i for i in filtered if i["theme_label"] == sel_theme]
    if sel_stage != "All": filtered = [i for i in filtered if i["journey_label"] == sel_stage]
    if sel_source != "All": filtered = [i for i in filtered if i["source"] == sel_source]

    st.markdown(f"**Showing {len(filtered)} insights**")

    for item in filtered:
        color = get_theme_color(item["theme"])
        opp_class = get_opp_class(item.get("opportunity_score", 50))
        smap = {"negative": "sentiment-negative", "positive": "sentiment-positive", "neutral": "sentiment-neutral"}
        sclass = smap.get(item["sentiment"], "sentiment-neutral")

        card_html = f"""
        <div class="insight-card {opp_class}">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <div>
                    <span class="theme-badge" style="background: {color}30; color: {color}; border: 1px solid {color}50;">{item["theme_label"]}</span>
                    <span class="theme-badge stage-badge">{item["journey_stage"]}</span>
                    <span class="theme-badge {sclass}">{item["sentiment"].upper()}</span>
                </div>
                <div style="color: #888; font-size: 0.8rem;">{item["source"]} | Score: <b style="color:{color};">{item.get("opportunity_score", "N/A")}</b></div>
            </div>
            <div style="font-style: italic; color: #f0f0f0; margin: 8px 0;">"{item["raw_text"]}"</div>
            <div style="font-size: 0.85rem; color: #aaa;">
                <b style="color:#ddd;">Impact:</b> {item["impact_on_conversion"]} | <b style="color:#ddd;">Frequency:</b> {item["frequency_score"]}/100 | 
                <a href="{item["evidence_url"]}" target="_blank">View Source ↗</a>
            </div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

elif view == "🏆 Opportunity Ranker":
    st.subheader("🏆 Ranked Opportunities for Wishlist Conversion")
    st.markdown("Scored by: **Frequency × Conversion Impact × Solveability**")

    for i, opp in enumerate(ranking):
        score = opp["score"]
        opp_class = get_opp_class(score)
        badge_color = '#ff6b6b' if score >= 80 else '#feca57' if score >= 60 else '#1dd1a1'

        rank_html = f"""
        <div class="insight-card {opp_class}">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div style="flex: 1;">
                    <div style="font-size: 1.3rem; font-weight: 700; color: #ffffff; margin-bottom: 4px;">#{i+1} {opp["theme_label"]}</div>
                    <div style="color: #b0b3c7; margin-bottom: 8px;">
                        <b style="color:#fff;">Score:</b> {score}/100 | <b style="color:#fff;">Evidence:</b> {opp["evidence_count"]} data points | <b style="color:#fff;">Frequency:</b> {opp["frequency"]}
                    </div>
                    <div style="background: #252538; padding: 12px; border-radius: 8px; margin: 8px 0; border: 1px solid #333;">
                        <div style="font-size: 0.9rem; color: #ddd; margin-bottom: 4px;"><b style="color:#74b9ff;">💡 Conversion Impact:</b> {opp["conversion_impact"]}</div>
                        <div style="font-size: 0.9rem; color: #ddd; margin-bottom: 4px;"><b style="color:#55efc4;">🔧 Solveability:</b> {opp["solveability"]}</div>
                        <div style="font-size: 0.85rem; color: #aaa; font-style: italic;">"{opp["key_quote"]}"</div>
                    </div>
                </div>
                <div style="background: {badge_color}; color: #1a1a2e; padding: 8px 16px; border-radius: 20px; font-weight: 700; font-size: 1.2rem; margin-left: 16px;">{score}</div>
            </div>
        </div>
        """
        st.markdown(rank_html, unsafe_allow_html=True)

elif view == "🧪 Live Analyzer":
    st.subheader("🧪 Live Feedback Analyzer")
    st.markdown("Paste any AJIO review, Reddit post, or user comment. The AI will categorize it against our wishlist conversion framework.")

    user_input = st.text_area("Paste user feedback here:", height=120, 
                              placeholder="Example: I loved the kurta design but I have no idea if it will fit me. The size chart is confusing and there are no reviews with photos.")

    if st.button("Analyze Feedback", type="primary"):
        if user_input.strip():
            text_lower = user_input.lower()
            themes_detected = []

            if any(w in text_lower for w in ["size", "fit", "fitting", "tight", "loose", "chart", "measurement", "sizing"]):
                themes_detected.append(("FIT_UNCERTAINTY", "Fit & Sizing Confidence", 92))
            if any(w in text_lower for w in ["quality", "cheap", "fabric", "material", "stitching", "color different", "see-through"]):
                themes_detected.append(("QUALITY_DOUBT", "Product Quality Mismatch", 85))
            if any(w in text_lower for w in ["review", "rating", "photo", "picture", "no one bought", "social proof"]):
                themes_detected.append(("INFO_GAP", "Missing Social Proof & Reviews", 88))
            if any(w in text_lower for w in ["return", "refund", "pickup", "exchange", "customer care", "customer service"]):
                themes_detected.append(("RETURN_NIGHTMARE", "Return & Refund Friction", 70))
            if any(w in text_lower for w in ["trust", "scam", "fraud", "never again", "elsewhere", "deteriorated"]):
                themes_detected.append(("TRUST_DEFICIT", "Platform Trust Erosion", 78))
            if any(w in text_lower for w in ["price", "expensive", "discount", "sale", "costly", "cheap price"]):
                themes_detected.append(("PRICE_WAITING", "Price Sensitivity", 55))
            if any(w in text_lower for w in ["app", "ui", "cluttered", "slow", "ads", "notification"]):
                themes_detected.append(("APP_FRICTION", "App Experience Friction", 45))
            if any(w in text_lower for w in ["forget", "forgot", "remember", "reminder", "lost interest"]):
                themes_detected.append(("FORGOTTEN_WISHLIST", "Wishlist Discovery & Reminders", 55))
            if any(w in text_lower for w in ["myntra", "amazon", "compare", "comparison", "check other"]):
                themes_detected.append(("EXTERNAL_COMPARISON", "Cross-Platform Comparison Behavior", 52))

            if not themes_detected:
                themes_detected.append(("UNCATEGORIZED", "General Feedback", 30))

            st.success("Analysis Complete!")
            for theme_code, theme_label, score in themes_detected:
                color = get_theme_color(theme_code)
                result_html = f"""
                <div style="background: #1a1d29; border: 2px solid {color}; border-radius: 12px; padding: 16px; margin: 12px 0;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-size: 1.2rem; font-weight: 700; color: {color};">{theme_label}</div>
                            <div style="color: #888; font-size: 0.9rem; margin-top: 4px;">Code: {theme_code} | Opportunity Score: {score}/100</div>
                        </div>
                        <div style="background: {color}; color: #1a1a2e; padding: 8px 16px; border-radius: 20px; font-weight: 700;">{score}</div>
                    </div>
                </div>
                """
                st.markdown(result_html, unsafe_allow_html=True)

            st.info("""
            **Note:** This demo uses rule-based classification. In the full version, this would call an LLM (GPT-4/Claude) for nuanced semantic analysis.
            """)
        else:
            st.warning("Please paste some feedback to analyze.")

elif view == "📖 Methodology":
    st.subheader("📖 How This Engine Works")
    st.markdown("""
    ### Data Sources
    - **Play Store** — Android app reviews (2025–2026)
    - **App Store** — iOS app reviews (2025–2026)
    - **Reddit** — r/IndianFashionAddicts, r/mumbai, r/India, r/TwoXIndia
    - **YouTube Comments** — AJIO haul video comment sections
    - **Trustpilot** — Aggregated user reviews and complaints

    ### AI Processing Pipeline
    1. **Ingestion** — Raw text collected from public sources via scrapers
    2. **Thematic Tagging** — LLM classifies each comment into wishlist-relevant themes
    3. **Journey Mapping** — Each comment is mapped to a stage in the wishlist-to-purchase funnel
    4. **Scoring** — Opportunity score = Frequency × Conversion Impact × Solveability

    ### Opportunity Scoring Formula
    ```
    Score = (Frequency_Score / 100) × (Impact_Weight) × (Solveability_Weight) × 100
    ```
    - **Frequency:** How often does this theme appear? (0–100)
    - **Conversion Impact:** Does this directly block a wishlist purchase? (High=1.0, Medium=0.7, Low=0.4)
    - **Solveability:** Can we realistically solve this with product innovation? (High=1.0, Medium=0.7, Low=0.4)

    ### Why This Matters
    Instead of generic sentiment analysis, this engine **connects every insight to the business metric**: 
    *"% of users who purchase at least one wishlist item within 30 days."*

    ### Limitations
    - Sample size is directional, not statistically significant
    - Rule-based live analyzer is a prototype; production would use fine-tuned LLM
    - Does not include primary research data (see Part 3: User Interviews)
    """)

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.8rem;">
    AJIO Wishlist Discovery Engine | Built for PM Fellowship Graduation Project | 2026
</div>
""", unsafe_allow_html=True)