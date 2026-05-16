import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuration ---
st.set_page_config(page_title="Syracuse Housing Monitor", layout="wide", initial_sidebar_state="expanded")

# --- Enterprise CSS Overhaul ---
st.markdown("""
<style>
.stApp { background-color: #FDFDFD; }
[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #FFFFFF !important;
    border: 1px solid #EDF2F7 !important;
    border-radius: 6px !important;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04) !important;
    padding: 20px !important;
    margin-bottom: 20px !important;
}
.kpi-container { text-align: center; padding: 10px 0; }
.kpi-label { font-size: 0.85rem; color: #718096; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; }
.kpi-value { font-size: 2.4rem; font-weight: 800; color: #1A202C; margin-top: -5px; }
.kpi-trend-up { color: #E53E3E; font-size: 2.4rem; } 
h1 { font-weight: 900; color: #1A202C; text-align: center; letter-spacing: -0.02em; margin-bottom: 0;}
.subtitle { text-align: center; color: #718096; font-size: 1.1rem; margin-bottom: 30px; margin-top: 5px;}
h3 { font-size: 1.05rem !important; font-weight: 700 !important; color: #2D3748 !important; border-bottom: 1px solid #E2E8F0; padding-bottom: 8px; margin-bottom: 20px !important; text-transform: uppercase; letter-spacing: 0.05em;}
.stTabs [data-baseweb="tab-list"] { gap: 30px; }
.stTabs [data-baseweb="tab"] { font-weight: 700; color: #A0AEC0; }
.stTabs [data-baseweb="tab"][aria-selected="true"] { color: #2C7A7B; border-bottom-color: #2C7A7B; }
</style>
""", unsafe_allow_html=True)

# --- Professional Palette (Ghost-Bar Fix) ---
COLOR_TEAL = "#2C7A7B" 
COLOR_CORAL = "#E53E3E" 
# We removed the ultra-light colors so they don't vanish on a white background
SCALE_TEAL = ["#4FD1C5", "#38B2AC", "#319795", "#2C7A7B", "#285E61", "#234E52"]
SCALE_RED = ["#FC8181", "#F56565", "#E53E3E", "#C53030", "#9B2C2C", "#742A2A"]

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv("syracuse_safe_housing_data.csv")
    df = df.dropna(subset=['Latitude', 'Longitude'])
    df['plain_english_summary'] = df['plain_english_summary'].fillna("Requires physical inspection.")
    df['is_registered'] = df['RRisValid'].notna()
    if 'clean_property_zip' in df.columns:
        df['clean_property_zip'] = df['clean_property_zip'].astype(str)
    return df

try:
    df = load_data()
except:
    st.error("Data connection failed.")
    st.stop()

# --- Sidebar Logic ---
st.sidebar.title("Controls")
hazard_options = ["All Hazards"] + list(df['hazard_tag'].dropna().unique())
selected_hazard = st.sidebar.selectbox("Select Hazard Type:", hazard_options)
filtered_df = df if selected_hazard == "All Hazards" else df[df['hazard_tag'] == selected_hazard]

# --- UI START ---
st.title("Syracuse Safe Housing Monitor")
st.markdown("<div class='subtitle'>A Data-Driven Lens into Housing Safety and Landlord Accountability</div>", unsafe_allow_html=True)

# --- Metric Row ---
t_unfit = len(filtered_df)
abs_pct = (filtered_df['is_absentee'].sum() / t_unfit * 100) if t_unfit > 0 else 0
open_v = filtered_df[filtered_df['status_type_name'].str.upper() == 'OPEN']
a_days = open_v['days_unsafe'].mean() if not open_v.empty else 0
clstrs = len(filtered_df.groupby('owner_name').filter(lambda x: len(x) >= 3)['owner_name'].unique())

