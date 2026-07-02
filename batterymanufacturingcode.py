import FreeCAD as App
import FreeCADGui as Gui
import Part
import math

# ==========================================
# 1. PARAMETERS & COLORS
# ==========================================

width = 3600.0
depth = 3000.0
tank_straight_h = 2700.0
hopper_cone_h = 1500.0
wall_thickness = 30.0

frame_tube_size = 150.0
fork_pocket_w = 600.0
fork_pocket_h = 240.0
outlet_size = 600.0

#Inclined Conveyor belt
belt_width = 800.0
frame_width = 1000.0
bottom_len = 1500.0
incline_len = 4000.0
top_len = 1500.0
incline_angle = 25.0
leg_base_height = 800.0  # Height of the lower section from floor


col_plastic = (0.9, 0.9, 0.95)
col_steel = (0.75, 0.75, 0.78)
col_handle = (0.1, 0.1, 0.1)
col_lid = (0.9, 0.6, 0.1)
col_pipe_yellow = (1.0, 0.8, 0.0)
col_red = (0.85, 0.1, 0.15)
col_black = (0.1, 0.1, 0.1)
col_white = (0.9, 0.9, 0.9)
col_yellow = (1.0, 0.8, 0.0)
col_metal = (0.6, 0.6, 0.65)
col_steel_grey = (0.80, 0.80, 0.82)
col_liner_red = (0.75, 0.15, 0.15)



def ensure_document():
    doc = App.ActiveDocument
    if not doc:
        doc = App.newDocument("IBCHopper")
    return doc

# ==========================================
# 2. HELPER FUNCTIONS
# ==========================================

def make_box(doc, name, l, w, h, x, y, z, color, offset=(0,0,0), rotation_angle=0, rotation_axis=App.Vector(0,0,1)):
    shape = Part.makeBox(l, w, h)
    if rotation_angle != 0:
        shape.rotate(App.Vector(0,0,0), rotation_axis, rotation_angle)
    shape.translate(App.Vector(x + offset[0], y + offset[1], z + offset[2]))
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = shape
    obj.ViewObject.ShapeColor = color
    return obj

def make_cylinder(doc, name, radius, height, x, y, z, color, offset=(0,0,0), axis=App.Vector(0,0,1)):
    shape = Part.makeCylinder(radius, height)
    if axis == App.Vector(0,1,0): # Y axis
        shape.rotate(App.Vector(0,0,0), App.Vector(1,0,0), -90)
    elif axis == App.Vector(1,0,0): # X axis
        shape.rotate(App.Vector(0,0,0), App.Vector(0,1,0), 90)
    shape.translate(App.Vector(x + offset[0], y + offset[1], z + offset[2]))
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = shape
    obj.ViewObject.ShapeColor = color
    return obj

# ==============================================================================
# MAIN DRAWING FUNCTION FOR THE HOPPER
# ==============================================================================
 
def make_tank_shape(doc, name, offset=(0,0,0)):
    # --- A. Build Outer Shape ---
    tank_top = Part.makeBox(width, depth, tank_straight_h)
    tank_top.translate(App.Vector(0, 0, hopper_cone_h))
    
    # Ribs
    rib_depth = 45.0
    rib_width = 240.0
    ribs = []
    num_ribs = 3
    spacing = width / num_ribs
    
    for i in range(num_ribs):
        r1 = Part.makeBox(rib_width, rib_depth * 2, tank_straight_h)
        r1.translate(App.Vector((i * spacing) + (spacing/2) - (rib_width/2), -rib_depth, hopper_cone_h))
        ribs.append(r1)
        r2 = Part.makeBox(rib_width, rib_depth * 2, tank_straight_h)
        r2.translate(App.Vector((i * spacing) + (spacing/2) - (rib_width/2), depth - rib_depth, hopper_cone_h))
        ribs.append(r2)
        
    if ribs:
        rib_compound = Part.makeCompound(ribs)
        tank_top = tank_top.cut(rib_compound)

    # Outer Cone
    p1 = App.Vector(0,0,hopper_cone_h)
    p2 = App.Vector(width,0,hopper_cone_h)
    p3 = App.Vector(width,depth,hopper_cone_h)
    p4 = App.Vector(0,depth,hopper_cone_h)
    wire_top = Part.makePolygon([p1, p2, p3, p4, p1])
    
    out_x = (width - outlet_size)/2
    out_y = (depth - outlet_size)/2
    p1b = App.Vector(out_x, out_y, 0)
    p2b = App.Vector(out_x + outlet_size, out_y, 0)
    p3b = App.Vector(out_x + outlet_size, out_y + outlet_size, 0)
    p4b = App.Vector(out_x, out_y + outlet_size, 0)
    wire_bot = Part.makePolygon([p1b, p2b, p3b, p4b, p1b])
    
    outer_cone = Part.makeLoft([wire_bot, wire_top], True)
    outer_shape = tank_top.fuse(outer_cone)

    # --- B. Build Inner Shape (Negative Volume) ---
    inner_w = width - (2 * wall_thickness)
    inner_d = depth - (2 * wall_thickness)
    inner_box = Part.makeBox(inner_w, inner_d, tank_straight_h + 30) 
    inner_box.translate(App.Vector(wall_thickness, wall_thickness, hopper_cone_h))
    
    # Inner Cone Wire Top
    pi1 = App.Vector(wall_thickness, wall_thickness, hopper_cone_h)
    pi2 = App.Vector(width-wall_thickness, wall_thickness, hopper_cone_h)
    pi3 = App.Vector(width-wall_thickness, depth-wall_thickness, hopper_cone_h)
    pi4 = App.Vector(wall_thickness, depth-wall_thickness, hopper_cone_h)
    wire_inner_top = Part.makePolygon([pi1, pi2, pi3, pi4, pi1])
    
    # Inner Cone Wire Bot (Matches outlet)
    wire_inner_bot = Part.makePolygon([p1b, p2b, p3b, p4b, p1b])
    
    inner_cone = Part.makeLoft([wire_inner_bot, wire_inner_top], True)
    inner_shape = inner_box.fuse(inner_cone)
    
    # --- C. Final Cut ---
    tank_final = outer_shape.cut(inner_shape)
    tank_final.translate(App.Vector(offset[0], offset[1], offset[2]))
    
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = tank_final
    obj.ViewObject.ShapeColor = col_plastic
    obj.ViewObject.Transparency = 40
    return obj

def make_chute_shape(doc, name, offset=(0,0,0)):
    out_x = (width - outlet_size)/2
    out_y = (depth - outlet_size)/2
    
    chute = Part.makeBox(outlet_size, outlet_size + 150, 300)
    chute.rotate(App.Vector(outlet_size/2,0,0), App.Vector(1,0,0), 30)
    chute.translate(App.Vector(out_x, out_y - 150, -150))
    
    inner = Part.makeBox(outlet_size - 18, outlet_size + 150, 300)
    inner.rotate(App.Vector(outlet_size/2,0,0), App.Vector(1,0,0), 90)
    inner.translate(App.Vector(out_x + 9, out_y - 150, -150 + 9))
    
    final = chute.cut(inner)
    final.translate(App.Vector(offset[0], offset[1], offset[2]))
    
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = final
    obj.ViewObject.ShapeColor = col_steel
    return obj

# ==========================================
# 3. BUILDER
# ==========================================

def build_ibc_hopper(doc, offset=(0,0,0)):
    # --- 1. PLASTIC TANK ---
    make_tank_shape(doc, "IBC_Tank", offset)
    
    # --- 2. FRAME ---
    leg_h = tank_straight_h + hopper_cone_h
    gap = 15.0
    rim_z = leg_h - frame_tube_size
    pocket_z = 300.0
    
    # Legs
    make_box(doc, "Leg_FL", frame_tube_size, frame_tube_size, leg_h + 300, -frame_tube_size-gap, -frame_tube_size-gap, 0, col_steel, offset)
    make_box(doc, "Leg_FR", frame_tube_size, frame_tube_size, leg_h + 300, width+gap, -frame_tube_size-gap, 0, col_steel, offset)
    make_box(doc, "Leg_BR", frame_tube_size, frame_tube_size, leg_h + 300, width+gap, depth+gap, 0, col_steel, offset)
    make_box(doc, "Leg_BL", frame_tube_size, frame_tube_size, leg_h + 300, -frame_tube_size-gap, depth+gap, 0, col_steel, offset)
    
    # Rim
    make_box(doc, "Rim_F", width + 2*gap + 2*frame_tube_size, frame_tube_size, frame_tube_size, -frame_tube_size-gap, -frame_tube_size-gap, rim_z, col_steel, offset)
    make_box(doc, "Rim_B", width + 2*gap + 2*frame_tube_size, frame_tube_size, frame_tube_size, -frame_tube_size-gap, depth+gap, rim_z, col_steel, offset)
    make_box(doc, "Rim_L", frame_tube_size, depth + 2*gap, frame_tube_size, -frame_tube_size-gap, -gap, rim_z, col_steel, offset)
    make_box(doc, "Rim_R", frame_tube_size, depth + 2*gap, frame_tube_size, width+gap, -gap, rim_z, col_steel, offset)
    
    # Pockets (Constructed from plates)
    def build_pocket(y_pos):
        plen = width + 600
        x_st = -300
        th = 15.0
        make_box(doc, f"Pkt_B_{y_pos}", plen, fork_pocket_w, th, x_st, y_pos, pocket_z, col_steel, offset)
        make_box(doc, f"Pkt_T_{y_pos}", plen, fork_pocket_w, th, x_st, y_pos, pocket_z + fork_pocket_h - th, col_steel, offset)
        make_box(doc, f"Pkt_S1_{y_pos}", plen, th, fork_pocket_h, x_st, y_pos, pocket_z, col_steel, offset)
        make_box(doc, f"Pkt_S2_{y_pos}", plen, th, fork_pocket_h, x_st, y_pos + fork_pocket_w - th, pocket_z, col_steel, offset)

    build_pocket(depth/2 - fork_pocket_w - 150)
    build_pocket(depth/2 + 150)
    
    make_box(doc, "Beam_1", frame_tube_size, depth, frame_tube_size, width/4, 0, pocket_z + fork_pocket_h, col_steel, offset)
    make_box(doc, "Beam_2", frame_tube_size, depth, frame_tube_size, width*0.75, 0, pocket_z + fork_pocket_h, col_steel, offset)

    # --- 3. DETAILS ---
    make_box(doc, "Lid", width, depth, 60, 0, 0, tank_straight_h + hopper_cone_h, col_lid, offset)
    make_chute_shape(doc, "Chute", offset)
    
    out_x = (width - outlet_size)/2
    out_y = (depth - outlet_size)/2
    make_box(doc, "Slide", outlet_size + 120, 30, outlet_size + 120, out_x - 60, out_y - 60, 0, col_steel, offset)
    
    # Handle
    pivot_x = -frame_tube_size
    pivot_y = depth/2
    pivot_z = hopper_cone_h * 0.7
    handle_len = 2700.0
    
    make_box(doc, "Handle", 60, 60, handle_len, pivot_x, pivot_y, pivot_z, col_steel, offset, rotation_angle=-75, rotation_axis=App.Vector(0,1,0))
    
    grip_x = pivot_x + (handle_len * math.sin(math.radians(75)))
    grip_z = pivot_z + (handle_len * math.cos(math.radians(75)))
    make_cylinder(doc, "Grip", 54, 450, grip_x, pivot_y - 225, grip_z, col_handle, offset, axis=App.Vector(0,1,0))
    make_box(doc, "Link", 60, 30, 1200, out_x + outlet_size/2, out_y - 60, 0, col_steel, offset)


# ==============================================================================
# MAIN DRAWING FUNCTION FOR THE RECTANGULAR PIPES FOR PNEUMATIC CONVEYING
# ==============================================================================
# --- Rectangular Pipe ---
def create_rectangular_pipe(name, x, y, z, length, width, height, thickness=40):
    # Outer box
    outer = Part.makeBox(length, width, height)
    # Inner box for hollowing (slightly longer to ensure clean cut at ends)
    inner = Part.makeBox(length + 20, width - 2*thickness, height - 2*thickness)
    inner.translate(App.Vector(-10, thickness, thickness))
    
    shape = outer.cut(inner)
    obj = App.ActiveDocument.addObject("Part::Feature", name)
    obj.Shape = shape
    obj.Placement = App.Placement(App.Vector(x, y, z),App.Rotation(App.Vector(0,1,0), -22.5))
    obj.ViewObject.ShapeColor = (0.7, 0.7, 0.7) # Metallic Grey
    return obj

# ==============================================================================
# MAIN DRAWING FUNCTION  FOR THE MIXING MACHINE(COORDINATES UNCHANGED)
# ==============================================================================

def draw_industrial_mixer(doc, offset_coords=(0,0,0)):
    # Colors
    col_white   = (0.90, 0.90, 0.90)
    col_steel   = (0.75, 0.75, 0.77)
    col_dark    = (0.20, 0.20, 0.20)
    col_orange  = (0.90, 0.40, 0.00)
    col_grey    = (0.60, 0.60, 0.60)
    col_red     = (0.80, 0.10, 0.10)

    # Dimensions
    base_w = 2400
    base_d = 3000
    col_w = 1800
    col_d = 1200
    col_h = 4200
    
    # --------------------------------------------------------------------------
    # 1. BASE AND WHEELS
    # --------------------------------------------------------------------------
    # Left Leg
    make_box(doc, "Base_Leg_L", 450, base_d, 300, 0, 0, 240, col_white, offset_coords)
    # Right Leg
    make_box(doc, "Base_Leg_R", 450, base_d, 300, base_w - 450, 0, 240, col_white, offset_coords)
    # Back Connection
    make_box(doc, "Base_Back", base_w, 900, 300, 0, 0, 240, col_white, offset_coords)

    # Wheels (Castors)
    wheel_positions = [
        (225, 300), (225, base_d-300),       # Left
        (base_w-225, 300), (base_w-225, base_d-300) # Right
    ]
    
    for i, (wx, wy) in enumerate(wheel_positions):
        make_cylinder(doc, f"Wheel_{i}", 120, 120, wx - 60, wy, 120, col_orange, offset_coords, axis=App.Vector(0,1,0))
        make_box(doc, f"Wheel_Mount_{i}", 180, 180, 120, wx - 90, wy - 90, 120, col_dark, offset_coords)

    # --------------------------------------------------------------------------
    # 2. MAIN COLUMN AND LIFT
    # --------------------------------------------------------------------------
    col_x_start = (base_w - col_w) / 2
    
    # Main Column
    make_box(doc, "Column_Main", col_w, col_d, col_h, col_x_start, 0, 180, col_white, offset_coords)
    
    # Tracks
    make_box(doc, "Column_Track_L", 150, 60, col_h - 600, col_x_start + 150, col_d, 200, col_steel, offset_coords)
    make_box(doc, "Column_Track_R", 150, 60, col_h - 600, col_x_start + col_w - 300, col_d, 600, col_steel, offset_coords)

    # --------------------------------------------------------------------------
    # 3. TOP HEAD
    # --------------------------------------------------------------------------
    head_w = col_w + 300
    head_d = 3300
    head_h = 1500
    head_z = 540 + col_h
    
    make_box(doc, "Head_Main", head_w, head_d, head_h, col_x_start - 150, 0, head_z, col_white, offset_coords)
    make_box(doc, "Head_Top_Detail", head_w - 300, head_d - 300, 150, col_x_start, 150, head_z + head_h, col_white, offset_coords)
    make_cylinder(doc, "Motor_Top", 360, 900, base_w/2, 600, head_z + head_h + 150, col_steel, offset_coords)

    # Pistons
    make_cylinder(doc, "Piston_L", 90, 2400, col_x_start - 90, 600, head_z - 2400, col_steel, offset_coords)
    make_cylinder(doc, "Piston_R", 90, 2400, col_x_start + col_w + 90, 600, head_z - 2400, col_steel, offset_coords)

    # --------------------------------------------------------------------------
    # 4. CONTROL PANEL
    # --------------------------------------------------------------------------
    panel_w = 600
    panel_d = 1500
    panel_h = 2100
    panel_z = 1800
    
    make_box(doc, "Control_Panel", panel_w, panel_d, panel_h, col_x_start - panel_w, 150, panel_z, col_grey, offset_coords)
             
    # Buttons
    for r in range(4):
        for c in range(3):
            bx = col_x_start - panel_w + 30
            by = 300 + (c * 180)
            bz = panel_z + 1800 - (r * 180)
            make_cylinder(doc, f"Button_{r}_{c}", 45, 30, bx, by, bz, col_red, offset_coords, axis=App.Vector(1,0,0))

    # --------------------------------------------------------------------------
    # 5. MIXING SHAFTS
    # --------------------------------------------------------------------------
    shaft_center_x = base_w / 2
    shaft_center_y = head_d - 1050 
    shaft_z_start = head_z
    shaft_len = 2700
    
    # Center Shaft
    make_cylinder(doc, "Shaft_Center", 75, shaft_len, shaft_center_x, shaft_center_y, shaft_z_start - shaft_len, col_steel, offset_coords)
    make_cylinder(doc, "Blade_Disc", 240, 30, shaft_center_x, shaft_center_y, shaft_z_start - shaft_len, col_steel, offset_coords)
                  
    # Anchor Frame
    make_box(doc, "Anchor_Top", 1200, 120, 90, shaft_center_x - 600, shaft_center_y - 60, shaft_z_start - 300, col_steel, offset_coords)
    make_box(doc, "Anchor_Arm_L", 90, 90, shaft_len - 300, shaft_center_x - 600, shaft_center_y - 45, shaft_z_start - shaft_len, col_steel, offset_coords)
    make_box(doc, "Anchor_Arm_R", 90, 90, shaft_len - 300, shaft_center_x + 510, shaft_center_y - 45, shaft_z_start - shaft_len, col_steel, offset_coords)
    make_box(doc, "Scraper_Blade_1", 90, 300, 300, shaft_center_x - 600, shaft_center_y - 150, shaft_z_start - shaft_len + 300, col_white, offset_coords, rotation_angle=45, rotation_axis=App.Vector(0,0,1))

    # --------------------------------------------------------------------------
    # 6. TANK
    # --------------------------------------------------------------------------
    tank_rad = 900
    tank_h = 2250
    tank_z = 540
    
    make_cylinder(doc, "Tank_Body", tank_rad, tank_h, shaft_center_x, shaft_center_y, tank_z, col_steel, offset_coords)
    make_cylinder(doc, "Tank_Rim", tank_rad + 60, 90, shaft_center_x, shaft_center_y, tank_z + tank_h - 90, col_steel, offset_coords)
    make_box(doc, "Tank_Handle", 600, 120, 45, shaft_center_x - 100, shaft_center_y + tank_rad, tank_z + 1500, col_steel, offset_coords)

    # Tank Wheels
    tank_wheel_z = tank_z - 120
    make_cylinder(doc, "Tank_Wheel_1", 90, 90, shaft_center_x - 600, shaft_center_y - 600, tank_wheel_z, col_dark, offset_coords, axis=App.Vector(0,1,0))
    make_cylinder(doc, "Tank_Wheel_2", 90, 90, shaft_center_x + 600, shaft_center_y - 600, tank_wheel_z, col_dark, offset_coords, axis=App.Vector(0,1,0))
    make_cylinder(doc, "Tank_Wheel_3", 90, 90, shaft_center_x, shaft_center_y + 750, tank_wheel_z, col_dark, offset_coords, axis=App.Vector(0,1,0))



# ==============================================================================
# MAIN DRAWING FUNCTION FOR THE COATING VESSEL
# ==============================================================================

def draw_coating_line(doc, offset_coords=(0,0,0)):
    # Colors
    col_grey_light = (0.85, 0.85, 0.85)
    col_grey_dark  = (0.40, 0.40, 0.40)
    col_blue       = (0.10, 0.30, 0.80)
    col_yellow     = (0.95, 0.80, 0.10)
    col_black      = (0.10, 0.10, 0.10)
    col_roller     = (0.70, 0.90, 0.90)

    # Dimensions
    total_len = 12000
    width = 3000
    platform_h = 2800
    
    # --------------------------------------------------------------------------
    # 1. FOREGROUND STATION (Unwinder/Rewinder & Main Control)
    # --------------------------------------------------------------------------
    # Left Main Column
    make_box(doc, "Front_Col_L", 1000, 600, 3000, 0, 0, 0, col_grey_light, offset_coords)
    # Right Main Column
    make_box(doc, "Front_Col_R", 1000, 600, 3000, 0, width-600, 0, col_grey_light, offset_coords)
    # Top Crossbeam
    make_box(doc, "Front_Beam", 1000, width, 400, 0, 0, 2600, col_grey_light, offset_coords)
             
    # Blue Control Cabinet
    make_box(doc, "Main_Control_Panel", 300, 800, 1200, 1000, -100, 800, col_blue, offset_coords)
    # Screen
    make_box(doc, "Control_Screen", 20, 300, 200, 1300, 100, 1500, col_black, offset_coords)

    # Main Rollers
    make_cylinder(doc, "Main_Roller_1", 200, width-200, 500, 100, 1500, col_roller, offset_coords, axis=App.Vector(0,1,0))
    make_cylinder(doc, "Main_Roller_2", 200, width-200, 1400, 100, 1500, col_roller, offset_coords, axis=App.Vector(0,1,0))
                  
    # Side housing
    make_box(doc, "Mech_Housing_R", 1400, 400, 1000, 400, width-400, 1000, col_grey_light, offset_coords)

    # Yellow Safety Fence
    for i in range(4):
        make_cylinder(doc, f"Yellow_Post_{i}", 20, 1000, 1200 + (i*300), -500, 0, col_yellow, offset_coords)
    make_cylinder(doc, "Yellow_Rail_Top", 15, 1000, 1200, -500, 900, col_yellow, offset_coords, axis=App.Vector(1,0,0))
    make_cylinder(doc, "Yellow_Rail_Mid", 15, 1000, 1200, -500, 500, col_yellow, offset_coords, axis=App.Vector(1,0,0))

    # --------------------------------------------------------------------------
    # 2. GROUND FLOOR MACHINERY
    # --------------------------------------------------------------------------
    num_stations = 4
    station_len = 2000
    start_x = 2500
    
    for i in range(num_stations):
        sx = start_x + (i * station_len)
        
        # Base Unit
        make_box(doc, f"Station_Base_{i}", 1500, width-1000, 800, sx, 500, 0, col_grey_light, offset_coords)
        
        # Upper Arches
        make_box(doc, f"Station_Arch_L_{i}", 500, 300, 1500, sx + 500, 500, 800, col_grey_light, offset_coords)
        make_box(doc, f"Station_Arch_R_{i}", 500, 300, 1500, sx + 500, width-800, 800, col_grey_light, offset_coords)
                 
        # Internal Roller
        make_cylinder(doc, f"Station_Roll_{i}", 150, width-1200, sx + 750, 600, 1200, col_black, offset_coords, axis=App.Vector(0,1,0))
        # Blue Panel
        make_box(doc, f"Station_Panel_{i}", 600, 100, 800, sx + 450, 400, 500, col_blue, offset_coords)

    # --------------------------------------------------------------------------
    # 3. OVERHEAD PLATFORM AND OVENS
    # --------------------------------------------------------------------------
    # Platform Floor
    make_box(doc, "Platform_Floor", total_len, width + 500, 150, 0, -500, platform_h, col_grey_dark, offset_coords)
             
    # Legs
    leg_positions = [2500, 6000, 9500]
    for i, lx in enumerate(leg_positions):
        make_box(doc, f"Platform_Leg_L_{i}", 400, 400, platform_h, lx, -500, 0, col_grey_light, offset_coords)
        make_box(doc, f"Platform_Leg_R_{i}", 400, 400, platform_h, lx, width, 0, col_grey_light, offset_coords)

    # Ovens
    oven_start_x = 2000
    oven_len = 9000
    make_box(doc, "Oven_Main", oven_len, width-500, 1200, oven_start_x, 250, platform_h + 150, col_grey_light, offset_coords)
    make_box(doc, "Oven_Top", oven_len - 1000, width-1000, 400, oven_start_x + 500, 500, platform_h + 1350, col_grey_dark, offset_coords)
    
    # Fascia
    make_box(doc, "Platform_Fascia", total_len, 50, 600, 0, -500, platform_h, col_blue, offset_coords)

    # --------------------------------------------------------------------------
    # 4. RAILINGS AND STAIRS
    # --------------------------------------------------------------------------
    rail_height = 1000
    num_rails = int(total_len / 1000)
    
    # Railings
    make_cylinder(doc, "Rail_Top_Bar", 20, total_len, 0, -500, platform_h + rail_height, col_black, offset_coords, axis=App.Vector(1,0,0))
    make_cylinder(doc, "Rail_Mid_Bar", 20, total_len, 0, -500, platform_h + (rail_height/2), col_black, offset_coords, axis=App.Vector(1,0,0))
    
    for i in range(num_rails + 1):
        rx = i * 1000
        make_cylinder(doc, f"Rail_Post_{i}", 20, rail_height, rx, -500, platform_h, col_black, offset_coords)

    # Stairs
    stair_x = total_len - 1500
    stair_w = 1000
    stair_h_step = 200
    stair_run = 200
    num_steps = int(platform_h / stair_h_step)
    
    for i in range(num_steps):
        sx = stair_x + (i * stair_run)
        sz = platform_h - ((i+1) * stair_h_step)
        
        make_box(doc, f"Step_{i}", stair_run, stair_w, 20, sx, -1500, sz, col_grey_dark, offset_coords)
        if i % 2 == 0:
            make_cylinder(doc, f"Stair_Rail_Post_{i}", 15, 800, sx, -1500, sz, col_black, offset_coords)


