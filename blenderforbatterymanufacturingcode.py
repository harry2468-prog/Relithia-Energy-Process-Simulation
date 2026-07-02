import bpy
import json
import os
import math
import mathutils

# ==============================================================================
# CONFIGURATION
# ==============================================================================

JSON_PATH = os.path.expanduser("~/battery_factory_data.json")

# 1. FACTORY TRANSFORM
GLOBAL_MOVE_Y = -30
GLOBAL_MOVE_X = -12.0
GLOBAL_ROT_Z  = 45.0
S = 0.001  # Scale: mm to meters

# ------------------------------------------------------------------------------
# 2. INDIVIDUAL OBJECT ADJUSTMENTS (METERS) <--- EDIT THESE NUMBERS
# Format: (Side-to-Side, Forward-Back, Height/Up-Down)
# ------------------------------------------------------------------------------

# Adjustments for the PLATES (Start of line)
ADJUST_PLATE = (0.6, 0.9, 0.1) 

# Adjustments for the STACKED CELL (Middle of line)
ADJUST_STACK = (0.0, 0.0, 0.1)

# Adjustments for the BATTERIES (End of line)
ADJUST_BATT  = (1.5, 2.2, 1.5) 

# ------------------------------------------------------------------------------

# 3. TIMING (Frames)
NUM_PRODUCTS = 5       
TIME_GAP = 120         
DUR_FEED = 150         
DUR_PROCESS = 300      
DUR_FINISH = 600       
DUR_ROBOT = 150        

# ==============================================================================
# 1. SCENE PREPARATION
# ==============================================================================

def setup_scene():
    """Sets up the static factory environment."""
    for obj in bpy.data.objects:
        if obj.name.startswith("Sim_Instance"):
            bpy.data.objects.remove(obj, do_unlink=True)

    if "FACTORY_MASTER" in bpy.data.objects:
        anchor = bpy.data.objects["FACTORY_MASTER"]
        anchor.location = (0,0,0)
        anchor.rotation_euler = (0,0,0)
    else:
        bpy.ops.object.empty_add(type='ARROWS', radius=10)
        anchor = bpy.context.object
        anchor.name = "FACTORY_MASTER"

    for obj in bpy.data.objects:
        if obj == anchor: continue
        if obj.name.startswith("Sim_"): continue
        if obj.name.startswith("Source_"): continue
        
        if obj.parent is None:
            obj.parent = anchor
            obj.matrix_parent_inverse = anchor.matrix_world.inverted()

    anchor.location.y = GLOBAL_MOVE_Y
    anchor.location.x = GLOBAL_MOVE_X
    anchor.rotation_euler.z = math.radians(GLOBAL_ROT_Z)
    bpy.context.view_layer.update()
    return anchor

# ==============================================================================
# 2. SOURCE OBJECT CREATION
# ==============================================================================

def normalize_object(obj):
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    if obj.parent:
        mat = obj.matrix_world.copy()
        obj.parent = None
        obj.matrix_world = mat
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    obj.location = (0.0, 0.0, 0)
    obj.rotation_euler = (0, 0, 0)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    obj.hide_viewport = True
    obj.hide_render = True

def find_and_join_parts(target_name, search_terms, blacklist=[]):
    bpy.ops.object.select_all(action='DESELECT')
    objects_to_join = []
    
    for obj in bpy.data.objects:
        if any(b in obj.name for b in blacklist): continue
        for term in search_terms:
            if term in obj.name and "Source_" not in obj.name and "Sim_" not in obj.name:
                objects_to_join.append(obj)
                break
    
    if not objects_to_join:
        print(f"Warning: No parts found for {target_name}")
        return None

    ctx = bpy.context.copy()
    ctx['active_object'] = objects_to_join[0]
    ctx['selected_editable_objects'] = objects_to_join
    for o in objects_to_join: o.select_set(True)
    bpy.context.view_layer.objects.active = objects_to_join[0]
    bpy.ops.object.join()
    
    final_obj = bpy.context.active_object
    final_obj.name = f"Source_{target_name}"
    normalize_object(final_obj)
    return final_obj

