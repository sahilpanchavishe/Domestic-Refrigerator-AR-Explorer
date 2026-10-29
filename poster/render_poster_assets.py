"""
Blender Poster High-Resolution Render Script (Fixed Studio Lighting & Tracked Cameras)
Renders bright, publication-quality 3D views of the Domestic Refrigerator for the A3 Technical Poster.
"""

import bpy
import mathutils
import math
import os

def look_at(cam_obj, target_vec):
    """Accurately orient camera to look directly at target_vec."""
    direction = target_vec - cam_obj.location
    rot_quat = direction.to_track_quat('-Z', 'Y')
    cam_obj.rotation_euler = rot_quat.to_euler()

def setup_camera(name, location, target_vec, lens=45):
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

def setup_render_settings(output_path, res_x=1920, res_y=1200):
    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_EEVEE'
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGB'
    scene.render.film_transparent = False
    scene.render.resolution_x = res_x
    scene.render.resolution_y = res_y
    scene.render.filepath = output_path

def setup_studio_lighting():
    scene = bpy.context.scene
    world = bpy.data.worlds.new('StudioWorld')
    scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get('Background')
    if bg:
        bg.inputs['Color'].default_value = (0.95, 0.96, 0.98, 1.0)
        bg.inputs['Strength'].default_value = 0.9

    # Key Light (Sun / Strong Area)
    key_data = bpy.data.lights.new(name="SunKey", type='SUN')
    key_data.energy = 4.5
    key_obj = bpy.data.objects.new("SunKey", key_data)
    bpy.context.collection.objects.link(key_obj)
    key_obj.location = (3.5, 4.0, 5.0)
    look_at(key_obj, mathutils.Vector((0, 0, 0.95)))

    # Fill Light (Cool Cyan Accent)
    fill_data = bpy.data.lights.new(name="FillLight", type='POINT')
    fill_data.energy = 300
    fill_data.color = (0.8, 0.95, 1.0)
    fill_obj = bpy.data.objects.new("FillLight", fill_data)
    bpy.context.collection.objects.link(fill_obj)
    fill_obj.location = (-3.5, 2.5, 2.0)

    # Rear/Rim Light (Warm Copper Accent)
    rim_data = bpy.data.lights.new(name="RimLight", type='POINT')
    rim_data.energy = 400
    rim_data.color = (1.0, 0.9, 0.8)
    rim_obj = bpy.data.objects.new("RimLight", rim_data)
    bpy.context.collection.objects.link(rim_obj)
    rim_obj.location = (0.0, -3.5, 2.2)

def main():
    blend_path = '/Users/sahilpanchavishe/Desktop/Domestic-Refrigerator-AR-Explorer/Assets/Models/Domestic_Refrigerator.blend'
    out_dir = '/Users/sahilpanchavishe/Desktop/Domestic-Refrigerator-AR-Explorer/poster/renders'
    os.makedirs(out_dir, exist_ok=True)
    
    print(f"Opening {blend_path}")
    bpy.ops.wm.open_mainfile(filepath=blend_path)
    
    setup_studio_lighting()

    left_hinge = bpy.data.objects.get("10_Fresh_Food_Door_Assembly")
    right_hinge = bpy.data.objects.get("11_Freezer_Door_Assembly")
    target_center = mathutils.Vector((0, 0, 0.95))
    
    # -------------------------------------------------------------
    # VIEW 1: Assembled Refrigerator (Front-Isometric with Open Doors)
    # -------------------------------------------------------------
    # Advance to frame 40 where keyframed door opening reaches maximum angle (~78°)
    bpy.context.scene.frame_set(40)
    
    cam1 = setup_camera("CamFrontOpen", mathutils.Vector((2.1, 2.7, 1.6)), target_center, lens=42)
    setup_render_settings(os.path.join(out_dir, "fig1a_front_open.png"))
    bpy.ops.render.render(write_still=True)
    print("Rendered fig1a_front_open.png with open doors at frame 40")
    
    # -------------------------------------------------------------
    # VIEW 2: Rear Hardware View (Machinery, Compressor, Coils)
    # -------------------------------------------------------------
    # Return to frame 0 (closed doors)
    bpy.context.scene.frame_set(0)
    
    # Hide outer casing panel to reveal internal components clearly for engineering drawing
    rear_casing = bpy.data.objects.get("Rear_Outer_Casing")
    if rear_casing: rear_casing.hide_render = True
    
    # Target lower machinery and rear coils: center around z=0.85, looking from behind
    target_rear = mathutils.Vector((0, -0.2, 0.85))
    cam2 = setup_camera("CamRear", mathutils.Vector((-1.4, -2.6, 1.4)), target_rear, lens=42)
    setup_render_settings(os.path.join(out_dir, "fig1b_rear_machinery.png"))
    bpy.ops.render.render(write_still=True)
    print("Rendered fig1b_rear_machinery.png")
    
    # -------------------------------------------------------------
    # VIEW 3: Exploded View
    # -------------------------------------------------------------
    bpy.context.scene.frame_set(0)
    # Clear animations so offsets are preserved on doors
    for hinge_obj in [left_hinge, right_hinge]:
        if hinge_obj:
            hinge_obj.animation_data_clear()
            hinge_obj.rotation_euler = (0, 0, 0)
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
            
    cam3 = setup_camera("CamExploded", mathutils.Vector((2.6, -2.5, 2.0)), target_center, lens=38)
    setup_render_settings(os.path.join(out_dir, "fig1c_exploded.png"))
    bpy.ops.render.render(write_still=True)
    print("Rendered fig1c_exploded.png")

if __name__ == '__main__':
    main()
