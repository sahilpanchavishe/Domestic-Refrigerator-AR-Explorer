"""
Composites transparent Blender renders onto pure white (#ffffff) cards
with subtle drop contact shadow for authentic technical document rendering.
"""

import os
from PIL import Image, ImageFilter, ImageOps

RENDERS_DIR = '/Users/sahilpanchavishe/Desktop/Domestic-Refrigerator-AR-Explorer/poster/renders'

def composite_to_white(raw_filename, out_filename, add_shadow=True):
    raw_path = os.path.join(RENDERS_DIR, raw_filename)
    out_path = os.path.join(RENDERS_DIR, out_filename)
    
    if not os.path.exists(raw_path):
        print(f"File not found: {raw_path}")
        return
        
    img = Image.open(raw_path).convert("RGBA")
    w, h = img.size
    
    # Create white canvas
    canvas = Image.new("RGBA", (w, h), (255, 255, 255, 255))
    
    if add_shadow:
        # Create subtle soft ambient occlusion / contact shadow from alpha mask
        alpha = img.split()[3]
        shadow_mask = alpha.filter(ImageFilter.GaussianBlur(radius=12))
        shadow_color = Image.new("RGBA", (w, h), (15, 23, 42, 60)) # 60/255 opacity
        
        # Shift shadow slightly downward to ground the object
        shadow_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        shadow_layer.paste(shadow_color, (0, 10), mask=shadow_mask)
        
        # Composite shadow over white canvas
        canvas = Image.alpha_composite(canvas, shadow_layer)
        
    # Paste 3D render over canvas using alpha channel
    final_img = Image.alpha_composite(canvas, img)
    final_rgb = final_img.convert("RGB")
    final_rgb.save(out_path, quality=95)
    print(f"Saved publication render: {out_path}")

def main():
    composite_to_white("fig1a_raw.png", "fig1a_front_open.png", add_shadow=True)
    composite_to_white("fig1c_raw.png", "fig1c_exploded.png", add_shadow=True)
    composite_to_white("fig2c_raw.png", "fig2c_flow_trace.png", add_shadow=True)

if __name__ == '__main__':
    main()
