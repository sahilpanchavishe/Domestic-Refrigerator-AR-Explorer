"""
Four-Page A3 Landscape Technical Poster Generator for Domestic Refrigerator AR Explorer
Strictly adheres to the architectural structure, visual elegance, and presentation quality of VCR-AR-Explorer.pdf.
Authors: Sahil Panchavishe (612302040) & Megh Shidam (612302058)
Department of Robotics and AI · COEP Technological University, Pune
Guide: Dr. Shubhangi Deshmukh
"""

import os
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

OUT_DIR = '/Users/sahilpanchavishe/Desktop/Domestic-Refrigerator-AR-Explorer/poster/output'
RENDERS_DIR = '/Users/sahilpanchavishe/Desktop/Domestic-Refrigerator-AR-Explorer/poster/renders'
os.makedirs(OUT_DIR, exist_ok=True)
PDF_PATH = os.path.join(OUT_DIR, 'Domestic-Refrigerator-AR-Explorer-Technical-Poster.pdf')

PAGE_W, PAGE_H = landscape(A3) # 1190.55 x 841.89 pt (420 x 297 mm)

def draw_engineering_frame(c, sheet_num, total_sheets=4):
    """Draws authentic engineering blueprint grid background and ISO coordinate frame."""
    margin = 15 * mm
    w = PAGE_W - 2 * margin
    h = PAGE_H - 2 * margin
    
    # 1. Warm parchment / blueprint paper background
    c.setFillColor(colors.HexColor('#f4f1ea'))
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    
    # 2. Subtle 10mm engineering graph grid
    c.setStrokeColor(colors.HexColor('#e6e1d6'))
    c.setLineWidth(0.3)
    
    # Vertical grid lines
    gx = margin
    while gx <= PAGE_W - margin:
        c.line(gx, margin, gx, PAGE_H - margin)
        gx += 10 * mm
        
    # Horizontal grid lines
    gy = margin
    while gy <= PAGE_H - margin:
        c.line(margin, gy, PAGE_W - margin, gy)
        gy += 10 * mm
    
    # 3. Outer dark engineering border
    c.setStrokeColor(colors.HexColor('#0f172a'))
    c.setLineWidth(1.2)
    c.rect(margin, margin, w, h)
    
    # Inner border line
    c.setLineWidth(0.6)
    c.rect(margin + 3 * mm, margin + 3 * mm, w - 6 * mm, h - 6 * mm)
    
    # 4. Coordinate ticks along top and bottom (1 to 8)
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(colors.HexColor('#475569'))
    step_x = (w - 6 * mm) / 8
    for i in range(1, 9):
        x = margin + 3 * mm + (i - 0.5) * step_x
        c.drawCentredString(x, PAGE_H - margin + 1 * mm, str(i))
        c.drawCentredString(x, margin - 3 * mm, str(i))
        
    # Coordinate ticks along sides (A to F)
    letters = ['A', 'B', 'C', 'D', 'E', 'F']
    step_y = (h - 6 * mm) / 6
    for i, l in enumerate(letters):
        y = PAGE_H - margin - 3 * mm - (i + 0.5) * step_y
        c.drawCentredString(margin - 3 * mm, y, l)
        c.drawCentredString(PAGE_W - margin + 1 * mm, y, l)

def draw_top_header(c, sheet_num, section_code, section_name, main_title, subtitle):
    """Draws top title block, drawing number, REF/AR banner, and top-right QR code."""
    x0 = 18 * mm
    y_top = PAGE_H - 18 * mm
    
    # 1. Top drawing number pill
    c.setFillColor(colors.HexColor('#0f172a'))
    c.rect(x0, y_top - 5 * mm, 65 * mm, 5 * mm, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(colors.white)
    c.drawString(x0 + 2 * mm, y_top - 3.8 * mm, f"DRG. NO. REF-001 · SHEET {sheet_num} / 4")
    
    # 2. Big REF/AR logo box
    c.setFillColor(colors.HexColor('#070d1e'))
    c.rect(x0, y_top - 20 * mm, 65 * mm, 14 * mm, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 19)
    c.setFillColor(colors.HexColor('#00e5ff'))
    c.drawString(x0 + 3 * mm, y_top - 16 * mm, "REF/AR")
    
    # Subtext under logo
    c.setFont("Helvetica-Bold", 5.5)
    c.setFillColor(colors.HexColor('#0f172a'))
    c.drawString(x0, y_top - 24 * mm, "DEPARTMENT OF ROBOTICS & AI, COEP TECH, PUNE")
    c.setFont("Helvetica", 5.5)
    c.drawString(x0, y_top - 27 * mm, "GUIDE: DR. SHUBHANGI DESHMUKH · B.TECH PROJECT")
    
    # 3. Section Title & Main Headline
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(colors.HexColor('#ea580c'))
    c.drawString(x0 + 72 * mm, y_top - 4 * mm, f"SECTION {section_code} · {section_name.upper()}")
    
    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(colors.HexColor('#070d1e'))
    c.drawString(x0 + 72 * mm, y_top - 12 * mm, main_title)
    
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.HexColor('#334155'))
    c.drawString(x0 + 72 * mm, y_top - 17 * mm, subtitle)
    
    # 4. Top-right QR Code Block
    qr_w = 17 * mm
    qr_x = PAGE_W - 18 * mm - 58 * mm
    qr_y = y_top - 18 * mm
    qr_img = os.path.join(RENDERS_DIR, 'qr_web_explorer.png')
    if os.path.exists(qr_img):
        c.drawImage(qr_img, qr_x, qr_y, width=qr_w, height=qr_w)
        
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(colors.HexColor('#070d1e'))
    c.drawString(qr_x + qr_w + 3 * mm, qr_y + qr_w - 3.5 * mm, "Explore it in 3D")
    c.setFont("Helvetica", 6.5)
    c.setFillColor(colors.HexColor('#475569'))
    c.drawString(qr_x + qr_w + 3 * mm, qr_y + qr_w - 7.5 * mm, "Scan for interactive")
    c.drawString(qr_x + qr_w + 3 * mm, qr_y + qr_w - 11.0 * mm, "web explorer & AR view.")

