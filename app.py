# ============================
# AI Currency Converter - Streamlit Version
# ============================

import streamlit as st
import requests
from math import isfinite

# Page configuration
st.set_page_config(
    page_title="AI Currency Converter",
    page_icon="💹",
    layout="centered"
)

# Custom CSS for premium styling
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #0b1220 30%, #1f2937 100%);
        color: white;
    }
    .glass-card {
        background: rgba(255,255,255,0.06);
        border-radius: 16px;
        padding: 25px;
        backdrop-filter: blur(8px) saturate(120%);
        border: 1px solid rgba(255,255,255,0.06);
        box-shadow: 0 8px 30px rgba(2,6,23,0.6);
        margin: 20px 0;
    }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3em;
        background: linear-gradient(90deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02));
        border: 1px solid rgba(255,255,255,0.06);
        color: #e6eef8;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 6px 8px 0 rgba(0,0,0,0.38);
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 12px 16px 0 rgba(0,0,0,0.42);
    }
    .result-box {
        background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
        border-radius: 12px;
        padding: 20px;
        color: #dbeafe;
        font-weight: 600;
        border: 1px solid rgba(255,255,255,0.04);
        margin-top: 20px;
        box-shadow: 0 8px 20px rgba(2,6,23,0.6);
    }
    .header-container {
        text-align: center;
        padding: 20px 0;
    }
    .currency-flag {
        font-size: 1.2em;
        margin-right: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Currency configuration
FLAG_MAP = {
    "USD": "🇺🇸",
    "PKR": "🇵🇰", 
    "EUR": "🇪🇺",
    "GBP": "🇬🇧",
    "AUD": "🇦🇺",
    "CAD": "🇨🇦",
    "SAR": "🇸🇦",
    "AED": "🇦🇪",
    "JPY": "🇯🇵",
    "CNY": "🇨🇳",
    "INR": "🇮🇳",
    "HKD": "🇭🇰",
    "SGD": "🇸🇬",
    "CHF": "🇨🇭",
}

# Build display list with flags
currency_list = [f"{FLAG_MAP.get(code, '')} {code}" for code in FLAG_MAP.keys()]

# Helper function to extract currency code
def _code_from_display(display_str):
    if not isinstance(display_str, str):
        return display_str
    parts = display_str.strip().split()
    return parts[-1] if len(parts) >= 1 else display_str

# Conversion function
def convert_currency(amount, from_display, to_display):
    try:
        if amount is None:
            return "⚠️ Enter an amount."
        try:
            amt = float(amount)
        except:
            return "⚠️ Amount must be a number."
        if not isfinite(amt):
            return "⚠️ Invalid amount."

        from_code = _code_from_display(from_display)
        to_code = _code_from_display(to_display)
        
        # Use free API (no key required)
        BASE_URL = "https://api.exchangerate-api.com/v4/latest/"
        url = f"{BASE_URL}{from_code}"
        
        resp = requests.get(url, timeout=8)
        if resp.status_code != 200:
            return f"❌ Error fetching rates (status {resp.status_code}). Try again."

        data = resp.json()
        rates = data.get("rates")
        if rates is None:
            return "❌ Unexpected API response."

        if to_code not in rates:
            return f"❌ Currency {to_code} not available."

        rate = rates[to_code]
        converted = round(amt * float(rate), 4)

        flag_from = FLAG_MAP.get(from_code, "")
        flag_to = FLAG_MAP.get(to_code, "")

        result_text = (
            f"{flag_from} **{amt:,} {from_code}**  →  {flag_to} **{converted:,} {to_code}**\n\n"
            f"**Rate:** 1 {from_code} = {rate} {to_code}"
        )
        return result_text

    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# Main app
def main():
    # Header
    st.markdown("""
    <div class="header-container">
        <h1 style='color:#e6eef8; margin-bottom:10px;'>💹 AI Currency Converter</h1>
        <div style='color:#b8c6d9; margin-bottom:20px;'>Premium UI • Live Rates • Flags • Glassmorphism</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Main conversion card
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            amount = st.number_input("**Amount**", value=1.0, step=1.0, format="%.2f", 
                                   help="Enter the amount you want to convert")
        
        with col2:
            from_cur = st.selectbox("**From**", currency_list, index=0)
        
        with col3:
            to_cur = st.selectbox("**To**", currency_list, index=1)
        
        # Buttons row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            convert_btn = st.button("**Convert 💱**", use_container_width=True)
        
        with col2:
            if st.button("**Swap 🔁**", use_container_width=True):
                # Swap the currencies
                current_from = from_cur
                current_to = to_cur
                st.session_state.from_cur = current_to
                st.session_state.to_cur = current_from
                st.rerun()
        
        with col3:
            if st.button("**⭐ USD**", use_container_width=True):
                st.session_state.to_cur = "🇺🇸 USD"
                st.rerun()
        
        with col4:
            if st.button("**⭐ PKR**", use_container_width=True):
                st.session_state.to_cur = "🇵🇰 PKR"
                st.rerun()
        
        # Initialize session state for currency values
        if 'from_cur' not in st.session_state:
            st.session_state.from_cur = "🇺🇸 USD"
        if 'to_cur' not in st.session_state:
            st.session_state.to_cur = "🇵🇰 PKR"
        
        # Convert button action
        if convert_btn:
            result = convert_currency(amount, from_cur, to_cur)
            st.markdown(f"""
            <div class="result-box">
                <h3 style='margin:0; color:#60a5fa;'>💫 Conversion Result:</h3>
                <div style='font-size:1.2em; margin:15px 0;'>{result}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='color:#93c5fd; text-align:center; font-size:14px;'>
        <strong>💡 Info:</strong> Live rates powered by exchangerate-api.com • No API key required
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
