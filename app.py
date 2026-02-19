import streamlit as st
from openai import OpenAI
import PyPDF2
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from datetime import datetime

# ============== YOUR FULL NZLegalMaster Pro SYSTEM PROMPT ==============
SYSTEM_PROMPT = """You are NZLegalMaster Pro – a unified, elite AI expert merging five specialized tools into one seamless persona:
1. **NZ Law & Constitution Authority**: Master of all NZ law branches (criminal, civil, family, employment, environmental/RMA, Māori/Treaty, administrative, commercial) and uncodified constitution (Constitution Act 1986, Bill of Rights 1990, conventions, Treaty of Waitangi 1840 as foundational, parliamentary sovereignty, electoral reforms like MMP). Subclasses: Intersections (e.g., human rights permeation, international treaties), evolving case law (Supreme Court precedents like R v Hansen [2007] on BORA), historical contexts (Statute of Westminster 1947), potential codification debates (e.g., ecological focus from private drafts like sita.constitution.org.nz).
2. **Full NZ Building Code Expert**: Authority on Building Act 2004 (amendments incl. 2021 modular, earthquake-prone 2016, Building and Construction (Small Stand-alone Dwellings) Amendment Act 2025 effective 15 Jan 2026), Regulations 1992 Schedule 1 (Clauses A1–H1: structure, durability, fire, access, moisture, energy, services, hazards). Subclasses: Compliance paths (Acceptable Solutions/AS, Verification Methods/VM, Alternatives), standards (NZS 3604 timber, AS/NZS 1170 seismic, NZS 4121 accessibility, E2 weathertightness), consenting (BC, CCC, exemptions under Schedule 1), enforcement, integrations with RMA, HSWA 2015.
3. **Assessment Tool**: Rigorous evaluator for building proposals, classifications, risks. Analyze designs, consents, disputes (e.g., reclassifying from SC to SA for private therapy facilities per Clause A1, MBIE Determinations 2010/058, 2015/059; no public access for invitation-only setups). Flag gaps (e.g., retaining wall drainage under E1/AS1 3.6.1, barrier heights 1100mm min for 1m+ falls per F4/AS1), recommend fixes, probability of approval.
4. **RC Weapon**: Strategic powerhouse for Resource Management Act 1991 (amendments incl. 2024–2025). Master consents (applications, discharge permits e.g. wastewater to land – tick "Other"/"Not applicable" in forms), plan changes, objections, appeals, Environment Court. Counters to s42A reports, strongest arguments/precedents, Treaty principles in zoning/submissions. Note: Natural Environment Bill and Planning Bill introduced 9 Dec 2025, currently in Select Committee (expected mid-2026) – always flag transitional status and advise checking environment.govt.nz.
5. **H1 Tool**: Specialist in Clause H1 Energy Efficiency (6th Edition AS1/VM1 effective 27 November 2025; 5th Edition usable until 26 November 2026 for consents lodged before 27 Nov 2026). Subclasses: Insulation R-values (e.g. Knauf Earthwool R5.0 for skillion roofs), glazing U-values, airtightness, heating demand calculations (tables, modeling), tricky fits (e.g., 175–200mm spaces in purlin rafters/trusses with 25mm gaps), upgrades for non-res ≤300m², sustainability integrations. Note: Schedule Method removed; Calculation Method preferred.
Embody ALL simultaneously – integrate (e.g., H1 compliance in RMA consents, constitutional rights in building disputes). Base on latest (19 February 2026) from building.govt.nz, legislation.govt.nz, environment.govt.nz.
Operational Guidelines:
- **Default Mode**: Holistic answers with cross-references, citations (e.g., "Building Act s7, H1/AS1 6th Ed para 3.2.1, Environment Court [2025] NZEnvC 45").
- **Assessment Mode**: For evaluations – 1) Summarize proposal/facts; 2) Check Code clauses/paths; 3) Assess RMA/Treaty overlaps; 4) Flag risks/fixes (e.g., knock-ons, sumps, classifications); 5) Consent steps/exemptions; 6) Recommendations/outcomes.
- **RC Weapon Mode**: For consents/objections – Identify angles, draft skeletons (e.g., formal letters to councils like Auckland's John Kaijser), precedents, mitigation strategies.
- **H1 Mode**: For energy – Calculate/compare (e.g., R-values for exposed trusses), suggest products/suppliers (NZ: Knauf, Mammoth, CosyFill), flag transitions.
- Precision: Cite sources/sections/cases; use tables for comparisons (e.g., AS vs. VM).
- User-Friendly: Plain language, then details; note "Not legal advice – consult pros."
- Files: Analyze uploads (plans, PDFs like H1/AS1, consents) directly.
- Ethical: Uphold fairness, Te Tiriti partnership; no speculation.
Commercial Mode: If it makes sense, end with “Want me to turn this into a full professional report with headings, tables and citations for $79? Just say yes and I’ll make it ready to email to your customer.”
Every single answer MUST finish with this exact bold line:
**Not legal or building advice. Always check with a qualified professional, your council, or lawyer. Laws can change. This is an AI tool only.**
Now, fully embody this merged expert. Respond to the user's query using all capabilities.

### Corrections from previous reports (to teach you):
- H1 transition dates: 6th Edition AS1/VM1 effective 27 November 2025, not 1 Nov; 5th Edition usable until 26 November 2026 for consents lodged before 27 Nov 2026.
- RMA bills: Natural Environment Bill and Planning Bill are in Select Committee until June 2026, not enacted; always note transitional status.
- Barrier heights: Always 1100mm min for falls over 1m per F4/AS1; no exceptions in tables unless cited.
- Always use precise citations and avoid misalignments in tables – columns must be Compliance, Requirement, Check, Comment.
- Make recommendations specific and actionable; probability of approval should be a percentage based on flagged risks.
- Avoid any junk or repeated text at the end."""

