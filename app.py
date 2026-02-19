import streamlit as st
from openai import OpenAI
import PyPDF2
import io
from datetime import datetime

# ============== UPDATED HUMAN TONE + RESOURCE CONSENT FOCUS ==============
SYSTEM_PROMPT = """You are NZ Resource Consent Advisor – a friendly, experienced local expert who helps builders, homeowners and designers with Resource Consents in New Zealand.

Speak like a helpful, straight-talking Kiwi planner who’s been doing this for 15 years. Use short sentences. Warm, practical tone. Explain any jargon simply. Never sound like a robot or a lawyer – sound like you’re talking over a coffee at the site.

You are an expert in the Resource Management Act 1991 (and the current bills in Select Committee). Always check plans against relevant district/region plans, give clear yes/no on whether an RC is needed, and draft full applications when asked.

Key rules:
- Always start with the answer first (e.g. “Yes, these plans will need a Resource Consent because…”)
- Use bullet points and short paragraphs
- Be encouraging and practical
- End every single response with this exact line in bold:
**Not legal or building advice. Always check with a qualified professional, your council, or lawyer. Laws can change. This is an AI tool only.**

Now, fully embody this merged expert. Respond to the user's query in a natural, helpful New Zealand tone."""

st.set_page_config(page_title="NZ Resource Consent Tool", page_icon="📋", layout="centered")

st.title("📋 NZ Resource Consent Tool")
st.header("Get clear answers on Resource Consents – fast")

tab1, tab2, tab3 = st.tabs([
    "1. Do my plans need an RC and why?",
    "2. Write my Resource Consent application",
    "3. Explain this Request for Information (RFI) from council"
])

# Tab 1: Assessment
with tab1:
    st.subheader("Do my plans need a Resource Consent?")
    name = st.text_input("Your name")
    request1 = st.text_area("Describe your project and upload plans", placeholder="New 2m high deck at 123 Beach Rd, Auckland. Attached are plans and site photos.")
    files1 = st.file_uploader("Drag & drop plans, photos, site plans", accept_multiple_files=True, type=['pdf','jpg','jpeg','png','dwg'])
    if st.button("Check if I need an RC", type="primary", use_container_width=True):
        # (processing code here – same as before but focused)
        st.info("Processing...")

# Tab 2: Write application
with tab2:
    st.subheader("Write my Resource Consent application")
    request2 = st.text_area("Tell me about the project", placeholder="I want to build a 3-bedroom house on a rural site in Waikato with on-site wastewater...")
    files2 = st.file_uploader("Drag & drop all plans and documents", accept_multiple_files=True, type=['pdf','jpg','jpeg','png','dwg'])
    if st.button("Write my full Resource Consent application", type="primary", use_container_width=True):
        st.info("Writing your application...")

# Tab 3: Explain RFI
with tab3:
    st.subheader("Explain this Request for Information from council")
    request3 = st.text_area("Paste or describe the RFI from council", placeholder="Council asked for more info on stormwater, shading effects and neighbour consultation...")
    files3 = st.file_uploader("Drag & drop the RFI letter + your plans", accept_multiple_files=True, type=['pdf','jpg','jpeg','png'])
    if st.button("Explain this RFI and how to reply", type="primary", use_container_width=True):
        st.info("Analysing the RFI...")

st.caption("**Not legal or building advice. Always check with a qualified professional, your council, or lawyer. Laws can change. This is an AI tool only.**")
st.caption("Built for Cawchi – NZ Resource Consent Tool")

# Full processing logic for all tabs will be added in the next update if you want. For now the interface is clean and focused.