# ==============================================================================
# MAIN DRAWING FUNCTION FOR THE HEAT EXCHANGER
# ==============================================================================

def draw_alfa_laval_phe(doc, offset_coords=(0,0,0)):
    # -- Dimensions --
    frame_w = 1200       
    frame_h = 3000      
    frame_th = 60       
    pack_len = 1500      
    follower_th = 60    
    total_len = 3000    
    
    # -- Colors --
    col_blue   = (0.05, 0.25, 0.65)
    col_red    = (0.85, 0.30, 0.25)
    col_silver = (0.80, 0.80, 0.80)
    col_dark   = (0.20, 0.20, 0.20)
    col_light  = (0.60, 0.60, 0.60)

    # --------------------------------------------------------------------------
    # 1. FIXED HEAD (Front Blue Plate)
    # --------------------------------------------------------------------------
    make_box(doc, "Fixed_Head", frame_w, frame_th, frame_h, 0, 0, 0, col_blue, offset_coords)
    make_box(doc, "Logo", 120, 2, 80, (frame_w-120)/2, -2, frame_h * 0.6, col_silver, offset_coords)

    # Lifting Lugs
    make_box(doc, "Lug_Top_L", 80, frame_th, 40, -20, 0, frame_h - 20, col_blue, offset_coords)
    make_box(doc, "Lug_Top_R", 80, frame_th, 40, frame_w - 60, 0, frame_h - 20, col_blue, offset_coords)

    # --------------------------------------------------------------------------
    # 2. PLATE PACK
    # --------------------------------------------------------------------------
    num_plates = 50
    plate_gap = pack_len / num_plates
    plate_w = frame_w - 60
    plate_h = frame_h - 140
    
    for i in range(num_plates):
        py = frame_th + (i * plate_gap)
        c = col_dark if i % 2 == 0 else col_light
        make_box(doc, f"Plate_{i}", plate_w, plate_gap - 0.5, plate_h, 30, py, 70, c, offset_coords)

    # --------------------------------------------------------------------------
    # 3. MOVABLE FOLLOWER
    # --------------------------------------------------------------------------
    follower_y = frame_th + pack_len
    make_box(doc, "Movable_Follower", frame_w, follower_th, frame_h, 0, follower_y, 0, col_blue, offset_coords)

    # --------------------------------------------------------------------------
    # 4. REAR SUPPORT COLUMN
    # --------------------------------------------------------------------------
    col_y = total_len
    col_w = 200
    
    make_box(doc, "Support_Column", col_w, 80, frame_h + 50, (frame_w - col_w)/2, col_y, 0, col_blue, offset_coords)
    make_box(doc, "Rear_Foot", 300, 150, 20, (frame_w - 300)/2, col_y - 35, -20, col_silver, offset_coords)

    # --------------------------------------------------------------------------
    # 5. GUIDE RAILS
    # --------------------------------------------------------------------------
    rail_rad = 20
    rail_len = total_len + 50
    
    make_cylinder(doc, "Rail_Top", rail_rad, rail_len, frame_w/2, -25, frame_h - 60, col_silver, offset_coords, axis=App.Vector(0,1,0))
    make_cylinder(doc, "Rail_Bottom", rail_rad, rail_len, frame_w/2, -25, 60, col_silver, offset_coords, axis=App.Vector(0,1,0))

    # --------------------------------------------------------------------------
    # 6. TIE RODS
    # --------------------------------------------------------------------------
    rod_rad = 15
    rod_positions_z = [150, frame_h/2, frame_h - 150]
    rod_x_offsets = [-40, frame_w + 40]
    
    for side_idx, rx in enumerate(rod_x_offsets):
        for i, rz in enumerate(rod_positions_z):
            # Red Sleeve
            make_cylinder(doc, f"Rod_Sleeve_{side_idx}_{i}", rod_rad + 3, pack_len + 20, rx, frame_th - 10, rz, col_red, offset_coords, axis=App.Vector(0,1,0))
            # Silver Extension
            extension_len = total_len - (frame_th + pack_len) - 100
            make_cylinder(doc, f"Rod_Extension_{side_idx}_{i}", rod_rad, extension_len, rx, frame_th + pack_len, rz, col_silver, offset_coords, axis=App.Vector(0,1,0))
            # Nuts
            make_cylinder(doc, f"Nut_Front_{side_idx}_{i}", 25, 20, rx, -20, rz, col_silver, offset_coords, axis=App.Vector(0,1,0))
            make_cylinder(doc, f"Nut_Back_{side_idx}_{i}", 25, 20, rx, frame_th + pack_len + 5, rz, col_silver, offset_coords, axis=App.Vector(0,1,0))

    # --------------------------------------------------------------------------
    # 7. PORTS
    # --------------------------------------------------------------------------
    port_rad = 80
    port_depth = 40
    
    px_L = 160
    px_R = frame_w - 160
    pz_B = 220
    pz_T = frame_h - 220
    
    port_centers = [(px_L, pz_T), (px_R, pz_T), (px_L, pz_B), (px_R, pz_B)]
    
    for i, (px, pz) in enumerate(port_centers):
        make_cylinder(doc, f"Port_Flange_{i}", port_rad, port_depth, px, -port_depth, pz, col_silver, offset_coords, axis=App.Vector(0,1,0))
        make_cylinder(doc, f"Port_Hole_{i}", port_rad - 15, port_depth + 2, px, -port_depth - 1, pz, col_dark, offset_coords, axis=App.Vector(0,1,0))
        
        # Stud Bolts
        num_studs = 8
        for j in range(num_studs):
            ang = (2 * math.pi / num_studs) * j
            sx = px + (port_rad + 12) * math.cos(ang)
            sz = pz + (port_rad + 12) * math.sin(ang)
            make_cylinder(doc, f"Stud_{i}_{j}", 6, 25, sx, -15, sz, col_silver, offset_coords, axis=App.Vector(0,1,0))

    # --------------------------------------------------------------------------
    # 8. FEET
    # --------------------------------------------------------------------------
    foot_w = 140
    foot_h = 20
    
    make_box(doc, "Foot_Front_L", foot_w, 100, foot_h, 40, -40, -foot_h, col_silver, offset_coords)
    make_box(doc, "Foot_Front_R", foot_w, 100, foot_h, frame_w - 40 - foot_w, -40, -foot_h, col_silver, offset_coords)

# ==============================================================================
# MAIN DRAWING FUNCTION FOR THE WATER STORAGE TANK
# ==============================================================================

def build_tank(doc, offset=(0,0,0)):
    # Local variables for tank size to prevent global confusion   
    # Tank Dims
    tank_dia = 2000.0
    tank_len = 5000.0
    tank_dish_ratio = 0.25
    saddle_width = 300.0
    leg_height = 1000.0
    radius = tank_dia / 2.0
    axis_h = leg_height + radius
    # Colours
    col_tank_blue = (0.1, 0.4, 0.8)
    col_black_steel = (0.1, 0.1, 0.1)
    col_stainless = (0.80, 0.82, 0.85)
    
    # --- A. MAIN TANK BODY (BLUE) ---
    # 1. Main Shell (Cylinder)
    # Using axis (1,0,0) rotates it to X-axis alignment
    make_cylinder(doc, "TankShell", radius, tank_len, -tank_len/2, 0, axis_h, col_tank_blue, offset, axis=App.Vector(1,0,0))

    # 2. Heads (Ellipsoidal)
    # Right Head
    head_r = Part.makeSphere(radius)
    mat_r = App.Matrix()
    mat_r.scale(tank_dish_ratio, 1.0, 1.0)
    head_r.transformShape(mat_r)
    # Apply offset + local translation
    head_r.translate(App.Vector(offset[0] + tank_len/2, offset[1], offset[2] + axis_h))
    
    obj_head_r = doc.addObject("Part::Feature", "TankHead_R")
    obj_head_r.Shape = head_r
    obj_head_r.ViewObject.ShapeColor = col_tank_blue
    
    # Left Head
    head_l = Part.makeSphere(radius)
    mat_l = App.Matrix()
    mat_l.scale(tank_dish_ratio, 1.0, 1.0)
    head_l.transformShape(mat_l)
    # Apply offset + local translation
    head_l.translate(App.Vector(offset[0] - tank_len/2, offset[1], offset[2] + axis_h))
    
    obj_head_l = doc.addObject("Part::Feature", "TankHead_L")
    obj_head_l.Shape = head_l
    obj_head_l.ViewObject.ShapeColor = col_tank_blue

    # Seams (Toroidal rings)
    seam_radius = 5.0
    for i in [-0.25, 0.0, 0.25]:
        sx = tank_len * i
        seam = Part.makeTorus(radius, seam_radius)
        seam.rotate(App.Vector(0,0,0), App.Vector(0,1,0), 90)
        seam.translate(App.Vector(offset[0] + sx, offset[1], offset[2] + axis_h))
        
        obj_seam = doc.addObject("Part::Feature", f"Seam_{i}")
        obj_seam.Shape = seam
        obj_seam.ViewObject.ShapeColor = col_tank_blue

    # --- B. SADDLE SUPPORTS ---
    support_positions = [-1500, 1500]
    for i, sx in enumerate(support_positions):
        # Cradle (Requires Boolean Cut)
        cradle_h = radius + 200
        cradle_w = radius * 2.2
        block = Part.makeBox(saddle_width, cradle_w, cradle_h)
        block.translate(App.Vector(sx - saddle_width/2, -cradle_w/2, leg_height))
        
        cutter = Part.makeCylinder(radius + 5, 2000)
        cutter.rotate(App.Vector(0,0,0), App.Vector(0,1,0), 90)
        cutter.translate(App.Vector(-1000, 0, axis_h))
        
        cradle = block.cut(cutter)
        cradle.translate(App.Vector(*offset))
        
        obj_cradle = doc.addObject("Part::Feature", f"Cradle_{i}")
        obj_cradle.Shape = cradle
        obj_cradle.ViewObject.ShapeColor = col_black_steel
        
        # Legs
        make_box(doc, f"Leg_L_{i}", saddle_width, 150, leg_height, 
                 sx - saddle_width/2, -radius - 50, 0, col_black_steel, offset=offset)
                 
        make_box(doc, f"Leg_R_{i}", saddle_width, 150, leg_height, 
                 sx - saddle_width/2, radius - 100, 0, col_black_steel, offset=offset)
                 
        # Base Plates
        plate_dim = 400
        make_box(doc, f"BasePlate_L_{i}", plate_dim, plate_dim, 20, 
                 sx - plate_dim/2, -radius - 50 - (plate_dim-150)/2, 0, col_black_steel, offset=offset)
                 
        make_box(doc, f"BasePlate_R_{i}", plate_dim, plate_dim, 20, 
                 sx - plate_dim/2, radius - 100 - (plate_dim-150)/2, 0, col_black_steel, offset=offset)
                 
        # Brace
        make_box(doc, f"Brace_{i}", saddle_width, radius*2, 100, 
                 sx - saddle_width/2, -radius, 200, col_black_steel, offset=offset)

    # --- C. TOP FITTINGS ---
    mw_x = -1500
    mw_r = 300
    mw_h = 150
    
    # Manway Neck
    make_cylinder(doc, "ManwayNeck", mw_r, mw_h, 
                  mw_x, 0, axis_h + radius * 0.9, col_stainless, offset=offset)
                  
    # Manway Lid
    make_cylinder(doc, "ManwayLid", mw_r + 40, 20, 
                  mw_x, 0, axis_h + radius * 0.9 + mw_h, col_stainless, offset=offset)
                  
    # Hinge
    make_box(doc, "Hinge", 50, 100, 40, 
             mw_x - 25, mw_r, axis_h + radius * 0.9 + mw_h - 10, col_stainless, offset=offset)

    # Nozzles
    nozzle_coords = [1000, 1300, 1600]
    for i, nx in enumerate(nozzle_coords):
        # Pipe
        make_cylinder(doc, f"NozzlePipe_{i}", 60, 250, 
                      nx, 0, axis_h + radius * 0.9, col_stainless, offset=offset)
        
        # Flange (if not the elbow one)
        if i != 2:
            make_cylinder(doc, f"NozzleFlange_{i}", 100, 20, 
                          nx, 0, axis_h + radius * 0.9 + 250, col_stainless, offset=offset)
        
        # Elbow Special Case
        if i == 2:
            elbow = Part.makeTorus(150, 60, App.Vector(0,0,0), App.Vector(0,1,0), 0, 90)
            elbow.rotate(App.Vector(0,0,0), App.Vector(0,1,0), 180)
            elbow.translate(App.Vector(nx + 150, 0, axis_h + radius * 0.9 + 250))
            elbow.translate(App.Vector(*offset))
            
            obj_elbow = doc.addObject("Part::Feature", f"NozzleElbow_{i}")
            obj_elbow.Shape = elbow
            obj_elbow.ViewObject.ShapeColor = col_stainless

    # --- D. LIFTING LUGS ---
    lug_x_pos = [-1800, 1800]
    for i, lx in enumerate(lug_x_pos):
        lug = Part.makeBox(150, 20, 150)
        hole = Part.makeCylinder(30, 20)
        hole.rotate(App.Vector(0,0,0), App.Vector(1,0,0), -90)
        hole.translate(App.Vector(75, 0, 100))
        lug = lug.cut(hole)
        lug.translate(App.Vector(lx - 75, -10, axis_h + radius))
        lug.translate(App.Vector(*offset))
        
        obj_lug = doc.addObject("Part::Feature", f"LiftLug_{i}")
        obj_lug.Shape = lug
        obj_lug.ViewObject.ShapeColor = col_stainless


# ==============================================================================
# MAIN DRAWING FUNCTION FOR THE COATING LIQUID
# ==============================================================================

def draw_fuel_tank(doc, offset_coords=(0,0,0)):
    # Colors
    col_white = (0.95, 0.95, 0.95)
    col_steel = (0.70, 0.70, 0.70)
    col_black = (0.10, 0.10, 0.10)

    # Dimensions
    tank_radius = 750
    tank_len = 3500
    skid_len = 4200
    skid_width = 1100
    skid_pipe_rad = 60
    
    tank_z = 1000
    skid_z = 60
    
    # --------------------------------------------------------------------------
    # 1. SKID BASE
    # --------------------------------------------------------------------------
    
    # Skid Rails
    make_cylinder(doc, "Skid_Rail_L", skid_pipe_rad, skid_len, -350, -skid_width/2, skid_z, col_white, offset_coords, axis=App.Vector(1,0,0))
    make_cylinder(doc, "Skid_Rail_R", skid_pipe_rad, skid_len, -350, skid_width/2, skid_z, col_white, offset_coords, axis=App.Vector(1,0,0))

    # Skid End Caps
    make_cylinder(doc, "Skid_Tip_FL", skid_pipe_rad, 200, skid_len - 350, -skid_width/2, skid_z, col_white, offset_coords, axis=App.Vector(0,0,1))
    make_cylinder(doc, "Skid_Tip_FR", skid_pipe_rad, 200, skid_len - 350, skid_width/2, skid_z, col_white, offset_coords, axis=App.Vector(0,0,1))
    make_cylinder(doc, "Skid_Tip_BL", skid_pipe_rad, 200, -350, -skid_width/2, skid_z, col_white, offset_coords, axis=App.Vector(0,0,1))
    make_cylinder(doc, "Skid_Tip_BR", skid_pipe_rad, 200, -350, skid_width/2, skid_z, col_white, offset_coords, axis=App.Vector(0,0,1))
                  
    # Lifting Lugs
    for x_pos in [-250, skid_len - 450]:
        make_box(doc, "Lug_L", 50, 20, 100, x_pos, -skid_width/2, skid_z + 50, col_steel, offset_coords)
        make_box(doc, "Lug_R", 50, 20, 100, x_pos, skid_width/2, skid_z + 50, col_steel, offset_coords)

    # --------------------------------------------------------------------------
    # 2. TANK SUPPORTS
    # --------------------------------------------------------------------------
    num_supports = 3
    support_spacing = 1200
    start_x = 200
    
    for i in range(num_supports):
        sx = start_x + (i * support_spacing)
        
        make_box(doc, f"Cross_Beam_{i}", 100, skid_width, 80, sx, -skid_width/2, skid_z + skid_pipe_rad, col_white, offset_coords)
        saddle_h = tank_z - (skid_z + skid_pipe_rad) - 50
        make_box(doc, f"Saddle_{i}", 20, skid_width - 100, saddle_h, sx + 40, -(skid_width - 100)/2, skid_z + skid_pipe_rad + 80, col_white, offset_coords)

    # --------------------------------------------------------------------------
    # 3. MAIN TANK BODY
    # --------------------------------------------------------------------------
    make_cylinder(doc, "Tank_Body", tank_radius, tank_len, 0, 0, tank_z, col_white, offset_coords, axis=App.Vector(1,0,0))
    make_cylinder(doc, "Cap_Back", tank_radius, 20, 0, 0, tank_z, col_white, offset_coords, axis=App.Vector(1,0,0))
    make_cylinder(doc, "Cap_Front", tank_radius, 20, tank_len - 20, 0, tank_z, col_white, offset_coords, axis=App.Vector(1,0,0))

    # --------------------------------------------------------------------------
    # 4. FRONT VALVE BOX
    # --------------------------------------------------------------------------
    box_w = 500
    box_h = 500
    box_d = 400
    
    make_box(doc, "Valve_Box", box_d, box_w, box_h, tank_len, -box_w/2, tank_z - tank_radius + 100, col_white, offset_coords)
    make_box(doc, "Valve_Box_Lid", box_d, box_w - 40, 20, tank_len, -(box_w-40)/2, tank_z - tank_radius + 100 + box_h, col_white, offset_coords)
    make_cylinder(doc, "Valve_Outlet", 40, 100, tank_len + box_d, 0, tank_z - tank_radius + 100 + 150, col_black, offset_coords, axis=App.Vector(1,0,0))

    # --------------------------------------------------------------------------
    # 5. TOP FITTINGS
    # --------------------------------------------------------------------------
    nozzle_positions = [600, 1200, 1800]
    for i, nx in enumerate(nozzle_positions):
        make_cylinder(doc, f"Nozzle_Neck_{i}", 80, 150, nx, 0, tank_z + tank_radius - 20, col_white, offset_coords)
        make_cylinder(doc, f"Nozzle_Top_{i}", 120, 20, nx, 0, tank_z + tank_radius + 130, col_white, offset_coords)

    # Lifting Lugs on Top
    make_box(doc, "Lift_Lug_Front", 100, 20, 150, tank_len - 600, 0, tank_z + tank_radius, col_white, offset_coords)
    make_box(doc, "Lift_Lug_Rear", 100, 20, 150, 600, 0, tank_z + tank_radius, col_white, offset_coords)

    # --------------------------------------------------------------------------
    # 6. REAR LADDER / RAIL
    # --------------------------------------------------------------------------
    rail_x = 100
    rail_h = 500
    
    make_cylinder(doc, "Ladder_Leg_L", 20, rail_h, rail_x, -300, tank_z + tank_radius, col_steel, offset_coords)
    make_cylinder(doc, "Ladder_Leg_R", 20, rail_h, rail_x, 300, tank_z + tank_radius, col_steel, offset_coords)
    make_cylinder(doc, "Ladder_Top", 20, 600, rail_x, -300, tank_z + tank_radius + rail_h, col_steel, offset_coords, axis=App.Vector(0,1,0))
    make_cylinder(doc, "Ladder_Return_L", 20, 300, rail_x, -300, tank_z + tank_radius + rail_h, col_steel, offset_coords, axis=App.Vector(1,0,0))



# ==============================================================================
# MAIN DRAWING FUNCTION FOR THE CALENDERING MACHINE
# ==============================================================================

def draw_fabric_machine(doc, offset_coords=(0, 0, 0)):
    # -- Definitions --
    # Colors
    col_frame  = (0.85, 0.85, 0.85)  # Aluminum/Silver
    col_panel  = (0.95, 0.95, 0.95)  # White Enclosure
    col_black  = (0.15, 0.15, 0.15)  # Towers
    col_orange = (1.00, 0.50, 0.10)  # The Fabric
    col_red    = (0.90, 0.10, 0.10)  # Knobs/E-Stop
    col_green  = (0.10, 0.80, 0.10)  # Start Button
    col_blue   = (0.20, 0.40, 0.80)  # Levers
    col_steel  = (0.70, 0.70, 0.72)  # Rollers

    # Base Dimensions
    base_w = 4800
    base_d = 3600
    base_h = 2400

    # ==========================================================================
    # 1. BASE UNIT & WHEELS
    # ==========================================================================

    # Main Table Frame
    make_box(doc, "Base_Frame_Top",
             base_w, base_d, 40,
             0, 0, base_h,
             col_frame, offset_coords)

    # Main Cabinet Body
    make_box(doc, "Base_Cabinet",
             base_w - 100, base_d - 100, base_h - 100,
             50, 50, 100,
             col_panel, offset_coords)

    # Left Side Plate (with Blue Levers)
    make_box(doc, "Left_Panel_Plate",
             500, 20, 600,
             50, -20, 150,
             col_panel, offset_coords)

    # 3 Blue Levers on the left
    for i in range(3):
        lx = 150 + (i * 120)
        lz = 600
        # Pivot Base
        make_cylinder(doc, f"Lever_Pivot_{i}",
                      15, 40,
                      lx, -30, lz,
                      col_steel, offset_coords,
                      axis=App.Vector(0, 1, 0))
        # Handle
        make_cylinder(doc, f"Lever_Handle_{i}",
                      10, 100,
                      lx, -50, lz - 50,
                      col_blue, offset_coords,
                      axis=App.Vector(0, 0, 1))

    # Caster Wheels
    wheel_positions = [
        (100, 100), (base_w - 100, 100),
        (100, base_d - 100), (base_w - 100, base_d - 100)
    ]
    for i, (wx, wy) in enumerate(wheel_positions):
        # Wheel
        make_cylinder(doc, f"Wheel_{i}",
                      40, 40,
                      wx, wy, 40,
                      (0.2, 0.2, 0.2), offset_coords,
                      axis=App.Vector(0, 1, 0))
        # Mount
        make_box(doc, f"Wheel_Mount_{i}",
                 60, 60, 60,
                 wx - 30, wy - 30, 40,
                 col_frame, offset_coords)

    # ==========================================================================
    # 2. CONTROL BOX (Front Right)
    # ==========================================================================
    ctrl_w = 1800
    ctrl_d = 1050
    ctrl_h = 1950
    ctrl_x = base_w - 2100
    ctrl_y = -900  # Sticks out in front

    # Box Body
    make_box(doc, "Control_Box_Main",
             ctrl_w, ctrl_d, ctrl_h,
             ctrl_x, ctrl_y, 100,
             col_panel, offset_coords)

    # Top Interface Plate
    make_box(doc, "Control_Face",
             ctrl_w - 40, ctrl_d - 40, 10,
             ctrl_x + 20, ctrl_y + 20, 100 + ctrl_h,
             (0.3, 0.3, 0.3), offset_coords)

    # Buttons
    # Red E-Stop
    make_cylinder(doc, "Btn_EStop",
                  25, 20,
                  ctrl_x + 300, ctrl_y + 150, 100 + ctrl_h + 10,
                  col_red, offset_coords)
    # Green Start
    make_cylinder(doc, "Btn_Start",
                  15, 10,
                  ctrl_x + 400, ctrl_y + 100, 100 + ctrl_h + 10,
                  col_green, offset_coords)
    # Black Switches
    make_cylinder(doc, "Sw_1",
                  10, 15,
                  ctrl_x + 500, ctrl_y + 100, 100 + ctrl_h + 10,
                  col_black, offset_coords)

    # Logo/Fan area on front face
    make_cylinder(doc, "Vent_Fan",
                  40, 10,
                  ctrl_x + 500, ctrl_y, 300,
                  col_black, offset_coords,
                  axis=App.Vector(0, 1, 0))

    # ==========================================================================
    # 3. PROCESSING TOWERS (The Black Structures)
    # ==========================================================================
    # There are two identical towers
    t_width = 750
    t_depth = 1200
    t_height = 1200
    t_y_start = 600

    # Locations for Tower 1 and Tower 2
    tower_locs = [
        ("Tower1", base_w - 400),
        ("Tower2", base_w - 900)
    ]

    for name, tx in tower_locs:
        # Left Leg
        make_box(doc, f"{name}_L",
                 30, t_depth, t_height,
                 tx, t_y_start, base_h,
                 col_black, offset_coords)
        # Right Leg
        make_box(doc, f"{name}_R",
                 30, t_depth, t_height,
                 tx + t_width, t_y_start, base_h,
                 col_black, offset_coords)
        # Top Bar
        make_box(doc, f"{name}_Top",
                 t_width + 30, t_depth, 30,
                 tx, t_y_start, base_h + t_height,
                 col_black, offset_coords)

        # Steel Rollers inside
        make_cylinder(doc, f"{name}_Roller_Top",
                      40, t_width,
                      tx + 15, t_y_start + 100, base_h + 250,
                      col_steel, offset_coords,
                      axis=App.Vector(1, 0, 0))
        make_cylinder(doc, f"{name}_Roller_Bot",
                      40, t_width,
                      tx + 15, t_y_start + 100, base_h + 150,
                      col_steel, offset_coords,
                      axis=App.Vector(1, 0, 0))

        # Pneumatic Cylinders on top (2 per tower)
        for i in range(2):
            py = t_y_start + 100 + (i * 150)
            # Cylinder Body
            make_cylinder(doc, f"{name}_Pneu_{i}",
                          30, 120,
                          tx + (t_width / 2), py, base_h + t_height + 30,
                          col_frame, offset_coords)
            # Red Knob on top
            make_cylinder(doc, f"{name}_Knob_{i}",
                          15, 20,
                          tx + (t_width / 2), py, base_h + t_height + 150,
                          col_red, offset_coords)

    # Central Cover/Tunnel between towers
    make_box(doc, "Center_Tunnel",
             200, t_depth, t_height - 100,
             base_w - 620, t_y_start, base_h,
             col_frame, offset_coords)

    # ==========================================================================
    # 4. ORANGE MATERIAL WEB
    # ==========================================================================

    # Input Roll at the back
    roll_x = base_w - 300
    roll_y = 2400
    make_cylinder(doc, "Input_Roll",
                  80, 500,
                  roll_x, roll_y, base_h + 150,
                  col_orange, offset_coords,
                  axis=App.Vector(1, 0, 0))

    # Web Segment 1: Roll to Tower 1
    make_box(doc, "Web_Seg1",
             300, 250, 2,
             roll_x - 300, 400, base_h + 150,
             col_orange, offset_coords)

    # Web Segment 2: Through Machine
    make_box(doc, "Web_Main",
             1000, 250, 2,
             base_w - 1200, 300, base_h + 150,
             col_orange, offset_coords)

    # Web Segment 3: Exit Drape
    make_box(doc, "Web_Exit",
             200, 250, 2,
             base_w - 1400, 300, base_h + 150,
             col_orange, offset_coords,
             rotation_angle=15,
             rotation_axis=App.Vector(0, 1, 0))




