import bpy
import random
import math

# ==============================================================================
# 1. SETTINGS & ANCHOR TRANSFORM
# ==============================================================================
SCALE = 0.001          # mm to meters
STAGGER_GAP = 15       # Delay between objects
START_FRAME = 1        

# ASSEMBLY TRANSFORM (Use this to Rotate/Move the WHOLE PLANT)
OFFSET_X = -1.0       
OFFSET_Y = -1.20       
ROTATION_DEG = 45.0   

# LIST OF PCB OBJECT NAMES
PCB_NAMES = (
    "Vertical_Component_PCB", 
    "Central_Chip_PCB_Assembly", 
    "Green_PCB_Assembly", 
    "Raytheon_Fused",
    "Green_Shield_PCB"
)

# ==============================================================================
# 2. PATH DEFINITIONS
# ==============================================================================

# Standard Path (Feeder -> Conveyor -> Into Shredder Top)
PCB_PATH_SHORT = [
    {"frame": 0,   "pos": (500,   600, 900)},   # Start on Feeder Center
    {"frame": 100, "pos": (4000,  600, 900)},   # Feeder End
    {"frame": 180, "pos": (6500,  600, 850)},   # Conveyor
    {"frame": 200, "pos": (7000,  600, 850)},   
    {"frame": 236, "pos": (7500,  300, 1500)},  # Shift Y to Shredder Center
    {"frame": 260, "pos": (7500,  300, 1000)},  # Drop into blades
]

# Green Shield Path (Feeder -> Shredder -> Drop to Screw Conv)
GREEN_SHIELD_PATH = [
    {"frame": 0,   "pos": (200,   600, 950)},
    {"frame": 100, "pos": (4000,  600, 950)},
    {"frame": 180, "pos": (6500,  600, 850)},
    {"frame": 200, "pos": (7500,  300, 1500)},  # Shredder Top
    {"frame": 220, "pos": (7500,  300, 0)},     # Fall Through
    {"frame": 300, "pos": (10000, 0, 1400)},    # Screw Conv Start (Center Y=0)
    {"frame": 450, "pos": (14000, 0, 1400)},
    {"frame": 500, "pos": (14000, 0, 1300)},
    {"frame": 640, "pos": (14000, 0, 1300)},
]

# Sphere Path (Shredder Output -> Full Downstream Flow)
SPHERE_PATH = [
    {"frame": 200, "pos": (7500,  300, 0)},     # Shredder Bottom
    {"frame": 220, "pos": (8500,  -100, 1000)},
    {"frame": 250, "pos": (10000, -100, 1400)},    # Screw Start
    {"frame": 350, "pos": (18000, -100, 1400)},    # Screw End
    {"frame": 400, "pos": (18500, -100, 2500)},    # Crusher Hopper
    {"frame": 450, "pos": (22000, -100, 1500)},    # Crusher Discharge
    {"frame": 500, "pos": (24600, 350, 1000)},  # Pocket Conv 2 Start (Y adjusted)
    {"frame": 600, "pos": (31000, 350, 3500)},  # Pocket Conv 2 Top
    {"frame": 650, "pos": (32000, 500, 2800)},  # Decline Conv Start (Y=500 for belt center)
    {"frame": 750, "pos": (38000, 500, 800)},   # Decline Conv End
    {"frame": 800, "pos": (39500, 300, 1600)},  # Ball Mill In (Y=300)
    {"frame": 900, "pos": (44500, 300, 1600)},  # Ball Mill Out
    {"frame": 950, "pos": (42000, 0, 2000)},    # Swan Neck 1 / Mag Sep
    {"frame": 1050, "pos": (55000, 0, 2000)},   # Secondary Process
    {"frame": 1150, "pos": (63000, 100, 1500)}, # Scrubber In
    {"frame": 1250, "pos": (68500, 100, 1000)}, # Scrubber Out
    {"frame": 1300, "pos": (70000, 0, 2400)},   # Centrifugal Concentrator
    {"frame": 1350, "pos": (70000, 0, 1000)},   # Final Product Bin
]

# ==============================================================================
# 3. ENGINE
# ==============================================================================

