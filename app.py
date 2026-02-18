import streamlit as st

st.set_page_config(page_title="NZ LAW & BUILDING - FREE Beta", page_icon="🏗️", layout="centered")

st.title("🏗️ FREE BETA")
st.header("NZ Building Consent Check Report")

st.subheader("Get a full expert NZ Building Code check **100% FREE** right now")

st.write("Help us test NZLegalMaster Pro. Your professional report comes back in 24-48 hours by email.")

st.divider()

st.markdown("""
**What you get:**
- Full risk check (structure, fire, moisture, H1 energy, etc.)
- Exact fixes with real Building Code references
- Probability of council approval
- Clean professional report ready to send
""")

st.success("**Completely free during beta** – your feedback makes it better!")

with st.form("beta_form", clear_on_submit=True):
    name = st.text_input("Your full name *", placeholder="John Smith")
    email = st.text_input("Your email * (report sent here)", placeholder="your@email.com")
    project = st.text_area("Tell us about your project", placeholder="e.g. new deck in Auckland, house extension, 2m retaining wall...")
    concerns = st.text_area("Any specific worries?", placeholder="H1 insulation, fire rating, moisture, RMA, classification...")

    st.markdown("### 📎 Drag & drop your files here")
    files = st.file_uploader(
        "Plans, RFIs, RCs, PDFs, drawings, photos – any number allowed",
        accept_multiple_files=True,
        type=['pdf', 'jpg', 'jpeg', 'png', 'dwg', 'doc', 'docx']
    )

    submitted = st.form_submit_button("🚀 Submit for FREE Report", type="primary", use_container_width=True)

if submitted:
    if name and email and files:
        st.success(f"✅ Thank you {name}! {len(files)} files received.")
        st.balloons()
        st.info(f"Your report will be emailed to **{email}** within 24-48 hours.\n\nNZLegalMaster Pro is analysing everything now.")
    else:
        st.error("Please fill name, email and upload at least one file.")

st.caption("**Not legal or building advice. Always check with a qualified professional, your council, or lawyer. Laws can change. This is an AI tool only.**")
