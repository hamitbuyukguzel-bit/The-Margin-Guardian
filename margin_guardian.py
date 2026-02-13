import streamlit as st

# Hamit Büyükgüzel - Paradox Engine: Margin Guardian
st.set_page_config(page_title="Margin Guardian", page_icon="🛡️", layout="centered")

# --- CSS Stil Düzenlemesi (Harvard/Princeton Estetiği) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stNumberInput, .stSelectbox { background-color: #1a1c24 !important; }
    .stAlert { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Margin Guardian")
st.subheader("Liquidation Rescue & DCA Simulator")
st.write("---")

# --- Input Alanları ---
col1, col2 = st.columns(2)

with col1:
    side = st.selectbox("Position Side", ["Short", "Long"])
    entry_price = st.number_input("Initial Entry Price ($)", min_value=0.0, value=60000.0, step=100.0)
    initial_margin = st.number_input("Initial Margin ($)", min_value=0.0, value=50.0, step=10.0)

with col2:
    leverage = st.number_input("Leverage (x)", min_value=1, max_value=125, value=10)
    current_price = st.number_input("Current/Add-on Price ($)", min_value=0.0, value=64500.0, step=100.0)
    added_margin = st.number_input("Margin to Add ($)", min_value=0.0, value=95.0, step=5.0)

# --- Hesaplama Motoru ---
def calculate_rescue(entry, current, margin_init, margin_add, lev, side):
    # Pozisyon Büyüklükleri
    pos_size_init = margin_init * lev
    pos_size_add = margin_add * lev
    total_pos_size = pos_size_init + pos_size_add
    total_margin = margin_init + margin_add
    
    # Yeni Ortalama Giriş Fiyatı (Ağırlıklı Ortalama)
    new_entry = (pos_size_init * entry + pos_size_add * current) / total_pos_size
    
    # Fiyat Değişimi %
    price_diff_pct = (current - new_entry) / new_entry
    
    # Zarar/Kar % (Kaldıraç Etkisiyle)
    if side == "Short":
        pnl_pct = -price_diff_pct * lev * 100
        new_liq_price = new_entry * (1 + (1 / lev))
    else:
        pnl_pct = price_diff_pct * lev * 100
        new_liq_price = new_entry * (1 - (1 / lev))
    
    # Liq'e Uzaklık
    dist_to_liq = abs((new_liq_price - current) / current) * 100
    
    return new_entry, pnl_pct, new_liq_price, dist_to_liq

# Sonuçları Al
new_entry, pnl, liq_price, dist = calculate_rescue(entry_price, current_price, initial_margin, added_margin, leverage, side)

# --- Görsel Çıktılar ---
st.write("### 📊 Post-DCA Analysis")

res_col1, res_col2 = st.columns(2)
res_col1.metric("New Avg. Entry", f"${new_entry:,.2f}")
res_col2.metric("New PnL (%)", f"{pnl:,.2f}%", delta_color="inverse")

res_col3, res_col4 = st.columns(2)
res_col3.metric("New Liq. Price", f"${liq_price:,.2f}")
res_col4.metric("Distance to Liq.", f"{dist:,.2f}%")

# --- Risk Uyarıları (Paradox Engine Mantığı) ---
st.write("---")
if dist < 5:
    st.error(f"⚠️ HIGH RISK: Price is only {dist:.2f}% away from liquidation! Consider adding more margin.")
elif dist < 15:
    st.warning(f"🔔 MODERATE RISK: Buffer zone is {dist:.2f}%. Watch the volatility.")
else:
    st.success(f"✅ SAFE ZONE: You have a {dist:.2f}% safety buffer.")

st.info(f"**Paradox Engine Insight:** Adding ${added_margin} reduced your PnL from an estimated critical level to {pnl:.2f}%.")

st.caption("Developed by Hamit Büyükgüzel | Paradox Engine Finance")
