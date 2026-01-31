import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="RetailPulse | Analytics", layout="wide")

# 2. STRICT LEFT-ALIGN & BRANDING CSS
st.markdown("""
    <style>
    /* Global Background */
    .main { background-color: #0E1117; }
    
    /* SIDEBAR ARROW VISIBILITY */
    button[kind="headerNoSpacing"] {
        visibility: visible !important;
        color: #FF4B4B !important;
    }

    /* RED CHARGE SEARCH BOX */
    div[data-baseweb="input"] {
        border: 2px solid #FF4B4B !important;
        border-radius: 8px !important;
    }
    
    /* THE "NUCLEAR" LEFT ALIGN: Targeting every possible cell container */
    /* 1. Headers */
    th { 
        text-align: left !important; 
        padding-left: 15px !important; 
        background-color: #1E2130 !important; 
    }
    
    /* 2. Standard Cells */
    td { 
        text-align: left !important; 
        padding-left: 15px !important; 
    }
    
    /* 3. Streamlit Grid Cells (The most important part) */
    div[data-testid="stDataFrame"] div[role="gridcell"] {
        justify-content: flex-start !important;
        text-align: left !important;
    }

    /* 4. Forcing the inner text wrapper of numeric cells to the left */
    div[data-testid="stDataFrame"] div[role="gridcell"] > div {
        text-align: left !important;
        justify-content: flex-start !important;
        width: 100% !important;
        display: flex !important;
    }

    /* Corporate Header Bar */
    .header-bar {
        background-color: #1E2130;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        border-bottom: 5px solid #FF4B4B;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    
    /* STRATEGY MATRIX HEADER */
    .table-header-block {
        background-color: #1E2130;
        padding: 1rem;
        border-radius: 12px 12px 0 0;
        border-left: 6px solid #FF4B4B;
        margin-top: 1.5rem;
        color: white;
        font-weight: 900;
        font-size: 1.2rem;
        text-transform: uppercase;
        letter-spacing: 3px;
        font-family: 'Segoe UI', sans-serif;
    }

    /* METRIC CARDS */
    .glass-card {
        background: linear-gradient(145deg, #1e2130, #161922);
        border: 1px solid rgba(255, 75, 75, 0.3);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
    }
    .glass-label { color: #A0AEC0; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px; }
    .glass-value { color: #FF4B4B; font-size: 1.8rem; font-weight: 800; margin: 0; }

    /* STRATEGIC ADVICE BOX */
    .eye-catching-advice {
        background-color: #0068C9;
        color: white;
        padding: 18px;
        border-radius: 10px;
        border-left: 6px solid #FFFFFF;
        font-size: 0.95rem;
        font-weight: 700;
        margin-top: 10px;
    }
    
    /* Sidebar Spacing */
    [data-testid="stSidebar"] { padding-top: 0.5rem; }
    .stSlider { margin-top: -20px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

try:
    df = pd.read_csv('validated_association_rules.csv')
    
    with st.sidebar:
        st.header("🔍 Search & Filter")
        search_query = st.text_input("Product Quick Search", placeholder="eg. PLATES").upper()
        
        st.divider()
        st.subheader("Rule Thresholds")
        lift_threshold = st.slider("Min Lift", 1.0, 10.0, 2.0)
        conf_threshold = st.slider("Min Confidence", 0.1, 1.0, 0.5)
        z_threshold = st.slider("Min Z-Score", 0.0, 25.0, 1.96)
        
        st.markdown("""
            <div class="eye-catching-advice">
                💡 STRATEGIC ADVICE:<br>
                Target Lift > 6.0 and Z-Score > 1.96 for high-impact bundling.
            </div>
        """, unsafe_allow_html=True)

    filtered_rules = df[
        (df['lift'] >= lift_threshold) & 
        (df['confidence'] >= conf_threshold) & 
        (df['z_score'] >= z_threshold)
    ]
    if search_query:
        filtered_rules = filtered_rules[
            filtered_rules['antecedents'].str.contains(search_query) | 
            filtered_rules['consequents'].str.contains(search_query)
        ]

    st.markdown(f"""
        <div class="header-bar">
            <h1 style="color:white; font-weight:900; font-size:3.2rem; margin:0; letter-spacing:-2px;">RETAIL<span style="color:#FF4B4B">PULSE</span> ANALYTICS</h1>
            <p style="color: #A0AEC0; margin-top:5px; font-weight:500; font-size:1.1rem;">Predictive Association Strategy Engine</p>
        </div>
    """, unsafe_allow_html=True)

    # Convert to float to avoid the format specifier error seen in your logs
    avg_lift = float(filtered_rules['lift'].mean()) if not filtered_rules.empty else 0.0
    avg_conf = float(filtered_rules['confidence'].mean()) if not filtered_rules.empty else 0.0
    max_z = float(filtered_rules['z_score'].max()) if not filtered_rules.empty else 0.0
    
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.markdown(f'<div class="glass-card"><p class="glass-label">Total Rules</p><p class="glass-value">{len(df)}</p></div>', unsafe_allow_html=True)
    m2.markdown(f'<div class="glass-card"><p class="glass-label">Filtered Rules</p><p class="glass-value">{len(filtered_rules)}</p></div>', unsafe_allow_html=True)
    m3.markdown(f'<div class="glass-card"><p class="glass-label">Avg. Lift</p><p class="glass-value">{avg_lift:.2f}</p></div>', unsafe_allow_html=True)
    m4.markdown(f'<div class="glass-card"><p class="glass-label">Avg. PROBABILITY</p><p class="glass-value">{avg_conf:.2f}</p></div>', unsafe_allow_html=True)
    m5.markdown(f'<div class="glass-card"><p class="glass-label">Peak Z-Score</p><p class="glass-value">{max_z:.1f}</p></div>', unsafe_allow_html=True)

    st.markdown('<div class="table-header-block">ASSOCIATION STRATEGY MATRIX</div>', unsafe_allow_html=True)
    
    # Render table - st.dataframe columns are now forced left by the CSS above
    st.dataframe(
        filtered_rules.sort_values('lift', ascending=False), 
        column_config={
            "antecedents": st.column_config.TextColumn("Bought", width="medium"),
            "consequents": st.column_config.TextColumn("Recommended", width="medium"),
            "support": st.column_config.NumberColumn("Frequency", format="%.3f", width="small"),
            "confidence": st.column_config.ProgressColumn("Probability", min_value=0, max_value=1, format="%.2f", width="small"),
            "lift": st.column_config.NumberColumn("Lift", format="%.2f", width="small"),
            "z_score": st.column_config.NumberColumn("Z-Score", format="%.2f", width="small"),
        },
        hide_index=True,
        use_container_width=True 
    )

except FileNotFoundError:
    st.error("Data Engine Missing.")