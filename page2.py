from reportlab.platypus import Paragraph, Table, TableStyle, Frame, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

from reportlab.platypus import Table, TableStyle, Image, Paragraph
from reportlab.lib import colors
from reportlab.platypus import Paragraph, Table, TableStyle, Frame, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm


# ===== Genset Database =====
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

def make_section(image_path, content_lines, styles):
    # Create Image (left) and content (right)
    img = Image(image_path, width=180, height=130)

    bullet_points = [Paragraph(f"• {line}", styles["Normal"]) for line in content_lines]

    table = Table(
        [[img, bullet_points]],
        colWidths=[190, 350]
    )

    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("BOX", (0, 0), (-1, -1), 0.25, colors.grey),
    ]))

    return table


def add_page_two(pdf, kva_choice, phase_choice):
    pdf.showPage()
    width, height = A4
    styles = getSampleStyleSheet()
    data = genset_data.get(kva_choice, {})
    kWe = data.get("kWe", "N/A")
    model = data.get("model", "N/A")
    bhp = data.get("bhp", "N/A")

    header_title = f"<b><font size=14 color='darkblue'>MAHINDRA POWEROL {kva_choice} {phase_choice.upper()} DG SET</font></b>"
    sub_title = "<font size=12 color='gray'>(CPCB-IV+ Emission Norms)</font>"
    header_frame = Frame(40, height - 100, width - 80, 60, showBoundary=0)
    header_frame.addFromList([
        Paragraph(header_title, styles["Title"]),
        Spacer(1, 6),
        Paragraph(sub_title, styles["Normal"])
    ], pdf)

    sections = []
    warranty_text = (
    "Warranty: 1 Year / 5000 Hrs. & 5C for 5 Years"
    if kva_choice.strip().startswith("5")
    else "Warranty: 2 Years / 5000 Hrs. & 5C for 5 Years"
)

    sections.append(make_section("features.png", [
    "<b>Product Salient Features:</b>",
    "Low operating & Maintenance cost (500 Hrs./1Year)",
    "Wide Service Network across India",
    "Proven Engine & Rugged Usage",
    "CPCB IV+ Compliant | Remote Monitoring",
    "Single Window Warranty Policy",
    "Low Footprint | Umbrella Sales+Service",
    warranty_text
], styles))

    sections.append(make_section("engine.png", [
        "<b>ENGINE:</b>",
        "Mahindra 4 Stroke, Inline, Liquid Cooled",
        "Mechanical, Low Fuel Consumption",
        "Dry Air Cleaner + Indicator",
        "Electrical Starter Motor + Charging Alt.",
        "Lube Oil & Coolant Pre-filled",
        "1 × 12V DC Battery",
        f"<b>Model: {model} | BHP: {bhp} | RPM: 1500</b>"
    ], styles))

    sections.append(make_section("alternator.png", [
        "<b>ALTERNATOR:</b>",
        "Brushless, Revolving Field, Self-excited",
        "Complies with IS/IEC60034-1",
        "H-Class Insulation | Compact Build",
        "Sealed Bearings | Light Weight",
        f"<b>Power: {kva_choice} KVA / {kWe} KW, 415V, 0.8 PF</b>",
        "Max Unbalanced Load (Phase): 10%"
    ], styles))

    sections.append(make_section("controller.png", [
        "<b>CONTROLLER:</b>",
        "Sedmac GC111X (ARM-based) with Graphic LCD & Backlit Display",
        "Modes: AMF, Manual, Remote Start/Stop (1φ & 3φ)",
        "Engine Monitoring: Oil Pressure, Coolant Temp, Fuel, Battery, Hours",
        "Alternator Monitoring: Voltage (L-N, L-L), Current, KW/KVA, Frequency, PF",
        "Protections: Low Oil, High Temp, Overspeed, Sensor Faults, Low Fuel, Battery Volts",
        "AC Protections: Under/Over Voltage & Frequency, Overload, Load Imbalance, Sensing Faults",
        "Maintenance Alerts: Run Hours & Due Date",
        "Communication: USB, RS485, CAN | Front Panel Configurable"
    ], styles))

    frame = Frame(40, 40, width - 80, height - 140, showBoundary=0)
    content = []
    for sec in sections:
        content.append(sec)
        content.append(Spacer(1, 20))
    frame.addFromList(content, pdf)
    add_page_three(pdf, kva_choice, phase_choice)

