"""
Blender Publication-Quality Poster Render Script
Generates high-contrast, perfectly framed, transparent-background 3D renders
and composites them onto pure white (#ffffff) for seamless inclusion in the technical poster.
"""

import bpy
import mathutils
import math
import os
import subprocess

def look_at(cam_obj, target_vec):
    """Accurately orient camera to look directly at target_vec."""
    direction = target_vec - cam_obj.location
    rot_quat = direction.to_track_quat('-Z', 'Y')
    cam_obj.rotation_euler = rot_quat.to_euler()

def setup_camera(name, location, target_vec, lens=38):
    cam = bpy.data.objects.get(name)
    if not cam:
        cam_data = bpy.data.cameras.new(name)
        cam = bpy.data.objects.new(name, cam_data)
        bpy.context.collection.objects.link(cam)
    bpy.context.scene.camera = cam
    cam.location = location
    look_at(cam, target_vec)
    cam.data.lens = lens
    return cam

def setup_render_settings(output_path, res_x=2400, res_y=1500):
    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_EEVEE'
    scene.render.film_transparent = True
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'
    scene.render.resolution_x = res_x
    scene.render.resolution_y = res_y
    scene.render.filepath = output_path

def apply_engineering_materials():
    """Applies high-contrast, publication-grade materials to all components."""
    for m in bpy.data.materials:
        bsdf = None
        if m.use_nodes:
            for n in m.node_tree.nodes:
                if n.type == 'BSDF_PRINCIPLED':
                    bsdf = n
                    break
        if not bsdf: continue
        
        name = m.name
        if 'Door' in name or 'Enamel' in name or 'Brushed' in name:
            # Sleek dark titanium / satin graphite exterior
            bsdf.inputs['Base Color'].default_value = (0.22, 0.25, 0.28, 1.0)
            bsdf.inputs['Metallic'].default_value = 0.75
            bsdf.inputs['Roughness'].default_value = 0.28
        elif 'Compressor' in name:
            # Glossy deep black enamel
            bsdf.inputs['Base Color'].default_value = (0.02, 0.02, 0.03, 1.0)
            bsdf.inputs['Metallic'].default_value = 0.35
            bsdf.inputs['Roughness'].default_value = 0.12
        elif 'Copper' in name:
            # Gleaming copper tubing
            bsdf.inputs['Base Color'].default_value = (0.88, 0.45, 0.20, 1.0)
            bsdf.inputs['Metallic'].default_value = 0.95
            bsdf.inputs['Roughness'].default_value = 0.15
        elif 'Condenser' in name:
            # Heat dissipating satin black
            bsdf.inputs['Base Color'].default_value = (0.08, 0.09, 0.10, 1.0)
            bsdf.inputs['Metallic'].default_value = 0.45
            bsdf.inputs['Roughness'].default_value = 0.35
        elif 'Interior' in name:
            # Pristine clean white interior liner
            bsdf.inputs['Base Color'].default_value = (0.95, 0.96, 0.97, 1.0)
            bsdf.inputs['Roughness'].default_value = 0.25
        elif 'Glass' in name:
            # Aqua tinted tempered glass
            bsdf.inputs['Base Color'].default_value = (0.65, 0.88, 0.95, 1.0)
            bsdf.inputs['Roughness'].default_value = 0.05
            if 'Transmission Weight' in bsdf.inputs:
                bsdf.inputs['Transmission Weight'].default_value = 0.85
            elif 'Transmission' in bsdf.inputs:
                bsdf.inputs['Transmission'].default_value = 0.85
        elif 'Evaporator' in name or 'Fins' in name:
            # Bright silver aluminum fins
            bsdf.inputs['Base Color'].default_value = (0.92, 0.94, 0.96, 1.0)
            bsdf.inputs['Metallic'].default_value = 0.9
            bsdf.inputs['Roughness'].default_value = 0.2
        elif 'Plastic' in name:
            bsdf.inputs['Base Color'].default_value = (0.85, 0.88, 0.90, 1.0)
            bsdf.inputs['Roughness'].default_value = 0.3

def setup_studio_lighting():
    """Configures high-contrast studio lighting with interior cabinet LED."""
    for obj in list(bpy.context.collection.objects):
        if obj.type == 'LIGHT':
            bpy.data.objects.remove(obj, do_unlink=True)
            
    # Key Light (Front-Top Sun)
    key = bpy.data.lights.new(name="KeySun", type='SUN')
    key.energy = 4.0
    key_obj = bpy.data.objects.new("KeySun", key)
    bpy.context.collection.objects.link(key_obj)
    key_obj.location = (2.5, 3.2, 4.0)
    look_at(key_obj, mathutils.Vector((0, 0, 0.9)))
    
    # Fill Light (Cool ambient soft sun)
    fill = bpy.data.lights.new(name="FillSun", type='SUN')
    fill.energy = 2.2
    fill.color = (0.92, 0.96, 1.0)
    fill_obj = bpy.data.objects.new("FillSun", fill)
    bpy.context.collection.objects.link(fill_obj)
    fill_obj.location = (-3.0, 2.5, 2.0)
    look_at(fill_obj, mathutils.Vector((0, 0, 0.9)))
    
    # Interior Refrigerator LED Glow
    led = bpy.data.lights.new(name="InteriorLED", type='POINT')
    led.energy = 150
    led.color = (0.95, 0.98, 1.0)
    led_obj = bpy.data.objects.new("InteriorLED", led)
    bpy.context.collection.objects.link(led_obj)
    led_obj.location = (0.0, 0.05, 1.25)
    
    # Machinery Accent Rim Light (Warm copper highlight)
    rim = bpy.data.lights.new(name="MachineryRim", type='POINT')
    rim.energy = 350
    rim.color = (1.0, 0.85, 0.70)
    rim_obj = bpy.data.objects.new("MachineryRim", rim)
    bpy.context.collection.objects.link(rim_obj)
    rim_obj.location = (0.0, -2.5, 0.6)