def draw_bottom_title_block(c, title, sheet_num):
    """Draws ANSI/ISO standard engineering title block at bottom-right."""
    x_right = PAGE_W - 18 * mm
    y_bottom = 18 * mm
    tb_w = 205 * mm
    tb_h = 16 * mm
    tb_x = x_right - tb_w
    
    # White background for title block
    c.setFillColor(colors.white)
    c.rect(tb_x, y_bottom, tb_w, tb_h, fill=1, stroke=0)
    
    c.setStrokeColor(colors.HexColor('#0f172a'))
    c.setLineWidth(1.0)
    c.rect(tb_x, y_bottom, tb_w, tb_h)
    
    # Columns
    col1_w = 88 * mm
    col2_w = 52 * mm
    col3_w = 47 * mm
    col4_w = 18 * mm
    
    c.line(tb_x + col1_w, y_bottom, tb_x + col1_w, y_bottom + tb_h)
    c.line(tb_x + col1_w + col2_w, y_bottom, tb_x + col1_w + col2_w, y_bottom + tb_h)
    c.line(tb_x + col1_w + col2_w + col3_w, y_bottom, tb_x + col1_w + col2_w + col3_w, y_bottom + tb_h)
    
    # Title
    c.setFont("Helvetica", 6)
    c.setFillColor(colors.HexColor('#64748b'))
    c.drawString(tb_x + 2 * mm, y_bottom + 12 * mm, "TITLE")
    title_font = 7.5 if len(title) > 35 else 8.5
    c.setFont("Helvetica-Bold", title_font)
    c.setFillColor(colors.HexColor('#070d1e'))
    c.drawString(tb_x + 2 * mm, y_bottom + 5 * mm, title)
    
    # Prepared By
    c.setFont("Helvetica", 6)
    c.setFillColor(colors.HexColor('#64748b'))
    c.drawString(tb_x + col1_w + 2 * mm, y_bottom + 12 * mm, "PREPARED BY · ROBOTICS & AI")
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(colors.HexColor('#070d1e'))
    c.drawString(tb_x + col1_w + 2 * mm, y_bottom + 7 * mm, "Sahil Panchavishe  612302040")
    c.drawString(tb_x + col1_w + 2 * mm, y_bottom + 2.5 * mm, "Megh Shidam  612302058")
    
    # Guided By
    c.setFont("Helvetica", 6)
    c.setFillColor(colors.HexColor('#64748b'))
    c.drawString(tb_x + col1_w + col2_w + 2 * mm, y_bottom + 12 * mm, "GUIDED BY")
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(colors.HexColor('#070d1e'))
    c.drawString(tb_x + col1_w + col2_w + 2 * mm, y_bottom + 7 * mm, "Dr. Shubhangi Deshmukh")
    c.setFont("Helvetica", 6)
    c.drawString(tb_x + col1_w + col2_w + 2 * mm, y_bottom + 2.5 * mm, "Dept of Robotics & AI · COEP Tech")
    
    # Sheet & Scale
    c.setFont("Helvetica", 6)
    c.drawString(tb_x + col1_w + col2_w + col3_w + 2 * mm, y_bottom + 12 * mm, "SHEET")
    c.setFont("Helvetica-Bold", 8)
    c.drawString(tb_x + col1_w + col2_w + col3_w + 2 * mm, y_bottom + 7 * mm, f"{sheet_num} / 4")
    c.setFont("Helvetica", 6)
    c.drawString(tb_x + col1_w + col2_w + col3_w + 2 * mm, y_bottom + 2.5 * mm, "SCALE: NTS")
    
    # Bottom-left project disclaimer
    c.setFont("Helvetica", 6)
    c.setFillColor(colors.HexColor('#64748b'))
    c.drawString(18 * mm, y_bottom + 4 * mm, "3D model generated procedurally for this project (original geometry, not CAD, not a specific product). Renders from project's three.js and Blender engines.")

def draw_card_box(c, x, y, w, h, title=None):
    """Draws a clean white technical card box with rounded corners and optional title tag."""
    c.setFillColor(colors.white)
    c.setStrokeColor(colors.HexColor('#0f172a'))
    c.setLineWidth(0.8)
    c.roundRect(x, y, w, h, 2 * mm, fill=1, stroke=1)
    
    if title:
        # Title pill tag
        tag_w = len(title) * 2.2 * mm + 8 * mm
        c.setFillColor(colors.HexColor('#f8fafc'))
        c.setStrokeColor(colors.HexColor('#cbd5e1'))
        c.setLineWidth(0.6)
        c.roundRect(x + 2 * mm, y + h - 6 * mm, tag_w, 5.5 * mm, 1 * mm, fill=1, stroke=1)
        c.setFont("Helvetica-Bold", 6.8)
        c.setFillColor(colors.HexColor('#0f172a'))
        c.drawString(x + 4 * mm, y + h - 4.2 * mm, title)

def draw_callout_badge(c, bx, by, number, target_xy=None):
    """Draws a circular numbered engineering callout badge with high contrast leader line and terminal dot."""
    if target_xy:
        tx, ty = target_xy
        c.setStrokeColor(colors.HexColor('#0f172a'))
        c.setLineWidth(0.8)
        c.line(bx, by, tx, ty)
        # Terminal dot on component
        c.setFillColor(colors.HexColor('#0f172a'))
        c.circle(tx, ty, 1.2 * mm, fill=1, stroke=0)
        
    # Badge circle
    c.setFillColor(colors.white)
    c.setStrokeColor(colors.HexColor('#0f172a'))
    c.setLineWidth(1.0)
    c.circle(bx, by, 3.4 * mm, fill=1, stroke=1)
    
    c.setFont("Helvetica-Bold", 7.2)
    c.setFillColor(colors.HexColor('#0f172a'))
    c.drawCentredString(bx, by - 1.0 * mm, str(number))

