import streamlit as st
from google import genai

st.set_page_config(page_title="Brand Trademark Shield AI", page_icon="🛡️", layout="centered")

st.title("🛡️ Brand Trademark Shield AI")
st.caption("Naye brand ya domain ka legal risk aur trademark class check karein")

# API Key handling
api_key = st.secrets.get("GEMINI_API_KEY", "")
if not api_key:
    api_key = st.text_input("Apni Gemini API Key enter karein:", type="password")

brand_name = st.text_input("Proposed Brand Name / Domain:", placeholder="e.g., AlphaVeda, UrbanFit")
business_type = st.text_area("Business kiska hai? (Details likhein):", placeholder="e.g., Ayurvedic supplements & Shilajit, Clothing, Cloud kitchen")

if st.button("Conflict & Risk Check Karein", type="primary"):
    if not api_key:
        st.error("Kripya valid Gemini API Key dalein.")
    elif not brand_name or not business_type:
        st.warning("Brand name aur Business details dono bharna zaroori hai.")
    else:
        with st.spinner("Trademark analysis chal raha hai..."):
            try:
                client = genai.Client(api_key=api_key)
                
                prompt = f"""
                You are an expert Indian Intellectual Property and Trademark Consultant.
                Analyze the proposed brand name for potential legal conflicts, class classification, and registrability under the Indian Trade Marks Act, 1999 (NICE Classification).

                Proposed Brand Name: {brand_name}
                Business / Product Nature: {business_type}

                Provide a structured report in clear Hinglish with the following sections:
                1. Relevant Trademark Class (NICE Classification): Name the primary class (1-45) and sub-classes, explaining why.
                2. Distinctiveness & Conflict Analysis: Check for generic words and phonetic/visual similarity risks with existing known brands.
                3. Risk Score (0% to 100%): Give a clear percentage (Low / Moderate / High Risk) with a 2-line verdict.
                4. Actionable Suggestions & Safe Alternatives: Provide 3 distinctive and safer name variations.
                """

                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt
                )
                
                st.success("Analysis Complete!")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Error aaya: {str(e)}")
              