def main():
    blend_path = '/Users/sahilpanchavishe/Desktop/Domestic-Refrigerator-AR-Explorer/Assets/Models/Domestic_Refrigerator.blend'
    out_dir = '/Users/sahilpanchavishe/Desktop/Domestic-Refrigerator-AR-Explorer/poster/renders'
    os.makedirs(out_dir, exist_ok=True)
    
    print(f"Opening {blend_path}")
    bpy.ops.wm.open_mainfile(filepath=blend_path)
    
    apply_engineering_materials()
    setup_studio_lighting()
    
    # Parent door hinge brackets to cabinet body so they stay fixed to cabinet
    cabinet = bpy.data.objects.get('08_Cabinet_Body')
    if cabinet:
        for name in ['Left_Door_Hinge_1', 'Left_Door_Hinge_2', 'Left_Door_Hinge_3', 
                     'Right_Door_Hinge_1', 'Right_Door_Hinge_2', 'Right_Door_Hinge_3']:
            h = bpy.data.objects.get(name)
            if h: h.parent = cabinet

    left_hinge = bpy.data.objects.get("10_Fresh_Food_Door_Assembly")
    right_hinge = bpy.data.objects.get("11_Freezer_Door_Assembly")
    
    # -------------------------------------------------------------
    # 1. FIG 1A: ASSEMBLED FRONT VIEW (OPEN DOORS)
    # -------------------------------------------------------------
    # Both doors swing outward: left door opens to -68°, right door opens to +68°
    if left_hinge:
        left_hinge.animation_data_clear()
        left_hinge.rotation_euler.z = math.radians(-68)
    if right_hinge:
        right_hinge.animation_data_clear()
        right_hinge.rotation_euler.z = math.radians(68)
        
    target_assembled = mathutils.Vector((0, 0.05, 0.90))
    cam1 = setup_camera("CamFrontOpen", mathutils.Vector((1.75, 2.75, 1.35)), target_assembled, lens=36)
    
    raw_1a = os.path.join(out_dir, "fig1a_raw.png")
    setup_render_settings(raw_1a)
    bpy.ops.render.render(write_still=True)
    print("Rendered fig1a_raw.png")
    
    # -------------------------------------------------------------
    # 2. FIG 1B: EXPLODED VIEW (REAR ISOMETRIC)
    # -------------------------------------------------------------
    for hinge_obj in [left_hinge, right_hinge]:
        if hinge_obj:
            hinge_obj.animation_data_clear()
            hinge_obj.rotation_euler = (0, 0, 0)
            
    # Explode component offsets
    offsets = {
        '01_Compressor': (-0.32, -0.42, -0.16),
        '02_Condenser_Coil': (0, -0.62, 0.0),
        '03_Capillary_Tube': (0.35, -0.38, 0.12),
        '04_Evaporator_Unit': (0, 0.25, 0.38),
        '05_Filter_Drier': (0.42, -0.48, -0.12),
        '06_Condenser_Fan': (0.52, -0.42, -0.20),
        '07_Refrigerant_Lines': (-0.2, -0.32, -0.1),
        '09_Shelves_And_Drawers': (0, 0.62, 0.12),
        '10_Fresh_Food_Door_Assembly': (-0.65, 0.62, 0.18),
        '11_Freezer_Door_Assembly': (0.65, 0.62, 0.18),
        '12_Rear_Ventilation_Grille': (0, -0.82, -0.26)
    }
    for name, offset in offsets.items():
        obj = bpy.data.objects.get(name)
        if obj:
            obj.location = (obj.location[0] + offset[0], obj.location[1] + offset[1], obj.location[2] + offset[2])
            
    # Hide outer casing panel to clearly display interior coils and lines
    rc = bpy.data.objects.get('Rear_Outer_Casing')
    if rc: rc.hide_render = True
    
    target_exploded = mathutils.Vector((0, -0.05, 0.80))
    cam2 = setup_camera("CamExploded", mathutils.Vector((-2.9, -3.3, 1.85)), target_exploded, lens=34)
    
    raw_1b = os.path.join(out_dir, "fig1c_raw.png")
    setup_render_settings(raw_1b)
    bpy.ops.render.render(write_still=True)
    print("Rendered fig1c_raw.png (Exploded)")

    # -------------------------------------------------------------
    # 3. FIG 2C: REAR MACHINERY CLOSE-UP (FLOW TRACE VIEW)
    # -------------------------------------------------------------
    # Reopen file to reset offsets for clean assembled rear view
    bpy.ops.wm.open_mainfile(filepath=blend_path)
    apply_engineering_materials()
    setup_studio_lighting()
    
    rc = bpy.data.objects.get('Rear_Outer_Casing')
    if rc: rc.hide_render = True
    
    target_machinery = mathutils.Vector((0, -0.25, 0.75))
    cam3 = setup_camera("CamMachinery", mathutils.Vector((-1.35, -2.2, 1.25)), target_machinery, lens=42)
    raw_2c = os.path.join(out_dir, "fig2c_raw.png")
    setup_render_settings(raw_2c, res_x=1600, res_y=1600)
    bpy.ops.render.render(write_still=True)
    print("Rendered fig2c_raw.png")

if __name__ == '__main__':
    main()
