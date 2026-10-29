"""
Procedural Refrigerator Assembly & Model Generation Script for Domestic Refrigerator AR Explorer
Authors: Sahil Panchavishe (612302040) & Megh Shidam (612302058)
COEP Technological University, Pune - Department of Robotics and AI
"""

import bpy
import mathutils
import math
import os
import sys

def create_material(name, base_color, metallic=0.0, roughness=0.5, alpha=1.0, transmission=0.0):
    mat = bpy.data.materials.get(name)
    if mat is None:
        mat = bpy.data.materials.new(name=name)
    if mat.node_tree:
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs['Base Color'].default_value = base_color
            bsdf.inputs['Metallic'].default_value = metallic
            bsdf.inputs['Roughness'].default_value = roughness
            if 'Transmission Weight' in bsdf.inputs:
                bsdf.inputs['Transmission Weight'].default_value = transmission
            elif 'Transmission' in bsdf.inputs:
                bsdf.inputs['Transmission'].default_value = transmission
    return mat

def build_evaporator_coil(parent):
    """Builds an authentic Evaporator coil with cooling fin pack in the freezer cooling compartment."""
    curve_data = bpy.data.curves.new('Evaporator_Tube_Curve', type='CURVE')
    curve_data.dimensions = '3D'
    curve_data.bevel_depth = 0.007
    curve_data.bevel_resolution = 4
    
    spline = curve_data.splines.new('BEZIER')
    points_coords = [
        (0.08, -0.26, 1.35),
        (0.38, -0.26, 1.35),
        (0.38, -0.26, 1.42),
        (0.08, -0.26, 1.42),
        (0.08, -0.26, 1.49),
        (0.38, -0.26, 1.49),
        (0.38, -0.26, 1.56),
        (0.08, -0.26, 1.56),
        (0.08, -0.26, 1.63),
        (0.38, -0.26, 1.63),
    ]
    spline.bezier_points.add(len(points_coords) - 1)
    for i, coord in enumerate(points_coords):
        p = spline.bezier_points[i]
        p.co = coord
        p.handle_left_type = 'AUTO'
        p.handle_right_type = 'AUTO'
        
    tube_obj = bpy.data.objects.new('Evaporator_Coil_Serpentine', curve_data)
    bpy.context.collection.objects.link(tube_obj)
    tube_obj.parent = parent
    
    mat_copper = bpy.data.materials.get("Copper_Refrigerant_Tube")
    if mat_copper:
        tube_obj.data.materials.append(mat_copper)
        
    # Cooling fin block (aluminum heat exchange plate stack)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.23, -0.26, 1.49))
    fin_pack = bpy.context.active_object
    fin_pack.name = 'Evaporator_Cooling_Fins'
    fin_pack.scale = (0.32, 0.035, 0.30)
    fin_pack.parent = parent
    mat_fins = create_material("Evaporator_Aluminum_Fins", (0.85, 0.88, 0.92, 1.0), metallic=0.75, roughness=0.25)
    if fin_pack.data.materials:
        fin_pack.data.materials[0] = mat_fins
    else:
        fin_pack.data.materials.append(mat_fins)
        
    # Accumulator canister at evaporator exit
    bpy.ops.mesh.primitive_cylinder_add(radius=0.022, depth=0.12, location=(0.06, -0.24, 1.40))
    accum = bpy.context.active_object
    accum.name = 'Evaporator_Accumulator'
    accum.parent = parent
    accum.data.materials.append(mat_copper)

def build_thermostat_unit(parent):
    """Builds interior thermostat dial and sensor box."""
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.43, 0.05, 1.25))
    box = bpy.context.active_object
    box.name = 'Thermostat_Housing'
    box.scale = (0.035, 0.08, 0.065)
    box.parent = parent
    mat_plastic = bpy.data.materials.get("Cool_Grey_Plastic")
    if not mat_plastic:
        mat_plastic = create_material("Thermostat_Plastic", (0.9, 0.92, 0.95, 1.0), metallic=0.1, roughness=0.4)
    box.data.materials.append(mat_plastic)
    
    # Dial knob
    bpy.ops.mesh.primitive_cylinder_add(radius=0.018, depth=0.015, location=(-0.41, 0.05, 1.25))
    dial = bpy.context.active_object
    dial.name = 'Thermostat_Knob_Dial'
    dial.rotation_euler = (0, math.radians(90), 0)
    dial.parent = parent
    mat_dial = create_material("Dial_Cyan_Accent", (0.05, 0.75, 0.85, 1.0), metallic=0.3, roughness=0.2)
    dial.data.materials.append(mat_dial)

