"""
Four-Page A3 Landscape Technical Poster Generator for Domestic Refrigerator AR Explorer
Strictly adheres to the architectural structure and presentation quality of VCR-AR-Explorer.pdf.
Authors: Sahil Panchavishe (612302040) & Megh Shidam (612302058)
COEP Technological University, Pune - Department of Robotics and AI
"""

import os
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.units import mm, inch
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
    """Draws ISO/ANSI standard engineering border with coordinate ticks (1-8, A-F)."""
    margin = 15 * mm
    w = PAGE_W - 2 * margin
    h = PAGE_H - 2 * margin
    
    # Outer thin border
    c.setStrokeColor(colors.HexColor('#0f172a'))
    c.setLineWidth(1.2)
    c.rect(margin, margin, w, h)
    
    # Inner border line
    c.setLineWidth(0.6)
    c.rect(margin + 3 * mm, margin + 3 * mm, w - 6 * mm, h - 6 * mm)
    
    # Coordinate ticks along top and bottom (1 to 8)
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
    c.setFont("Helvetica-Bold", 7.5)
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
    
    c.setFont("Helvetica-Bold", 8.5)
    c.setFillColor(colors.HexColor('#070d1e'))
    c.drawString(qr_x + qr_w + 3 * mm, qr_y + 11 * mm, "Explore it in 3D")
    c.setFont("Helvetica", 7)
    c.setFillColor(colors.HexColor('#475569'))
    c.drawString(qr_x + qr_w + 3 * mm, qr_y + 7 * mm, "Scan for interactive")
    c.drawString(qr_x + qr_w + 3 * mm, qr_y + 3.5 * mm, "web explorer & AR view.")

def draw_callout_badge(c, bx, by, number, leader_from=None):
    """Draws a professional circular callout badge with high-contrast border and optional leader line."""
    if leader_from:
        c.setStrokeColor(colors.HexColor('#0284c7'))
        c.setLineWidth(1.0)
        c.line(leader_from[0], leader_from[1], bx, by)
    
    # Outer white ring for clarity over dark or light renders
    c.setStrokeColor(colors.white)
    c.setLineWidth(1.2)
    c.setFillColor(colors.HexColor('#0f172a'))
    c.circle(bx, by, 3.4 * mm, fill=1, stroke=1)
    
    c.setFont("Helvetica-Bold", 7.2)
    c.setFillColor(colors.white)
    c.drawCentredString(bx, by - 1.0 * mm, str(number))

def draw_bottom_title_block(c, title, sheet_num):
    """Draws ANSI/ISO standard engineering title block at bottom-right."""
    x_right = PAGE_W - 18 * mm
    y_bottom = 18 * mm
    tb_w = 205 * mm
    tb_h = 16 * mm
    tb_x = x_right - tb_w
    
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
    
    title_font_size = 7.5 if len(title) > 35 else 8.5
    c.setFont("Helvetica-Bold", title_font_size)
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
    c.drawString(18 * mm, y_bottom + 4 * mm, "Original procedural 3D geometry generated for engineering education. Verified glTF 2.0 asset. Renders from project Three.js and Blender engines.")