# ==============================================================================
# MAIN DRAWING FUNCTION FOR THE HORIZONTAL CONVEYOR BELT
# ==============================================================================


def pocket_conveyor(doc, offset=(0,0,0)):
    """
    Draws a cleated/pocket conveyor based on the reference image.
    Offset allows placement at specific global coordinates.
    """
    
    # --- Parameters ---
    conv_len = 6000.0
    conv_width = 1500.0
    rail_h = 140.0
    rail_thick = 5.0
    belt_level = 90.0  # Height of belt surface from bottom of rail
    #Colours
    col_frame_grey = (0.75, 0.75, 0.78)
    col_cleat_blue = (0.0, 0.3, 0.8)
    col_motor_box  = (0.35, 0.4, 0.45)
    col_black      = (0.1, 0.1, 0.1)
    col_gold       = (0.8, 0.6, 0.1)
    col_belt_green = (0.0, 0.6, 0.3)
    
    # ------------------------------------
    # A. FRAME (Side Rails)
    # ------------------------------------
    # Left Rail (Vertical)
    make_box(doc, "Rail_L_Vert", conv_len, rail_thick, rail_h, 
             0, 0, 0, col_frame_grey, offset)
    # Left Rail (Top Flange - simulating C-channel)
    make_box(doc, "Rail_L_Top", conv_len, 40, rail_thick, 
             0, 0, rail_h - rail_thick, col_frame_grey, offset)
             
    # Right Rail (Vertical)
    make_box(doc, "Rail_R_Vert", conv_len, rail_thick, rail_h, 
             0, conv_width - rail_thick, 0, col_frame_grey, offset)
    # Right Rail (Top Flange)
    make_box(doc, "Rail_R_Top", conv_len, 40, rail_thick, 
             0, conv_width - 40, rail_h - rail_thick, col_frame_grey, offset)

    # Cross bracing (underneath)
    num_braces = 4
    for i in range(num_braces):
        bx = (conv_len / (num_braces + 1)) * (i + 1)
        make_box(doc, f"Brace_{i}", 50, conv_width - (2*rail_thick), 40, 
                 bx, rail_thick, 0, col_frame_grey, offset)

    # ------------------------------------
    # B. BELT & ROLLERS
    # ------------------------------------
    # Main Belt Surface -- CHANGED TO GREEN
    make_box(doc, "Belt_Surface", conv_len - 100, conv_width - 20, 5, 
             50, 10, belt_level, col_belt_green, offset)
    
    # Center Guide Stripe (The light blue line in image)
    make_box(doc, "Belt_CenterLine", conv_len - 100, 10, 1, 
             50, (conv_width/2) - 5, belt_level + 5, (0.0, 0.8, 1.0), offset)

    # End Roller (Front)
    make_cylinder(doc, "Roller_Front", 40, conv_width - 10, 
                  conv_len - 50, 5, belt_level - 35, col_black, offset, axis=App.Vector(0,1,0))
    # Roller Shaft Front
    make_cylinder(doc, "Shaft_Front", 10, conv_width + 40, 
                  conv_len - 50, -20, belt_level - 35, col_gold, offset, axis=App.Vector(0,1,0))

    # End Roller (Back/Drive)
    make_cylinder(doc, "Roller_Back", 40, conv_width - 10, 
                  50, 5, belt_level - 35, col_black, offset, axis=App.Vector(0,1,0))

    # ------------------------------------
    # C. POCKETS (CLEATS) - The Blue Bars
    # ------------------------------------
    num_cleats = 12
    cleat_pitch = (conv_len - 200) / num_cleats
    cleat_w = conv_width - 30
    
    for i in range(num_cleats):
        cx = 100 + (i * cleat_pitch)
        # Cleat shape: Blue bar
        make_box(doc, f"Cleat_{i}", 15, cleat_w, 20, 
                 cx, 15, belt_level + 5, col_cleat_blue, offset)

    # ------------------------------------
    # D. DRIVE UNIT (Motor Box) - Left Side
    # ------------------------------------
    box_l = 250
    box_w = 200
    box_h = 300
    
    # Main electrical/motor box
    make_box(doc, "DriveBox_Main", box_l, box_w, box_h, 
             -box_l, -box_w - 20, belt_level - 100, col_motor_box, offset)
             
    # Connection bracket to frame
    make_box(doc, "Drive_Bracket", 50, 50, 200, 
             0, -50, belt_level - 50, col_frame_grey, offset)

    # ------------------------------------
    # E. CONTROL PENDANT (The hanging arm)
    # ------------------------------------
    # Arm Pivot
    make_cylinder(doc, "Arm_Pivot", 15, 60, 
                  150, -60, belt_level - 20, col_black, offset, axis=App.Vector(0,1,0))
    
    # Vertical Arm
    make_box(doc, "Arm_Vert", 20, 20, 200, 
             140, -80, belt_level - 220, col_frame_grey, offset)
             
    # The Handle/Interface at bottom
    make_box(doc, "Arm_Handle", 80, 20, 80, 
             110, -80, belt_level - 300, col_frame_grey, offset, 
             rotation_angle=45, rotation_axis=App.Vector(0,1,0))

    # ------------------------------------
    # F. LEGS / SUPPORTS
    # ------------------------------------
    leg_h = 600.0
    leg_x_positions = [500, 2500]
    
    for i, lx in enumerate(leg_x_positions):
        # Leg Vertical Post
        make_box(doc, f"Leg_Post_{i}", 80, 80, leg_h, 
                 lx, conv_width, -leg_h + 50, col_frame_grey, offset)
        
        # Connection Plate to Rail
        make_box(doc, f"Leg_Plate_{i}", 120, 10, 150, 
                 lx - 20, conv_width, 0, col_black, offset)
                 
    # ------------------------------------
    # G. SENSORS / SIDE DETAILS
    # ------------------------------------
    # Sensor Bracket on the side
    sensor_x = 1200
    make_box(doc, "Sensor_Mount", 100, 40, 10, 
             sensor_x, -40, 50, col_frame_grey, offset)
    make_cylinder(doc, "Sensor_Head", 10, 30, 
                  sensor_x + 50, -30, 60, col_black, offset)

# ==============================================================================
# MAIN DRAWING FUNCTION FOR THE PIPING CONNECTIONS
# ==============================================================================

# --- 1. Flanged Pipe (Bolted sections using cylinders) ---
# Now accepts explicit start_p and end_p vectors from the layout
def create_jointed_pipe(doc, name, start_p, end_p, pipe_r, joint_r, color, offset=(0,0,0)):
    # Calculate Global Positions by applying offset to the passed coordinates
    col_pipe_yellow = (1.0, 0.8, 0.0)
    p1 = App.Vector(start_p.x + offset[0], start_p.y + offset[1], start_p.z + offset[2])
    p2 = App.Vector(end_p.x + offset[0], end_p.y + offset[1], end_p.z + offset[2])
    
    vector = p2.sub(p1)
    length = vector.Length
    if length == 0: return None
    direction = vector.normalize()

    # Create main pipe
    pipe = Part.makeCylinder(pipe_r, length)
    
    # Calculate Axis-Angle rotation
    z_axis = App.Vector(0,0,1)
    axis = z_axis.cross(direction)
    if axis.Length < 1e-7:
        angle = 0 if direction.z > 0 else 180
        axis = App.Vector(1,0,0)
    else:
        angle = math.degrees(math.acos(z_axis.dot(direction)))
    
    pipe.rotate(App.Vector(0,0,0), axis, angle)
    pipe.translate(p1)
    
    # Create Joints (Flanges)
    j_thick = 40.0
    j1 = Part.makeCylinder(joint_r, j_thick)
    j1.rotate(App.Vector(0,0,0), axis, angle)
    j1.translate(p1)
    
    j2 = Part.makeCylinder(joint_r, j_thick)
    j2.rotate(App.Vector(0,0,0), axis, angle)
    j2.translate(p2.sub(direction.multiply(j_thick)))
    
    shape = pipe.fuse(j1).fuse(j2)
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = shape
    obj.ViewObject.ShapeColor = color
    return obj


# ==========================================
# 2. MAIN BUILD ROUTINE FOR THE LIQUID TANK
# ==========================================

def liquid_tank(doc, offset=(0,0,0)):
    # --- Configuration ---
    tank_radius = 1000.0
    tank_height = 2500.0
    roof_height = 400.0
    ladder_width = 500.0
    ladder_off = 150.0
    cage_start_h = 1200.0

    col_tank_silver = (0.75, 0.77, 0.80)
    col_rail_yellow = (0.95, 0.8, 0.1)
    col_ladder_blue = (0.1, 0.3, 0.7)
    col_white = (0.9, 0.9, 0.9)

    # --- A. TANK BODY ---
    # Main Shell
    make_cylinder(doc, "TankShell", tank_radius, tank_height, 0, 0, 0, 
                  col_tank_silver, offset)
    
    # Roof (Cone - Manual creation required for shapes not covered by helpers)
    roof = Part.makeCone(tank_radius, 0, roof_height)
    roof.translate(App.Vector(0 + offset[0], 0 + offset[1], tank_height + offset[2]))
    obj_roof = doc.addObject("Part::Feature", "TankRoof")
    obj_roof.Shape = roof
    obj_roof.ViewObject.ShapeColor = col_tank_silver
    
    # Rim (Boolean Cut)
    rim = Part.makeCylinder(tank_radius + 50, 100)
    inner = Part.makeCylinder(tank_radius, 100)
    rim = rim.cut(inner)
    rim.translate(App.Vector(0 + offset[0], 0 + offset[1], (tank_height - 50) + offset[2]))
    obj_rim = doc.addObject("Part::Feature", "TopRim")
    obj_rim.Shape = rim
    obj_rim.ViewObject.ShapeColor = col_rail_yellow

    # --- B. LADDER ASSEMBLY ---
    lad_x = 0
    lad_y = -tank_radius - ladder_off
    rail_radius = 20.0
    rail_h = tank_height + 1000
    
    # Rails
    make_cylinder(doc, "Rail_L", rail_radius, rail_h, 
                  lad_x - ladder_width/2, lad_y, 0, 
                  col_ladder_blue, offset)
    make_cylinder(doc, "Rail_R", rail_radius, rail_h, 
                  lad_x + ladder_width/2, lad_y, 0, 
                  col_ladder_blue, offset)
    
    # Rungs
    num_rungs = int(rail_h / 300)
    for i in range(num_rungs):
        rz = 300 + (i * 300)
        # Axis (1,0,0) aligns cylinder along X for rungs
        make_cylinder(doc, f"Rung_{i}", 10, ladder_width, 
                      lad_x - ladder_width/2, lad_y, rz, 
                      col_rail_yellow, offset, axis=App.Vector(1,0,0))

    # Brackets
    num_brackets = int(tank_height / 1500)
    for i in range(num_brackets):
        bz = 1000 + (i * 1500)
        # Left Bracket
        make_box(doc, f"Bracket_L_{i}", 20, ladder_off, 40, 
                 lad_x - ladder_width/2 - 10, lad_y, bz, 
                 col_ladder_blue, offset)
        # Right Bracket
        make_box(doc, f"Bracket_R_{i}", 20, ladder_off, 40, 
                 lad_x + ladder_width/2 - 10, lad_y, bz, 
                 col_ladder_blue, offset)

    # Safety Cage (Complex shape requiring manual construction)
    cage_r = 350.0
    cage_h = rail_h - cage_start_h
    
    # Hoops
    num_hoops = int(cage_h / 800)
    for i in range(num_hoops + 1):
        hz = cage_start_h + (i * 800)
        hoop = Part.makeTorus(cage_r, 5)
        hoop.rotate(App.Vector(0,0,0), App.Vector(1,0,0), 90)
        
        # Cut opening
        cut_box = Part.makeBox(cage_r*2, cage_r, 20)
        cut_box.translate(App.Vector(-cage_r, 0, -10))
        hoop = hoop.cut(cut_box)
        
        # Apply global offset manually
        hoop.translate(App.Vector(lad_x + offset[0], (lad_y - (cage_r - 50)) + offset[1], hz + offset[2]))
        obj = doc.addObject("Part::Feature", f"CageHoop_{i}")
        obj.Shape = hoop
        obj.ViewObject.ShapeColor = col_rail_yellow

    # Straps
    for angle in [-45, 0, 45]:
        sx = (cage_r) * math.sin(math.radians(angle))
        sy = -(cage_r) * math.cos(math.radians(angle))
        hoop_center_y = lad_y - (cage_r - 50)
        
        make_box(doc, f"Strap_{angle}", 5, 40, cage_h, 
                 lad_x + sx, hoop_center_y + sy, cage_start_h, 
                 col_rail_yellow, offset)

    # --- C. TOP RAILING ---
    rail_h_top = 1100.0
    num_posts = 16
    
    # Handrails (Manual Torus with Boolean Cut)
    handrail = Part.makeTorus(tank_radius, 20)
    handrail.translate(App.Vector(0, 0, tank_height + rail_h_top))
    
    midrail = Part.makeTorus(tank_radius, 15)
    midrail.translate(App.Vector(0, 0, tank_height + rail_h_top/2))
    
    # Cutout
    ladder_cutout = Part.makeBox(ladder_width + 100, 1000, 2000)
    ladder_cutout.translate(App.Vector(-(ladder_width+100)/2, -tank_radius - 500, tank_height))
    
    handrail = handrail.cut(ladder_cutout)
    midrail = midrail.cut(ladder_cutout)
    
    # Apply offset to final shapes
    handrail.translate(App.Vector(offset[0], offset[1], offset[2]))
    midrail.translate(App.Vector(offset[0], offset[1], offset[2]))
    
    obj_hr = doc.addObject("Part::Feature", "Handrail")
    obj_hr.Shape = handrail
    obj_hr.ViewObject.ShapeColor = col_rail_yellow
    obj_mr = doc.addObject("Part::Feature", "Midrail")
    obj_mr.Shape = midrail
    obj_mr.ViewObject.ShapeColor = col_rail_yellow
    
    # Posts
    for i in range(num_posts):
        angle = (360.0 / num_posts) * i
        if 260 < angle < 280: continue
        
        rad = math.radians(angle)
        px = tank_radius * math.cos(rad)
        py = tank_radius * math.sin(rad)
        
        make_cylinder(doc, f"Post_{i}", 20, rail_h_top, 
                      px, py, tank_height, 
                      col_rail_yellow, offset)

    # --- D. MANWAY ---
    mw_angle = -120 
    mw_rad = math.radians(mw_angle)
    mw_z = 800
    mw_x = tank_radius * math.cos(mw_rad)
    mw_y = tank_radius * math.sin(mw_rad)
    
    # Manual construction due to complex rotation
    neck = Part.makeCylinder(300, 200)
    neck.rotate(App.Vector(0,0,0), App.Vector(0,1,0), 90)
    neck.rotate(App.Vector(0,0,0), App.Vector(0,0,1), mw_angle)
    neck.translate(App.Vector(mw_x, mw_y, mw_z))
    
    tip_x = (tank_radius + 200) * math.cos(mw_rad)
    tip_y = (tank_radius + 200) * math.sin(mw_rad)
    
    lid = Part.makeCylinder(350, 30)
    lid.rotate(App.Vector(0,0,0), App.Vector(0,1,0), 90)
    lid.rotate(App.Vector(0,0,0), App.Vector(0,0,1), mw_angle)
    lid.translate(App.Vector(tip_x, tip_y, mw_z))
    
    hinge = Part.makeBox(50, 100, 40)
    hinge.rotate(App.Vector(0,0,0), App.Vector(0,0,1), mw_angle)
    hinge.translate(App.Vector(tip_x, tip_y, mw_z))
    
    manway = neck.fuse(lid).fuse(hinge)
    manway.translate(App.Vector(offset[0], offset[1], offset[2]))
    
    obj_mw = doc.addObject("Part::Feature", "Manway")
    obj_mw.Shape = manway
    obj_mw.ViewObject.ShapeColor = col_white
    
    # Bolts
    for i in range(8):
        bang = (360/8) * i
        brad = math.radians(bang)
        lb_y = 280 * math.cos(brad)
        lb_z = 280 * math.sin(brad)
        
        rot_y = lb_y * math.cos(mw_rad)
        rot_x = -lb_y * math.sin(mw_rad)
        
        # Using manual rotation/translation to match Manway orientation
        bolt = Part.makeCylinder(15, 40)
        bolt.rotate(App.Vector(0,0,0), App.Vector(0,1,0), 90)
        bolt.rotate(App.Vector(0,0,0), App.Vector(0,0,1), mw_angle)
        bolt.translate(App.Vector(tip_x + rot_x + offset[0], tip_y + rot_y + offset[1], mw_z + lb_z + offset[2]))
        
        obj = doc.addObject("Part::Feature", f"MwBolt_{i}")
        obj.Shape = bolt
        obj.ViewObject.ShapeColor = col_tank_silver

    # --- E. TOP NOZZLE ---
    noz_angle = -45
    noz_rad = math.radians(noz_angle)
    nx = (tank_radius - 300) * math.cos(noz_rad)
    ny = (tank_radius - 300) * math.sin(noz_rad)
    nz = tank_height
    
    make_cylinder(doc, "TopNozzlePipe", 80, 300, nx, ny, nz, col_white, offset)
    make_cylinder(doc, "TopNozzleFlange", 120, 20, nx, ny, nz + 280, col_white, offset)



# ==============================================================================
# MAIN DRAWING FUNCTION FOR THE SLITTING MACHINE 
# ==============================================================================


