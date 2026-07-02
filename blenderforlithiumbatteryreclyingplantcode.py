import bpy
import random
import math

# ==============================================================================
# 1. SETTINGS & ANCHOR TRANSFORM
# ==============================================================================
SCALE = 0.001          # mm to meters
STAGGER_GAP = 12       # Delay between objects
START_FRAME = 1        

# ASSEMBLY TRANSFORM (Maintained)
OFFSET_X = -50.0       
OFFSET_Y = -40.0       
ROTATION_DEG = 45.0    

# NAMES OF THE SPECIAL SCHEMATIC PARTICLES TO BE TREATED AS SHREDDED
SCHEMATIC_NAMES = (
    "Battery_Diagram_Fused", 
    "LiI_Battery_Fused", 
    "JellyRoll_Battery_Fused"
)

# ==============================================================================
# 2. PATH DEFINITIONS (Machine Local Space in mm) - MAINTAINED
# ==============================================================================
BASE_PATH = [
    {"frame": 0,   "pos": (-3000, -500, 650)}, # Start on Feeder
    {"frame": 100, "pos": (1000,  -500, 650)}, # Edge of Feeder
    {"frame": 150, "pos": (4000,  -500,  600)}, # Drop onto main conveyor
    {"frame": 250, "pos": (6300,  -500,  600)}, # Reaching Shredder Mouth
]

WHOLE_EXTENSION = [{"frame": 280, "pos": (7200, -500,  200)}]

# The path these three schematics will now follow
PARTICLE_EXTENSION = [
    {"frame": 300, "pos": (7200, -500,  -100)},   
    {"frame": 350, "pos": (12000, 350, -100)},  
    {"frame": 470, "pos": (17800, 350, -100)},  
    {"frame": 540, "pos": (18500, 350, -500)},
    {"frame": 764, "pos": (20740, 100, -200)},
    {"frame": 954, "pos": (22640, 100, 500)},
    {"frame": 1254, "pos": (25640, 100, 1319)}, 
    {"frame": 1490, "pos": (26000, 100, -200)}, 
    {"frame": 1634, "pos": (26437, 100, -319)}, 
]

SPHERE_EXTENSION = [
    {"frame": 300, "pos": (7200, -500,  200)},   
    {"frame": 350, "pos": (12000, 350, 950)},  
    {"frame": 470, "pos": (17800, 350, 950)},  
    {"frame": 540, "pos": (18500, 350, 350)},
    {"frame": 640, "pos": (19500, 350, 350)},
    {"frame": 730, "pos": (20400, 350, 350)},
    {"frame": 764, "pos": (20740, 350, 500)},
    {"frame": 884, "pos": (21940, 350, 1150)},
    {"frame": 954, "pos": (22640, 350, 1579)},
    {"frame": 1390, "pos": (27000, -200, 2219)},
    {"frame": 1432, "pos": (27000, -250, 1600)},  
    {"frame": 1812, "pos": (30800, -250, 2800)},
    {"frame": 1832, "pos": (30800, 150, 2900)},
    {"frame": 1902, "pos": (31500, 150, 3100)},  
    {"frame": 2502, "pos": (37500, 150, 3100)},
    {"frame": 3452, "pos": (47000, 250, 4180)},
    {"frame": 4052, "pos": (53000, 250, 4180)},
    {"frame": 4652, "pos": (59000, 250, 1000)},
    {"frame": 4770, "pos": (60500, 250, 1000)}, 
    {"frame": 5133, "pos": (64125, 250, 2691)},
    {"frame": 5283, "pos": (65625, 250, 2691)}, 
    {"frame": 5358, "pos": (66375, 250, 3241)},
    {"frame": 5621, "pos": (69000, 250, 2900)},
    {"frame": 5771, "pos": (70500, 150, 2900)},  
    {"frame": 6179, "pos": (74578, 150, 1300)},
    {"frame": 6329, "pos": (76078, 150, 1300)},
    {"frame": 6621, "pos": (79000, 100, 1100)},
    {"frame": 7121, "pos": (86000, 350, 1100)},
    {"frame": 7621, "pos": (91000, 350, 1100)},
    {"frame": 8221, "pos": (97000, 350, 1100)},
    {"frame": 8881, "pos": (103600, 350, 2900)},
]

# ==============================================================================
# 3. ENGINE
# ==============================================================================