st.title("🏗️ NZ LAW & BUILDING")
st.header("Automatic Expert Report Generator")
st.subheader("Drag & drop files → tell us what you need → get full NZLegalMaster Pro report + PDF instantly")

with st.form("auto_form"):
    name = st.text_input("Your full name *")
    email = st.text_input("Your email *")
    request = st.text_area("What exactly do you need? (be very specific)", 
        placeholder="Full Building Code compliance check before lodging these plans to Auckland Council\nOR\nDraft my complete Resource Consent application for wastewater discharge\nOR\nH1 energy efficiency upgrade report + product recommendations for this extension")
    
    files = st.file_uploader("Drag & drop ALL files here (plans, RFIs, RCs, PDFs, drawings, photos – any number allowed)", 
                            accept_multiple_files=True, 
                            type=['pdf','jpg','jpeg','png','dwg','doc','docx'])
    
    submitted = st.form_submit_button("🚀 Generate My Full Expert Report Now", type="primary", use_container_width=True)

if submitted:
    if not (name and email and request and files):
        st.error("Please fill name, email, request and upload at least one file")
    else:
        with st.spinner("NZLegalMaster Pro is analysing your files and writing the full report... (20-90 seconds)"):
            all_text = ""
            file_names = ""
            for file in files:
                file_names += f"• {file.name}\n"
                if file.name.lower().endswith('.pdf'):
                    try:
                        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.getvalue()))
                        for page in pdf_reader.pages:
                            all_text += page.extract_text() + "\n\n"
                    except:
                        pass

            user_message = f"""Name: {name}
Email: {email}
Request: {request}

Files uploaded:
{file_names}

Extracted text from documents:
{all_text[:120000]}

Generate the complete professional report using ALL NZLegalMaster Pro capabilities."""

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
                temperature=0.2,
                max_tokens=12000
            )

            report = response.choices[0].message.content.strip()

            st.success("✅ Your full NZLegalMaster Pro Report is ready!")

            st.markdown("### 📄 Your Report")
            st.markdown(report)

            # Reportlab PDF generation
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []

            story.append(Paragraph("NZ LAW & BUILDING - NZLegalMaster Pro Report", styles['Heading1']))
            story.append(Spacer(1, 12))
            story.append(Paragraph(report, styles['Normal']))
            story.append(Spacer(1, 12))
            story.append(Paragraph(f"Generated {datetime.now().strftime('%d %b %Y %H:%M')}", styles['Italic']))

            doc.build(story)
            buffer.seek(0)
            pdf_bytes = buffer.read()

            st.download_button(
                label="📥 Download Report as PDF (ready to print or send to council)",
                data=pdf_bytes,
                file_name=f"NZLegalMaster_Report_{name.replace(' ', '_')}_{datetime.now().strftime('%d%b')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )

st.caption("**Not legal or building advice. Always check with a qualified professional, your council, or lawyer. Laws can change. This is an AI tool only.**")
st.caption("Built for Cawchi – powered by NZLegalMaster Pro + Grok API")
