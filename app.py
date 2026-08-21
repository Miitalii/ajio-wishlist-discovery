import streamlit as st
import json
from collections import Counter

st.set_page_config(page_title="AJIO Wishlist Discovery Engine", page_icon="🛍️", layout="wide")

# NO CACHE - always read fresh data
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
    .metric-card { background: #1a1d29; border-radius: 12px; padding: 20px; border-top: 3px solid #feca57; text-align: left; }
    .metric-card-alt { background: #1a1d29; border-radius: 12px; padding: 20px; border-top: 3px solid #ff6b6b; text-align: left; }
    .metric-number { font-size: 2rem; font-weight: 700; color: #ffffff; }
    .metric-label-card { font-size: 0.85rem; color: #8888a0; margin-top: 4px; }
    .insight-card { background: #1a1d29; border-left: 4px solid #667eea; padding: 1rem; margin-bottom: 0.8rem; border-radius: 0 8px 8px 0; color: #e0e0e0; }
    .opportunity-high { border-left: 4px solid #ff6b6b; }
    .opportunity-medium { border-left: 4px solid #feca57; }
    .opportunity-low { border-left: 4px solid #1dd1a1; }
    .theme-badge { display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; margin-right: 8px; }
    .stage-badge { background: #2d3561; color: #74b9ff; }
    .sentiment-negative { background: #3d1f1f; color: #ff7675; }
    .sentiment-positive { background: #1f3d1f; color: #55efc4; }
    .sentiment-neutral { background: #3d331f; color: #fdcb6e; }
    a { color: #74b9ff !important;