def prepare_sources():
    sources = {}
    ignore = ["Pipe", "Cyc", "Tube", "Hose", "Exchanger", "Tank"]

    sources["AL"] = find_and_join_parts("AL_Plate", ["Silver_Edge", "Black_Center"], ignore)
    sources["CU"] = find_and_join_parts("CU_Plate", ["Copper_Edge", "Graphite_Center"], ignore)
    sources["STACK"] = find_and_join_parts("Stacked_Cell", ["Anode_", "Cathode_", "Sep_", "Tab_"], ignore)
    sources["BATT"] = find_and_join_parts("Battery_Full", ["Battery_Body", "Battery_Cap", "Pos_", "Neg_", "Label_", "Gear_", "Leaf_"], ignore)
    sources["ROBO1"] = find_and_join_parts("Robot",["Shoulder_Cap_L", "Lower_Arm_Main","Elbow_Joint", "Forearm_Rib", "Cable_1", "Cable_2", "Cable_3", "Cable_4", "Clamp_1", "Clamp_2", "Forearm", "Wrist_1","Wrist_2","Counterweight","Gripper_Base","Finger_L1","Finger_L2","Finger_R1","Finger_R2"],ignore)
    sources["ROBO2"] = find_and_join_parts("Robot",["Shoulder_Cap_L001", "Lower_Arm_Main001","Elbow_Joint001", "Forearm_Rib001", "Cable_006", "Cable_007", "Cable_008", "Cable_009", "Clamp_001", "Clamp_002", "Forearm001", "Wrist_001","Wrist_002","Counterweight001","Gripper_Base001","Finger_L001","Finger_L002","Finger_R001","Finger_R002"],ignore)

    return sources

# ==============================================================================
# 3. ANIMATION
# ==============================================================================

def get_loc(coords_mm, anchor, adjustment_tuple):
    # Base Position from JSON
    base = mathutils.Vector((coords_mm[0]*S, coords_mm[1]*S, coords_mm[2]*S))
    
    # Add the specific adjustment (X, Y, Z)
    offset = mathutils.Vector(adjustment_tuple)
    
    # Apply Factory Rotation
    return anchor.matrix_world @ (base + offset)

def get_rot(deg_z, anchor):
    return (0, 0, math.radians(deg_z) + anchor.rotation_euler.z)

def keyframe(obj, frame, loc, rot, visible):
    if not obj: return
    obj.location = loc
    obj.rotation_euler = rot
    obj.keyframe_insert("location", frame=frame)
    obj.keyframe_insert("rotation_euler", frame=frame)
    obj.hide_viewport = not visible
    obj.hide_render = not visible
    obj.keyframe_insert("hide_viewport", frame=frame)
    obj.keyframe_insert("hide_render", frame=frame)

