import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, Table, TableStyle, Frame, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from io import BytesIO
import datetime
import base64
from page2 import add_page_two
from page2 import add_page_four

genset_data = {
    "5 KVA": {"kWe": 4, "model": "KD15-441GSI4", "bhp": 8.2, "dim": "1050 x 620 x 745", "tank": 15},
    "10 KVA": {"kWe": 8, "model": "M2155G1", "bhp": 16.3, "dim": "1750 x 900 x 1250", "tank": 55},
    "15* KVA": {"kWe": 12, "model": "M2155G2", "bhp": 18.3, "dim": "1750 x 900 x 1250", "tank": 55},
    "15 KVA": {"kWe": 12, "model": "M3205G1", "bhp": 22.7, "dim": "1990 x 900 x 1330", "tank": 75},
    "20* KVA": {"kWe": 16, "model": "M3205G2", "bhp": 25.2, "dim": "1990 x 900 x 1330", "tank": 75},
    "25* KVA": {"kWe": 20, "model": "M3205G3", "bhp": 30.5, "dim": "1990 x 900 x 1330", "tank": 75},
    "25 KVA": {"kWe": 20, "model": "M3205G4", "bhp": 35.1, "dim": "1990 x 900 x 1330", "tank": 75},
    "30 KVA": {"kWe": 24, "model": "M3205G5", "bhp": 40, "dim": "2325 x 980 x 1330", "tank": 75},
    "35* KVA": {"kWe": 28, "model": "M320565", "bhp": 40, "dim": "2325 x 980 x 1330", "tank": 75},
    "40 KVA": {"kWe": 32, "model": "M4275G1", "bhp": 51.8, "dim": "2325 x 980 x 1330", "tank": 115},
    "45* KVA": {"kWe": 36, "model": "M4275G1", "bhp": 51.8, "dim": "2325 x 980 x 1330", "tank": 115},
    "50 KVA": {"kWe": 40, "model": "V435561", "bhp": 65.4, "dim": "2600 x 1130 x 1575", "tank": 156},
    "58.5 KVA": {"kWe": 46.8, "model": "V4355G2", "bhp": 75.5, "dim": "2600 x 1130 x 1575", "tank": 156},
    "82.5 KVA": {"kWe": 66, "model": "V4355G4", "bhp": 101.3, "dim": "3190 x 1225 x 1575", "tank": 169},
    "100 KVA": {"kWe": 80, "model": "H4485G2", "bhp": 126, "dim": "3950 x 1350 x 1425", "tank": 250},
    "125 KVA": {"kWe": 100, "model": "H4485G1", "bhp": 156, "dim": "3950 x 1350 x 1425", "tank": 250},
    "160 KVA": {"kWe": 128, "model": "H6725G2", "bhp": 199, "dim": "4201 x 1400 x 1745", "tank": 388},
    "180 KVA": {"kWe": 144, "model": "H6725G3", "bhp": 223, "dim": "4201 x 1400 x 1745", "tank": 388},
    "200 KVA": {"kWe": 160, "model": "H6725G4", "bhp": 247, "dim": "4201 x 1400 x 1745", "tank": 388},
    "250 KVA": {"kWe": 200, "model": "H6935G1", "bhp": 310, "dim": "4750 x 1600 x 2000", "tank": 425},
    "320 KVA": {"kWe": 256, "model": "H6935G2", "bhp": 390, "dim": "4750 x 1600 x 2000", "tank": 570},
}




st.set_page_config(page_title="Quotation Generator", layout="centered")
st.title("🧾 Quotation PDF with Header, Inputs & Preview")

# === USER INPUT FIELDS ===
lead_ref = st.text_input("🔢 Lead Reference Number", value="V-42-06")
customer_name = st.text_area("🏢 Customer/Company Name", value="PARVATI ENGINEERS & CONTRACTORS\nKOLHAPUR")
ref_source = st.selectbox("📞 Reference Source", ["Enquiry Over Telephone", "IndiaMart", "Email", "Walk-In"])
kva_choice = st.selectbox("Select Genset Rating (kVA):", genset_data.keys())
details = genset_data[kva_choice]

st.write(f"**Power Rating (kWe):** {details['kWe']}")
st.write(f"**Engine Model:** {details['model']}")
st.write(f"**Rated Power Output (BHP):** {details['bhp']}")
st.write(f"**Dimensions (L×W×H):** {details['dim']}")
st.write(f"**Fuel Tank Capacity:** {details['tank']} L")
phase_choice = st.selectbox("🔌 Phase", ["Single Phase", "3 Phase"])
num_sets = st.number_input("Number of Generators", min_value=1, value=1)
dg_cost = st.number_input("Cost per Generator (INR)", min_value=10000, value=385000)
transport_cost = st.number_input("Transportation Cost (INR)", min_value=0, value=8000)
amf_cost = st.number_input("Optional AMF Panel Cost (INR)", min_value=0, value=16500)
contact_number = st.text_input("📞 Contact Number", value="9096255252")
email_address = st.text_input("📧 Email", value="")
attention_name = st.text_input("👤 Kind Attention", value="Mr. Sangram Repe")

bottom_right_image_path = "footer_img.png"
header_path = "header.png"