def draw_slitting_machine(doc, offset_coords=(0,0,0)):
    # -- Colors --
    col_body   = (0.75, 0.85, 0.95) # Light Blue Machine Body
    col_steel  = (0.75, 0.75, 0.75) # Silver/Steel parts
    col_dark   = (0.15, 0.15, 0.15) # Black belt/rubber
    col_trans  = (0.85, 0.90, 0.95) # Transparent cover (simulated light blue)
    col_red    = (0.80, 0.10, 0.10) # Red knobs/buttons
    col_green  = (0.10, 0.80, 0.10) # Green buttons
    col_yellow = (0.90, 0.90, 0.10) # Yellow buttons
    col_panel  = (0.95, 0.95, 0.95) # White/Grey Control Panel background

    # -- Dimensions (SCALED BY 2) --
    base_w = 3600
    base_d = 2000
    base_h = 1400
    
    # ==========================================================================
    # 1. BASE CABINET
    # ==========================================================================
    # Main Box (z offset 50 -> 100, 100 -> 200)
    make_box(doc, "Base_Cabinet", base_w, base_d, base_h, 0, 0, 200, col_body, offset_coords)
    
    # Vented Doors (3 Doors)
    door_w = (base_w / 3) - 80
    door_h = base_h - 200
    
    for i in range(3):
        dx = 60 + (i * (door_w + 80))
        make_box(doc, f"Door_{i}", door_w, 40, door_h, dx, -40, 300, col_body, offset_coords)
        
        # Grid Pattern on doors (Simulated with small boxes)
        grid_rows = 5
        grid_cols = 5
        gw = (door_w - 80) / grid_cols
        gh = (door_h - 80) / grid_rows
        
        for r in range(grid_rows):
            for c in range(grid_cols):
                gx = dx + 40 + (c * gw)
                gz = 340 + (r * gh)
                # Drawing "holes" as dark squares
                make_box(doc, f"Grid_{i}_{r}_{c}", gw-10, 10, gh-10, gx, -44, gz, col_dark, offset_coords)
        
        # Door Handle
        make_cylinder(doc, f"Handle_{i}", 10, 120, dx + door_w - 60, -60, 900, col_steel, offset_coords, axis=App.Vector(0,0,1))

    # Handwheel on middle door
    make_cylinder(doc, "Handwheel_Main", 80, 40, base_w/2, -80, 1200, col_dark, offset_coords, axis=App.Vector(0,1,0))

    # Feet
    feet_pos = [200, base_w/2, base_w-200]
    for fx in feet_pos:
        make_cylinder(doc, f"Foot_F_{int(fx)}", 80, 200, fx, 200, 0, col_steel, offset_coords, axis=App.Vector(0,0,1))
        make_cylinder(doc, f"Foot_B_{int(fx)}", 80, 200, fx, base_d-200, 0, col_steel, offset_coords, axis=App.Vector(0,0,1))

    # ==========================================================================
    # 2. CONVEYOR TABLE (Right Side)
    # ==========================================================================
    conv_x = 1200
    conv_w = base_w - 1300
    conv_d = base_d - 400
    
    # Conveyor Bed
    make_box(doc, "Conveyor_Bed", conv_w, conv_d, 100, conv_x, 200, base_h + 200, col_body, offset_coords)
    # The Belt Surface
    make_box(doc, "Conveyor_Belt", conv_w - 40, conv_d - 40, 10, conv_x + 20, 220, base_h + 300, col_dark, offset_coords)
    
    # Side Rails
    make_box(doc, "Rail_F", conv_w, 40, 120, conv_x, 200, base_h + 300, col_steel, offset_coords)
    make_box(doc, "Rail_B", conv_w, 40, 120, conv_x, base_d - 240, base_h + 300, col_steel, offset_coords)
    
    # Adjustable Guide Bars on Conveyor
    make_box(doc, "Guide_Bar_1", conv_d - 200, 20, 20, conv_x + 600, 300, base_h + 320, col_steel, offset_coords, rotation_angle=30, rotation_axis=App.Vector(0,0,1))
    make_box(doc, "Guide_Bar_2", conv_d - 200, 20, 20, conv_x + 1200, 300, base_h + 320, col_steel, offset_coords, rotation_angle=-30, rotation_axis=App.Vector(0,0,1))

    # ==========================================================================
    # 3. CUTTING HEAD UNIT (Left Side)
    # ==========================================================================
    head_w = 1200
    head_d = base_d
    head_h = 1000
    
    # Safety Cover (Transparent)
    # Main arched cover
    make_box(doc, "Safety_Cover_L", 40, head_d - 200, head_h, 0, 100, base_h + 200, col_trans, offset_coords)
    make_box(doc, "Safety_Cover_R", 40, head_d - 200, head_h, head_w, 100, base_h + 200, col_trans, offset_coords)
    make_box(doc, "Safety_Cover_Top", head_w, head_d - 200, 40, 0, 100, base_h + 200 + head_h, col_trans, offset_coords)
    # Front curved sheet approx
    make_box(doc, "Safety_Cover_Front", head_w, 40, head_h, 0, 100, base_h + 200, col_trans, offset_coords, rotation_angle=15, rotation_axis=App.Vector(1,0,0))
    
    # Internal Mechanism (Abstracted)
    make_box(doc, "Cutter_Mech", 600, 800, 800, 300, 400, base_h + 200, col_dark, offset_coords)
    make_cylinder(doc, "Cutter_Piston", 80, 400, 600, 800, base_h + 1000, col_steel, offset_coords, axis=App.Vector(0,0,1))

    # Handle Bar across front
    make_cylinder(doc, "Handle_Bar", 30, head_w + 200, -100, 80, base_h + 600, col_steel, offset_coords, axis=App.Vector(1,0,0))

    # ==========================================================================
    # 4. TOP ROLL FEED & CONTROL UNIT
    # ==========================================================================
    # Vertical Posts holding the top structure
    make_box(doc, "Post_R", 200, 200, 2000, base_w - 300, base_d - 300, base_h + 200, col_body, offset_coords)
    
    # Top Cross Structure (Roll Holder)
    top_y = base_d - 500
    top_z = base_h + 1600
    
    make_box(doc, "Roll_Frame_R", 100, 1200, 800, base_w - 300, top_y - 1200, top_z, col_body, offset_coords)
    make_box(doc, "Roll_Frame_L", 100, 1200, 800, 1200, top_y - 1200, top_z, col_body, offset_coords)
    
    # Rollers (Black/Silver with Red clips)
    roll_x_start = 1300
    roll_len = base_w - 1700
    
    # Top Roll
    make_cylinder(doc, "Feed_Roll_1", 80, roll_len, roll_x_start, top_y - 200, top_z + 600, col_dark, offset_coords, axis=App.Vector(1,0,0))
    # Bottom Roll
    make_cylinder(doc, "Feed_Roll_2", 80, roll_len, roll_x_start, top_y - 600, top_z + 200, col_dark, offset_coords, axis=App.Vector(1,0,0))
    
    # Red Clips/Guides on Top Roll
    for i in range(4):
        cx = roll_x_start + 200 + (i * 500)
        make_cylinder(doc, f"Red_Clip_{i}", 100, 60, cx, top_y - 200, top_z + 600, col_red, offset_coords, axis=App.Vector(1,0,0))

    # ==========================================================================
    # 5. CONTROL PANEL (Top Left)
    # ==========================================================================
    panel_x = 800
    panel_z = base_h + 1800
    
    # Panel Box
    make_box(doc, "Control_Box", 1000, 400, 600, panel_x, 100, panel_z, col_panel, offset_coords)
    
    # Screen (Black Rectangle)
    make_box(doc, "Screen", 400, 20, 300, panel_x + 300, 90, panel_z + 150, col_dark, offset_coords)
    
    # Buttons
    # Top Row
    make_cylinder(doc, "Btn_1", 30, 20, panel_x + 100, 90, panel_z + 500, col_red, offset_coords, axis=App.Vector(0,1,0))
    make_cylinder(doc, "Btn_2", 30, 20, panel_x + 200, 90, panel_z + 500, col_yellow, offset_coords, axis=App.Vector(0,1,0))
    # Bottom Row
    make_cylinder(doc, "Btn_3", 30, 20, panel_x + 100, 90, panel_z + 100, col_green, offset_coords, axis=App.Vector(0,1,0))
    make_cylinder(doc, "Btn_4", 30, 20, panel_x + 200, 90, panel_z + 100, col_yellow, offset_coords, axis=App.Vector(0,1,0))
    make_cylinder(doc, "Btn_5", 30, 20, panel_x + 800, 90, panel_z + 100, col_red, offset_coords, axis=App.Vector(0,1,0))


# ==============================================================================
# MAIN DRAWING FUNCTION FOR THE STACKING MACHINE
# ==============================================================================

def draw_battery_stacker(doc, offset_coords=(0,0,0)):
    # -- Colors --
    col_white  = (0.95, 0.95, 0.95)
    col_base   = (0.93, 0.93, 0.91)
    col_blue   = (0.10, 0.45, 0.85)
    col_dark   = (0.15, 0.15, 0.15)
    col_steel  = (0.75, 0.75, 0.75)
    col_alum   = (0.85, 0.85, 0.85)

    # -- Dimensions (Scaled x3) --
    base_w = 6600
    base_d = 6800
    base_h = 2100
    table_z = base_h

    # ==========================================================================
    # 1. BASE CABINET
    # ==========================================================================
    make_box(doc, "Base_Cabinet", base_w, base_d, base_h, 0, 0, 0, col_base, offset_coords)
    make_box(doc, "Table_Plate", base_w + 150, base_d + 150, 60, -75, -75, base_h, col_steel, offset_coords)

    door_w = 1500
    door_h = 1500
    door_y = -15

    # Right Doors
    make_box(doc, "Door_R1", door_w, 60, door_h, 3600, door_y, 300, col_white, offset_coords)
    make_box(doc, "Door_R2", door_w, 60, door_h, 5130, door_y, 300, col_white, offset_coords)
    make_box(doc, "Handle_R1", 60, 30, 300, 4950, door_y-30, 900, col_dark, offset_coords)
    make_box(doc, "Handle_R2", 60, 30, 300, 5250, door_y-30, 900, col_dark, offset_coords)

    # Left Doors
    make_box(doc, "Door_L1", door_w, 60, door_h, 300, door_y, 300, col_white, offset_coords)
    make_box(doc, "Door_L2", door_w, 60, door_h, 1830, door_y, 300, col_white, offset_coords)
    make_box(doc, "Handle_L1", 60, 30, 300, 1650, door_y-30, 900, col_dark, offset_coords)
    make_box(doc, "Handle_L2", 60, 30, 300, 1950, door_y-30, 900, col_dark, offset_coords)

    # Side Vent
    make_cylinder(doc, "Vent_Fan", 180, 60, -30, base_d/2, 1050, col_dark, offset_coords, axis=App.Vector(0,1,0))
    make_box(doc, "Slot_1", 60, 450, 120, -30, base_d/2 - 600, 600, col_dark, offset_coords)
    make_box(doc, "Slot_2", 60, 450, 120, -30, base_d/2 + 150, 600, col_dark, offset_coords)

    # Feet
    feet_pos = [
        (300, 300), (base_w-300, 300),
        (300, base_d-300), (base_w-300, base_d-300),
        (base_w/2, 300), (base_w/2, base_d-300)
    ]

    for i, (fx, fy) in enumerate(feet_pos):
        make_cylinder(doc, f"Foot_{i}", 120, 300, fx, fy, -300, col_dark, offset_coords)
        make_cylinder(doc, f"Foot_Plate_{i}", 180, 60, fx, fy, -300, col_steel, offset_coords)

    # ==========================================================================
    # 2. GANTRY STRUCTURE
    # ==========================================================================
    col_w = 450
    col_h = 3000
    col_y_offset = 900

    make_box(doc, "Col_FL", col_w, col_w, col_h, 1200, col_y_offset, table_z, col_white, offset_coords)
    make_box(doc, "Col_FR", col_w, col_w, col_h, 4200, col_y_offset, table_z, col_white, offset_coords)
    make_box(doc, "Col_BL", col_w, col_w, col_h, 1200, base_d - col_y_offset - col_w, table_z, col_white, offset_coords)
    make_box(doc, "Col_BR", col_w, col_w, col_h, 4200, base_d - col_y_offset - col_w, table_z, col_white, offset_coords)

    make_box(doc, "Brace_FL", 60, 900, 900, 1650, col_y_offset, table_z + col_h - 900, col_white, offset_coords)
    make_box(doc, "Brace_FR", 60, 900, 900, 4140, col_y_offset, table_z + col_h - 900, col_white, offset_coords)

    make_box(doc, "Top_Beam_F", 4800, 600, 300, 600, col_y_offset - 75, table_z + col_h, col_alum, offset_coords)
    make_box(doc, "Top_Beam_B", 4800, 600, 300, 600, base_d - col_y_offset - 375, table_z + col_h, col_alum, offset_coords)

    for i in range(3):
        ry = col_y_offset + (i * 900)
        make_box(doc, f"Cross_Rail_{i}", 4800, 300, 150, 600, ry, table_z + col_h + 300, col_steel, offset_coords)

    # ==========================================================================
    # 3. OVERHEAD ACTUATORS
    # ==========================================================================
    actuator_x = [1800, 3600]
    actuator_z = table_z + col_h + 450

    for i, ax in enumerate(actuator_x):
        make_box(doc, f"Act_Bracket_{i}", 900, 1200, 150, ax - 450, base_d/2 - 600, actuator_z, col_white, offset_coords)
        make_cylinder(doc, f"Act_Motor_{i}", 180, 900, ax, base_d/2, actuator_z + 150, col_dark, offset_coords)
        make_box(doc, f"Act_Mech_{i}", 300, 300, 600, ax + 240, base_d/2 - 150, actuator_z + 150, col_white, offset_coords)

    # ==========================================================================
    # 4. UNWIND STATIONS (Left & Right)
    # ==========================================================================
    # --- Left Unwinder ---
    uw_l_x = 300
    uw_l_y = base_d / 2
    uw_z_center = table_z + 1800

    make_box(doc, "UW_Plate_L", 60, 1200, 1800, uw_l_x, uw_l_y - 600, table_z + 600, col_white, offset_coords)
    make_cylinder(doc, "Roll_L", 450, 600, uw_l_x - 600, uw_l_y, uw_z_center, col_blue, offset_coords, axis=App.Vector(1,0,0))
    make_cylinder(doc, "Motor_L", 150, 450, uw_l_x + 60, uw_l_y, uw_z_center, col_dark, offset_coords, axis=App.Vector(1,0,0))
    make_cylinder(doc, "Tens_L1", 60, 750, uw_l_x - 450, uw_l_y + 300, uw_z_center - 600, col_steel, offset_coords, axis=App.Vector(1,0,0))
    make_cylinder(doc, "Tens_L2", 60, 750, uw_l_x - 450, uw_l_y - 300, uw_z_center - 600, col_steel, offset_coords, axis=App.Vector(1,0,0))

    # --- Right Unwinder ---
    uw_r_x = base_w - 360

    make_box(doc, "UW_Plate_R", 60, 1200, 1800, uw_r_x, uw_l_y - 600, table_z + 600, col_white, offset_coords)
    make_cylinder(doc, "Roll_R", 450, 600, uw_r_x + 60, uw_l_y, uw_z_center, col_blue, offset_coords, axis=App.Vector(1,0,0))
    make_cylinder(doc, "Motor_R", 150, 450, uw_r_x - 450, uw_l_y, uw_z_center, col_dark, offset_coords, axis=App.Vector(1,0,0))
    make_cylinder(doc, "Tens_R1", 60, 750, uw_r_x - 150, uw_l_y + 300, uw_z_center - 600, col_steel, offset_coords, axis=App.Vector(1,0,0))
    make_cylinder(doc, "Tens_R2", 60, 750, uw_r_x - 150, uw_l_y - 300, uw_z_center - 600, col_steel, offset_coords, axis=App.Vector(1,0,0))

    # ==========================================================================
    # 5. INTERNAL MECHANISMS
    # ==========================================================================
    num_heads = 4
    spacing = 1050
    start_x = 1800
    center_y = base_d / 2

    for i in range(num_heads):
        hx = start_x + (i * spacing)
        make_box(doc, f"Head_Guide_{i}", 300, 300, 900, hx, center_y - 150, table_z + 300, col_white, offset_coords)
        make_box(doc, f"Head_Block_{i}", 750, 450, 240, hx - 225, center_y - 225, table_z + 750, col_blue, offset_coords)
        make_box(doc, f"Die_Block_{i}", 450, 450, 300, hx - 75, center_y - 225, table_z + 60, col_blue, offset_coords)
        make_cylinder(doc, f"Head_Pneu_{i}", 60, 300, hx + 150, center_y, table_z + 990, col_dark, offset_coords, axis=App.Vector(0,0,1))


# ==============================================================================
# MAIN DRAWING FUNCTION FOR THE HOT PRESSING MACHINE
# ==============================================================================

def draw_processing_machine(doc, offset_coords=(0,0,0)):
    # -- Colors --
    col_frame   = (0.90, 0.90, 0.90) # White/Light Grey Enclosure
    col_trim    = (0.70, 0.75, 0.75) # Greenish/Grey Trim
    col_panel   = (0.60, 0.60, 0.65) # Control Panel Face
    col_window  = (0.10, 0.10, 0.10) # Dark Glass
    col_steel   = (0.80, 0.80, 0.80) # Table/Metal
    col_black   = (0.15, 0.15, 0.15) # Black details (Hinges, Knobs)
    col_red     = (0.80, 0.10, 0.10) # Red buttons
    col_wheel   = (0.30, 0.10, 0.10) # Reddish wheels

    # -- Dimensions (Scaled x3) --
    total_w = 4800 # 1600 * 3
    total_d = 2400 # 800 * 3
    base_h = 2100 # 700 * 3
    upper_h = 2400 # 800 * 3
    
    # ==========================================================================
    # 1. BASE CABINET
    # ==========================================================================
    # Main lower body
    make_box(doc, "Base_Body", total_w, total_d, base_h, 0, 0, 300, col_frame, offset_coords)
    
    # Trim/Frame outline
    # Bottom Frame
    make_box(doc, "Frame_Bot", total_w, total_d, 120, 0, 0, 300, col_trim, offset_coords)
    # Top of Base Frame
    make_box(doc, "Frame_Mid", total_w, total_d, 120, 0, 0, 300 + base_h - 120, col_trim, offset_coords)
    # Vertical Dividers
    make_box(doc, "Frame_Vert_L", 120, total_d, base_h, 0, 0, 300, col_trim, offset_coords)
    make_box(doc, "Frame_Vert_M", 120, total_d, base_h, total_w/2, 0, 300, col_trim, offset_coords)
    make_box(doc, "Frame_Vert_R", 120, total_d, base_h, total_w-120, 0, 300, col_trim, offset_coords)

    # Lower Doors
    door_w = (total_w / 2) - 180
    door_h = base_h - 300
    
    # Left Lower Door
    make_box(doc, "Door_Low_L", door_w, 60, door_h, 150, -30, 450, col_frame, offset_coords)
    make_box(doc, "Handle_Low_L", 30, 60, 240, 150 + door_w - 120, -75, 1200, col_black, offset_coords)
    
    # Right Lower Door
    make_box(doc, "Door_Low_R", door_w, 60, door_h, (total_w/2) + 150, -30, 450, col_frame, offset_coords)
    make_box(doc, "Handle_Low_R", 30, 60, 240, (total_w/2) + 150 + 120, -75, 1200, col_black, offset_coords)

    # Hinges
    hinge_z = [600, 1800]
    for z in hinge_z:
        make_box(doc, f"Hinge_LL_{z}", 60, 75, 90, 90, -36, z, col_black, offset_coords)
        make_box(doc, f"Hinge_LR_{z}", 60, 75, 90, total_w - 150, -36, z, col_black, offset_coords)

    # ==========================================================================
    # 2. UPPER LEFT SECTION (Process Chamber)
    # ==========================================================================
    ul_w = total_w * 0.55
    ul_h = upper_h
    start_z = 300 + base_h
    
    # Main Box
    make_box(doc, "Upper_L_Body", ul_w, total_d, ul_h, 0, 0, start_z, col_frame, offset_coords)
    
    # Frame Trim
    make_box(doc, "UL_Frame_Top", ul_w, total_d, 120, 0, 0, start_z + ul_h - 120, col_trim, offset_coords)
    make_box(doc, "UL_Frame_Mid", 120, total_d, ul_h, ul_w/2 - 60, 0, start_z, col_trim, offset_coords)
    
    # Upper Doors
    u_door_w = (ul_w / 2) - 120
    u_door_h = ul_h - 240
    
    # Upper Door Left
    make_box(doc, "U_Door_L", u_door_w, 60, u_door_h, 90, -30, start_z + 120, col_frame, offset_coords)
    # Upper Door Right
    make_box(doc, "U_Door_R", u_door_w, 60, u_door_h, (ul_w/2) + 60, -30, start_z + 120, col_frame, offset_coords)
    
    # Handles
    make_box(doc, "U_Handle_L", 30, 60, 240, 90 + u_door_w - 90, -75, start_z + 900, col_black, offset_coords)
    make_box(doc, "U_Handle_R", 30, 60, 240, (ul_w/2) + 150, -75, start_z + 900, col_black, offset_coords)

    # Oval Windows
    win_w = 360
    win_h = 900
    win_z_center = start_z + 1200
    
    # Window Left
    wx_l = 90 + (u_door_w/2) - (win_w/2)
    make_box(doc, "Win_Box_L", win_w, 15, win_h, wx_l, -36, win_z_center - win_h/2, col_window, offset_coords)
    make_cylinder(doc, "Win_Top_L", win_w/2, 15, wx_l + win_w/2, -36, win_z_center + win_h/2, col_window, offset_coords, axis=App.Vector(1,0,0))
    make_cylinder(doc, "Win_Bot_L", win_w/2, 15, wx_l + win_w/2, -36, win_z_center - win_h/2, col_window, offset_coords, axis=App.Vector(1,0,0))
    
    # Window Right
    wx_r = (ul_w/2) + 60 + (u_door_w/2) - (win_w/2)
    make_box(doc, "Win_Box_R", win_w, 15, win_h, wx_r, -36, win_z_center - win_h/2, col_window, offset_coords)
    make_cylinder(doc, "Win_Top_R", win_w/2, 15, wx_r + win_w/2, -36, win_z_center + win_h/2, col_window, offset_coords, axis=App.Vector(1,0,0))
    make_cylinder(doc, "Win_Bot_R", win_w/2, 15, wx_r + win_w/2, -36, win_z_center - win_h/2, col_window, offset_coords, axis=App.Vector(1,0,0))

    # ==========================================================================
    # 3. UPPER RIGHT SECTION (Control Panel)
    # ==========================================================================
    ur_w = total_w - ul_w
    ur_x = ul_w
    
    # Main Control Box
    make_box(doc, "Control_Box", ur_w, total_d, ul_h, ur_x, 0, start_z, col_panel, offset_coords)
    
    # Trim
    make_box(doc, "UR_Frame_Top", ur_w, total_d, 120, ur_x, 0, start_z + ul_h - 120, col_trim, offset_coords)
    
    # Panel Elements
    # Top Row: Small Displays
    for i in range(3):
        make_box(doc, f"Disp_Top_{i}", 240, 30, 150, ur_x + 240 + (i*450), -30, start_z + 1950, col_frame, offset_coords)
        make_box(doc, f"Disp_Screen_{i}", 180, 15, 90, ur_x + 270 + (i*450), -36, start_z + 1980, col_window, offset_coords)

    # Middle Row: Larger Displays/Controllers
    for i in range(3):
        make_box(doc, f"Disp_Mid_{i}", 300, 30, 180, ur_x + 210 + (i*450), -30, start_z + 1500, col_frame, offset_coords)
        make_box(doc, f"Disp_Screen_M_{i}", 240, 15, 120, ur_x + 240 + (i*450), -36, start_z + 1530, col_window, offset_coords)

    # Touch Screen (Center)
    make_box(doc, "Touch_Screen_Bezel", 450, 30, 300, ur_x + 750, -30, start_z + 900, col_frame, offset_coords)
    make_box(doc, "Touch_Screen", 390, 15, 240, ur_x + 780, -36, start_z + 930, (0.2, 0.2, 0.4), offset_coords)

    # Knobs (Black)
    make_cylinder(doc, "Knob_L", 60, 60, ur_x + 300, -60, start_z + 1050, col_black, offset_coords, axis=App.Vector(0,1,0))
    make_cylinder(doc, "Knob_R", 60, 60, ur_x + 1800, -60, start_z + 1050, col_black, offset_coords, axis=App.Vector(0,1,0))

    # Button Row (Red/Green)
    for i in range(4):
        bx = ur_x + 750 + (i*120)
        col = col_red if i % 2 == 0 else (0.1, 0.8, 0.1)
        make_cylinder(doc, f"Btn_{i}", 30, 30, bx, -45, start_z + 600, col, offset_coords, axis=App.Vector(0,1,0))

    # ==========================================================================
    # 4. RIGHT EXTENSION TABLE (Output)
    # ==========================================================================
    tbl_w = 1800
    tbl_d = total_d - 300
    tbl_x = total_w
    tbl_z = start_z - 450
    
    # Table surface
    make_box(doc, "Table_Surf", tbl_w, tbl_d, 60, tbl_x, 150, tbl_z, col_steel, offset_coords)
    # Frame/Rail of table
    make_box(doc, "Table_Rail_F", tbl_w, 60, 120, tbl_x, 150, tbl_z, col_black, offset_coords)
    make_box(doc, "Table_Rail_B", tbl_w, 60, 120, tbl_x, total_d-150, tbl_z, col_black, offset_coords)
    
    # Internal Mechanism
    make_cylinder(doc, "Int_Motor_1", 180, 600, ur_x + 300, 600, start_z - 600, col_black, offset_coords, axis=App.Vector(1,0,0))
    make_cylinder(doc, "Int_Motor_2", 180, 600, ur_x + 300, 1500, start_z - 600, col_black, offset_coords, axis=App.Vector(1,0,0))

    # ==========================================================================
    # 5. LEFT SHELF
    # ==========================================================================
    shelf_w = 600
    make_box(doc, "Shelf_L", shelf_w, total_d, 60, -shelf_w, 0, start_z, col_steel, offset_coords)

    # ==========================================================================
    # 6. WHEELS & FEET
    # ==========================================================================
    wheel_rad = 120
    
    # Wheels
    wheel_pos = [(300, 300), (total_w-300, 300), (300, total_d-300), (total_w-300, total_d-300)]
    for i, (wx, wy) in enumerate(wheel_pos):
        make_cylinder(doc, f"Wheel_{i}", wheel_rad, 90, wx, wy, wheel_rad, col_wheel, offset_coords, axis=App.Vector(0,1,0))
        make_box(doc, f"Wheel_Brack_{i}", 180, 180, 120, wx-90, wy-90, wheel_rad*2, col_steel, offset_coords)

    # Feet
    feet_pos = [(total_w/2, 300), (total_w/2, total_d-300)]
    for i, (fx, fy) in enumerate(feet_pos):
        make_cylinder(doc, f"Level_Foot_{i}", 60, 240, fx, fy, 0, col_black, offset_coords)
        make_cylinder(doc, f"Level_Pad_{i}", 120, 30, fx, fy, 0, col_black, offset_coords)



# ==============================================================================
# MAIN DRAWING FUNCTION FOR ULTRASONIC WELDING MACHINE
# ==============================================================================