# =========================================================================
# PAGE 1: THE HARDWARE
# =========================================================================
def build_page_1(c):
    draw_engineering_frame(c, 1)
    draw_top_header(
        c, 1, 'A', 'THE HARDWARE',
        "A domestic refrigerator, taken apart",
        "An original 3D model of a household frost-free domestic refrigerator, exploded into its parts. Numbers on each drawing match the legend."
    )
    draw_bottom_title_block(c, "THE HARDWARE: REFRIGERATOR, TAKEN APART", 1)
    
    x0 = 18 * mm
    y_content_top = PAGE_H - 48 * mm
    
    # ---------------------------------------------------------------------
    # Card 1: FIG. 1A · ASSEMBLED (OPEN DOORS)
    # ---------------------------------------------------------------------
    fig1a_w = 185 * mm
    fig1a_h = 120 * mm
    fig1a_x = x0
    fig1a_y = y_content_top - fig1a_h
    draw_card_box(c, fig1a_x, fig1a_y, fig1a_w, fig1a_h, "FIG. 1A · ASSEMBLED (OPEN DOORS)")
    
    fig1a_img = os.path.join(RENDERS_DIR, 'fig1a_front_open.png')
    if os.path.exists(fig1a_img):
        c.drawImage(fig1a_img, fig1a_x + 4 * mm, fig1a_y + 3 * mm, width=fig1a_w - 8 * mm, height=fig1a_h - 10 * mm, preserveAspectRatio=True)
        
    # Fig 1A Callout pins with leader lines
    draw_callout_badge(c, fig1a_x + 22 * mm, fig1a_y + 88 * mm, 8, (fig1a_x + 55 * mm, fig1a_y + 95 * mm))   # Cabinet PUF
    draw_callout_badge(c, fig1a_x + 18 * mm, fig1a_y + 55 * mm, 10, (fig1a_x + 42 * mm, fig1a_y + 55 * mm))  # Fresh Food Door
    draw_callout_badge(c, fig1a_x + 72 * mm, fig1a_y + 108 * mm, 4, (fig1a_x + 105 * mm, fig1a_y + 98 * mm)) # Evaporator Unit
    draw_callout_badge(c, fig1a_x + 72 * mm, fig1a_y + 50 * mm, 9, (fig1a_x + 92 * mm, fig1a_y + 52 * mm))   # Shelves & Drawers
    draw_callout_badge(c, fig1a_x + 168 * mm, fig1a_y + 65 * mm, 11, (fig1a_x + 152 * mm, fig1a_y + 65 * mm)) # Freezer Door

    # ---------------------------------------------------------------------
    # Card 2: FIG. 1B · EXPLODED VIEW
    # ---------------------------------------------------------------------
    fig1b_w = 193 * mm
    fig1b_h = 120 * mm
    fig1b_x = fig1a_x + fig1a_w + 6 * mm
    fig1b_y = fig1a_y
    draw_card_box(c, fig1b_x, fig1b_y, fig1b_w, fig1b_h, "FIG. 1B · EXPLODED VIEW")
    
    fig1c_img = os.path.join(RENDERS_DIR, 'fig1c_exploded.png')
    if os.path.exists(fig1c_img):
        c.drawImage(fig1c_img, fig1b_x + 4 * mm, fig1b_y + 3 * mm, width=fig1b_w - 8 * mm, height=fig1b_h - 10 * mm, preserveAspectRatio=True)
        
    # Fig 1B Callout pins with leader lines
    draw_callout_badge(c, fig1b_x + 105 * mm, fig1b_y + 112 * mm, 4, (fig1b_x + 105 * mm, fig1b_y + 100 * mm)) # Evaporator
    draw_callout_badge(c, fig1b_x + 155 * mm, fig1b_y + 85 * mm, 2, (fig1b_x + 135 * mm, fig1b_y + 70 * mm))   # Condenser Coil
    draw_callout_badge(c, fig1b_x + 172 * mm, fig1b_y + 45 * mm, 12, (fig1b_x + 148 * mm, fig1b_y + 38 * mm))  # Ventilation Grille
    draw_callout_badge(c, fig1b_x + 148 * mm, fig1b_y + 22 * mm, 6, (fig1b_x + 142 * mm, fig1b_y + 26 * mm))   # Condenser Fan
    draw_callout_badge(c, fig1b_x + 120 * mm, fig1b_y + 42 * mm, 3, (fig1b_x + 118 * mm, fig1b_y + 35 * mm))   # Capillary Tube
    draw_callout_badge(c, fig1b_x + 106 * mm, fig1b_y + 12 * mm, 1, (fig1b_x + 106 * mm, fig1b_y + 20 * mm))   # Compressor
    draw_callout_badge(c, fig1b_x + 75 * mm, fig1b_y + 38 * mm, 7, (fig1b_x + 92 * mm, fig1b_y + 32 * mm))    # Refrigerant Lines
    draw_callout_badge(c, fig1b_x + 35 * mm, fig1b_y + 75 * mm, 10, (fig1b_x + 42 * mm, fig1b_y + 75 * mm))   # Door Assembly

    # ---------------------------------------------------------------------
    # Lower Section: Component Legend & Data Boxes
    # ---------------------------------------------------------------------
    leg_y_top = fig1a_y - 6 * mm
    leg_w = 230 * mm
    leg_h = 76 * mm
    draw_card_box(c, x0, leg_y_top - leg_h, leg_w, leg_h, "Component legend")
    
    legend_items = [
        (1, "Compressor", "Draws in low-pressure refrigerant vapour from evaporator and raises its pressure and temperature so it can reject heat in the condenser."),
        (2, "Condenser", "Rejects heat (Q_out) from the refrigerant to the surroundings and condenses high-pressure vapour into liquid."),
        (3, "Expansion Device", "Throttles high-pressure liquid, plunging its pressure and saturation temperature as it enters the evaporator."),
        (4, "Evaporator", "Absorbs heat (Q_in) from the food compartments, vaporising the low-pressure cold liquid refrigerant."),
        (5, "Receiver / Filter-Drier", "Adsorbs trace moisture (zeolite beads) and filters solid particulate debris before the capillary entrance."),
        (6, "Condenser Fan", "Forces ambient room air across the condenser coil and compressor casing to accelerate heat transfer."),
        (7, "Refrigerant Circuit Lines", "Hot-gas discharge line, liquid line, and insulated low-pressure suction vapour line."),
        (8, "PUF Insulation & Cabinet", "Cyclopentane-blown polyurethane foam insulation (k ≈ 0.02 W/m·K) preventing heat ingress."),
        (9, "Shelves & Crisper Drawers", "Tempered glass shelves and humidity-regulated vegetable crisper storage drawers."),
        (10, "Fresh Food Door Assembly", "Insulated cabinet door with magnetic bellows gasket seal and moulded door shelf bins."),
        (11, "Freezer Door Assembly", "Dedicated sub-zero compartment door mounted on dual-axis hinge pivots."),
        (12, "Rear Ventilation Grille", "Protective rear stamped grille channelising forced cooling air exhaust across the machinery bay.")
    ]
    
    col_w = (leg_w - 8 * mm) / 2
    for i, (num, name, desc) in enumerate(legend_items):
        cx = x0 + 4 * mm + (0 if i < 6 else col_w)
        cy = leg_y_top - 12 * mm - (i % 6) * 9.8 * mm
        
        # Number badge circle (white with black border)
        c.setFillColor(colors.white)
        c.setStrokeColor(colors.HexColor('#0f172a'))
        c.setLineWidth(0.8)
        c.circle(cx + 3 * mm, cy + 1.2 * mm, 2.8 * mm, fill=1, stroke=1)
        c.setFont("Helvetica-Bold", 6.8)
        c.setFillColor(colors.HexColor('#0f172a'))
        c.drawCentredString(cx + 3 * mm, cy + 0.3 * mm, str(num))
        
        c.setFont("Helvetica-Bold", 7.2)
        c.setFillColor(colors.HexColor('#0f172a'))
        c.drawString(cx + 7.5 * mm, cy + 1.8 * mm, name)
        
        c.setFont("Helvetica", 6.0)
        c.setFillColor(colors.HexColor('#475569'))
        c.drawString(cx + 7.5 * mm, cy - 1.5 * mm, desc[:72] + ("..." if len(desc) > 72 else ""))
        
    # Right Data Box: Model Data & Laboratory Rig Data
    data_x = x0 + leg_w + 6 * mm
    data_w = PAGE_W - 18 * mm - data_x
    data_h = leg_h
    draw_card_box(c, data_x, leg_y_top - data_h, data_w, data_h)
    
    # Model Data Section
    c.setFont("Helvetica-Bold", 8.5)
    c.setFillColor(colors.HexColor('#0f172a'))
    c.drawString(data_x + 4 * mm, leg_y_top - 6 * mm, "Model data")
    
    # verified teal pill
    c.setFillColor(colors.HexColor('#0d9488'))
    c.roundRect(data_x + 24 * mm, leg_y_top - 7.5 * mm, 14 * mm, 4.2 * mm, 1 * mm, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 5.5)
    c.setFillColor(colors.white)
    c.drawCentredString(data_x + 31 * mm, leg_y_top - 6.2 * mm, "verified")
    
    specs = [
        ("MODEL", "Original procedural GLB (glTF 2.0), generated by generate_refrigerator_model.py"),
        ("VALIDATION", "Khronos glTF-Validator: 0 errors, 0 warnings"),
        ("GEOMETRY", "165 named nodes · 151 meshes · 15 PBR materials"),
        ("FOOTPRINT", "1.00 m wide × 0.72 m deep × 1.80 m tall (generic domestic scale)")
    ]
    for idx, (lbl, val) in enumerate(specs):
        sy = leg_y_top - 12 * mm - idx * 4.2 * mm
        c.setFont("Helvetica-Bold", 6.2)
        c.setFillColor(colors.HexColor('#64748b'))
        c.drawString(data_x + 4 * mm, sy, lbl)
        
        # Dotted leader line
        c.setStrokeColor(colors.HexColor('#cbd5e1'))
        c.setLineWidth(0.5)
        c.setDash([1, 2], 0)
        c.line(data_x + 22 * mm, sy + 1 * mm, data_x + 35 * mm, sy + 1 * mm)
        c.setDash([], 0)
        
        c.setFont("Helvetica", 6.2)
        c.setFillColor(colors.HexColor('#0f172a'))
        c.drawString(data_x + 37 * mm, sy, val)
        
    # Rig Data Section
    np_y = leg_y_top - 34 * mm
    c.setFont("Helvetica-Bold", 8.5)
    c.setFillColor(colors.HexColor('#0f172a'))
    c.drawString(data_x + 4 * mm, np_y, "Typical domestic nameplate specifications")
    
    # to be filled red pill
    c.setFillColor(colors.HexColor('#c2410c'))
    c.roundRect(data_x + 72 * mm, np_y - 1.5 * mm, 17 * mm, 4.2 * mm, 1 * mm, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 5.5)
    c.setFillColor(colors.white)
    c.drawCentredString(data_x + 80.5 * mm, np_y - 0.2 * mm, "representative")
    
    np_specs = [
        ("REFRIGERANT", "R134a / R600a (Isobutane, GWP=3, ODP=0)"),
        ("COMPRESSOR", "1/6 to 1/4 HP Hermetic Reciprocating (~120W to 180W input)"),
        ("CONDENSING P", "8.0 to 12.5 bar (~35°C to 45°C saturation temp)"),
        ("EVAPORATING P", "1.1 to 1.4 bar (~ -20°C to -15°C saturation temp)"),
        ("ESTIMATED COP", "1.8 to 2.4 (Typical household operating range)")
    ]
    for idx, (lbl, val) in enumerate(np_specs):
        sy = np_y - 6 * mm - idx * 4.2 * mm
        c.setFont("Helvetica-Bold", 6.2)
        c.setFillColor(colors.HexColor('#64748b'))
        c.drawString(data_x + 4 * mm, sy, lbl)
        
        # Dotted leader line
        c.setStrokeColor(colors.HexColor('#cbd5e1'))
        c.setLineWidth(0.5)
        c.setDash([1, 2], 0)
        c.line(data_x + 25 * mm, sy + 1 * mm, data_x + 38 * mm, sy + 1 * mm)
        c.setDash([], 0)
        
        c.setFont("Helvetica", 6.2)
        c.setFillColor(colors.HexColor('#0f172a'))
        c.drawString(data_x + 40 * mm, sy, val)
        
    c.showPage()