# =========================================================================
# PAGE 1: THE HARDWARE
# =========================================================================
def build_page_1(c):
    draw_engineering_frame(c, 1)
    draw_top_header(
        c, 1, 'A', 'THE HARDWARE',
        "A domestic refrigerator, taken apart",
        "An original 3D model of a household frost-free domestic refrigerator, exploded into its parts. Numbers match the legend."
    )
    draw_bottom_title_block(c, "THE HARDWARE: REFRIGERATOR, TAKEN APART", 1)
    
    x0 = 18 * mm
    y_content_top = PAGE_H - 48 * mm
    
    # Render 1: Assembled Refrigerator (Front-Open)
    fig1a_w = 180 * mm
    fig1a_h = 115 * mm
    fig1a_x = x0
    fig1a_y = y_content_top - fig1a_h
    
    c.setStrokeColor(colors.HexColor('#cbd5e1'))
    c.setLineWidth(0.8)
    c.rect(fig1a_x, fig1a_y, fig1a_w, fig1a_h, fill=0)
    
    # Figure label banner
    c.setFillColor(colors.HexColor('#f1f5f9'))
    c.rect(fig1a_x, fig1a_y + fig1a_h - 6 * mm, 45 * mm, 6 * mm, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(colors.HexColor('#0f172a'))
    c.drawString(fig1a_x + 2 * mm, fig1a_y + fig1a_h - 4.2 * mm, "FIG. 1A · ASSEMBLED (OPEN DOORS)")
    
    fig1a_img = os.path.join(RENDERS_DIR, 'fig1a_front_open.png')
    if os.path.exists(fig1a_img):
        c.drawImage(fig1a_img, fig1a_x + 10 * mm, fig1a_y + 4 * mm, width=fig1a_w - 20 * mm, height=fig1a_h - 12 * mm, preserveAspectRatio=True)
        
    # Fig 1A Engineering Callouts
    draw_callout_badge(c, fig1a_x + 36 * mm, fig1a_y + 60 * mm, 10)  # Fresh Food Door
    draw_callout_badge(c, fig1a_x + 148 * mm, fig1a_y + 65 * mm, 11) # Freezer Door
    draw_callout_badge(c, fig1a_x + 115 * mm, fig1a_y + 88 * mm, 4)  # Evaporator Unit
    draw_callout_badge(c, fig1a_x + 85 * mm, fig1a_y + 52 * mm, 9)   # Shelves & Crisper Drawers
    draw_callout_badge(c, fig1a_x + 55 * mm, fig1a_y + 98 * mm, 8)   # Cabinet PUF Insulation
        
    # Render 2: Exploded View / Rear Machinery
    fig1b_w = 190 * mm
    fig1b_h = 115 * mm
    fig1b_x = fig1a_x + fig1a_w + 10 * mm
    fig1b_y = fig1a_y
    
    c.rect(fig1b_x, fig1b_y, fig1b_w, fig1b_h, fill=0)
    c.setFillColor(colors.HexColor('#f1f5f9'))
    c.rect(fig1b_x, fig1b_y + fig1b_h - 6 * mm, 40 * mm, 6 * mm, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(colors.HexColor('#0f172a'))
    c.drawString(fig1b_x + 2 * mm, fig1b_y + fig1b_h - 4.2 * mm, "FIG. 1B · EXPLODED REAR VIEW")
    
    fig1c_img = os.path.join(RENDERS_DIR, 'fig1c_exploded.png')
    if os.path.exists(fig1c_img):
        c.drawImage(fig1c_img, fig1b_x + 10 * mm, fig1b_y + 4 * mm, width=fig1b_w - 20 * mm, height=fig1b_h - 12 * mm, preserveAspectRatio=True)
        
    # Fig 1B Engineering Callouts
    draw_callout_badge(c, fig1b_x + 48 * mm, fig1b_y + 24 * mm, 1)   # Compressor
    draw_callout_badge(c, fig1b_x + 82 * mm, fig1b_y + 20 * mm, 6)   # Condenser Fan
    draw_callout_badge(c, fig1b_x + 100 * mm, fig1b_y + 36 * mm, 5)  # Filter-Drier
    draw_callout_badge(c, fig1b_x + 58 * mm, fig1b_y + 44 * mm, 7)   # Refrigerant Lines
    draw_callout_badge(c, fig1b_x + 106 * mm, fig1b_y + 58 * mm, 3)  # Capillary Tube
    draw_callout_badge(c, fig1b_x + 82 * mm, fig1b_y + 70 * mm, 2)   # Condenser Coil
    draw_callout_badge(c, fig1b_x + 82 * mm, fig1b_y + 10 * mm, 12)  # Rear Ventilation Grille
        
    # Lower Section: Component Legend & Model Data Box
    leg_y_top = fig1a_y - 6 * mm
    leg_w = 230 * mm
    leg_h = 80 * mm
    
    # Legend Frame
    c.rect(x0, leg_y_top - leg_h, leg_w, leg_h, fill=0)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(x0 + 3 * mm, leg_y_top - 6 * mm, "Component legend")
    
    # 12 Legend Items in 2 Columns
    legend_items = [
        (1, "Hermetic Compressor", "Draws in LP refrigerant vapour from evaporator, compresses it to HP gas."),
        (2, "Condenser Coil", "Rejects heat (Q_out) to surroundings, condensing HP vapour to liquid."),
        (3, "Capillary Tube", "Throttles high-pressure liquid, plunging pressure & saturation temperature."),
        (4, "Evaporator Unit", "Absorbs heat (Q_in) from food space, vaporising sub-zero refrigerant."),
        (5, "Filter-Drier", "Adsorbs trace moisture (zeolite beads) & filters debris before capillary."),
        (6, "Condenser Fan", "Forces ambient room air across condenser coil and compressor casing."),
        (7, "Refrigerant Circuit Lines", "Discharge, condenser return, and insulated suction lines."),
        (8, "PUF Insulation & Cabinet", "Cyclopentane-blown foam (k ≈ 0.02 W/m·K) preventing heat leak."),
        (9, "Shelves & Crisper Drawers", "Tempered glass shelves and humidity-regulated produce bins."),
        (10, "Fresh Food Door Assembly", "Insulated left door with magnetic bellows gasket seal and bins."),
        (11, "Freezer Door Assembly", "Sub-zero compartment right door with dual hinge pivot."),
        (12, "Rear Ventilation Grille", "Chassis louvers channeling forced hot air exhaust from compressor.")
    ]
    
    col_w = (leg_w - 8 * mm) / 2
    for i, (num, name, desc) in enumerate(legend_items):
        cx = x0 + 4 * mm + (0 if i < 6 else col_w)
        cy = leg_y_top - 14 * mm - (i % 6) * 10.5 * mm
        
        # Circle badge
        c.setFillColor(colors.HexColor('#0f172a'))
        c.circle(cx + 3 * mm, cy + 1.5 * mm, 3.2 * mm, fill=1, stroke=0)
        c.setFont("Helvetica-Bold", 7)
        c.setFillColor(colors.white)
        c.drawCentredString(cx + 3 * mm, cy + 0.3 * mm, str(num))
        
        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(colors.HexColor('#0f172a'))
        c.drawString(cx + 8 * mm, cy + 2 * mm, name)
        
        c.setFont("Helvetica", 6.5)
        c.setFillColor(colors.HexColor('#475569'))
        c.drawString(cx + 8 * mm, cy - 1.5 * mm, desc)
        
    # Right Data Boxes: Verified Model Data & Nameplate Data
    data_x = x0 + leg_w + 6 * mm
    data_w = PAGE_W - 18 * mm - data_x
    data_h = leg_h
    
    c.rect(data_x, leg_y_top - data_h, data_w, data_h, fill=0)
    
    # Model Data Title
    c.setFont("Helvetica-Bold", 8.5)
    c.setFillColor(colors.HexColor('#0f172a'))
    c.drawString(data_x + 3 * mm, leg_y_top - 6 * mm, "Model data")
    c.setFillColor(colors.HexColor('#16a34a'))
    c.setFont("Helvetica-Bold", 6.5)
    c.drawString(data_x + 22 * mm, leg_y_top - 6 * mm, "[VERIFIED GLTF 2.0]")
    
    specs = [
        ("MODEL", "Original procedural GLB, generated by generate_refrigerator_model.py"),
        ("VALIDATION", "Khronos glTF-Validator: 0 errors, 0 warnings"),
        ("HIERARCHY", "165 named nodes · 151 meshes · 15 PBR materials"),
        ("DOOR HINGES", "Dual animated pivot axes (-0.485m & +0.485m hinge origins)"),
        ("FOOTPRINT", "1.00 m wide × 0.72 m deep × 1.80 m tall (generic domestic scale)")
    ]
    for idx, (lbl, val) in enumerate(specs):
        sy = leg_y_top - 12 * mm - idx * 4.5 * mm
        c.setFont("Helvetica-Bold", 6.5)
        c.setFillColor(colors.HexColor('#475569'))
        c.drawString(data_x + 3 * mm, sy, f"{lbl}:")
        c.setFont("Helvetica", 6.5)
        c.setFillColor(colors.HexColor('#0f172a'))
        c.drawString(data_x + 26 * mm, sy, val)
        
    # Lower Nameplate Data Section
    np_y = leg_y_top - 38 * mm
    c.line(data_x, np_y + 2 * mm, data_x + data_w, np_y + 2 * mm)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(data_x + 3 * mm, np_y - 3 * mm, "Typical domestic nameplate specifications")
    c.setFont("Helvetica-Bold", 6.5)
    c.setFillColor(colors.HexColor('#ea580c'))
    c.drawString(data_x + 65 * mm, np_y - 3 * mm, "[REPRESENTATIVE REFERENCE]")
    
    np_specs = [
        ("REFRIGERANT", "R134a / R600a (Isobutane, GWP=3, ODP=0)"),
        ("COMPRESSOR", "1/6 to 1/4 HP Hermetic Reciprocating (~120W to 180W)"),
        ("CONDENSING P", "8.0 to 12.5 bar (~35°C to 45°C saturation temp)"),
        ("EVAPORATING P", "1.1 to 1.4 bar (~ -20°C to -15°C saturation temp)"),
        ("ESTIMATED COP", "1.8 to 2.4 (Typical seasonal household operating range)")
    ]
    for idx, (lbl, val) in enumerate(np_specs):
        sy = np_y - 9 * mm - idx * 4.5 * mm
        c.setFont("Helvetica-Bold", 6.5)
        c.setFillColor(colors.HexColor('#475569'))
        c.drawString(data_x + 3 * mm, sy, f"{lbl}:")
        c.setFont("Helvetica", 6.5)
        c.setFillColor(colors.HexColor('#0f172a'))
        c.drawString(data_x + 28 * mm, sy, val)
        
    c.showPage()

# =========================================================================
# PAGE 2: HOW A DOMESTIC REFRIGERATOR WORKS
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
    
    # Fig 2A: Cycle Schematic Diagram
    fig2a_w = 175 * mm
    fig2a_h = 105 * mm
    fig2a_x = x0
    fig2a_y = y_content_top - fig2a_h
    
    c.setStrokeColor(colors.HexColor('#cbd5e1'))
    c.setLineWidth(0.8)
    c.rect(fig2a_x, fig2a_y, fig2a_w, fig2a_h, fill=0)
    c.setFillColor(colors.HexColor('#f1f5f9'))
    c.rect(fig2a_x, fig2a_y + fig2a_h - 6 * mm, 45 * mm, 6 * mm, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(colors.HexColor('#0f172a'))
    c.drawString(fig2a_x + 2 * mm, fig2a_y + fig2a_h - 4.2 * mm, "FIG. 2A · CYCLE SCHEMATIC")
    
    fig2a_img = os.path.join(RENDERS_DIR, 'fig2a_cycle_schematic.png')
    if os.path.exists(fig2a_img):
        c.drawImage(fig2a_img, fig2a_x + 5 * mm, fig2a_y + 4 * mm, width=fig2a_w - 10 * mm, height=fig2a_h - 12 * mm, preserveAspectRatio=True)
        
    # Fig 2B: p-h Diagram Sketch
    fig2b_w = 125 * mm
    fig2b_h = 105 * mm
    fig2b_x = fig2a_x + fig2a_w + 6 * mm
    fig2b_y = fig2a_y
    
    c.rect(fig2b_x, fig2b_y, fig2b_w, fig2b_h, fill=0)
    c.setFillColor(colors.HexColor('#f1f5f9'))
    c.rect(fig2b_x, fig2b_y + fig2b_h - 6 * mm, 45 * mm, 6 * mm, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(colors.HexColor('#0f172a'))
    c.drawString(fig2b_x + 2 * mm, fig2b_y + fig2b_h - 4.2 * mm, "FIG. 2B · p–h DIAGRAM SKETCH")
    
    fig2b_img = os.path.join(RENDERS_DIR, 'fig2b_ph_diagram.png')
    if os.path.exists(fig2b_img):
        c.drawImage(fig2b_img, fig2b_x + 4 * mm, fig2b_y + 4 * mm, width=fig2b_w - 8 * mm, height=fig2b_h - 12 * mm, preserveAspectRatio=True)
        
    # High vs Low Pressure Summary Box
    sum_w = PAGE_W - 18 * mm - (fig2b_x + fig2b_w + 6 * mm)
    sum_x = fig2b_x + fig2b_w + 6 * mm
    sum_y = fig2a_y
    sum_h = fig2a_h
    
    c.rect(sum_x, sum_y, sum_w, sum_h, fill=0)
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(colors.HexColor('#b91c1c'))
    c.drawString(sum_x + 3 * mm, sum_y + sum_h - 8 * mm, "■ High-pressure side")
    c.setFont("Helvetica", 6.8)
    c.setFillColor(colors.HexColor('#334155'))
    c.drawString(sum_x + 3 * mm, sum_y + sum_h - 14 * mm, "Compressor outlet → condenser coil → filter-drier →")
    c.drawString(sum_x + 3 * mm, sum_y + sum_h - 18 * mm, "capillary inlet. Refrigerant rejects heat (Q_out) here.")
    
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(colors.HexColor('#0284c7'))
    c.drawString(sum_x + 3 * mm, sum_y + sum_h - 28 * mm, "■ Low-pressure side")
    c.setFont("Helvetica", 6.8)
    c.setFillColor(colors.HexColor('#334155'))
    c.drawString(sum_x + 3 * mm, sum_y + sum_h - 34 * mm, "Capillary outlet → evaporator coil → suction line →")
    c.drawString(sum_x + 3 * mm, sum_y + sum_h - 38 * mm, "compressor inlet. Refrigerant boils & absorbs heat (Q_in).")
    
    c.line(sum_x + 3 * mm, sum_y + sum_h - 46 * mm, sum_x + sum_w - 3 * mm, sum_y + sum_h - 46 * mm)
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(colors.HexColor('#0f172a'))
    c.drawString(sum_x + 3 * mm, sum_y + sum_h - 52 * mm, "Energy balance (steady state):")
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(colors.HexColor('#ea580c'))
    c.drawString(sum_x + 3 * mm, sum_y + sum_h - 58 * mm, "Q_out = Q_in + W_in")
    c.setFont("Helvetica-Bold", 8)
    c.drawString(sum_x + 3 * mm, sum_y + sum_h - 64 * mm, "COP = Q_in / W_in")
    
    # 3D Conceptual Flow Render Box
    flow_box_y = sum_y
    flow_box_h = 32 * mm
    c.setFont("Helvetica-Bold", 6.5)
    c.setFillColor(colors.HexColor('#64748b'))
    c.drawString(sum_x + 3 * mm, sum_y + 24 * mm, "FIG. 2C · FLOW TRACE IN 3D")
    fig1b_img = os.path.join(RENDERS_DIR, 'fig1b_rear_machinery.png')
    if os.path.exists(fig1b_img):
        c.drawImage(fig1b_img, sum_x + 3 * mm, sum_y + 2 * mm, width=sum_w - 6 * mm, height=21 * mm, preserveAspectRatio=True)
        
    # Lower 4 Detailed Process Cards
    card_y_top = fig2a_y - 6 * mm
    card_h = 88 * mm
    card_w = (PAGE_W - 36 * mm - 9 * mm) / 4
    
    cards_data = [
        (1, "Evaporation (heat absorbed)",
         "Cold, low-pressure liquid-vapour mixture enters the evaporator coil.",
         "It absorbs heat from food and air in the freezer and fresh food compartments, boiling into low-pressure vapour.",
         "Ideal: Constant-pressure heat addition until refrigerant is saturated vapour.",
         "Real: Slight frictional pressure drop across coil; vapour is superheated 3-5 K at outlet to protect compressor.",
         "#0284c7"),
        (2, "Compression (work input)",
         "Compressor draws in low-pressure vapour and squeezes it into hot gas.",
         "Driven by electric motor work input. Pressure and saturation temperature rise above room ambient.",
         "Ideal: Reversible isentropic (adiabatic) compression (s1 = s2).",
         "Real: Valve losses, motor winding heat, and piston friction make compression non-isentropic (s2 > s1).",
         "#dc2626"),
        (3, "Condensation (heat rejected)",
         "Hot, high-pressure vapour discharges into the rear condenser coil.",
         "Rejects heat (Q_out = Q_in + W_in) to room air. Refrigerant desuperheats, condenses, and subcools.",
         "Ideal: Constant-pressure heat rejection to saturated liquid state.",
         "Real: Slight subcooling (3-8 K) occurs at coil exit, ensuring 100% liquid enters capillary tube.",
         "#ea580c"),
        (4, "Expansion (throttling)",
         "High-pressure liquid is forced through the narrow capillary tube.",
         "High hydraulic resistance causes pressure to drop abruptly. A fraction flashes to vapour, chilling the stream.",
         "Ideal: Irreversible throttling at constant enthalpy (h3 = h4, zero work).",
         "Real: Adiabatic flow with critical choking; soldered to suction line to form internal heat exchanger.",
         "#0ea5e9")
    ]
    
    for i, (num, title, p1, p2, ideal_t, real_t, col) in enumerate(cards_data):
        cx = x0 + i * (card_w + 3 * mm)
        c.rect(cx, card_y_top - card_h, card_w, card_h, fill=0)
        
        # Number badge
        c.setFillColor(colors.HexColor(col))
        c.circle(cx + 5 * mm, card_y_top - 6 * mm, 3.5 * mm, fill=1, stroke=0)
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(colors.white)
        c.drawCentredString(cx + 5 * mm, card_y_top - 7.2 * mm, str(num))
        
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(colors.HexColor('#0f172a'))
        c.drawString(cx + 11 * mm, card_y_top - 6.5 * mm, title)
        
        c.setFont("Helvetica", 6.8)
        c.setFillColor(colors.HexColor('#334155'))
        c.drawString(cx + 3 * mm, card_y_top - 14 * mm, p1[:55])
        c.drawString(cx + 3 * mm, card_y_top - 18 * mm, p1[55:110])
        c.drawString(cx + 3 * mm, card_y_top - 23 * mm, p2[:55])
        c.drawString(cx + 3 * mm, card_y_top - 27 * mm, p2[55:110])
        
        # Ideal block
        c.setFillColor(colors.HexColor('#f8fafc'))
        c.rect(cx + 2 * mm, card_y_top - 54 * mm, card_w - 4 * mm, 24 * mm, fill=1, stroke=0)
        c.setFont("Helvetica-Bold", 6.5)
        c.setFillColor(colors.HexColor('#0f172a'))
        c.drawString(cx + 3 * mm, card_y_top - 33 * mm, "Ideal cycle:")
        c.setFont("Helvetica", 6.2)
        c.setFillColor(colors.HexColor('#475569'))
        c.drawString(cx + 3 * mm, card_y_top - 38 * mm, ideal_t[:50])
        c.drawString(cx + 3 * mm, card_y_top - 42 * mm, ideal_t[50:100])
        
        # Real block
        c.setFont("Helvetica-Bold", 6.5)
        c.setFillColor(colors.HexColor('#b91c1c'))
        c.drawString(cx + 3 * mm, card_y_top - 48 * mm, "Real system:")
        c.setFont("Helvetica", 6.2)
        c.setFillColor(colors.HexColor('#475569'))
        c.drawString(cx + 3 * mm, card_y_top - 52 * mm, real_t[:50])
        c.drawString(cx + 3 * mm, card_y_top - 56 * mm, real_t[50:100])
        
    c.showPage()

# =========================================================================
# PAGE 3: THE PROJECT
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
    
    # 4 Top Columns: C1 Objective, C2 Architecture, C3 How it works, C4 Applications
    col_w = (PAGE_W - 36 * mm - 9 * mm) / 4
    col_h = 95 * mm
    
    # C1: Objective & Motivation
    c.setStrokeColor(colors.HexColor('#cbd5e1'))
    c.rect(x0, y_content_top - col_h, col_w, col_h, fill=0)
    c.setFont("Helvetica-Bold", 8.5)
    c.setFillColor(colors.HexColor('#0f172a'))
    c.drawString(x0 + 3 * mm, y_content_top - 7 * mm, "C1 Objective & motivation")
    c.setFont("Helvetica", 6.8)
    c.setFillColor(colors.HexColor('#334155'))
    
    lines_c1 = [
        "Students learn the vapour compression cycle as",
        "a theoretical four-stage schematic, but a real",
        "domestic refrigerator is a complex machine with",
        "hidden coils, capillary lines, and foamed insulation.",
        "",
        "This project bridges the gap: every component can",
        "be tapped to inspect its thermodynamic function,",
        "the door opens smoothly on dual hinge pivots, and",
        "the life-size refrigerator can be placed in AR on",
        "a real floor or table — with zero app installation.",
        "",
        "• Identify the 4 core cycle components in 3D.",
        "• Trace high-pressure and low-pressure sides.",
        "• Walk around the virtual appliance in life-size AR.",
        "• Relate physical layout to the p-h diagram."
    ]
    for idx, l in enumerate(lines_c1):
        c.drawString(x0 + 3 * mm, y_content_top - 14 * mm - idx * 4.2 * mm, l)
        
    # C2: Implementation Architecture
    c2_x = x0 + col_w + 3 * mm
    c.rect(c2_x, y_content_top - col_h, col_w, col_h, fill=0)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(c2_x + 3 * mm, y_content_top - 7 * mm, "C2 Implementation architecture")
    
    # Draw architecture boxes
    c.setFillColor(colors.HexColor('#070d1e'))
    c.rect(c2_x + 5 * mm, y_content_top - 20 * mm, col_w - 10 * mm, 8 * mm, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 6.8)
    c.setFillColor(colors.HexColor('#00e5ff'))
    c.drawCentredString(c2_x + col_w / 2, y_content_top - 15 * mm, "generate_refrigerator_model.py (Blender Python)")
    
    c.setFillColor(colors.HexColor('#ea580c'))
    c.rect(c2_x + 10 * mm, y_content_top - 34 * mm, col_w - 20 * mm, 8 * mm, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.drawCentredString(c2_x + col_w / 2, y_content_top - 29 * mm, "Domestic_Refrigerator.glb (glTF 2.0)")
    
    c.setFillColor(colors.HexColor('#f1f5f9'))
    c.setStrokeColor(colors.HexColor('#1e2e5c'))
    c.rect(c2_x + 4 * mm, y_content_top - 58 * mm, (col_w - 10 * mm) / 2, 18 * mm, fill=1, stroke=1)
    c.setFont("Helvetica-Bold", 6.5)
    c.setFillColor(colors.HexColor('#0f172a'))
    c.drawCentredString(c2_x + 4 * mm + (col_w - 10 * mm) / 4, y_content_top - 46 * mm, "Web Explorer")
    c.setFont("Helvetica", 5.5)
    c.drawCentredString(c2_x + 4 * mm + (col_w - 10 * mm) / 4, y_content_top - 51 * mm, "React · Three.js")
    
    c.rect(c2_x + 6 * mm + (col_w - 10 * mm) / 2, y_content_top - 58 * mm, (col_w - 10 * mm) / 2, 18 * mm, fill=1, stroke=1)
    c.setFont("Helvetica-Bold", 6.5)
    c.setFillColor(colors.HexColor('#0f172a'))
    c.drawCentredString(c2_x + 6 * mm + 3 * (col_w - 10 * mm) / 4, y_content_top - 46 * mm, "WebAR / XR")
    c.setFont("Helvetica", 5.5)
    c.drawCentredString(c2_x + 6 * mm + 3 * (col_w - 10 * mm) / 4, y_content_top - 51 * mm, "<model-viewer>")
    
    c.setFont("Helvetica-Bold", 6)
    c.setFillColor(colors.HexColor('#0284c7'))
    c.drawString(c2_x + 4 * mm, y_content_top - 68 * mm, "Unity 6 URP Player")
    c.drawString(c2_x + 4 * mm, y_content_top - 73 * mm, "A3 Poster PDF Generator")
    c.setFont("Helvetica", 5.8)
    c.setFillColor(colors.HexColor('#475569'))
    c.drawString(c2_x + 4 * mm, y_content_top - 80 * mm, "Single shared JSON dataset drives website,")
    c.drawString(c2_x + 4 * mm, y_content_top - 84 * mm, "Unity app, and this poster for 100% agreement.")
    
    # C3: How it works
    c3_x = c2_x + col_w + 3 * mm
    c.rect(c3_x, y_content_top - col_h, col_w, col_h, fill=0)
    c.setFont("Helvetica-Bold", 8.5)
    c.setFillColor(colors.HexColor('#0f172a'))
    c.drawString(c3_x + 3 * mm, y_content_top - 7 * mm, "C3 How it works")
    
    lines_c3 = [
        "3D MODEL",
        "Procedural geometry (compressor shell, swept copper",
        "tubing, serpentine condenser, evaporator fins) with",
        "dual animated door hinges exported to glTF 2.0.",
        "",
        "WEB EXPLORER",
        "Interactive tap/click raycast picking, single-part highlight,",
        "ghosted isolate mode, explode slider, cycle flow",
        "pulse animation, and full component library modal.",
        "",
        "AUGMENTED REALITY",
        "Zero-install WebAR: WebXR & Scene Viewer on",
        "ARCore Android; AR Quick Look on iOS. Live camera",
        "overlay fallback on desktops & laptops.",
        "",
        "UNITY 6 PROJECT",
        "URP scenes: MainMenu, RefrigeratorExplorer, and",
        "AR Foundation scene for optional native builds."
    ]
    for idx, l in enumerate(lines_c3):
        is_heading = l in ["3D MODEL", "WEB EXPLORER", "AUGMENTED REALITY", "UNITY 6 PROJECT"]
        c.setFont("Helvetica-Bold" if is_heading else "Helvetica", 6.5 if is_heading else 6.0)
        c.setFillColor(colors.HexColor('#0f172a') if is_heading else colors.HexColor('#475569'))
        c.drawString(c3_x + 3 * mm, y_content_top - 13 * mm - idx * 4.0 * mm, l)
        
    # C4: Applications & Limitations
    c4_x = c3_x + col_w + 3 * mm
    c.rect(c4_x, y_content_top - col_h, col_w, col_h, fill=0)
    c.setFont("Helvetica-Bold", 8.5)
    c.setFillColor(colors.HexColor('#0f172a'))
    c.drawString(c4_x + 3 * mm, y_content_top - 7 * mm, "C4 Applications & limitations")
    
    lines_c4 = [
        "USE IT FOR",
        "• Pre-lab briefing before thermal lab experiments",
        "• Self-study, revision, and 3D exploration on phones",
        "• Visualizing concealed internal cooling components",
        "• Explaining refrigeration to non-specialists",
        "",
        "KEEP IN MIND",
        "• Educational visualization — not manufacturing CAD",
        "• Illustrative generic domestic proportions",
        "• Flow animation is conceptual, not CFD simulation",
        "• No proprietary brand specifications invented",
        "• AR tracking relies on device ARCore / ARKit"
    ]
    for idx, l in enumerate(lines_c4):
        is_heading = l in ["USE IT FOR", "KEEP IN MIND"]
        c.setFont("Helvetica-Bold" if is_heading else "Helvetica", 6.8 if is_heading else 6.2)
        c.setFillColor(colors.HexColor('#0284c7' if l == "USE IT FOR" else '#ea580c') if is_heading else colors.HexColor('#334155'))
        c.drawString(c4_x + 3 * mm, y_content_top - 14 * mm - idx * 4.4 * mm, l)
        
    # Bottom Row: 4 Application Screenshots / Mockup Figures
    fig_y_top = y_content_top - col_h - 6 * mm
    fig_h = 100 * mm
    fig_w = col_w
    
    figs = [
        ("FIG. 3A · WEB EXPLORER (DESKTOP)", os.path.join(RENDERS_DIR, 'fig3a_web_explorer.png')),
        ("FIG. 3B · REAR MACHINERY ISOLATE", os.path.join(RENDERS_DIR, 'fig1b_rear_machinery.png')),
        ("FIG. 3C · AR ROOM PLACEMENT", os.path.join(RENDERS_DIR, 'fig3c_ar_page.png')),
        ("FIG. 3D · ASSEMBLED FRONT VIEW", os.path.join(RENDERS_DIR, 'fig1a_front_open.png'))
    ]
    
    for i, (f_title, f_path) in enumerate(figs):
        fx = x0 + i * (fig_w + 3 * mm)
        c.rect(fx, fig_y_top - fig_h, fig_w, fig_h, fill=0)
        c.setFillColor(colors.HexColor('#f1f5f9'))
        c.rect(fx, fig_y_top - 6 * mm, fig_w, 6 * mm, fill=1, stroke=0)
        c.setFont("Helvetica-Bold", 7)
        c.setFillColor(colors.HexColor('#0f172a'))
        c.drawString(fx + 2 * mm, fig_y_top - 4.2 * mm, f_title)
        
        if os.path.exists(f_path):
            c.drawImage(f_path, fx + 2 * mm, fig_y_top - fig_h + 3 * mm, width=fig_w - 4 * mm, height=fig_h - 11 * mm, preserveAspectRatio=True)
            
    c.showPage()

# =========================================================================
# PAGE 4: SCAN AND EXPLORE
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
    
    # Left Box: CODE 1 · AR
    ar_box_w = 185 * mm
    ar_box_h = 115 * mm
    ar_box_x = x0
    ar_box_y = y_content_top - ar_box_h
    
    c.setStrokeColor(colors.HexColor('#cbd5e1'))
    c.rect(ar_box_x, ar_box_y, ar_box_w, ar_box_h, fill=0)
    
    # Red top pill
    c.setFillColor(colors.HexColor('#dc2626'))
    c.rect(ar_box_x, ar_box_y + ar_box_h - 5 * mm, 45 * mm, 5 * mm, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(colors.white)
    c.drawString(ar_box_x + 2 * mm, ar_box_y + ar_box_h - 3.8 * mm, "AUGMENTED REALITY")
    
    # Large QR Code
    qr_sz = 65 * mm
    qr_ar_img = os.path.join(RENDERS_DIR, 'qr_ar_view.png')
    if os.path.exists(qr_ar_img):
        c.drawImage(qr_ar_img, ar_box_x + 8 * mm, ar_box_y + 20 * mm, width=qr_sz, height=qr_sz)
        
    # Steps
    tx = ar_box_x + qr_sz + 16 * mm
    ty = ar_box_y + ar_box_h - 15 * mm
    
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(colors.HexColor('#dc2626'))
    c.drawString(tx, ty, "CODE 1 · AR")
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.HexColor('#0f172a'))
    c.drawString(tx, ty - 8 * mm, "The fridge, in")
    c.drawString(tx, ty - 15 * mm, "your room")
    
    c.setFont("Helvetica", 7.5)
    c.setFillColor(colors.HexColor('#334155'))
    c.drawString(tx, ty - 22 * mm, "Place the refrigerator on a real floor or table")
    c.drawString(tx, ty - 26 * mm, "at life size, open the doors, and walk around it.")
    
    steps_ar = [
        ("01", "Scan, then tap View in your space."),
        ("02", "Move the phone slowly over a floor or table."),
        ("03", "Walk around it; tap Open Doors to see inside.")
    ]
    for idx, (num, st) in enumerate(steps_ar):
        sy = ty - 34 * mm - idx * 8 * mm
        c.rect(tx, sy, 6 * mm, 5 * mm, fill=0)
        c.setFont("Helvetica-Bold", 6.5)
        c.setFillColor(colors.HexColor('#dc2626'))
        c.drawCentredString(tx + 3 * mm, sy + 1.5 * mm, num)
        c.setFont("Helvetica", 7)
        c.setFillColor(colors.HexColor('#0f172a'))
        c.drawString(tx + 8 * mm, sy + 1.5 * mm, st)
        
    c.setFont("Helvetica", 6.5)
    c.setFillColor(colors.HexColor('#64748b'))
    c.drawString(tx, ty - 60 * mm, "Android: Chrome with Google Play Services for AR (ARCore).")
    c.drawString(tx, ty - 64 * mm, "iPhone/iPad: Safari with AR Quick Look.")
    c.drawString(tx, ty - 68 * mm, "Camera permission asked only when AR starts.")
    
    # Right Box: CODE 2 · WEB
    web_box_w = 185 * mm
    web_box_h = 115 * mm
    web_box_x = ar_box_x + ar_box_w + 10 * mm
    web_box_y = ar_box_y
    
    c.rect(web_box_x, web_box_y, web_box_w, web_box_h, fill=0)
    
    # Cyan top pill
    c.setFillColor(colors.HexColor('#0284c7'))
    c.rect(web_box_x, web_box_y + web_box_h - 5 * mm, 45 * mm, 5 * mm, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(colors.white)
    c.drawString(web_box_x + 2 * mm, web_box_y + web_box_h - 3.8 * mm, "WEB EXPLORER")
    
    qr_web_img = os.path.join(RENDERS_DIR, 'qr_web_explorer.png')
    if os.path.exists(qr_web_img):
        c.drawImage(qr_web_img, web_box_x + 8 * mm, web_box_y + 20 * mm, width=qr_sz, height=qr_sz)
        
    # Steps
    tx2 = web_box_x + qr_sz + 16 * mm
    ty2 = web_box_y + web_box_h - 15 * mm
    
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(colors.HexColor('#0284c7'))
    c.drawString(tx2, ty2, "CODE 2 · WEB")
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.HexColor('#0f172a'))
    c.drawString(tx2, ty2 - 8 * mm, "The whole")
    c.drawString(tx2, ty2 - 15 * mm, "appliance, interactive")
    
    c.setFont("Helvetica", 7.5)
    c.setFillColor(colors.HexColor('#334155'))
    c.drawString(tx2, ty2 - 22 * mm, "Rotate the refrigerator in 3D, tap any of the")
    c.drawString(tx2, ty2 - 26 * mm, "13 parts, open doors, and read the specifications.")
    
    steps_web = [
        ("01", "Scan to open the 3D explorer in browser."),
        ("02", "Tap compressor, condenser, valve or coils."),
        ("03", "Toggle Open Doors or drag Explode slider.")
    ]
    for idx, (num, st) in enumerate(steps_web):
        sy = ty2 - 34 * mm - idx * 8 * mm
        c.rect(tx2, sy, 6 * mm, 5 * mm, fill=0)
        c.setFont("Helvetica-Bold", 6.5)
        c.setFillColor(colors.HexColor('#0284c7'))
        c.drawCentredString(tx2 + 3 * mm, sy + 1.5 * mm, num)
        c.setFont("Helvetica", 7)
        c.setFillColor(colors.HexColor('#0f172a'))
        c.drawString(tx2 + 8 * mm, sy + 1.5 * mm, st)
        
    c.setFont("Helvetica", 6.5)
    c.setFillColor(colors.HexColor('#64748b'))
    c.drawString(tx2, ty2 - 60 * mm, "Works in modern browsers on phones, tablets & laptops.")
    c.drawString(tx2, ty2 - 64 * mm, "Nothing to install · Pure WebGL & WebXR.")
    c.drawString(tx2, ty2 - 68 * mm, "Touch & mouse gestures for orbit, pan and zoom.")
    
    # Lower Section: Project Details (Left) and References & Credits (Right)
    low_y_top = ar_box_y - 6 * mm
    low_h = 80 * mm
    low_w1 = 185 * mm
    low_w2 = 185 * mm
    
    # Project Details
    c.rect(x0, low_y_top - low_h, low_w1, low_h, fill=0)
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(colors.HexColor('#0f172a'))
    c.drawString(x0 + 3 * mm, low_y_top - 6 * mm, "Project")
    
    proj_rows = [
        ("TITLE", "Domestic Refrigerator AR Explorer — Interactive 3D & AR"),
        ("TEAM", "Sahil Panchavishe · 612302040\nMegh Shidam · 612302058"),
        ("BRANCH", "Robotics & AI (B.Tech)"),
        ("GUIDE", "Dr. Shubhangi Deshmukh"),
        ("INSTITUTION", "Department of Robotics & AI, COEP Technological University, Pune")
    ]
    
    curr_y = low_y_top - 14 * mm
    for lbl, val in proj_rows:
        c.setFont("Helvetica-Bold", 7)
        c.setFillColor(colors.HexColor('#475569'))
        c.drawString(x0 + 4 * mm, curr_y, lbl)
        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(colors.HexColor('#0f172a'))
        if "\n" in val:
            v1, v2 = val.split("\n")
            c.drawString(x0 + 28 * mm, curr_y, v1)
            c.drawString(x0 + 28 * mm, curr_y - 3.8 * mm, v2)
            curr_y -= 8.5 * mm
        else:
            c.drawString(x0 + 28 * mm, curr_y, val)
            curr_y -= 6.5 * mm
            
    # References & Credits
    ref_x = x0 + low_w1 + 10 * mm
    c.rect(ref_x, low_y_top - low_h, low_w2, low_h, fill=0)
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(colors.HexColor('#0f172a'))
    c.drawString(ref_x + 3 * mm, low_y_top - 6 * mm, "References & credits")
    
    ref_lines = [
        "• C. P. Arora, Refrigeration and Air Conditioning, 3rd ed., McGraw-Hill, 2008.",
        "• W. F. Stoecker & J. W. Jones, Refrigeration and Air Conditioning, McGraw-Hill.",
        "• Y. A. Çengel & M. A. Boles, Thermodynamics: An Engineering Approach, McGraw-Hill.",
        "• ASHRAE Handbook — Refrigeration (Systems and Equipment), ASHRAE, 2022.",
        "• Software: three.js, Google <model-viewer>, React 19, Vite 6, TypeScript, ReportLab.",
        "• Unity: Unity 6 (URP, glTFast, AR Foundation, ARCore XR Plugin).",
        "• 3D Model: Original procedural educational visualization created via Blender 5.2 Python API.",
        "• Validation: Khronos Group glTF-Validator 2.0 (0 errors, 0 warnings)."
    ]
    for idx, rl in enumerate(ref_lines):
        c.setFont("Helvetica", 6.8)
        c.setFillColor(colors.HexColor('#334155'))
        c.drawString(ref_x + 3 * mm, low_y_top - 14 * mm - idx * 5.2 * mm, rl)
        
    c.showPage()

def generate_pdf():
    print(f"Generating 4-page A3 landscape PDF: {PDF_PATH}")
    c = canvas.Canvas(PDF_PATH, pagesize=landscape(A3))
    
    build_page_1(c)
    build_page_2(c)
    build_page_3(c)
    build_page_4(c)
    
    c.save()
    print("SUCCESS: 4-Page A3 Landscape Technical Poster generated successfully!")

if __name__ == '__main__':
    generate_pdf()
