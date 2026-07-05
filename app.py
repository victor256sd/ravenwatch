import streamlit as st
import pandas as pd
import pydeck as pdk
import feedparser
from openai import OpenAI

# --------------------------------------------------------------------------------
# 1. CYBER COMMAND GLOBAL STYLING & CONFIGURATION
# --------------------------------------------------------------------------------
st.set_page_config(
    page_title="RAVENWATCH INTELLIGENCE DASHBOARD", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Custom High-Tech CSS Injection for a dark dashboard theme
st.markdown("""
    <style>
        /* Base application background and primary layout text color */
        .stApp {
            background-color: #060b13;
            color: #d1d5db;
        }
        /* Dashboard Container Borders mimicking target vectors */
        div[data-testid="stVerticalBlock"] > div {
            border-color: #1e293b !important;
        }
        div[data-testid="stMetricContainer"] {
            background-color: #0b132b;
            border: 1px solid #00f2fe;
            border-radius: 4px;
            padding: 12px;
            box-shadow: 0 0 10px rgba(0, 242, 254, 0.1);
        }
        /* Custom scrolling data stream containers */
        .intel-container {
            background-color: #09111e;
            border-left: 3px solid #ff007f;
            padding: 10px;
            margin-bottom: 8px;
            border-radius: 0 4px 4px 0;
        }
        /* Metric values neon highlights */
        div[data-testid="stMetricValue"] {
            color: #00f2fe !important;
            font-family: 'Courier New', monospace;
            font-size: 1.8rem !important;
        }
        h1, h2, h3 {
            color: #ffffff !important;
            font-family: 'Courier New', monospace;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
    </style>
""", unsafe_allow_html=True)

# --------------------------------------------------------------------------------
# 2. OPENAI INTEGRATION & ENVIRONMENT SETUP
# --------------------------------------------------------------------------------
# SECURE LOCAL & CLOUD STORAGE PLACEMARKER
# Local production development: Add to `.streamlit/secrets.toml` -> OPENAI_API_KEY="your_key"
# Streamlit Community Cloud: Add via Settings -> Advanced Settings -> Secrets Configuration
if "OPENAI_API_KEY" in st.secrets:
    openai_key = st.secrets["OPENAI_API_KEY"]
else:
    # Fallback option to manually enter via the sidebar interface
    openai_key = st.sidebar.text_input("🔑 OPENAI API KEY DEPLOYMENT", type="password", help="Input your key here or host using secrets.toml")

# Initialize OpenAI Client if key is provided
client = OpenAI(api_key=openai_key) if openai_key else None

# --------------------------------------------------------------------------------
# 3. REAL-TIME SECURITY INTELLIGENCE DATA ENGINES
# --------------------------------------------------------------------------------
@st.cache_data(ttl=300)
def fetch_travel_advisories():
    """Streams live executive protection warnings directly from US State Dept."""
    feed_url = "https://state.gov"
    try:
        feed = feedparser.parse(feed_url)
        if feed.entries:
            return [{"title": entry.title, "link": entry.link, "summary": entry.get("summary", "")} for entry in feed.entries[:6]]
    except Exception:
        pass
    # Fallback asset arrays if network firewall restricts RSS fetch
    return [
        {"title": "Mexico - Level 3: Reconsider Travel (Crime & Kidnapping)", "link": "#", "summary": "High risk profile within specific transit corridors."},
        {"title": "Colombia - Level 2: Exercise Increased Caution (Terrorism)", "link": "#", "summary": "Active operational footprints in localized rural border sectors."},
        {"title": "Nigeria - Level 4: Do Not Travel (Civil Unrest & Kidnapping)", "link": "#", "summary": "Extreme tactical threat profile surrounding industrial infrastructure."}
    ]

@st.cache_data(ttl=600)
def get_tactical_assets():
    """Generates structured geographic coordinates for VIP/Corporate Asset tracking."""
    return pd.DataFrame({
        'lat': [19.4326, 4.7110, 6.5244, 1.3521, 35.6762],
        'lon': [-99.1332, -74.0721, 3.3792, 103.8198, 139.6503],
        'asset_name': ['HQ Regional Office - Mexico City', 'Ex-Dir Convoy Vector - Bogotá', 'Supply Chain Depot - Lagos', 'Regional Office - Singapore', 'Corporate Suite - Tokyo'],
        'threat_index': [75, 40, 90, 10, 15],
        'status': ['Amber Alert', 'Normal Operations', 'Critical Watch', 'Secure', 'Secure']
    })

# Gather real-time telemetry datasets
advisories = fetch_travel_advisories()
asset_df = get_tactical_assets()

# --------------------------------------------------------------------------------
# 4. DASHBOARD HEADER & SYSTEM STATUS METRICS
# --------------------------------------------------------------------------------
st.title("⚡ GSOC TACTICAL MONITOR")
st.caption("🔒 EXECUTIVE PROTECTION & CORPORATE SECURITY INTELLIGENCE STREAM")

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric(label="🛰️ MONITOR STATUS", value="NOMINAL", delta="SYSTEM STABLE")
with m2:
    st.metric(label="⚠️ LIVE SECURITY ALERTS", value=f"{len(advisories)} Active", delta="+1 Critical")
with m3:
    st.metric(label="👥 ON-SITE VIP CONVOYS", value="1 Active Track", delta="Bogotá Vector")
with m4:
    st.metric(label="💻 CYBER THREAT INDEX", value="ELEVATED", delta="APT-41 Scans Active")

st.markdown("<hr style='border:1px solid #1e293b'>", unsafe_allow_html=True)

# --------------------------------------------------------------------------------
# 5. SPLIT PANEL LAYOUT ENGINE
# --------------------------------------------------------------------------------
left_column, right_column = st.columns([1.1, 0.9])

# --- LEFT COLUMN: SPATIAL GEO-INTEL & DATA TABLES ---
with left_column:
    st.subheader("📍 Global Situation Asset Map")
    
    # Tactical heat gradient color mapping for Pydeck
    asset_df['color_r'] = asset_df['threat_index'].apply(lambda x: 255 if x > 50 else 0)
    asset_df['color_g'] = asset_df['threat_index'].apply(lambda x: 0 if x > 70 else (242 if x > 20 else 255))
    asset_df['color_b'] = asset_df['threat_index'].apply(lambda x: 127 if x > 50 else 0)

    view_state = pdk.ViewState(latitude=15.0, longitude=10.0, zoom=1.1, pitch=30)
    
    # Layer 1: Threat Heat Circles surrounding assets
    asset_layer = pdk.Layer(
        'ScatterplotLayer',
        data=asset_df,
        get_position='[lon, lat]',
        get_color='[color_r, color_g, color_b, 180]',
        get_radius='threat_index * 8000',
        pickable=True,
        auto_highlight=True
    )

    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/dark-v10',
        initial_view_state=view_state,
        layers=[asset_layer],
        tooltip={"text": "Asset: {asset_name}\nThreat Rating: {threat_index}/100\nStatus: {status}"}
    ))

    st.subheader("📊 Asset Security Parameters & Threat Indexes")
    st.dataframe(
        asset_df[['asset_name', 'threat_index', 'status']], 
        use_container_width=True, 
        hide_index=True,
        height=180
    )