def run_anchored_simulation():
    # Set context to Object Mode
    if bpy.ops.object.mode_set.poll():
        bpy.ops.object.mode_set(mode='OBJECT')

    bpy.context.preferences.edit.keyframe_new_interpolation_type = 'LINEAR'

    # --- SETUP ANCHOR ---
    anchor_name = "PLANT_ANCHOR"
    anchor = bpy.data.objects.get(anchor_name)
    if not anchor:
        bpy.ops.object.empty_add(type='PLAIN_AXES', radius=5)
        anchor = bpy.context.active_object
        anchor.name = anchor_name

    # Apply global offset/rotation
    anchor.location = (OFFSET_X, OFFSET_Y, 0)
    anchor.rotation_euler[2] = math.radians(ROTATION_DEG)

    # --- CRITICAL FIX: PARENT STATIC PLANT PARTS ---
    # This finds ALL objects that don't have a parent yet and attaches them to the Anchor.
    # This ensures the Feeder, Shredder, and Conveyor meshes move with the anchor.
    for obj in bpy.data.objects:
        if obj != anchor and obj.parent is None:
            # Save current world matrix
            mat = obj.matrix_world.copy()
            # Parent to anchor
            obj.parent = anchor
            # Restore world matrix (keeps visual position while becoming a child)
            obj.matrix_world = mat
            # Now apply the Inverse Parent matrix so it sticks to the anchor's new pos
            obj.matrix_parent_inverse = anchor.matrix_world.inverted()

    # --- IDENTIFY ANIMATION TARGETS ---
    all_targets = []
    for obj in bpy.data.objects:
        if any(name in obj.name for name in PCB_NAMES):
            all_targets.append((obj, "PCB"))
        elif "Sphere" in obj.name or "Particle" in obj.name:
            all_targets.append((obj, "SPHERE"))

    random.seed(42)
    random.shuffle(all_targets)

    # --- ANIMATION LOOP ---
    bpy.context.scene.frame_end = 3000
    
    for i, (obj, p_type) in enumerate(all_targets):
        obj.animation_data_clear()
        
        # Ensure Moving Parts are also parented (Redundant safety check)
        if obj.parent != anchor:
            mat = obj.matrix_world.copy()
            obj.parent = anchor
            obj.matrix_world = mat
            obj.matrix_parent_inverse = anchor.matrix_world.inverted()
        
        stagger = START_FRAME + (i * STAGGER_GAP)
        path = []
        
        # --- LOGIC SWITCH ---
        if p_type == "PCB":
            if "Green_Shield_PCB" in obj.name:
                path = GREEN_SHIELD_PATH
                # Visible from start
                obj.hide_viewport = False; obj.hide_render = False
                obj.keyframe_insert(data_path="hide_viewport", frame=stagger)
                obj.keyframe_insert(data_path="hide_render", frame=stagger)
            else:
                path = PCB_PATH_SHORT
                # Visible from start
                obj.hide_viewport = False; obj.hide_render = False
                obj.keyframe_insert(data_path="hide_viewport", frame=stagger)
                obj.keyframe_insert(data_path="hide_render", frame=stagger)

            # Movement Logic
            for wp in path:
                target_f = wp["frame"] + stagger
                obj.location = (wp["pos"][0] * SCALE, wp["pos"][1] * SCALE, wp["pos"][2] * SCALE)
                obj.keyframe_insert(data_path="location", frame=target_f)
            
            # Vanish at end
            vanish_f = path[-1]["frame"] + stagger
            obj.keyframe_insert(data_path="hide_viewport", frame=vanish_f)
            obj.hide_viewport = True; obj.hide_render = True
            obj.keyframe_insert(data_path="hide_viewport", frame=vanish_f + 1)
            obj.keyframe_insert(data_path="hide_render", frame=vanish_f + 1)

        elif p_type == "SPHERE":
            path = SPHERE_PATH
            
            # Movement Logic
            for wp in path:
                target_f = wp["frame"] + stagger
                obj.location = (wp["pos"][0] * SCALE, wp["pos"][1] * SCALE, wp["pos"][2] * SCALE)
                obj.keyframe_insert(data_path="location", frame=target_f)
            
            # Invisible initially
            obj.hide_viewport = True; obj.hide_render = True
            obj.keyframe_insert(data_path="hide_viewport", frame=1)
            obj.keyframe_insert(data_path="hide_render", frame=1)
            
            # Appear at Shredder
            spawn_f = path[0]["frame"] + stagger
            obj.keyframe_insert(data_path="hide_viewport", frame=spawn_f - 1)
            obj.hide_viewport = False; obj.hide_render = False
            obj.keyframe_insert(data_path="hide_viewport", frame=spawn_f)
            obj.keyframe_insert(data_path="hide_render", frame=spawn_f)

        # Force Linear Interpolation (Pythonic way for Blender > 2.8)
        if obj.animation_data and obj.animation_data.action:
            action = obj.animation_data.action
            if hasattr(action, "fcurves"):
                for fc in action.fcurves:
                    for kp in fc.keyframe_points:
                        kp.interpolation = 'LINEAR'

    print("Simulation Complete: Plant Rotated, PCBs and Spheres Animated.")

run_anchored_simulation()