def draw_assembly_machine(doc, offset_coords=(0,0,0)):

    col_base    = (0.95, 0.95, 0.95)
    col_frame   = (0.75, 0.75, 0.75)
    col_glass   = (0.85, 0.90, 0.95)
    col_dark    = (0.20, 0.20, 0.20)
    col_panel   = (0.90, 0.90, 0.90)
    col_screen  = (0.10, 0.10, 0.10)
    col_red     = (0.80, 0.10, 0.10)
    col_yellow  = (0.95, 0.85, 0.10)
    col_green   = (0.10, 0.80, 0.10)
    col_steel   = (0.60, 0.60, 0.65)

    # -- Dimensions ×2 --
    machine_l = 8000
    machine_w = 4000
    base_h    = 1600
    cage_h    = 2800
    total_h   = base_h + cage_h
    frame_th  = 120

    # ==========================================================================
    # 1. BASE CABINET
    # ==========================================================================
    make_box(doc, "Base_Cabinet", machine_l, machine_w, base_h, 0, 0, 0, col_base, offset_coords)

    num_vents = 8
    vent_spacing = machine_l / num_vents
    for i in range(num_vents):
        vx = 400 + (i * vent_spacing)
        make_box(doc, f"Vent_{i}", 400, 20, 400, vx, -10, base_h/2 - 200, col_dark, offset_coords)

    num_feet_x = 5
    for i in range(num_feet_x):
        fx = 200 + (i * (machine_l / (num_feet_x-1)))
        make_cylinder(doc, f"Foot_F_{i}", 80, 200, fx, 200, -200, col_dark, offset_coords)
        make_cylinder(doc, f"Foot_B_{i}", 80, 200, fx, machine_w - 200, -200, col_dark, offset_coords)

    # ==========================================================================
    # 2. SAFETY ENCLOSURE
    # ==========================================================================
    num_posts = 5
    post_spacing = machine_l / (num_posts - 1)

    for i in range(num_posts):
        px = i * post_spacing
        make_box(doc, f"Post_F_{i}", frame_th, frame_th, cage_h, px, 0, base_h, col_frame, offset_coords)
        make_box(doc, f"Post_B_{i}", frame_th, frame_th, cage_h, px, machine_w - frame_th, base_h, col_frame, offset_coords)
        make_box(doc, f"Beam_Cross_{i}", frame_th, machine_w, frame_th, px, 0, total_h, col_frame, offset_coords)

    make_box(doc, "Rail_Top_F", machine_l, frame_th, frame_th, 0, 0, total_h, col_frame, offset_coords)
    make_box(doc, "Rail_Mid_F", machine_l, frame_th, frame_th, 0, 0, base_h + cage_h/2, col_frame, offset_coords)
    make_box(doc, "Rail_Top_B", machine_l, frame_th, frame_th, 0, machine_w - frame_th, total_h, col_frame, offset_coords)

    for i in range(num_posts - 1):
        wx = (i * post_spacing) + frame_th
        w_width = post_spacing - frame_th
        if i != 2:
            make_box(doc, f"Glass_F_{i}", w_width, 20, cage_h - 40, wx, 20, base_h + 20, col_glass, offset_coords)
        make_box(doc, f"Glass_B_{i}", w_width, 20, cage_h - 40, wx, machine_w - 40, base_h + 20, col_glass, offset_coords)
        make_box(doc, f"Glass_Top_{i}", w_width, machine_w - frame_th*2, 20, wx, frame_th, total_h, col_glass, offset_coords)

    make_box(doc, "Glass_L", 20, machine_w, cage_h, 20, 0, base_h, col_glass, offset_coords)
    make_box(doc, "Glass_R", 20, machine_w, cage_h, machine_l - 40, 0, base_h, col_glass, offset_coords)

    # ==========================================================================
    # 3. CONTROL PANEL
    # ==========================================================================
    panel_w = 1200
    panel_h = 1600
    panel_d = 400
    panel_x = machine_l / 2 + 400
    panel_z = base_h + 600

    make_box(doc, "Control_Box", panel_w, panel_d, panel_h, panel_x, -panel_d/2, panel_z, col_panel, offset_coords)
    make_box(doc, "HMI_Screen", 600, 20, 400, panel_x + 300, -panel_d/2 - 10, panel_z + 900, col_screen, offset_coords)

    make_cylinder(doc, "Btn_EStop", 50, 40, panel_x + 900, -panel_d/2 - 30, panel_z + 550, col_red, offset_coords, axis=App.Vector(0,1,0))
    make_cylinder(doc, "Btn_Start", 30, 40, panel_x + 300, -panel_d/2 - 30, panel_z + 550, col_green, offset_coords, axis=App.Vector(0,1,0))
    make_cylinder(doc, "Btn_Stop", 30, 40, panel_x + 400, -panel_d/2 - 30, panel_z + 550, col_dark, offset_coords, axis=App.Vector(0,1,0))

    # ==========================================================================
    # 4. INTERNAL MECHANISMS
    # ==========================================================================
    make_box(doc, "Internal_Rail", machine_l - 400, 200, 100, 200, machine_w/2, base_h + 1200, col_frame, offset_coords)

    num_stations = 4
    for i in range(num_stations):
        sx = 1000 + (i * 1600)
        make_box(doc, f"Z_Axis_{i}", 200, 200, 800, sx, machine_w/2, base_h + 400, col_steel, offset_coords)
        make_cylinder(doc, f"Tool_Head_{i}", 80, 200, sx + 100, machine_w/2 + 100, base_h + 300, col_dark, offset_coords)
        make_box(doc, f"Station_Base_{i}", 400, 400, 40, sx - 100, machine_w/2 - 100, base_h, col_steel, offset_coords)

    make_box(doc, "Internal_Conveyor", machine_l, 800, 20, 0, machine_w/2 - 200, base_h + 10, col_dark, offset_coords)


# ==============================================================================
# MAIN DRAWING FUNCTION  FOR THE LASER WELDING MACHINE
# ==============================================================================

def draw_laser_welding_machine(doc, offset_coords=(0,0,0)):
    # -- Colors --
    col_white   = (0.95, 0.95, 0.95)
    col_beige   = (0.90, 0.85, 0.75)
    col_orange  = (1.00, 0.55, 0.00)
    col_steel   = (0.75, 0.75, 0.75)
    col_dark    = (0.15, 0.15, 0.15)
    col_screen  = (0.10, 0.10, 0.30)
    col_blue    = (0.00, 0.40, 0.90)
    col_red     = (0.80, 0.10, 0.10)
    col_green   = (0.10, 0.80, 0.10)

    # -- Dimensions (Original * 3) --
    main_w = 3600 # 1200 * 3
    main_d = 3000 # 1000 * 3
    base_h = 2400 # 800 * 3
    table_z = base_h
    
    # ==========================================================================
    # 1. MAIN MACHINE BASE
    # ==========================================================================
    make_box(doc, "Main_Base", main_w, main_d, base_h, 0, 0, 0, col_white, offset_coords)
    
    # Front Control Console
    make_box(doc, "Front_Console", main_w, 450, 300, 0, -450, base_h - 300, col_white, offset_coords)
    
    # Buttons
    btn_y = -300
    btn_z = base_h - 150
    make_cylinder(doc, "Btn_EStop", 75, 60, 300, btn_y, btn_z, col_red, offset_coords, axis=App.Vector(0,0,1))
    make_cylinder(doc, "Btn_Start", 45, 60, 600, btn_y, btn_z, col_green, offset_coords, axis=App.Vector(0,0,1))
    make_cylinder(doc, "Btn_Stop", 45, 60, 900, btn_y, btn_z, col_red, offset_coords, axis=App.Vector(0,0,1))
    make_cylinder(doc, "Btn_Reset", 45, 60, 1200, btn_y, btn_z, col_dark, offset_coords, axis=App.Vector(0,0,1))

    # Feet
    feet_x = [300, main_w-300]
    feet_y = [300, main_d-300]
    for fx in feet_x:
        for fy in feet_y:
            make_cylinder(doc, f"Foot_{fx}_{fy}", 90, 240, fx, fy, -240, col_dark, offset_coords)
            make_cylinder(doc, f"Foot_Pad_{fx}_{fy}", 150, 30, fx, fy, -240, col_steel, offset_coords)

    # ==========================================================================
    # 2. WORKSTATION & FIXTURES
    # ==========================================================================
    plate_th = 60
    make_box(doc, "Fixture_Plate", main_w - 300, main_d - 600, plate_th, 150, 150, table_z, col_orange, offset_coords)
    
    # Fixtures Grid
    rows = 6
    cols = 10
    start_x = 300
    start_y = 300
    spacing_x = 300
    spacing_y = 360
    
    for r in range(rows):
        for c in range(cols):
            cx = start_x + (c * spacing_x)
            cy = start_y + (r * spacing_y)
            make_cylinder(doc, f"Cell_{r}_{c}", 60, 180, cx, cy, table_z + plate_th, col_steel, offset_coords)
            make_cylinder(doc, f"Cell_Tip_{r}_{c}", 15, 30, cx, cy, table_z + plate_th + 180, col_blue, offset_coords)

    make_box(doc, "Clamp_L", 150, 1200, 300, 150, 600, table_z + plate_th, col_steel, offset_coords)
    make_cylinder(doc, "Clamp_Lever_L", 30, 450, 225, 1200, table_z + plate_th + 300, col_dark, offset_coords)

    # ==========================================================================
    # 3. GANTRY & LASER SYSTEM
    # ==========================================================================
    gantry_h = 2400
    post_w = 360
    
    make_box(doc, "Gantry_Col_L", post_w, 600, gantry_h, 150, main_d - 750, table_z, col_steel, offset_coords)
    make_box(doc, "Gantry_Col_R", post_w, 600, gantry_h, main_w - 510, main_d - 750, table_z, col_steel, offset_coords)
    
    beam_z = table_z + gantry_h - 450
    make_box(doc, "Cross_Beam", main_w, 450, 450, 0, main_d - 675, beam_z, col_steel, offset_coords)
    
    head_x = main_w / 2
    make_box(doc, "Laser_Carriage", 450, 600, 60, head_x - 225, main_d - 750, beam_z, col_dark, offset_coords)
    make_box(doc, "Z_Slide", 360, 360, 1200, head_x - 180, main_d - 1050, beam_z - 600, col_steel, offset_coords)
    
    make_box(doc, "Laser_Head_Box", 300, 450, 600, head_x - 150, main_d - 1140, beam_z - 600, col_white, offset_coords)
    make_cylinder(doc, "Laser_Nozzle", 45, 300, head_x, main_d - 900, beam_z - 900, col_dark, offset_coords)
    
    make_cylinder(doc, "Cable_Chain", 90, 1200, head_x, main_d - 300, beam_z + 450, col_dark, offset_coords)

    # ==========================================================================
    # 4. MONITOR ARM
    # ==========================================================================
    arm_h = table_z + 1200
    make_cylinder(doc, "Monitor_Pole", 60, 1200, main_w - 150, main_d - 300, table_z, col_steel, offset_coords)
    make_box(doc, "Monitor_Arm", 900, 60, 60, main_w - 150, main_d - 300, arm_h, col_steel, offset_coords, rotation_angle=45, rotation_axis=App.Vector(0,0,1))
    
    screen_x = main_w + 450
    screen_y = main_d - 900
    make_box(doc, "Monitor_Case", 60, 1200, 750, screen_x, screen_y, arm_h - 300, col_dark, offset_coords)
    make_box(doc, "Monitor_Face", 15, 1140, 690, screen_x - 15, screen_y + 30, arm_h - 270, col_screen, offset_coords)

    # ==========================================================================
    # 5. CHILLER UNIT (Right Side)
    # ==========================================================================
    chiller_x = main_w + 900
    chiller_w = 1800
    chiller_d = 2400
    chiller_h = 3000
    
    make_box(doc, "Chiller_Body", chiller_w, chiller_d, chiller_h, chiller_x, 0, 150, col_beige, offset_coords)
    
    for i in range(10):
        gz = 450 + (i * 180)
        make_box(doc, f"Chiller_Grille_{i}", chiller_w - 300, 15, 120, chiller_x + 150, -15, gz, col_dark, offset_coords)
        
    make_cylinder(doc, "Chiller_Fan_Guard", 600, 60, chiller_x + chiller_w/2, chiller_d/2, 150 + chiller_h, col_dark, offset_coords)
    
    make_cylinder(doc, "Hose_1", 60, 1200, chiller_x, 300, 600, col_blue, offset_coords, axis=App.Vector(1,0,0))
    make_cylinder(doc, "Hose_2", 60, 1200, chiller_x, 600, 600, col_red, offset_coords, axis=App.Vector(1,0,0))
    
    make_cylinder(doc, "Chiller_Wheel_FL", 90, 150, chiller_x + 150, 150, 0, col_dark, offset_coords, axis=App.Vector(0,1,0))
    make_cylinder(doc, "Chiller_Wheel_FR", 90, 150, chiller_x + chiller_w - 150, 150, 0, col_dark, offset_coords, axis=App.Vector(0,1,0))

    # ==========================================================================
    # 6. FUME EXTRACTOR (Left Side)
    # ==========================================================================
    ext_x = -1500
    ext_w = 1200
    ext_d = 1200
    ext_h = 1500
    
    make_box(doc, "Extractor_Body", ext_w, ext_d, ext_h, ext_x, 0, 0, col_white, offset_coords)
    make_box(doc, "Extractor_Top", ext_w, ext_d, 150, ext_x, 0, ext_h, col_blue, offset_coords)
    
    make_cylinder(doc, "Flex_Hose_1", 120, 1800, ext_x + ext_w/2, ext_d/2, ext_h, col_dark, offset_coords)
    make_cylinder(doc, "Flex_Hose_2", 120, 1800, ext_x + ext_w/2, ext_d/2, ext_h + 1800, col_dark, offset_coords, axis=App.Vector(1,0,0))
    make_cylinder(doc, "Flex_Nozzle", 150, 300, ext_x + ext_w/2 + 1800, ext_d/2, ext_h + 1500, col_steel, offset_coords)



# ==============================================================================
# MAIN DRAWING FUNCTION FOR SEALING MACHINE
# ==============================================================================

def draw_lamination_machine(doc, offset_coords=(0,0,0)):

    # -- Colors --
    col_frame   = (0.80, 0.80, 0.80)
    col_door    = (0.60, 0.90, 0.90)
    col_dark    = (0.15, 0.15, 0.15)
    col_yellow  = (0.95, 0.75, 0.10)
    col_blue    = (0.10, 0.30, 0.90)
    col_green   = (0.20, 0.70, 0.30)
    col_white   = (0.95, 0.95, 0.95)

    # -- Dimensions (Scaled x3) --
    base_w = 9600
    base_d = 5400
    base_h = 2700
    table_z = base_h

    # ==========================================================================
    # 1. BASE CABINET STRUCTURE
    # ==========================================================================
    make_box(doc, "Base_Top", base_w, base_d, 150, 0, 0, base_h, col_frame, offset_coords)
    make_box(doc, "Base_Bot", base_w, base_d, 150, 0, 0, 300, col_frame, offset_coords)

    make_box(doc, "Div_L", 150, base_d, base_h, 0, 0, 0, col_frame, offset_coords)
    make_box(doc, "Div_R", 150, base_d, base_h, base_w - 150, 0, 0, col_frame, offset_coords)
    make_box(doc, "Div_M1", 150, base_d, base_h, 3000, 0, 0, col_frame, offset_coords)
    make_box(doc, "Div_M2", 150, base_d, base_h, 6600, 0, 0, col_frame, offset_coords)

    make_box(doc, "Door_L1", 1350, 60, 2100, 180, -30, 480, col_door, offset_coords)
    make_box(doc, "Door_L2", 1350, 60, 2100, 1560, -30, 480, col_door, offset_coords)
    make_box(doc, "Door_C1", 1650, 60, 2100, 3180, -30, 480, col_door, offset_coords)
    make_box(doc, "Door_C2", 1650, 60, 2100, 4860, -30, 480, col_door, offset_coords)
    make_box(doc, "Door_R", 2700, 60, 2100, 6780, -30, 480, col_door, offset_coords)

    door_centers = [855, 2235, 4005, 5685, 8130]
    for x in door_centers:
        make_box(doc, f"Handle_{x}", 45, 90, 300, x, -75, 1500, col_dark, offset_coords)
        for v in range(6):
            make_box(doc, f"Vent_L_{x}_{v}", 120, 15, 30, x - 90, -36, 900 + (v * 90), col_frame, offset_coords)
            make_box(doc, f"Vent_R_{x}_{v}", 120, 15, 30, x + 90, -36, 900 + (v * 90), col_frame, offset_coords)

    feet_x = [300, 3000, 6600, 9300]
    feet_y = [300, base_d - 300]
    for fx in feet_x:
        for fy in feet_y:
            make_cylinder(doc, f"Foot_{fx}_{fy}", 120, 300, fx, fy, 0, col_dark, offset_coords)
            make_cylinder(doc, f"Foot_Plate_{fx}_{fy}", 180, 60, fx, fy, 0, col_frame, offset_coords)

    # ==========================================================================
    # 2. UPPER ALUMINUM FRAMEWORK
    # ==========================================================================
    post_w = 240
    post_h = 2400

    post_locs = [
        (600, 900), (600, 3600),
        (2400, 900), (2400, 3600),
        (4200, 900), (4200, 3600),
        (6000, 900), (6000, 3600),
        (8400, 900), (8400, 3600)
    ]

    for i, (px, py) in enumerate(post_locs):
        make_box(doc, f"Post_{i}", post_w, post_w, post_h, px, py, table_z, col_frame, offset_coords)

    make_box(doc, "Beam_Long_F", 8400, post_w, post_w, 600, 900, table_z + post_h, col_frame, offset_coords)
    make_box(doc, "Beam_Long_B", 8400, post_w, post_w, 600, 3600, table_z + post_h, col_frame, offset_coords)

    cross_x = [600, 2400, 4200, 6000, 8400]
    for cx in cross_x:
        make_box(doc, f"Beam_Cross_{cx}", post_w, 2700, post_w, cx, 900, table_z + post_h, col_frame, offset_coords)

    # ==========================================================================
    # 3. UNWIND STATION
    # ==========================================================================
    make_box(doc, "Unwind_Plate", 60, 3000, 1800, 600, 750, table_z + 600, col_white, offset_coords)

    make_cylinder(doc, "Roll_Blue_1", 540, 900, 300, 1500, table_z + 1200, col_blue, offset_coords, axis=App.Vector(1,0,0))
    make_cylinder(doc, "Roll_Blue_2", 540, 900, 300, 3000, table_z + 2100, col_blue, offset_coords, axis=App.Vector(1,0,0))

    make_cylinder(doc, "Motor_Roll_1", 150, 450, 750, 1500, table_z + 1200, col_dark, offset_coords, axis=App.Vector(1,0,0))
    make_cylinder(doc, "Motor_Roll_2", 150, 450, 750, 3000, table_z + 2100, col_dark, offset_coords, axis=App.Vector(1,0,0))

    # ==========================================================================
    # 4. PROCESSING AREA
    # ==========================================================================
    plate_w = 1500
    plate_d = 2400
    plate_x_start = 1500

    for i in range(3):
        px = plate_x_start + (i * 2100)
        make_box(doc, f"Yellow_Plate_{i}", plate_w, plate_d, 60, px, 1050, table_z + 150, col_yellow, offset_coords)
        make_box(doc, f"Mech_Frame_{i}", plate_w, 600, 300, px, 1950, table_z + 1200, col_dark, offset_coords)
        make_cylinder(doc, f"Piston_{i}_L", 90, 900, px + 300, 2250, table_z + 300, col_frame, offset_coords)
        make_cylinder(doc, f"Piston_{i}_R", 90, 900, px + 1200, 2250, table_z + 300, col_frame, offset_coords)

    make_box(doc, "Top_Black_Unit", 1800, 1200, 600, 3600, 1650, table_z + 2700, col_dark, offset_coords)
    make_cylinder(doc, "Black_Roller_Top", 180, 1500, 4500, 1500, table_z + 3000, col_dark, offset_coords, axis=App.Vector(1,0,0))

    # ==========================================================================
    # 5. OUTPUT CONVEYOR
    # ==========================================================================
    conv_x = 7200
    make_box(doc, "Conv_Frame", 2400, 2400, 300, conv_x, 1050, table_z + 150, col_frame, offset_coords)
    make_box(doc, "Belt_1", 2400, 150, 30, conv_x, 1200, table_z + 450, col_green, offset_coords)
    make_box(doc, "Belt_2", 2400, 150, 30, conv_x, 3150, table_z + 450, col_green, offset_coords)

    make_box(doc, "End_Table", 1800, 3000, 60, base_w, 750, table_z, col_frame, offset_coords)
    make_box(doc, "End_Leg", 120, 120, 1800, base_w + 1500, 2250, table_z - 1200, col_frame, offset_coords,
             rotation_angle=30, rotation_axis=App.Vector(0,1,0))

    # ==========================================================================
    # 6. SENSORS
    # ==========================================================================
    for i in range(5):
        sx = 1800 + (i * 1500)
        make_cylinder(doc, f"Sensor_{i}", 30, 150, sx, 900, table_z + 300, col_dark, offset_coords)


# ==============================================================================
# MAIN DRAWING FUNCTION FOR DRYING MACHINE
# ==============================================================================


def draw_industrial_machine(doc, offset_coords=(0,0,0)):
    # Colors
    c_blue   = (0.0, 0.5, 0.8)
    c_grey   = (0.6, 0.6, 0.6)
    c_dark   = (0.3, 0.3, 0.3)
    c_orange = (1.0, 0.4, 0.0)
    c_yellow = (1.0, 0.9, 0.0)

    # 1. BOTTOM SUPPORT STRUCTURE (Grey Legs)
    leg_x = [500, 4500, 8500, 12500]
    for i, x in enumerate(leg_x):
        make_box(doc, f"Leg_L_{i}", 800, 800, 1500, x, 1000, 0, c_grey, offset_coords)
        make_box(doc, f"Leg_R_{i}", 800, 800, 1500, x, 5200, 0, c_grey, offset_coords)
        make_box(doc, f"Brace_{i}", 600, 5000, 400, x + 100, 1000, 1000, c_grey, offset_coords)

    # 2. MAIN BLUE BASE FRAME
    make_box(doc, "Base_Beam_L", 14000, 500, 1000, 0, 800, 1500, c_blue, offset_coords)
    make_box(doc, "Base_Beam_R", 14000, 500, 1000, 0, 5700, 1500, c_blue, offset_coords)
    make_box(doc, "Base_End_F", 400, 5400, 1000, 0, 800, 1500, c_blue, offset_coords)
    make_box(doc, "Base_End_B", 400, 5400, 1000, 13600, 800, 1500, c_blue, offset_coords)

    # 3. ROTARY DRUM ASSEMBLY
    drum_rad = 2200
    drum_len = 12000
    make_cylinder(doc, "Drum_Main", drum_rad, drum_len, 1000, 3500, 4500, c_grey, offset_coords, axis=App.Vector(1,0,0))

    for i in range(8):
        make_cylinder(
            doc,
            f"Drum_Ring_{i}",
            drum_rad + 100,
            300,
            1500 + (i * 1400),
            3500,
            4500,
            c_dark,
            offset_coords,
            axis=App.Vector(1,0,0)
        )

    # 4. ORANGE SIDE GUARDS
    make_box(doc, "Orange_Side_L", 10000, 200, 1200, 2000, 600, 2500, c_orange, offset_coords)
    make_box(doc, "Orange_Side_R", 10000, 200, 1200, 2000, 6200, 2500, c_orange, offset_coords)

    # 5. YELLOW SAFETY RAILING
    for i in range(4):
        make_box(doc, f"Rail_Post_{i}", 100, 100, 1800, 11000 + (i * 800), 6000, 2500, c_yellow, offset_coords)

    make_box(doc, "Rail_Top", 3000, 100, 100, 11000, 6000, 4200, c_yellow, offset_coords)

    # 6. VOC PIPING
    pipe_rad = 400
    make_cylinder(doc, "VOC_Main_Pipe", pipe_rad, 15000, -500, 3500, 8000, c_grey, offset_coords, axis=App.Vector(1,0,0))
    make_cylinder(doc, "VOC_Support", 150, 2000, 3000, 3500, 6000, c_grey, offset_coords)

    # 7. DISCHARGE END
    make_box(doc, "End_Housing", 2000, 6000, 6000, 13000, 500, 2000, c_grey, offset_coords)
    make_box(
        doc,
        "Output_Chute",
        3000,
        2000,
        1000,
        14000,
        2500,
        1000,
        c_grey,
        offset_coords,
        rotation_angle=-35,
        rotation_axis=App.Vector(0,1,0)
    )



# ==============================================================================
# MAIN DRAWING FUNCTION FOR THE ELECTROLYTE FILLING MACHINE
# ==============================================================================

