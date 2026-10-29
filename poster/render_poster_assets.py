"""
Blender Poster High-Resolution Render Script
Renders actual 3D views of the Domestic Refrigerator for the A3 Technical Poster.
"""

import bpy
import mathutils
import math
import os

def setup_camera(location, rotation_euler, lens=50):
    cam = bpy.data.objects.get("PosterCamera")
    if not cam:
        cam_data = bpy.data.cameras.new("PosterCamera")
        cam = bpy.data.objects.new("PosterCamera", cam_data)
        bpy.context.collection.objects.link(cam)
    bpy.context.scene.camera = cam
    cam.location = location
    cam.rotation_euler = rotation_euler
    cam.data.lens = lens
    return cam

def setup_render_engine(output_path, res_x=1920, res_y=1200):
    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_EEVEE'
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'
    scene.render.resolution_x = res_x
    scene.render.resolution_y = res_y
    scene.render.filepath = output_path
    scene.render.film_transparent = True

def main():
    blend_path = '/Users/sahilpanchavishe/Desktop/Domestic-Refrigerator-AR-Explorer/Assets/Models/Domestic_Refrigerator.blend'
    out_dir = '/Users/sahilpanchavishe/Desktop/Domestic-Refrigerator-AR-Explorer/poster/renders'
    os.makedirs(out_dir, exist_ok=True)
    
    print(f"Opening {blend_path}")
    bpy.ops.wm.open_mainfile(filepath=blend_path)
    
    # Studio lighting
    light_data = bpy.data.lights.new(name="StudioKey", type='AREA')
    light_data.energy = 800
    light_data.size = 3.0
    light_obj = bpy.data.objects.new("StudioKey", light_data)
    bpy.context.collection.objects.link(light_obj)
    light_obj.location = (2.5, 3.5, 3.2)
    light_obj.rotation_euler = (math.radians(45), 0, math.radians(35))
    
    fill_data = bpy.data.lights.new(name="StudioFill", type='AREA')
    fill_data.energy = 500
    fill_data.size = 4.0
    fill_obj = bpy.data.objects.new("StudioFill", fill_data)
    bpy.context.collection.objects.link(fill_obj)
    fill_obj.location = (-3.0, 2.0, 2.5)
    fill_obj.rotation_euler = (math.radians(35), 0, math.radians(-50))
    
    rim_data = bpy.data.lights.new(name="StudioRim", type='AREA')
    rim_data.energy = 900
    rim_data.size = 3.0
    rim_obj = bpy.data.objects.new("StudioRim", rim_data)
    bpy.context.collection.objects.link(rim_obj)
    rim_obj.location = (0.0, -3.5, 2.5)
    rim_obj.rotation_euler = (math.radians(45), 0, math.radians(180))

    left_hinge = bpy.data.objects.get("10_Fresh_Food_Door_Assembly")
    right_hinge = bpy.data.objects.get("11_Freezer_Door_Assembly")
    
    # View 1: Assembled Refrigerator (Front-Isometric with open doors revealing interior)
    if left_hinge: left_hinge.rotation_euler.z = math.radians(65)
    if right_hinge: right_hinge.rotation_euler.z = math.radians(-65)
    setup_camera((2.1, 2.4, 1.6), (math.radians(72), 0, math.radians(42)), lens=42)
    setup_render_engine(os.path.join(out_dir, "fig1a_front_open.png"))
    bpy.ops.render.render(write_still=True)
    print("Rendered fig1a_front_open.png")
    
    # View 2: Rear Hardware View (Compressor, Condenser, Fan, Filter-Drier, Capillary Tube)
    if left_hinge: left_hinge.rotation_euler.z = 0
    if right_hinge: right_hinge.rotation_euler.z = 0
    # Hide outer casing panel to reveal internal components clearly for engineering drawing
    rear_casing = bpy.data.objects.get("Rear_Outer_Casing")
    if rear_casing: rear_casing.hide_render = True
    setup_camera((-1.2, -2.5, 1.2), (math.radians(74), 0, math.radians(-155)), lens=45)
    setup_render_engine(os.path.join(out_dir, "fig1b_rear_machinery.png"))
    bpy.ops.render.render(write_still=True)
    print("Rendered fig1b_rear_machinery.png")
    
    # View 3: Exploded View
    offsets = {
        '01_Compressor': (-0.35, 0, -0.45),
        '02_Condenser_Coil': (0, 0, -0.65),
        '03_Capillary_Tube': (0.25, 0.15, -0.35),
        '04_Evaporator_Unit': (0, 0.3, 0.4),
        '05_Filter_Drier': (0.35, -0.1, -0.3),
        '06_Condenser_Fan': (0.45, 0, -0.55),
        '07_Refrigerant_Lines': (-0.25, 0, -0.3),
        '09_Shelves_And_Drawers': (0, 0.5, 0.25),
        '10_Fresh_Food_Door_Assembly': (-0.55, 0.2, 0.45),
        '11_Freezer_Door_Assembly': (0.55, 0.2, 0.45),
        '12_Rear_Ventilation_Grille': (0, 0, -0.85)
    }
    for name, offset in offsets.items():
        obj = bpy.data.objects.get(name)
        if obj:
            obj.location = (obj.location[0] + offset[0], obj.location[1] + offset[1], obj.location[2] + offset[2])
            
    setup_camera((2.8, -2.6, 2.0), (math.radians(68), 0, math.radians(135)), lens=38)
    setup_render_engine(os.path.join(out_dir, "fig1c_exploded.png"))
    bpy.ops.render.render(write_still=True)
    print("Rendered fig1c_exploded.png")

if __name__ == '__main__':
    main()
