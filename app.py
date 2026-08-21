import streamlit as st
import json
from collections import Counter

st.set_page_config(page_title="AJIO Wishlist Discovery Engine", page_icon="🛍️", layout="wide")

st.html("<style>body{background:#0e1117;color:#e0e0e0;}</style>")

with open("ajio_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

insights = data["insights"]
ranking = data["opportunity_ranking"]

total = len(insights)
themes = len(set(i["theme"] for i in insights))
sources = len(set(i["source"] for i in insights))
source_counts = Counter(i["source"] for i in insights)

st.markdown("<h1 style='color:#ffffff;margin-bottom:0.2rem;'>🛍️ AJIO Wishlist Discovery Engine</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#a0a0b0;margin-bottom:2rem;'>Uncovering why users save but do not buy — across <b>Play Store, App Store, Reddit, YouTube & Trustpilot</b></p>", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Items Analyzed", total)
c2.metric("Items Classified", total)
c3.metric("Themes Identified", themes)
c4.metric("Sources", sources)

st.markdown("<hr style='border-color:#333;margin:1.5rem 0;'>", unsafe_allow_html=True)

st.markdown("<h3 style='color:#feca57;margin-bottom:1rem;'>📊 Source Breakdown</h3>", unsafe_allow_html=True)

source_meta = {
    "Play Store": {"icon": "📱", "color": "#1dd1a1"},
    "App Store": {"icon": "🍎", "color": "#ff6b6b"},
    "Reddit": {"icon": "🤖", "color": "#feca57"},
    "YouTube": {"icon": "▶️", "color": "#ff7675"},
    "Trustpilot": {"icon": "⭐", "color": "#74b9ff"},
}

cols = st.columns(5)
for idx, (src, count) in enumerate(source_counts.most_common()):
    meta = source_meta.get(src, {"icon": "📄", "color": "#888"})
    key = src.lower().replace(" ", "_")
    with cols[idx]:
        st.markdown(f"<div style='background:#1a1d29;border-radius:12px;padding:16px;border-top:3px solid {meta['color']};text-align:center;'><div style='font-size:1.8rem;'>{meta['icon']}</div><div style='font-size:1.6rem;font-weight:700;color:#fff;'>{count}</div><div style='font-size:0.8rem;color:#888;'>{key}</div></div>", unsafe_allow_html=True)

st.markdown("<hr style='border-color:#333;margin:1.5rem 0;'>", unsafe_allow_html=True)

st.markdown("<h3 style='color:#ff6b6b;margin-bottom:1rem;'>🎯 Opportunity Ranking</h3>", unsafe_allow_html=True)

for r in ranking:
    score = r["score"]
    color = "#ff6b6b" if score >= 80 else "#feca57" if score >= 60 else "#1dd1a1"
    st.markdown(f"<div style='background:#1a1d29;border-left:4px solid {color};padding:1rem;margin-bottom:0.6rem;border-radius:0 8px 8px 0;'><div style='display:flex;justify-content:space-between;align-items:center;'><span style='font-weight:600;color:#fff;font-size:1.05rem;'>{r['theme_label']}</span><span style='background:{color};color:#000;padding:4px 12px;border-radius:20px;font-weight:700;font-size:0.85rem;'>{score}</span></div><div style='color:#888;font-size:0.85rem;margin-top:6px;'>📊 {r['frequency']} &nbsp;|&nbsp; 🎯 {r['conversion_impact']} &nbsp;|&nbsp; 🔧 Solveability: {r['solveability']}</div><div style='color:#a0a0b0;font-size:0.8rem;margin-top:4px;font-style:italic;'>\"{r['key_quote']}\"</div></div>", unsafe_allow_html=True)

st.markdown("<hr style='border-color:#333;margin:1.5rem 0;'>", unsafe_allow_html=True)

st.markdown("<h3 style='color:#74b9ff;margin-bottom:1rem;'>🔍 Raw Insights</h3>", unsafe_allow_html=True)

sel_source = st.selectbox("Filter by Source", ["All"] + sorted(set(i["source"] for i in insights)))
sel_theme = st.selectbox("Filter by Theme", ["All"] + sorted(set(i["theme_label"] for i in insights)))
sel_stage = st.selectbox("Filter by Journey Stage", ["All"] + sorted(set(i["journey_stage"] for i in insights)))

filtered = insights
if sel_source != "All":
    filtered = [i for i in filtered if i["source"] == sel_source]
if sel_theme != "All":
    filtered = [i for i in filtered if i["theme_label"] == sel_theme]
if sel_stage != "All":
    filtered = [i for i in filtered if i["journey_stage"] == sel_stage]

st.markdown(f"<p style='color:#888;margin-bottom:1rem;'>Showing <b>{len(filtered)}</b> of {total} insights</p>", unsafe_allow_html=True)

for item in filtered:
    sent_color = "#ff7675" if item["sentiment"] == "negative" else "#55efc4" if item["sentiment"] == "positive" else "#fdcb6e"
    sent_bg = "#3d1f1f" if item["sentiment"] == "negative" else "#1f3d1f" if item["sentiment"] == "positive" else "#3d331f"
    stage_color = "#74b9ff"
    st.markdown(f"<div style='background:#1a1d29;border-left:4px solid #667eea;padding:1rem;margin-bottom:0.6rem;border-radius:0 8px 8px 0;'><div style='display:flex;gap:8px;margin-bottom:8px;flex-wrap:wrap;'><span style='background:#2d3561;color:{stage_color};padding:3px 10px;border-radius:20px;font-size:0.75rem;font-weight:600;'>{item['journey_stage']}</span><span style='background:{sent_bg};color:{sent_color};padding:3px 10px;border-radius:20px;font-size:0.75rem;font-weight:600;'>{item['sentiment']}</span><span style='background:#2d1f3d;color:#a29bfe;padding:3px 10px;border-radius:20px;font-size:0.75rem;font-weight:600;'>{item['source']}</span></div><div style='color:#e0e0e0;font-size:0.95rem;margin-bottom:6px;'>{item['raw_text']}</div><div style='color:#888;font-size:0.8rem;'>Theme: <b>{item['theme_label']}</b> &nbsp;|&nbsp; Impact: <b>{item['impact_on_conversion']}</b> &nbsp;|&nbsp; Score: <b>{item['opportunity_score']}</b></div></div>", unsafe_allow_html=True)
