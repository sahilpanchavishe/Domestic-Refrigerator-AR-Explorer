"""
Generates high quality application screenshots and diagrams for Page 2 and Page 3 of the technical poster.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

out_dir = '/Users/sahilpanchavishe/Desktop/Domestic-Refrigerator-AR-Explorer/poster/renders'
os.makedirs(out_dir, exist_ok=True)

# 1. Generate Fig 2B: P-h Diagram Sketch
def generate_ph_diagram():
    fig, ax = plt.subplots(figsize=(6, 4.5), dpi=300)
    fig.patch.set_facecolor('#f8fafc')
    ax.set_facecolor('#ffffff')
    
    # Saturation dome
    h_liq = np.linspace(150, 300, 100)
    p_liq = np.exp((h_liq - 150) / 45) * 0.8
    h_vap = np.linspace(300, 420, 100)
    p_vap = np.exp((420 - h_vap) / 38) * 0.8
    
    ax.plot(h_liq, p_liq, color='#0284c7', linewidth=2.5, label='Saturated Liquid')
    ax.plot(h_vap, p_vap, color='#0369a1', linewidth=2.5, label='Saturated Vapour')
    
    # Cycle points: 1 (Evap exit), 2 (Comp exit), 3 (Cond exit), 4 (Capillary exit)
    p1, h1 = 1.2, 395
    p2, h2 = 10.5, 440
    p3, h3 = 10.5, 240
    p4, h4 = 1.2, 240
    
    # Plot cycle lines
    ax.plot([h1, h2], [p1, p2], color='#dc2626', linewidth=2.8, label='1→2 Compression')
    ax.plot([h2, h3], [p2, p3], color='#ea580c', linewidth=2.8, label='2→3 Condensation')
    ax.plot([h3, h4], [p3, p4], color='#0284c7', linewidth=2.8, linestyle='--', label='3→4 Throttling (Capillary)')
    ax.plot([h4, h1], [p4, p1], color='#0ea5e9', linewidth=2.8, label='4→1 Evaporation')
    
    # State point circles & labels with safe non-overlapping offsets
    points = [(h1, p1, '1 (LP Vapour)', '#0284c7', (-15, -18)),
              (h2, p2, '2 (HP Hot Gas)', '#dc2626', (10, 2)),
              (h3, p3, '3 (HP Subcooled Liq)', '#ea580c', (-115, 6)),
              (h4, p4, '4 (LP Cold Mix)', '#0ea5e9', (-100, -18))]
              
    for h, p, label, col, offset in points:
        ax.plot(h, p, 'o', markersize=8, color=col, markeredgecolor='black', markeredgewidth=1.2)
        ax.annotate(label, (h, p), textcoords="offset points", xytext=offset,
                    fontweight='bold', fontsize=8.5, color='#0f172a')
                    
    # Annotations positioned cleanly
    ax.text(320, 12.5, 'Q_out (Heat Rejected to Room)', color='#ea580c', fontweight='bold', fontsize=9.5, ha='center')
    ax.text(320, 0.65, 'Q_in (Heat Absorbed from Food)', color='#0284c7', fontweight='bold', fontsize=9.5, ha='center')
    ax.text(420, 4.0, 'W_in (Compressor Work)', color='#dc2626', fontweight='bold', fontsize=8.5, rotation=52)
    ax.text(225, 4.0, 'Capillary Tube\n(h3 = h4)', color='#0369a1', fontweight='bold', fontsize=8, ha='center')
    
    ax.set_yscale('log')
    ax.set_ylim(0.5, 22)
    ax.set_xlim(110, 490)
    ax.set_xlabel('Specific Enthalpy h [kJ/kg] →', fontweight='bold', fontsize=9.5)
    ax.set_ylabel('Pressure p [bar] (log scale) →', fontweight='bold', fontsize=9.5)
    ax.set_title('FIG. 2B · p–h DIAGRAM (DOMESTIC REFRIGERATOR VCR CYCLE)', fontweight='bold', fontsize=10.5, pad=12)
    ax.grid(True, which="both", ls=":", color="#cbd5e1")
    
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, 'fig2b_ph_diagram.png'), dpi=300)
    plt.close()
    print("Generated fig2b_ph_diagram.png")

# 2. Generate Fig 2A: Schematic Diagram
def generate_cycle_schematic():
    fig, ax = plt.subplots(figsize=(6.5, 4.5), dpi=300)
    fig.patch.set_facecolor('#f8fafc')
    ax.set_facecolor('#ffffff')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # Compressor (bottom-center)
    comp_rect = patches.FancyBboxPatch((4.0, 0.6), 2.0, 1.3, boxstyle="round,pad=0.1", fc='#fee2e2', ec='#dc2626', lw=2)
    ax.add_patch(comp_rect)
    ax.text(5.0, 1.3, '1 COMPRESSOR', ha='center', va='center', fontweight='bold', fontsize=10, color='#991b1b')
    ax.text(5.0, 0.9, 'W_in (Electric Work)', ha='center', va='center', fontsize=8, color='#b91c1c')
    
    # Condenser (top)
    cond_rect = patches.FancyBboxPatch((2.2, 5.9), 5.6, 1.4, boxstyle="round,pad=0.1", fc='#ffedd5', ec='#ea580c', lw=2)
    ax.add_patch(cond_rect)
    ax.text(5.0, 6.7, '2 CONDENSER COIL', ha='center', va='center', fontweight='bold', fontsize=11, color='#9a3412')
    ax.text(5.0, 6.2, 'Q_out (Heat Rejected to Kitchen Surroundings)', ha='center', va='center', fontsize=8.5, color='#c2410c')
    
    # Expansion device / Capillary Tube (left)
    exp_rect = patches.FancyBboxPatch((0.5, 3.1), 2.3, 1.5, boxstyle="round,pad=0.1", fc='#e0f2fe', ec='#0284c7', lw=2)
    ax.add_patch(exp_rect)
    ax.text(1.65, 4.0, '3 CAPILLARY TUBE', ha='center', va='center', fontweight='bold', fontsize=9.5, color='#075985')
    ax.text(1.65, 3.5, 'Throttling (h3 = h4)', ha='center', va='center', fontsize=8, color='#0369a1')
    
    # Evaporator (right)
    evap_rect = patches.FancyBboxPatch((7.2, 3.1), 2.3, 1.5, boxstyle="round,pad=0.1", fc='#dbeafe', ec='#2563eb', lw=2)
    ax.add_patch(evap_rect)
    ax.text(8.35, 4.0, '4 EVAPORATOR', ha='center', va='center', fontweight='bold', fontsize=10, color='#1e40af')
    ax.text(8.35, 3.5, 'Q_in (Heat Absorbed)', ha='center', va='center', fontsize=8, color='#1d4ed8')
    
    # Arrows connecting cycle with clean non-overlapping labels
    # 1 -> 2: Compressor to Condenser (Hot Gas)
    ax.annotate('', xy=(6.5, 5.9), xytext=(5.8, 1.9),
                arrowprops=dict(arrowstyle="->", color='#dc2626', lw=2.5))
    ax.text(6.8, 2.7, 'HP Hot Vapour (2)', color='#dc2626', fontweight='bold', fontsize=8.5)
    
    # 2 -> 3: Condenser to Capillary Tube (Subcooled Liquid)
    ax.annotate('', xy=(1.65, 4.6), xytext=(2.5, 6.1),
                arrowprops=dict(arrowstyle="->", color='#ea580c', lw=2.5))
    ax.text(1.1, 5.4, 'HP Liquid (3)', color='#ea580c', fontweight='bold', fontsize=8.5)
    
    # 3 -> 4: Capillary Tube to Evaporator (Cold Liquid-Vapour Mix)
    ax.annotate('', xy=(7.2, 3.85), xytext=(2.8, 3.85),
                arrowprops=dict(arrowstyle="->", color='#0284c7', lw=2.5, ls='--'))
    ax.text(5.0, 4.15, 'LP Cold Liquid-Vapour Mixture (4)', color='#0284c7', fontweight='bold', fontsize=8.5, ha='center')
    
    # 4 -> 1: Evaporator to Compressor (Suction Line)
    ax.annotate('', xy=(4.5, 1.9), xytext=(7.5, 3.1),
                arrowprops=dict(arrowstyle="->", color='#2563eb', lw=2.5))
    ax.text(6.3, 2.0, 'LP Vapour Suction Line (1)', color='#2563eb', fontweight='bold', fontsize=8.5)
    
    # High pressure vs low pressure division line
    ax.axhline(y=4.95, color='#94a3b8', linestyle=':', linewidth=1.5)
    ax.text(0.6, 5.15, 'HIGH-PRESSURE CONDENSING SIDE', color='#b91c1c', fontweight='bold', fontsize=8)
    ax.text(0.6, 2.6, 'LOW-PRESSURE EVAPORATING SIDE', color='#0369a1', fontweight='bold', fontsize=8)
    
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, 'fig2a_cycle_schematic.png'), dpi=300)
    plt.close()
    print("Generated fig2a_cycle_schematic.png")

# 3. Generate Fig 3A, 3B, 3C UI Mockups
def generate_ui_figures():
    # Use existing renders to create realistic app interface composites
    front_img_path = os.path.join(out_dir, 'fig1a_front_open.png')
    rear_img_path = os.path.join(out_dir, 'fig1b_rear_machinery.png')
    
    # Fig 3A: Web Explorer Interface Card
    fig, ax = plt.subplots(figsize=(6, 4), dpi=300)
    fig.patch.set_facecolor('#070d1e')
    ax.set_facecolor('#0b142d')
    
    if os.path.exists(front_img_path):
        img = Image.open(front_img_path)
        ax.imshow(img, extent=[1, 9, 0.5, 7.5])
        
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # UI Overlays
    # Top bar
    top_bar = patches.Rectangle((0, 7.2), 10, 0.8, fc='#091129', ec='#1e2e5c', lw=1)
    ax.add_patch(top_bar)
    ax.text(0.4, 7.6, 'DOMESTIC REFRIGERATOR AR EXPLORER · 3D WEB VIEWER', color='#00e5ff', fontweight='bold', fontsize=8, va='center')
    
    # Inspector panel on right
    side_panel = patches.Rectangle((7.2, 0), 2.8, 7.2, fc='#091129', ec='#1e2e5c', lw=1)
    ax.add_patch(side_panel)
    ax.text(7.5, 6.7, 'PART #01', color='#00e5ff', fontweight='bold', fontsize=8)
    ax.text(7.5, 6.3, 'HERMETIC COMPRESSOR', color='#ffffff', fontweight='bold', fontsize=8)
    ax.text(7.5, 5.7, 'Function: Vapour Compression\nRefrigerant: R134a / R600a\nWork Input: W_in\nPressure: 1.2 to 11 bar', color='#94a3b8', fontsize=6.5, va='top')
    
    # Buttons at bottom
    btn1 = patches.FancyBboxPatch((0.5, 0.4), 1.8, 0.5, boxstyle="round,pad=0.05", fc='#00e5ff', ec='#48cae4')
    ax.add_patch(btn1)
    ax.text(1.4, 0.65, 'OPEN DOORS', color='#070d1e', fontweight='bold', fontsize=7, ha='center', va='center')
    
    btn2 = patches.FancyBboxPatch((2.6, 0.4), 1.8, 0.5, boxstyle="round,pad=0.05", fc='#1e293b', ec='#334155')
    ax.add_patch(btn2)
    ax.text(3.5, 0.65, 'EXPLODE 40%', color='#f8fafc', fontweight='bold', fontsize=7, ha='center', va='center')
    
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, 'fig3a_web_explorer.png'), dpi=300)
    plt.close()
    print("Generated fig3a_web_explorer.png")
    
    # Fig 3C: AR Experience View
    fig, ax = plt.subplots(figsize=(6, 4), dpi=300)
    fig.patch.set_facecolor('#070d1e')
    ax.set_facecolor('#131b2e')
    
    if os.path.exists(front_img_path):
        img = Image.open(front_img_path)
        ax.imshow(img, extent=[2, 8, 1, 7])
        
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # AR Tracking grid
    for x in np.linspace(1, 9, 9):
        ax.plot([x, x], [0.5, 2.5], color='#00e5ff', alpha=0.3, lw=0.8)
    for y in np.linspace(0.5, 2.5, 5):
        ax.plot([1, 9], [y, y], color='#00e5ff', alpha=0.3, lw=0.8)
        
    ar_banner = patches.FancyBboxPatch((2.5, 7.1), 5.0, 0.6, boxstyle="round,pad=0.05", fc=(0, 0, 0, 0.75), ec='#00e5ff', lw=1)
    ax.add_patch(ar_banner)
    ax.text(5.0, 7.4, 'SURFACE DETECTED · TAP TO PLACE IN ROOM', color='#00e5ff', fontweight='bold', fontsize=7.5, ha='center', va='center')
    
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, 'fig3c_ar_page.png'), dpi=300)
    plt.close()
    print("Generated fig3c_ar_page.png")

if __name__ == '__main__':
    generate_ph_diagram()
    generate_cycle_schematic()
    generate_ui_figures()