# ===== Page 3 =====
def add_page_three(pdf, kva_choice, phase_choice):
    pdf.showPage()
    width, height = A4
    styles = getSampleStyleSheet()
    data = genset_data.get(kva_choice, {})
    dims = data.get("dim", "N/A")
    tank = data.get("tank", "N/A")

    header_title = f"<b><font size=14 color='darkblue'>MAHINDRA POWEROL {kva_choice} {phase_choice.upper()} DG SET</font></b>"
    sub_title = "<font size=12 color='gray'>(CPCB-IV+ Emission Norms)</font>"
    frame_header = Frame(40, height - 140, width - 80, 60, showBoundary=0)
    frame_header.addFromList([
        Paragraph(header_title, styles["Title"]),
        Spacer(1, 6),
        Paragraph(sub_title, styles["Normal"])
    ], pdf)

    enclosure_points = [
        "<b>Specifically designed</b> to meet stringent MoEF / CPCB norms",
        "Performs from <b>10°C to 55°C</b> without external cooling",
        "<b>Fade-resistant UV</b> powder-coated paint",
        "Fire retardant insulation (PU Foam / Rockwool)",
        "<b>Draw-out fuel tank</b> for easy maintenance",
        "Compact design with <b>lowest footprint</b>",
        "<b>Easy access</b> for serviceable parts",
        "Mounted on common MS base frame with AVM pads",
        "<b>External fuel filling</b> provision (Outside Canopy)",
        "After Treatment System (ATS) for emissions",
        f"Dimensions: <b>{dims} mm</b>",
        f"Fuel Tank Capacity: <b>{tank} L</b>"
    ]

    try:
        image = Image("features.png", width=180, height=130)
    except:
        image = Paragraph("", styles["Normal"])

    enclosure_table = Table(
        [[image, [Paragraph(f"• {pt}", styles["Normal"]) for pt in enclosure_points]]],
        colWidths=[190, 350]
    )

    enclosure_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("BOX", (0, 0), (-1, -1), 0.25, colors.grey),
    ]))

    frame = Frame(40, 60, width - 80, height - 200, showBoundary=0)
    frame.addFromList([enclosure_table], pdf)

    



def add_page_four(pdf, kva_choice, phase_choice, num_sets, dg_cost, transport_cost, amf_cost):
    pdf.showPage()
    width, height = A4
    styles = getSampleStyleSheet()

    # Header
    header_frame = Frame(40, height - 120, width - 80, 80, showBoundary=0)
    header_frame.addFromList([
        Paragraph("<b><font size=16 color='darkblue'>TECHNO ELECTROMECHS</font></b>", styles["Title"]),
        Spacer(1, 6),
        Paragraph(f"<b><font size=12>PRICE SCHEDULE WITH TECHNICAL SPECIFICATIONS – {kva_choice.upper()} CPCB-IV+ SILENT DG SET</font></b>", styles["Normal"])
    ], pdf)

    desc_text = f"Mahindra Powerol {kva_choice} {phase_choice.upper()} Diesel Generating Set (CPCB-IV+) with Auto Logic Panel (discounted price)"

    # === Calculations ===
    total_dg_cost = num_sets * dg_cost
    total_basic = total_dg_cost + transport_cost
    gst = round(total_basic * 0.18, 2)
    net_cost = total_basic + gst

    # Table data
    data = [
        [Paragraph("<b>SL.NO.</b>", styles["Normal"]),
         Paragraph("<b>DESCRIPTION</b>", styles["Normal"]),
         Paragraph("<b>QTY.</b>", styles["Normal"]),
         Paragraph("<b>RATE (INR)</b>", styles["Normal"]),
         Paragraph("<b>AMOUNT (INR)</b>", styles["Normal"])],

        ["01",
         Paragraph(desc_text, styles["Normal"]),
         f"{num_sets} NO.",
         f"{dg_cost:,.2f}",
         f"{total_dg_cost:,.2f}"],

        ["02",
         Paragraph("Transportation", styles["Normal"]),
         "01 JOB",
         f"{transport_cost:,.2f}",
         f"{transport_cost:,.2f}"],

        ["",
         Paragraph("<b>Total Basic Cost</b>", styles["Normal"]),
         "",
         "",
         Paragraph(f"<b>{total_basic:,.2f}</b>", styles["Normal"])],

        ["",
         Paragraph("GST @ 18%", styles["Normal"]),
         "",
         "",
         Paragraph(f"<b>{gst:,.2f}</b>", styles["Normal"])],

        ["",
         Paragraph("<b>Net Cost: DG SET SUPPLY</b>", styles["Normal"]),
         "",
         "",
         Paragraph(f"<b>{net_cost:,.2f}</b>", styles["Normal"])],

        ["",
         Paragraph("<i>Optional: AMF Panel (Auto Control Panel), if required</i>", styles["Normal"]),
         "",
         "",
         f"{amf_cost:,.2f}" if isinstance(amf_cost, (int, float)) else amf_cost]
    ]

    table = Table(data, colWidths=[25*mm, 90*mm, 25*mm, 30*mm, 35*mm])
    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DDEEFF")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (2, 1), (-1, -1), "RIGHT"),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("SPAN", (1, 6), (3, 6)),
        ("TEXTCOLOR", (1, 6), (1, 6), colors.gray),
    ]))

    # Frame to place content
    content_frame = Frame(40, 40, width - 80, height - 160, showBoundary=0)
    content_frame.addFromList([table], pdf)
    # Add contact block below the table
    contact = [
    Spacer(1, 100),
    Paragraph("<b>Thanking You,</b>", styles["Normal"]),
    Paragraph("<b>Yours Sincerely,</b>", styles["Normal"]),
    Spacer(1, 6),
    Paragraph("<b>TECHNO ELECTROMECHS</b>", styles["Normal"]),
    Paragraph("VENKATESH BHAT", styles["Normal"]),
    Paragraph("📞 9823012044 / 9022330752", styles["Normal"]),
    Spacer(1, 6),
    Paragraph("<i>Techno Serving the Customer since 25 years</i>", styles["Italic"]),
    Paragraph("<b><font color='darkblue'>AUTHORISED SALES SERVICE AND SPARES</font></b>", styles["Normal"]),
]

    content_frame.addFromList(contact, pdf)
    # Call page five
    add_page_five(pdf)