def draw_glovebox_system(doc, offset_coords=(0,0,0)):
    # -- Colors --
    col_white   = (0.95, 0.95, 0.95)
    col_glass   = (0.80, 0.90, 0.95)
    col_steel   = (0.70, 0.70, 0.70)
    col_dark    = (0.20, 0.20, 0.20)
    col_blue    = (0.10, 0.40, 0.80)
    col_red     = (0.80, 0.10, 0.10)

    # -- General Dimensions (Original * 3) --
    mod_w = 3600    # 1200 * 3
    mod_d = 2400    # 800 * 3
    base_h = 2700   # 900 * 3
    main_h = 3000   # 1000 * 3
    top_h = 900     # 300 * 3
    
    # ==========================================================================
    # 1. FOUR GLOVEBOX MODULES
    # ==========================================================================
    for i in range(4):
        x_off = i * mod_w
        
        # Lower Cabinet
        make_box(doc, f"Base_{i}", mod_w - 30, mod_d, base_h, x_off, 0, 0, col_white, offset_coords)
        
        # Upper Chamber
        make_box(doc, f"Chamber_{i}", mod_w - 30, mod_d, main_h, x_off, 0, base_h, col_white, offset_coords)
        
        # Front Window (Glass Pane)
        make_box(doc, f"Window_{i}", mod_w - 300, 30, main_h - 450, x_off + 150, -15, base_h + 150, col_glass, offset_coords)
        
        # Top Control Section
        make_box(doc, f"Top_{i}", mod_w - 30, mod_d, top_h, x_off, 0, base_h + main_h, col_white, offset_coords)

        # Glove Ports (Circular rings on the window)
        port_radius = 330 # 110 * 3
        # Positions: (x_off + original_offset * 3, base_h + original_offset * 3)
        port_positions = [ (x_off + 900, base_h + 1050), (x_off + 1800, base_h + 1050), (x_off + 2700, base_h + 1050) ]
        if i == 3: # Far right module special arrangement
             port_positions = [ (x_off + 750, base_h + 1650), (x_off + 1650, base_h + 1650), 
                                (x_off + 750, base_h + 750), (x_off + 1650, base_h + 750), (x_off + 2550, base_h + 1050) ]

        for p_idx, (px, pz) in enumerate(port_positions):
            make_cylinder(doc, f"Port_{i}_{p_idx}", port_radius, 60, px, -45, pz, col_dark, offset_coords, axis=App.Vector(0,1,0))

        # Control Panel Elements (Buttons/Gauges on top)
        for g_idx in range(4):
            make_cylinder(doc, f"Gauge_{i}_{g_idx}", 75, 15, x_off + 1200 + (g_idx * 240), -15, base_h + main_h + 450, col_steel, offset_coords, axis=App.Vector(0,1,0))

        # Legs and Wheels
        leg_x = [x_off + 150, x_off + mod_w - 300]
        for lx in leg_x:
            make_box(doc, f"Leg_{i}_{lx}", 120, 120, 450, lx, mod_d/2, -450, col_steel, offset_coords)
            make_cylinder(doc, f"Wheel_{i}_{lx}", 120, 90, lx+60, mod_d/2 + 60, -540, col_dark, offset_coords)

    # ==========================================================================
    # 2. TOUCHSCREEN INTERFACES
    # ==========================================================================
    for i in [1, 3]:
        tx = (i * mod_w) + 1800
        make_box(doc, f"Monitor_Base_{i}", 750, 120, 540, tx, -120, base_h + 1500, col_dark, offset_coords)
        make_box(doc, f"Screen_{i}", 690, 15, 480, tx + 30, -135, base_h + 1530, col_steel, offset_coords)

    # ==========================================================================
    # 3. VACUUM AIRLOCK (Right side cylinder)
    # ==========================================================================
    airlock_x = 4 * mod_w
    airlock_radius = 840 # 280 * 3
    airlock_len = 1800   # 600 * 3
    
    # Horizontal Cylinder
    make_cylinder(doc, "Airlock_Body", airlock_radius, airlock_len, airlock_x - 300, mod_d/2, base_h + 1350, col_steel, offset_coords, axis=App.Vector(1,0,0))
    
    # Blue Door at the end
    make_cylinder(doc, "Airlock_Door", airlock_radius + 60, 120, airlock_x + airlock_len - 300, mod_d/2, base_h + 1350, col_blue, offset_coords, axis=App.Vector(1,0,0))
    
    # Door Handle mechanism
    make_cylinder(doc, "Handle_Hub", 120, 300, airlock_x + airlock_len - 180, mod_d/2, base_h + 1350, col_steel, offset_coords, axis=App.Vector(1,0,0))
    for angle in [0, 90, 180, 270]:
        rad_angle = math.radians(angle)
        hx = airlock_x + airlock_len - 120
        hy = mod_d/2 + math.cos(rad_angle) * 450
        hz = base_h + 1350 + math.sin(rad_angle) * 450
        make_cylinder(doc, f"Handle_Spoke_{angle}", 45, 600, hx, hy, hz, col_steel, offset_coords, axis=App.Vector(1,0,0))

    # ==========================================================================
    # 4. EXTERNAL GAS PURIFICATION / PIPING
    # ==========================================================================
    make_box(doc, "Side_Cabinet", 1200, mod_d, base_h + main_h, airlock_x + 300, 0, 0, col_white, offset_coords)
    make_cylinder(doc, "Gas_Inlet", 90, 1200, airlock_x + 900, mod_d - 150, base_h + main_h + 300, col_steel, offset_coords)



# ==============================================================================
# MAIN DRAWING FUNCTION FOR BATTERY FORMATION MACHINE
# ==============================================================================

def draw_battery_cabinet(doc, offset_coords=(0,0,0)):
    # Colors (Declared inside function)
    c_frame  = (0.9, 0.9, 0.92)    # Silver/White
    c_inner  = (0.0, 0.8, 0.8)     # Cyan/Teal background
    c_batt   = (0.1, 0.1, 0.6)     # Dark Blue (Battery Modules)
    c_detail = (0.2, 0.2, 0.2)     # Black/Dark Grey (Vents, Feet)
    c_latch  = (0.6, 0.2, 0.6)     # Purple (Handles)

    # Main Dimensions (Scaled by 3 as requested)
    cab_height = 6000.0
    cab_width = 4800.0
    cab_depth = 2400.0
    
    control_panel_width = 1200.0
    rack_area_width = cab_width - control_panel_width
    col_width = rack_area_width / 2.0

    # 1. MAIN FRAME & OUTER SHELL
    # Bottom Base
    make_box(doc, "Base", cab_width, cab_depth, 300, 0, 0, 0, c_frame, offset_coords)
    # Top Cap
    make_box(doc, "Top", cab_width, cab_depth, 300, 0, 0, cab_height - 300, c_frame, offset_coords)
    
    # Right Control Cabinet Body
    make_box(doc, "ControlCab", control_panel_width, cab_depth - 150, cab_height - 600, 
             rack_area_width, 75, 300, c_frame, offset_coords)
    
    # Vertical Dividers for Racks
    # Left Wall
    make_box(doc, "WallLeft", 150, cab_depth - 150, cab_height - 600, 
             0, 75, 300, c_frame, offset_coords)
    # Middle Post
    make_box(doc, "WallMid", 150, cab_depth - 150, cab_height - 600, 
             col_width - 75, 75, 300, c_frame, offset_coords)
    
    # Back Panel (Cyan)
    make_box(doc, "BackPanel", rack_area_width, 60, cab_height - 600, 
             0, cab_depth - 60, 300, c_inner, offset_coords)

    # 2. FEET (Cylinders or Boxes)
    make_box(doc, "FootFL", 240, 240, 120, 60, 60, -120, c_detail, offset_coords)
    make_box(doc, "FootFR", 240, 240, 120, cab_width - 300, 60, -120, c_detail, offset_coords)
    make_box(doc, "FootBL", 240, 240, 120, 60, cab_depth - 300, -120, c_detail, offset_coords)
    make_box(doc, "FootBR", 240, 240, 120, cab_width - 300, cab_depth - 300, -120, c_detail, offset_coords)

    # 3. BATTERY ROWS (The blue packs)
    num_rows = 8
    start_z = 450
    vertical_space = (cab_height - 750) / num_rows
    
    # Dimensions for one battery tray
    tray_w = col_width - 180
    tray_d = cab_depth - 450
    tray_h = 300

    for r in range(num_rows):
        current_z = start_z + (r * vertical_space)
        
        # Left Column
        make_box(doc, f"TrayL_{r}", tray_w, tray_d, tray_h, 
                 165, 150, current_z, c_batt, offset_coords)
        # Left Latches
        make_box(doc, f"LatchL_{r}", 30, 150, 120, 
                 165, 120, current_z + 90, c_latch, offset_coords)
        
        # Right Column
        make_box(doc, f"TrayR_{r}", tray_w, tray_d, tray_h, 
                 col_width + 90, 150, current_z, c_batt, offset_coords)
        # Right Latches
        make_box(doc, f"LatchR_{r}", 30, 150, 120, 
                 col_width + 90 + tray_w - 30, 120, current_z + 90, c_latch, offset_coords)

        # Shelf supports underneath
        make_box(doc, f"ShelfL_{r}", tray_w + 60, tray_d, 30, 
                 135, 150, current_z - 30, c_frame, offset_coords)
        make_box(doc, f"ShelfR_{r}", tray_w + 60, tray_d, 30, 
                 col_width + 60, 150, current_z - 30, c_frame, offset_coords)

    # 4. DETAILS ON RIGHT CONTROL PANEL (Vents and switches)
    # Vents
    for v in range(5):
        vz = 1200 + (v * 900)
        make_box(doc, f"Vent_{v}", 600, 30, 450, 
                 rack_area_width + 300, 60, vz, c_detail, offset_coords)
        # Switches
        make_box(doc, f"Switch_{v}", 120, 30, 120, 
                 rack_area_width + 120, 60, vz + 150, c_detail, offset_coords)

    # 5. TOP FANS (Cylinders)
    fan_y = cab_depth / 2
    for f in range(3):
        fx = 900 + (f * 1500)
        make_cylinder(doc, f"Fan_{f}", 240, 90, fx, fan_y, cab_height, c_detail, offset_coords)



# ==============================================================================
# MAIN DRAWING FUNCTION FOR THE GRADING MACHINE
# ==============================================================================

def draw_acey_machine(doc, offset_coords=(0,0,0)):
    # --- Colors ---
    c_cream  = (0.93, 0.92, 0.88) # Main chassis color
    c_blue   = (0.05, 0.2, 0.7)   # "ACEY" logo and Battery cells
    c_silver = (0.80, 0.80, 0.80) # Aluminum pneumatic cylinders/pistons
    c_dark   = (0.25, 0.25, 0.25) # Vents, display background, wheels
    c_red    = (0.9, 0.1, 0.1)    # LED display digits
    c_gold   = (0.85, 0.7, 0.3)   # Contact probes

    # --- Dimensions (Scaled by 3) ---
    m_height = 6000.0
    m_width  = 3300.0
    m_depth  = 4200.0
    
    rack_w = 2400.0 # Width of the shelf area
    side_w = m_width - rack_w # Width of the right-side solid cabinet area

    # 1. BASE & WHEELS
    # Main base frame
    make_box(doc, "BaseFrame", m_width, m_depth, 300, 0, 0, 240, c_cream, offset_coords)
    
    # Castor Wheels (4 corners)
    # Positions scaled: 50->150, 100->300, 150->450
    wheel_positions = [(150, 300), (m_width-300, 300), (150, m_depth-450), (m_width-300, m_depth-450)]
    for i, (wx, wy) in enumerate(wheel_positions):
        make_cylinder(doc, f"Wheel_{i}", 120, 240, wx+60, wy+60, 0, c_dark, offset_coords)

    # 2. MAIN CABINET STRUCTURE
    # Top Header (Controls housing)
    make_box(doc, "TopHeader", m_width, m_depth, 540, 0, 0, m_height - 540, c_cream, offset_coords)
    
    # Right Side Panel (The large solid wall)
    make_box(doc, "RightWall", side_w, m_depth, m_height - 840, rack_w, 0, 540, c_cream, offset_coords)
    
    # Left Vertical Post
    make_box(doc, "LeftPost", 180, 180, m_height - 840, 0, 0, 540, c_cream, offset_coords)
    make_box(doc, "LeftPostBack", 180, 180, m_height - 840, 0, m_depth - 180, 540, c_cream, offset_coords)

    # Back Panel (Behind shelves)
    make_box(doc, "BackPanel", rack_w, 60, m_height - 840, 0, m_depth - 60, 540, c_cream, offset_coords)

    # 3. SHELVES AND BATTERY MECHANISM
    # There are 5 shelf levels in the image
    num_levels = 5
    shelf_pitch = (m_height - 1200) / num_levels
    
    for i in range(num_levels):
        z_base = 660 + (i * shelf_pitch)
        
        # A. The Shelf Tray
        make_box(doc, f"Tray_{i}", rack_w - 60, m_depth - 300, 75, 30, 150, z_base, c_cream, offset_coords)
        
        # B. Battery Cells (Blue prismatic cans)
        # 12 cells per row
        cell_w = 120
        cell_d = 240
        cell_h = 300
        gap = 45
        start_x = 150
        
        for c in range(12):
            cx = start_x + (c * (cell_w + gap))
            # Draw cell
            make_box(doc, f"Cell_{i}_{c}", cell_w, cell_d, cell_h, cx, 450, z_base + 75, c_blue, offset_coords)
            # Draw Gold Probe above cell
            make_cylinder(doc, f"Probe_{i}_{c}", 12, 90, cx + cell_w/2, 570, z_base + cell_h + 105, c_gold, offset_coords)

        # C. Upper Clamp/Probe Mechanism Rail
        rail_z = z_base + cell_h + 165
        make_box(doc, f"ClampRail_{i}", rack_w - 120, m_depth - 300, 90, 60, 150, rail_z, c_cream, offset_coords)
        
        # D. Pneumatic Cylinders (The silver pistons on the right side of the rack)
        # Mounting block
        make_box(doc, f"PistonMount_{i}", 150, 240, 540, rack_w - 180, 240, z_base + 90, c_cream, offset_coords)
        # Cylinder body
        make_cylinder(doc, f"PistonBody_{i}", 60, 360, rack_w - 105, 360, z_base + 180, c_silver, offset_coords)
        # Piston rod (shiny part)
        make_cylinder(doc, f"PistonRod_{i}", 30, 240, rack_w - 105, 360, z_base + 540, c_silver, offset_coords)

    # 4. SIDE VENTS (On the right solid panel)
    # The image shows columns of small horizontal slots
    for col in range(2):
        vx = rack_w + 300 + (col * 300)
        for row in range(15):
            vz = 1500 + (row * 180)
            make_box(doc, f"Vent_{col}_{row}", 30, 150, 45, vx, 0, vz, c_dark, offset_coords)

    # 5. TOP LOGO AND DISPLAY
    # "ACEY" Logo Box (Simulated as a blue block)
    make_box(doc, "LogoBox", 450, 30, 150, 120, -15, m_height - 390, c_blue, offset_coords)
    
    # Digital Display Panel
    make_box(doc, "DisplayBG", 540, 30, 180, 750, -15, m_height - 405, c_dark, offset_coords)
    # Red numbers
    make_box(doc, "DisplayNum", 300, 30, 90, 870, -24, m_height - 360, c_red, offset_coords)
    
    # Small indicator lights (Green/Red dots on left post)
    make_cylinder(doc, "Light_Green", 24, 30, 90, 0, 3000, (0.0, 1.0, 0.0), offset_coords, axis=App.Vector(0,1,0))
    make_cylinder(doc, "Light_Red", 24, 30, 90, 0, 2850, (1.0, 0.0, 0.0), offset_coords, axis=App.Vector(0,1,0))


# ==============================================================================
# MAIN DRAWING FUNCTION FOR THE BATTERY CHARGING AND DISCHARGING MACHINE
# ==============================================================================

def draw_cleaning_machine(doc, offset_coords=(0,0,0)):

    # --- Colors ---
    c_steel   = (0.75, 0.75, 0.78)
    c_white   = (0.95, 0.95, 0.95)
    c_glass   = (0.60, 0.80, 0.90)
    c_blue    = (0.10, 0.30, 0.70)
    c_dark    = (0.20, 0.20, 0.20)
    c_control = (0.85, 0.85, 0.85)

    # --- Dimensions ---
    main_l = 9600
    main_w = 3600
    main_h = 6000

    ext_l = 5400
    ext_w = 3600
    ext_h = 3000

    # 1. MAIN UNIT STRUCTURE

    make_box(doc, "Main_Top_Beam", main_l, main_w, 300, 0, 0, main_h - 300, c_steel, offset_coords)
    make_box(doc, "Main_Bot_Beam", main_l, main_w, 300, 0, 0, 0, c_steel, offset_coords)
    make_box(doc, "Main_Mid_Beam", main_l, main_w, 300, 0, 0, 2400, c_steel, offset_coords)

    posts_x = [0, 1800, 5700, 9300]
    for i, x in enumerate(posts_x):
        make_box(doc, f"Post_{i}", 300, main_w, main_h, x, 0, 0, c_steel, offset_coords)

    make_box(doc, "Control_Box", 1500, 60, 3000, 150, 0, 2700, c_control, offset_coords)

    for i in range(3):
        make_cylinder(
            doc, f"Button_{i}", 45, 60,
            450 + (i * 180), -60, 5100,
            (1, 0, 0), offset_coords,
            axis=App.Vector(0,1,0)
        )

    make_box(doc, "Screen", 900, 30, 600, 450, -30, 3900, (0.1, 0.1, 0.1), offset_coords)

    make_box(doc, "Window_1", 3600, 60, 2700, 2100, 30, 2700, c_glass, offset_coords)
    make_box(doc, "Window_2", 3300, 60, 2700, 6000, 30, 2700, c_glass, offset_coords)

    for i in range(4):
        make_cylinder(
            doc, f"Pipe_H_{i}", 90, 7200,
            2100, 600 + (i * 450), 900 + (i * 150),
            c_dark, offset_coords,
            axis=App.Vector(1,0,0)
        )
        make_cylinder(
            doc, f"Pump_{i}", 180, 1200,
            2700 + (i * 1800), 1200, 300,
            c_steel, offset_coords
        )

    make_box(doc, "Top_Filter", 3000, 2400, 1500, 4500, 600, main_h, c_white, offset_coords)
    make_cylinder(doc, "Gauge", 120, 60, 4800, 570, main_h + 750, c_steel, offset_coords, axis=App.Vector(0,1,0))

    for i in range(3):
        make_box(doc, f"Gen_{i}", 750, 1200, 600, 600 + (i * 900), 300, main_h, c_blue, offset_coords)

    start_x_ext = main_l

    make_box(doc, "Ext_Frame_Top", ext_l, ext_w, 240, start_x_ext, 0, ext_h, c_steel, offset_coords)
    make_box(doc, "Ext_Frame_Bot", ext_l, ext_w, 240, start_x_ext, 0, 300, c_steel, offset_coords)

    make_box(doc, "Ext_Leg_1", 240, 240, ext_h, start_x_ext, 0, 0, c_steel, offset_coords)
    make_box(doc, "Ext_Leg_2", 240, 240, ext_h, start_x_ext + ext_l - 240, 0, 0, c_steel, offset_coords)
    make_box(doc, "Ext_Leg_3", 240, 240, ext_h, start_x_ext, ext_w - 240, 0, c_steel, offset_coords)
    make_box(doc, "Ext_Leg_4", 240, 240, ext_h, start_x_ext + ext_l - 240, ext_w - 240, 0, c_steel, offset_coords)

    tank_x = start_x_ext + 1200
    tank_l = 3000
    tank_h = 2100

    make_box(doc, "Tank_Body", tank_l, ext_w - 300, tank_h, tank_x, 150, ext_h, c_white, offset_coords)
    make_box(doc, "Tank_Trim_L", 150, ext_w - 300, tank_h, tank_x, 150, ext_h, c_steel, offset_coords)
    make_box(doc, "Tank_Trim_R", 150, ext_w - 300, tank_h, tank_x + tank_l - 150, 150, ext_h, c_steel, offset_coords)

    make_box(doc, "Tank_Lid", tank_l, ext_w - 600, 450, tank_x, 300, ext_h + tank_h, c_white, offset_coords)
    make_box(doc, "Lid_Handle", 600, 60, 60, tank_x + 1200, 240, ext_h + tank_h + 150, c_steel, offset_coords)

    make_box(doc, "Rail_1", ext_l, 60, 60, start_x_ext, 30, 1200, c_steel, offset_coords)
    make_box(doc, "Rail_2", ext_l, 60, 60, start_x_ext, 30, 2100, c_steel, offset_coords)



# ==========================================
# .DRAWING FUNCTION FOR THE AL COATED PLATE
# ==========================================

def draw_sectional_plate(doc, offset=(0,0,0)):
    # --- LOCAL PARAMETERS ---
    plate_length = 1200.0
    total_width = 800.0
    thickness = 150
    edge_width = 80
    center_width = total_width - (2 * edge_width)

    # --- COLORS ---
    silver_color = (0.85, 0.85, 0.85)
    black_color = (0.1, 0.1, 0.1)

    # --- GEOMETRY GENERATION ---
    # A. Left Silver Edge
    make_box(doc, "Silver_Edge_Left", edge_width, plate_length, thickness, 0, 0, 0, silver_color, offset)

    # B. Center Black Section
    make_box(doc, "Black_Center_Plate", center_width, plate_length, thickness, edge_width, 0, 0, black_color, offset)

    # C. Right Silver Edge
    make_box(doc, "Silver_Edge_Right", edge_width, plate_length, thickness, edge_width + center_width, 0, 0, silver_color, offset)



# ==========================================
# .DRAWING FUNCTION CU COATED PLATE
# ==========================================

def draw_copper_plate(doc, offset=(0,0,0)):
    """
    Draws the Copper-Graphite-Copper Plate.
    All parameters are local to avoid conflicts with the Silver plate code.
    """
    
    # --- LOCAL PARAMETERS ---
    plate_length = 1200.0
    total_width = 900.0
    thickness = 100.0
    edge_width = 100.0      # Width of the copper strips

    # Calculated Dimensions
    center_width = total_width - (2 * edge_width)

    # --- LOCAL COLORS ---
    # Copper color (Reddish-Brown metallic)
    copper_color = (0.72, 0.45, 0.20) 
    # Dark Grey/Black (Graphite/Anode material)
    dark_grey_color = (0.15, 0.15, 0.15) 

    # --- GEOMETRY GENERATION ---

    # A. Left Copper Edge
    make_box(doc, "Copper_Edge_Left", 
             edge_width, plate_length, thickness, 
             0, 0, 0, 
             copper_color, offset)

    # B. Center Dark Section
    make_box(doc, "Graphite_Center_Plate", 
             center_width, plate_length, thickness, 
             edge_width, 0, 0, 
             dark_grey_color, offset)

    # C. Right Copper Edge
    make_box(doc, "Copper_Edge_Right", 
             edge_width, plate_length, thickness, 
             edge_width + center_width, 0, 0, 
             copper_color, offset)




# ==========================================
# .DRAWING FUNCTION FOR A STACKED CELL
# ==========================================

def draw_stacked_cell(doc, offset=(0,0,0)):
    # --- PARAMETERS ---
    plate_width = 800.0
    plate_length = 1200.0
    
    # Thicknesses
    electrode_thick = 10.0
    separator_thick = 5
    
    # Tabs
    tab_width = 150.0
    tab_length = 200.0
    
    # Repeats
    num_repeats = 6 
    
    # --- COLORS ---
    anode_color = (0.6, 0.6, 0.6)    # Grey
    cathode_color = (0.1, 0.1, 0.1)  # Black
    sep_color = (0.95, 0.95, 0.95)   # White
    tab_gold = (0.8, 0.6, 0.2)
    tab_silver = (0.9, 0.9, 0.9)

    # --- GEOMETRY LOOP ---
    current_z = 0.0
    
    for i in range(num_repeats):
        # 1. ANODE (Grey)
        make_box(doc, "Anode_{}".format(i), 
                 plate_width, plate_length, electrode_thick, 
                 0, 0, current_z, 
                 anode_color, offset)
                 
        # Anode Tab
        make_box(doc, "Tab_Anode_{}".format(i), 
                 tab_width, tab_length, electrode_thick, 
                 10, plate_length, current_z, 
                 tab_gold, offset)
                 
        current_z += electrode_thick
        
        # 2. SEPARATOR (White)
        make_box(doc, "Sep_1_{}".format(i), 
                 plate_width, plate_length, separator_thick, 
                 0, 0, current_z, 
                 sep_color, offset)
                 
        current_z += separator_thick
        
        # 3. CATHODE (Black)
        make_box(doc, "Cathode_{}".format(i), 
                 plate_width, plate_length, electrode_thick, 
                 0, 0, current_z, 
                 cathode_color, offset)
        
        # Cathode Tab
        make_box(doc, "Tab_Cathode_{}".format(i), 
                 tab_width, tab_length, electrode_thick, 
                 plate_width - 10 - tab_width, plate_length, current_z, 
                 tab_silver, offset)
                 
        current_z += electrode_thick

        # 4. SEPARATOR (White)
        make_box(doc, "Sep_2_{}".format(i), 
                 plate_width, plate_length, separator_thick, 
                 0, 0, current_z, 
                 sep_color, offset)
                 
        current_z += separator_thick