# --- RIGHT COLUMN: AI POSTURE & REAL-TIME INCIDENT COMM ---
with right_column:
    st.subheader("🧠 Automated Counter-Threat Executive Brief")
    
    if client:
        # Construct automated payload of our live data points to compile threat intelligence via LLM
        raw_advisories_text = "\n".join([a['title'] for a in advisories])
        raw_assets_text = "\n".join([f"{row['asset_name']} (Threat Level: {row['threat_index']})" for _, row in asset_df.iterrows()])
        
        prompt = f"""
        You are a senior Corporate Security Director and Dignitary Protection Expert. 
        Analyze the following live telemetry and write a brief, hyper-concise tactical brief for the C-Suite executive team.
        Include critical focus points for physical threat minimization and immediate protective operations adjustments.

        Live Travel Advisories:
        {raw_advisories_text}

        Monitored High-Value Asset Hubs:
        {raw_assets_text}
        
        Format beautifully using markdown. Use clear bold warnings. Keep it under 150 words total. Do not waste space.
        """
        
        try:
            with st.spinner("🔄 Generating dynamic tactical brief via OpenAI LLM matrix..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a professional tactical security intelligence analyst."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=250,
                    temperature=0.3
                )
                st.markdown(f"<div style='background-color:#0b132b; padding:15px; border-radius:4px; border-left: 3px solid #00f2fe;'>{response.choices[0].message.content}</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Execution Error interfacing OpenAI Engine: {e}")
    else:
        st.info("ℹ️ Provide your OpenAI API key in the sidebar to activate real-time intelligence briefing models.")
        # Simulation Mock for testing visibility without an API key
        with st.expander("👁️ View Simulated Threat Model Output Template"):
            st.markdown("""
            **⚠️ CRITICAL INTERIM SECURITY BRIEF:**
            *   **Bogotá Vector Analysis:** The Ex-Dir Convoy operational route displays elevated volatility metrics. Recommend shifting to low-profile B-tier armored transport vectors immediately.
            *   **Lagos Infrastructure Guard:** Supply Chain Logistics Hub monitoring indicates a critical threshold threat index of **90**. Implement pre-planned asset lockups and suspend localized staff transits for the next 24 hours.
            """)

    st.subheader("🛡️ Strategic Posture Assessment")
    with st.container(border=True):
        st.markdown("Executive Protection Readiness Index:")
        st.progress(0.92, text="Personal Security Detail (PSD) Allocation Matrix")
        st.markdown("Digital footprint / OSINT Tracking status:")
        st.progress(0.65, text="Executive Identity Dark Web Scrubbing Progress")
        st.markdown("", unsafe_allow_html=True)

# --------------------------------------------------------------------------------
# 6. SPLIT PANEL LAYOUT ENGINE
# --------------------------------------------------------------------------------

col_feed_1, col_feed_2 = st.columns(2)
with col_feed_1:
    st.subheader("🚩 Live US Department of State Advisories")

with st.container(height=280, border=True):
    for alert in advisories:
        st.markdown(f""f"⚠️ {alert['title']}"f"{alert['summary'][:160]}..."f"<a href='{alert['link']}' target='_blank' style='color:#ff007f; text-decoration:none; font-size:12px;'>Review Dossier Link →"f"",unsafe_allow_html=True)

with col_feed_2:
    st.subheader("🌐 OSINT Critical Cyber & Asset Warnings")

with st.container(height=280, border=True):
    cyber_alerts = [("CRITICAL", "Zero-day exploitation vector detected targeting corporate remote executive mobile endpoints."),("WARNING", "Geopolitical hacktivist deployment targeting core logistical supply networks."),("NOTICE", "Planned civil demonstrations mapped across major regional operational hubs tomorrow."),("SECURITY", "Executive digital footprint exposure detected on clear-web tracking indexing platform.")]


for level, msg in cyber_alerts:

    if level == "CRITICAL":
        color = "#ff007f"
    elif level == "WARNING":
        color = "#f59e0b"
    else:
        color = "#00f2fe"

    st.markdown(
        f"""
        <div class="intel-container">
            <strong style="color:{color};">{level}</strong><br>
            {msg}
        </div>
        """,
        unsafe_allow_html=True
    )