m1, m2, m3, m4 = st.columns(4)
with m1: st.markdown(f"<div class='kpi-container'><div class='kpi-label'>Unfit Properties</div><div class='kpi-value'>{t_unfit:,}</div></div>", unsafe_allow_html=True)
with m2: st.markdown(f"<div class='kpi-container'><div class='kpi-label'>Absentee Ownership</div><div class='kpi-value kpi-trend-up'>{abs_pct:.1f}%</div></div>", unsafe_allow_html=True)
with m3: st.markdown(f"<div class='kpi-container'><div class='kpi-label'>Avg Days Unresolved</div><div class='kpi-value'>{a_days:.0f}</div></div>", unsafe_allow_html=True)
with m4: st.markdown(f"<div class='kpi-container'><div class='kpi-label'>High-Risk Owners</div><div class='kpi-value kpi-trend-up'>{clstrs}</div></div>", unsafe_allow_html=True)

st.write("")

# --- Main Layout ---
left, right = st.columns([6, 4], gap="large")

with left:
    with st.container():
        st.markdown("### 🗺️ Geographic Hotspots")
        fig_map = px.scatter_mapbox(
            filtered_df, lat="Latitude", lon="Longitude", color="is_absentee",
            color_discrete_map={True: COLOR_CORAL, False: COLOR_TEAL},
            size="days_unsafe", size_max=12, opacity=0.75, zoom=11.5,
            mapbox_style="carto-positron", hover_name="address"
        )
        fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, showlegend=False)
        st.plotly_chart(fig_map, use_container_width=True, height=520, config={'displayModeBar': False})

    st.write("")

    with st.container():
        st.markdown("### 🔍 Investigation Hub")
        t1, t2 = st.tabs(["Stalled Violation Leaderboard", "Owner Portfolio Lookup"])
        with t1:
            st.dataframe(open_v.sort_values('days_unsafe', ascending=False).head(15)[['address', 'owner_name', 'days_unsafe', 'plain_english_summary']], use_container_width=True, hide_index=True)
        with t2:
            owners = sorted(filtered_df['owner_name'].dropna().unique())
            owner = st.selectbox("Select Owner from view:", [""] + owners)
            if owner:
                o_df = filtered_df[filtered_df['owner_name'] == owner]
                st.info(f"**{owner}** has **{len(o_df)}** filtered violations.")
                st.dataframe(o_df[['address', 'hazard_tag', 'days_unsafe', 'plain_english_summary']], use_container_width=True, hide_index=True)

with right:
    with st.container():
        st.markdown("### 📊 Violation Categories")
        h_counts = filtered_df['hazard_tag'].value_counts().reset_index()
        fig_h = px.bar(h_counts, x='count', y='hazard_tag', orientation='h', color='count', color_continuous_scale=SCALE_TEAL)
        fig_h.update_layout(xaxis_visible=False, yaxis_title=None, margin={"r":10,"t":10,"l":10,"b":10}, template="plotly_white", coloraxis_showscale=False)
        fig_h.update_traces(texttemplate='%{x}', textposition='outside', textfont_size=12)
        st.plotly_chart(fig_h, use_container_width=True, height=280, config={'displayModeBar': False})

    with st.container():
        st.markdown("### 📝 Registry Status")
        reg = filtered_df['is_registered'].value_counts().reset_index()
        reg['label'] = reg['is_registered'].map({True: 'Registered', False: 'Unregistered'})

        # PLOTLY BUG FIX: Added `color='label'` so it forces the color map to work!
        fig_p = px.pie(reg, values='count', names='label', color='label', hole=0.65, 
                       color_discrete_map={'Registered': COLOR_TEAL, 'Unregistered': COLOR_CORAL})

        fig_p.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5))
        fig_p.update_traces(textinfo='percent', textfont_size=14, textposition='inside')
        st.plotly_chart(fig_p, use_container_width=True, height=240, config={'displayModeBar': False})

    with st.container():
        st.markdown("### 🏙️ Zip Code Impact")
        zips = filtered_df['clean_property_zip'].value_counts().reset_index().head(5)
        fig_z = px.bar(zips, x='clean_property_zip', y='count', color='count', color_continuous_scale=SCALE_RED)
        fig_z.update_layout(xaxis_title=None, yaxis_visible=False, margin={"r":10,"t":10,"l":10,"b":10}, template="plotly_white", coloraxis_showscale=False)
        fig_z.update_traces(texttemplate='%{y}', textposition='outside', textfont_size=12)
        st.plotly_chart(fig_z, use_container_width=True, height=200, config={'displayModeBar': False})