# Scale Factor: 10.0 (Tenfold increase)
SF = 10.0 

# ==========================================
# LOGO GENERATOR
# ==========================================

def draw_logo(doc, suffix, center_x, face_y, center_z, offset, is_back_face=False):
    """
    Draws the logo (Label, Gear, Leaf, Vein) at a specific location.
    All dimensions are multiplied by SF (10.0).
    """
    
    # --- Local Colors ---
    c_label_bg   = (0.0, 0.35, 0.58) # Blue (Matches Body)
    c_gear_black = (0.0, 0.0, 0.0)
    c_leaf_green = (0.46, 0.75, 0.26)
    c_vein_white = (1.0, 1.0, 1.0)
    
    # --- Dimensions Scaled ---
    label_w = 60.0 * SF
    label_h = 50.0 * SF
    # Original scale was 0.15 relative to 100mm width. 
    # We multiply by SF to keep proportion with the 1000mm width.
    scale = 0.15 * SF 
    
    # --- Rotation Logic ---
    # Rotate 180 around Z if it's the back face
    rot_angle = 180 if is_back_face else 0
    rot_axis = App.Vector(0,0,1)
    
    # Y-Offset: Protrusion scaled
    protrusion = 0.5 * SF
    y_shift = protrusion if is_back_face else -protrusion

    # 1. LABEL BACKGROUND
    # Thickness 0.5 scaled
    lbl_thick = 0.5 * SF
    lbl = Part.makeBox(label_w, lbl_thick, label_h)
    
    # Translate to center local origin
    lbl.translate(App.Vector(-label_w/2, -lbl_thick if not is_back_face else 0, -label_h/2))
    
    if is_back_face:
        lbl.rotate(App.Vector(0,0,0), rot_axis, rot_angle)
        
    lbl.translate(App.Vector(center_x, face_y, center_z))
    
    obj_lbl = doc.addObject("Part::Feature", f"Label_{suffix}")
    obj_lbl.Shape = lbl
    obj_lbl.ViewObject.ShapeColor = c_label_bg

    # 2. GEAR
    gear_r = 110.0 * scale
    tooth_len = 30.0 * scale
    gear_thick = 1.5 * SF
    
    # Hub
    hub = Part.makeCylinder(gear_r, gear_thick)
    hub.rotate(App.Vector(0,0,0), App.Vector(1,0,0), 90) # Upright
    
    # Teeth
    full_gear = hub
    for i in range(8):
        angle_deg = i * 45
        tooth_w = 20 * scale
        t_box = Part.makeBox(tooth_len, tooth_w, gear_thick)
        t_box.translate(App.Vector(gear_r - (1 * SF), -tooth_w/2, 0)) # Offset from center
        t_box.rotate(App.Vector(0,0,0), App.Vector(0,0,1), angle_deg) # Radial pos
        t_box.rotate(App.Vector(0,0,0), App.Vector(1,0,0), 90) # Upright
        full_gear = full_gear.fuse(t_box)

    # Hole
    hole_thick = 2.0 * SF
    hole = Part.makeCylinder(100.0 * scale, hole_thick)
    hole.rotate(App.Vector(0,0,0), App.Vector(1,0,0), 90)
    # Adjustment for Z-fighting/Position
    hole.translate(App.Vector(0, -0.25 * SF, 0))
    
    gear_final = full_gear.cut(hole)
    
    # Fill Hole with Blue (Label Color)
    hole_fill = hole
    
    # Shift slightly in front of label
    gear_y_shift = (y_shift * 2) 
    
    # Rotate & Position Gear
    if is_back_face:
        gear_final.rotate(App.Vector(0,0,0), rot_axis, rot_angle)
        hole_fill.rotate(App.Vector(0,0,0), rot_axis, rot_angle)
        
    gear_final.translate(App.Vector(center_x, face_y + gear_y_shift, center_z))
    hole_fill.translate(App.Vector(center_x, face_y + gear_y_shift, center_z))

    obj_gear = doc.addObject("Part::Feature", f"Gear_{suffix}")
    obj_gear.Shape = gear_final
    obj_gear.ViewObject.ShapeColor = c_gear_black
    
    obj_hole = doc.addObject("Part::Feature", f"GearHole_{suffix}")
    obj_hole.Shape = hole_fill
    obj_hole.ViewObject.ShapeColor = c_label_bg

    # 3. LEAF
    leaf_r = 130.0 * scale
    leaf_thick = 2.0 * SF
    
    pts_right = [App.Vector(0,0,0), App.Vector(leaf_r*0.8, leaf_r*0.2, 0), App.Vector(leaf_r, leaf_r, 0)]
    # FIX: Use BSplineCurve class and convert to Shape (Edge)
    curve1 = Part.BSplineCurve()
    curve1.buildFromPoles(pts_right)
    bs1 = curve1.toShape()
    
    pts_left  = [App.Vector(leaf_r, leaf_r, 0), App.Vector(leaf_r*0.2, leaf_r*0.8, 0), App.Vector(0,0,0)]
    # FIX: Use BSplineCurve class and convert to Shape (Edge)
    curve2 = Part.BSplineCurve()
    curve2.buildFromPoles(pts_left)
    bs2 = curve2.toShape()
    
    leaf_wire = Part.Wire([bs1, bs2])
    leaf_face = Part.Face(leaf_wire)
    leaf_solid = leaf_face.extrude(App.Vector(0, 0, leaf_thick))
    
    # Orient (Upright + Tilted)
    leaf_solid.rotate(App.Vector(0,0,0), App.Vector(1,0,0), 90) 
    leaf_solid.rotate(App.Vector(0,0,0), App.Vector(0,1,0), -45)
    
    # Local Position Adjustment
    leaf_offset_y = -90 * scale
    leaf_local_z_pos = (leaf_offset_y * -1) - (leaf_r*0.5)
    leaf_solid.translate(App.Vector(0, 0, leaf_local_z_pos))
    
    # Rotate & Position Leaf
    if is_back_face:
        leaf_solid.rotate(App.Vector(0,0,0), rot_axis, rot_angle)
        
    leaf_solid.translate(App.Vector(center_x, face_y + gear_y_shift, center_z))
    
    obj_leaf = doc.addObject("Part::Feature", f"Leaf_{suffix}")
    obj_leaf.Shape = leaf_solid
    obj_leaf.ViewObject.ShapeColor = c_leaf_green

    # 4. VEIN
    v_pts = [
        App.Vector(5*scale, 5*scale, 0), 
        App.Vector(leaf_r*0.5, leaf_r*0.5, 0), 
        App.Vector(leaf_r*0.8, leaf_r*0.9, 0)
    ]
    
    # FIX: Use BSplineCurve class and convert to Shape (Edge)
    v_curve_geom = Part.BSplineCurve()
    v_curve_geom.buildFromPoles(v_pts)
    vein_edge = v_curve_geom.toShape()
    
    # Vein thickness scales with 'scale' automatically via radius
    vein_profile = Part.makeCircle(2.5 * scale, App.Vector(0,0,0), App.Vector(0,0,1))
    
    # MakePipe requires a Wire path
    vein_solid = Part.Wire([vein_edge]).makePipe(vein_profile)
    
    # Orient
    vein_solid.rotate(App.Vector(0,0,0), App.Vector(1,0,0), 90) 
    vein_solid.rotate(App.Vector(0,0,0), App.Vector(0,1,0), -45)
    vein_solid.translate(App.Vector(0, 0, leaf_local_z_pos))
    
    # Protrude slightly from leaf
    vein_prot_dist = 0.5 * SF
    vein_prot = -vein_prot_dist if not is_back_face else vein_prot_dist
    vein_solid.translate(App.Vector(0, vein_prot, 0))

    if is_back_face:
        vein_solid.rotate(App.Vector(0,0,0), rot_axis, rot_angle)
    
    vein_solid.translate(App.Vector(center_x, face_y + gear_y_shift, center_z))
    
    obj_vein = doc.addObject("Part::Feature", f"Vein_{suffix}")
    obj_vein.Shape = vein_solid
    obj_vein.ViewObject.ShapeColor = c_vein_white


# ==========================================
# MAIN DRAWING FUNCTION FOR THE CELL
# ==========================================

def draw_battery_cell(doc, offset=(0,0,0)):
    # --- PARAMETERS SCALED ---
    bat_w = 100.0 * SF
    bat_d = 25.0 * SF
    bat_h = 90.0 * SF
    top_h = 3.0 * SF
    
    # Colors
    c_blue   = (0.0, 0.35, 0.58)
    c_red    = (0.70, 0.0, 0.0)
    c_black  = (0.1, 0.1, 0.1)
    c_silver = (0.85, 0.85, 0.85)
    c_white  = (1.0, 1.0, 1.0)

    # --- A. BODY ---
    make_box(doc, "Battery_Body", bat_w, bat_d, bat_h, 0, 0, 0, c_blue, offset)
    make_box(doc, "Battery_Cap", bat_w, bat_d, top_h, 0, 0, bat_h, c_blue, offset)

    # --- B. TERMINALS ---
    term_r = 7.0 * SF
    term_h = 8.0 * SF
    y_center = bat_d / 2
    z_base = bat_h + top_h
    
    # Positions
    pos_x_loc = 20 * SF
    neg_x_loc = 80 * SF
    
    # Positive
    make_cylinder(doc, "Pos_Base", term_r, term_h, pos_x_loc, y_center, z_base, c_red, offset)
    make_cylinder(doc, "Pos_Tip", term_r * 0.7, 2.0 * SF, pos_x_loc, y_center, z_base + term_h, c_silver, offset)
    
    # Pos Signs (scaled dims and coords)
    # V: 2x10x1 -> 2*SF, 10*SF, 1*SF. Position: 19, 2, h-2
    make_box(doc, "Pos_Sign_V", 2*SF, 10*SF, 1*SF, 19*SF, 2*SF, bat_h - (2*SF), c_white, offset, rotation_angle=90, rotation_axis=App.Vector(1,0,0))
    # H: 10x2x1 -> Position: 15, 2, h-6
    make_box(doc, "Pos_Sign_H", 10*SF, 2*SF, 1*SF, 15*SF, 2*SF, bat_h - (6*SF), c_white, offset, rotation_angle=90, rotation_axis=App.Vector(1,0,0))

    # Negative
    make_cylinder(doc, "Neg_Base", term_r, term_h, neg_x_loc, y_center, z_base, c_black, offset)
    make_cylinder(doc, "Neg_Tip", term_r * 0.7, 2.0 * SF, neg_x_loc, y_center, z_base + term_h, c_silver, offset)
    # Neg Sign: 10x2x1. Position: 75, 2, h-6
    make_box(doc, "Neg_Sign", 10*SF, 2*SF, 1*SF, 75*SF, 2*SF, bat_h - (6*SF), c_white, offset, rotation_angle=90, rotation_axis=App.Vector(1,0,0))

    # --- C. LOGOS (BOTH SIDES) ---
    logo_cx = bat_w / 2
    logo_cz = bat_h / 2
    
    # 1. Front Logo (Positioned at y = 0, facing -Y)
    draw_logo(doc, "Front", logo_cx, 0, logo_cz, offset, is_back_face=False)
    
    # 2. Back Logo (Positioned at y = bat_d, facing +Y)
    draw_logo(doc, "Back", logo_cx, bat_d, logo_cz, offset, is_back_face=True)


def make_robot_pipe(doc, name, p1, p2, radius=None, color=(0.8,0.8,0.8), offset=(0,0,0), sf=1.0):
    if radius is None: 
        radius = 14.0 * sf
    vec = App.Vector(p2[0]-p1[0], p2[1]-p1[1], p2[2]-p1[2])
    height = vec.Length
    if height < (0.001 * sf): return None
    obj = doc.addObject("Part::Feature", name)
    shape = Part.makeCylinder(radius, height)
    z_axis = App.Vector(0, 0, 1)
    rot_axis = z_axis.cross(vec)
    if rot_axis.Length > 0.0001:
        angle = math.degrees(z_axis.getAngle(vec))
        shape.rotate(App.Vector(0,0,0), rot_axis, angle)
    elif vec.z < 0:
        shape.rotate(App.Vector(0,0,0), App.Vector(1,0,0), 180)
    shape.translate(App.Vector(p1[0] + offset[0], p1[1] + offset[1], p1[2] + offset[2]))
    obj.Shape = shape
    try:
        if App.GuiUp:
            obj.ViewObject.ShapeColor = color
    except:
        pass
    return obj

# ==============================================================================
# ROBOTIC ARM DRAWING FUNCTION
# ==============================================================================

def draw_robotic_arm(doc, offset_coords=(0,0,0)):
    # ==========================================
    # CONFIGURATION
    # ==========================================
    SF = 2.0 

    COL_YELLOW = (1.0, 0.8, 0.0)
    COL_BLACK  = (0.1, 0.1, 0.1)
    COL_SILVER = (0.75, 0.75, 0.75)
    COL_CABLE  = (0.05, 0.05, 0.05)

    # --- 1. THE PEDESTAL ---
    pedestal_w = 800 * SF
    pedestal_h = 700 * SF
    
    make_box(doc, "Pedestal_Main", pedestal_w, pedestal_w, pedestal_h, -pedestal_w/2, -pedestal_w/2, 0, COL_BLACK, offset=offset_coords)
    make_box(doc, "Pedestal_Plate", pedestal_w + (100*SF), pedestal_w + (100*SF), 50*SF, -(pedestal_w/2 + 50*SF), -(pedestal_w/2 + 50*SF), pedestal_h, COL_BLACK, offset=offset_coords)
    make_box(doc, "Pedestal_Detail_F", pedestal_w - (100*SF), 50*SF, pedestal_h - (100*SF), -(pedestal_w/2 - 50*SF), -pedestal_w/2 - 50*SF, 50*SF, COL_SILVER, offset=offset_coords)

    # --- 2. TURRET ---
    turret_z = pedestal_h + (50*SF)
    make_robot_pipe(doc, "Turret_Base", (0,0,turret_z), (0,0,turret_z + (200*SF)), radius=350*SF, color=COL_BLACK, offset=offset_coords, sf=SF)
    make_robot_pipe(doc, "Turret_Body", (0,0,turret_z + (200*SF)), (0,0,turret_z + (500*SF)), radius=300*SF, color=COL_YELLOW, offset=offset_coords, sf=SF)

    # --- 3. LOWER ARM ---
    shoulder_z = turret_z + (500*SF)
    make_robot_pipe(doc, "Shoulder_Cap_L", (0, -350*SF, shoulder_z), (0, -300*SF, shoulder_z), radius=200*SF, color=COL_BLACK, offset=offset_coords, sf=SF)
    make_robot_pipe(doc, "Shoulder_Cap_R", (0, 300*SF, shoulder_z), (0, 350*SF, shoulder_z), radius=200*SF, color=COL_BLACK, offset=offset_coords, sf=SF)

    elbow_pt = (-300*SF, 0, shoulder_z + 800*SF)
    shoulder_pt = (0, 0, shoulder_z)
    make_robot_pipe(doc, "Lower_Arm_Main", shoulder_pt, elbow_pt, radius=250*SF, color=COL_YELLOW, offset=offset_coords, sf=SF)
    
    # Counterweight (using Y-axis rotation based on middle tuple value)
    make_box(doc, "Counterweight", 300*SF, 400*SF, 400*SF, -400*SF, -200*SF, shoulder_z + 100*SF, COL_YELLOW, offset=offset_coords, rotation_angle=-20, rotation_axis=App.Vector(0,1,0))

    # --- 4. UPPER ARM ---
    wrist_pt = (1200*SF, 0, shoulder_z + 600*SF) 
    make_robot_pipe(doc, "Elbow_Joint", (elbow_pt[0], -300*SF, elbow_pt[2]), (elbow_pt[0], 300*SF, elbow_pt[2]), radius=180*SF, color=COL_YELLOW, offset=offset_coords, sf=SF)
    make_robot_pipe(doc, "Forearm", elbow_pt, wrist_pt, radius=140*SF, color=COL_YELLOW, offset=offset_coords, sf=SF)
    
    make_box(doc, "Forearm_Rib", 800*SF, 100*SF, 50*SF, 0, -50*SF, shoulder_z + 850*SF, COL_YELLOW, offset=offset_coords, rotation_angle=-10, rotation_axis=App.Vector(0,1,0))

    # --- 5. WRIST ---
    wrist_end = (wrist_pt[0] + 200*SF, wrist_pt[1], wrist_pt[2] - 100*SF)
    make_robot_pipe(doc, "Wrist_1", wrist_pt, wrist_end, radius=130*SF, color=COL_BLACK, offset=offset_coords, sf=SF)
    wrist_face = (wrist_end[0] + 100*SF, wrist_end[1], wrist_end[2] - 50*SF)
    make_robot_pipe(doc, "Wrist_2", wrist_end, wrist_face, radius=110*SF, color=COL_YELLOW, offset=offset_coords, sf=SF)

    # --- 6. GRIPPER ---
    grip_base_pos = (wrist_face[0], wrist_face[1], wrist_face[2])
    make_box(doc, "Gripper_Base", 100*SF, 400*SF, 200*SF, grip_base_pos[0], -200*SF, grip_base_pos[2]-100*SF, COL_BLACK, offset=offset_coords, rotation_angle=25, rotation_axis=App.Vector(0,1,0))
    
    # Fingers
    make_box(doc, "Finger_L1", 300*SF, 50*SF, 100*SF, grip_base_pos[0]+50*SF, -200*SF, grip_base_pos[2], COL_BLACK, offset=offset_coords, rotation_angle=45, rotation_axis=App.Vector(0,1,0))
    make_box(doc, "Finger_L2", 200*SF, 50*SF, 50*SF, grip_base_pos[0]+250*SF, -200*SF, grip_base_pos[2]-150*SF, COL_BLACK, offset=offset_coords, rotation_angle=-10, rotation_axis=App.Vector(0,1,0))
    
    make_box(doc, "Finger_R1", 300*SF, 50*SF, 100*SF, grip_base_pos[0]+50*SF, 150*SF, grip_base_pos[2], COL_BLACK, offset=offset_coords, rotation_angle=45, rotation_axis=App.Vector(0,1,0))
    make_box(doc, "Finger_R2", 200*SF, 50*SF, 50*SF, grip_base_pos[0]+250*SF, 150*SF, grip_base_pos[2]-150*SF, COL_BLACK, offset=offset_coords, rotation_angle=-10, rotation_axis=App.Vector(0,1,0))

    # --- 7. CABLING ---
    c1 = (0, 200*SF, shoulder_z + 200*SF)
    c2 = (-200*SF, 200*SF, shoulder_z + 900*SF)
    c3 = (200*SF, 150*SF, shoulder_z + 800*SF)
    c4 = (800*SF, 150*SF, shoulder_z + 700*SF)
    
    make_robot_pipe(doc, "Cable_1", (0, 150*SF, turret_z+300*SF), c1, radius=40*SF, color=COL_CABLE, offset=offset_coords, sf=SF)
    make_robot_pipe(doc, "Cable_2", c1, c2, radius=40*SF, color=COL_CABLE, offset=offset_coords, sf=SF)
    make_robot_pipe(doc, "Cable_3", c2, c3, radius=40*SF, color=COL_CABLE, offset=offset_coords, sf=SF)
    make_robot_pipe(doc, "Cable_4", c3, c4, radius=30*SF, color=COL_CABLE, offset=offset_coords, sf=SF)
    
    make_robot_pipe(doc, "Clamp_1", c3, (c3[0]+50*SF, c3[1], c3[2]), radius=45*SF, color=COL_BLACK, offset=offset_coords, sf=SF)
    make_robot_pipe(doc, "Clamp_2", c4, (c4[0]+50*SF, c4[1], c4[2]), radius=45*SF, color=COL_BLACK, offset=offset_coords, sf=SF)



def make_pipe(doc, name, p1, p2, radius=None, color=(0.8,0.8,0.8), offset=(0,0,0), sf=1.0):
    """
    Creates a cylinder. 
    sf: Scale Factor passed from main function.
    """
    # Handle Default Radius logic locally using passed sf
    if radius is None: 
        radius = 14.0 * sf
        
    vec = App.Vector(p2[0]-p1[0], p2[1]-p1[1], p2[2]-p1[2])
    height = vec.Length
    # Minimal height check scaled
    if height < (0.001 * sf): return None
    
    obj = doc.addObject("Part::Feature", name)
    shape = Part.makeCylinder(radius, height)
    
    # Orient cylinder
    z_axis = App.Vector(0, 0, 1)
    rot_axis = z_axis.cross(vec)
    if rot_axis.Length > 0.0001:
        angle = math.degrees(z_axis.getAngle(vec))
        shape.rotate(App.Vector(0,0,0), rot_axis, angle)
    elif vec.z < 0:
        shape.rotate(App.Vector(0,0,0), App.Vector(1,0,0), 180)
        
    # Translate to p1 + offset
    shape.translate(App.Vector(p1[0] + offset[0], p1[1] + offset[1], p1[2] + offset[2]))
    obj.Shape = shape
    obj.ViewObject.ShapeColor = color
    
    # Add simulated joints at ends (black spheres)
    j_rad = radius * 1.5
    col_joint = (0.1, 0.1, 0.1) # Hardcoded black for joints
    
    j1 = doc.addObject("Part::Feature", name + "_j1")
    j1.Shape = Part.makeSphere(j_rad, App.Vector(p1[0] + offset[0], p1[1] + offset[1], p1[2] + offset[2]))
    j1.ViewObject.ShapeColor = col_joint
    
    j2 = doc.addObject("Part::Feature", name + "_j2")
    j2.Shape = Part.makeSphere(j_rad, App.Vector(p2[0] + offset[0], p2[1] + offset[1], p2[2] + offset[2]))
    j2.ViewObject.ShapeColor = col_joint
    
    return obj


# ==============================================================================
# 2. MAIN LOGIC FUNCTION FOR THE PACKAGING TABLE
# ==============================================================================

