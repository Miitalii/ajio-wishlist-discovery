import streamlit as st
import json
from collections import Counter

# Page config
st.set_page_config(
    page_title="AJIO Wishlist Discovery Engine",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data
@st.cache_data
def load_data():
    with open("ajio_data.json", "r") as f:
        return json.load(f)

data = load_data()
insights = data["insights"]
ranking = data["opportunity_ranking"]

# Custom CSS
st.markdown("""
<style>
    .main-header { font-size: 2.5rem; font-weight: 700; color: #1a1a2e; margin-bottom: 0.5rem; }
    .sub-header { font-size: 1.1rem; color: #4a4a6a; margin-bottom: 2rem; }
    .insight-card { background: #f8f9fa; border-left: 4px solid #667eea; padding: 1rem; margin-bottom: 0.8rem; border-radius: 0 8px 8px 0; }
    .opportunity-high { border-left: 4px solid #e74c3c; }
    .opportunity-medium { border-left: 4px solid #f39c12; }
    .opportunity-low { border-left: 4px solid #27ae60; }
    .theme-badge { display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; margin-right: 8px; }
    .stage-badge { background: #e3f2fd; color: #1565c0; }
    .sentiment-negative { background: #ffebee; color: #c62828; }
    .sentiment-positive { background: #e8f5e9; color: #2e7d32; }
    .sentiment-neutral { background: #fff3e0; color: #e65100; }
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🛍️ AJIO Discovery")
st.sidebar.markdown("---")
st.sidebar.markdown("""
**Goal:** Increase % of users who purchase at least 1 wishlist item within 30 days.

**Approach:** AI-powered analysis of public user feedback mapped to the wishlist-to-purchase journey.
""")

view = st.sidebar.radio(
    "Select View",
    ["📊 Executive Dashboard", "🔍 Thematic Analysis", "🏆 Opportunity Ranker", "🧪 Live Analyzer", "📖 Methodology"]
)

# Header
st.markdown('<div class="main-header">AJIO Wishlist-to-Purchase Discovery Engine</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-powered analysis of user feedback to identify highest-impact conversion blockers</div>', unsafe_allow_html=True)

# Helper functions
def get_theme_color(theme):
    colors = {
        "FIT_UNCERTAINTY": "#e74c3c", "QUALITY_DOUBT": "#e67e22", "TRUST_DEFICIT": "#9b59b6",
        "INFO_GAP": "#3498db", "RETURN_NIGHTMARE": "#e74c3c", "APP_FRICTION": "#95a5a6",
        "PRICE_SATISFACTION": "#27ae60", "FORGOTTEN_WISHLIST": "#8e44ad", "EXTERNAL_COMPARISON": "#16a085"
    }
    return colors.get(theme, "#667eea")

def get_opportunity_class(score):
    if score >= 80: return "opportunity-high"
    elif score >= 60: return "opportunity-medium"
    else: return "opportunity-low"

# VIEW 1: Executive Dashboard
if view == "📊 Executive Dashboard":
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Total Data Points", len(insights))
    with col2: st.metric("Sources Analyzed", len(set(i["source"] for i in insights)))
    with col3: st.metric("Themes Identified", len(set(i["theme"] for i in insights)))
    with col4: st.metric("Top Opportunity", ranking[0]["theme_label"])
    
    st.markdown("---")
    st.subheader("🎯 Theme Distribution Across Feedback")
    
    theme_counts = Counter([i["theme_label"] for i in insights])
    st.bar_chart(dict(theme_counts))
    
    st.markdown("---")
    st.subheader("🛤️ Where in the Wishlist Journey Do Problems Occur?")
    
    journey_counts = Counter([i["journey_label"] for i in insights])
    st.bar_chart(dict(journey_counts))
    
    st.info("""
    **How to read this:** `PRE_PURCHASE` issues are direct conversion blockers — users are actively considering 
    a wishlist item but something stops them. `POST_DELIVERY` issues are trust eroders — they make users 
    hesitant to buy from their wishlist in the future.
    """)
    
    st.markdown("---")
    st.subheader("📡 Feedback Sources")
    source_counts = Counter([i["source"] for i in insights])
    col_s1, col_s2 = st.columns([2, 1])
    with col_s1: st.bar_chart(dict(source_counts))
    with col_s2:
        for src, cnt in source_counts.items():
            st.write(f"**{src}:** {cnt}")

# VIEW 2: Thematic Analysis
elif view == "🔍 Thematic Analysis":
    st.subheader("🔍 Deep Dive: Feedback Themes")
    
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        selected_theme = st.selectbox("Filter by Theme", ["All"] + sorted(list(set(i["theme_label"] for i in insights))))
    with col_f2:
        selected_stage = st.selectbox("Filter by Journey Stage", ["All"] + sorted(list(set(i["journey_label"] for i in insights))))
    with col_f3:
        selected_source = st.selectbox("Filter by Source", ["All"] + sorted(list(set(i["source"] for i in insights))))
    
    filtered = insights
    if selected_theme != "All": filtered = [i for i in filtered if i["theme_label"] == selected_theme]
    if selected_stage != "All": filtered = [i for i in filtered if i["journey_label"] == selected_stage]
    if selected_source != "All": filtered = [i for i in filtered if i["source"] == selected_source]
    
    st.markdown(f"**Showing {len(filtered)} insights**")
    
    for item in filtered:
        color = get_theme_color(item["theme"])
        opp_class = get_opportunity_class(item.get("opportunity_score", 50))
        sentiment_map = {"negative": "sentiment-negative", "positive": "sentiment-positive", "neutral": "sentiment-neutral"}
        sentiment_class = sentiment_map.get(item["sentiment"], "sentiment-neutral")
        
        st.markdown(f"""
        <div class="insight-card {opp_class}">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <div>
                    <span class="theme-badge" style="background: {color}20; color: {color};">{item["theme_label"]}</span>
                    <span class="theme-badge stage-badge">{item["journey_stage"]}</span>
                    <span class="theme-badge {sentiment_class}">{item["sentiment"].upper()}</span>
                </div>
                <div style="color: #666; font-size: 0.8rem;">{item["source"]} | Score: <b>{item.get("opportunity_score", "N/A")}</b></div>
            </div>
            <div style="font-style: italic; color: #333; margin: 8px 0;">"{item["raw_text"]}"</div>
            <div style="font-size: 0.85rem; color: #666;">
                <b>Impact:</b> {item["impact_on_conversion"]} | <b>Frequency:</b> {item["frequency_score"]}/100 | 
                <a href="{item["evidence_url"]}" target="_blank" style="color: #667eea;">View Source ↗</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

# VIEW 3: Opportunity Ranker
elif view == "🏆 Opportunity Ranker":
    st.subheader("🏆 Ranked Opportunities for Wishlist Conversion")
    st.markdown("Scored by: **Frequency × Conversion Impact × Solveability**")
    
    for i, opp in enumerate(ranking):
        score = opp["score"]
        opp_class = get_opportunity_class(score)
        badge_color = '#e74c3c' if score >= 80 else '#f39c12' if score >= 60 else '#27ae60'
        
        st.markdown(f"""
        <div class="insight-card {opp_class}">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div style="flex: 1;">
                    <div style="font-size: 1.3rem; font-weight: 700; color: #1a1a2e; margin-bottom: 4px;">#{i+1} {opp["theme_label"]}</div>
                    <div style="color: #4a4a6a; margin-bottom: 8px;">
                        <b>Score:</b> {score}/100 | <b>Evidence:</b> {opp["evidence_count"]} data points | <b>Frequency:</b> {opp["frequency"]}
                    </div>
                    <div style="background: white; padding: 12px; border-radius: 8px; margin: 8px 0;">
                        <div style="font-size: 0.9rem; color: #555; margin-bottom: 4px;"><b>💡 Conversion Impact:</b> {opp["conversion_impact"]}</div>
                        <div style="font-size: 0.9rem; color: #555; margin-bottom: 4px;"><b>🔧 Solveability:</b> {opp["solveability"]}</div>
                        <div style="font-size: 0.85rem; color: #666; font-style: italic;">"{opp["key_quote"]}"</div>
                    </div>
                </div>
                <div style="background: {badge_color}; color: white; padding: 8px 16px; border-radius: 20px; font-weight: 700; font-size: 1.2rem; margin-left: 16px;">{score}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# VIEW 4: Live Analyzer
elif view == "🧪 Live Analyzer":
    st.subheader("🧪 Live Feedback Analyzer")
    st.markdown("Paste any AJIO review, Reddit post, or user comment. The AI will categorize it against our wishlist conversion framework.")
    
    user_input = st.text_area("Paste user feedback here:", height=120, 
                              placeholder="Example: 'I loved the kurta design but I have no idea if it will fit me. The size chart is confusing and there are no reviews with photos.'")
    
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
                st.markdown(f"""
                <div style="background: white; border: 2px solid {color}; border-radius: 12px; padding: 16px; margin: 12px 0;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-size: 1.2rem; font-weight: 700; color: {color};">{theme_label}</div>
                            <div style="color: #666; font-size: 0.9rem; margin-top: 4px;">Code: {theme_code} | Opportunity Score: {score}/100</div>
                        </div>
                        <div style="background: {color}; color: white; padding: 8px 16px; border-radius: 20px; font-weight: 700;">{score}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.info("**Note:** This demo uses rule-based classification. In the full version, this would call an LLM (GPT-4/Claude) for nuanced semantic analysis.")
        else:
            st.warning("Please paste some feedback to analyze.")

# VIEW 5: Methodology
elif view == "📖 Methodology":
    st.subheader("📖 How This Engine Works")
    st.markdown("""
    ### Data Sources
    - **Trustpilot** — Aggregated user reviews (2025–2026)
    - **Reddit** — r/IndianFashionAddicts, r/mumbai, r/India
    - **Medium / Product Analysis** — Third-party UX audits
    - **YouTube Comments** — Haul video comment sections
    - **Play Store / App Store** — App reviews (analyzed via sentiment extraction)
    
    ### AI Processing Pipeline
    1. **Ingestion** — Raw text collected from public sources
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
<div style="text-align: center; color: #888; font-size: 0.8rem;">
    AJIO Wishlist Discovery Engine | Built for PM Fellowship Graduation Project | 2026
</div>
""", unsafe_allow_html=True)