# === CLOSING SECTION ===
def add_closing_section(pdf, width, height):
    styles = getSampleStyleSheet()
    normal = styles["Normal"]

    # Enclosed docs list
    enclosed_items = [
        Paragraph("<b>Enclosed documents are the part of our quotation:</b>", normal),
        Spacer(1, 6),
        Paragraph("1. Catalogue of the DG Set", normal),
        Paragraph("2. Technical Specification", normal),
        Paragraph("3. Price Schedule with Terms and Conditions.", normal),
    ]

    # Optional image on the right
    try:
        img = Image("footer_img.png", width=140, height=100)
    except:
        img = Paragraph("", normal)

    enclosed_table = Table(
        [[enclosed_items, img]],
        colWidths=[300, 180],
        hAlign='LEFT'
    )
    enclosed_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))

    # Closing message
    closing_para = Paragraph(
        "We hope you will find our offer competitive and look forward to the receipt of your valuable order. "
        "However, if you would like to have any further information, please feel free to call us.",
        normal,
    )

    # Signature block
    signature = [
        Paragraph("Thanking you with Regards,", normal),
        Spacer(1, 6),
        Paragraph("<b>For Techno Electromechs</b>", normal),
        Paragraph("Venkatesh Bhat", normal),
        Paragraph("9823012044 / 9022330752", normal),
        Paragraph("e-mail: techno.tems@gmail.com", normal),
        Spacer(1, 10),
        Paragraph("REG ADDRESS: 54/15 A, “SHRI-NIVASA”, NEAR VASANTRAO CHOUGULE SCHOOL, MOREWADI ROAD, KOLHAPUR-416004", normal),
        Spacer(1, 10),
        Table(
    [[Paragraph("<b><i>Techno Serving the Customer since 25 years</i></b>", styles["Normal"])]],
    colWidths=[460],
    style=TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.yellow),          # Yellow background
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.red),              # Red text
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTSIZE", (0, 0), (-1, -1), 12),                       # Slightly bigger text
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),                   # More vertical padding
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.red),               # Red border box
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
    ])
),
Spacer(1, 6),


    ]

    # Frame
    frame = Frame(40, 60, width - 80, height - 500, showBoundary=0)
    elements = [enclosed_table, Spacer(1, 20), closing_para, Spacer(1, 20)] + signature
    frame.addFromList(elements, pdf)

# === PDF GENERATION ===
def create_pdf():
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    try:
        pdf.drawImage(header_path, x=0, y=height - 50 * mm, width=210 * mm, height=45 * mm)
    except Exception as e:
        st.error(f"⚠️ Could not load header: {e}")
        return None

    y_pos = height - 180

    # Lead ref & date
    pdf.setFont("Helvetica-Bold", 11)
    # Draw background box
    box_x = 35
    box_y = y_pos - 5
    box_width = 530
    box_height = 25

    pdf.setFillColor(colors.whitesmoke)
    pdf.roundRect(box_x, box_y, box_width, box_height, radius=5, fill=True, stroke=False)

# Draw border
    pdf.setLineWidth(0.5)
    pdf.setStrokeColor(colors.gray)
    pdf.roundRect(box_x, box_y, box_width, box_height, radius=5, fill=False, stroke=True)

# Add text
    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(45, y_pos, f"LEAD REFERENCE: {lead_ref}")
    pdf.drawString(350, y_pos, f"DATE: {datetime.date.today().strftime('%d-%m-%Y')}")

    y_pos -= 30

    # Customer info
    pdf.setFont("Helvetica", 11)
    for line in customer_name.split("\n"):
        pdf.drawString(40, y_pos, line.strip())
        y_pos -= 15

    y_pos -= 10
    pdf.drawString(40, y_pos, f"Contact: {contact_number}")
    y_pos -= 15
    pdf.drawString(40, y_pos, f"e-mail: {email_address}")
    y_pos -= 15
    pdf.drawString(40, y_pos, f"KIND ATTENTION: {attention_name}")
    y_pos -= 25

    pdf.drawString(40, y_pos, f"REFERENCE: {ref_source}")
    y_pos -= 20
    pdf.drawString(40, y_pos, f"SUB: Offer for the supply of Mahindra Powerol make {kva_choice}-{phase_choice} CPCB -IV+ Emission Norms DG-SET")
    y_pos -= 35

    pdf.setFont("Helvetica", 11)
    pdf.drawString(40, y_pos, "Dear Sir / Madam,")
    y_pos -= 20

    # Paragraph
    styles = getSampleStyleSheet()
    para_text = (
        f"We thank you very much for your valuable enquiry and are pleased to quote our best and reasonable offer "
        f"for the supply of <b>Mahindra Powerol make {kva_choice} {phase_choice} CPCB -IV+</b> Emission Norms DG SET."
    )
    paragraph = Paragraph(para_text, style=styles["Normal"])
    frame = Frame(40, y_pos - 60, width=500, height=60, showBoundary=0)
    frame.addFromList([paragraph], pdf)
    y_pos -= 80

    # Add closing section
    add_closing_section(pdf, width, height)

    # Page 2: Generator Info Page
    add_page_two(pdf, kva_choice, phase_choice)
    add_page_four(pdf, kva_choice, phase_choice, num_sets, dg_cost, transport_cost, amf_cost)
    pdf.save()
    buffer.seek(0)
    return buffer

# === STREAMLIT UI ===
if st.button("📄 Generate PDF with Preview"):
    pdf_data = create_pdf()
    if pdf_data:
        st.success("✅ PDF Generated!")
        base64_pdf = base64.b64encode(pdf_data.read()).decode('utf-8')
        pdf_data.seek(0)
        st.markdown("### 🖼️ Preview:")
        st.markdown(f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="800"></iframe>', unsafe_allow_html=True)
        st.download_button(
            label="📥 Download PDF",
            data=pdf_data,
            file_name=f"quotation_{lead_ref}.pdf",
            mime="application/pdf"
        )


