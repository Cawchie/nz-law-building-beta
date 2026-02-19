import streamlit as st
from openai import OpenAI
import PyPDF2
import io
from datetime import datetime

# Friendly Kiwi Resource Consent Expert (human tone)
SYSTEM_PROMPT = """You are a friendly, straight-talking Kiwi resource consent expert with 15 years experience. You help builders and homeowners get their consents approved fast and easy.

Talk like a helpful mate on the job site – simple words, short sentences, bullet points, encouraging, practical.

For "Do my plans need an RC" – give clear yes/no + why + next steps.

For "Write my resource consent" – draft the full application in plain English with all sections ready to submit.

For "Explain RFI" – explain what council is asking for and how to reply simply.

Always end with:
**Not legal or building advice. Always check with a qualified professional, your council, or lawyer. Laws can change. This is an AI tool only.**

Now, fully embody this expert."""

st.set_page_config(page_title="NZ Resource Consent Tool", page_icon="📋", layout="centered")

st.title("📋 NZ Resource Consent Tool")
st.header("Practical help with Resource Consents")

tab1, tab2, tab3 = st.tabs([
    "1. Do my plans need an RC and why?",
    "2. Write my resource consent",
    "3. Explain request for information from council"
])

def process_request(prompt_prefix, request, files):
    with st.spinner("NZ Resource Consent Advisor is working... (20-60 seconds)"):
        all_text = ""
        file_names = ""
        for file in files:
            file_names += f"• {file.name}\n"
            if file.name.lower().endswith('.pdf'):
                try:
                    pdf = PyPDF2.PdfReader(io.BytesIO(file.getvalue()))
                    for page in pdf.pages:
                        all_text += page.extract_text() + "\n\n"
                except:
                    pass

        user_message = f"{prompt_prefix}\nRequest: {request}\nFiles: {file_names}\nExtracted text: {all_text[:120000]}"

        client = OpenAI(
            api_key=st.secrets["xai_api_key"],
            base_url="https://api.x.ai/v1"
        )

        response = client.chat.completions.create(
            model="grok-4",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.3,
            max_tokens=8000
        )

        report = response.choices[0].message.content.strip()

        st.success("✅ Report ready!")
        st.markdown("### 📄 Your Report")
        st.markdown(report)

        st.download_button(
            label="📥 Download Report as TXT",
            data=report,
            file_name=f"Resource_Consent_Report_{datetime.now().strftime('%d%b')}.txt",
            mime="text/plain",
            use_container_width=True
        )
        st.info("💡 To save as PDF: Click browser menu → Print → Save as PDF")

# Tab 1
with tab1:
    st.subheader("Do my plans need a Resource Consent?")
    name1 = st.text_input("Your name", key="name1")
    request1 = st.text_area("Describe your project", key="request1", placeholder="New 2m deck at 123 Beach Rd, Auckland...")
    files1 = st.file_uploader("Drag & drop plans, photos, site plans", accept_multiple_files=True, type=['pdf','jpg','jpeg','png','dwg'], key="files1")
    if st.button("Check if I need an RC", type="primary", use_container_width=True):
        if name1 and request1 and files1:
            process_request("Do these plans need a Resource Consent and why?", request1, files1)
        else:
            st.error("Please fill name, request and upload files")

# Tab 2
with tab2:
    st.subheader("Write my Resource Consent application")
    name2 = st.text_input("Your name", key="name2")
    request2 = st.text_area("Describe your project", key="request2", placeholder="3-bedroom house on rural Waikato site with on-site wastewater...")
    files2 = st.file_uploader("Drag & drop plans and documents", accept_multiple_files=True, type=['pdf','jpg','jpeg','png','dwg'], key="files2")
    if st.button("Write my full Resource Consent application", type="primary", use_container_width=True):
        if name2 and request2 and files2:
            process_request("Write the full Resource Consent application for this project", request2, files2)
        else:
            st.error("Please fill name, request and upload files")

# Tab 3
with tab3:
    st.subheader("Explain this Request for Information from council")
    name3 = st.text_input("Your name", key="name3")
    request3 = st.text_area("Paste or describe the RFI", key="request3", placeholder="Council asked for more info on stormwater, shading and neighbour consultation...")
    files3 = st.file_uploader("Drag & drop the RFI letter + your plans", accept_multiple_files=True, type=['pdf','jpg','jpeg','png','dwg'], key="files3")
    if st.button("Explain this RFI and how to reply", type="primary", use_container_width=True):
        if name3 and request3 and files3:
            process_request("Explain this RFI from council and how to reply", request3, files3)
        else:
            st.error("Please fill name, RFI description and upload files")

st.caption("**Not legal or building advice. Always check with a qualified professional, your council, or lawyer. Laws can change. This is an AI tool only.**")
st.caption("Built for Cawchi – NZ Resource Consent Tool")