def run_anchored_simulation():
    if bpy.ops.object.mode_set.poll():
        bpy.ops.object.mode_set(mode='OBJECT')

    # Force Linear Interpolation as global preference for new keys
    bpy.context.preferences.edit.keyframe_new_interpolation_type = 'LINEAR'

    # --- SETUP ANCHOR ---
    anchor_name = "PLANT_ANCHOR"
    anchor = bpy.data.objects.get(anchor_name)
    if not anchor:
        bpy.ops.object.empty_add(type='PLAIN_AXES', radius=5)
        anchor = bpy.context.active_object
        anchor.name = anchor_name

    anchor.location = (OFFSET_X, OFFSET_Y, 0)
    anchor.rotation_euler[2] = math.radians(ROTATION_DEG)

    # Parent MACHINERY to anchor (Excluding particles)
    for obj in bpy.data.objects:
        is_particle = obj.name.startswith(("Anim_", "Fused_")) or obj.name in SCHEMATIC_NAMES
        if obj.name != anchor_name and not is_particle:
            if obj.parent is None:
                mw = obj.matrix_world.copy()
                obj.parent = anchor
                obj.matrix_parent_inverse = anchor.matrix_world.inverted()
                obj.matrix_world = mw

    # --- PROCESS PARTICLES ---
    bpy.context.scene.frame_end = 3000
    
    # Collect all targets including the three new schematic names
    targets = [obj for obj in bpy.data.objects if 
               obj.name.startswith(("Anim_", "Fused_")) or 
               obj.name in SCHEMATIC_NAMES]
               
    random.seed(42)
    random.shuffle(targets)

    for i, obj in enumerate(targets):
        obj.animation_data_clear()
        
        # Parent to anchor to align coordinates
        mw = obj.matrix_world.copy()
        obj.parent = anchor
        obj.matrix_parent_inverse = anchor.matrix_world.inverted()
        obj.matrix_world = mw
        
        path = BASE_PATH.copy()
        is_whole = False
        
        # CATEGORY LOGIC
        if obj.name.startswith("Anim_Particle"):
            # Black/Silver/Brown Spheres (Scrubber Path)
            path.extend(SPHERE_EXTENSION)
        elif obj.name.startswith("Fused_") or obj.name in SCHEMATIC_NAMES:
            # Shredded cells AND the 3 requested Schematics (Pneumatic Path)
            path.extend(PARTICLE_EXTENSION)
        else:
            # Whole Batteries (Smartphone, Samsung, etc. - Stop at Shredder)
            path.extend(WHOLE_EXTENSION)
            is_whole = True
            
        stagger = START_FRAME + (i * STAGGER_GAP)
        
        # Keyframe location
        for wp in path:
            target_f = wp["frame"] + stagger
            obj.location = (wp["pos"][0] * SCALE, wp["pos"][1] * SCALE, wp["pos"][2] * SCALE)
            obj.keyframe_insert(data_path="location", frame=target_f)

        # Visibility logic
        if is_whole:
            obj.hide_viewport = False; obj.hide_render = False
            obj.keyframe_insert(data_path="hide_viewport", frame=stagger)
            vanish_f = WHOLE_EXTENSION[-1]["frame"] + stagger
            obj.keyframe_insert(data_path="hide_viewport", frame=vanish_f)
            obj.hide_viewport = True; obj.hide_render = True
            obj.keyframe_insert(data_path="hide_viewport", frame=vanish_f + 1)
        else:
            # Shredded items / Schematics spawn at frame 300
            obj.hide_viewport = True; obj.hide_render = True
            obj.keyframe_insert(data_path="hide_viewport", frame=1)
            spawn_f = 300 + stagger
            obj.keyframe_insert(data_path="hide_viewport", frame=spawn_f - 1)
            obj.hide_viewport = False; obj.hide_render = False
            obj.keyframe_insert(data_path="hide_viewport", frame=spawn_f)

        # FIX: Robust attribute check for linear interpolation
        if obj.animation_data and obj.animation_data.action:
            action = obj.animation_data.action
            if hasattr(action, "fcurves"):
                for fc in action.fcurves:
                    for kp in fc.keyframe_points:
                        kp.interpolation = 'LINEAR'

    print(f"Integration Complete: {len(targets)} particles integrated into the Shredder-Pneumatic flow.")

run_anchored_simulation()