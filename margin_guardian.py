import streamlit as st

# Developed by Hamit Büyükgüzel
# Part of "The Paradox Engine: Finance & Risk Module"

st.set_page_config(page_title="Margin Guardian | Paradox Engine", page_icon="🛡️", layout="centered")

# --- Custom Professional UI Styling ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stNumberInput, .stSelectbox { background-color: #1a1c24 !important; }
    .stMetric { border: 1px solid #30363d; border-radius: 8px; padding: 10px; background-color: #161b22; }
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Margin Guardian")
st.markdown("### *Liquidation Mitigation & DCA Analytics Lab*")
st.write("---")

# --- Interactive Sidebar for Project Info ---
with st.sidebar:
    st.header("Project Info")
    st.info("**Paradox Engine** Finance Module v1.0")
    st.write("Ensuring methodological rigor in high-stakes financial environments.")
    st.write("Developed by: **Hamit Büyükgüzel**")
    st.write("GitHub: `hamitbuyukguzel-bit` Concepts")

# --- Data Input Section ---
st.markdown("#### 📥 Position Parameters")
col1, col2 = st.columns(2)

with col1:
    side = st.selectbox("Position Side", ["Short", "Long"])
    entry_price = st.number_input("Initial Entry Price ($)", min_value=0.0, value=60000.0, step=100.0)
    initial_margin = st.number_input("Initial Margin ($)", min_value=0.0, value=50.0, step=10.0)

with col2:
    leverage = st.number_input("Leverage Ratio (x)", min_value=1, max_value=125, value=10)
    current_price = st.number_input("Add-on / Market Price ($)", min_value=0.0, value=64500.0, step=100.0)
    added_margin = st.number_input("Capital to Inject ($)", min_value=0.0, value=95.0, step=5.0)

# --- Core Calculation Engine ---
def calculate_rescue(entry, current, margin_init, margin_add, lev, side):
    # Calculate Notional Sizes
    pos_size_init = margin_init * lev
    pos_size_add = margin_add * lev
    total_pos_size = pos_size_init + pos_size_add
    
    # New Weighted Average Entry Price
    new_entry = (pos_size_init * entry + pos_size_add * current) / total_pos_size
    
    # Percentage Difference from Entry
    price_diff_pct = (current - new_entry) / new_entry
    
    # PnL Percentage (Leveraged)
    if side == "Short":
        pnl_pct = -price_diff_pct * lev * 100
        # Basic Liquidation Formula (Distance based on Maintenance Margin approx.)
        new_liq_price = new_entry * (1 + (1 / lev))
    else:
        pnl_pct = price_diff_pct * lev * 100
        new_liq_price = new_entry * (1 - (1 / lev))
    
    # Distance to Liquidation Threshold
    dist_to_liq = abs((new_liq_price - current) / current) * 100
    
    return new_entry, pnl_pct, new_liq_price, dist_to_liq

# Run Calculations
new_entry, pnl, liq_price, dist = calculate_rescue(entry_price, current_price, initial_margin, added_margin, leverage, side)

# --- Result Visualization ---
st.write("---")
st.markdown("#### 📊 Post-Capital Injection Analysis")

res_col1, res_col2 = st.columns(2)
with res_col1:
    st.metric("New Average Entry", f"${new_entry:,.2f}")
    st.metric("New Liq. Price", f"${liq_price:,.2f}")

with res_col2:
    st.metric("New PnL (%)", f"{pnl:,.2f}%")
    st.metric("Safety Buffer (Distance)", f"{dist:.2f}%")

# --- Risk Evaluation Notifications ---
st.write("---")
if dist < 5:
    st.error(f"⚠️ **Critical Risk:** Safety Buffer is extremely low ({dist:.2f}%). Immediate risk of liquidation.")
elif dist < 15:
    st.warning(f"🔔 **Moderate Risk:** Safety Buffer is {dist:.2f}%. High market volatility could trigger liquidation.")
else:
    st.success(f"✅ **Safe Zone:** Safety Buffer established at {dist:.2f}%. The risk has been significantly mitigated.")

# --- Paradox Engine Insight ---
st.markdown(f"""
> **Quantitative Insight:** Injecting **${added_margin:.2f}** has recalculated your weighted entry to **${new_entry:,.2f}**. 
> This strategic adjustment has provided a safety buffer of **${abs(liq_price - current):,.2f}** between current price and total loss.
""")

st.caption("© 2026 The Paradox Engine | Developed by Hamit Büyükgüzel")