def animate_relay_race(run_id, start_frame, wp, anchor, sources):
    
    def spawn(key):
        src = sources.get(key)
        if not src: return None
        new_obj = src.copy()
        new_obj.data = src.data.copy()
        new_obj.animation_data_clear()
        new_obj.name = f"Sim_{key}_{run_id}"
        bpy.context.collection.objects.link(new_obj)
        return new_obj

    p_al = spawn("AL")
    p_cu = spawn("CU")
    stack = spawn("STACK")
   

    t0 = start_frame
    t1 = t0 + DUR_FEED
    t2 = t1 + DUR_PROCESS
    t3 = t2 + DUR_FINISH
    t4 = t3 + DUR_ROBOT

    # Helper that accepts the specific adjustment
    loc = lambda k, adj: get_loc(wp[k], anchor, adj)
    rot = lambda z: get_rot(z, anchor)

    # --- LEG 1: PLATES (Uses ADJUST_PLATE) ---
    if p_al and p_cu:
        adj = ADJUST_PLATE
        keyframe(p_al, t0, loc("start_anode", adj), rot(0), True)
        keyframe(p_cu, t0, loc("start_cathode", adj), rot(0), True)
        
        keyframe(p_al, t0 + (DUR_FEED/2), loc("slitting_anode", adj), rot(0), True)
        keyframe(p_cu, t0 + (DUR_FEED/2), loc("slitting_cathode", adj), rot(0), True)
        
        keyframe(p_al, t1, loc("stacking_machine", adj), rot(0), True)
        keyframe(p_cu, t1, loc("stacking_machine", adj), rot(0), True)
        
        keyframe(p_al, t1+1, loc("stacking_machine", adj), rot(0), False)
        keyframe(p_cu, t1+1, loc("stacking_machine", adj), rot(0), False)

    # --- LEG 2: STACK (Uses ADJUST_STACK) ---
    if stack:
        adj = ADJUST_STACK
        keyframe(stack, t0, loc("stacking_machine", adj), rot(90), False)
        
        keyframe(stack, t1, loc("stacking_machine", adj), rot(90), False)
        keyframe(stack, t1+1, loc("stacking_machine", adj), rot(90), True)
        
        keyframe(stack, t1 + (DUR_PROCESS*0.3), loc("hot_press", adj), rot(90), True)
        keyframe(stack, t1 + (DUR_PROCESS*0.6), loc("ultrasonic", adj), rot(90), True)
        keyframe(stack, t1 + (DUR_PROCESS*0.8), loc("laser_weld", adj), rot(90), True)
        
        keyframe(stack, t2, loc("sealing", adj), rot(90), True)
        keyframe(stack, t2+1, loc("sealing", adj), rot(90), False)

    # --- LEG 3: BATTERY (Uses ADJUST_BATT) ---
    if batt:
        adj = ADJUST_BATT 
        
        keyframe(batt, t0, loc("sealing", adj), rot(0), False)
        
        keyframe(batt, t2, loc("sealing", adj), rot(0), False)
        keyframe(batt, t2+1, loc("sealing", adj), rot(0), True)
        
        keyframe(batt, t2 + 100, loc("drying", adj), rot(0), True)
        keyframe(batt, t2 + 200, loc("filling", adj), rot(0), True)
        keyframe(batt, t2 + 300, loc("formation", adj), rot(0), True)
        keyframe(batt, t2 + 350, loc("grading", adj), rot(0), True)
        keyframe(batt, t2 + 450, loc("charging", adj), rot(0), True)
        
        keyframe(batt, t3, loc("robot_pickup", adj), rot(0), True)
        
        # Robot Motion
        keyframe(batt, t3 + 30, loc("robot_lift", adj), rot(0), True)
        swing_rot = (0, math.radians(180), rot(90)[2])
        
        keyframe(batt, t3 + 100, loc("robot_swing", adj), swing_rot, True)
        keyframe(batt, t4, loc("robot_drop", adj), swing_rot, True)

# ==============================================================================
# 4. EXECUTION
# ==============================================================================

def run_simulation():
    if not os.path.exists(JSON_PATH):
        print(f"Error: JSON file not found at {JSON_PATH}")
        return
        
    with open(JSON_PATH, 'r') as f:
        data = json.load(f)
    wp = data["waypoints"]

    # ==========================================================================
    # --- MODIFICATION: CONTROL DISTANCE HERE ---
    # ==========================================================================
    
    # Positive Value = INCREASE travel distance
    # Negative Value = DECREASE travel distance
    # Unit: Millimeters
    EXTRA_DISTANCE_MM = 5000.0 
    
    # 1. Move the end destination (Stacking Machine)
    if "stacking_machine" in wp:
        wp["stacking_machine"][0] += EXTRA_DISTANCE_MM

    # 2. Adjust intermediate points so they stretch evenly
    if "slitting_anode" in wp:
        wp["slitting_anode"][0] += (EXTRA_DISTANCE_MM / 2)
    if "slitting_cathode" in wp:
        wp["slitting_cathode"][0] += (EXTRA_DISTANCE_MM / 2)

    # ==========================================================================

    print("--- 1. Setting up Factory ---")
    anchor = setup_scene()
    
    print("--- 2. Preparing Relay Runners ---")
    sources = prepare_sources()
    
    print("--- 3. Running Race ---")
    for i in range(NUM_PRODUCTS):
        start_frame = 1 + (i * TIME_GAP)
        animate_relay_race(i, start_frame, wp, anchor, sources)
    
    bpy.context.scene.frame_end = 1 + (NUM_PRODUCTS * TIME_GAP) + DUR_FEED + DUR_PROCESS + DUR_FINISH + DUR_ROBOT
    bpy.context.scene.frame_start = 1
    
    print("--- SIMULATION READY ---")

if __name__ == "__main__":
    run_simulation()