# =========================================================================
# PAGE 2: THE REFRIGERATION CYCLE
# =========================================================================
def build_page_2(c):
    draw_engineering_frame(c, 2)
    draw_top_header(
        c, 2, 'B', 'THE REFRIGERATION CYCLE',
        "One loop, two pressures",
        "How refrigerant carries heat out of a cold space: it boils at low pressure in the evaporator and condenses at high pressure in the condenser."
    )
    draw_bottom_title_block(c, "THE REFRIGERATION CYCLE: THERMODYNAMIC PRINCIPLE", 2)
    
    x0 = 18 * mm
    y_content_top = PAGE_H - 48 * mm
    
    # ---------------------------------------------------------------------
    # Top Row: Fig 2A (Schematic), Fig 2B (p-h Diagram), Side Summary Card
    # ---------------------------------------------------------------------
    top_row_h = 112 * mm
    top_row_y = y_content_top - top_row_h
    
    # Fig 2A: Cycle Schematic Card
    fig2a_w = 152 * mm
    draw_card_box(c, x0, top_row_y, fig2a_w, top_row_h, "FIG. 2A · CYCLE SCHEMATIC")
    fig2a_img = os.path.join(RENDERS_DIR, 'fig2a_cycle_schematic.png')
    if os.path.exists(fig2a_img):
        c.drawImage(fig2a_img, x0 + 4 * mm, top_row_y + 4 * mm, width=fig2a_w - 8 * mm, height=top_row_h - 12 * mm, preserveAspectRatio=True)
        
    # Fig 2B: p-h Diagram Card
    fig2b_w = 132 * mm
    fig2b_x = x0 + fig2a_w + 6 * mm
    draw_card_box(c, fig2b_x, top_row_y, fig2b_w, top_row_h, "FIG. 2B · p–h SKETCH (SCHEMATIC)")
    fig2b_img = os.path.join(RENDERS_DIR, 'fig2b_ph_diagram.png')
    if os.path.exists(fig2b_img):
        c.drawImage(fig2b_img, fig2b_x + 4 * mm, top_row_y + 4 * mm, width=fig2b_w - 8 * mm, height=top_row_h - 12 * mm, preserveAspectRatio=True)
        
    # Side Card: High & Low Pressure Summary & Fig 2C 3D Flow Trace
    side_w = PAGE_W - 18 * mm - (fig2b_x + fig2b_w + 6 * mm)
    side_x = fig2b_x + fig2b_w + 6 * mm
    draw_card_box(c, side_x, top_row_y, side_w, top_row_h)
    
    # High-pressure side
    c.setFillColor(colors.HexColor('#dc2626'))
    c.rect(side_x + 4 * mm, top_row_y + top_row_h - 8 * mm, 3 * mm, 3 * mm, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(colors.HexColor('#0f172a'))
    c.drawString(side_x + 9 * mm, top_row_y + top_row_h - 7.5 * mm, "High-pressure side")
    c.setFont("Helvetica", 6.2)
    c.setFillColor(colors.HexColor('#475569'))
    c.drawString(side_x + 4 * mm, top_row_y + top_row_h - 12 * mm, "Compressor outlet → condenser → filter-drier →")
    c.drawString(side_x + 4 * mm, top_row_y + top_row_h - 15.5 * mm, "capillary inlet. Refrigerant rejects heat (Q_out) here.")
    
    # Low-pressure side
    c.setFillColor(colors.HexColor('#0284c7'))
    c.rect(side_x + 4 * mm, top_row_y + top_row_h - 22 * mm, 3 * mm, 3 * mm, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(colors.HexColor('#0f172a'))
    c.drawString(side_x + 9 * mm, top_row_y + top_row_h - 21.5 * mm, "Low-pressure side")
    c.setFont("Helvetica", 6.2)
    c.setFillColor(colors.HexColor('#475569'))
    c.drawString(side_x + 4 * mm, top_row_y + top_row_h - 26 * mm, "Capillary outlet → evaporator → suction line →")
    c.drawString(side_x + 4 * mm, top_row_y + top_row_h - 29.5 * mm, "compressor inlet. Refrigerant absorbs heat (Q_in).")
    
    # Energy Balance Equation
    c.setFont("Helvetica-Bold", 6.8)
    c.setFillColor(colors.HexColor('#0f172a'))
    c.drawString(side_x + 4 * mm, top_row_y + top_row_h - 36 * mm, "Energy balance (steady state):")
    c.setFont("Helvetica-Bold", 7.0)
    c.setFillColor(colors.HexColor('#ea580c'))
    c.drawString(side_x + 4 * mm, top_row_y + top_row_h - 41 * mm, "Q_out = Q_in + W_in")
    c.drawString(side_x + 4 * mm, top_row_y + top_row_h - 45.5 * mm, "COP = Q_in / W_in")
    
    # Mini Fig 2C: Flow Trace in 3D Model
    fig2c_card_h = 56 * mm
    c.setStrokeColor(colors.HexColor('#cbd5e1'))
    c.line(side_x, top_row_y + fig2c_card_h + 4 * mm, side_x + side_w, top_row_y + fig2c_card_h + 4 * mm)
    c.setFont("Helvetica-Bold", 6.5)
    c.setFillColor(colors.HexColor('#475569'))
    c.drawString(side_x + 4 * mm, top_row_y + fig2c_card_h + 1 * mm, "FIG. 2C · FLOW TRACE IN 3D MODEL")
    
    fig2c_img = os.path.join(RENDERS_DIR, 'fig2c_flow_trace.png')
    if os.path.exists(fig2c_img):
        c.drawImage(fig2c_img, side_x + 4 * mm, top_row_y + 2 * mm, width=side_w - 8 * mm, height=fig2c_card_h - 4 * mm, preserveAspectRatio=True)

    # ---------------------------------------------------------------------
    # Bottom Row: 4 Process Cards (1 Evaporation, 2 Compression, 3 Condensation, 4 Expansion)
    # ---------------------------------------------------------------------
    bot_y_top = top_row_y - 6 * mm
    bot_h = 82 * mm
    card_w = (PAGE_W - 36 * mm - 18 * mm) / 4 # 4 equal cards with 6mm gutters
    
    processes = [
        (1, "Evaporation (heat absorbed)", 
         "Cold, low-pressure liquid-vapour mixture enters the evaporator coil.",
         "It absorbs heat from food compartments, boiling into low-pressure vapour.",
         "Ideal: Constant-pressure heat addition until refrigerant is saturated vapour.",
         "Real: Slight frictional pressure drop across coil; vapour is superheated 3-5 K at outlet to protect compressor."),
         
        (2, "Compression (work input)", 
         "Compressor draws in low-pressure vapour and squeezes it into hot gas.",
         "Driven by electric motor work input. Pressure and saturation temperature rise above room ambient.",
         "Ideal: Reversible isentropic (adiabatic) compression (s1 = s2).",
         "Real: Valve losses, motor winding heat, and piston friction make compression non-isentropic (s2 > s1)."),
         
        (3, "Condensation (heat rejected)", 
         "Hot, high-pressure vapour discharges into the rear condenser coil.",
         "Rejects heat (Q_out = Q_in + W_in) to room air. Refrigerant desuperheats, condenses, and subcools.",
         "Ideal: Constant-pressure heat rejection to saturated liquid state.",
         "Real: Slight subcooling (3-8 K) occurs at coil exit, ensuring 100% liquid enters capillary tube."),
         
        (4, "Expansion (throttling)", 
         "High-pressure liquid is forced through the narrow capillary tube.",
         "High hydraulic resistance causes pressure to drop abruptly. A fraction flashes to vapour, chilling the stream.",
         "Ideal: Irreversible throttling at constant enthalpy (h3 = h4, zero work).",
         "Real: Adiabatic flow with critical choking; soldered to suction line to form internal heat exchanger.")
    ]
    
    for idx, (num, title, p1, p2, ideal, real) in enumerate(processes):
        bx = x0 + idx * (card_w + 6 * mm)
        by = bot_y_top - bot_h
        draw_card_box(c, bx, by, card_w, bot_h)
        
        # Number badge (white with black border)
        c.setFillColor(colors.HexColor('#0f172a'))
        c.circle(bx + 7 * mm, by + bot_h - 7 * mm, 3.5 * mm, fill=1, stroke=0)
        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(colors.white)
        c.drawCentredString(bx + 7 * mm, by + bot_h - 8.2 * mm, str(num))
        
        c.setFont("Helvetica-Bold", 7.8)
        c.setFillColor(colors.HexColor('#0f172a'))
        c.drawString(bx + 13 * mm, by + bot_h - 7.5 * mm, title)
        
        # Paragraphs
        c.setFont("Helvetica", 6.5)
        c.setFillColor(colors.HexColor('#334155'))
        c.drawString(bx + 4 * mm, by + bot_h - 15 * mm, p1[:58] + ("..." if len(p1) > 58 else ""))
        c.drawString(bx + 4 * mm, by + bot_h - 19 * mm, p2[:58] + ("..." if len(p2) > 58 else ""))
        
        # Ideal Cycle
        c.setFont("Helvetica-Bold", 6.5)
        c.setFillColor(colors.HexColor('#0f172a'))
        c.drawString(bx + 4 * mm, by + bot_h - 26 * mm, "Ideal cycle:")
        c.setFont("Helvetica", 6.2)
        c.setFillColor(colors.HexColor('#475569'))
        c.drawString(bx + 4 * mm, by + bot_h - 30 * mm, ideal[:60] + ("..." if len(ideal) > 60 else ""))
        
        # Real System
        c.setFont("Helvetica-Bold", 6.5)
        c.setFillColor(colors.HexColor('#dc2626'))
        c.drawString(bx + 4 * mm, by + bot_h - 38 * mm, "Real system:")
        c.setFont("Helvetica", 6.2)
        c.setFillColor(colors.HexColor('#475569'))
        c.drawString(bx + 4 * mm, by + bot_h - 42 * mm, real[:60] + ("..." if len(real) > 60 else ""))
        
    c.showPage()

# =========================================================================
# PAGE 3: THE PROJECT (ARCHITECTURE & APP VIEWS)
# =========================================================================
def build_page_3(c):
    draw_engineering_frame(c, 3)
    draw_top_header(
        c, 3, 'C', 'THE PROJECT',
        "One model, three ways in",
        "Objective, architecture and implementation of the Domestic Refrigerator AR Explorer: one procedural model, three ways to learn from it."
    )
    draw_bottom_title_block(c, "THE PROJECT: HOW IT IS BUILT", 3)
    
    x0 = 18 * mm
    y_content_top = PAGE_H - 48 * mm
    
    # ---------------------------------------------------------------------
    # Top Row: 4 Cards (C1 Motivation, C2 Architecture, C3 How it works, C4 Limitations)
    # ---------------------------------------------------------------------
    top_h = 100 * mm
    top_y = y_content_top - top_h
    col_w = (PAGE_W - 36 * mm - 18 * mm) / 4
    
    # Card C1: Objective & motivation
    c1_x = x0
    draw_card_box(c, c1_x, top_y, col_w, top_h)
    
    # Pill tag
    c.setFillColor(colors.HexColor('#0f172a'))
    c.roundRect(c1_x + 4 * mm, top_y + top_h - 8 * mm, 6 * mm, 5 * mm, 1 * mm, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 6.8)
    c.setFillColor(colors.white)
    c.drawCentredString(c1_x + 7 * mm, top_y + top_h - 6.5 * mm, "C1")
    c.setFont("Helvetica-Bold", 8.5)
    c.setFillColor(colors.HexColor('#0f172a'))
    c.drawString(c1_x + 12 * mm, top_y + top_h - 6.8 * mm, "Objective & motivation")
    
    c1_text = (
        "Students learn the vapour compression cycle as a theoretical four-stage schematic, "
        "but a domestic refrigerator is a complex machine with hidden coils, capillary lines, "
        "and foamed insulation.\n\n"
        "This project bridges the gap: every component can be tapped to inspect its thermodynamic function, "
        "the door opens smoothly on dual hinge pivots, and the life-size refrigerator can be placed in AR on "
        "a real floor or table — with zero app installation.\n\n"
        "• Identify the 4 core cycle components in 3D.\n"
        "• Trace high-pressure and low-pressure sides.\n"
        "• Walk around the virtual appliance in life-size AR.\n"
        "• Relate physical layout to the p–h diagram."
    )
    c.setFont("Helvetica", 6.5)
    c.setFillColor(colors.HexColor('#334155'))
    ty = top_y + top_h - 16 * mm
    for line in c1_text.split('\n'):
        if line == '':
            ty -= 2.5 * mm
        else:
            c.drawString(c1_x + 4 * mm, ty, line)
            ty -= 3.8 * mm
            
    # Card C2: Implementation architecture
    c2_x = c1_x + col_w + 6 * mm
    draw_card_box(c, c2_x, top_y, col_w, top_h)
    
    c.setFillColor(colors.HexColor('#0f172a'))
    c.roundRect(c2_x + 4 * mm, top_y + top_h - 8 * mm, 6 * mm, 5 * mm, 1 * mm, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 6.8)
    c.setFillColor(colors.white)
    c.drawCentredString(c2_x + 7 * mm, top_y + top_h - 6.5 * mm, "C2")
    c.setFont("Helvetica-Bold", 8.5)
    c.setFillColor(colors.HexColor('#0f172a'))
    c.drawString(c2_x + 12 * mm, top_y + top_h - 6.8 * mm, "Implementation architecture")
    
    # Architecture Flowchart Blocks
    flow_y = top_y + top_h - 22 * mm
    # 1. Blender Generator Box
    c.setFillColor(colors.HexColor('#070d1e'))
    c.roundRect(c2_x + 6 * mm, flow_y, col_w - 12 * mm, 10 * mm, 2 * mm, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 6.5)
    c.setFillColor(colors.HexColor('#00e5ff'))
    c.drawCentredString(c2_x + col_w / 2, flow_y + 4 * mm, "generate_refrigerator_model.py (Blender)")
    c.setFont("Helvetica", 5.5)
    c.setFillColor(colors.HexColor('#94a3b8'))
    c.drawCentredString(c2_x + col_w / 2, flow_y + 1.5 * mm, "Python procedural geometry & dual pivots")
    
    # Arrow
    c.setStrokeColor(colors.HexColor('#0f172a'))
    c.line(c2_x + col_w / 2, flow_y, c2_x + col_w / 2, flow_y - 4 * mm)
    
    # 2. glTF 2.0 Asset Box
    flow_y -= 14 * mm
    c.setFillColor(colors.HexColor('#ea580c'))
    c.roundRect(c2_x + 10 * mm, flow_y, col_w - 20 * mm, 9 * mm, 2 * mm, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 6.8)
    c.setFillColor(colors.white)
    c.drawCentredString(c2_x + col_w / 2, flow_y + 4 * mm, "Domestic_Refrigerator.glb")
    c.setFont("Helvetica", 5.5)
    c.drawCentredString(c2_x + col_w / 2, flow_y + 1.5 * mm, "Khronos Validated glTF 2.0 Asset")
    
    # 3 Branches: Website, WebAR, Unity
    flow_y -= 16 * mm
    c.setFillColor(colors.white)
    c.setStrokeColor(colors.HexColor('#1e2e5c'))
    c.setLineWidth(0.8)
    # Web Explorer box
    c.roundRect(c2_x + 4 * mm, flow_y, (col_w - 12 * mm) / 2, 11 * mm, 1 * mm, fill=1, stroke=1)
    c.setFont("Helvetica-Bold", 6.2)
    c.setFillColor(colors.HexColor('#0f172a'))
    c.drawCentredString(c2_x + 4 * mm + (col_w - 12 * mm) / 4, flow_y + 6 * mm, "Web Explorer")
    c.setFont("Helvetica", 5.5)
    c.setFillColor(colors.HexColor('#64748b'))
    c.drawCentredString(c2_x + 4 * mm + (col_w - 12 * mm) / 4, flow_y + 2.5 * mm, "React 19 · Three.js")
    
    # WebAR Box
    c.roundRect(c2_x + 6 * mm + (col_w - 12 * mm) / 2, flow_y, (col_w - 12 * mm) / 2, 11 * mm, 1 * mm, fill=1, stroke=1)
    c.setFont("Helvetica-Bold", 6.2)
    c.setFillColor(colors.HexColor('#0f172a'))
    c.drawCentredString(c2_x + 6 * mm + 3 * (col_w - 12 * mm) / 4, flow_y + 6 * mm, "WebAR Engine")
    c.setFont("Helvetica", 5.5)
    c.setFillColor(colors.HexColor('#64748b'))
    c.drawCentredString(c2_x + 6 * mm + 3 * (col_w - 12 * mm) / 4, flow_y + 2.5 * mm, "SceneViewer / QuickLook")
    
    # Bottom sync text
    c.setFont("Helvetica", 6.0)
    c.setFillColor(colors.HexColor('#64748b'))
    c.drawString(c2_x + 4 * mm, top_y + 8 * mm, "Single shared JSON dataset drives website,")
    c.drawString(c2_x + 4 * mm, top_y + 4.5 * mm, "Unity app, and poster for 100% data agreement.")
    
    # Card C3: How it works
    c3_x = c2_x + col_w + 6 * mm
    draw_card_box(c, c3_x, top_y, col_w, top_h)
    
    c.setFillColor(colors.HexColor('#0f172a'))
    c.roundRect(c3_x + 4 * mm, top_y + top_h - 8 * mm, 6 * mm, 5 * mm, 1 * mm, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 6.8)
    c.setFillColor(colors.white)
    c.drawCentredString(c3_x + 7 * mm, top_y + top_h - 6.5 * mm, "C3")
    c.setFont("Helvetica-Bold", 8.5)
    c.setFillColor(colors.HexColor('#0f172a'))
    c.drawString(c3_x + 12 * mm, top_y + top_h - 6.8 * mm, "How it works")
    
    c3_items = [
        ("3D MODEL", "Procedural geometry (compressor shell, swept copper tubing, serpentine condenser, evaporator fins) with dual animated door hinges exported to glTF 2.0."),
        ("WEB EXPLORER", "Interactive tap/click raycast picking, single-part highlight, ghosted isolate mode, explode slider, cycle flow pulse animation, and full component library modal."),
        ("AUGMENTED REALITY", "Zero-install WebAR: WebXR & Scene Viewer on ARCore Android; AR Quick Look on iOS. Live camera overlay fallback on desktops & laptops."),
        ("UNITY 6 PROJECT", "URP scenes: MainMenu, RefrigeratorExplorer, and AR Foundation scene for optional native builds.")
    ]
    ty = top_y + top_h - 16 * mm
    for header, desc in c3_items:
        c.setFont("Helvetica-Bold", 6.5)
        c.setFillColor(colors.HexColor('#0f172a'))
        c.drawString(c3_x + 4 * mm, ty, header)
        ty -= 3.5 * mm
        c.setFont("Helvetica", 6.2)
        c.setFillColor(colors.HexColor('#475569'))
        c.drawString(c3_x + 4 * mm, ty, desc[:62] + ("..." if len(desc) > 62 else ""))
        ty -= 3.5 * mm
        c.drawString(c3_x + 4 * mm, ty, desc[62:124] + ("..." if len(desc) > 124 else ""))
        ty -= 5.0 * mm

    # Card C4: Applications & limitations
    c4_x = c3_x + col_w + 6 * mm
    draw_card_box(c, c4_x, top_y, col_w, top_h)
    
    c.setFillColor(colors.HexColor('#0f172a'))
    c.roundRect(c4_x + 4 * mm, top_y + top_h - 8 * mm, 6 * mm, 5 * mm, 1 * mm, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 6.8)
    c.setFillColor(colors.white)
    c.drawCentredString(c4_x + 7 * mm, top_y + top_h - 6.5 * mm, "C4")
    c.setFont("Helvetica-Bold", 8.5)
    c.setFillColor(colors.HexColor('#0f172a'))
    c.drawString(c4_x + 12 * mm, top_y + top_h - 6.8 * mm, "Applications & limitations")
    
    c4_text = (
        "USE IT FOR\n"
        "• Pre-lab briefing before thermal lab experiments\n"
        "• Self-study, revision, and 3D exploration on phones\n"
        "• Visualizing concealed internal cooling components\n"
        "• Explaining refrigeration to non-specialists\n\n"
        "KEEP IN MIND\n"
        "• Educational visualization — not manufacturing CAD\n"
        "• Illustrative generic domestic proportions\n"
        "• Flow animation is conceptual, not CFD simulation\n"
        "• No proprietary brand specifications invented\n"
        "• AR tracking relies on device ARCore / ARKit"
    )
    ty = top_y + top_h - 16 * mm
    for line in c4_text.split('\n'):
        if line.startswith('USE IT FOR') or line.startswith('KEEP IN MIND'):
            c.setFont("Helvetica-Bold", 6.8)
            c.setFillColor(colors.HexColor('#0284c7') if 'USE' in line else colors.HexColor('#ea580c'))
            c.drawString(c4_x + 4 * mm, ty, line)
            ty -= 3.8 * mm
        elif line == '':
            ty -= 2.0 * mm
        else:
            c.setFont("Helvetica", 6.2)
            c.setFillColor(colors.HexColor('#334155'))
            c.drawString(c4_x + 4 * mm, ty, line)
            ty -= 3.8 * mm

    # ---------------------------------------------------------------------
    # Bottom Row: 4 Application Screenshot Cards
    # ---------------------------------------------------------------------
    bot_h = 94 * mm
    bot_y = top_y - 6 * mm - bot_h
    
    # Fig 3A: Web Explorer (Desktop)
    draw_card_box(c, c1_x, bot_y, col_w, bot_h, "FIG. 3A · WEB EXPLORER (DESKTOP)")
    fig3a_img = os.path.join(RENDERS_DIR, 'fig3a_web_explorer.png')
    if os.path.exists(fig3a_img):
        c.drawImage(fig3a_img, c1_x + 4 * mm, bot_y + 4 * mm, width=col_w - 8 * mm, height=bot_h - 12 * mm, preserveAspectRatio=True)
        
    # Fig 3C: AR Page
    draw_card_box(c, c2_x, bot_y, col_w, bot_h, "FIG. 3C · AR PAGE")
    fig3c_img = os.path.join(RENDERS_DIR, 'fig3c_ar_page.png')
    if os.path.exists(fig3c_img):
        c.drawImage(fig3c_img, c2_x + 4 * mm, bot_y + 4 * mm, width=col_w - 8 * mm, height=bot_h - 12 * mm, preserveAspectRatio=True)
        
    # Fig 3B: Phone View
    draw_card_box(c, c3_x, bot_y, col_w, bot_h, "FIG. 3B · PHONE VIEW")
    fig3b_img = os.path.join(RENDERS_DIR, 'fig3b_phone_view.png')
    if os.path.exists(fig3b_img):
        c.drawImage(fig3b_img, c3_x + 4 * mm, bot_y + 4 * mm, width=col_w - 8 * mm, height=bot_h - 12 * mm, preserveAspectRatio=True)
        
    # Fig 3D: 3D Cycle Mode
    draw_card_box(c, c4_x, bot_y, col_w, bot_h, "FIG. 3D · 3D CYCLE MODE")
    fig3d_img = os.path.join(RENDERS_DIR, 'fig3d_cycle_mode.png')
    if os.path.exists(fig3d_img):
        c.drawImage(fig3d_img, c4_x + 4 * mm, bot_y + 4 * mm, width=col_w - 8 * mm, height=bot_h - 12 * mm, preserveAspectRatio=True)
        
    c.showPage()

# =========================================================================
# PAGE 4: SCAN · EXPLORE (QR CODES & PROJECT METADATA)
# =========================================================================
def build_page_4(c):
    draw_engineering_frame(c, 4)
    draw_top_header(
        c, 4, 'D', 'ACCESS',
        "Scan · Explore",
        "Two codes, two ways in. Open your phone camera and point it at either code. Nothing to install."
    )
    draw_bottom_title_block(c, "SCAN · EXPLORE: ACCESS & CREDITS", 4)
    
    x0 = 18 * mm
    y_content_top = PAGE_H - 48 * mm
    
    # ---------------------------------------------------------------------
    # Top Row: Two Large QR Cards (AR on Left, Web Explorer on Right)
    # ---------------------------------------------------------------------
    qr_card_w = 188 * mm
    qr_card_h = 125 * mm
    qr_card_y = y_content_top - qr_card_h
    
    # Card 1: AUGMENTED REALITY
    draw_card_box(c, x0, qr_card_y, qr_card_w, qr_card_h)
    
    # Red Banner Pill
    c.setFillColor(colors.HexColor('#dc2626'))
    c.rect(x0, qr_card_y + qr_card_h - 6 * mm, 45 * mm, 6 * mm, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 6.8)
    c.setFillColor(colors.white)
    c.drawString(x0 + 4 * mm, qr_card_y + qr_card_h - 4.2 * mm, "AUGMENTED REALITY")
    
    # Big AR QR Code
    qr_ar_img = os.path.join(RENDERS_DIR, 'qr_ar_view.png')
    big_qr_size = 62 * mm
    big_qr_x = x0 + 10 * mm
    big_qr_y = qr_card_y + 24 * mm
    if os.path.exists(qr_ar_img):
        c.drawImage(qr_ar_img, big_qr_x, big_qr_y, width=big_qr_size, height=big_qr_size)
        
    # AR Text Content
    ar_tx = big_qr_x + big_qr_size + 10 * mm
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(colors.HexColor('#dc2626'))
    c.drawString(ar_tx, qr_card_y + qr_card_h - 18 * mm, "CODE 1 · AR")
    
    c.setFont("Helvetica-Bold", 17)
    c.setFillColor(colors.HexColor('#070d1e'))
    c.drawString(ar_tx, qr_card_y + qr_card_h - 26 * mm, "The fridge, in")
    c.drawString(ar_tx, qr_card_y + qr_card_h - 33 * mm, "your room")
    
    c.setFont("Helvetica", 7.5)
    c.setFillColor(colors.HexColor('#334155'))
    c.drawString(ar_tx, qr_card_y + qr_card_h - 40 * mm, "Place the refrigerator on a real floor or table")
    c.drawString(ar_tx, qr_card_y + qr_card_h - 44.5 * mm, "at life size, open the doors, and walk around it.")
    
    # Step instructions
    steps_ar = [
        ("01", "Scan, then tap View in your space."),
        ("02", "Move the phone slowly over a floor or table."),
        ("03", "Walk around it; tap Open Doors to see inside.")
    ]
    for idx, (badge, text) in enumerate(steps_ar):
        sy = qr_card_y + qr_card_h - 54 * mm - idx * 7.5 * mm
        c.setStrokeColor(colors.HexColor('#dc2626'))
        c.setLineWidth(0.8)
        c.roundRect(ar_tx, sy, 7 * mm, 5 * mm, 1 * mm, fill=0, stroke=1)
        c.setFont("Helvetica-Bold", 6.5)
        c.setFillColor(colors.HexColor('#dc2626'))
        c.drawCentredString(ar_tx + 3.5 * mm, sy + 1.2 * mm, badge)
        
        c.setFont("Helvetica", 7.0)
        c.setFillColor(colors.HexColor('#0f172a'))
        c.drawString(ar_tx + 10 * mm, sy + 1.2 * mm, text)
        
    # Direct AR URL
    c.setFont("Helvetica-Bold", 6.2)
    c.setFillColor(colors.HexColor('#64748b'))
    c.drawString(big_qr_x, qr_card_y + 12 * mm, "OR TYPE URL:")
    c.setFont("Helvetica-Bold", 7.0)
    c.setFillColor(colors.HexColor('#070d1e'))
    c.drawString(big_qr_x, qr_card_y + 7 * mm, "https://sahilpanchavishe.github.io/Domestic-Refrigerator-AR-Explorer/#ar")

    # Card 2: WEB EXPLORER
    card2_x = x0 + qr_card_w + 8 * mm
    card2_w = PAGE_W - 18 * mm - card2_x
    draw_card_box(c, card2_x, qr_card_y, card2_w, qr_card_h)
    
    # Blue Banner Pill
    c.setFillColor(colors.HexColor('#0284c7'))
    c.rect(card2_x, qr_card_y + qr_card_h - 6 * mm, 38 * mm, 6 * mm, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 6.8)
    c.setFillColor(colors.white)
    c.drawString(card2_x + 4 * mm, qr_card_y + qr_card_h - 4.2 * mm, "WEB EXPLORER")
    
    # Big Web QR Code
    qr_web_img = os.path.join(RENDERS_DIR, 'qr_web_explorer.png')
    big_web_x = card2_x + 10 * mm
    if os.path.exists(qr_web_img):
        c.drawImage(qr_web_img, big_web_x, big_qr_y, width=big_qr_size, height=big_qr_size)
        
    # Web Text Content
    web_tx = big_web_x + big_qr_size + 10 * mm
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(colors.HexColor('#0284c7'))
    c.drawString(web_tx, qr_card_y + qr_card_h - 18 * mm, "CODE 2 · WEB")
    
    c.setFont("Helvetica-Bold", 17)
    c.setFillColor(colors.HexColor('#070d1e'))
    c.drawString(web_tx, qr_card_y + qr_card_h - 26 * mm, "The whole")
    c.drawString(web_tx, qr_card_y + qr_card_h - 33 * mm, "appliance, interactive")
    
    c.setFont("Helvetica", 7.5)
    c.setFillColor(colors.HexColor('#334155'))
    c.drawString(web_tx, qr_card_y + qr_card_h - 40 * mm, "Rotate the refrigerator in 3D, tap any of the")
    c.drawString(web_tx, qr_card_y + qr_card_h - 44.5 * mm, "13 parts, open doors, and read the specifications.")
    
    steps_web = [
        ("01", "Scan to open the 3D explorer in browser."),
        ("02", "Tap compressor, condenser, valve or coils."),
        ("03", "Toggle Open Doors or drag Explode slider.")
    ]
    for idx, (badge, text) in enumerate(steps_web):
        sy = qr_card_y + qr_card_h - 54 * mm - idx * 7.5 * mm
        c.setStrokeColor(colors.HexColor('#0284c7'))
        c.setLineWidth(0.8)
        c.roundRect(web_tx, sy, 7 * mm, 5 * mm, 1 * mm, fill=0, stroke=1)
        c.setFont("Helvetica-Bold", 6.5)
        c.setFillColor(colors.HexColor('#0284c7'))
        c.drawCentredString(web_tx + 3.5 * mm, sy + 1.2 * mm, badge)
        
        c.setFont("Helvetica", 7.0)
        c.setFillColor(colors.HexColor('#0f172a'))
        c.drawString(web_tx + 10 * mm, sy + 1.2 * mm, text)
        
    c.setFont("Helvetica-Bold", 6.2)
    c.setFillColor(colors.HexColor('#64748b'))
    c.drawString(big_web_x, qr_card_y + 12 * mm, "OR TYPE URL:")
    c.setFont("Helvetica-Bold", 7.0)
    c.setFillColor(colors.HexColor('#070d1e'))
    c.drawString(big_web_x, qr_card_y + 7 * mm, "https://sahilpanchavishe.github.io/Domestic-Refrigerator-AR-Explorer/")

    # ---------------------------------------------------------------------
    # Lower Section: Project Details (Left) & References & Credits (Right)
    # ---------------------------------------------------------------------
    bot_y_top = qr_card_y - 6 * mm
    bot_h = 70 * mm
    bot_y = bot_y_top - bot_h
    
    # Project Details Card
    draw_card_box(c, x0, bot_y, qr_card_w, bot_h, "Project")
    
    proj_rows = [
        ("TITLE", "Domestic Refrigerator AR Explorer — Interactive 3D & AR"),
        ("TEAM", "Sahil Panchavishe · 612302040\nMegh Shidam · 612302058"),
        ("BRANCH", "Robotics & AI (B.Tech)"),
        ("GUIDE", "Dr. Shubhangi Deshmukh"),
        ("INSTITUTION", "Department of Robotics & AI, COEP Technological University, Pune")
    ]
    py = bot_y + bot_h - 14 * mm
    for lbl, val in proj_rows:
        c.setFont("Helvetica-Bold", 6.8)
        c.setFillColor(colors.HexColor('#64748b'))
        c.drawString(x0 + 4 * mm, py, lbl)
        
        c.setStrokeColor(colors.HexColor('#cbd5e1'))
        c.setLineWidth(0.5)
        c.setDash([1, 2], 0)
        c.line(x0 + 24 * mm, py + 1 * mm, x0 + 36 * mm, py + 1 * mm)
        c.setDash([], 0)
        
        c.setFont("Helvetica-Bold" if lbl == "TEAM" else "Helvetica", 6.8)
        c.setFillColor(colors.HexColor('#0f172a'))
        if '\n' in val:
            v1, v2 = val.split('\n')
            c.drawString(x0 + 38 * mm, py + 1.5 * mm, v1)
            c.drawString(x0 + 38 * mm, py - 2.5 * mm, v2)
            py -= 8.5 * mm
        else:
            c.drawString(x0 + 38 * mm, py, val)
            py -= 7.0 * mm

    # References & Credits Card
    draw_card_box(c, card2_x, bot_y, card2_w, bot_h, "References & credits")
    
    refs = [
        "• C. P. Arora, Refrigeration and Air Conditioning, 3rd ed., McGraw-Hill, 2008.",
        "• W. F. Stoecker & J. W. Jones, Refrigeration and Air Conditioning, McGraw-Hill.",
        "• Y. A. Çengel & M. A. Boles, Thermodynamics: An Engineering Approach, McGraw-Hill.",
        "• ASHRAE Handbook — Refrigeration (Systems and Equipment), ASHRAE, 2022.",
        "• Software: three.js, Google <model-viewer>, React 19, Vite 6, TypeScript, ReportLab.",
        "• Unity: Unity 6 (URP, glTFast, AR Foundation, ARCore XR Plugin).",
        "• 3D Model: Original procedural educational visualization created via Blender 5.2 Python API.",
        "• Validation: Khronos Group glTF-Validator 2.0 (0 errors, 0 warnings)."
    ]
    ry = bot_y + bot_h - 13 * mm
    c.setFont("Helvetica", 6.2)
    c.setFillColor(colors.HexColor('#334155'))
    for ref in refs:
        c.drawString(card2_x + 4 * mm, ry, ref)
        ry -= 4.4 * mm
        
    c.showPage()

def main():
    print(f"Generating 4-page A3 landscape PDF: {PDF_PATH}")
    c = canvas.Canvas(PDF_PATH, pagesize=landscape(A3))
    
    build_page_1(c)
    build_page_2(c)
    build_page_3(c)
    build_page_4(c)
    
    c.save()
    print("SUCCESS: 4-Page A3 Landscape Technical Poster generated successfully!")

if __name__ == '__main__':
    main()