def main():
    source_glb = '/Users/sahilpanchavishe/Downloads/refrigerator_educational.glb'
    target_dir = '/Users/sahilpanchavishe/Desktop/Domestic-Refrigerator-AR-Explorer/Assets/Models'
    blend_path = os.path.join(target_dir, 'Domestic_Refrigerator.blend')
    glb_path = os.path.join(target_dir, 'Domestic_Refrigerator.glb')
    
    print(f"Loading source model: {source_glb}")
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=source_glb)
    
    # Scene root
    root = bpy.data.objects.get("Refrigerator_Root")
    if not root:
        root = bpy.data.objects.new("Domestic_Refrigerator", None)
        bpy.context.collection.objects.link(root)
    else:
        root.name = "Domestic_Refrigerator"
        
    # Create empty groupings for major educational components
    groups = {
        "01_Compressor": [
            "Compressor_Main_Shell", "Compressor_Top_Dome", "Compressor_Top_Neck",
            "Compressor_Terminal_Cover", "Compressor_Mounting_Foot_Left", "Compressor_Mounting_Foot_Right"
        ],
        "02_Condenser_Coil": [
            "Condenser_Coil_Serpentine", "Rear_Upper_Coil_Bracket", "Rear_Lower_Cross_Bracket"
        ],
        "03_Capillary_Tube": [
            "Capillary_Tube"
        ],
        "04_Evaporator_Unit": [],
        "05_Filter_Drier": [
            "Filter_Drier_Canister", "Filter_Drier_Mounting_Clip"
        ],
        "06_Condenser_Fan": [
            "Condenser_Cooling_Fan_Guard_Ring", "Condenser_Fan_Hub",
            "Condenser_Fan_Blade_1", "Condenser_Fan_Blade_2", "Condenser_Fan_Blade_3",
            "Condenser_Fan_Blade_4", "Condenser_Fan_Blade_5"
        ],
        "07_Refrigerant_Lines": [
            "Compressor_Discharge_Tube", "Condenser_Return_Tube", "Suction_Return_Line"
        ],
        "08_Cabinet_Body": [
            "Cabinet_Left_Side_Panel", "Cabinet_Right_Side_Panel", "Cabinet_Top_Panel", "Cabinet_Base_Panel",
            "Interior_Back_Liner", "Interior_Left_Liner", "Interior_Right_Liner", "Interior_Floor_Liner",
            "Interior_Top_Liner", "Central_Compartment_Divider",
            "Opening_Gasket_Left", "Opening_Gasket_Right", "Opening_Gasket_Top", "Opening_Gasket_Bottom",
            "Left_Front_Adjustable_Foot", "Left_Front_Foot_Pad", "Left_Rear_Adjustable_Foot", "Left_Rear_Foot_Pad",
            "Right_Front_Adjustable_Foot", "Right_Front_Foot_Pad", "Right_Rear_Adjustable_Foot", "Right_Rear_Foot_Pad",
            "Fresh_Food_Air_Vent_Slot_1", "Fresh_Food_Air_Vent_Slot_2", "Fresh_Food_Air_Vent_Slot_3",
            "Fresh_Food_Air_Vent_Slot_4", "Fresh_Food_Air_Vent_Slot_5",
            "Freezer_Air_Vent_Slot_1", "Freezer_Air_Vent_Slot_2", "Freezer_Air_Vent_Slot_3",
            "Freezer_Air_Vent_Slot_4", "Freezer_Air_Vent_Slot_5"
        ],
        "09_Shelves_And_Drawers": [
            "Fresh_Food_Glass_Shelf_1", "Fresh_Food_Glass_Shelf_2", "Fresh_Food_Glass_Shelf_3", "Fresh_Food_Glass_Shelf_4",
            "Fresh_Food_Shelf_Rail_1_L", "Fresh_Food_Shelf_Rail_1_R", "Fresh_Food_Shelf_Rail_2_L", "Fresh_Food_Shelf_Rail_2_R",
            "Fresh_Food_Shelf_Rail_3_L", "Fresh_Food_Shelf_Rail_3_R", "Fresh_Food_Shelf_Rail_4_L", "Fresh_Food_Shelf_Rail_4_R",
            "Freezer_Glass_Shelf_1", "Freezer_Glass_Shelf_2", "Freezer_Glass_Shelf_3", "Freezer_Glass_Shelf_4",
            "Freezer_Shelf_Rail_1_L", "Freezer_Shelf_Rail_1_R", "Freezer_Shelf_Rail_2_L", "Freezer_Shelf_Rail_2_R",
            "Freezer_Shelf_Rail_3_L", "Freezer_Shelf_Rail_3_R", "Freezer_Shelf_Rail_4_L", "Freezer_Shelf_Rail_4_R",
            "Produce_Drawer_Body", "Produce_Drawer_Front", "Produce_Drawer_Handle",
            "Freezer_Lower_Bin_Body", "Freezer_Lower_Bin_Front",
            "Freezer_Upper_Bin_Body", "Freezer_Upper_Bin_Front"
        ],
        "12_Rear_Ventilation_Grille": [
            "Rear_Outer_Casing", "Rear_Cable_Clamp",
            "Rear_Casing_Vertical_Rib_1", "Rear_Casing_Vertical_Rib_2", "Rear_Casing_Vertical_Rib_3",
            "Rear_Casing_Vertical_Rib_4", "Rear_Casing_Vertical_Rib_5", "Rear_Casing_Vertical_Rib_6",
            "Rear_Casing_Vertical_Rib_7", "Rear_Casing_Vertical_Rib_8", "Rear_Casing_Vertical_Rib_9",
            "Rear_Vent_Slat_1", "Rear_Vent_Slat_2", "Rear_Vent_Slat_3", "Rear_Vent_Slat_4", "Rear_Vent_Slat_5"
        ],
        "13_Thermostat_Electrical": [
            "Rear_Electrical_Connector_Block", "Red_Electrical_Wire", "Yellow_Electrical_Wire"
        ]
    }
    
    group_empties = {}
    for group_name, members in groups.items():
        grp = bpy.data.objects.new(group_name, None)
        bpy.context.collection.objects.link(grp)
        grp.parent = root
        group_empties[group_name] = grp
        for m_name in members:
            obj = bpy.data.objects.get(m_name)
            if obj:
                obj.parent = grp
                
    # Build Evaporator into group 04
    build_evaporator_coil(group_empties["04_Evaporator_Unit"])
    
    # Build Thermostat into group 13
    build_thermostat_unit(group_empties["13_Thermostat_Electrical"])
    
    # Setup Hinge Assemblies
    # 1. Left Door Hinge (Fresh Food Door)
    left_hinge = bpy.data.objects.new("10_Fresh_Food_Door_Assembly", None)
    left_hinge.location = (-0.485, 0.355, 0.0)
    bpy.context.collection.objects.link(left_hinge)
    left_hinge.parent = root
    
    left_door_parts = [o for o in bpy.data.objects if o.name.startswith("Fresh_Food_Door_") or o.name.startswith("Fresh_Food_Handle_")]
    left_hinge_hardware = [o for o in bpy.data.objects if o.name.startswith("Left_Door_Hinge_")]
    
    for obj in left_door_parts:
        obj.parent = left_hinge
        obj.matrix_parent_inverse.identity()
        obj.location = (0, 0, 0)
        obj.rotation_euler = (0, 0, 0)
        
    for h in left_hinge_hardware:
        h.parent = left_hinge
        
    # 2. Right Door Hinge (Freezer Door)
    right_hinge = bpy.data.objects.new("11_Freezer_Door_Assembly", None)
    right_hinge.location = (0.485, 0.355, 0.0)
    bpy.context.collection.objects.link(right_hinge)
    right_hinge.parent = root
    
    right_door_parts = [o for o in bpy.data.objects if o.name.startswith("Freezer_Door_") or o.name.startswith("Freezer_Handle_")]
    right_hinge_hardware = [o for o in bpy.data.objects if o.name.startswith("Right_Door_Hinge_")]
    
    for obj in right_door_parts:
        obj.parent = right_hinge
        obj.matrix_parent_inverse.identity()
        obj.location = (0, 0, 0)
        obj.rotation_euler = (0, 0, 0)
        
    for h in right_hinge_hardware:
        h.parent = right_hinge
        
    # Animate Door Opening & Closing
    bpy.context.scene.frame_start = 0
    bpy.context.scene.frame_end = 120
    
    open_angle_rad = math.radians(78.0)
    
    # Keyframe Left Door Hinge
    left_hinge.rotation_euler = (0, 0, 0)
    left_hinge.keyframe_insert("rotation_euler", frame=0)
    left_hinge.rotation_euler = (0, 0, open_angle_rad)
    left_hinge.keyframe_insert("rotation_euler", frame=40)
    left_hinge.rotation_euler = (0, 0, open_angle_rad)
    left_hinge.keyframe_insert("rotation_euler", frame=80)
    left_hinge.rotation_euler = (0, 0, 0)
    left_hinge.keyframe_insert("rotation_euler", frame=120)
    
    # Keyframe Right Door Hinge
    right_hinge.rotation_euler = (0, 0, 0)
    right_hinge.keyframe_insert("rotation_euler", frame=0)
    right_hinge.rotation_euler = (0, 0, -open_angle_rad)
    right_hinge.keyframe_insert("rotation_euler", frame=40)
    right_hinge.rotation_euler = (0, 0, -open_angle_rad)
    right_hinge.keyframe_insert("rotation_euler", frame=80)
    right_hinge.rotation_euler = (0, 0, 0)
    right_hinge.keyframe_insert("rotation_euler", frame=120)
    
    # Keyframe Fan rotation
    fan_hub = bpy.data.objects.get("Condenser_Fan_Hub")
    if fan_hub:
        fan_hub.rotation_euler = (0, 0, 0)
        fan_hub.keyframe_insert("rotation_euler", frame=0)
        fan_hub.rotation_euler = (0, math.radians(360 * 4), 0)
        fan_hub.keyframe_insert("rotation_euler", frame=120)
        
    # Save Blender project file
    print(f"Saving .blend: {blend_path}")
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    
    # Export GLB
    print(f"Exporting .glb: {glb_path}")
    bpy.ops.export_scene.gltf(
        filepath=glb_path,
        export_format='GLB',
        use_selection=False,
        export_apply=False,
        export_animations=True,
        export_def_bones=False,
        export_optimize_animation_size=False
    )
    
    print("SUCCESS: Blender model and GLB exported successfully!")

if __name__ == '__main__':
    main()
