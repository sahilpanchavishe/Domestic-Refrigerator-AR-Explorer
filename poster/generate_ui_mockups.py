"""
Generates publication-quality technical diagrams and application screenshots
matching the visual standard of VCR-AR-Explorer.pdf.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

out_dir = '/Users/sahilpanchavishe/Desktop/Domestic-Refrigerator-AR-Explorer/poster/renders'
os.makedirs(out_dir, exist_ok=True)

# -------------------------------------------------------------------------
# 1. FIG 2B: Thermodynamic p–h Diagram Sketch (VCR Cycle)
# -------------------------------------------------------------------------
def generate_ph_diagram():
    fig, ax = plt.subplots(figsize=(6.2, 4.8), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')
    
    # Saturation bell curve
    h_liq = np.linspace(150, 310, 100)
    p_liq = np.exp((h_liq - 150) / 45) * 0.8
    h_vap = np.linspace(310, 430, 100)
    p_vap = np.exp((430 - h_vap) / 38) * 0.8
    
    ax.plot(h_liq, p_liq, color='#0284c7', linewidth=2.0, label='Saturated Liquid')
    ax.plot(h_vap, p_vap, color='#0369a1', linewidth=2.0, label='Saturated Vapour')
    
    # Cycle state points:
    # 1: Evaporator exit (LP superheated vapour)
    # 2: Compressor discharge (HP hot gas)
    # 3: Condenser exit (HP subcooled liquid)
    # 4: Capillary exit (LP cold mixture)
    p1, h1 = 1.25, 395
    p2, h2 = 10.5, 435
    p3, h3 = 10.5, 245
    p4, h4 = 1.25, 245
    
    # Cycle process lines
    ax.plot([h1, h2], [p1, p2], color='#dc2626', linewidth=2.5, label='1→2 Compression')
    ax.plot([h2, h3], [p2, p3], color='#ea580c', linewidth=2.5, label='2→3 Condensation')
    ax.plot([h3, h4], [p3, p4], color='#0284c7', linewidth=2.5, linestyle='--', label='3→4 Throttling')
    ax.plot([h4, h1], [p4, p1], color='#0ea5e9', linewidth=2.5, label='4→1 Evaporation')
    
    # Annotate state points with circular badges
    points = [
        (h1, p1, '1', 'LP Vapour', (-20, -18)),
        (h2, p2, '2', 'HP Hot Gas', (10, 2)),
        (h3, p3, '3', 'HP Subcooled Liq', (-115, 6)),
        (h4, p4, '4', 'LP Cold Mix', (-100, -18))
    ]
    for h, p, num, text, offset in points:
        ax.plot(h, p, 'o', markersize=7, color='#0f172a', markeredgecolor='white', markeredgewidth=1.2)
        ax.annotate(f"{num} · {text}", (h, p), textcoords="offset points", xytext=offset,
                    fontweight='bold', fontsize=8, color='#0f172a')
                    
    # Thermodynamic annotations
    ax.text(320, 13.0, 'Q_out · heat rejected to surroundings', color='#ea580c', fontweight='bold', fontsize=8.5, ha='center')
    ax.text(320, 0.65, 'Q_in · heat absorbed from food compartments', color='#0284c7', fontweight='bold', fontsize=8.5, ha='center')
    ax.text(420, 3.8, '1→2 compression\n(W_in work)', color='#dc2626', fontweight='bold', fontsize=7.5, rotation=52)
    ax.text(225, 3.8, '3→4 throttling\n(h3 = h4)', color='#0369a1', fontweight='bold', fontsize=7.5, ha='center')
    
    ax.text(200, 1.2, 'sat. liquid', color='#64748b', fontsize=7, ha='center')
    ax.text(370, 1.2, 'sat. vapour', color='#64748b', fontsize=7, ha='center')
    
    ax.set_yscale('log')
    ax.set_ylim(0.5, 22)
    ax.set_xlim(110, 480)
    ax.set_xlabel('Specific enthalpy h [kJ/kg] →', fontweight='bold', fontsize=8.5)
    ax.set_ylabel('Pressure p [bar] (log scale) →', fontweight='bold', fontsize=8.5)
    ax.set_title('SCHEMATIC · NOT TO SCALE · REPRESENTATIVE DATA', fontweight='bold', fontsize=8, color='#dc2626', pad=8, loc='right')
    ax.grid(True, which="both", ls=":", color="#e2e8f0", linewidth=0.8)
    
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, 'fig2b_ph_diagram.png'), dpi=300)
    plt.close()
    print("Generated fig2b_ph_diagram.png")

# -------------------------------------------------------------------------
# 2. FIG 2A: Thermodynamic Cycle Schematic
# -------------------------------------------------------------------------
def generate_cycle_schematic():
    fig, ax = plt.subplots(figsize=(6.8, 4.8), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # Division line between High-Pressure and Low-Pressure sides
    ax.axhline(y=4.85, color='#cbd5e1', linestyle=':', linewidth=1.2)
    ax.text(0.5, 5.05, 'HIGH-PRESSURE SIDE', color='#dc2626', fontweight='bold', fontsize=8)
    ax.text(0.5, 2.5, 'LOW-PRESSURE SIDE', color='#0284c7', fontweight='bold', fontsize=8)
    
    # Heat exchange arrows
    ax.annotate('', xy=(5.0, 7.5), xytext=(5.0, 7.0), arrowprops=dict(arrowstyle="->", color='#dc2626', lw=2))
    ax.text(5.0, 7.6, '▲ Q_out · heat rejected to surroundings', ha='center', color='#dc2626', fontweight='bold', fontsize=8.5)
    
    ax.annotate('', xy=(5.0, 2.5), xytext=(5.0, 3.0), arrowprops=dict(arrowstyle="<-", color='#0284c7', lw=2))
    ax.text(5.0, 2.2, '▼ Q_in · heat absorbed from food compartments', ha='center', color='#0284c7', fontweight='bold', fontsize=8.5)
    
    # 2. Condenser Coil (Top)
    cond_rect = patches.FancyBboxPatch((3.0, 5.6), 4.0, 1.3, boxstyle="round,pad=0.08", fc='#ffffff', ec='#ea580c', lw=2)
    ax.add_patch(cond_rect)
    ax.text(5.0, 6.25, '2 Condenser', ha='center', va='center', fontweight='bold', fontsize=10, color='#0f172a')
    
    # 1. Compressor (Bottom right)
    comp_rect = patches.FancyBboxPatch((6.0, 0.8), 3.0, 1.4, boxstyle="round,pad=0.08", fc='#ffffff', ec='#dc2626', lw=2)
    ax.add_patch(comp_rect)
    ax.text(7.5, 1.5, '1 Compressor', ha='center', va='center', fontweight='bold', fontsize=10, color='#0f172a')
    ax.annotate('', xy=(7.5, 0.8), xytext=(7.5, 0.2), arrowprops=dict(arrowstyle="->", color='#0f172a', lw=1.8))
    ax.text(7.5, 0.05, 'W_in (Electric work)', ha='center', fontsize=7.5, fontweight='bold', color='#475569')
    
    # 3. Capillary Tube (Left)
    cap_rect = patches.FancyBboxPatch((0.8, 3.2), 2.8, 1.4, boxstyle="round,pad=0.08", fc='#ffffff', ec='#0284c7', lw=2)
    ax.add_patch(cap_rect)
    ax.text(2.2, 3.9, '3 Capillary Tube', ha='center', va='center', fontweight='bold', fontsize=10, color='#0f172a')
    
    # 4. Evaporator (Bottom center)
    evap_rect = patches.FancyBboxPatch((2.2, 2.7), 3.8, 1.3, boxstyle="round,pad=0.08", fc='#ffffff', ec='#0ea5e9', lw=2)
    ax.add_patch(evap_rect)
    ax.text(4.1, 3.35, '4 Evaporator', ha='center', va='center', fontweight='bold', fontsize=10, color='#0f172a')
    
    # Cycle flow arrows:
    # 1 -> 2: Compressor to Condenser (Hot Gas)
    ax.annotate('', xy=(7.0, 5.6), xytext=(7.5, 2.2), arrowprops=dict(arrowstyle="->", color='#dc2626', lw=2.5))
    ax.text(8.2, 4.0, 'HP hot vapour 2', color='#dc2626', fontweight='bold', fontsize=8, ha='center')
    
    # 2 -> 3: Condenser to Capillary Tube (Liquid)
    ax.annotate('', xy=(2.0, 4.6), xytext=(3.0, 6.25), arrowprops=dict(arrowstyle="->", color='#ea580c', lw=2.5))
    ax.text(2.0, 5.5, 'HP liquid 3', color='#ea580c', fontweight='bold', fontsize=8)
    
    # 3 -> 4: Capillary Tube to Evaporator (Cold Mix)
    ax.annotate('', xy=(2.2, 3.35), xytext=(0.8, 3.9), arrowprops=dict(arrowstyle="->", color='#0284c7', lw=2.5, ls='--'))
    ax.text(1.2, 3.0, 'LP liquid + vapour 4', color='#0284c7', fontweight='bold', fontsize=8)
    
    # 4 -> 1: Evaporator to Compressor (Suction Line)
    ax.annotate('', xy=(6.0, 1.5), xytext=(6.0, 3.35), arrowprops=dict(arrowstyle="->", color='#0ea5e9', lw=2.5))
    ax.text(6.8, 2.5, 'LP vapour 1', color='#0ea5e9', fontweight='bold', fontsize=8)
    
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, 'fig2a_cycle_schematic.png'), dpi=300)
    plt.close()
    print("Generated fig2a_cycle_schematic.png")

# -------------------------------------------------------------------------
# 3. FIG 3A, 3B, 3C, 3D UI MOCKUPS
# -------------------------------------------------------------------------
def generate_ui_figures():
    front_img = os.path.join(out_dir, 'fig1a_front_open.png')
    rear_img = os.path.join(out_dir, 'fig2c_flow_trace.png')
    
    # Fig 3A: Web Explorer Desktop
    fig, ax = plt.subplots(figsize=(6, 4), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#070d1e')
    
    if os.path.exists(front_img):
        img = Image.open(front_img)
        ax.imshow(img, extent=[0.5, 7.5, 0.5, 7.5])
        
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # Top bar
    top_bar = patches.Rectangle((0, 7.2), 10, 0.8, fc='#091129', ec='#1e2e5c', lw=1)
    ax.add_patch(top_bar)
    ax.text(0.4, 7.6, 'DOMESTIC REFRIGERATOR AR EXPLORER · WEB VIEWER', color='#00e5ff', fontweight='bold', fontsize=7.5, va='center')
    
    # Inspector panel on right
    side_panel = patches.Rectangle((7.0, 0), 3.0, 7.2, fc='#091129', ec='#1e2e5c', lw=1)
    ax.add_patch(side_panel)
    ax.text(7.3, 6.7, 'PART #01 · COMPRESSOR', color='#00e5ff', fontweight='bold', fontsize=7.5)
    ax.text(7.3, 6.2, 'Hermetic Reciprocating Unit', color='#ffffff', fontweight='bold', fontsize=7)
    ax.text(7.3, 5.5, 'Refrigerant: R134a / R600a\nPressure: 1.25 bar → 10.5 bar\nDrive: 1/5 HP Single-Phase\nDisplacement: 5.8 cc', color='#94a3b8', fontsize=6.2, va='top')
    
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, 'fig3a_web_explorer.png'), dpi=300)
    plt.close()
    print("Generated fig3a_web_explorer.png")
    
    # Fig 3B: Mobile Phone View
    fig, ax = plt.subplots(figsize=(4, 5.5), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#070d1e')
    
    if os.path.exists(front_img):
        img = Image.open(front_img)
        ax.imshow(img, extent=[0.5, 9.5, 1.5, 8.5])
        
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Phone header
    phone_hdr = patches.Rectangle((0, 9.0), 10, 1.0, fc='#091129', ec='#1e2e5c', lw=1)
    ax.add_patch(phone_hdr)
    ax.text(5.0, 9.5, 'REF/AR · MOBILE EXPLORER', color='#00e5ff', fontweight='bold', fontsize=8, ha='center', va='center')
    
    # Bottom inspector drawer
    phone_drawer = patches.FancyBboxPatch((0.5, 0.4), 9.0, 2.2, boxstyle="round,pad=0.1", fc='#091129', ec='#00e5ff', lw=1)
    ax.add_patch(phone_drawer)
    ax.text(0.9, 2.1, 'PART #02 · CONDENSER COIL', color='#00e5ff', fontweight='bold', fontsize=7.5)
    ax.text(0.9, 1.5, 'High-Side Heat Rejection · Forced Air Cooling', color='#f8fafc', fontsize=6.5)
    ax.text(0.9, 0.9, 'Tap part to inspect · Drag to orbit · Pinch to zoom', color='#94a3b8', fontsize=6)
    
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, 'fig3b_phone_view.png'), dpi=300)
    plt.close()
    print("Generated fig3b_phone_view.png")

    # Fig 3C: AR Experience View
    fig, ax = plt.subplots(figsize=(6, 4), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#131b2e')
    
    if os.path.exists(front_img):
        img = Image.open(front_img)
        ax.imshow(img, extent=[2, 8, 1, 7])
        
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # AR Tracking grid
    for x in np.linspace(1, 9, 9):
        ax.plot([x, x], [0.5, 2.5], color='#00e5ff', alpha=0.35, lw=0.8)
    for y in np.linspace(0.5, 2.5, 5):
        ax.plot([1, 9], [y, y], color='#00e5ff', alpha=0.35, lw=0.8)
        
    ar_banner = patches.FancyBboxPatch((2.2, 7.1), 5.6, 0.6, boxstyle="round,pad=0.05", fc=(0, 0, 0, 0.8), ec='#00e5ff', lw=1)
    ax.add_patch(ar_banner)
    ax.text(5.0, 7.4, 'FLOOR DETECTED · TAP TO PLACE AT LIFE SIZE (1:1)', color='#00e5ff', fontweight='bold', fontsize=7.5, ha='center', va='center')
    
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, 'fig3c_ar_page.png'), dpi=300)
    plt.close()
    print("Generated fig3c_ar_page.png")

    # Fig 3D: 3D Cycle Mode
    fig, ax = plt.subplots(figsize=(6, 4), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#070d1e')
    
    if os.path.exists(rear_img):
        img = Image.open(rear_img)
        ax.imshow(img, extent=[1, 9, 0.5, 7.5])
        
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    flow_tag = patches.FancyBboxPatch((0.5, 7.1), 5.5, 0.6, boxstyle="round,pad=0.05", fc='#091129', ec='#00e5ff', lw=1)
    ax.add_patch(flow_tag)
    ax.text(0.8, 7.4, 'REFRIGERANT FLOW ACTIVE · STAGE 2: CONDENSATION', color='#00e5ff', fontweight='bold', fontsize=7, va='center')
    
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, 'fig3d_cycle_mode.png'), dpi=300)
    plt.close()
    print("Generated fig3d_cycle_mode.png")

if __name__ == '__main__':
    generate_ph_diagram()
    generate_cycle_schematic()
    generate_ui_figures()
