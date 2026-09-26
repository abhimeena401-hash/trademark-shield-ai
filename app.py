import streamlit as st
import os
from google import genai

st.set_page_config(
    page_title="BrandShield AI",
    page_icon="🛡️",
    layout="centered"
)

# Secrets se key apne aap load hogi
api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

st.title("🛡️ BrandShield AI")
st.subheader("Trademark & Legal Conflict Detector")
st.caption("Kisi bhi brand ya domain ko launch karne se pehle legal risk check karein.")

brand_name = st.text_input(
    "Proposed Brand Name / Domain:",
    placeholder="e.g., Chaiwala.com, AlphaVeda"
)

business_type = st.text_area(
    "Business / Products Offered:",
    placeholder="e.g., Ecommerce tea selling, tea bags, pouch packaging..."
)

if st.button("🚀 Analyze Legal Risk & Trademark Class", type="primary", use_container_width=True):
    if not brand_name.strip() or not business_type.strip():
        st.warning("Kripya Brand Name aur Business Details dono bharein.")
    elif not api_key:
        st.error("Backend API Key set nahi hai. Streamlit Secrets check karein.")
    else:
        with st.spinner("Analyzing NICE Trademark Classes & Legal Conflicts..."):
            try:
                client = genai.Client(api_key=api_key.strip())
                
                prompt = f"""
                You are a senior Indian Trademark Attorney and Intellectual Property Expert.
                Analyze the proposed brand name under the Trade Marks Act, 1999 and NICE Classification.

                Brand Name: {brand_name}
                Business Activity: {business_type}

                Return the response strictly structured in clear, bold, actionable Hinglish with the following sections:

                ### 1. 📋 Relevant NICE Trademark Classification
                - **Primary Class:** (e.g., Class 30 for Tea/Coffee, Class 35 for Online Retail) with clear reason.
                - **Secondary / Defensive Classes:** (Which other classes they should also file to protect online sales).

                ### 2. ⚖️ Distinctiveness & Dispute Risk
                - **Generic / Descriptive Check:** (Kya ye aam lafz hai jo legally protect nahi ho sakta?)
                - **Phonetic & Visual Sound-alike:** (Does it conflict with well-known brands like MBA Chaiwala, Chaayos, Chai Point, etc.?)

                ### 3. 🎯 Risk Verdict
                - State **RISK LEVEL: [LOW / MODERATE / HIGH]**
                - Estimated Conflict Score: **X%**
                - 2-line direct legal advice.

                ### 4. 💡 3 Alternative Safe Variations
                Provide 3 high-recall, legally defensible, distinctive brand name alternatives.
                """

                response = client.models.generate_content(
                    model='gemini-3.8-flash',
                    contents=prompt
                )
                
                st.markdown("---")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
                
