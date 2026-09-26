import streamlit as st
import os
from google import genai

st.set_page_config(
    page_title="BrandShield AI - Trademark & Legal Conflict Detector",
    page_icon="🛡️",
    layout="centered"
)

# Custom Styling for Clean FinTech UI
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .metric-card {
        background: linear-gradient(135deg, #1e2638 0%, #161a25 100%);
        border: 1px solid #2d3748;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 15px;
    }
    .badge-safe {
        background-color: #065f46;
        color: #6ee7b7;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 600;
        display: inline-block;
    }
    .badge-warn {
        background-color: #854d0e;
        color: #fde047;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 600;
        display: inline-block;
    }
    .badge-danger {
        background-color: #991b1b;
        color: #fca5a5;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 600;
        display: inline-block;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ BrandShield AI")
st.subheader("Indian Trademark & Domain Conflict Intelligence")
st.caption("Naye business ya brand par legal notice aur copyright dispute aane se pehle check karein.")

# Fetch API key automatically
api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", ""))

if not api_key:
    api_key = st.text_input("Gemini API Key (Admin Mode):", type="password")

# Quick Example Autofills
col1, col2 = st.columns(2)
example_clicked = False
if col1.button("🧪 Example: AlphaVeda (Ayurveda)"):
    st.session_state["b_name"] = "AlphaVeda"
    st.session_state["b_type"] = "Ayurvedic herbal supplements, Shilajit and dry fruits health powders."
    example_clicked = True

if col2.button("🧪 Example: NikeFit (Sportswear)"):
    st.session_state["b_name"] = "NikeFit"
    st.session_state["b_type"] = "Gym wear t-shirts, activewear joggers, and sports shoes."
    example_clicked = True

brand_name = st.text_input(
    "Proposed Brand Name / Domain:",
    value=st.session_state.get("b_name", ""),
    placeholder="e.g., AlphaVeda, UrbanFit, RoyalCraft"
)

business_type = st.text_area(
    "Business / Products Offered:",
    value=st.session_state.get("b_type", ""),
    placeholder="e.g., E-commerce store for men's apparel, organic supplements, web design studio..."
)

if st.button("🚀 Analyze Legal Risk & Trademark Class", type="primary", use_container_width=True):
    if not api_key:
        st.error("Admin: API Key configure nahi hui hai. Secrets me GEMINI_API_KEY add karein.")
    elif not brand_name.strip() or not business_type.strip():
        st.warning("Kripya Brand Name aur Business details dono fill karein.")
    else:
        with st.spinner("Analyzing NICE Trademark Classes, Phonetic Matching & Dispute Database..."):
            try:
                client = genai.Client(api_key=api_key)
                
                prompt = f"""
                You are a senior Indian Trademark Attorney and Intellectual Property Expert.
                Analyze the following brand under the Trade Marks Act, 1999 and NICE Classification.

                Brand Name: {brand_name}
                Business Activity: {business_type}

                Return the response strictly structured in clear, bold, actionable Hinglish with the following sections:

                ### 1. 📋 Relevant NICE Trademark Classification
                - **Primary Class:** (e.g., Class 25, Class 5, Class 35) with clear reason.
                - **Secondary / Defensive Classes:** (Which other classes they should also file to block copycats).

                ### 2. ⚖️ Distinctiveness & Dispute Risk
                - **Generic / Descriptive Check:** (Kya ye aam lafz hai jo legally protect nahi ho sakta?)
                - **Phonetic & Visual Sound-alike:** (Does it conflict with well-known registered brands like Nike, Himalaya, Tata, etc.?)

                ### 3. 🎯 Risk Verdict
                - State **RISK LEVEL: [LOW / MODERATE / HIGH]**
                - Estimated Conflict Score: **X%**
                - 2-line direct legal advice.

                ### 4. 💡 3 Alternative Safe Variations
                Provide 3 high-recall, legally defensible, distinctive brand name alternatives if there is any risk.
                """

                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt
                )
                
                st.markdown("---")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