def draw_assembly_workstation(doc, offset_coords=(0,0,0)):
    # ==========================================
    # CONFIGURATION (Moved Inside)
    # ==========================================
    # Scale Factor: 10.0 (Tenfold increase)
    SF = 5.0 

    # Colors (RGB tuples)
    COL_PIPE = (0.8, 0.8, 0.8)       # Silver/Aluminum
    COL_JOINT = (0.1, 0.1, 0.1)      # Black joints
    COL_TABLE = (0.9, 0.9, 0.9)      # White/Grey laminate
    COL_BOARD = (0.6, 0.45, 0.3)     # Cardboard/Wood brown
    COL_BELT = (0.2, 0.6, 0.3)       # Green conveyor belt
    COL_SHIRT = (0.0, 0.4, 0.8)      # Blue worker shirt
    COL_SKIN = (0.8, 0.6, 0.5)       # Skin tone
    COL_BIN = (0.7, 0.7, 0.75)       # Grey plastic bins

    # Dimensions Scaled
    table_w = 1400 * SF
    table_d = 800 * SF
    table_h = 400 * SF
    overhead_h = 2100 * SF

    # --- Frame Skeleton ---
    # Vertical Posts
    posts = [
        (0, 0), (table_w, 0),       # Front
        (0, table_d), (table_w, table_d) # Back
    ]

    for idx, (px, py) in enumerate(posts):
        # Back posts go up, front posts stop at table
        h = overhead_h if idx > 1 else table_h + (100 * SF) 
        make_pipe(doc, f"Post_{idx}", (px, py, 0), (px, py, h), color=COL_PIPE, offset=offset_coords, sf=SF)

    # Horizontal Beams (Table Level) - Z offset scaled
    beam_low_z = 200 * SF
    make_pipe(doc, "Beam_Low_F", (0, 0, beam_low_z), (table_w, 0, beam_low_z), color=COL_PIPE, offset=offset_coords, sf=SF)
    make_pipe(doc, "Beam_Low_B", (0, table_d, beam_low_z), (table_w, table_d, beam_low_z), color=COL_PIPE, offset=offset_coords, sf=SF)
    make_pipe(doc, "Beam_Low_L", (0, 0, beam_low_z), (0, table_d, beam_low_z), color=COL_PIPE, offset=offset_coords, sf=SF)
    make_pipe(doc, "Beam_Low_R", (table_w, 0, beam_low_z), (table_w, table_d, beam_low_z), color=COL_PIPE, offset=offset_coords, sf=SF)

    beam_table_z = table_h - (50 * SF)
    make_pipe(doc, "Beam_Table_F", (0, 0, beam_table_z), (table_w, 0, beam_table_z), color=COL_PIPE, offset=offset_coords, sf=SF)
    make_pipe(doc, "Beam_Table_B", (0, table_d, beam_table_z), (table_w, table_d, beam_table_z), color=COL_PIPE, offset=offset_coords, sf=SF)
    make_pipe(doc, "Beam_Table_L", (0, 0, beam_table_z), (0, table_d, beam_table_z), color=COL_PIPE, offset=offset_coords, sf=SF)
    make_pipe(doc, "Beam_Table_R", (table_w, 0, beam_table_z), (table_w, table_d, beam_table_z), color=COL_PIPE, offset=offset_coords, sf=SF)

    # Overhead Structure
    overhead_off = 400 * SF
    make_pipe(doc, "Overhead_Top_F", (0, table_d - overhead_off, overhead_h), (table_w, table_d - overhead_off, overhead_h), color=COL_PIPE, offset=offset_coords, sf=SF)
    make_pipe(doc, "Overhead_Top_B", (0, table_d, overhead_h), (table_w, table_d, overhead_h), color=COL_PIPE, offset=offset_coords, sf=SF)
    make_pipe(doc, "Overhead_Connect_L", (0, table_d, overhead_h), (0, table_d - overhead_off, overhead_h), color=COL_PIPE, offset=offset_coords, sf=SF)
    make_pipe(doc, "Overhead_Connect_R", (table_w, table_d, overhead_h), (table_w, table_d - overhead_off, overhead_h), color=COL_PIPE, offset=offset_coords, sf=SF)

    # Light Bar
    make_box(doc, "Light", table_w - (100*SF), 50*SF, 30*SF, 50*SF, table_d - (300*SF), overhead_h - (50*SF), (0.95, 0.95, 1.0), offset=offset_coords)

    # --- Surfaces & Panels ---
    # Main Tabletop
    make_box(doc, "TableTop", table_w + (40*SF), table_d + (40*SF), 25*SF, -20*SF, -20*SF, table_h, COL_TABLE, offset=offset_coords)

    # Side Panel (Brown Board)
    make_box(doc, "SidePanel", 20*SF, table_d, table_h, -20*SF, 0, 0, COL_BOARD, offset=offset_coords)
    make_box(doc, "BackPanelLow", table_w, 20*SF, table_h/2, 0, table_d, 0, COL_BOARD, offset=offset_coords)

    # --- Accessories ---
    # Monitor Arm & Screen
    make_pipe(doc, "MonitorPost", (table_w/2, table_d, table_h), (table_w/2, table_d, table_h + (400*SF)), color=COL_PIPE, offset=offset_coords, sf=SF)
    make_box(doc, "Monitor", 400*SF, 30*SF, 250*SF, (table_w/2) - (200*SF), table_d - (200*SF), table_h + (300*SF), (0.2, 0.2, 0.2), offset=offset_coords)

    # Drawer Unit (Under table)
    make_box(doc, "DrawerUnit", 200*SF, 300*SF, 300*SF, 100*SF, 100*SF, table_h - (320*SF), (0.95, 0.95, 0.95), offset=offset_coords)
    make_box(doc, "DrawerHandle", 200*SF, 20*SF, 20*SF, 200*SF, 100*SF, table_h - (60*SF), (0.2, 0.2, 0.2), offset=offset_coords)


    # ==============================================================================
    # 3. CONVEYOR BELT
    # ==============================================================================
    conv_x = table_w + (400 * SF)
    conv_y = 200 * SF
    conv_len = 2000 * SF
    conv_w = 500 * SF
    conv_h = 400 * SF

    # Legs
    num_legs = 4
    spacing = conv_len / (num_legs - 1)
    leg_rad = 30 * SF

    for i in range(num_legs):
        lx = conv_x + (i * spacing)
        make_pipe(doc, f"ConvLeg_{i}_F", (lx, conv_y, 0), (lx, conv_y, conv_h), radius=leg_rad, color=(0.7, 0.7, 0.7), offset=offset_coords, sf=SF)
        make_pipe(doc, f"ConvLeg_{i}_B", (lx, conv_y + conv_w, 0), (lx, conv_y + conv_w, conv_h), radius=leg_rad, color=(0.7, 0.7, 0.7), offset=offset_coords, sf=SF)

    # Frame
    make_box(doc, "ConvFrameL", conv_len, 20*SF, 60*SF, conv_x, conv_y, conv_h, (0.6, 0.6, 0.6), offset=offset_coords)
    make_box(doc, "ConvFrameR", conv_len, 20*SF, 60*SF, conv_x, conv_y + conv_w - (20*SF), conv_h, (0.6, 0.6, 0.6), offset=offset_coords)

    # Belt
    make_box(doc, "ConvBelt", conv_len, conv_w - (40*SF), 10*SF, conv_x, conv_y + (20*SF), conv_h + (40*SF), COL_BELT, offset=offset_coords)
    
    # ==============================================================================
    # 4. MOBILE CART (Under conveyor)
    # ==============================================================================
    cart_x = conv_x + (1000 * SF)
    cart_y = conv_y + (100 * SF)
    cart_w = 400 * SF
    cart_h = 500 * SF
    cart_depth_off = 300 * SF
    cart_shelf_off = 50 * SF

    make_pipe(doc, "Cart_L1", (cart_x, cart_y, cart_shelf_off), (cart_x, cart_y, cart_h), color=COL_PIPE, offset=offset_coords, sf=SF)
    make_pipe(doc, "Cart_L2", (cart_x + cart_w, cart_y, cart_shelf_off), (cart_x + cart_w, cart_y, cart_h), color=COL_PIPE, offset=offset_coords, sf=SF)
    make_pipe(doc, "Cart_L3", (cart_x, cart_y + cart_depth_off, cart_shelf_off), (cart_x, cart_y + cart_depth_off, cart_h), color=COL_PIPE, offset=offset_coords, sf=SF)
    make_pipe(doc, "Cart_L4", (cart_x + cart_w, cart_y + cart_depth_off, cart_shelf_off), (cart_x + cart_w, cart_y + cart_depth_off, cart_h), color=COL_PIPE, offset=offset_coords, sf=SF)
    make_box(doc, "CartShelf", cart_w, 300*SF, 20*SF, cart_x, cart_y, 200*SF, COL_TABLE, offset=offset_coords)

    # Stacked Totes on Cart
    tote_l = 350 * SF
    tote_w = 250 * SF
    tote_h = 150 * SF
    tote_off = 25 * SF

    make_box(doc, "Tote1", tote_l, tote_w, tote_h, cart_x + tote_off, cart_y + tote_off, cart_h, COL_BIN, offset=offset_coords)
    make_box(doc, "Tote2", tote_l, tote_w, tote_h, cart_x + tote_off, cart_y + tote_off, cart_h + tote_h, COL_BIN, offset=offset_coords)



def create_layout():
    doc = ensure_document()
    #Draw Hopper
    build_ibc_hopper(doc, offset=( -4000, 0, 0)) 
    build_ibc_hopper(doc, offset=( -4000, -4000, 0)) 
    # Draw the machine with an offset
    create_rectangular_pipe("ExitChute", -500, 0, 0, 4000, 800, 800)
    create_rectangular_pipe("Chute", -500, -4000, 0, 4000, 800, 800)
    #Draw the mixing machine
    draw_industrial_mixer(doc, offset_coords=(3000, 0, 0))
    draw_industrial_mixer(doc, offset_coords=(3000, -4000, 0))
    #Draw coating vessel   
    draw_coating_line(doc, offset_coords=(7000, 0, 0))   
    draw_coating_line(doc, offset_coords=(7000, -4000, 0))
    #Draw heat exchanger
    draw_alfa_laval_phe(doc, offset_coords=(15800, -8500, 0))
    draw_alfa_laval_phe(doc, offset_coords=(15800, 5000, 0))
    # Blue Storage Tanks placed besides the coating vessel
    tank_offset1 = (10000, -8000, 0)
    tank_offset2 = (10000, 5500, 0)
    build_tank(doc, offset=tank_offset1)
    build_tank(doc, offset=tank_offset2)
    # Draw coating liquid tank 
    draw_fuel_tank(doc, offset_coords=(20000, -8000, 0))
    draw_fuel_tank(doc, offset_coords=(20000, 5500, 0))   
    # Draw the calendering machine
    draw_fabric_machine(doc, offset_coords=(22000, 0, 0))
    draw_fabric_machine(doc, offset_coords=(22000, -6000, 0))
    #Draw the horizontal conveyor belts
    pocket_conveyor(doc, offset=(17000, 1500, 1000))
    pocket_conveyor(doc, offset=(17000,-3500,1000))
    pocket_conveyor(doc, offset=(24000,-4000,1000))
    pocket_conveyor(doc, offset=(24000, 0,1000))
    pocket_conveyor(doc, offset=(30000, -1000,1200))
    pocket_conveyor(doc, offset=(30000, -3000,1200))
    pocket_conveyor(doc, offset=(42000, -3000,1000))
    pocket_conveyor(doc, offset=(48000, -3000,1000))
    pocket_conveyor(doc, offset=(60000, -3000,1000))
    pocket_conveyor(doc, offset=(65500, -3000,1000))
    pocket_conveyor(doc, offset=(71500, -3000,1000))
    pocket_conveyor(doc, offset=(85500, -2000,2500))
    pocket_conveyor(doc, offset=(105000, -2000,3500))
    pocket_conveyor(doc, offset=(125000, -2000,3500))
    pocket_conveyor(doc, offset=(135000, -2000,3500))
    pocket_conveyor(doc, offset=(143000, -2000,3500))
    # --- 1. PIPE: ANODE MIXER TO ANODE COATER ---
    # From Anode mixer discharge to Anode coater feed manifold
    anode_mixer = App.Vector(3500, 500, 1000)
    anode_coater = App.Vector(7500, 500, 1000)
    create_jointed_pipe(doc, "Mixer_Coater_Cyc", anode_mixer, anode_coater, 200, 240, col_pipe_yellow)
    # --- 2. PIPE: CATHODE MIXER TO CATHODE COATER ---
    # From Cathode mixer discharge to Cathode coater feed manifold
    cathode_mixer = App.Vector(3500, -3500, 1000)
    cathode_coater = App.Vector(7500, -3500, 1000)
    create_jointed_pipe(doc, "Mixer_Cathode_Cyc", cathode_mixer, cathode_coater, 220, 270, col_pipe_yellow)
     # --- 3. PIPE: ANODE COATER TO HEAT EXCHANGER ---
    # From Anode mixer discharge to Anode coater feed manifold
    anode_coater1 = App.Vector(16000, 1000, 4000)
    heat_exchanger1 = App.Vector(16000, 1000, 6000)
    create_jointed_pipe(doc, "Anode_Coater_Exchange_Cyc", anode_coater1, heat_exchanger1, 170, 100, col_pipe_yellow)
    anode_coater2 = App.Vector(16000, 1000, 5900)
    heat_exchanger2 = App.Vector(16000, 6500, 5900)
    create_jointed_pipe(doc, "Anode_Coater_Exchange_Cyc", anode_coater2, heat_exchanger2, 170, 100, col_pipe_yellow)
    anode_coater3 = App.Vector(16000, 6500, 5900)
    heat_exchanger3 = App.Vector(16000, 6500, 2500)
    create_jointed_pipe(doc, "Anode_Coater_Exchange_Cyc", anode_coater3, heat_exchanger3, 170, 100, col_pipe_yellow)
    # --- 4. PIPE: CATHODE COATER TO HEAT EXCHANGER ---
    # From Cathode mixer discharge to Cathode coater feed manifold
    cathode_coater1 = App.Vector(16000, -3000, 4000)
    Heat_exchanger1 = App.Vector(16000, -3000, 6000)
    create_jointed_pipe(doc, "Anode_Coater_Exchange_Cyc", cathode_coater1, Heat_exchanger1, 170, 100, col_pipe_yellow)
    cathode_coater2 = App.Vector(16000, -3000, 5900)
    Heat_exchanger2 = App.Vector(16000, -7000, 5900)
    create_jointed_pipe(doc, "Anode_Coater_Exchange_Cyc", cathode_coater2, Heat_exchanger2, 170, 100, col_pipe_yellow)
    cathode_coater3 = App.Vector(16000, -7000, 5900)
    Heat_exchanger3 = App.Vector(16000, -7000, 2500)
    create_jointed_pipe(doc, "Anode_Coater_Exchange_Cyc", cathode_coater3, Heat_exchanger3, 170, 100, col_pipe_yellow)
      # --- 5. PIPE: STORAGE TANK TO HEAT EXCHANGER ---
    # From Storage tank discharge to Heat exchanger feed manifold
    tank_coater1 = App.Vector(11500, 5400, 2500)
    tank_exchanger1 = App.Vector(11500, 5400, 4000)
    create_jointed_pipe(doc, "Anode_Coater_Exchange_Cyc", tank_coater1, tank_exchanger1, 170, 100, col_pipe_yellow)
    tank_coater2 = App.Vector(11500, 5400, 3900)
    tank_exchanger2 = App.Vector(16000, 5400, 3900)
    create_jointed_pipe(doc, "Anode_Coater_Exchange_Cyc", tank_coater2, tank_exchanger2, 170, 100, col_pipe_yellow)
    tank_coater3 = App.Vector(16000, 5400, 3900)
    tank_exchanger3 = App.Vector(16000, 5400, 2500)
    create_jointed_pipe(doc, "Anode_Coater_Exchange_Cyc", tank_coater3, tank_exchanger3, 170, 100, col_pipe_yellow)
    # --- 6. PIPE: STORAGE TANK TO HEAT EXCHANGER ---
    # From Cathode mixer discharge to Cathode coater feed manifold
    Tank_coater1 = App.Vector(11500, -8000, 2500)
    Tank_exchanger1 = App.Vector(11500, -8000, 4000)
    create_jointed_pipe(doc, "Anode_Coater_Exchange_Cyc", Tank_coater1, Tank_exchanger1, 170, 100, col_pipe_yellow)
    Tank_coater2 = App.Vector(11500, -8000, 3900)
    Tank_exchanger2 = App.Vector(16000, -8000, 3900)
    create_jointed_pipe(doc, "Anode_Coater_Exchange_Cyc", Tank_coater2, Tank_exchanger2, 170, 100, col_pipe_yellow)
    Tank_coater3 = App.Vector(16000, -8000, 3900)
    Tank_exchanger3 = App.Vector(16000, -8000, 2500)
    create_jointed_pipe(doc, "Anode_Coater_Exchange_Cyc", Tank_coater3, Tank_exchanger3, 170, 100, col_pipe_yellow)
    # --- 7. PIPE: HEAT EXCHANGER TO STORAGE TANK ---
    # From Heat exchanger discharge to Storage Tank feed manifold
    heat_exchanger1 = App.Vector(16000, 5400, 1500)
    storage_tank1 = App.Vector(21000, 5400, 1500)
    create_jointed_pipe(doc, "Anode_Coater_Exchange_Cyc", heat_exchanger1, storage_tank1, 170, 100, col_pipe_yellow)
    # --- 8. PIPE: HEAT EXCHANGER TO STORAGE TANK ---
    # From Heat exchanger discharge to Storage Tank feed manifold
    Heat_exchanger1 = App.Vector(16000, -8000, 1500)
    Storage_tank1 = App.Vector(21000, -8000, 1500)
    create_jointed_pipe(doc, "Anode_Coater_Exchange_Cyc", Heat_exchanger1, Storage_tank1, 170, 100, col_pipe_yellow)
    Heat_exchanger2 = App.Vector(21000, 5400, 1500)
    Storage_tank2 = App.Vector(21000, 5400, 1000)
    create_jointed_pipe(doc, "Anode_Coater_Exchange_Cyc", Heat_exchanger2, Storage_tank2, 170, 100, col_pipe_yellow)
    # Call build function with offset coordinates
    liquid_tank(doc, offset=(0.0, -8000.0, 0.0))
    liquid_tank(doc, offset=(0.0, 5500.0, 0.0))
    # --- 9. PIPE: STORAGE TANK TO MIXING TANK ---
    # From Storage tank  discharge to Mixing Tank feed manifold
    liquid_tank1 = App.Vector(0, 5500, 1500)
    mixing_tank1 = App.Vector(3300, 5500, 1500)
    create_jointed_pipe(doc, "Anode_Coater_Exchange_Cyc", liquid_tank1, mixing_tank1, 100, 100, col_pipe_yellow)
    liquid_tank2 = App.Vector(3300, 5490, 1500)
    mixing_tank2 = App.Vector(3300, 1000, 1500)
    create_jointed_pipe(doc, "Anode_Coater_Exchange_Cyc", liquid_tank2, mixing_tank2, 100, 100, col_pipe_yellow)
    # --- 9. PIPE: STORAGE TANK TO MIXING TANK ---
    # From Storage tank  discharge to Mixing Tank feed manifold
    Liquid_tank1 = App.Vector(0, -8500, 1500)
    Mixing_tank1 = App.Vector(3300,-8500, 1500)
    create_jointed_pipe(doc, "Anode_Coater_Exchange_Cyc", Liquid_tank1, Mixing_tank1, 100, 100, col_pipe_yellow)
    Liquid_tank2 = App.Vector(3300, -8500, 1500)
    Mixing_tank2 = App.Vector(3300, -3000, 1500)
    create_jointed_pipe(doc, "Anode_Coater_Exchange_Cyc", Liquid_tank2, Mixing_tank2, 100, 100, col_pipe_yellow)
    #Draw Slitting Machine
    draw_slitting_machine(doc, offset_coords=(30000, 0, 0))
    draw_slitting_machine(doc, offset_coords=(30000, -4000, 0))
    #Draw stacking machine
    draw_battery_stacker(doc, offset_coords=(36000, -4500, 0))
    # Draw the Hot pressing machine
    draw_processing_machine(doc, offset_coords=(46000, -3500, 0))
    #Draw ultrasonic welding machine
    draw_assembly_machine(doc, offset_coords=(54000, -3500, 0))
    #Draw the laser welding machine
    draw_laser_welding_machine(doc, offset_coords=(66000, -3500, 0))
    #Draw the sealing machine
    draw_lamination_machine(doc, offset_coords=(75000, -3500, 0))
    #Draw the machine with an offset
    draw_industrial_machine(doc, offset_coords=(90000, -4500, 0))    
    # Drawing the electrolyte filling machine
    draw_glovebox_system(doc, offset_coords=(110000, -2000, 0))
    # Drawing the Formation Machine
    draw_battery_cabinet(doc, offset_coords=(130000, -2000, 0))
    # Drawing the Grading machine 
    draw_acey_machine(doc, offset_coords=(140000, -2500, 0))
    #Draw charging and discharging machine    
    draw_cleaning_machine(doc, offset_coords=(148000, -2000, 0))
    #Drawing the positive coated plate
    #Particle to move along the belt
    al_offset = (16500, -3350, 1200)
    draw_sectional_plate(doc, al_offset)
    #Drawing the negative coated plate
    #Particle to move along the belt
    cu_offset = (16500, 1600, 1150) 
    draw_copper_plate(doc, cu_offset)
    #Drawing the Stacked Cell
    #Particle to move along the belt
    stacked_offset = (42500, -3000, 1100)
    draw_stacked_cell(doc, stacked_offset)
    #Drawing the battery 
    #Particle to move along the belt
    battery_offset1 = (86000, -1900, 2500)
    draw_battery_cell(doc, battery_offset1)
    #Particle to move along the belt
    battery_offset2 = ( 86000, -1525, 2500)
    draw_battery_cell(doc, battery_offset2)
    #Particle to move along the belt
    battery_offset3 = (86000, -1150, 2500)
    draw_battery_cell(doc, battery_offset3)
    #Particle to move along the belt
    battery_offset4 = (86000, -775, 2500)
    draw_battery_cell(doc, battery_offset4)
    # 2. Call the main logic function using offset coordinates
    #The arm to rotate along the axis
    draw_robotic_arm(doc, offset_coords=(162000, 1000, 700))
    draw_robotic_arm(doc, offset_coords=(169000, 1000,700))
    # 2. Call the main logic function using the requested offset coordinates
    draw_assembly_workstation(doc, offset_coords=(161000, -2000, 0))

    doc.recompute()
    try:
        Gui.SendMsgToActiveView("ViewFit")
        Gui.activeDocument().activeView().viewAxonometric()
    except:
        pass
    print("Lithium Battery Plant Assembled.")

import csv
import os

def generate_and_save_equipment_report():
    # Equipment Data: (Name, Length_mm, Width_mm, Quantity)
    equipment_data = [
        ("IBC Hopper", 3600, 3000, 2),
        ("Industrial Mixer", 2400, 3000, 2),
        ("Coating Line", 12000, 3000, 2),
        ("Alfa Laval Heat Exchanger", 1200, 3000, 2),
        ("Water Storage Tank (Horizontal)", 5000, 2000, 2),
        ("Fuel/Coating Liquid Tank", 4200, 1100, 2),
        ("Calendering (Fabric) Machine", 4800, 3600, 2),
        ("Pocket Conveyor Belt", 6000, 1500, 16),
        ("Liquid Storage Tank (Vertical)", 2000, 2000, 2),
        ("Slitting Machine", 3600, 2000, 2),
        ("Battery Stacking Machine", 6600, 6800, 1),
        ("Hot Pressing Machine", 4800, 2400, 1),
        ("Ultrasonic Welding Machine", 8000, 4000, 1),
        ("Laser Welding Machine", 3600, 3000, 1),
        ("Lamination/Sealing Machine", 9600, 5400, 1),
        ("Industrial Drying Machine", 14000, 6000, 1),
        ("Electrolyte Filling (Glovebox)", 14400, 2400, 1),
        ("Battery Formation Cabinet", 4800, 2400, 1),
        ("Grading (ACEY) Machine", 3300, 4200, 1),
        ("Charging/Cleaning Machine", 15000, 3600, 1),
        ("Robotic Arm (Pedestal Base)", 1600, 1600, 2),
        ("Assembly Workstation", 7000, 4000, 1),
    ]

    # File Path (Saves to your user home folder)
    file_path = os.path.expanduser("~/factory_equipment_list.csv")

    # Header for the CSV
    header = ["Equipment Name", "Quantity", "Length (m)", "Width (m)", "Total Area (m2)"]
    rows_to_save = []
    grand_total_area = 0.0

    # Calculate Data
    for name, length_mm, width_mm, qty in equipment_data:
        l_m = length_mm / 1000.0
        w_m = width_mm / 1000.0
        total_item_area = (l_m * w_m) * qty
        grand_total_area += total_item_area
        rows_to_save.append([name, qty, l_m, w_m, round(total_item_area, 2)])

    # 1. SAVE TO CSV FILE
    try:
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(rows_to_save)
            writer.writerow([]) # Empty line
            writer.writerow(["GRAND TOTAL AREA", "", "", "", round(grand_total_area, 2)])
        print(f"\n✅ Data successfully stored at: {file_path}")
    except Exception as e:
        print(f"❌ Error saving file: {e}")

    # 2. PRINT TO CONSOLE (For immediate viewing)
    print("-" * 85)
    print(f"{'Equipment Name':<30} | {'Qty':<4} | {'L (m)':<7} | {'W (m)':<7} | {'Area (m2)':<10}")
    print("-" * 85)
    for row in rows_to_save:
        print(f"{row[0]:<30} | {row[1]:<4} | {row[2]:<7.2f} | {row[3]:<7.2f} | {row[4]:<10.2f}")
    print("-" * 85)
    print(f"GRAND TOTAL AREA: {grand_total_area:.2f} m2\n")


if __name__ == "__main__":
    create_layout()
    generate_and_save_equipment_report()