from reportlab.platypus import Paragraph, Frame, Table, TableStyle, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def add_page_five(pdf):
    pdf.showPage()
    width, height = A4
    styles = getSampleStyleSheet()
    
    # Custom paragraph style for better readability
    styles.add(ParagraphStyle(name='Justify', alignment=4, fontSize=9, leading=12))

    # === Page Title ===
    title = Paragraph("<b><font size=14 color='darkblue'>TECHNO ELECTROMECHS</font></b>", styles["Title"])
    subtitle = Paragraph("<b><font size=12>TERMS & CONDITIONS:</font></b>", styles["Heading3"])

    full_text = """
<b>Taxes:</b> Prices are Inclusive of GST in net cost @18%. Shown as above.<br/><br/>
<b>TERMS OF PAYMENT:</b> 100% advance for Immediate Delivery or 30% payment as an advance along with order & balance 70% payment against Performa invoice prior to dispatch from our OEM factory.<br/><br/>
<b>FREIGH & TRANSIT INSURANCE:</b> Prices are Included in net cost<br/><br/>
<b>STATUTORY APPROVALS:</b> Approvals from concern authorities shall be to customer’s account.<br/><br/>
<b>DELIVERY:</b> Supply within 2-4 Weeks from the date of receipt of your order along with advance, subject to force majeure conditions and unforeseen delay, which is beyond our / our manufacturers’ control.<br/><br/>
<b>WARRANTY:</b> The offered Engine & Alternator is warranted for a period of 2 years from the date of dispatch OR 6000 Hrs. of operation from the date of commissioning, whichever is earlier against any manufacturing defect/defective materials only. However, electrical and other proprietary items would be covered as per their respective manufacturer’s standard warranty clause. The warranty will not cover the normal wear and tear or damages caused by accident, wrong handling and improper maintenance. Warranty is not applicable for contactors and other electrical components fitted on main source of supply line<br/><br/>
<b>VALIDITY:</b> Our offer shall remain valid for a period of 8 Days and subject to our confirmation thereafter.<br/><br/>
<b>SCOPE OF SUPPLY:</b> Our offer is confined to whatever is specifically included and stipulated in the technical and commercial clauses and is subject to changes as may be mutually agreed upon finalization of the contract.<br/><br/>
<b>EXCLUSIONS:</b> Our offer is for supply of equipment only. Installation job work, i.e., unloading of DGset at site, earthing pits, G.I. strips, foundation, power cabling & control cabling with end terminations, exhaust piping with supports, manual changeover switch etc. Shall be charged extra.<br/><br/>
<b>ARBITRATION:</b> In the event of any disputes or differences arising between the parties out of or relating to the validity, construction, meaning, operation or effect of this offer, or any amendments or other documents relating to this offer, or the breach of the terms of any document agreed to between the parties, the same shall be referred to Arbitration, as per the provisions of the Arbitration and Conciliation Act 1996 and the arbitration proceedings shall be held at respective jurisdiction area.<br/><br/>
<b>SPECIAL CLAUSE:</b><br/>
1. Customer must indicate their GST/TAN/PAN & date in their Purchase Order.<br/>
2. If the delivery of the DG Set is not taken as per the Order, then equipment may be delivered to other customer and new delivery schedule will be mutually decided with the price implication as required.<br/>
3. Cancellation Charges: If purchase order is cancelled by the customer, cancellation charges will be applicable @ 2.5% of the basic order value<br/><br/>
It will be a pleasure serving you for your valued requirement. Looking forward to provide you our best of the services.
"""

    contact = [
        Paragraph("<b>Thanking You,</b>", styles["Normal"]),
        Paragraph("<b>Yours Sincerely,</b>", styles["Normal"]),
        Spacer(1, 6),
        Paragraph("<b>TECHNO ELECTROMECHS</b>", styles["Normal"]),
        Paragraph("VENKATESH BHAT", styles["Normal"]),
        Paragraph("📞 9823012044 / 9022330752", styles["Normal"]),
        Spacer(1, 6),
        Paragraph("<i>Techno Serving the Customer since 25 years</i>", styles["Italic"]),
        Paragraph("<b><font color='darkblue'>AUTHORISED SALES SERVICE AND SPARES</font></b>", styles["Normal"]),
    ]

    content = [title, subtitle, Spacer(1, 6), Paragraph(full_text, styles["Justify"])] + contact

    # Wrap everything inside a table with border (like a box)
    box = Table([[c] for c in content], colWidths=[width - 80])
    box.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 1.0, colors.black),
        ("INNERPADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))

    frame = Frame(40, 40, width - 80, height - 60, showBoundary=0)
    frame.addFromList([box], pdf)
