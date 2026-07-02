import FreeCAD as App
import Part
import FreeCADGui as Gui
import math
import random
from functools import reduce


# --- DIMENSIONS ---
# Feeder & Conveyor
feeder_length = 4000.0
feeder_width = 1200.0
feeder_height = 600.0
grizzly_length = 1000.0 
wall_thickness = 20.0
conv_length = 3000.0
conv_width = 800.0
roller_width = 700.0
conv_height = 800.0
rail_height = 120.0
rail_thick = 40.0
roller_dia = 60.0
roller_pitch = 85.0
frame_len = 4500.0
frame_width = 1600.0
frame_height = 1100.0
box_len = 1600.0
box_width = 1200.0
box_height = 900.0
trough_len = 8000.0
trough_dia = 800.0
trough_thick = 20.0
segment_len = 1000.0
augur_dia = trough_dia * 0.75
augur_pitch = trough_dia * 0.8
total_length = 10000.0
total_width = 3400.0
hopper_count = 4
section_len = total_length / hopper_count
leg_height = 1500.0
frame_beam_size = 80.0
housing_height = 3100.0
top_flat_width = 1000.0

width = 1600.0
depth = 1600.0
body_height = 2200.0
hopper_height = 1000.0
leg_height = 1400.0  # Height from floor to bottom of main body

# Discharge
discharge_size = 300.0


# Pyrolysis Dims
pyro_dia = 1400.0
pyro_cyl_height = 1600.0
pyro_dish_ratio = 0.35 

# Tank Dims
tank_dia = 2000.0
tank_len = 5000.0
tank_dish_ratio = 0.25
saddle_width = 300.0
leg_height = 1000.0

#Pneumatic Dimensions
belt_width = 800.0
horiz_len = 2400.0
incline_len = 7500.0
incline_angle = 25.0
frame_height = 150.0
rail_height = 300.0

#Crusher Dimensions
track_len = 3800.0
track_w = 600.0
track_h = 700.0
chassis_w = 2200.0

#Hydrocyclone Dimensions
num_cyclones = 4
cluster_radius = 900.0   # Center to cyclone center
tank_radius = 1000.0      # Central feed tank
launder_radius = 1200.0  # Bottom collection tub
launder_height = 2000.0

cyclone_dia = 640.0
cyclone_len_cyl = 900.0
cyclone_len_cone = 1600.0

mod_width = 1500.0  # Width of one hopper section
mod_depth = 2000.0  # Depth of the unit
num_mods = 2        # Two hopper sections side-by-side
total_width = mod_width * num_mods
housing_h = 3000.0
hopper_h = 1000.0
leg_h = 1500.0      # Legs go from ground to bottom of housing

# DMS
drum_dia = 2000.0
drum_len = 5500.0
incline_angle = 15.0
frame_width = 1100.0
leg_base_height = 1500.0

#Conveyor belt
# Geometry
belt_width = 800.0
frame_width = 1000.0
bottom_len = 1500.0
incline_len = 4000.0
top_len = 1500.0
incline_angle = 25.0
leg_base_height = 800.0  # Height of the lower section from floor

#Magnetic Separator
mag_tank_len = 3500.0
mag_tank_width = 2200.0
mag_tank_height = 2000.0
mag_wall_thick = 100.0

mag_side_box_width = 1000.0

mag_drum_dia = 1100.0
mag_drum_len = mag_tank_width - 200.0
mag_roller_dia = 1000.0

mag_chute_len = 2200.0
mag_chute_width = mag_drum_len

#Ball Mill
ballmill_drum_diameter = 1600.0
ballmill_drum_length = 3500.0
ballmill_girth_gear_dia = 2200.0
ballmill_girth_gear_width = 250.0
ballmill_base_frame_width = 2400.0
ballmill_base_frame_len = 5000.0
ballmill_rotation_axis_height = 1600.0

#Trommel Screener
trommel_drum_len = 6000.0
trommel_drum_dia = 2200.0
trommel_frame_width = 2800.0
trommel_support_leg_height = 1000.0
trommel_hopper_wall_height = 1500.0
trommel_tire_width = 300.0
trommel_tire_thickness = 100.0

#Declined Conveyor
dec_belt_width = 800.0
dec_frame_width = 1000.0
dec_high_flat_len = 1500.0    # Initial high section
dec_slope_len = 4500.0        # Descending section
dec_low_flat_len = 1500.0     # Final low section
dec_decline_angle = 25.0      # Angle of descent
dec_rail_h = 180.0
dec_start_height = 2800.0     # Starting elevation from floor

#Centrifugal Concentrator
centri_drum_diameter = 3300.0
centri_drum_h = 2400.0
centri_module_gap = 3200.0  # Spacing between units
centri_cradle_w = 2800.0
centri_cradle_h = 2000.0
centri_bolt_r = 16.0
centri_spout_dia = 500.0
centri_hose_radius = 80.0
centri_arch_radius = 800.0



# --- COLORS ---
col_steel_grey = (0.80, 0.80, 0.82)
col_liner_red = (0.75, 0.15, 0.15)
col_motor_teal = (0.0, 0.45, 0.45)
col_base_blue = (0.1, 0.1, 0.6)
col_black_rubber = (0.05, 0.05, 0.05)
col_spring_steel = (0.25, 0.25, 0.25)
col_frame_grey = (0.3, 0.3, 0.35)
col_roller_silver = (0.7, 0.7, 0.7)
col_foot_black = (0.1, 0.1, 0.1)
col_box_dark = (0.2, 0.2, 0.2)
col_button_red = (0.8, 0.1, 0.1)
COL_HOPPER_BLUE = (0.0, 0.4, 0.8)
COL_BOX_GREEN   = (0.2, 0.8, 0.2)
COL_FRAME_GREY  = (0.25, 0.3, 0.35)
COL_MOTOR_GREY  = (0.4, 0.4, 0.45)
COL_SHAFT_RED   = (0.8, 0.2, 0.2)
col_blue_liner = (0.2, 0.6, 0.9)
col_motor_grey = (0.3, 0.35, 0.4)
col_guard_yellow = (0.9, 0.8, 0.1)
col_lid_metal = (0.6, 0.6, 0.65)
col_tank_blue = (0.1, 0.4, 0.8)
col_stainless = (0.80, 0.82, 0.85)
col_black_steel = (0.1, 0.1, 0.1)
col_flange = (0.7, 0.7, 0.75)
col_glass = (0.6, 0.8, 0.9)
col_vessel_orange = (1.0, 0.5, 0.0)
col_pipe_yellow = (1.0, 0.8, 0.0) 
col_belt_green = (0.0, 0.4, 0.2)
col_frame_white = (0.9, 0.9, 0.9)
col_base_black = (0.1, 0.1, 0.1)
col_motor_silver = (0.7, 0.7, 0.75)
col_red = (0.85, 0.1, 0.15)
col_black = (0.1, 0.1, 0.1)
col_white = (0.9, 0.9, 0.9)
col_yellow = (1.0, 0.8, 0.0)
col_metal = (0.6, 0.6, 0.65)
col_frame_grey = (0.75, 0.75, 0.78)
col_cleat_blue = (0.0, 0.3, 0.8)
col_motor_box  = (0.35, 0.4, 0.45)
col_black      = (0.1, 0.1, 0.1)
col_gold       = (0.8, 0.6, 0.1) 
col_belt_green = (0.0, 0.6, 0.3)
col_grey_paint = (0.55, 0.6, 0.62)
col_dark_metal = (0.2, 0.2, 0.25)
col_handle_black = (0.1, 0.1, 0.1)
col_grey_body = (0.5, 0.55, 0.6)  # Main tank/pipes
col_blue_cyc = (0.1, 0.3, 0.8)    # The Cyclones
col_valve_wheel = (0.6, 0.2, 0.2) # Red Handwheels
col_dark_metal = (0.2, 0.2, 0.25) # Bolts/Flanges/Valve Body
col_grey_body = (0.75, 0.77, 0.80)  # Galvanized/Grey paint
col_dark_grey = (0.3, 0.3, 0.35)    # Frame/Legs
col_black = (0.1, 0.1, 0.1)         # Header pipe
col_valve = (0.4, 0.4, 0.45)        # Valves
col_casing = (0.85, 0.85, 0.9)   # Light Grey/White Housing
col_stiffener = (0.7, 0.7, 0.75) # Structural ribs
col_plates = (0.2, 0.8, 0.2)     # Bright Green (Internals)
col_internal_beam = (0.8, 0.2, 0.2) # Red (Internals)
col_structure = (0.6, 0.6, 0.65) # Legs/Brackets
col_sepro_blue = (0.05, 0.3, 0.6)
col_black = (0.1, 0.1, 0.1)
col_metal = (0.7, 0.7, 0.75)
col_dark_grey = (0.3, 0.3, 0.35)
col_frame_blue = (0.1, 0.2, 0.7)
col_belt_black = (0.1, 0.1, 0.1)
col_roller_red = (0.8, 0.2, 0.2)
col_guard_beige = (0.85, 0.82, 0.75)
col_metal = (0.7, 0.7, 0.75)
col_grey_paint = (0.55, 0.55, 0.60) # Machine Grey
col_rubber = (0.1, 0.1, 0.12)       # Black Rubber
col_steel = (0.80, 0.80, 0.82)      # Shiny Steel (Chute)
col_chrome = (0.9, 0.9, 0.95)       # Springs/Rods
col_brass = (0.8, 0.6, 0.2)         # Wingnuts (simulated)
mag_col_grey_paint = (0.55, 0.55, 0.60) # Machine Grey
mag_col_rubber = (0.1, 0.1, 0.12)       # Black Rubber
mag_col_steel = (0.80, 0.80, 0.82)      # Shiny Steel (Chute)
mag_col_chrome = (0.9, 0.9, 0.95)       # Springs/Rods
mag_col_brass = (0.8, 0.6, 0.2)         # Wingnuts (simulated)
mag_col_grey_paint = (0.55, 0.55, 0.60) # Machine Grey
mag_col_rubber = (0.1, 0.1, 0.12)       # Black Rubber
mag_col_steel = (0.80, 0.80, 0.82)      # Shiny Steel (Chute)
mag_col_chrome = (0.9, 0.9, 0.95)       # Springs/Rods
mag_col_brass = (0.8, 0.6, 0.2)         # Wingnuts (simulated)
ballmill_color_primary = (0.95, 0.65, 0.1)  # Industrial Gold
ballmill_color_foundation = (0.3, 0.35, 0.38) # Deep Slate Grey
ballmill_color_gears = (0.15, 0.15, 0.15)    # Charcoal
ballmill_color_components = (0.65, 0.65, 0.68) # Metallic Silver
trommel_col_green = (0.35, 0.75, 0.45)
trommel_col_mesh_red = (0.35, 0.15, 0.15)
trommel_col_tire_black = (0.1, 0.1, 0.1)
trommel_col_drive_shaft = (0.2, 0.2, 0.2)
trommel_col_motor_blue = (0.2, 0.2, 0.6)
dec_col_belt_blue = (0.0, 0.5, 0.8)     # Cleated blue belt
dec_col_frame_grey = (0.7, 0.7, 0.75)   # Galvanized steel
dec_col_roller_silver = (0.9, 0.9, 0.9) # Stainless rollers
dec_col_leg_dark = (0.2, 0.2, 0.25)     # Dark supports
centri_col_main_blue = (0.0, 0.45, 0.75) 
centri_col_hose_charcoal = (0.12, 0.12, 0.12)
centri_col_liner_maroon = (0.55, 0.15, 0.15)
centri_col_dark_steel = (0.22, 0.26, 0.32)
centri_col_bolt_silver = (0.72, 0.72, 0.76)



def ensure_document():
    """Ensures there is an active document to draw in."""
    doc = App.ActiveDocument
    if not doc:
        doc = App.newDocument("Processing_Plant")
    return doc

def get_global(x, y, z):
    """Helper to return a vector for positioning."""
    return App.Vector(x, y, z)

# --- HELPER FUNCTIONS ---

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


def make_sphere(doc, name, radius, x, y, z, color, offset=(0, 0, 0)):
    """Creates a sphere and positions it based on local coords and global offset."""
    shape = Part.makeSphere(radius)
    # Apply translation including the global offset
    shape.translate(App.Vector(x + offset[0], y + offset[1], z + offset[2]))
    
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = shape
    
    # VISUAL PROPERTIES
    obj.ViewObject.ShapeColor = color
    obj.ViewObject.DisplayMode = "Shaded"
    obj.ViewObject.LineWidth = 0.0          # Set to 0 to create a smooth, "glossy" look without mesh lines
    obj.ViewObject.PointColor = color
    obj.ViewObject.Lighting = "Two side"    # Enhances reflective look
    
    return obj


def make_robust_spring(doc, name, radius, height, coils, wire_rad, x, y, z, offset=(0,0,0)):
    # --- SCALE FACTOR ---
    scale_factor = 1.8
    
    # Scale inputs
    s_radius = radius * scale_factor
    s_height = height * scale_factor
    s_wire_rad = wire_rad * scale_factor
    s_x = x * scale_factor
    s_y = y * scale_factor
    s_z = z * scale_factor
    
    pitch = s_height / coils
    rings = []
    for i in range(coils):
        torus = Part.makeTorus(s_radius, s_wire_rad)
        z_shift = (i * pitch) + (pitch / 2)
        # Apply scaled local coordinates + global offset
        torus.translate(App.Vector(s_x + offset[0], s_y + offset[1], s_z + z_shift + offset[2]))
        rings.append(torus)
    spring_compound = Part.makeCompound(rings)
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = spring_compound
    obj.ViewObject.ShapeColor = col_spring_steel
    return obj


def make_trapezoid_hopper(doc, name, b_len, b_width, t_len, t_width, height, x, y, z, color, offset=(0,0,0)):
    # --- SCALE FACTOR ---
    scale_factor = 1.0
    
    # Apply scaling to dimensions
    s_b_len = b_len * scale_factor
    s_b_width = b_width * scale_factor
    s_t_len = t_len * scale_factor
    s_t_width = t_width * scale_factor
    s_height = height * scale_factor
    
    # Bottom Rectangle
    p1 = App.Vector(-s_b_len/2, -s_b_width/2, 0)
    p2 = App.Vector(s_b_len/2, -s_b_width/2, 0)
    p3 = App.Vector(s_b_len/2, s_b_width/2, 0)
    p4 = App.Vector(-s_b_len/2, s_b_width/2, 0)
    wire_bottom = Part.makePolygon([p1, p2, p3, p4, p1])
    
    # Top Rectangle
    p1t = App.Vector(-s_t_len/2, -s_t_width/2, s_height)
    p2t = App.Vector(s_t_len/2, -s_t_width/2, s_height)
    p3t = App.Vector(s_t_len/2, s_t_width/2, s_height)
    p4t = App.Vector(-s_t_len/2, s_t_width/2, s_height)
    wire_top = Part.makePolygon([p1t, p2t, p3t, p4t, p1t])
    
    # Loft
    shape = Part.makeLoft([wire_bottom, wire_top], True)
    
    # Translation (Scaling the target coordinates and the centering logic)
    # offset remains unscaled as it usually represents the global origin shift
    shape.translate(App.Vector(
        (x + b_len/2) * scale_factor + offset[0], 
        (y + b_width/2) * scale_factor + offset[1], 
        z * scale_factor + offset[2]
    ))
    
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = shape
    obj.ViewObject.ShapeColor = color
    return obj

def create_auger_segment(doc, name, dia, pitch, length, x, y, z, color, offset=(0,0,0)):
    # --- SCALE FACTOR ---
    scale_factor = 1.8
    
    # Scale dimensions
    s_radius = (dia / 2.0) * scale_factor
    s_pitch = pitch * scale_factor
    s_length = length * scale_factor
    
    # Create scaled helix
    helix = Part.makeHelix(s_pitch, s_length, s_radius)
    
    # Create scaled profile (The circle radius and its center vector must be scaled)
    profile_center = App.Vector(s_radius, 0, 0)
    profile = Part.makeCircle(s_radius, profile_center, App.Vector(0, 1, 0))
    
    # Build the solid
    auger_solid = Part.Wire(helix.Edges).makePipe(Part.Wire([profile]))
    
    # Rotation remains the same (90 degrees is constant regardless of scale)
    auger_solid.rotate(App.Vector(0,0,0), App.Vector(0,1,0), 90)
    
    # Scale the translation coordinates (x, y, z)
    # The offset is typically a global placement coordinate and is added after scaling
    tx = x * scale_factor + offset[0]
    ty = y * scale_factor + offset[1]
    tz = z * scale_factor + offset[2]
    
    auger_solid.translate(get_global(tx, ty, tz))
    
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = auger_solid
    obj.ViewObject.ShapeColor = color
    return obj


# --- EQUIPMENT BUILDERS ---
def create_equipment(doc, offset=(0,0,0)):
    # --- SCALE FACTOR ---
    scale_factor = 1.8

    # 1. MAIN BODY (TROUGH)
    make_box(doc, "Wall_Left", feeder_length * scale_factor, wall_thickness * scale_factor, feeder_height * scale_factor, 0, 0, 0, col_steel_grey, offset)
    make_box(doc, "Flange_L_Top", feeder_length * scale_factor, 100 * scale_factor, wall_thickness * scale_factor, 0, -80 * scale_factor, (feeder_height - 20) * scale_factor, col_steel_grey, offset)
    make_box(doc, "Flange_L_Bot", feeder_length * scale_factor, 100 * scale_factor, wall_thickness * scale_factor, 0, -80 * scale_factor, 0, col_steel_grey,  offset)
    
    make_box(doc, "Wall_Right", feeder_length * scale_factor, wall_thickness * scale_factor, feeder_height * scale_factor, 0, (feeder_width - 20) * scale_factor, 0, col_steel_grey, offset)
    make_box(doc, "Flange_R_Top", feeder_length * scale_factor, 100 * scale_factor, wall_thickness * scale_factor, 0, (feeder_width - 20) * scale_factor, (feeder_height - 20) * scale_factor, col_steel_grey, offset)
    make_box(doc, "Flange_R_Bot", feeder_length * scale_factor, 100 * scale_factor, wall_thickness * scale_factor, 0, (feeder_width - 20) * scale_factor, 0, col_steel_grey, offset)
    
    make_box(doc, "Wall_Back", wall_thickness * scale_factor, feeder_width * scale_factor, feeder_height * scale_factor, -20 * scale_factor, 0, 0, col_steel_grey, offset)
    make_box(doc, "Floor", (feeder_length - grizzly_length) * scale_factor, (feeder_width - 40) * scale_factor, wall_thickness * scale_factor, 0, 20 * scale_factor, 20 * scale_factor, col_steel_grey, offset)
    
    # Liners
    make_box(doc, "Liner_L", feeder_length * scale_factor, 10 * scale_factor, (feeder_height - 50) * scale_factor, 0, 20 * scale_factor, 30 * scale_factor, col_liner_red, offset)
    make_box(doc, "Liner_R", feeder_length * scale_factor, 10 * scale_factor, (feeder_height - 50) * scale_factor, 0, (feeder_width - 30) * scale_factor, 30 * scale_factor, col_liner_red, offset)
    make_box(doc, "Liner_Floor", (feeder_length - grizzly_length) * scale_factor, (feeder_width - 60) * scale_factor, 10 * scale_factor, 0, 30 * scale_factor, 40 * scale_factor, col_liner_red, offset)
    
    # 2. GRIZZLY BARS
    num_bars = 5
    bar_w = ((feeder_width - 40) / (num_bars * 1.5)) * scale_factor
    gap = bar_w * 0.5
    curr_y = (20 * scale_factor) + gap/2
    start_x = (feeder_length - grizzly_length) * scale_factor
    for i in range(num_bars + 1):
        make_box(doc, f"Bar_{i}", grizzly_length * scale_factor, bar_w, 40 * scale_factor, start_x, curr_y, 20 * scale_factor, col_steel_grey, offset)
        make_box(doc, f"BarCap_{i}", grizzly_length * scale_factor, bar_w, 10 * scale_factor, start_x, curr_y, 60 * scale_factor, col_liner_red, offset)
        curr_y += bar_w + gap

    # 3. SUSPENSION
    spring_h, spring_radius = 300, 60
    mounts = [
        (400, -150), 
        (400, feeder_width + 150), 
        (feeder_length - 400, -150), 
        (feeder_length - 400, feeder_width + 150)
    ]
    for i, (sx, sy) in enumerate(mounts):
        make_box(doc, f"SpringTop_{i}", 300 * scale_factor, 300 * scale_factor, 20 * scale_factor, (sx - 150) * scale_factor, (sy - 150) * scale_factor, 0, col_steel_grey, offset)
        make_robust_spring(doc, f"Spring_{i}", spring_radius, spring_h, 8, 12, sx, sy, -spring_h, offset)
        make_box(doc, f"SpringBot_{i}", 350 * scale_factor, 350 * scale_factor, 20 * scale_factor, (sx - 175) * scale_factor, (sy - 175) * scale_factor, (-spring_h - 20) * scale_factor, col_steel_grey, offset)
        
        gusset_y = 0 if sy < 0 else feeder_width
        gusset_off = -20 if sy < 0 else 0
        make_box(doc, f"Gusset_{i}", 200 * scale_factor, 150 * scale_factor, 200 * scale_factor, (sx - 100) * scale_factor, (gusset_y + gusset_off) * scale_factor, -200 * scale_factor, col_steel_grey, offset)

    # 4. DRIVE MECHANISM
    ex_x = 1200 * scale_factor
    make_box(doc, "ExciterBox", 800 * scale_factor, (feeder_width + 200) * scale_factor, 400 * scale_factor, ex_x, -100 * scale_factor, -400 * scale_factor, col_steel_grey, offset)
    make_box(doc, "MotorBase", 600 * scale_factor, 400 * scale_factor, 50 * scale_factor, ex_x, -700 * scale_factor, -950 * scale_factor, col_base_blue, offset)
    make_box(doc, "MotorPivot", 200 * scale_factor, 300 * scale_factor, 150 * scale_factor, ex_x + 200 * scale_factor, -650 * scale_factor, -900 * scale_factor, col_base_blue, offset)
    make_cylinder(doc, "Motor", 250 * scale_factor, 550 * scale_factor, ex_x + 300 * scale_factor, -500 * scale_factor, -500 * scale_factor, col_motor_teal, offset, App.Vector(0,1,0))
    make_cylinder(doc, "Pulley_Top", 120 * scale_factor, 60 * scale_factor, ex_x + 400 * scale_factor, -150 * scale_factor, -200 * scale_factor, col_liner_red, offset, App.Vector(0,1,0))
    make_cylinder(doc, "Pulley_Bot", 80 * scale_factor, 60 * scale_factor, ex_x + 300 * scale_factor, -500 * scale_factor, -500 * scale_factor, col_liner_red, offset, App.Vector(0,1,0))
    
    for k in range(3):
        belt_off = k * 20 * scale_factor
        # Angles remain unscaled
        make_box(doc, f"Belt_{k}", 15 * scale_factor, 15 * scale_factor, 680 * scale_factor, ex_x + 270 * scale_factor, (-180) * scale_factor + belt_off, -480 * scale_factor, col_black_rubber, offset, -25, App.Vector(0,1,0))


def build_conveyor(doc, offset=(0,0,0)):
    # --- SCALE FACTOR ---
    S = 1.5 
    
    # Scaled Global Dimensions
    s_conv_len = conv_length * S
    s_rail_thick = rail_thick * S
    s_rail_height = rail_height * S
    s_conv_width = conv_width * S
    s_conv_height = conv_height * S
    s_roller_dia = roller_dia * S
    s_roller_pitch = roller_pitch * S
    s_roller_width = roller_width * S

    # --- A. SIDE RAILS ---
    make_box(doc, "Rail_Left", s_conv_len, s_rail_thick, s_rail_height, 0, 0, s_conv_height - s_rail_height, col_frame_grey, offset)
    make_box(doc, "Rail_Right", s_conv_len, s_rail_thick, s_rail_height, 0, s_conv_width - s_rail_thick, s_conv_height - s_rail_height, col_frame_grey, offset)
    
    # Scaled Bolts
    num_bolts = int(s_conv_len / (300 * S))
    for i in range(num_bolts):
        bx = (150 * S) + (i * 300 * S)
        bz = s_conv_height - (s_rail_height / 2)
        make_cylinder(doc, f"Bolt_L_{i}", 8 * S, 5 * S, bx, -5 * S, bz, col_roller_silver, offset, App.Vector(0,1,0))
        make_cylinder(doc, f"Bolt_R_{i}", 8 * S, 5 * S, bx, s_conv_width, bz, col_roller_silver, offset, App.Vector(0,1,0))

    # --- B. ROLLERS ---
    num_rollers = int(s_conv_len / s_roller_pitch)
    rollers_shape_list = []
    current_x = (s_conv_len - ((num_rollers - 1) * s_roller_pitch)) / 2
    z_roller = s_conv_height - (s_roller_dia / 2) - (5 * S)
    
    for i in range(num_rollers):
        cyl = Part.makeCylinder(s_roller_dia / 2, s_roller_width)
        cyl.rotate(App.Vector(0,0,0), App.Vector(1,0,0), -90)
        # Translation positioning scaled
        y_pos = s_rail_thick + ((s_conv_width - 2 * s_rail_thick - s_roller_width) / 2)
        cyl.translate(App.Vector(current_x + offset[0], y_pos + offset[1], z_roller + offset[2]))
        rollers_shape_list.append(cyl)
        current_x += s_roller_pitch
        
    roller_compound = Part.makeCompound(rollers_shape_list)
    obj_r = doc.addObject("Part::Feature", "Rollers_Set")
    obj_r.Shape = roller_compound
    obj_r.ViewObject.ShapeColor = col_roller_silver

    # --- C. LEGS ---
    leg_positions = [200 * S, (s_conv_len / 2) - (50 * S), s_conv_len - (300 * S)]
    for i, lx in enumerate(leg_positions):
        # Vertical Struts
        make_box(doc, f"Leg_L_{i}", 80 * S, 80 * S, s_conv_height - s_rail_height, lx, 0, 0, col_frame_grey, offset)
        make_box(doc, f"Leg_R_{i}", 80 * S, 80 * S, s_conv_height - s_rail_height, lx, s_conv_width - (80 * S), 0, col_frame_grey, offset)
        # Cross Brace
        make_box(doc, f"Leg_Brace_{i}", 80 * S, s_conv_width, 60 * S, lx, 0, s_conv_height - s_rail_height - (200 * S), col_frame_grey, offset)
        
        # Adjustable Feet
        make_cylinder(doc, f"Foot_Pad_L_{i}", 40 * S, 20 * S, lx + (40 * S), 40 * S, 0, col_foot_black, offset)
        make_cylinder(doc, f"Foot_Thread_L_{i}", 10 * S, 100 * S, lx + (40 * S), 40 * S, 0, col_roller_silver, offset)
        make_cylinder(doc, f"Foot_Pad_R_{i}", 40 * S, 20 * S, lx + (40 * S), s_conv_width - (40 * S), 0, col_foot_black, offset)
        make_cylinder(doc, f"Foot_Thread_R_{i}", 10 * S, 100 * S, lx + (40 * S), s_conv_width - (40 * S), 0, col_roller_silver, offset)

    # --- D. CONTROL BOX ---
    box_x = (s_conv_len / 2) - (100 * S)
    box_y = -150 * S
    box_z = s_conv_height - (500 * S)
    box_w, box_h, box_d = 250 * S, 400 * S, 150 * S
    
    make_box(doc, "ControlBox_Main", box_w, box_d, box_h, box_x, box_y, box_z, col_box_dark, offset)
    make_box(doc, "Mounting_Plate", box_w + (40 * S), 20 * S, box_h, box_x - (20 * S), box_y + box_d, box_z, col_frame_grey, offset)
    
    # Interface Elements
    make_cylinder(doc, "Btn_Stop", 20 * S, 20 * S, box_x + box_w/2, box_y, box_z + (300 * S), col_button_red, offset, App.Vector(0,1,0))
    make_cylinder(doc, "Btn_Start", 15 * S, 15 * S, box_x + box_w/2, box_y, box_z + (240 * S), (0.2, 0.8, 0.2), offset, App.Vector(0,1,0))
    make_cylinder(doc, "Knob_Speed", 12 * S, 25 * S, box_x + box_w/2, box_y, box_z + (180 * S), col_roller_silver, offset, App.Vector(0,1,0))
    make_cylinder(doc, "Cable_Gland", 15 * S, 30 * S, box_x + (50 * S), box_y + box_d/2, box_z - (30 * S), (0.1, 0.1, 0.1), offset)


def build_shredder(doc, offset=(0,0,0)):
    # --- SCALE FACTOR ---
    S = 1.8
    
    # Scaled base variables
    beam_size = 200.0 * S
    s_frame_len = frame_len * S
    s_frame_width = frame_width * S
    s_frame_height = frame_height * S
    s_box_len = box_len * S
    s_box_width = box_width * S
    s_box_height = box_height * S

    # --- A. STRUCTURAL FRAME ---
    make_box(doc, "Beam_Bot_F", s_frame_len, beam_size, beam_size, 0, 0, 0, COL_FRAME_GREY, offset)
    make_box(doc, "Beam_Bot_B", s_frame_len, beam_size, beam_size, 0, s_frame_width - beam_size, 0, COL_FRAME_GREY, offset)
    make_box(doc, "Beam_Top_F", s_frame_len, beam_size, beam_size, 0, 0, s_frame_height, COL_FRAME_GREY, offset)
    make_box(doc, "Beam_Top_B", s_frame_len, beam_size, beam_size, 0, s_frame_width - beam_size, s_frame_height, COL_FRAME_GREY, offset)
    
    leg_coords = [0, (frame_len/2 - 100) * S, s_frame_len - beam_size]
    for i, lx in enumerate(leg_coords):
        make_box(doc, f"Leg_F_{i}", beam_size, beam_size, s_frame_height, lx, 0, 0, COL_FRAME_GREY, offset)
        make_box(doc, f"Leg_B_{i}", beam_size, beam_size, s_frame_height, lx, s_frame_width - beam_size, 0, COL_FRAME_GREY, offset)
        make_box(doc, f"Cross_Bot_{i}", beam_size, s_frame_width, beam_size/2, lx, 0, 50 * S, COL_FRAME_GREY, offset)
        make_box(doc, f"Cross_Top_{i}", beam_size, s_frame_width, beam_size, lx, 0, s_frame_height, COL_FRAME_GREY, offset)

    # --- B. SHREDDER BOX ---
    box_x = (s_frame_len - s_box_len) / 2
    box_y = (s_frame_width - s_box_width) / 2
    box_z = s_frame_height + beam_size
    make_box(doc, "ShredderBox", s_box_len, s_box_width, s_box_height, box_x, box_y, box_z, COL_BOX_GREEN, offset)
    
    rib_thick, rib_depth = 40 * S, 40 * S
    for i in range(4):
        rx = box_x + (i * (s_box_len/3))
        make_box(doc, f"Rib_V_{i}", rib_thick, s_box_width + 2*rib_depth, s_box_height, rx, box_y - rib_depth, box_z, COL_BOX_GREEN, offset)
    for i in range(3):
        rz = box_z + (i * (s_box_height/2))
        make_box(doc, f"Rib_H_{i}", s_box_len, s_box_width + 2*rib_depth, rib_thick, box_x, box_y - rib_depth, rz, COL_BOX_GREEN, offset)

    # Hopper
    make_trapezoid_hopper(doc, "Hopper", s_box_len, s_box_width, s_box_len + (500 * S), s_box_width + (500 * S), 800.0 * S, box_x, box_y, box_z + s_box_height, COL_HOPPER_BLUE, offset)

    # --- C. DRIVE TRAIN ---
    gb_x, gb_len = box_x + s_box_len + (50 * S), 800 * S
    make_box(doc, "Gearbox_Main", gb_len, s_box_width, 700 * S, gb_x, box_y, box_z, COL_HOPPER_BLUE, offset)
    make_cylinder(doc, "Bearing_R", 250 * S, 200 * S, gb_x, box_y + s_box_width/2, box_z + 300 * S, COL_HOPPER_BLUE, offset, App.Vector(1,0,0))
    make_box(doc, "Guard_R", 100 * S, s_box_width, 800 * S, gb_x + gb_len, box_y, box_z, COL_MOTOR_GREY, offset)
    
    br_x = box_x - (500 * S)
    make_box(doc, "BearingBox_L", 450 * S, s_box_width, 600 * S, br_x, box_y, box_z, COL_HOPPER_BLUE, offset)
    make_cylinder(doc, "Shaft_L", 100 * S, 100 * S, box_x - (100 * S), box_y + s_box_width/2, box_z + 300 * S, COL_SHAFT_RED, offset, App.Vector(1,0,0))

    motor_rad, motor_len, motor_x, motor_z = 250 * S, 600 * S, box_x - (200 * S), 300 * S
    # Motors & Bases
    make_cylinder(doc, "Motor_L", motor_rad, motor_len, motor_x, s_frame_width/2, motor_z, COL_MOTOR_GREY, offset, App.Vector(1,0,0))
    make_box(doc, "MotorBase_L", motor_len, 500 * S, 50 * S, motor_x, (s_frame_width/2)-(250 * S), motor_z - motor_rad, COL_FRAME_GREY, offset)
    
    motor_x_r = gb_x + (100 * S)
    make_cylinder(doc, "Motor_R", motor_rad, motor_len, motor_x_r, s_frame_width/2, motor_z, COL_MOTOR_GREY, offset, App.Vector(1,0,0))
    make_box(doc, "MotorBase_R", motor_len, 500 * S, 50 * S, motor_x_r, (s_frame_width/2)-(250 * S), motor_z - motor_rad, COL_FRAME_GREY, offset)
    
    make_box(doc, "BeltCover_L", 150 * S, 400 * S, s_frame_height, motor_x, (s_frame_width/2)-(200 * S), motor_z, COL_FRAME_GREY, offset)
    make_box(doc, "BeltCover_R", 150 * S, 400 * S, s_frame_height, motor_x_r, (s_frame_width/2)-(200 * S), motor_z, COL_FRAME_GREY, offset)


def build_reactor(doc, offset=(0,0,0)):
    # --- SCALING FACTOR ---
    scale_factor = 1.6
    
    # Local variable for radius to avoid global overlap
    radius = (pyro_dia / 2.0) * scale_factor
    # Calculate key heights
    dish_h = radius * pyro_dish_ratio
    z_cyl_start = dish_h 
    z_cyl_end = z_cyl_start + (pyro_cyl_height * scale_factor)
    
    # --- A. MAIN VESSEL BODY (ORANGE) ---
    
    # 1. Cylinder (Using new syntax + Orange)
    make_cylinder(doc, "TankCylinder", radius, pyro_cyl_height * scale_factor, 0, 0, z_cyl_start, col_vessel_orange, offset)
    
    # 2. Bottom Dished Head (Ellipsoidal)
    sphere_bot = Part.makeSphere(radius)
    mat_bot = App.Matrix()
    mat_bot.scale(1.0, 1.0, pyro_dish_ratio)
    sphere_bot.transformShape(mat_bot)
    # Manual Translation required for sphere
    sphere_bot.translate(App.Vector(offset[0], offset[1], z_cyl_start + offset[2]))
    
    obj_bot = doc.addObject("Part::Feature", "TankHead_Bottom")
    obj_bot.Shape = sphere_bot
    obj_bot.ViewObject.ShapeColor = col_vessel_orange # ORANGE
    
    # 3. Top Dished Head
    sphere_top = Part.makeSphere(radius)
    mat_top = App.Matrix()
    mat_top.scale(1.0, 1.0, pyro_dish_ratio)
    sphere_top.transformShape(mat_top)
    sphere_top.translate(App.Vector(offset[0], offset[1], z_cyl_end + offset[2]))
    
    obj_top = doc.addObject("Part::Feature", "TankHead_Top")
    obj_top.Shape = sphere_top
    obj_top.ViewObject.ShapeColor = col_vessel_orange # ORANGE
    obj_top.ViewObject.Transparency = 10 

    # --- B. SIGHT GLASS ---
    sg_w = 150.0 * scale_factor
    sg_h = 1000.0 * scale_factor
    sg_d = 50.0 * scale_factor
    sg_y_pos = radius - (20 * scale_factor)
    sg_z_pos = z_cyl_start + ((pyro_cyl_height * scale_factor) - sg_h)/2
    
    # Frame (Stainless)
    make_box(doc, "SightGlassFrame", sg_w, sg_d, sg_h, 
             -sg_w/2, sg_y_pos, sg_z_pos, col_stainless, offset)
             
    # Glass (Blue/Glass color)
    glass_obj = make_box(doc, "SightGlassWindow", sg_w - (40 * scale_factor), sg_d + (10 * scale_factor), sg_h - (40 * scale_factor), 
                         -(sg_w-(40 * scale_factor))/2, sg_y_pos + (10 * scale_factor), sg_z_pos + (20 * scale_factor), col_glass, offset)
    glass_obj.ViewObject.Transparency = 50

    # --- C. SUPPORT LUGS ---
    lug_w = 150.0 * scale_factor
    lug_h = 200.0 * scale_factor
    lug_ext = 150.0 * scale_factor
    lug_z = z_cyl_start + (400.0 * scale_factor)
    
    angles = [45, 135, 225, 315]
    
    for i, ang in enumerate(angles):
        rad_ang = math.radians(ang)
        
        # Calculate rotated coordinates
        base_r = radius - (5 * scale_factor)
        base_tangent = -10 * scale_factor
        
        lx = (base_r * math.cos(rad_ang)) - (base_tangent * math.sin(rad_ang))
        ly = (base_r * math.sin(rad_ang)) + (base_tangent * math.cos(rad_ang))
        
        # Main Lug Body (Keeping Stainless)
        make_box(doc, f"Lug_Body_{i}", lug_ext, 20 * scale_factor, lug_h, 
                 lx, ly, lug_z, col_stainless, 
                 offset=offset, rotation_angle=ang, rotation_axis=App.Vector(0,0,1))
                 
        # Lug Cap
        cx = ((base_r - (10 * scale_factor)) * math.cos(rad_ang)) - ((base_tangent - (40 * scale_factor)) * math.sin(rad_ang))
        cy = ((base_r - (10 * scale_factor)) * math.sin(rad_ang)) + ((base_tangent - (40 * scale_factor)) * math.cos(rad_ang))
        
        make_box(doc, f"Lug_Cap_{i}", lug_ext + (20 * scale_factor), 100 * scale_factor, 20 * scale_factor, 
                 cx, cy, lug_z + lug_h, col_stainless, 
                 offset=offset, rotation_angle=ang, rotation_axis=App.Vector(0,0,1))

    # --- D. MANWAY (Assembly of parts) ---
    manway_r = 250.0 * scale_factor
    manway_h = 150.0 * scale_factor
    manway_offset = radius * 0.5
    mw_angle = 45
    mw_rad = math.radians(mw_angle)
    
    mx = manway_offset * math.cos(mw_rad)
    my = manway_offset * math.sin(mw_rad)
    
    # Neck (Stainless)
    make_cylinder(doc, "MW_Neck", manway_r, manway_h, 
                  mx, my, z_cyl_end + (dish_h * 0.7), col_stainless, 
                  offset=offset, axis=App.Vector(0,0,1))
    
    # Flange
    make_cylinder(doc, "MW_Flange", manway_r + (50 * scale_factor), 20 * scale_factor, 
                  mx, my, z_cyl_end + (dish_h * 0.7) + manway_h, col_stainless, 
                  offset=offset, axis=App.Vector(0,0,1))
    
    # Lid
    make_cylinder(doc, "MW_Lid", manway_r + (50 * scale_factor), 30 * scale_factor, 
                  mx, my, z_cyl_end + (dish_h * 0.7) + manway_h + (20 * scale_factor), col_stainless, 
                  offset=offset, axis=App.Vector(0,0,1))

    # Hinge Box
    hx_local = manway_offset + manway_r
    hy_local = -25 * scale_factor
    
    hx_rot = (hx_local * math.cos(mw_rad)) - (hy_local * math.sin(mw_rad))
    hy_rot = (hx_local * math.sin(mw_rad)) + (hy_local * math.cos(mw_rad))
    
    make_box(doc, "MW_Hinge", 100 * scale_factor, 50 * scale_factor, 50 * scale_factor, 
             hx_rot, hy_rot, z_cyl_end + (dish_h * 0.7) + manway_h, col_stainless,
             offset=offset, rotation_angle=mw_angle)

    # --- E. AGITATOR DRIVE ---
    top_z = z_cyl_end + dish_h
    
    # Lantern & Gearbox (Stainless)
    make_cylinder(doc, "AgitatorLantern", 150 * scale_factor, 300 * scale_factor, 
                  0, 0, top_z, col_stainless, offset=offset)
    
    make_box(doc, "Gearbox", 400 * scale_factor, 400 * scale_factor, 200 * scale_factor, 
             -200 * scale_factor, -200 * scale_factor, top_z + (300 * scale_factor), col_stainless, offset=offset)
    
    # Motor (TEAL - Retained)
    motor_r = 140 * scale_factor
    motor_h = 500 * scale_factor
    make_cylinder(doc, "AgitatorMotor", motor_r, motor_h, 
                  0, 0, top_z + (500 * scale_factor), col_motor_teal, offset=offset)



def build_tank(doc, offset=(0,0,0)):
    # Local variables for tank size to prevent global confusion
    radius = tank_dia / 2.0
    axis_h = leg_height + radius
    
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


def build_connecting_pipe(doc, start_offset, end_offset):
    # Pyrolysis top point (approx): (18500, 300, 2160) [Based on pyro height + dish]
    pyro_r = pyro_dia / 2.0
    pyro_h = pyro_cyl_height + (pyro_r * pyro_dish_ratio)
    p_start = App.Vector(start_offset[0], start_offset[1], start_offset[2] + pyro_h)
    
    # Tank top nozzle point (approx): (20500 + 1000, 4000, leg_height + tank_r + tank_r*0.9 + 250)
    # The first nozzle is at x=1000 relative to tank center
    tank_r = tank_dia / 2.0
    tank_axis_h = leg_height + tank_r
    tank_noz_h = tank_axis_h + (tank_r * 0.9) + 250
    p_end = App.Vector(end_offset[0] + 1000, end_offset[1], end_offset[2] + tank_noz_h)
    
    # 1. Vertical Riser from Pyro
    riser_h = 500
    make_cylinder(doc, "Pipe_Riser", 60, riser_h, p_start.x, p_start.y, p_start.z, col_pipe_yellow)
    
    # 2. Horizontal Run (X-direction)
    p_corner1 = App.Vector(p_start.x, p_start.y, p_start.z + riser_h)
    x_dist = p_end.x - p_corner1.x
    make_cylinder(doc, "Pipe_Horiz_X", 60, x_dist, p_corner1.x, p_corner1.y, p_corner1.z, col_pipe_yellow, axis=App.Vector(1,0,0))
    
    # 3. Horizontal Run (Y-direction)
    p_corner2 = App.Vector(p_end.x, p_corner1.y, p_corner1.z)
    y_dist = p_end.y - p_corner2.y
    make_cylinder(doc, "Pipe_Horiz_Y", 60, y_dist, p_corner2.x, p_corner2.y, p_corner2.z, col_pipe_yellow, axis=App.Vector(0,1,0))
    
    # 4. Vertical Drop to Tank
    p_corner3 = App.Vector(p_end.x, p_end.y, p_corner2.z)
    drop_h = p_corner3.z - p_end.z
    make_cylinder(doc, "Pipe_Drop", 60, drop_h, p_end.x, p_end.y, p_end.z, col_pipe_yellow)
    
    # Elbows (Optional visual polish)
    # Elbow 1 (Top of riser)
    e1 = Part.makeTorus(60, 20) # Simplified elbow
    e1.translate(p_corner1)
    obj_e1 = doc.addObject("Part::Feature", "Elbow1")
    obj_e1.Shape = e1
    obj_e1.ViewObject.ShapeColor = col_pipe_yellow
    
    # Elbow 2 (Turn to Y)
    e2 = Part.makeTorus(60, 20)
    e2.translate(p_corner2)
    obj_e2 = doc.addObject("Part::Feature", "Elbow2")
    obj_e2.Shape = e2
    obj_e2.ViewObject.ShapeColor = col_pipe_yellow

    # Elbow 3 (Turn Down)
    e3 = Part.makeTorus(60, 20)
    e3.translate(p_corner3)
    obj_e3 = doc.addObject("Part::Feature", "Elbow3")
    obj_e3.Shape = e3
    obj_e3.ViewObject.ShapeColor = col_pipe_yellow



def pneumatic_conveyor(doc, offset=(0,0,0)):
    """
    Builds the conveyor assembly at a specific offset coordinate.
    """
    rad = math.radians(incline_angle)
    pivot_x = horiz_len
    pivot_z = 0
    
    # --- A. CONVEYOR BODY (WHITE FRAME) ---
    make_box(doc, "Frame_Horiz_L", horiz_len, 20, frame_height, 
             0, 0, 0, col_frame_white, offset)
             
    make_box(doc, "Frame_Horiz_R", horiz_len, 20, frame_height, 
             0, belt_width-20, 0, col_frame_white, offset)
             
    make_box(doc, "Frame_Incline_L", incline_len, 20, frame_height, 
             pivot_x, 0, pivot_z, col_frame_white, offset, 
             rotation_angle=-incline_angle, rotation_axis=App.Vector(0,1,0))

    make_box(doc, "Frame_Incline_R", incline_len, 20, frame_height, 
             pivot_x, belt_width-20, pivot_z, col_frame_white, offset, 
             rotation_angle=-incline_angle, rotation_axis=App.Vector(0,1,0))

    # --- B. THE BELT (GREEN) ---
    make_box(doc, "Belt_Horiz", horiz_len, belt_width-40, 10, 
             0, 20, frame_height-50, col_belt_green, offset)
             
    make_box(doc, "Belt_Incline", incline_len, belt_width-40, 10, 
             pivot_x, 20, pivot_z + frame_height - 50, col_belt_green, offset,
             rotation_angle=-incline_angle, rotation_axis=App.Vector(0,1,0))

    # Cleats
    num_cleats = 15
    cleat_spacing = incline_len / num_cleats
    for i in range(num_cleats):
        cx_dist = i * cleat_spacing
        dx = cx_dist * math.cos(rad)
        dz = cx_dist * math.sin(rad)
        
        final_x = pivot_x + dx
        final_z = pivot_z + frame_height - 40 + dz
        
        make_box(doc, f"Cleat_{i}", 20, belt_width-40, 30, 
                 final_x, 20, final_z, col_belt_green, offset,
                 rotation_angle=-incline_angle, rotation_axis=App.Vector(0,1,0))

    # --- C. MOBILE BASE (BLACK) ---
    base_len = 2500.0
    base_w = belt_width + 200
    base_h = 100.0
    
    make_box(doc, "Base_L", base_len, 100, base_h, 
             500, -100, -400, col_base_black, offset)
             
    make_box(doc, "Base_R", base_len, 100, base_h, 
             500, belt_width, -400, col_base_black, offset)
             
    make_box(doc, "Base_Cross_F", 100, base_w, base_h, 
             500, -100, -400, col_base_black, offset)
             
    make_box(doc, "Base_Cross_B", 100, base_w, base_h, 
             500 + base_len - 100, -100, -400, col_base_black, offset)

    # Wheels
    wheel_positions = [550, 500 + base_len - 50]
    for i, wx in enumerate(wheel_positions):
        make_cylinder(doc, f"Wheel_L_{i}", 60, 50, 
                      wx, -50, -460, (0.3,0.3,0.3), offset, axis=App.Vector(0,1,0))
                      
        make_cylinder(doc, f"Wheel_R_{i}", 60, 50, 
                      wx, belt_width+50, -460, (0.3,0.3,0.3), offset, axis=App.Vector(0,1,0))

    # --- D. LIFTING MECHANISM ---
    make_box(doc, "Pivot_Support", 100, base_w-200, 300, 
             600, 0, -300, col_base_black, offset)
             
    arm_len = 2000
    make_box(doc, "LiftArm", 100, 100, arm_len, 
             2000, belt_width/2 - 50, -400, col_base_black, offset,
             rotation_angle=-45, rotation_axis=App.Vector(0,1,0))

    # --- E. GUARD RAILS ---
    num_posts = 6
    post_spacing = incline_len / num_posts
    for side in [0, 1]: 
        y_pos = -10 if side == 0 else belt_width + 10
        # Posts
        for i in range(num_posts):
            dist = i * post_spacing
            px = pivot_x + (dist * math.cos(rad))
            pz = pivot_z + (dist * math.sin(rad))
            
            make_cylinder(doc, f"Post_{side}_{i}", 10, rail_height, 
                          px, y_pos, pz + frame_height, col_base_black, offset)

        # Top Rail (Manual shape creation required for non-standard axis rotation)
        shape_rail = Part.makeCylinder(10, incline_len)
        # Rotate to align with incline
        shape_rail.rotate(App.Vector(0,0,0), App.Vector(0,1,0), 90 + incline_angle)
        # Translate to position
        rail_start_z = pivot_z + frame_height + rail_height
        shape_rail.translate(App.Vector(pivot_x + offset[0], y_pos + offset[1], rail_start_z + offset[2]))
        
        obj_rail = doc.addObject("Part::Feature", f"HandRail_{side}")
        obj_rail.Shape = shape_rail
        obj_rail.ViewObject.ShapeColor = col_base_black

    # --- F. MOTORS ---
    motor_x = pivot_x + 200
    motor_z = pivot_z + 100
    
    make_cylinder(doc, "Motor_Main", 120, 350, 
                  motor_x, -350, motor_z, col_motor_silver, offset, axis=App.Vector(0,1,0))
                  
    make_box(doc, "Gearbox", 200, 150, 200, 
             motor_x - 100, -150, motor_z - 100, (0.5, 0.5, 0.5), offset)
             
    make_cylinder(doc, "Motor_Sec", 100, 300, 
                  pivot_x + 1500, -300, pivot_z + 600, col_motor_silver, offset, axis=App.Vector(0,1,0))

    # --- G. DISCHARGE HOOD ---
    top_x = pivot_x + (incline_len * math.cos(rad))
    top_z = pivot_z + (incline_len * math.sin(rad))
    
    hood_obj = make_box(doc, "DischargeHood", 400, belt_width, 300, 
             top_x - 200, 0, top_z + frame_height, (0.8, 0.8, 0.8), offset,
             rotation_angle=-incline_angle, rotation_axis=App.Vector(0,1,0))
    hood_obj.ViewObject.Transparency = 50



def build_crusher(doc, offset=(0,0,0)):
    """
    Builds the Crusher Machine at a specified offset coordinate.
    """
    
    # --- A. CRAWLER TRACKS ---
    track_spacing = chassis_w - track_w
    for side in [-1, 1]:
        y_pos = (track_spacing/2 * side) - (track_w/2)
        if side == 1: y_pos = (track_spacing/2)
        
        # Main Track
        make_box(doc, f"Track_Body_{side}", track_len - track_h, track_w, track_h, 
                 -track_len/2 + track_h/2, y_pos, 0, col_black, offset)
        
        # Ends
        make_cylinder(doc, f"Track_Wheel_F_{side}", track_h/2, track_w, 
                      track_len/2 - track_h/2, y_pos, track_h/2, col_black, offset, axis=App.Vector(0,1,0))
                      
        make_cylinder(doc, f"Track_Wheel_R_{side}", track_h/2, track_w, 
                      -track_len/2 + track_h/2, y_pos, track_h/2, col_black, offset, axis=App.Vector(0,1,0))

    # --- B. CHASSIS FRAME ---
    make_box(doc, "Chassis_Main", track_len - 500, chassis_w - 200, 300, 
             -(track_len-500)/2, -(chassis_w-200)/2, track_h - 100, col_black, offset)

    # --- C. MAIN BODY ---
    deck_height = track_h + 300
    body_len = 4500
    
    # Lower Body
    make_box(doc, "Body_Lower", body_len, chassis_w, 1000, 
             -2000, -chassis_w/2, deck_height, col_red, offset)
             
    # Engine Block
    eng_len = 1500
    eng_h = 1400
    eng_w = chassis_w - 400
    eng_x = 0
    make_box(doc, "Engine_Block", eng_len, eng_w, eng_h, 
             eng_x, -eng_w/2, deck_height + 1000, col_red, offset)
             
    # Vents
    make_box(doc, "Vent_Panel", 800, 20, 1000, 
             eng_x + 200, -eng_w/2 - 20, deck_height + 1200, col_white, offset)
             
    for i in range(5):
        make_box(doc, f"Vent_{i}", 600, 25, 50, 
                 eng_x + 300, -eng_w/2 - 22, deck_height + 1300 + (i*150), col_black, offset)

    # --- Crusher Housing ---
    crusher_x = -1500
    make_box(doc, "Crusher_Housing", 1200, 1500, 1200, 
             crusher_x, -750, deck_height + 1000, col_red, offset)
             
    # Chamfer Top (Box rotated 30 deg around Y)
    make_box(doc, "Crusher_Top_Angle", 800, 1500, 500, 
             crusher_x + 200, -750, deck_height + 2200, col_red, offset,
             rotation_angle=-30, rotation_axis=App.Vector(0,1,0))
             
    # Branding Panel
    make_box(doc, "Brand_Panel", 800, 20, 400, 
             crusher_x + 200, -750 - 20, deck_height + 1200, col_white, offset)

    # --- D. FEED HOPPER ---
    hopper_x = -3500
    hopper_z = deck_height + 1800
    
    # Left Wall
    make_box(doc, "Hopper_Wall_L", 1500, 20, 800, 
             hopper_x, chassis_w/2, hopper_z, col_black, offset,
             rotation_angle=-30, rotation_axis=App.Vector(1,0,0))
             
    # Right Wall
    make_box(doc, "Hopper_Wall_R", 1500, 20, 800, 
             hopper_x, -chassis_w/2, hopper_z, col_black, offset,
             rotation_angle=30, rotation_axis=App.Vector(1,0,0))
             
    # Back Wall
    make_box(doc, "Hopper_Wall_B", 20, chassis_w + 400, 800, 
             hopper_x, -(chassis_w+400)/2, hopper_z, col_black, offset,
             rotation_angle=-20, rotation_axis=App.Vector(0,1,0))

    # --- E. MAIN CONVEYOR ---
    conv_len = 5000
    conv_w = 1000
    conv_angle = 25
    pivot_x = 1500
    pivot_z = deck_height
    rad = math.radians(conv_angle)
    
    # Frame
    make_box(doc, "MainConveyor_Frame", conv_len, conv_w, 300, 
             pivot_x, -conv_w/2, pivot_z, col_red, offset,
             rotation_angle=-conv_angle, rotation_axis=App.Vector(0,1,0))
             
    # Belt
    make_box(doc, "MainConveyor_Belt", conv_len + 200, conv_w - 100, 50, 
             pivot_x - 100, -(conv_w-100)/2, pivot_z + 200, col_black, offset,
             rotation_angle=-conv_angle, rotation_axis=App.Vector(0,1,0))
             
    # Hood
    tip_x = pivot_x + (conv_len * math.cos(rad))
    tip_z = pivot_z + (conv_len * math.sin(rad))
    
    make_box(doc, "Discharge_Hood", 600, conv_w + 50, 500, 
             tip_x - 400, -(conv_w+50)/2, tip_z + 200, col_black, offset,
             rotation_angle=-conv_angle, rotation_axis=App.Vector(0,1,0))

    # --- F. SIDE CONVEYOR ---
    # Manually created to handle compound rotation (Y then Z axis)
    side_shape = Part.makeBox(3000, 600, 200)
    side_shape.rotate(App.Vector(0,0,0), App.Vector(0,1,0), -25)
    side_shape.rotate(App.Vector(0,0,0), App.Vector(0,0,1), 90)
    
    # Apply manual translation using offset
    side_shape.translate(App.Vector(-500 + offset[0], chassis_w/2 + offset[1], deck_height - 200 + offset[2]))
    
    obj_sc = doc.addObject("Part::Feature", "SideConveyor")
    obj_sc.Shape = side_shape
    obj_sc.ViewObject.ShapeColor = col_black

    # --- G. LADDER & DETAILS ---
    lad_x = -500
    lad_y = -chassis_w/2 - 10
    lad_w = 400
    lad_h = 1200
    lad_base = 200
    
    # Rails
    make_box(doc, "Ladder_Rail_L", 50, 50, lad_h, 
             lad_x, lad_y, lad_base, col_yellow, offset,
             rotation_angle=-15, rotation_axis=App.Vector(0,1,0))
             
    make_box(doc, "Ladder_Rail_R", 50, 50, lad_h, 
             lad_x + lad_w, lad_y, lad_base, col_yellow, offset,
             rotation_angle=-15, rotation_axis=App.Vector(0,1,0))
             
    # Steps
    for i in range(5):
        step_z = lad_base + 200 + (i * 200)
        shift_x = (i * 200) * math.tan(math.radians(15))
        
        make_box(doc, f"Step_{i}", lad_w, 40, 20, 
                 lad_x + 25 + shift_x, lad_y + 5, step_z, col_yellow, offset)
                 
    # Control Panel
    panel_x = 500
    make_box(doc, "ControlPanel", 400, 200, 500, 
             panel_x, -chassis_w/2 - 50, deck_height, (0.2, 0.2, 0.3), offset)
             
    for r in range(3):
        for c in range(3):
            make_cylinder(doc, f"Btn_{r}_{c}", 15, 10, 
                          panel_x + 50 + (c*50), -chassis_w/2 - 55, deck_height + 350 - (r*50), 
                          (0.0, 1.0, 0.0), offset, axis=App.Vector(0,1,0))



def pocket_conveyor(doc, offset=(0,0,0)):
    """
    Draws a cleated/pocket conveyor based on the reference image.
    Offset allows placement at specific global coordinates.
    """
    
    # --- Parameters ---
    conv_len = 6000.0
    conv_width = 1000.0
    rail_h = 140.0
    rail_thick = 5.0
    belt_level = 90.0  # Height of belt surface from bottom of rail
    
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


def make_hopper_loft(doc, name, top_w, top_l, bot_r, height, x, y, z, color, offset=(0,0,0)):
    # Top Rectangle
    p1 = App.Vector(-top_l/2, -top_w/2, height)
    p2 = App.Vector(top_l/2, -top_w/2, height)
    p3 = App.Vector(top_l/2, top_w/2, height)
    p4 = App.Vector(-top_l/2, top_w/2, height)
    wire_top = Part.makePolygon([p1, p2, p3, p4, p1])
    
    # Bottom Circle
    circle = Part.makeCircle(bot_r, App.Vector(0,0,0), App.Vector(0,0,1))
    wire_bot = Part.Wire(circle)
    
    # Loft
    loft = Part.makeLoft([wire_bot, wire_top], True)
    
    # Apply translation with offset
    loft.translate(App.Vector(x + offset[0], y + offset[1], z + offset[2]))
    
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = loft
    obj.ViewObject.ShapeColor = color
    return obj

def make_housing_profile(doc, name, length, w_bottom, w_top, h, x, y, z, color, offset=(0,0,0)):
    # Profile on YZ plane extruded along X
    y_bot = w_bottom / 2
    y_top = w_top / 2
    pts = [
        App.Vector(0, -y_bot, 0),
        App.Vector(0, y_bot, 0),
        App.Vector(0, y_top, h),
        App.Vector(0, -y_top, h),
        App.Vector(0, -y_bot, 0)
    ]
    poly = Part.makePolygon(pts)
    face = Part.Face(poly)
    prism = face.extrude(App.Vector(length, 0, 0))
    
    # Apply translation with offset
    # Note: original logic used x - length/2 as start point for extrusion
    prism.translate(App.Vector((x - length/2) + offset[0], y + offset[1], z + offset[2]))
    
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = prism
    obj.ViewObject.ShapeColor = color
    return obj

# ==========================================
# 4. MAIN BUILD ROUTINE
# ==========================================

def build_cleaner(doc, offset=(0,0,0)):
    """
    Builds the Grain Cleaner at the specified offset coordinates.
    """
    base_z = leg_height
    
    # --- A. STRUCTURAL FRAME ---
    # Beams
    make_box(doc, "Beam_L", total_length, frame_beam_size, frame_beam_size, 
             total_length/2 - section_len/2, -total_width/2, base_z, col_grey_paint, offset)
             
    make_box(doc, "Beam_R", total_length, frame_beam_size, frame_beam_size, 
             total_length/2 - section_len/2, total_width/2 - frame_beam_size, base_z, col_grey_paint, offset)
    
    # Legs
    for i in range(hopper_count + 1):
        x_pos = (i * section_len)
        make_box(doc, f"Leg_L_{i}", frame_beam_size, frame_beam_size, leg_height, 
                 x_pos, -total_width/2, 0, col_grey_paint, offset)
                 
        make_box(doc, f"Leg_R_{i}", frame_beam_size, frame_beam_size, leg_height, 
                 x_pos, total_width/2 - frame_beam_size, 0, col_grey_paint, offset)
        
        # Bracing (using make_box rotation logic)
        if i < hopper_count:
            brace_len = math.sqrt(section_len**2 + leg_height**2)
            angle = math.degrees(math.atan2(leg_height, section_len))
            
            # Note: Rotation in original was around (0,0,0) then translated. 
            # make_box rotates around (0,0,0) then translates. This logic holds.
            make_box(doc, f"Brace_{i}", brace_len, 10, 50, 
                     x_pos, -total_width/2 + frame_beam_size, 0, col_grey_paint, offset,
                     rotation_angle=-angle, rotation_axis=App.Vector(0,1,0))

    # --- B. HOPPERS ---
    hopper_h = 600.0
    outlet_r = 100.0
    for i in range(hopper_count):
        center_x = (i * section_len) + (section_len/2)
        h_len = section_len - 20
        h_wid = total_width - 20
        
        make_hopper_loft(doc, f"Hopper_{i}", h_wid, h_len, outlet_r, hopper_h, 
                         center_x, 0, base_z - hopper_h, col_grey_paint, offset)
                         
        make_cylinder(doc, f"Outlet_{i}", outlet_r, 100, 
                      center_x, 0, base_z - hopper_h - 100, col_grey_paint, offset)

    # --- C. UPPER HOUSING ---
    for i in range(hopper_count):
        center_x = (i * section_len) + (section_len/2)
        housing_len = section_len - 10
        
        make_housing_profile(doc, f"Housing_{i}", housing_len, total_width, top_flat_width, housing_height, 
                             center_x, 0, base_z + frame_beam_size, col_grey_paint, offset)
        
        # Inspection Door
        door_x = center_x - (housing_len-50)/2
        door_y = -(top_flat_width-50)/2
        door_z = base_z + frame_beam_size + housing_height
        
        make_box(doc, f"Door_{i}", housing_len - 50, top_flat_width - 50, 20, 
                 door_x, door_y, door_z, (0.6, 0.65, 0.67), offset)
        
        # Handles
        for h_side in [-1, 1]:
            h_y = h_side * (top_flat_width/2 - 10)
            make_box(doc, f"Latch_{i}_{h_side}", 50, 20, 30, 
                     center_x, h_y - 10, base_z + frame_beam_size + housing_height, col_handle_black, offset)

    # --- D. DISCHARGE CHUTE ---
    end_x = total_length
    # Box rotated around Y axis
    make_box(doc, "DischargeSpout", 600, 400, 400, 
             end_x, 0, base_z + 200, col_grey_paint, offset,
             rotation_angle=30, rotation_axis=App.Vector(0,1,0))
    
    # --- E. DRIVE MECHANISM ---
    make_box(doc, "BearingBlock", 150, 400, 150, 
             end_x, -200, base_z + housing_height/2, col_grey_paint, offset)
             
    # Drive Shaft (aligned X axis)
    # Helper expects axis=(1,0,0) for X alignment
    make_cylinder(doc, "DriveShaft", 40, 200, 
                  end_x, 0, base_z + housing_height/2 + 75, col_dark_metal, offset, axis=App.Vector(1,0,0))



def make_u_bend(doc, name, pipe_r, bend_r, x, y, z, rotation_z, color, offset=(0,0,0)):
    # Create a 180 degree torus segment
    # Major radius = bend_r, Minor radius = pipe_r
    # Angles: 0 to 180
    torus = Part.makeTorus(bend_r, pipe_r, App.Vector(0,0,0), App.Vector(0,0,1), 0, 180)
    
    # Orient vertically (arching over)
    torus.rotate(App.Vector(0,0,0), App.Vector(1,0,0), 90)
    
    # Rotate to face center
    torus.rotate(App.Vector(0,0,0), App.Vector(0,0,1), rotation_z)
    
    # Translate to position + Offset
    torus.translate(App.Vector(x + offset[0], y + offset[1], z + offset[2]))
    
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = torus
    obj.ViewObject.ShapeColor = color
    return obj

# Custom helper for Cone (as it's not in the standard requested list but needed for Cyclones)
def make_cone(doc, name, r1, r2, height, x, y, z, color, offset=(0,0,0)):
    shape = Part.makeCone(r1, r2, height)
    shape.translate(App.Vector(x + offset[0], y + offset[1], z + offset[2]))
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = shape
    obj.ViewObject.ShapeColor = color
    return obj

# ==========================================
# 4. MAIN BUILD ROUTINE
# ==========================================

def build_cluster(doc, offset=(0,0,0)):
    """
    Builds the Hydrocyclone cluster at the specified offset coordinates.
    """
    
    # Levels
    z_launder_base = 200.0
    z_cyclone_mid = z_launder_base + launder_height + 150
    z_cyclone_top = z_cyclone_mid + cyclone_len_cyl
    z_manifold_top = z_cyclone_top + 100
    
    # --- A. BOTTOM LAUNDER (TUB) ---
    # Outer Shell (Manual boolean cut required as helper make_cylinder adds object directly)
    # We will make two temporary cylinders, cut them, then add to doc
    l_outer = Part.makeCylinder(launder_radius, launder_height)
    l_inner = Part.makeCylinder(launder_radius - 20, launder_height)
    launder_shape = l_outer.cut(l_inner)
    launder_shape.translate(App.Vector(offset[0], offset[1], z_launder_base + offset[2]))
    
    obj_l = doc.addObject("Part::Feature", "Launder_Tub")
    obj_l.Shape = launder_shape
    obj_l.ViewObject.ShapeColor = col_grey_body
    
    # Discharge Spout
    make_cylinder(doc, "Launder_Out", 150, 200, 
                  -launder_radius, 0, z_launder_base + 200, col_grey_body, offset, axis=App.Vector(1,0,0))
    make_cylinder(doc, "Launder_Flange", 180, 20, 
                  -launder_radius-200, 0, z_launder_base + 200, col_dark_metal, offset, axis=App.Vector(1,0,0))

    # Legs
    for i in [45, 135, 225, 315]:
        rad = math.radians(i)
        lx = (launder_radius - 50) * math.cos(rad)
        ly = (launder_radius - 50) * math.sin(rad)
        make_cylinder(doc, f"Leg_{i}", 50, z_launder_base, 
                      lx, ly, 0, col_dark_metal, offset)

    # --- B. CENTRAL MANIFOLD ---
    make_cylinder(doc, "Feed_Manifold", tank_radius, z_manifold_top - z_launder_base + 100, 
                  0, 0, z_launder_base, col_grey_body, offset)
    
    # Dome Cap (Manual shape needed for Sphere)
    dome = Part.makeSphere(tank_radius)
    mat = App.Matrix()
    mat.scale(1.0, 1.0, 0.25)
    dome.transformShape(mat)
    dome.translate(App.Vector(offset[0], offset[1], z_manifold_top + 100 + offset[2]))
    
    obj_d = doc.addObject("Part::Feature", "Manifold_Cap")
    obj_d.Shape = dome
    obj_d.ViewObject.ShapeColor = col_grey_body

    # --- C. CYCLONES ---
    for i in range(num_cyclones):
        angle_deg = i * (360.0 / num_cyclones)
        angle_rad = math.radians(angle_deg)
        
        # Cyclone Center Coordinates
        cx = cluster_radius * math.cos(angle_rad)
        cy = cluster_radius * math.sin(angle_rad)
        
        # 1. Cone
        make_cone(doc, f"Cyc_Cone_{i}", cyclone_dia/5, cyclone_dia/2, cyclone_len_cone,
                  cx, cy, z_cyclone_mid - cyclone_len_cone, col_blue_cyc, offset)
        
        # 2. Cylinder Body
        make_cylinder(doc, f"Cyc_Cyl_{i}", cyclone_dia/2, cyclone_len_cyl,
                      cx, cy, z_cyclone_mid, col_blue_cyc, offset)
        
        # Flanges (Mid and Top)
        make_cylinder(doc, f"Flange_Mid_{i}", cyclone_dia/2 + 25, 20, 
                      cx, cy, z_cyclone_mid, col_dark_metal, offset)
        make_cylinder(doc, f"Flange_Top_{i}", cyclone_dia/2 + 25, 20, 
                      cx, cy, z_cyclone_top, col_dark_metal, offset)
        
        # 3. Inlet Pipe (Radial connection to Manifold)
        inlet_len = (cluster_radius - cyclone_dia/2) - tank_radius
        inlet_r = 70.0
        
        inlet = Part.makeCylinder(inlet_r, inlet_len)
        inlet.rotate(App.Vector(0,0,0), App.Vector(0,1,0), -90) # Align along X
        inlet.translate(App.Vector(tank_radius, 0, z_cyclone_mid + 100)) # Move to edge of tank
        inlet.rotate(App.Vector(0,0,0), App.Vector(0,0,1), angle_deg) # Rotate to radial position
        inlet.translate(App.Vector(offset[0], offset[1], offset[2])) # Apply global offset
        
        obj_in = doc.addObject("Part::Feature", f"Inlet_{i}")
        obj_in.Shape = inlet
        obj_in.ViewObject.ShapeColor = col_blue_cyc
        
        # 4. Valve (On Inlet)
        # Valve Body
        v_dist = tank_radius + (inlet_len * 0.4)
        vx = v_dist * math.cos(angle_rad)
        vy = v_dist * math.sin(angle_rad)
        vz = z_cyclone_mid + 100
        
        make_cylinder(doc, f"ValveBody_{i}", inlet_r + 20, 100, 
                      vx, vy, vz - 50, col_dark_metal, offset)
        # Valve Stem
        make_cylinder(doc, f"ValveStem_{i}", 15, 150, 
                      vx, vy, vz + 50, col_dark_metal, offset)
        
        # Handwheel (Manual Torus)
        wheel = Part.makeTorus(60, 10)
        wheel.translate(App.Vector(vx + offset[0], vy + offset[1], vz + 200 + offset[2]))
        
        obj_w = doc.addObject("Part::Feature", f"HandWheel_{i}")
        obj_w.Shape = wheel
        obj_w.ViewObject.ShapeColor = col_valve_wheel
        
        # 5. Overflow Pipe ("Candy Cane")
        # Vertical section up from cyclone
        pipe_r = 60.0
        make_cylinder(doc, f"Pipe_Up_{i}", pipe_r, 300, 
                      cx, cy, z_cyclone_top, col_grey_body, offset)
        
        # U-Bend (180 deg) pointing to center
        bend_radius = 200.0
        bend_z = z_cyclone_top + 300
        # Rotate bend to face INWARD (angle_deg + 180)
        make_u_bend(doc, f"Bend_{i}", pipe_r, bend_radius, cx, cy, bend_z, angle_deg + 180, col_grey_body, offset)
        
        # Downward pipe into manifold
        dx = (cluster_radius - (bend_radius*2)) * math.cos(angle_rad)
        dy = (cluster_radius - (bend_radius*2)) * math.sin(angle_rad)
        
        make_cylinder(doc, f"Pipe_Down_{i}", pipe_r, 200, 
                      dx, dy, z_manifold_top - 50, col_grey_body, offset)
        
        # 6. Support Bracket
        b_len = 200
        b_h = 200
        
        # We need a manual boolean cut for the wedge shape, then apply offset
        bracket = Part.makeBox(b_len, 20, b_h)
        cut_box = Part.makeBox(b_len + 10, 30, b_h + 10)
        cut_box.rotate(App.Vector(0,0,0), App.Vector(0,1,0), -45)
        cut_box.translate(App.Vector(0, -5, b_h))
        bracket = bracket.cut(cut_box)
        
        # Position
        bracket.translate(App.Vector(tank_radius, -10, z_cyclone_mid - 150))
        bracket.rotate(App.Vector(0,0,0), App.Vector(0,0,1), angle_deg)
        bracket.translate(App.Vector(offset[0], offset[1], offset[2]))
        
        obj_br = doc.addObject("Part::Feature", f"Bracket_{i}")
        obj_br.Shape = bracket
        obj_br.ViewObject.ShapeColor = col_grey_body




def make_hopper(doc, name, top_w, top_d, bot_w, bot_d, h, x, y, z, color, offset=(0,0,0)):
    # Top Rectangle (Larger)
    p1 = App.Vector(-top_w/2, -top_d/2, h)
    p2 = App.Vector(top_w/2, -top_d/2, h)
    p3 = App.Vector(top_w/2, top_d/2, h)
    p4 = App.Vector(-top_w/2, top_d/2, h)
    wire_top = Part.makePolygon([p1, p2, p3, p4, p1])
    
    # Bottom Rectangle (Smaller discharge)
    p1b = App.Vector(-bot_w/2, -bot_d/2, 0)
    p2b = App.Vector(bot_w/2, -bot_d/2, 0)
    p3b = App.Vector(bot_w/2, bot_d/2, 0)
    p4b = App.Vector(-bot_w/2, bot_d/2, 0)
    wire_bot = Part.makePolygon([p1b, p2b, p3b, p4b, p1b])
    
    # Loft
    loft = Part.makeLoft([wire_bot, wire_top], True)
    
    # Apply translation with offset
    loft.translate(App.Vector(x + offset[0], y + offset[1], z + offset[2]))
    
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = loft
    obj.ViewObject.ShapeColor = color
    return obj

# ==========================================
# 4. MAIN BUILD ROUTINE
# ==========================================

def build_dust_collector(doc, offset=(0,0,0)):
    """
    Builds the Dust Collector at the specified offset coordinates.
    """
    
    # Z-Coordinates
    z_floor = 0.0
    z_body_start = leg_height
    z_body_end = z_body_start + body_height
    z_hopper_discharge = z_body_start - hopper_height
    
    # --- A. LEGS & FRAME ---
    leg_size = 100.0
    # Legs are positioned at the corners of the main body width
    leg_positions = [
        (-width/2, -depth/2), (width/2 - leg_size, -depth/2),
        (-width/2, depth/2 - leg_size), (width/2 - leg_size, depth/2 - leg_size)
    ]
    
    for i, (lx, ly) in enumerate(leg_positions):
        # Leg Column
        make_box(doc, f"Leg_{i}", leg_size, leg_size, leg_height, 
                 lx, ly, 0, col_dark_grey, offset)
        
        # Foot Plate
        make_box(doc, f"Foot_{i}", leg_size+100, leg_size+100, 20, 
                 lx-50, ly-50, 0, col_dark_grey, offset)

    # Cross Bracing (Low level)
    brace_z = 300.0
    # Front/Back braces
    make_box(doc, "Brace_F", width, 60, 60, 
             -width/2, -depth/2 + 20, brace_z, col_dark_grey, offset)
             
    make_box(doc, "Brace_B", width, 60, 60, 
             -width/2, depth/2 - 80, brace_z, col_dark_grey, offset)
             
    # Side braces
    make_box(doc, "Brace_L", 60, depth, 60, 
             -width/2 + 20, -depth/2, brace_z, col_dark_grey, offset)
             
    make_box(doc, "Brace_R", 60, depth, 60, 
             width/2 - 80, -depth/2, brace_z, col_dark_grey, offset)

    # --- B. HOPPER ---
    # Creates the pyramid funnel
    make_hopper(doc, "Hopper", width, depth, discharge_size, discharge_size, hopper_height, 
                0, 0, z_hopper_discharge, col_grey_body, offset)
    
    # Discharge Flange
    make_box(doc, "DischargeFlange", discharge_size+100, discharge_size+100, 20, 
             -(discharge_size+100)/2, -(discharge_size+100)/2, z_hopper_discharge - 20, col_dark_grey, offset)

    # --- C. MAIN BODY ---
    # Main Box
    make_box(doc, "MainBody", width, depth, body_height, 
             -width/2, -depth/2, z_body_start, col_grey_body, offset)
    
    # Top Cap/Lid
    lid_h = 100
    make_box(doc, "TopLid", width+50, depth+50, lid_h, 
             -(width+50)/2, -(depth+50)/2, z_body_end, col_grey_body, offset)

    # --- D. STIFFENERS / RIBS ---
    # The image shows horizontal ribs wrapping around the body
    num_ribs = 4
    rib_spacing = body_height / num_ribs
    rib_thick = 40
    rib_depth = 50
    
    for i in range(num_ribs):
        rz = z_body_start + (i * rib_spacing) + (rib_spacing/2)
        # Create a hollow rectangle using 4 boxes
        
        # Front
        make_box(doc, f"Rib_F_{i}", width + 2*rib_depth, rib_depth, rib_thick, 
                 -width/2 - rib_depth, -depth/2 - rib_depth, rz, col_grey_body, offset)
                 
        # Back
        make_box(doc, f"Rib_B_{i}", width + 2*rib_depth, rib_depth, rib_thick, 
                 -width/2 - rib_depth, depth/2, rz, col_grey_body, offset)
                 
        # Left
        make_box(doc, f"Rib_L_{i}", rib_depth, depth, rib_thick, 
                 -width/2 - rib_depth, -depth/2, rz, col_grey_body, offset)
                 
        # Right
        make_box(doc, f"Rib_R_{i}", rib_depth, depth, rib_thick, 
                 width/2, -depth/2, rz, col_grey_body, offset)

    # --- E. SIDE INLET PIPE ---
    # Pipe entering the hopper area
    inlet_r = 250.0
    inlet_len = 600.0
    inlet_z = z_hopper_discharge + (hopper_height * 0.6)
    
    # Pipe aligned to X axis
    make_cylinder(doc, "InletPipe", inlet_r, inlet_len, 
                  width/2 - 100, 0, inlet_z, col_grey_body, offset, axis=App.Vector(1,0,0))
                  
    # Flange
    make_cylinder(doc, "InletFlange", inlet_r + 50, 30, 
                  width/2 + inlet_len - 30, 0, inlet_z, col_dark_grey, offset, axis=App.Vector(1,0,0))

    # --- F. TOP HEADER (PULSE JET SYSTEM) ---
    # Black pipe running along the front top edge
    header_dia = 150.0
    header_len = width - 200
    header_x = 0
    header_y = -depth/2 - 100 # In front of the box
    header_z = z_body_end + 150
    
    # The Header Tank (Cylinder rotated 90 deg around Y to align X)
    # The helper's axis=(1,0,0) handles X-alignment.
    # Note: original code used Part.makeCylinder and rotated manually.
    # Helper make_cylinder axis=1,0,0 rotates (0,0,0)->(0,1,0) 90 deg. 
    # Standard cylinder is along Z. Rotate around Y 90 deg makes it along X.
    make_cylinder(doc, "HeaderTank", header_dia/2, header_len, 
                  -header_len/2, header_y, header_z, col_black, offset, axis=App.Vector(1,0,0))
    
    # Valves connecting Header to Top Lid
    num_valves = 8
    valve_spacing = header_len / num_valves
    start_x = -header_len/2 + (valve_spacing/2)
    
    for i in range(num_valves):
        vx = start_x + (i * valve_spacing)
        
        # Connection Pipe (Horizontal from header to unit - Y axis)
        conn_len = 150
        make_cylinder(doc, f"ValvePipe_{i}", 20, conn_len, 
                      vx, header_y, header_z, col_black, offset, axis=App.Vector(0,1,0))
        
        # Valve Body (Vertical cylinder - Z axis)
        make_cylinder(doc, f"ValveBody_{i}", 30, 60, 
                      vx, header_y + 80, header_z + 20, col_valve, offset, axis=App.Vector(0,0,1))
        
        # Injection pipe (Elbow into lid - Vertical down)
        # Using Z axis, but position is shifted
        make_cylinder(doc, f"InjPipe_{i}", 20, 150, 
                      vx, header_y + 150, header_z - 150, col_black, offset, axis=App.Vector(0,0,1))




# Specialized helpers adapted to use offset
def make_loft(doc, name, bot_w, bot_d, top_w, top_d, h, x, y, z, color, offset=(0,0,0)):
    # Bottom Rectangle
    p1 = App.Vector(-bot_w/2, -bot_d/2, 0)
    p2 = App.Vector(bot_w/2, -bot_d/2, 0)
    p3 = App.Vector(bot_w/2, bot_d/2, 0)
    p4 = App.Vector(-bot_w/2, bot_d/2, 0)
    wire_bot = Part.makePolygon([p1, p2, p3, p4, p1])
    
    # Top Rectangle
    p1t = App.Vector(-top_w/2, -top_d/2, h)
    p2t = App.Vector(top_w/2, -top_d/2, h)
    p3t = App.Vector(top_w/2, top_d/2, h)
    p4t = App.Vector(-top_w/2, top_d/2, h)
    wire_top = Part.makePolygon([p1t, p2t, p3t, p4t, p1t])
    
    # Loft
    loft = Part.makeLoft([wire_bot, wire_top], True)
    loft.translate(App.Vector(x + offset[0], y + offset[1], z + offset[2]))
    
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = loft
    obj.ViewObject.ShapeColor = color
    return obj

def make_transition(doc, name, face_w, face_d, duct_w, duct_d, length, x, y, z, orient_x, color, offset=(0,0,0)):
    # Creates a transition duct (pyramid on its side)
    # orient_x = 1 (points right), -1 (points left)
    
    # Large Face (Attached to housing)
    p1 = App.Vector(0, -face_d/2, 0)
    p2 = App.Vector(0, face_d/2, 0)
    p3 = App.Vector(0, face_d/2, face_w)
    p4 = App.Vector(0, -face_d/2, face_w)
    wire_large = Part.makePolygon([p1, p2, p3, p4, p1])
    
    # Small Face (Duct flange)
    dx = length * orient_x
    p1s = App.Vector(dx, -duct_d/2, (face_w - duct_w)/2)
    p2s = App.Vector(dx, duct_d/2, (face_w - duct_w)/2)
    p3s = App.Vector(dx, duct_d/2, (face_w - duct_w)/2 + duct_w)
    p4s = App.Vector(dx, -duct_d/2, (face_w - duct_w)/2 + duct_w)
    wire_small = Part.makePolygon([p1s, p2s, p3s, p4s, p1s])
    
    loft = Part.makeLoft([wire_large, wire_small], True)
    loft.translate(App.Vector(x + offset[0], y + offset[1], z + offset[2]))
    
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = loft
    obj.ViewObject.ShapeColor = color
    return obj

# ==========================================
# 4. MAIN BUILD ROUTINE
# ==========================================

def build_esp(doc, offset=(0,0,0)):
    """
    Builds the Electrostatic Precipitator at the specified offset coordinates.
    """
    
    # Z-Levels
    z_ground = 0
    z_housing_bot = leg_h
    z_hopper_tip = z_housing_bot - hopper_h
    z_roof = z_housing_bot + housing_h
    
    # --- A. HOPPERS ---
    outlet_size = 300.0
    for i in range(num_mods):
        cx = (i * mod_width) + (mod_width/2)
        # Hopper Body
        make_loft(doc, f"Hopper_{i}", outlet_size, outlet_size, mod_width, mod_depth, hopper_h, 
                  cx, 0, z_hopper_tip, col_casing, offset)
                  
        # Flange
        make_box(doc, f"Flange_{i}", 400, 400, 50, 
                 cx - 200, -200, z_hopper_tip - 50, col_stiffener, offset)

    # --- B. MAIN HOUSING (WALLS) ---
    # Back Wall
    make_box(doc, "Wall_Back", total_width, 20, housing_h, 
             0, mod_depth/2, z_housing_bot, col_casing, offset)
             
    # Left Wall
    make_box(doc, "Wall_Left", 20, mod_depth, housing_h, 
             0, -mod_depth/2, z_housing_bot, col_casing, offset)
             
    # Right Wall
    make_box(doc, "Wall_Right", 20, mod_depth, housing_h, 
             total_width - 20, -mod_depth/2, z_housing_bot, col_casing, offset)
             
    # Roof
    make_box(doc, "Roof", total_width + 100, mod_depth + 100, 100, 
             -50, -mod_depth/2 - 50, z_roof, col_casing, offset)
    
    # Front Wall with Cutaway (Boolean operation requires manual offset)
    # 1. Create solid wall
    wall_f = Part.makeBox(total_width, 20, housing_h)
    wall_f.translate(App.Vector(0, -mod_depth/2, z_housing_bot))
    
    # 2. Create Cutout shape (window)
    cutout = Part.makeBox(total_width * 0.5, 100, housing_h * 0.6)
    cutout.translate(App.Vector(total_width * 0.4, -mod_depth/2 - 40, z_housing_bot + (housing_h*0.2)))
    
    # 3. Perform Cut
    wall_f_cut = wall_f.cut(cutout)
    
    # 4. Apply Offset
    wall_f_cut.translate(App.Vector(offset[0], offset[1], offset[2]))
    
    obj_wf = doc.addObject("Part::Feature", "Wall_Front_Cutaway")
    obj_wf.Shape = wall_f_cut
    obj_wf.ViewObject.ShapeColor = col_casing

    # --- C. INTERNAL COMPONENTS (VISIBLE THROUGH CUTAWAY) ---
    # Collecting Plates (Green)
    plate_gap = 400
    num_plates = int((total_width - 200) / plate_gap)
    plate_h = housing_h * 0.8
    plate_d = mod_depth * 0.8
    
    for i in range(num_plates):
        px = 200 + (i * plate_gap)
        make_box(doc, f"Plate_{i}", 20, plate_d, plate_h, 
                 px, -plate_d/2, z_housing_bot + (housing_h*0.1), col_plates, offset)
    
    # Rapping Beams (Red - Top and Bottom)
    beam_w = total_width - 100
    beam_d = mod_depth - 200
    
    # Top Beam
    make_box(doc, "Beam_Int_Top", beam_w, beam_d, 200, 
             50, -beam_d/2, z_housing_bot + housing_h - 400, col_internal_beam, offset)
             
    # Bottom Beam
    make_box(doc, "Beam_Int_Bot", beam_w, beam_d, 200, 
             50, -beam_d/2, z_housing_bot + 400, col_internal_beam, offset)
    
    # Discharge Electrodes (Thin frames between plates)
    for i in range(num_plates - 1):
        ex = 200 + (i * plate_gap) + (plate_gap/2)
        make_box(doc, f"Electrode_{i}", 5, plate_d - 100, plate_h - 200, 
                 ex, -(plate_d-100)/2, z_housing_bot + (housing_h*0.1) + 100, col_structure, offset)

    # --- D. EXTERNAL STIFFENERS (RIBS) ---
    # Horizontal beams wrapping the housing
    num_ribs = 4
    rib_spacing = housing_h / (num_ribs + 1)
    
    for i in range(num_ribs):
        rz = z_housing_bot + ((i + 1) * rib_spacing)
        
        # Front Rib (Cut by window - requires manual boolean + offset)
        rib_f = Part.makeBox(total_width, 50, 100)
        rib_f.translate(App.Vector(0, -mod_depth/2 - 50, rz))
        rib_f_cut = rib_f.cut(cutout) # Use same cutout to trim rib
        rib_f_cut.translate(App.Vector(offset[0], offset[1], offset[2]))
        
        obj_rf = doc.addObject("Part::Feature", f"Rib_F_{i}")
        obj_rf.Shape = rib_f_cut
        obj_rf.ViewObject.ShapeColor = col_stiffener
        
        # Side/Back Ribs
        make_box(doc, f"Rib_B_{i}", total_width, 50, 100, 
                 0, mod_depth/2, rz, col_stiffener, offset)
                 
        make_box(doc, f"Rib_L_{i}", 50, mod_depth, 100, 
                 -50, -mod_depth/2, rz, col_stiffener, offset)
                 
        make_box(doc, f"Rib_R_{i}", 50, mod_depth, 100, 
                 total_width, -mod_depth/2, rz, col_stiffener, offset)

    # --- E. TRANSITION DUCTS (INLET/OUTLET) ---
    # Pyramidal diffusers on sides
    t_len = 1000.0
    t_duct_size = 1500.0
    
    # Left Transition (Inlet)
    make_transition(doc, "Trans_Inlet", housing_h - 400, mod_depth - 400, t_duct_size, t_duct_size, t_len, 
                    0, 0, z_housing_bot + 200, -1, col_casing, offset)
    
    # Right Transition (Outlet)
    make_transition(doc, "Trans_Outlet", housing_h - 400, mod_depth - 400, t_duct_size, t_duct_size, t_len, 
                    total_width, 0, z_housing_bot + 200, 1, col_casing, offset)

    # --- F. SUPPORT STRUCTURE ---
    # Legs at corners and middle
    leg_coords = [0, total_width/2, total_width]
    
    for lx in leg_coords:
        # Front Leg
        make_box(doc, f"Leg_F_{lx}", 150, 150, z_housing_bot, 
                 lx - 75, -mod_depth/2 - 75, 0, col_structure, offset)
        # Back Leg
        make_box(doc, f"Leg_B_{lx}", 150, 150, z_housing_bot, 
                 lx - 75, mod_depth/2 - 75, 0, col_structure, offset)
        
    # Cross Bracing (Simple X)
    brace = Part.makeBox(total_width + 200, 20, 100)
    # Manual rotation for X? Original code just placed a horizontal bar.
    # We will keep it simple as per original
    brace.translate(App.Vector(-100 + offset[0], -mod_depth/2 - 75 + offset[1], leg_h/2 + offset[2]))
    
    obj_br = doc.addObject("Part::Feature", "Brace_Horiz_F")
    obj_br.Shape = brace
    obj_br.ViewObject.ShapeColor = col_structure


def make_hopper_shape(doc, name, x, y, z, rot_angle, color, offset=(0,0,0)):
    # Specialized shape logic kept, but refactored for offset
    w_top, l_top = 800, 800
    w_bot, l_bot = 400, 400
    h = 600
    
    p1 = App.Vector(-l_bot/2, -w_bot/2, 0)
    p2 = App.Vector(l_bot/2, -w_bot/2, 0)
    p3 = App.Vector(l_bot/2, w_bot/2, 0)
    p4 = App.Vector(-l_bot/2, w_bot/2, 0)
    wire_bot = Part.makePolygon([p1, p2, p3, p4, p1])
    
    p1t = App.Vector(-l_top/2 - 200, -w_top/2, h)
    p2t = App.Vector(l_top/2 - 200, -w_top/2, h)
    p3t = App.Vector(l_top/2 - 200, w_top/2, h)
    p4t = App.Vector(-l_top/2 - 200, w_top/2, h)
    wire_top = Part.makePolygon([p1t, p2t, p3t, p4t, p1t])
    
    loft = Part.makeLoft([wire_bot, wire_top], True)
    
    # Apply local rotation
    if rot_angle != 0:
        loft.rotate(App.Vector(0,0,0), App.Vector(0,1,0), -rot_angle)
    
    # Apply translation with offset
    loft.translate(App.Vector(x + offset[0], y + offset[1], z + offset[2]))
    
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = loft
    obj.ViewObject.ShapeColor = color
    return obj

# ==========================================
# 4. MAIN BUILD ROUTINE
# ==========================================

def build_scrubber(doc, offset=(0,0,0)):
    """
    Builds the Rotary Scrubber at the specified offset coordinates.
    """
    rad = math.radians(incline_angle)
    pivot_x = 3000
    pivot_z = leg_base_height + 200
    
    # --- A. STRUCTURAL FRAME ---
    beam_len = drum_len + 500
    beam_h = 200
    beam_w = 100
    start_z = pivot_z + (beam_len * math.sin(rad))
    start_x = pivot_x - (beam_len * math.cos(rad))
    
    # Left Beam (Box rotated around Y)
    make_box(doc, "Beam_L", beam_len, beam_w, beam_h, 
             start_x, -frame_width/2, start_z, col_black, offset,
             rotation_angle=-incline_angle, rotation_axis=App.Vector(0,1,0))
             
    # Right Beam
    make_box(doc, "Beam_R", beam_len, beam_w, beam_h, 
             start_x, frame_width/2 - beam_w, start_z, col_black, offset,
             rotation_angle=-incline_angle, rotation_axis=App.Vector(0,1,0))
             
    # Legs
    fractions = [0.1, 0.5, 0.9]
    for i, frac in enumerate(fractions):
        dist = beam_len * frac
        local_h = start_z - (dist * math.sin(rad))
        local_x = start_x + (dist * math.cos(rad))
        
        make_box(doc, f"Leg_L_{i}", 150, 150, local_h, 
                 local_x, -frame_width/2 - 25, 0, col_black, offset)
                 
        make_box(doc, f"Leg_R_{i}", 150, 150, local_h, 
                 local_x, frame_width/2 - 125, 0, col_black, offset)
                 
        make_box(doc, f"Foot_L_{i}", 250, 250, 20, 
                 local_x-50, -frame_width/2 - 75, 0, col_black, offset)
                 
        make_box(doc, f"Foot_R_{i}", 250, 250, 20, 
                 local_x-50, frame_width/2 - 175, 0, col_black, offset)
                 
        make_box(doc, f"Brace_{i}", 100, frame_width, 100, 
                 local_x + 25, -frame_width/2, local_h - 300, col_black, offset)

    # --- B. ROLLERS ---
    roller_locs = [0.2, 0.8]
    for i, frac in enumerate(roller_locs):
        dist = beam_len * frac
        rx = start_x + (dist * math.cos(rad))
        rz = start_z - (dist * math.sin(rad)) + beam_h
        
        # Roller Brackets
        make_box(doc, f"RollerBracket_L_{i}", 300, 100, 150, 
                 rx, -frame_width/2, rz, col_sepro_blue, offset,
                 rotation_angle=-incline_angle, rotation_axis=App.Vector(0,1,0))
                 
        make_box(doc, f"RollerBracket_R_{i}", 300, 100, 150, 
                 rx, frame_width/2 - 100, rz, col_sepro_blue, offset,
                 rotation_angle=-incline_angle, rotation_axis=App.Vector(0,1,0))
        
        # Left Wheel
        # Cylinder axis (1,0,0) -> Rotated 90 around Y. Then rotated -incline around Y.
        # This requires manual logic because helper make_cylinder aligns to cardinal axes first.
        # We'll create the shape, apply compound rotation, then translate with offset manually.
        
        w_shape = Part.makeCylinder(80, 50)
        w_shape.rotate(App.Vector(0,0,0), App.Vector(1,0,0), 90) # Orient horizontal (rolling direction)
        w_shape.rotate(App.Vector(0,0,0), App.Vector(0,1,0), -incline_angle) # Match incline
        
        # Calculate position + offset
        wx_l = rx + 150 + offset[0]
        wy_l = -frame_width/2 + 100 + offset[1]
        wz_l = rz + 150 + offset[2]
        
        w_shape.translate(App.Vector(wx_l, wy_l, wz_l))
        
        obj_wl = doc.addObject("Part::Feature", f"Wheel_L_{i}")
        obj_wl.Shape = w_shape
        obj_wl.ViewObject.ShapeColor = col_black
        
        # Right Wheel
        w_shape_r = Part.makeCylinder(80, 50)
        w_shape_r.rotate(App.Vector(0,0,0), App.Vector(1,0,0), 90)
        w_shape_r.rotate(App.Vector(0,0,0), App.Vector(0,1,0), -incline_angle)
        
        wx_r = rx + 150 + offset[0]
        wy_r = frame_width/2 - 150 + offset[1]
        wz_r = rz + 150 + offset[2]
        
        w_shape_r.translate(App.Vector(wx_r, wy_r, wz_r))
        
        obj_wr = doc.addObject("Part::Feature", f"Wheel_R_{i}")
        obj_wr.Shape = w_shape_r
        obj_wr.ViewObject.ShapeColor = col_black

    # --- C. DRUM ---
    drum_offset_z = 600
    drum_start_x = start_x + 200
    drum_start_z = start_z + beam_h + drum_offset_z
    seg_len = drum_len / 3
    
    for i in range(3):
        seg_dist = i * seg_len
        sx = drum_start_x + (seg_dist * math.cos(rad))
        sz = drum_start_z - (seg_dist * math.sin(rad))
        
        # Segment (Cylinder)
        # Helper make_cylinder axis=1,0,0 rotates 90 Y (aligns X).
        # We need alignment X, THEN rotation -incline around Y.
        # Since helper applies rotation_angle AFTER initial alignment, this works:
        # axis=(1,0,0) -> aligns with X
        # rotation_angle = -incline, rotation_axis = (0,1,0) -> rotates around Y
        
        # However, make_cylinder axis logic: 
        # if axis=(1,0,0): rotate (0,0,0), (0,1,0), 90.
        # We can't easily pass the compound rotation into the specific helper signature 
        # without modifying the helper or doing it manually like the wheels.
        # But wait, make_cylinder takes axis=Vector(). If we pass the actual inclined vector?
        # The helper logic provided hardcodes checks for (1,0,0) or (0,1,0).
        # We will do manual shape creation for complex rotations to ensure accuracy.
        
        cyl = Part.makeCylinder(drum_dia/2, seg_len)
        cyl.rotate(App.Vector(0,0,0), App.Vector(0,1,0), 90) # Align X
        cyl.rotate(App.Vector(0,0,0), App.Vector(0,1,0), -incline_angle) # Incline
        cyl.translate(App.Vector(sx + offset[0], offset[1], sz + offset[2]))
        
        obj_seg = doc.addObject("Part::Feature", f"DrumSeg_{i}")
        obj_seg.Shape = cyl
        obj_seg.ViewObject.ShapeColor = col_sepro_blue
        
        # Flange
        fx = sx + (seg_len * math.cos(rad))
        fz = sz - (seg_len * math.sin(rad))
        
        flange = Part.makeCylinder(drum_dia/2 + 40, 40)
        flange.rotate(App.Vector(0,0,0), App.Vector(0,1,0), 90)
        flange.rotate(App.Vector(0,0,0), App.Vector(0,1,0), -incline_angle)
        flange.translate(App.Vector(fx + offset[0], offset[1], fz + offset[2]))
        
        obj_fl = doc.addObject("Part::Feature", f"Flange_{i}")
        obj_fl.Shape = flange
        obj_fl.ViewObject.ShapeColor = col_metal
        
        # Tire
        if i != 1:
            tire_offset = seg_len * 0.5
            tx = sx + (tire_offset * math.cos(rad))
            tz = sz - (tire_offset * math.sin(rad))
            
            tire = Part.makeCylinder(drum_dia/2 + 20, 150)
            tire.rotate(App.Vector(0,0,0), App.Vector(0,1,0), 90)
            tire.rotate(App.Vector(0,0,0), App.Vector(0,1,0), -incline_angle)
            tire.translate(App.Vector(tx + offset[0], offset[1], tz + offset[2]))
            
            obj_tr = doc.addObject("Part::Feature", f"Tire_{i}")
            obj_tr.Shape = tire
            obj_tr.ViewObject.ShapeColor = col_metal

    # --- D. INLET & OUTLET ---
    make_hopper_shape(doc, "InletHopper", drum_start_x, 0, drum_start_z + 200, incline_angle, col_sepro_blue, offset)
    
    end_dist = drum_len
    ex = drum_start_x + (end_dist * math.cos(rad))
    ez = drum_start_z - (end_dist * math.sin(rad))
    
    pipe = Part.makeCylinder(drum_dia/2 - 100, 800)
    pipe.rotate(App.Vector(0,0,0), App.Vector(0,1,0), 90)
    pipe.rotate(App.Vector(0,0,0), App.Vector(0,1,0), -incline_angle)
    pipe.translate(App.Vector(ex + offset[0], offset[1], ez + offset[2]))
    
    obj_out = doc.addObject("Part::Feature", "OutletPipe")
    obj_out.Shape = pipe
    obj_out.ViewObject.ShapeColor = col_black

    # --- E. VENTS ---
    for i, dist_add in enumerate([1000, 2500]):
        px = drum_start_x + (dist_add * math.cos(rad))
        pz = drum_start_z - (dist_add * math.sin(rad))
        
        port = Part.makeCylinder(60, 400)
        port.rotate(App.Vector(0,0,0), App.Vector(0,1,0), -incline_angle) # Just incline (vertical relative to drum?)
        
        # Calculate shift relative to drum axis to place on top
        shift_z = (drum_dia/2) * math.cos(rad)
        shift_x = (drum_dia/2) * math.sin(rad)
        
        port.translate(App.Vector(px + shift_x + offset[0], offset[1], pz + shift_z + offset[2]))
        
        obj_pt = doc.addObject("Part::Feature", f"Vent_{i}")
        obj_pt.Shape = port
        obj_pt.ViewObject.ShapeColor = col_black




def build_swan_neck_conveyor(doc, offset=(0,0,0)):
    """
    Builds a Z-shape / Swan-neck conveyor at the specified offset.
    """
    
    # --- CALCULATION ---
    rad = math.radians(incline_angle)
    
    # Key Points (local coordinates relative to offset)
    # P1: Start of bottom section
    p1_x, p1_z = 0, leg_base_height
    
    # P2: Knee (End of bottom, Start of incline)
    p2_x, p2_z = bottom_len, leg_base_height
    
    # P3: Elbow (End of incline, Start of top)
    incline_run = incline_len * math.cos(rad)
    incline_rise = incline_len * math.sin(rad)
    p3_x = p2_x + incline_run
    p3_z = p2_z + incline_rise
    
    # P4: End of top section
    p4_x = p3_x + top_len
    p4_z = p3_z
    
    rail_h = 150.0
    guard_h = 250.0
    
    # ==========================
    # A. FRAME (Blue Channels)
    # ==========================
    
    # 1. Bottom Section Frame
    make_box(doc, "Frame_Bot_L", bottom_len, 50, rail_h, 
             p1_x, 0, p1_z - rail_h, col_frame_blue, offset)
    make_box(doc, "Frame_Bot_R", bottom_len, 50, rail_h, 
             p1_x, frame_width - 50, p1_z - rail_h, col_frame_blue, offset)
             
    # 2. Incline Section Frame
    make_box(doc, "Frame_Inc_L", incline_len, 50, rail_h, 
             p2_x, 0, p2_z - rail_h, col_frame_blue, offset,
             rotation_angle=-incline_angle, rotation_axis=App.Vector(0,1,0))
             
    make_box(doc, "Frame_Inc_R", incline_len, 50, rail_h, 
             p2_x, frame_width - 50, p2_z - rail_h, col_frame_blue, offset,
             rotation_angle=-incline_angle, rotation_axis=App.Vector(0,1,0))
             
    # 3. Top Section Frame
    make_box(doc, "Frame_Top_L", top_len, 50, rail_h, 
             p3_x, 0, p3_z - rail_h, col_frame_blue, offset)
    make_box(doc, "Frame_Top_R", top_len, 50, rail_h, 
             p3_x, frame_width - 50, p3_z - rail_h, col_frame_blue, offset)

    # ==========================
    # B. LEGS (Blue Supports)
    # ==========================
    leg_dim = 80.0
    
    # Leg Locations (X coordinates)
    leg_xs = [200, bottom_len - 200, p3_x + 200, p4_x - 200]
    mid_inc_x = p2_x + (incline_run / 2)
    
    for i, lx in enumerate(leg_xs + [mid_inc_x]):
        if lx <= p2_x: 
            lz = p1_z - rail_h
        elif lx >= p3_x: 
            lz = p3_z - rail_h
        else: 
            dist_along = (lx - p2_x)
            lz = (p2_z - rail_h) + (dist_along * math.tan(rad))
            
        make_box(doc, f"Leg_L_{i}", leg_dim, leg_dim, lz, 
                 lx, 0, 0, col_frame_blue, offset)
        make_box(doc, f"Leg_R_{i}", leg_dim, leg_dim, lz, 
                 lx, frame_width - leg_dim, 0, col_frame_blue, offset)
        make_box(doc, f"Cross_{i}", leg_dim, frame_width, leg_dim, 
                 lx, 0, lz - 200, col_frame_blue, offset)
        make_box(doc, f"Foot_L_{i}", leg_dim + 40, leg_dim + 40, 10, 
                 lx-20, -20, 0, col_frame_blue, offset)
        make_box(doc, f"Foot_R_{i}", leg_dim + 40, leg_dim + 40, 10, 
                 lx-20, frame_width - leg_dim - 20, 0, col_frame_blue, offset)

    # ==========================
    # C. BELT & PULLEYS
    # ==========================
    belt_thick = 10.0
    belt_y = (frame_width - belt_width) / 2
    
    make_box(doc, "Belt_Bot", bottom_len, belt_width, belt_thick, 
             p1_x, belt_y, p1_z, col_belt_black, offset)
             
    make_box(doc, "Belt_Inc", incline_len, belt_width, belt_thick, 
             p2_x, belt_y, p2_z, col_belt_black, offset,
             rotation_angle=-incline_angle, rotation_axis=App.Vector(0,1,0))
             
    make_box(doc, "Belt_Top", top_len, belt_width, belt_thick, 
             p3_x, belt_y, p3_z, col_belt_black, offset)
             
    make_cylinder(doc, "Pulley_Head", 100, belt_width + 20, 
                  p4_x, belt_y - 10, p3_z - 50, col_belt_black, offset, axis=App.Vector(0,1,0))
                  
    make_cylinder(doc, "Pulley_Tail", 100, belt_width + 20, 
                  p1_x, belt_y - 10, p1_z - 50, col_belt_black, offset, axis=App.Vector(0,1,0))

    # ==========================
    # D. ROLLERS
    # ==========================
    roller_spacing = 500.0
    roller_r = 40.0
    
    # Bottom Rollers
    num_bot = int(bottom_len / roller_spacing)
    for i in range(num_bot):
        rx = (i + 0.5) * roller_spacing
        make_cylinder(doc, f"Roller_Bot_{i}", roller_r, belt_width, 
                      rx, belt_y, p1_z - roller_r, col_roller_red, offset, axis=App.Vector(0,1,0))
                      
    # Incline Rollers (Manual Shape for correct rotation)
    num_inc = int(incline_len / roller_spacing)
    for i in range(num_inc):
        dist = (i + 0.5) * roller_spacing
        rx_local = dist * math.cos(rad)
        rz_local = dist * math.sin(rad)
        
        cyl = Part.makeCylinder(roller_r, belt_width)
        cyl.rotate(App.Vector(0,0,0), App.Vector(1,0,0), -90) 
        cyl.rotate(App.Vector(0,0,0), App.Vector(0,1,0), -incline_angle)
        cyl.translate(App.Vector(p2_x + rx_local + offset[0], belt_y + offset[1], p2_z + rz_local - roller_r + offset[2]))
        
        obj_r = doc.addObject("Part::Feature", f"Roller_Inc_{i}")
        obj_r.Shape = cyl
        obj_r.ViewObject.ShapeColor = col_roller_red

    # Top Rollers
    num_top = int(top_len / roller_spacing)
    for i in range(num_top):
        rx = p3_x + (i + 0.5) * roller_spacing
        make_cylinder(doc, f"Roller_Top_{i}", roller_r, belt_width, 
                      rx, belt_y, p3_z - roller_r, col_roller_red, offset, axis=App.Vector(0,1,0))

    # ==========================
    # E. SIDE GUARDS / HOPPERS
    # ==========================
    make_box(doc, "Guard_Bot_L", bottom_len, 10, guard_h, 
             p1_x, 0, p1_z, col_guard_beige, offset)
    make_box(doc, "Guard_Bot_R", bottom_len, 10, guard_h, 
             p1_x, frame_width - 10, p1_z, col_guard_beige, offset)
             
    make_box(doc, "Guard_Inc_L", incline_len, 10, guard_h, 
             p2_x, 0, p2_z, col_guard_beige, offset,
             rotation_angle=-incline_angle, rotation_axis=App.Vector(0,1,0))
    make_box(doc, "Guard_Inc_R", incline_len, 10, guard_h, 
             p2_x, frame_width - 10, p2_z, col_guard_beige, offset,
             rotation_angle=-incline_angle, rotation_axis=App.Vector(0,1,0))
             
    make_box(doc, "Guard_Top_L", top_len, 10, guard_h, 
             p3_x, 0, p3_z, col_guard_beige, offset)
    make_box(doc, "Guard_Top_R", top_len, 10, guard_h, 
             p3_x, frame_width - 10, p3_z, col_guard_beige, offset)

def make_spring_visual(doc, name, r, h, coils, x, y, z, offset=(0,0,0)):
    pitch = h / coils
    rings = []
    wire_r = 20.0  # Scaled from 2.0 to 20.0
    
    for i in range(coils):
        torus = Part.makeTorus(r, wire_r)
        torus.translate(App.Vector(x + offset[0], y + offset[1], z + (i * pitch) + offset[2]))
        rings.append(torus)
        
    comp = Part.makeCompound(rings)
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = comp
    obj.ViewObject.ShapeColor = mag_col_chrome

# ==========================================
# 4. MAIN BUILD ROUTINE
# ==========================================

def build_separator(doc, offset=(0,0,0)):
    """
    Builds the Magnetic Separator (10x Scale) at the specified offset.
    """
    
    # --- A. MAIN TANK BODY ---
    outer_box = Part.makeBox(mag_tank_len, mag_tank_width, mag_tank_height)
    inner_box = Part.makeBox(mag_tank_len - mag_wall_thick*2, mag_tank_width - mag_wall_thick*2, mag_tank_height)
    inner_box.translate(App.Vector(mag_wall_thick, mag_wall_thick, mag_wall_thick))
    
    # Cut inlet cutout at front top (Scaled 10x: 100->1000, 50->500)
    cutout = Part.makeBox(1000, mag_tank_width, 500)
    cutout.translate(App.Vector(mag_tank_len - 1000, 0, mag_tank_height - 500))
    
    tank_shape = outer_box.cut(inner_box).cut(cutout)
    tank_shape.translate(App.Vector(offset[0], offset[1], offset[2]))
    
    obj_tank = doc.addObject("Part::Feature", "TankBody")
    obj_tank.Shape = tank_shape
    obj_tank.ViewObject.ShapeColor = mag_col_grey_paint
    
    # Side Box (Motor Cover) - Left side (Scaled 10x: 50->500, 20->200)
    make_box(doc, "SideCover", mag_tank_len - 500, mag_side_box_width, mag_tank_height - 200, 
             0, -mag_side_box_width, 200, mag_col_grey_paint, offset)

    # --- B. DRUM & ROLLER ---
    # Position (Scaled 10x: 100->1000, 20->200)
    drum_x = 1000
    drum_z = mag_tank_height + 200
    
    # Main Drum (Lower)
    make_cylinder(doc, "MagneticDrum", mag_drum_dia/2, mag_drum_len, 
                  drum_x, mag_wall_thick, drum_z, mag_col_rubber, offset, axis=App.Vector(0,1,0))
    
    # Top Roller (Pressure)
    roller_z = drum_z + (mag_drum_dia/2) + (mag_roller_dia/2)
    make_cylinder(doc, "TopRoller", mag_roller_dia/2, mag_drum_len, 
                  drum_x, mag_wall_thick, roller_z, mag_col_rubber, offset, axis=App.Vector(0,1,0))
    
    # Bearings (Scaled 10x: 25->250, 10->100)
    make_cylinder(doc, "Bearing_L", 250, 100, 
                  drum_x, mag_wall_thick - 100, roller_z, mag_col_chrome, offset, axis=App.Vector(0,1,0))
    make_cylinder(doc, "Bearing_R", 250, 100, 
                  drum_x, mag_tank_width - mag_wall_thick, roller_z, mag_col_chrome, offset, axis=App.Vector(0,1,0))

    # --- C. SPRING TENSIONERS ---
    for side in [0, 1]:
        # (Scaled 10x: 15->150)
        y_pos = mag_wall_thick - 150 if side == 0 else mag_tank_width - mag_wall_thick + 150
        
        # 1. Vertical Rod (Scaled 10x: h 150->1500, r 6->60, x-40->x-400)
        rod_h = 1500
        rod_z = mag_tank_height
        make_cylinder(doc, f"Rod_{side}", 60, rod_h, 
                      drum_x - 400, y_pos, rod_z, mag_col_chrome, offset)
        
        # 2. Horizontal Arm (Scaled 10x: 80x20x20 -> 800x200x200)
        make_box(doc, f"Arm_{side}", 800, 200, 200, 
                 drum_x - 400, y_pos - 100, roller_z - 100, mag_col_steel, offset)
        
        # 3. Spring (Scaled 10x: r 10->100, h 60->600)
        make_spring_visual(doc, f"Spring_{side}", 100, 600, 10, 
                           drum_x - 400, y_pos, roller_z + 100, offset)
        
        # 4. Wingnut (Scaled 10x: Cone 8,4,10 -> 80,40,100 | Wings 40,5,10 -> 400,50,100)
        wn_z = roller_z + 100 + 600
        wn_cone = Part.makeCone(80, 40, 100)
        wn_cone.translate(App.Vector(drum_x - 400, y_pos, wn_z))
        wn_wings = Part.makeBox(400, 50, 100)
        wn_wings.translate(App.Vector(drum_x - 600, y_pos - 25, wn_z + 50))
        
        wn_shape = wn_cone.fuse(wn_wings)
        wn_shape.translate(App.Vector(offset[0], offset[1], offset[2]))
        
        obj_wn = doc.addObject("Part::Feature", f"Wingnut_{side}")
        obj_wn.Shape = wn_shape
        obj_wn.ViewObject.ShapeColor = mag_col_brass

    # --- D. DISCHARGE CHUTE ---
    chute_angle = 35 
    
    # 1. Bottom Plate (Scaled 10x: Thick 2->20, x+50->x+500, z-20->z-200)
    make_box(doc, "ChutePlate", mag_chute_len, mag_chute_width, 20, 
             drum_x + 500, mag_wall_thick, drum_z - 200, mag_col_steel, offset,
             rotation_angle=chute_angle, rotation_axis=App.Vector(0,1,0))
    
    # 2. Side Walls of Chute (Scaled 10x: height 50->500, thick 2->20)
    p1 = App.Vector(0,0,0)
    p2 = App.Vector(mag_chute_len, 0, 0)
    p3 = App.Vector(0, 0, 500) 
    
    wire = Part.makePolygon([p1, p2, p3, p1])
    face = Part.Face(wire)
    wall_tri = face.extrude(App.Vector(0, 20, 0)) 
    wall_tri.rotate(App.Vector(0,0,0), App.Vector(0,1,0), chute_angle)
    
    # Left Wall
    w1 = wall_tri.copy()
    w1.translate(App.Vector(drum_x + 500 + offset[0], mag_wall_thick + offset[1], drum_z - 200 + offset[2]))
    obj_cw1 = doc.addObject("Part::Feature", "ChuteWall_L")
    obj_cw1.Shape = w1
    obj_cw1.ViewObject.ShapeColor = mag_col_steel
    
    # Right Wall (Scaled 10x thick adjust: -2 -> -20)
    w2 = wall_tri.copy()
    w2.translate(App.Vector(drum_x + 500 + offset[0], mag_wall_thick + mag_chute_width - 20 + offset[1], drum_z - 200 + offset[2]))
    obj_cw2 = doc.addObject("Part::Feature", "ChuteWall_R")
    obj_cw2.Shape = w2
    obj_cw2.ViewObject.ShapeColor = mag_col_steel

    # --- E. OUTLET PORT (Scaled 10x: dia 600, len 400, x-800, z 500) ---
    port_dia = 600
    port_len = 400
    px = mag_tank_len - 800
    py = mag_tank_width
    pz = 500
    
    cyl_out = Part.makeCylinder(port_dia/2 + 100, port_len)
    cyl_out.rotate(App.Vector(0,0,0), App.Vector(1,0,0), -90)
    cyl_out.translate(App.Vector(px, py, pz))
    
    cyl_hole = Part.makeCylinder(port_dia/2, port_len + 100)
    cyl_hole.rotate(App.Vector(0,0,0), App.Vector(1,0,0), -90)
    cyl_hole.translate(App.Vector(px, py - 50, pz))
    
    port_shape = cyl_out.cut(cyl_hole)
    
    # Rings (Scaled 10x: Torus 2->20, spacing 10->100)
    for i in range(3):
        ring = Part.makeTorus(port_dia/2, 20)
        ring.rotate(App.Vector(0,0,0), App.Vector(1,0,0), 90)
        ring.translate(App.Vector(px, py + 100 + (i*100), pz))
        port_shape = port_shape.fuse(ring)
        
    port_shape.translate(App.Vector(offset[0], offset[1], offset[2]))
    obj_port = doc.addObject("Part::Feature", "OutletPort")
    obj_port.Shape = port_shape
    obj_port.ViewObject.ShapeColor = mag_col_grey_paint

    # --- F. MOUNTING FEET (Scaled 10x: 40->400, 10->100, hole 6->60) ---
    foot_sz = 400
    coords = [
        (0, -mag_side_box_width), 
        (mag_tank_len - foot_sz, -mag_side_box_width),
        (0, mag_tank_width),
        (mag_tank_len - foot_sz, mag_tank_width)
    ]
    
    for i, (fx, fy) in enumerate(coords):
        foot = Part.makeBox(foot_sz, foot_sz, 100)
        hole = Part.makeCylinder(60, 200)
        hole.translate(App.Vector(foot_sz/2, foot_sz/2, 0))
        foot = foot.cut(hole)
        foot.translate(App.Vector(fx + offset[0], fy + offset[1], offset[2]))
        
        obj_f = doc.addObject("Part::Feature", f"Foot_{i}")
        obj_f.Shape = foot
        obj_f.ViewObject.ShapeColor = mag_col_grey_paint



def build_ball_mill(offset=(0, 0, 0)):
    doc = ensure_document()
    
    # --- A. BASE FRAME STRUCTURE ---
    mill_beam_thickness = 200.0
    
    make_box(doc, "BM_BaseBeam_Left", ballmill_base_frame_len, mill_beam_thickness, mill_beam_thickness, 
             -ballmill_base_frame_len/2, -ballmill_base_frame_width/2, 0, ballmill_color_foundation, offset)
    
    make_box(doc, "BM_BaseBeam_Right", ballmill_base_frame_len, mill_beam_thickness, mill_beam_thickness, 
             -ballmill_base_frame_len/2, ballmill_base_frame_width/2 - mill_beam_thickness, 0, ballmill_color_foundation, offset)
    
    make_box(doc, "BM_BaseCross_Front", mill_beam_thickness, ballmill_base_frame_width - (2*mill_beam_thickness), mill_beam_thickness, 
             ballmill_base_frame_len/2 - mill_beam_thickness, -ballmill_base_frame_width/2 + mill_beam_thickness, 0, ballmill_color_foundation, offset)
    
    make_box(doc, "BM_BaseCross_Back", mill_beam_thickness, ballmill_base_frame_width - (2*mill_beam_thickness), mill_beam_thickness, 
             -ballmill_base_frame_len/2, -ballmill_base_frame_width/2 + mill_beam_thickness, 0, ballmill_color_foundation, offset)
    
    # --- B. SUPPORT PEDESTALS ---
    mill_pedestal_len = 400.0
    mill_ped_height = ballmill_rotation_axis_height - 400.0
    mill_ped_x_pos = ballmill_base_frame_len/2 - 400.0
    
    # Feed/Gear Side Pedestal
    make_box(doc, "BM_Pedestal_Feed", mill_pedestal_len, ballmill_base_frame_width, mill_ped_height, 
             mill_ped_x_pos, -ballmill_base_frame_width/2, mill_beam_thickness, ballmill_color_primary, offset)
    make_box(doc, "BM_Bearing_Housing_Feed", 500, 1000, 500, 
             mill_ped_x_pos - 50, -500, mill_beam_thickness + mill_ped_height, ballmill_color_primary, offset)
    
    # Discharge Side Pedestal
    mill_tail_x = -ballmill_base_frame_len/2 + 200.0
    make_box(doc, "BM_Pedestal_Discharge", mill_pedestal_len, ballmill_base_frame_width, mill_ped_height, 
             mill_tail_x, -ballmill_base_frame_width/2, mill_beam_thickness, ballmill_color_primary, offset)
    make_box(doc, "BM_Bearing_Housing_Discharge", 500, 1000, 500, 
             mill_tail_x - 50, -500, mill_beam_thickness + mill_ped_height, ballmill_color_primary, offset)

    # --- C. REVOLVING DRUM ASSEMBLY ---
    # Drum Shell
    drum_shell = Part.makeCylinder(ballmill_drum_diameter/2, ballmill_drum_length)
    drum_shell.rotate(App.Vector(0,0,0), App.Vector(0,1,0), 90)
    drum_shell.translate(App.Vector(-ballmill_drum_length/2 + offset[0], 0 + offset[1], ballmill_rotation_axis_height + offset[2]))
    
    obj_shell = doc.addObject("Part::Feature", "BM_Drum_Shell")
    obj_shell.Shape = drum_shell
    obj_shell.ViewObject.ShapeColor = ballmill_color_primary
    
    # Shell End Flanges
    mill_flange_width = 80.0
    mill_flange_dia = ballmill_drum_diameter + 100.0
    make_cylinder(doc, "BM_Flange_A", mill_flange_dia/2, mill_flange_width, 
                  ballmill_drum_length/2, 0, ballmill_rotation_axis_height, ballmill_color_primary, offset, axis=App.Vector(1,0,0))
    make_cylinder(doc, "BM_Flange_B", mill_flange_dia/2, mill_flange_width, 
                  -ballmill_drum_length/2 - mill_flange_width, 0, ballmill_rotation_axis_height, ballmill_color_primary, offset, axis=App.Vector(1,0,0))
    
    # End Cone Sections
    mill_cone_length = 400.0
    mill_trunnion_dia = 500.0
    
    # Forward Cone
    mill_cone_1 = Part.makeCone(mill_flange_dia/2, mill_trunnion_dia/2, mill_cone_length)
    mill_cone_1.rotate(App.Vector(0,0,0), App.Vector(0,1,0), 90)
    mill_cone_1.translate(App.Vector(ballmill_drum_length/2 + mill_flange_width + offset[0], offset[1], ballmill_rotation_axis_height + offset[2]))
    obj_c1 = doc.addObject("Part::Feature", "BM_Cone_Forward")
    obj_c1.Shape = mill_cone_1
    obj_c1.ViewObject.ShapeColor = ballmill_color_primary
    
    # Rear Cone
    mill_cone_2 = Part.makeCone(mill_flange_dia/2, mill_trunnion_dia/2, mill_cone_length)
    mill_cone_2.rotate(App.Vector(0,0,0), App.Vector(0,1,0), -90)
    mill_cone_2.translate(App.Vector(-ballmill_drum_length/2 - mill_flange_width + offset[0], offset[1], ballmill_rotation_axis_height + offset[2]))
    obj_c2 = doc.addObject("Part::Feature", "BM_Cone_Rear")
    obj_c2.Shape = mill_cone_2
    obj_c2.ViewObject.ShapeColor = ballmill_color_primary
    
    # Supporting Trunnions
    make_cylinder(doc, "BM_Trunnion_Feed", mill_trunnion_dia/2 - 50, 400, 
                  ballmill_drum_length/2 + mill_flange_width + mill_cone_length, 0, ballmill_rotation_axis_height, ballmill_color_primary, offset, axis=App.Vector(1,0,0))
    make_cylinder(doc, "BM_Trunnion_Discharge", mill_trunnion_dia/2 - 50, 400, 
                  -ballmill_drum_length/2 - mill_flange_width - mill_cone_length - 400, 0, ballmill_rotation_axis_height, ballmill_color_primary, offset, axis=App.Vector(1,0,0))

    # --- D. DRIVE GIRTH GEAR ---
    mill_gear_x_pos = (ballmill_drum_length/2) - 300
    mill_gear_base = Part.makeCylinder(ballmill_girth_gear_dia/2, ballmill_girth_gear_width)
    mill_gear_base.rotate(App.Vector(0,0,0), App.Vector(0,1,0), 90)
    mill_gear_base.translate(App.Vector(mill_gear_x_pos + offset[0], offset[1], ballmill_rotation_axis_height + offset[2]))
    
    obj_gear = doc.addObject("Part::Feature", "BM_Girth_Gear_Base")
    obj_gear.Shape = mill_gear_base
    obj_gear.ViewObject.ShapeColor = ballmill_color_primary
    
    # Gear Teeth Modeling
    mill_tooth_qty = 60
    mill_tooth_h, mill_tooth_w = 60.0, 40.0
    mill_teeth_list = []
    for i in range(mill_tooth_qty):
        tooth_angle = (360.0 / mill_tooth_qty) * i
        mill_t_shape = Part.makeBox(ballmill_girth_gear_width, mill_tooth_w, mill_tooth_h)
        mill_t_shape.translate(App.Vector(0, -mill_tooth_w/2, -mill_tooth_h/2))
        mill_t_shape.translate(App.Vector(0, 0, ballmill_girth_gear_dia/2))
        mill_t_shape.rotate(App.Vector(0,0,0), App.Vector(1,0,0), tooth_angle)
        mill_t_shape.translate(App.Vector(mill_gear_x_pos + offset[0], offset[1], ballmill_rotation_axis_height + offset[2]))
        mill_teeth_list.append(mill_t_shape)
    
    obj_teeth = doc.addObject("Part::Feature", "BM_Gear_Teeth")
    obj_teeth.Shape = Part.makeCompound(mill_teeth_list)
    obj_teeth.ViewObject.ShapeColor = ballmill_color_gears

    # --- E. LINER FASTENERS (BOLTS) ---
    mill_row_qty, mill_linear_qty = 12, 8
    mill_bolt_pitch = ballmill_drum_length / (mill_linear_qty + 1)
    mill_bolts_list = []
    for r in range(mill_row_qty):
        bolt_angle = (360.0 / mill_row_qty) * r
        for l in range(mill_linear_qty):
            bolt_x = -ballmill_drum_length/2 + (l + 1) * mill_bolt_pitch
            if abs(bolt_x - mill_gear_x_pos) < 200: continue
            mill_bolt = Part.makeCone(15, 10, 25)
            mill_bolt.translate(App.Vector(0, 0, ballmill_drum_diameter/2))
            mill_bolt.rotate(App.Vector(0,0,0), App.Vector(1,0,0), bolt_angle)
            mill_bolt.translate(App.Vector(bolt_x + offset[0], offset[1], ballmill_rotation_axis_height + offset[2]))
            mill_bolts_list.append(mill_bolt)
            
    obj_fasteners = doc.addObject("Part::Feature", "BM_Liner_Fasteners")
    obj_fasteners.Shape = Part.makeCompound(mill_bolts_list)
    obj_fasteners.ViewObject.ShapeColor = ballmill_color_components

    # --- F. TRUNNION BEARING CAPS ---
    mill_cap_radius, mill_cap_thick = 300.0, 50.0
    mill_cap_x_pos = ballmill_drum_length/2 + mill_flange_width + mill_cone_length + 400.0
    
    mill_cap_main = Part.makeCylinder(mill_cap_radius, mill_cap_thick)
    mill_cap_main.rotate(App.Vector(0,0,0), App.Vector(0,1,0), 90)
    
    mill_cap_bore = Part.makeCylinder(150, mill_cap_thick + 10)
    mill_cap_bore.rotate(App.Vector(0,0,0), App.Vector(0,1,0), 90)
    
    mill_cap_final = mill_cap_main.cut(mill_cap_bore)
    mill_cap_final.translate(App.Vector(mill_cap_x_pos + offset[0], offset[1], ballmill_rotation_axis_height + offset[2]))
    
    obj_cap = doc.addObject("Part::Feature", "BM_Bearing_Seal_Cap")
    obj_cap.Shape = mill_cap_final
    obj_cap.ViewObject.ShapeColor = ballmill_color_primary
    
    for i in range(8):
        bolt_circ_angle = (360/8) * i
        mill_arc = math.radians(bolt_circ_angle)
        mill_cy = 220 * math.cos(mill_arc)
        mill_cz = 220 * math.sin(mill_arc) + ballmill_rotation_axis_height
        make_cylinder(doc, f"BM_CapBolt_{i}", 15, 30, mill_cap_x_pos + mill_cap_thick, mill_cy, mill_cz, 
                      ballmill_color_components, offset, axis=App.Vector(1,0,0))



def build_trommel(offset=(0, 0, 0)):
    doc = ensure_document()
    # Height of the drum center
    trommel_z_axis = trommel_support_leg_height + (trommel_drum_dia/2) + 200
    
    # --- A. THE DRUM ASSEMBLY ---
    # Screen Mesh (Manual cut for thickness, then translate by offset)
    outer_cyl = Part.makeCylinder(trommel_drum_dia/2, trommel_drum_len)
    inner_cyl = Part.makeCylinder(trommel_drum_dia/2 - 20, trommel_drum_len)
    mesh_shape = outer_cyl.cut(inner_cyl)
    mesh_shape.rotate(App.Vector(0,0,0), App.Vector(0,1,0), 90)
    mesh_shape.translate(App.Vector(offset[0], offset[1], trommel_z_axis + offset[2]))
    
    obj_mesh = doc.addObject("Part::Feature", "Trommel_Mesh")
    obj_mesh.Shape = mesh_shape
    obj_mesh.ViewObject.ShapeColor = trommel_col_mesh_red
    obj_mesh.ViewObject.Transparency = 25
    
    # Longitudinal Ribs (Cage)
    num_ribs = 8
    for i in range(num_ribs):
        angle = (360.0 / num_ribs) * i
        rad = math.radians(angle)
        ry = (trommel_drum_dia/2) * math.cos(rad)
        rz = (trommel_drum_dia/2) * math.sin(rad)
        
        make_box(doc, f"Trommel_Rib_{i}", trommel_drum_len, 50, 50, 
                 0, ry, trommel_z_axis + rz - 25, trommel_col_green, offset)
        
    # Drive Tires
    make_cylinder(doc, "Trommel_Tire_F", trommel_drum_dia/2 + trommel_tire_thickness, trommel_tire_width, 
                  400, 0, trommel_z_axis, trommel_col_tire_black, offset, axis=App.Vector(1,0,0))
    make_cylinder(doc, "Trommel_Tire_R", trommel_drum_dia/2 + trommel_tire_thickness, trommel_tire_width, 
                  trommel_drum_len - 400 - trommel_tire_width, 0, trommel_z_axis, trommel_col_tire_black, offset, axis=App.Vector(1,0,0))

    # --- B. STRUCTURAL BASE ---
    trommel_beam_h, trommel_beam_w = 250, 150
    make_box(doc, "Trommel_MainBeam_L", trommel_drum_len + 400, trommel_beam_w, trommel_beam_h, 
             -200, -(trommel_frame_width/2), trommel_support_leg_height, trommel_col_green, offset)
    make_box(doc, "Trommel_MainBeam_R", trommel_drum_len + 400, trommel_beam_w, trommel_beam_h, 
             -200, (trommel_frame_width/2) - trommel_beam_w, trommel_support_leg_height, trommel_col_green, offset)
    
    # Support Legs
    leg_x_coords = [0, trommel_drum_len/2, trommel_drum_len]
    for i, lx in enumerate(leg_x_coords):
        make_box(doc, f"Trommel_Leg_L_{i}", 200, 200, trommel_support_leg_height, lx, -(trommel_frame_width/2)-25, 0, trommel_col_green, offset)
        make_box(doc, f"Trommel_Leg_R_{i}", 200, 200, trommel_support_leg_height, lx, (trommel_frame_width/2)-175, 0, trommel_col_green, offset)
        make_box(doc, f"Trommel_CrossBrace_{i}", 200, trommel_frame_width, 100, lx, -trommel_frame_width/2, 200, trommel_col_green, offset)

    # --- C. FEED HOPPER WALLS ---
    wall_l = trommel_drum_len - 200
    # Left Angled Wall
    make_box(doc, "Trommel_Hopper_Wall_L", wall_l, 20, trommel_hopper_wall_height, 
             100, -trommel_frame_width/2 + 200, trommel_support_leg_height + 200, trommel_col_green, offset, 
             rotation_angle=-30, rotation_axis=App.Vector(1,0,0))
    # Right Angled Wall
    make_box(doc, "Trommel_Hopper_Wall_R", wall_l, 20, trommel_hopper_wall_height, 
             100, trommel_frame_width/2 - 200, trommel_support_leg_height + 200, trommel_col_green, offset, 
             rotation_angle=30, rotation_axis=App.Vector(1,0,0))

    # --- D. DRIVE SYSTEM ---
    shaft_y_pos = trommel_frame_width/2 + 100
    shaft_z_pos = trommel_support_leg_height + 300
    make_cylinder(doc, "Trommel_DriveShaft", 40, trommel_drum_len, 0, shaft_y_pos, shaft_z_pos, trommel_col_drive_shaft, offset, axis=App.Vector(1,0,0))
    
    # Drive Wheels (That contact the tires)
    make_cylinder(doc, f"Trommel_DriveWheel_F", 150, trommel_tire_width, 400, shaft_y_pos-150, shaft_z_pos, trommel_col_tire_black, offset, axis=App.Vector(1,0,0))
    make_cylinder(doc, f"Trommel_DriveWheel_R", 150, trommel_tire_width, trommel_drum_len - 400 - trommel_tire_width, shaft_y_pos-150, shaft_z_pos, trommel_col_tire_black, offset, axis=App.Vector(1,0,0))
    
    # Motor & Housing
    make_cylinder(doc, "Trommel_Motor", 125, 450, -450, shaft_y_pos, shaft_z_pos, trommel_col_motor_blue, offset, axis=App.Vector(1,0,0))
    make_box(doc, "Trommel_Guard", 150, 200, 200, -50, shaft_y_pos-100, shaft_z_pos-100, trommel_col_green, offset)



def build_decline_conveyor(offset=(0, 0, 0)):
    doc = ensure_document()
    rad = math.radians(dec_decline_angle)
    
    # --- GEOMETRY CALCULATIONS ---
    # Knee Point (End of high flat, Start of decline)
    p1_x = dec_high_flat_len
    p1_z = dec_start_height
    
    # Elbow Point (End of decline, Start of low flat)
    p2_x = p1_x + (dec_slope_len * math.cos(rad))
    p2_z = p1_z - (dec_slope_len * math.sin(rad)) # Descending (Z decreases)
    
    # End Point
    p3_x = p2_x + dec_low_flat_len
    p3_z = p2_z

    # --- A. FRAME CHANNELS ---
    # 1. High Section (Top)
    make_box(doc, "DEC_Frame_High_L", dec_high_flat_len, 40, dec_rail_h, 0, 0, p1_z - dec_rail_h, dec_col_frame_grey, offset)
    make_box(doc, "DEC_Frame_High_R", dec_high_flat_len, 40, dec_rail_h, 0, dec_frame_width-40, p1_z - dec_rail_h, dec_col_frame_grey, offset)
    
    # 2. Decline Section (Sloping Down)
    # To rotate DOWN, we use a positive angle around Y but the math logic places it correctly
    make_box(doc, "DEC_Frame_Slope_L", dec_slope_len, 40, dec_rail_h, p1_x, 0, p1_z - dec_rail_h, dec_col_frame_grey, offset, 
             rotation_angle=dec_decline_angle, rotation_axis=App.Vector(0,1,0))
    make_box(doc, "DEC_Frame_Slope_R", dec_slope_len, 40, dec_rail_h, p1_x, dec_frame_width-40, p1_z - dec_rail_h, dec_col_frame_grey, offset, 
             rotation_angle=dec_decline_angle, rotation_axis=App.Vector(0,1,0))
             
    # 3. Low Section (Bottom)
    make_box(doc, "DEC_Frame_Low_L", dec_low_flat_len, 40, dec_rail_h, p2_x, 0, p2_z - dec_rail_h, dec_col_frame_grey, offset)
    make_box(doc, "DEC_Frame_Low_R", dec_low_flat_len, 40, dec_rail_h, p2_x, dec_frame_width-40, p2_z - dec_rail_h, dec_col_frame_grey, offset)

    # --- B. BELT & CLEATS ---
    belt_y = (dec_frame_width - dec_belt_width) / 2
    
    # High Belt
    make_box(doc, "DEC_Belt_High", dec_high_flat_len, dec_belt_width, 10, 0, belt_y, p1_z, dec_col_belt_blue, offset)
    # Slope Belt
    make_box(doc, "DEC_Belt_Slope", dec_slope_len, dec_belt_width, 10, p1_x, belt_y, p1_z, dec_col_belt_blue, offset, 
             rotation_angle=dec_decline_angle, rotation_axis=App.Vector(0,1,0))
    # Low Belt
    make_box(doc, "DEC_Belt_Low", dec_low_flat_len, dec_belt_width, 10, p2_x, belt_y, p2_z, dec_col_belt_blue, offset)

    # Cleats (Pockets to prevent material sliding down)
    num_cleats = 15
    for i in range(num_cleats):
        dist = (dec_slope_len / num_cleats) * i
        cx = p1_x + (dist * math.cos(rad))
        cz = p1_z - (dist * math.sin(rad)) + 10
        make_box(doc, f"DEC_Cleat_{i}", 20, dec_belt_width, 50, cx, belt_y, cz, dec_col_belt_blue, offset,
                 rotation_angle=dec_decline_angle, rotation_axis=App.Vector(0,1,0))

    # --- C. SUPPORT LEGS ---
    leg_dim = 80.0
    
    # High Legs (Tallest)
    make_box(doc, "DEC_Leg_High_L", leg_dim, leg_dim, p1_z - dec_rail_h, 200, 0, 0, dec_col_leg_dark, offset)
    make_box(doc, "DEC_Leg_High_R", leg_dim, leg_dim, p1_z - dec_rail_h, 200, dec_frame_width - leg_dim, 0, dec_col_leg_dark, offset)
    
    # Mid Legs (Under Slope)
    mid_x = p1_x + (p2_x - p1_x)/2
    mid_z = p1_z - (p1_z - p2_z)/2
    make_box(doc, "DEC_Leg_Mid_L", leg_dim, leg_dim, mid_z - dec_rail_h, mid_x, 0, 0, dec_col_leg_dark, offset)
    make_box(doc, "DEC_Leg_Mid_R", leg_dim, leg_dim, mid_z - dec_rail_h, mid_x, dec_frame_width - leg_dim, 0, dec_col_leg_dark, offset)
    
    # Low Legs (Shortest)
    make_box(doc, "DEC_Leg_Low_L", leg_dim, leg_dim, p2_z - dec_rail_h, p3_x - 400, 0, 0, dec_col_leg_dark, offset)
    make_box(doc, "DEC_Leg_Low_R", leg_dim, leg_dim, p2_z - dec_rail_h, p3_x - 400, dec_frame_width - leg_dim, 0, dec_col_leg_dark, offset)

    # --- D. END COMPONENTS ---
    # Intake Hopper at the TOP
    make_box(doc, "DEC_Intake_Hopper", 1000, dec_frame_width + 100, 500, 100, -50, p1_z, dec_col_frame_grey, offset)
    
    # Pulleys (Tail at top, Head at bottom)
    make_cylinder(doc, "DEC_Pulley_Top", 120, dec_frame_width + 40, 0, -20, p1_z - 120, dec_col_roller_silver, offset, axis=App.Vector(0,1,0))
    make_cylinder(doc, "DEC_Pulley_Bot", 120, dec_frame_width + 40, p3_x, -20, p3_z - 120, dec_col_roller_silver, offset, axis=App.Vector(0,1,0))


def build_centrifugal_concentrator(doc, offset=(0,0,0)):
    """
    Builds a dual-unit Centrifugal Concentrator at the specified numerical offset.
    """
    
    # We build two units side by side
    for unit_idx in [0, 1]:
        # Center X for this unit relative to the offset
        local_cx = unit_idx * centri_module_gap
        
        # --- A. MAIN DRUM BODY ---
        drum_z_start = centri_cradle_h - 200
        
        # 1. Main Bowl/Drum
        make_cylinder(doc, f"Centri_Drum_{unit_idx}", centri_drum_diameter/2, centri_drum_h, 
                      local_cx, 0, drum_z_start, centri_col_main_blue, offset)
        
        # 2. Top Rim Flange
        make_cylinder(doc, f"Centri_Rim_{unit_idx}", centri_drum_diameter/2 + 40, 40, 
                      local_cx, 0, drum_z_start + centri_drum_h - 40, centri_col_main_blue, offset)
        
        # 3. Bolts on Rim
        num_bolts = 12
        for i in range(num_bolts):
            ang = (360.0 / num_bolts) * i
            rad = math.radians(ang)
            bx = local_cx + (centri_drum_diameter/2 + 20) * math.cos(rad)
            by = (centri_drum_diameter/2 + 20) * math.sin(rad)
            bz = drum_z_start + centri_drum_h - 10
            make_cylinder(doc, f"Centri_Bolt_{unit_idx}_{i}", centri_bolt_r, 25, bx, by, bz, centri_col_bolt_silver, offset)

        # 4. Discharge Spouts
        spout_z = drum_z_start + 300
        # Outer Pipe
        make_cylinder(doc, f"Centri_Spout_Out_{unit_idx}", centri_spout_dia/2, 300, 
                      local_cx + centri_drum_diameter/2 - 50, 0, spout_z, centri_col_main_blue, offset, axis=App.Vector(1,0,0))
        # Inner Liner (Simulating the red interior)
        make_cylinder(doc, f"Centri_Spout_In_{unit_idx}", centri_spout_dia/2 - 10, 310, 
                      local_cx + centri_drum_diameter/2 - 50, 0, spout_z, centri_col_liner_maroon, offset, axis=App.Vector(1,0,0))

        # --- B. SUPPORT FRAME ---
        # Left Support Plate
        make_box(doc, f"Centri_Frame_L_{unit_idx}", 100, centri_cradle_w, centri_cradle_h, 
                 local_cx - centri_drum_diameter/2 - 100, -centri_cradle_w/2, 0, centri_col_main_blue, offset)
        
        # Right Support Plate
        make_box(doc, f"Centri_Frame_R_{unit_idx}", 100, centri_cradle_w, centri_cradle_h, 
                 local_cx + centri_drum_diameter/2, -centri_cradle_w/2, 0, centri_col_main_blue, offset)
        
        # Bottom Cross Beams
        make_box(doc, f"Centri_Base_F_{unit_idx}", centri_drum_diameter + 200, 100, 100, 
                 local_cx - centri_drum_diameter/2 - 100, -centri_cradle_w/2, 0, centri_col_main_blue, offset)
        make_box(doc, f"Centri_Base_B_{unit_idx}", centri_drum_diameter + 200, 100, 100, 
                 local_cx - centri_drum_diameter/2 - 100, centri_cradle_w/2 - 100, 0, centri_col_main_blue, offset)

        # Hydraulic Tilt Cylinder
        make_cylinder(doc, f"Centri_Hydraulic_{unit_idx}", 60, 500, 
                      local_cx - centri_drum_diameter/2 - 150, centri_cradle_w/2 + 20, 400, 
                      centri_col_dark_steel, offset, axis=App.Vector(0,0,1))

        # --- C. FEED HOSES ---
        # Vertical Riser
        make_cylinder(doc, f"Centri_Hose_Rise_{unit_idx}", centri_hose_radius, 800, 
                      local_cx, centri_cradle_w/2 + 200, drum_z_start, centri_col_hose_charcoal, offset)
        
        # Feed Arch (U-bend into center)
        # Using Part.makeTorus for the arch but applying the offset translation manually
        arch_z = drum_z_start + 800
        arch_y = centri_cradle_w/2 + 200 - centri_arch_radius
        
        arch_shape = Part.makeTorus(centri_arch_radius, centri_hose_radius, App.Vector(0,0,0), App.Vector(0,0,1), 0, 180)
        arch_shape.rotate(App.Vector(0,0,0), App.Vector(1,0,0), 90) # Stand upright
        arch_shape.rotate(App.Vector(0,0,0), App.Vector(0,0,1), 90) # Orient toward center
        arch_shape.translate(App.Vector(local_cx + offset[0], arch_y + offset[1], arch_z + offset[2]))
        
        obj_arch = doc.addObject("Part::Feature", f"Centri_Hose_Arch_{unit_idx}")
        obj_arch.Shape = arch_shape
        obj_arch.ViewObject.ShapeColor = centri_col_hose_charcoal

    # --- D. MANIFOLD SYSTEM ---
    # Horizontal Main Line (Across the front)
    manifold_y = -centri_cradle_w/2 - 150
    make_cylinder(doc, "Centri_Manifold_Main", 50, centri_module_gap + centri_drum_diameter, 
                  -centri_drum_diameter/2, manifold_y, 400, centri_col_main_blue, offset, axis=App.Vector(1,0,0))
    
    # Connection Ports
    for i in [0, 1]:
        make_cylinder(doc, f"Centri_Manifold_Conn_{i}", 50, 150, 
                      i * centri_module_gap, manifold_y, 400, centri_col_main_blue, offset, axis=App.Vector(0,1,0))




# --- 1. Flanged Pipe (Bolted sections using cylinders) ---
# Now accepts explicit start_p and end_p vectors from the layout
def create_jointed_pipe(doc, name, start_p, end_p, pipe_r, joint_r, color, offset=(0,0,0)):
    # Calculate Global Positions by applying offset to the passed coordinates
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

# --- 2. Smooth Duct (Continuous sweep along multiple points) ---
# Now accepts the point list directly from the layout
def create_duct(doc, name, path_points, radius, color, offset=(0,0,0)):
    # Apply offset to all points in the path
    global_points = []
    for p in path_points:
        global_points.append(App.Vector(p.x + offset[0], p.y + offset[1], p.z + offset[2]))
    
    # Create the path wire
    wire = Part.Wire(Part.makePolygon(global_points).Edges)
    # Create profile at the start point
    circle = Part.makeCircle(radius, global_points[0], global_points[1].sub(global_points[0]))
    profile = Part.Wire(circle)
    
    shape = wire.makePipe(profile)
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = shape
    obj.ViewObject.ShapeColor = color
    return obj

# --- 3. Angle Builder: Coordinates are now passed as arguments ---
def build_vessel_bolted_angle(doc, name, p_start, p_elbow, p_end, p_rad, j_rad, color, offset=(0,0,0)):
    # Calls the jointed pipe builder using the coordinates defined in layout
    # Segment 1: Start to Elbow
    create_jointed_pipe(doc, name + "_Seg1", p_start, p_elbow, p_rad, j_rad, color, offset)
    # Segment 2: Elbow to End
    create_jointed_pipe(doc, name + "_Seg2", p_elbow, p_end, p_rad, j_rad, color, offset)






# ==============================================================================
# SMARTPHONE BATTERY GENERATION (FUSED FOR BLENDER) WITH SCALING
# ==============================================================================
def draw_smartphone_battery(doc, offset_coords=(0, 0, 0), scale_factor=1.0):
    """
    Creates a fused smartphone battery. 
    Proportionally scales all details based on scale_factor.
    """
    S = scale_factor  
    battery_parts = []

    # --- COLORS ---
    c_body = (0.15, 0.15, 0.15)
    c_cap = (0.25, 0.25, 0.30)
    c_gold = (0.85, 0.70, 0.20)

    # --- DIMENSIONS (Scaled) ---
    bat_w = 54.0 * S
    bat_l = 85.0 * S
    bat_h = 5.0 * S
    r_edge = bat_h / 2.0
    body_len = 78.0 * S

    # 1. MAIN BODY
    battery_parts.append(make_box(doc, "Main_Core", bat_w - bat_h, body_len, bat_h, r_edge, 7.0 * S, 0, c_body, offset_coords))
    battery_parts.append(make_cylinder(doc, "Edge_L", r_edge, body_len, r_edge, 7.0 * S, r_edge, c_body, offset_coords, axis=App.Vector(0, 1, 0)))
    battery_parts.append(make_cylinder(doc, "Edge_R", r_edge, body_len, bat_w - r_edge, 7.0 * S, r_edge, c_body, offset_coords, axis=App.Vector(0, 1, 0)))

    # 2. BOTTOM CAP
    cap_len = 7.0 * S
    battery_parts.append(make_box(doc, "Cap_Core", bat_w - bat_h, cap_len, bat_h, r_edge, 0, 0, c_cap, offset_coords))
    battery_parts.append(make_cylinder(doc, "Cap_Edge_L", r_edge, cap_len, r_edge, 0, r_edge, c_cap, offset_coords, axis=App.Vector(0, 1, 0)))
    battery_parts.append(make_cylinder(doc, "Cap_Edge_R", r_edge, cap_len, bat_w - r_edge, 0, r_edge, c_cap, offset_coords, axis=App.Vector(0, 1, 0)))

    # 3. CONNECTORS (Scaled Details)
    pad_w = 6.0 * S
    pad_h = 3.0 * S
    pad_gap = 4.0 * S
    start_x = (bat_w / 2) - pad_w - pad_gap

    for i in range(3):
        px = start_x + (i * (pad_w + pad_gap))
        # Slot
        battery_parts.append(make_box(doc, f"Slot_{i}", pad_w, 1 * S, pad_h, px, -0.1 * S, 1 * S, c_body, offset_coords))
        # Gold Contact
        battery_parts.append(make_box(doc, f"Contact_{i}", pad_w - (1 * S), 0.5 * S, pad_h - (1 * S), px + (0.5 * S), -0.2 * S, 1.5 * S, c_gold, offset_coords))

    # --- FUSION STEP ---
    shapes_to_fuse = [obj.Shape for obj in battery_parts]
    fused_shape = reduce(lambda a, b: a.fuse(b), shapes_to_fuse)
    
    # Cleanup temporary parts from the tree
    for obj in battery_parts:
        doc.removeObject(obj.Name)
        
    final_obj = doc.addObject("Part::Feature", "Smartphone_Battery_Fused")
    final_obj.Shape = fused_shape
    final_obj.ViewObject.ShapeColor = c_body 
    
    return final_obj


# ==============================================================================
# MAIN DRAWING FUNCTION: SAMSUNG STYLE BATTERY (FUSED & SCALABLE)
# ==============================================================================

def draw_samsung_battery(doc, offset_coords=(0, 0, 0), scale_factor=1.0):
    
    # --- SCALE FACTOR ---
    S = scale_factor 

    # List to collect the temporary objects created by make_box/make_cylinder
    # We keep track of them so we can delete them after fusion.
    temp_objects = []

    # --- COLORS ---
    c_silver = (0.90, 0.90, 0.90)
    c_black  = (0.05, 0.05, 0.05)
    c_white  = (0.95, 0.95, 0.95)
    c_gold   = (0.85, 0.70, 0.20)
    c_grey   = (0.30, 0.30, 0.30)

    # --- DIMENSIONS (SCALED) ---
    bat_w = 55.0 * S
    bat_l = 70.0 * S
    bat_h = 5.0 * S
    r_corn = 2.0 * S

    # 1. MAIN BODY
    temp_objects.append(make_box(doc, "Body_Core", bat_w - (2 * r_corn), bat_l, bat_h, r_corn, 0, 0, c_silver, offset_coords))
    temp_objects.append(make_cylinder(doc, "Side_L", r_corn, bat_l, r_corn, 0, r_corn, c_silver, offset_coords, axis=App.Vector(0, 1, 0)))
    temp_objects.append(make_cylinder(doc, "Side_R", r_corn, bat_l, bat_w - r_corn, 0, r_corn, c_silver, offset_coords, axis=App.Vector(0, 1, 0)))
    temp_objects.append(make_box(doc, "Body_Fill", bat_w - (2 * r_corn), bat_l, bat_h, r_corn, 0, 0, c_silver, offset_coords))

    # 2. BLACK LABEL
    lbl_w = bat_w - (6.0 * S)
    lbl_l = bat_l - (10.0 * S)
    lbl_x = 3.0 * S
    lbl_y = 5.0 * S
    lbl_z = bat_h + (0.05 * S)
    temp_objects.append(make_box(doc, "Label_Bg", lbl_w, lbl_l, 0.1 * S, lbl_x, lbl_y, bat_h, c_black, offset_coords))

    # 3. CONNECTORS
    pad_w = 4.0 * S
    pad_h = 4.0 * S
    pad_gap = 3.0 * S
    start_x = (bat_w / 2) - (10.0 * S)
    for i in range(4):
        px = start_x + (i * (pad_w + pad_gap))
        temp_objects.append(make_box(doc, f"Pad_Recess_{i}", pad_w, 2 * S, bat_h, px, -0.1 * S, 0, c_black, offset_coords))
        temp_objects.append(make_box(doc, f"Contact_{i}", pad_w - (1 * S), 0.5 * S, bat_h - (2 * S), px + (0.5 * S), -0.2 * S, 1 * S, c_gold, offset_coords))

    # 4. TOP INDICATORS
    circ_y = bat_l - (3.0 * S)
    cx_p = 10 * S
    temp_objects.append(make_cylinder(doc, "Circ_Plus", 2.5 * S, 0.1 * S, cx_p, circ_y, bat_h, c_black, offset_coords))
    temp_objects.append(make_box(doc, "Plus_V", 0.5 * S, 3 * S, 0.2 * S, cx_p - (0.25 * S), circ_y - (1.5 * S), bat_h, c_silver, offset_coords))
    temp_objects.append(make_box(doc, "Plus_H", 3 * S, 0.5 * S, 0.2 * S, cx_p - (1.5 * S), circ_y - (0.25 * S), bat_h, c_silver, offset_coords))

    cx_m = 20 * S
    temp_objects.append(make_cylinder(doc, "Circ_Min", 2.5 * S, 0.1 * S, cx_m, circ_y, bat_h, c_black, offset_coords))
    temp_objects.append(make_box(doc, "Min_H", 3 * S, 0.5 * S, 0.2 * S, cx_m - (1.5 * S), circ_y - (0.25 * S), bat_h, c_silver, offset_coords))

    # 5. SAMSUNG LOGO
    logo_y = lbl_y + lbl_l - (12 * S)
    temp_objects.append(make_box(doc, "S1", 5 * S, 1 * S, 0.1 * S, lbl_x + (5 * S), logo_y + (5 * S), lbl_z, c_white, offset_coords))
    temp_objects.append(make_box(doc, "S2", 1 * S, 3 * S, 0.1 * S, lbl_x + (5 * S), logo_y + (2 * S), lbl_z, c_white, offset_coords))
    temp_objects.append(make_box(doc, "S3", 5 * S, 1 * S, 0.1 * S, lbl_x + (5 * S), logo_y + (2 * S), lbl_z, c_white, offset_coords))
    temp_objects.append(make_box(doc, "S4", 1 * S, 3 * S, 0.1 * S, lbl_x + (9 * S), logo_y - (1 * S), lbl_z, c_white, offset_coords))
    temp_objects.append(make_box(doc, "S5", 5 * S, 1 * S, 0.1 * S, lbl_x + (5 * S), logo_y - (1 * S), lbl_z, c_white, offset_coords))
    for i in range(6):
        bx = lbl_x + (13 * S) + (i * 6 * S)
        temp_objects.append(make_box(doc, f"Letter_{i}", 4 * S, 7 * S, 0.1 * S, bx, logo_y - (1 * S), lbl_z, c_white, offset_coords))
    temp_objects.append(make_box(doc, "NFC_Txt", 25 * S, 1 * S, 0.1 * S, lbl_x + (5 * S), logo_y - (4 * S), lbl_z, c_white, offset_coords))

    # 6. SPECS TEXT
    spec_y = logo_y - (10 * S)
    temp_objects.append(make_box(doc, "Made_Txt", 40 * S, 3 * S, 0.1 * S, lbl_x + (2 * S), spec_y, lbl_z, c_grey, offset_coords))
    temp_objects.append(make_box(doc, "Line_1", lbl_w - (4 * S), 0.5 * S, 0.1 * S, lbl_x + (2 * S), spec_y - (2 * S), lbl_z, c_white, offset_coords))
    temp_objects.append(make_box(doc, "Line_2", lbl_w - (4 * S), 0.5 * S, 0.1 * S, lbl_x + (2 * S), spec_y - (3 * S), lbl_z, c_white, offset_coords))
    volt_y = spec_y - (8 * S)
    for i in range(4):
        temp_objects.append(make_box(doc, f"Spec_Line_{i}", lbl_w - (6 * S), 1.2 * S, 0.1 * S, lbl_x + (3 * S), volt_y - (i * 2.5 * S), lbl_z, c_grey, offset_coords))

    # 7. ICONS
    icon_y = 10 * S
    ce_x = lbl_x + (5 * S)
    temp_objects.append(make_cylinder(doc, "CE_C", 4 * S, 0.1 * S, ce_x, icon_y + (5 * S), lbl_z, c_white, offset_coords))
    temp_objects.append(make_cylinder(doc, "CE_C_In", 3 * S, 0.2 * S, ce_x, icon_y + (5 * S), lbl_z, c_black, offset_coords))
    temp_objects.append(make_box(doc, "CE_Cut", 4 * S, 6 * S, 0.3 * S, ce_x + (1 * S), icon_y + (2 * S), lbl_z, c_black, offset_coords))
    rec_x = lbl_x + (15 * S)
    temp_objects.append(make_box(doc, "Rec_Tri", 6 * S, 5 * S, 0.1 * S, rec_x, icon_y + (2 * S), lbl_z, c_white, offset_coords))
    temp_objects.append(make_box(doc, "Rec_In", 4 * S, 3 * S, 0.2 * S, rec_x + (1 * S), icon_y + (3 * S), lbl_z, c_black, offset_coords))
    nom_x = lbl_x + (25 * S)
    temp_objects.append(make_box(doc, "NOM_Txt", 8 * S, 3 * S, 0.1 * S, nom_x, icon_y + (3 * S), lbl_z, c_white, offset_coords))
    bin_x = lbl_w - (5 * S)
    temp_objects.append(make_box(doc, "Bin_Body", 8 * S, 10 * S, 0.1 * S, bin_x, icon_y + (2 * S), lbl_z, c_white, offset_coords))
    temp_objects.append(make_box(doc, "Bin_In", 6 * S, 8 * S, 0.2 * S, bin_x + (1 * S), icon_y + (3 * S), lbl_z, c_black, offset_coords))
    temp_objects.append(make_box(doc, "X1", 12 * S, 1 * S, 0.2 * S, bin_x - (2 * S), icon_y + (6 * S), lbl_z, c_white, offset_coords, rotation_angle=45, rotation_axis=App.Vector(0, 0, 1)))
    temp_objects.append(make_box(doc, "X2", 12 * S, 1 * S, 0.2 * S, bin_x - (2 * S), icon_y + (6 * S), lbl_z, c_white, offset_coords, rotation_angle=-45, rotation_axis=App.Vector(0, 0, 1)))

    # 8. BOTTOM SAFETY SQUARES
    sq_y = lbl_y + (2 * S)
    sq_size = 6 * S
    for i in range(4):
        sx = lbl_x + (2 * S) + (i * (sq_size + (2 * S)))
        temp_objects.append(make_box(doc, f"Safe_Frame_{i}", sq_size, sq_size, 0.1 * S, sx, sq_y, lbl_z, c_white, offset_coords))
        temp_objects.append(make_box(doc, f"Safe_In_{i}", sq_size - (1 * S), sq_size - (1 * S), 0.2 * S, sx + (0.5 * S), sq_y + (0.5 * S), lbl_z, c_black, offset_coords))
        temp_objects.append(make_box(doc, f"Safe_Icon_{i}", sq_size - (3 * S), sq_size - (3 * S), 0.3 * S, sx + (1.5 * S), sq_y + (1.5 * S), lbl_z, c_white, offset_coords))

    # --- FUSION LOGIC ---
    if temp_objects:
        # 1. Extract the raw shapes from the FreeCAD objects
        shapes_to_fuse = [obj.Shape for obj in temp_objects]
        
        # 2. Perform boolean fusion (Union) on all shapes iteratively
        fused_shape = shapes_to_fuse[0]
        for s in shapes_to_fuse[1:]:
            fused_shape = fused_shape.fuse(s)
        
        # 3. Clean up: Remove the temporary individual parts from the document
        for obj in temp_objects:
            doc.removeObject(obj.Name)
            
        # 4. Create the final single Fused Object
        final_obj = doc.addObject("Part::Feature", "Samsung_Battery_Combined")
        final_obj.Shape = fused_shape
        final_obj.ViewObject.ShapeColor = c_silver # Uniform color for GLTF export
        
        return final_obj

 
# ==============================================================================
# MAIN DRAWING FUNCTION: CAMERON SINO STYLE LiPo BATTERY (FUSED & SCALABLE)
# ==============================================================================

def draw_lipo_battery(doc, offset_coords=(0, 0, 0), scale_factor=1.0):
    
    # --- SCALE FACTOR ---
    S = scale_factor

    all_shapes = []  # List to store shapes for fusion

    # --- COLORS ---
    c_body  = (0.10, 0.10, 0.10)
    c_label = (0.95, 0.95, 0.95)
    c_gold  = (0.85, 0.70, 0.20)
    c_blue  = (0.10, 0.20, 0.80)
    c_text  = (0.05, 0.05, 0.05)
    c_red   = (0.80, 0.10, 0.10)

    # --- DIMENSIONS (Scaled) ---
    bat_w = 60.0 * S
    bat_l = 75.0 * S
    bat_h = 5.0 * S
    r_edge = 2.5 * S

    # 1. MAIN BODY
    body_len = bat_l - (4.0 * S)

    all_shapes.append(make_box(
        doc, "Core",
        bat_w - (2 * r_edge), body_len, bat_h,
        r_edge, 4.0 * S, 0,
        c_body, offset_coords
    ))

    all_shapes.append(make_cylinder(
        doc, "Edge_L",
        r_edge, body_len,
        r_edge, 4.0 * S, r_edge,
        c_body, offset_coords,
        axis=App.Vector(0, 1, 0)
    ))

    all_shapes.append(make_cylinder(
        doc, "Edge_R",
        r_edge, body_len,
        bat_w - r_edge, 4.0 * S, r_edge,
        c_body, offset_coords,
        axis=App.Vector(0, 1, 0)
    ))

    # 2. TOP CAP
    cap_len = 4.0 * S
    all_shapes.append(make_box(
        doc, "Cap",
        bat_w, cap_len, bat_h,
        0, 0, 0,
        c_body, offset_coords
    ))

    # 3. CONTACTS
    pad_w = 5.0 * S
    pad_h = 3.0 * S
    pad_gap = 4.0 * S
    start_x = (bat_w / 2) - (10.0 * S)

    for i in range(3):
        px = start_x + (i * (pad_w + pad_gap))
        all_shapes.append(make_box(
            doc, f"Pad_Slot_{i}",
            pad_w, 0.5 * S, pad_h + (1 * S),
            px, -0.1 * S, 1 * S,
            c_body, offset_coords
        ))
        all_shapes.append(make_box(
            doc, f"Contact_{i}",
            pad_w - (1 * S), 0.2 * S, pad_h,
            px + (0.5 * S), -0.2 * S, 1.5 * S,
            c_gold, offset_coords
        ))

    # 4. LABEL
    z_surf = bat_h + (0.05 * S)
    all_shapes.append(make_box(
        doc, "Label_Bg",
        bat_w - (2 * S), bat_l - (6 * S), 0.1 * S,
        1 * S, 5 * S, bat_h,
        c_label, offset_coords
    ))

    # 5. GRAPHICS & TEXT
    # Logo
    logo_x = 40.0 * S
    logo_y = 10.0 * S
    all_shapes.append(make_cylinder(doc, "Logo_Out", 8 * S, 0.2 * S, logo_x, logo_y + (10 * S), z_surf, c_blue, offset_coords))
    all_shapes.append(make_cylinder(doc, "Logo_In", 7 * S, 0.3 * S, logo_x, logo_y + (10 * S), z_surf, c_label, offset_coords))
    all_shapes.append(make_box(doc, "Logo_Cut", 10 * S, 4 * S, 0.4 * S, logo_x, logo_y + (10 * S), z_surf, c_label, offset_coords))
    all_shapes.append(make_box(doc, "Logo_Text", 20 * S, 2 * S, 0.2 * S, logo_x - (10 * S), logo_y + (18 * S), z_surf, c_blue, offset_coords))

    # Model Info
    info_x = 5.0 * S
    info_y = 10.0 * S
    all_shapes.append(make_box(doc, "Txt_Model", 25 * S, 2 * S, 0.2 * S, info_x, info_y, z_surf, c_text, offset_coords))
    all_shapes.append(make_box(doc, "Txt_Part", 20 * S, 1.5 * S, 0.2 * S, info_x, info_y + (3 * S), z_surf, c_text, offset_coords))
    all_shapes.append(make_box(doc, "Txt_Rating", 25 * S, 1.5 * S, 0.2 * S, info_x, info_y + (6 * S), z_surf, c_text, offset_coords))

    # Caution Block
    caut_y = 25.0 * S
    all_shapes.append(make_box(doc, "Caut_Head", 50 * S, 2 * S, 0.2 * S, 5 * S, caut_y, z_surf, c_text, offset_coords))
    for i in range(5):
        all_shapes.append(make_box(doc, f"Caut_Line_{i}", 45 * S, 1 * S, 0.2 * S, 5 * S, caut_y + (4 * S) + (i * 2.5 * S), z_surf, c_text, offset_coords))

    # Attention Block
    attn_y = 45.0 * S
    all_shapes.append(make_box(doc, "Attn_Head", 50 * S, 2 * S, 0.2 * S, 5 * S, attn_y, z_surf, c_text, offset_coords))
    for i in range(4):
        all_shapes.append(make_box(doc, f"Attn_Line_{i}", 48 * S, 1 * S, 0.2 * S, 5 * S, attn_y + (4 * S) + (i * 2.5 * S), z_surf, c_text, offset_coords))

    # Icons
    icon_x = 35.0 * S
    icon_y = 60.0 * S
    all_shapes.append(make_box(doc, "Bin", 6 * S, 8 * S, 0.2 * S, icon_x, icon_y, z_surf, c_text, offset_coords))
    all_shapes.append(make_box(doc, "Bin_Void", 4 * S, 6 * S, 0.3 * S, icon_x + (1 * S), icon_y + (1 * S), z_surf, c_label, offset_coords))
    all_shapes.append(make_box(doc, "X1", 8 * S, 1 * S, 0.4 * S, icon_x - (1 * S), icon_y + (3 * S), z_surf, c_text, offset_coords, rotation_angle=45))
    all_shapes.append(make_box(doc, "X2", 8 * S, 1 * S, 0.4 * S, icon_x - (1 * S), icon_y + (3 * S), z_surf, c_text, offset_coords, rotation_angle=-45))
    
    ce_x = icon_x + (10 * S)
    all_shapes.append(make_cylinder(doc, "CE_C", 3 * S, 0.2 * S, ce_x, icon_y + (4 * S), z_surf, c_text, offset_coords))
    all_shapes.append(make_cylinder(doc, "CE_C_In", 2.2 * S, 0.3 * S, ce_x, icon_y + (4 * S), z_surf, c_label, offset_coords))
    all_shapes.append(make_box(doc, "CE_Cut", 3 * S, 4 * S, 0.4 * S, ce_x + (1 * S), icon_y + (2 * S), z_surf, c_label, offset_coords))

    # Direction Arrow
    all_shapes.append(make_box(doc, "Big_Arrow_Shaft", 2 * S, 50 * S, 0.2 * S, 2 * S, 10 * S, z_surf, c_text, offset_coords))
    all_shapes.append(make_box(doc, "Big_Arrow_Head_L", 2 * S, 8 * S, 0.2 * S, 2 * S, 10 * S, z_surf, c_text, offset_coords, rotation_angle=45))
    all_shapes.append(make_box(doc, "Big_Arrow_Head_R", 2 * S, 8 * S, 0.2 * S, 2 * S, 10 * S, z_surf, c_text, offset_coords, rotation_angle=-45))

    # --- FUSION STEP ---
    if all_shapes:
        # 1. Extract the raw shapes
        shapes_to_fuse = [obj.Shape for obj in all_shapes]
        
        # 2. Perform boolean fusion (Union) iteratively
        fused_shape = shapes_to_fuse[0]
        for s in shapes_to_fuse[1:]:
            fused_shape = fused_shape.fuse(s)
        
        # 3. Clean up temporary objects
        for obj in all_shapes:
            doc.removeObject(obj.Name)
            
        # 4. Create Final Object
        final_obj = doc.addObject("Part::Feature", "LiPo_Battery_Combined")
        final_obj.Shape = fused_shape
        final_obj.ViewObject.ShapeColor = c_body
        
        return final_obj

# ===============================================================================
# MAIN DRAWING FUNCTION: FLAT BATTERY PACK (FUSED & SCALABLE)
# ===============================================================================

def draw_flat_battery_fused(doc, offset_coords=(0, 0, 0), scale_factor=1.0):
    
    # --- SCALE FACTOR ---
    S = scale_factor

    # --- COLORS ---
    c_body = (0.10, 0.10, 0.10)
    c_white = (0.92, 0.92, 0.92)
    c_gold = (0.85, 0.75, 0.40)

    # --- DIMENSIONS (Scaled) ---
    bat_w = 270.0 * S
    bat_d = 120.0 * S
    bat_h = 20.0 * S

    # List to hold created FreeCAD objects temporarily
    battery_parts = []

    # 1. MAIN BODY
    battery_parts.append(make_box(doc, "Main_Body", bat_w, bat_d, bat_h, 0, 0, 0, c_body, offset=offset_coords))
    
    step_d = 15.0 * S
    battery_parts.append(make_box(doc, "Step_Down", bat_w, step_d, bat_h - (5 * S), 0, bat_d, 0, c_body, offset=offset_coords))

    # 2. CONNECTOR
    conn_x = 40.0 * S
    conn_w = 40.0 * S
    battery_parts.append(make_box(doc, "Conn_Housing", conn_w, 5 * S, 8 * S, conn_x, bat_d + step_d, 5 * S, c_body, offset=offset_coords))
    
    for i in range(8):
        px = conn_x + (3 * S) + (i * 4.5 * S)
        battery_parts.append(make_box(doc, f"Pin_{i}", 2 * S, 6 * S, 2 * S, px, bat_d + step_d - (1 * S), 8 * S, c_gold, offset=offset_coords))

    # 3. LOCKING TABS
    tab_w = 20.0 * S
    tab_pos = [60.0 * S, bat_w - (80.0 * S)]
    
    for i, tx in enumerate(tab_pos):
        battery_parts.append(make_box(doc, f"Tab_{i}", tab_w, 5 * S, 8 * S, tx, -5 * S, 5 * S, c_body, offset=offset_coords))
        battery_parts.append(make_box(doc, f"Latch_{i}", 5 * S, 2 * S, 4 * S, tx + (7.5 * S), -7 * S, 7 * S, c_body, offset=offset_coords))

    # 4. TEXT & LABELS
    z_surf = bat_h + (0.1 * S)
    battery_parts.append(make_box(doc, "Txt_Main", 80 * S, 5 * S, 0.1 * S, 20 * S, bat_d - (30 * S), z_surf, c_white, offset=offset_coords))
    battery_parts.append(make_box(doc, "Txt_Rating", 60 * S, 3 * S, 0.1 * S, 20 * S, bat_d - (40 * S), z_surf, c_white, offset=offset_coords))
    battery_parts.append(make_box(doc, "Txt_Model", 30 * S, 4 * S, 0.1 * S, 90 * S, bat_d - (25 * S), z_surf, c_white, offset=offset_coords))

    col_w = 60 * S
    start_x = 130 * S
    for i in range(8):
        ly = bat_d - (30 * S) - (i * 4 * S)
        battery_parts.append(make_box(doc, f"Txt_Col1_{i}", col_w, 1.5 * S, 0.1 * S, start_x, ly, z_surf, c_white, offset=offset_coords))
        battery_parts.append(make_box(doc, f"Txt_Col2_{i}", col_w, 1.5 * S, 0.1 * S, start_x + col_w + (10 * S), ly, z_surf, c_white, offset=offset_coords))

    # 5. ICONS
    icon_y = bat_d - (20 * S)
    tri_x = 140 * S
    battery_parts.append(make_box(doc, "Tri_Base", 12 * S, 2 * S, 0.1 * S, tri_x, icon_y + (35 * S), z_surf, c_white, offset=offset_coords))
    battery_parts.append(make_box(doc, "Tri_L", 12 * S, 2 * S, 0.1 * S, tri_x - (3 * S), icon_y + (40 * S), z_surf, c_white, offset=offset_coords, rotation_angle=60))
    battery_parts.append(make_box(doc, "Tri_R", 12 * S, 2 * S, 0.1 * S, tri_x + (9 * S), icon_y + (40 * S), z_surf, c_white, offset=offset_coords, rotation_angle=-60))

    ce_x = 170 * S
    battery_parts.append(make_cylinder(doc, "CE_C_Out", 5 * S, 0.1 * S, ce_x, icon_y + (45 * S), z_surf, c_white, offset=offset_coords))
    battery_parts.append(make_cylinder(doc, "CE_C_In", 3.5 * S, 0.2 * S, ce_x, icon_y + (45 * S), z_surf, c_body, offset=offset_coords))
    battery_parts.append(make_box(doc, "CE_C_Cut", 5 * S, 6 * S, 0.3 * S, ce_x + (2 * S), icon_y + (42 * S), z_surf, c_body, offset=offset_coords))

    battery_parts.append(make_cylinder(doc, "CE_E_Out", 5 * S, 0.1 * S, ce_x + (12 * S), icon_y + (45 * S), z_surf, c_white, offset=offset_coords))
    battery_parts.append(make_cylinder(doc, "CE_E_In", 3.5 * S, 0.2 * S, ce_x + (12 * S), icon_y + (45 * S), z_surf, c_body, offset=offset_coords))
    battery_parts.append(make_box(doc, "CE_E_Cut", 5 * S, 6 * S, 0.3 * S, ce_x + (14 * S), icon_y + (42 * S), z_surf, c_body, offset=offset_coords))
    battery_parts.append(make_box(doc, "CE_E_Bar", 4 * S, 1.5 * S, 0.1 * S, ce_x + (12 * S), icon_y + (44.5 * S), z_surf, c_white, offset=offset_coords))

    li_x = 200 * S
    battery_parts.append(make_box(doc, "Li_Top", 10 * S, 2 * S, 0.1 * S, li_x, icon_y + (50 * S), z_surf, c_white, offset=offset_coords))
    battery_parts.append(make_box(doc, "Li_R", 10 * S, 2 * S, 0.1 * S, li_x + (6 * S), icon_y + (42 * S), z_surf, c_white, offset=offset_coords, rotation_angle=-60))
    battery_parts.append(make_box(doc, "Li_L", 10 * S, 2 * S, 0.1 * S, li_x - (6 * S), icon_y + (42 * S), z_surf, c_white, offset=offset_coords, rotation_angle=60))
    battery_parts.append(make_box(doc, "Li_Txt", 6 * S, 2 * S, 0.1 * S, li_x - (3 * S), icon_y + (45 * S), z_surf, c_white, offset=offset_coords))

    bin_x = 230 * S
    battery_parts.append(make_box(doc, "Bin_Box", 10 * S, 12 * S, 0.1 * S, bin_x, icon_y + (40 * S), z_surf, c_white, offset=offset_coords))
    battery_parts.append(make_box(doc, "Bin_In", 8 * S, 10 * S, 0.2 * S, bin_x + (1 * S), icon_y + (41 * S), z_surf, c_body, offset=offset_coords))
    battery_parts.append(make_box(doc, "Bin_X1", 14 * S, 1.5 * S, 0.3 * S, bin_x - (2 * S), icon_y + (46 * S), z_surf, c_white, offset=offset_coords, rotation_angle=45))
    battery_parts.append(make_box(doc, "Bin_X2", 14 * S, 1.5 * S, 0.3 * S, bin_x - (2 * S), icon_y + (46 * S), z_surf, c_white, offset=offset_coords, rotation_angle=-45))

    # --- FUSION LOGIC ---
    if battery_parts:
        # 1. Extract the raw shapes
        shapes_to_fuse = [obj.Shape for obj in battery_parts]
        
        # 2. Fuse
        fused_shape = shapes_to_fuse[0]
        for s in shapes_to_fuse[1:]:
            fused_shape = fused_shape.fuse(s)
        
        # 3. Cleanup individual parts
        for obj in battery_parts:
            doc.removeObject(obj.Name)
            
        # 4. Create Final Object
        final_obj = doc.addObject("Part::Feature", "Flat_Battery_Fused")
        final_obj.Shape = fused_shape
        final_obj.ViewObject.ShapeColor = c_body
        
        return final_obj



# ============================================================================== 
# MAIN DRAWING FUNCTION: HP STYLE BATTERY (WITH SCALE FACTOR & FUSION)
# ==============================================================================

def draw_hp_battery(doc, offset_coords=(0, 0, 0), scale_factor=1.0):
    """
    Creates a fused HP-style laptop battery.
    All internal dimensions and positions are multiplied by scale_factor.
    """
    S = scale_factor
    # This list will collect the SHAPES of the temporary objects for the final fusion
    all_shapes = []
    # This list will keep track of the temporary OBJECTS so we can delete them after fusion
    temp_objects = []

    # --- COLORS ---
    c_body = (0.12, 0.12, 0.12)
    c_white = (0.90, 0.90, 0.90)
    c_sticker = (0.95, 0.95, 0.95)
    c_silver = (0.70, 0.70, 0.70)
    c_dark = (0.05, 0.05, 0.05)

    # --- DIMENSIONS (SCALED) ---
    bat_len = 270.0 * S
    spine_r = 11.0 * S

    # 1. SPINE
    spine = make_cylinder(doc, "Spine_Cyl", spine_r, bat_len, 0, 0, spine_r, c_body, offset_coords, axis=App.Vector(1, 0, 0))
    all_shapes.append(spine.Shape)
    temp_objects.append(spine)

    base = make_box(doc, "Base_Plate", bat_len, spine_r * 2, 2 * S, 0, -spine_r, 0, c_body, offset_coords)
    all_shapes.append(base.Shape)
    temp_objects.append(base)

    # 2. CONNECTOR BLOCK
    conn_len = 70.0 * S
    conn_w = 25.0 * S
    conn_h = 16.0 * S
    conn_x = 170.0 * S

    conn_housing = make_box(doc, "Connector_Housing", conn_len, conn_w, conn_h, conn_x, -conn_w, 2 * S, c_body, offset_coords)
    all_shapes.append(conn_housing.Shape)
    temp_objects.append(conn_housing)

    slot_w = 3 * S
    slot_d = 5 * S
    for i in range(8):
        sx = conn_x + (15 * S) + (i * 5 * S)
        slot = make_box(doc, f"Slot_{i}", slot_w, slot_d, 8 * S, sx, -conn_w, 8 * S, c_dark, offset_coords)
        all_shapes.append(slot.Shape)
        temp_objects.append(slot)
        
        if i < 7:
            pin = make_box(doc, f"Pin_{i}", 1 * S, 2 * S, 2 * S, sx + (1 * S), -conn_w + (1 * S), 10 * S, c_silver, offset_coords)
            all_shapes.append(pin.Shape)
            temp_objects.append(pin)

    # 3. LOCKING TABS
    tab_positions = [30.0, 80.0, 140.0, 260.0]
    for i, tx_val in enumerate(tab_positions):
        tx = tx_val * S
        tab = make_box(doc, f"Lock_Tab_{i}", 6 * S, 8 * S, 4 * S, tx, spine_r - (2 * S), spine_r, c_body, offset_coords)
        all_shapes.append(tab.Shape)
        temp_objects.append(tab)

    # 4. BARCODE STICKER
    bc_x = 40 * S
    bc_l = 50 * S
    bc_w = 12 * S

    sticker_bg = make_box(doc, "Barcode_Bg", bc_l, bc_w, 0.1 * S, bc_x, -5 * S, spine_r * 2, c_sticker, offset_coords)
    all_shapes.append(sticker_bg.Shape)
    temp_objects.append(sticker_bg)

    for i in range(15):
        bx = bc_x + (2 * S) + (i * 3 * S)
        w_line = (1 * S) if i % 2 == 0 else (2 * S)
        bar = make_box(doc, f"Bar_{i}", w_line, 8 * S, 0.2 * S, bx, -3 * S, spine_r * 2, c_dark, offset_coords)
        all_shapes.append(bar.Shape)
        temp_objects.append(bar)

    # 5. PRINTED TEXT (Simulated with lines)
    txt_x_start = 80 * S
    txt_z = spine_r * 2
    title = make_box(doc, "Txt_Title", 80 * S, 2 * S, 0.1 * S, txt_x_start, -6 * S, txt_z, c_white, offset_coords)
    all_shapes.append(title.Shape)
    temp_objects.append(title)

    for i in range(4):
        txt_line = make_box(doc, f"Txt_Line_{i}", 110 * S, 1 * S, 0.1 * S, txt_x_start, (-10 * S) - (i * 3 * S), txt_z, c_white, offset_coords)
        all_shapes.append(txt_line.Shape)
        temp_objects.append(txt_line)

    # 6. ICONS (Simplified)
    icon_x = 240 * S
    icon_z = spine_r * 2
    icon_c = make_cylinder(doc, "CE_C", 4 * S, 0.1 * S, icon_x, -5 * S, icon_z, c_white, offset_coords)
    all_shapes.append(icon_c.Shape)
    temp_objects.append(icon_c)

    bin_x = icon_x - (20 * S)
    bin_body = make_box(doc, "Bin", 8 * S, 10 * S, 0.1 * S, bin_x, -8 * S, icon_z, c_white, offset_coords)
    all_shapes.append(bin_body.Shape)
    temp_objects.append(bin_body)

    # 7. END CAPS
    cap_l = make_cylinder(doc, "Cap_L", spine_r + (0.5 * S), 2 * S, 0, 0, spine_r, c_body, offset_coords, axis=App.Vector(1, 0, 0))
    all_shapes.append(cap_l.Shape)
    temp_objects.append(cap_l)
    
    cap_r = make_cylinder(doc, "Cap_R", spine_r + (0.5 * S), 2 * S, bat_len - (2 * S), 0, spine_r, c_body, offset_coords, axis=App.Vector(1, 0, 0))
    all_shapes.append(cap_r.Shape)
    temp_objects.append(cap_r)

    # --------------------------------------------------------------------------
    # FINAL STEP: Fuse all shapes into a single object
    # --------------------------------------------------------------------------
    if all_shapes:
        fused_shape = reduce(lambda a, b: a.fuse(b), all_shapes)
        
        # Remove the temporary individual parts from the document
        for obj in temp_objects:
            doc.removeObject(obj.Name)
            
        fused_obj = doc.addObject("Part::Feature", "HP_Battery_Fused")
        fused_obj.Shape = fused_shape
        fused_obj.ViewObject.ShapeColor = (0.15, 0.15, 0.15)
        
        doc.recompute()
        return fused_obj


# ============================================================================== 
# MAIN DRAWING FUNCTION: BLACK LAPTOP BATTERY (SCALABLE & FUSED)
# ==============================================================================

def draw_black_battery(doc, offset_coords=(0, 0, 0), scale_factor=1.0):
    """
    Creates a fused Laptop battery (generic black style).
    All dimensions and positions are proportionally scaled by scale_factor.
    """
    S = scale_factor
    all_shapes = []
    temp_objects = []

    # --- COLORS ---
    c_body = (0.15, 0.15, 0.15)
    c_white = (0.90, 0.90, 0.90)
    c_silver = (0.60, 0.60, 0.60)

    # --- DIMENSIONS (SCALED) ---
    bat_len = 270.0 * S
    spine_r = 11.0 * S
    block_w = 40.0 * S
    block_h = 14.0 * S

    # 1. SPINE
    spine = make_cylinder(doc, "Spine", spine_r, bat_len, 0, 0, spine_r, c_body, offset_coords, axis=App.Vector(1, 0, 0))
    all_shapes.append(spine.Shape); temp_objects.append(spine)

    # 2. INTERFACE BLOCK
    block_len = 190.0 * S
    block_x = (bat_len - block_len) / 2

    int_block = make_box(doc, "Interface_Block", block_len, block_w, block_h, block_x, -block_w, 4*S, c_body, offset_coords)
    all_shapes.append(int_block.Shape); temp_objects.append(int_block)

    bridge = make_box(doc, "Bridge", block_len, 10*S, 10*S, block_x, -10*S, 6*S, c_body, offset_coords)
    all_shapes.append(bridge.Shape); temp_objects.append(bridge)

    # 3. CONNECTOR SLOT
    conn_w = 50.0 * S
    conn_x = (bat_len - conn_w) / 2

    for i in range(7):
        cx = conn_x + (i * 7 * S)
        fin = make_box(doc, f"Conn_Fin_{i}", 2*S, 8*S, 8*S, cx, -block_w, 6*S, c_body, offset_coords)
        all_shapes.append(fin.Shape); temp_objects.append(fin)

        if i < 6:
            pin = make_box(doc, f"Pin_{i}", 1*S, 4*S, 1*S, cx + 3*S, -block_w + 2*S, 10*S, c_silver, offset_coords)
            all_shapes.append(pin.Shape); temp_objects.append(pin)

    # 4. FEET & LOCKS
    foot_x_positions = [block_x + 10*S, block_x + block_len - 25*S]
    for i, fx in enumerate(foot_x_positions):
        foot = make_box(doc, f"Rubber_Foot_{i}", 15*S, 15*S, 2*S, fx, -35*S, 2*S, c_body, offset_coords)
        all_shapes.append(foot.Shape); temp_objects.append(foot)

    lock_l = make_box(doc, "Lock_L", 5*S, 15*S, 10*S, block_x - 5*S, -25*S, 6*S, c_body, offset_coords)
    all_shapes.append(lock_l.Shape); temp_objects.append(lock_l)

    lock_r = make_box(doc, "Lock_R", 5*S, 15*S, 10*S, block_x + block_len, -25*S, 6*S, c_body, offset_coords)
    all_shapes.append(lock_r.Shape); temp_objects.append(lock_r)

    # 5. LABELS
    label_z = block_h + (4.1 * S)
    text_x = block_x + (10 * S)
    h1 = make_box(doc, "Txt_Header_1", 60*S, 2*S, 0.1*S, text_x, -10*S, label_z, c_white, offset_coords)
    all_shapes.append(h1.Shape); temp_objects.append(h1)
    
    h2 = make_box(doc, "Txt_Header_2", 40*S, 1.5*S, 0.1*S, text_x, -14*S, label_z, c_white, offset_coords)
    all_shapes.append(h2.Shape); temp_objects.append(h2)

    warn_x = block_x + (80 * S)
    for i in range(6):
        line = make_box(doc, f"Warn_Line_{i}", 70*S, 1*S, 0.1*S, warn_x, (-10*S) - (i * 3 * S), label_z, c_white, offset_coords)
        all_shapes.append(line.Shape); temp_objects.append(line)

    # 6. ICONS
    icon_x = block_x + (160 * S)
    icon_y = -15 * S
    bin_box = make_box(doc, "Bin_Box", 10*S, 12*S, 0.1*S, icon_x, icon_y, label_z, c_white, offset_coords)
    all_shapes.append(bin_box.Shape); temp_objects.append(bin_box)
    
    # "X" Icon on Bin
    x1 = make_box(doc, "X_1", 14*S, 1*S, 0.2*S, icon_x - 2*S, icon_y + 6*S, label_z, c_white, offset_coords, rotation_angle=45)
    all_shapes.append(x1.Shape); temp_objects.append(x1)
    
    x2 = make_box(doc, "X_2", 14*S, 1*S, 0.2*S, icon_x - 2*S, icon_y + 6*S, label_z, c_white, offset_coords, rotation_angle=-45)
    all_shapes.append(x2.Shape); temp_objects.append(x2)

    # --------------------------------------------------------------------------
    # FINAL STEP: Fusion and Cleanup
    # --------------------------------------------------------------------------
    if all_shapes:
        fused_shape = reduce(lambda a, b: a.fuse(b), all_shapes)
        
        # Remove original parts to keep the document clean
        for obj in temp_objects:
            doc.removeObject(obj.Name)
            
        fused_obj = doc.addObject("Part::Feature", "LaptopBattery_Fused")
        fused_obj.Shape = fused_shape
        fused_obj.ViewObject.ShapeColor = (0.15, 0.15, 0.15)
        
        doc.recompute()
        return fused_obj


# ============================================================================== 
# MAIN DRAWING FUNCTION: RUGGED BATTERY PACK (SCALABLE & FUSED)
# ==============================================================================

def draw_rugged_battery(doc, offset_coords=(0, 0, 0), scale_factor=1.0):
    # Scale factor variable
    S = scale_factor
    all_shapes = []

    # --- COLORS ---
    c_olive = (0.28, 0.32, 0.22)
    c_dark = (0.15, 0.15, 0.15)
    c_silver = (0.70, 0.70, 0.70)
    c_white = (0.95, 0.95, 0.95)
    c_led_grn = (0.20, 0.90, 0.20)

    # --- DIMENSIONS (SCALED) ---
    w = 400.0 * S
    d = 300.0 * S
    h = 120.0 * S

    # 1. MAIN ENCLOSURE BODY
    all_shapes.append(make_box(doc, "Main_Case", w, d, h, 0, 0, 0, c_olive, offset_coords).Shape)

    # 2. COOLING RIBS
    num_ribs_top = 12
    rib_w = w
    rib_d = 10.0 * S
    rib_h = 5.0 * S
    gap = (d - (num_ribs_top * rib_d)) / (num_ribs_top + 1)

    for i in range(num_ribs_top):
        y_pos = gap + (i * (rib_d + gap))
        all_shapes.append(make_box(doc, f"Rib_Top_{i}", rib_w, rib_d, rib_h, 0, y_pos, h, c_olive, offset_coords).Shape)

    num_ribs_side = 5
    s_rib_h = 10.0 * S
    s_gap = (h - (num_ribs_side * s_rib_h)) / (num_ribs_side + 1)

    for i in range(num_ribs_side):
        z_pos = s_gap + (i * (s_rib_h + s_gap))
        # Side ribs offset by 5 scaled units
        all_shapes.append(make_box(doc, f"Rib_L_{i}", 5*S, d, s_rib_h, -5*S, 0, z_pos, c_olive, offset_coords).Shape)
        all_shapes.append(make_box(doc, f"Rib_R_{i}", 5*S, d, s_rib_h, w, 0, z_pos, c_olive, offset_coords).Shape)

    # 3. FRONT INTERFACE
    c1_x = 80 * S
    c1_z = h / 2
    all_shapes.append(make_cylinder(doc, "Conn1_Base", 30*S, 20*S, c1_x, -20*S, c1_z, c_dark, offset_coords, axis=App.Vector(0, 1, 0)).Shape)
    all_shapes.append(make_cylinder(doc, "Conn1_Cap", 25*S, 10*S, c1_x, -30*S, c1_z, c_olive, offset_coords, axis=App.Vector(0, 1, 0)).Shape)
    all_shapes.append(make_cylinder(doc, "Conn1_Pin", 5*S, 5*S, c1_x, -35*S, c1_z, c_silver, offset_coords, axis=App.Vector(0, 1, 0)).Shape)

    c2_x = 160 * S
    all_shapes.append(make_cylinder(doc, "Conn2_Base", 30*S, 20*S, c2_x, -20*S, c1_z, c_dark, offset_coords, axis=App.Vector(0, 1, 0)).Shape)
    all_shapes.append(make_cylinder(doc, "Conn2_Cap", 25*S, 10*S, c2_x, -30*S, c1_z, c_olive, offset_coords, axis=App.Vector(0, 1, 0)).Shape)
    all_shapes.append(make_cylinder(doc, "Conn2_Pin", 5*S, 5*S, c2_x, -35*S, c1_z, c_silver, offset_coords, axis=App.Vector(0, 1, 0)).Shape)

    all_shapes.append(make_cylinder(doc, "Lanyard_1", 1*S, 60*S, c1_x, -25*S, c1_z - 30*S, c_dark, offset_coords, axis=App.Vector(1, 0, 0)).Shape)
    all_shapes.append(make_cylinder(doc, "Lanyard_2", 1*S, 60*S, c2_x, -25*S, c1_z - 30*S, c_dark, offset_coords, axis=App.Vector(1, 0, 0)).Shape)

    for i in range(5):
        lx = (60 + (i * 30)) * S
        lz = 25 * S
        all_shapes.append(make_cylinder(doc, f"LED_{i}", 3*S, 2*S, lx, -2*S, lz, c_led_grn, offset_coords, axis=App.Vector(0, 1, 0)).Shape)
        all_shapes.append(make_box(doc, f"LED_Lbl_{i}", 10*S, 1*S, 2*S, lx - 5*S, -1*S, lz + 10*S, c_white, offset_coords).Shape)

    lbl_w = 140 * S
    lbl_h = 70 * S
    lbl_x = 220 * S
    lbl_z = 30 * S

    all_shapes.append(make_box(doc, "Info_Label", lbl_w, 1*S, lbl_h, lbl_x, -1*S, lbl_z, c_white, offset_coords).Shape)
    all_shapes.append(make_box(doc, "Text_Line_1", 120*S, 1*S, 5*S, lbl_x + 10*S, -1.5*S, lbl_z + 55*S, c_dark, offset_coords).Shape)
    all_shapes.append(make_box(doc, "Text_Line_2", 100*S, 1*S, 3*S, lbl_x + 10*S, -1.5*S, lbl_z + 45*S, c_dark, offset_coords).Shape)
    all_shapes.append(make_box(doc, "Text_Line_3", 110*S, 1*S, 3*S, lbl_x + 10*S, -1.5*S, lbl_z + 35*S, c_dark, offset_coords).Shape)

    sw_x = 370 * S
    sw_z = 20 * S
    all_shapes.append(make_box(doc, "Switch_Housing", 20*S, 5*S, 30*S, sw_x, -5*S, sw_z, c_dark, offset_coords).Shape)
    all_shapes.append(make_cylinder(doc, "Switch_Toggle", 2*S, 8*S, sw_x + 10*S, -8*S, sw_z + 20*S, c_white, offset_coords, axis=App.Vector(1, 0, 0)).Shape)

    # Handles
    h_depth = 100 * S
    h_z = (h / 2) - (20 * S)
    all_shapes.append(make_box(doc, "Handle_Base_L", 10*S, h_depth, 40*S, -10*S, (d - h_depth) / 2, h_z, c_dark, offset_coords).Shape)
    all_shapes.append(make_box(doc, "Handle_Bar_L", 5*S, 80*S, 5*S, -15*S, (d - 80*S) / 2, h_z + 17.5*S, c_dark, offset_coords).Shape)
    all_shapes.append(make_box(doc, "Handle_Base_R", 10*S, h_depth, 40*S, w, (d - h_depth) / 2, h_z, c_dark, offset_coords).Shape)
    all_shapes.append(make_box(doc, "Handle_Bar_R", 5*S, 80*S, 5*S, w + 10*S, (d - 80*S) / 2, h_z + 17.5*S, c_dark, offset_coords).Shape)

    # --------------------------------------------------------------------------
    # FINAL STEP: Fuse all shapes into a single object
    # --------------------------------------------------------------------------
    fused_shape = reduce(lambda a, b: a.fuse(b), all_shapes)
    fused_obj = doc.addObject("Part::Feature", "RuggedBattery_Fused")
    fused_obj.Shape = fused_shape
    fused_obj.ViewObject.ShapeColor = (0.35, 0.38, 0.30)  # Muted Olive
    doc.recompute()
    return fused_obj


# ==============================================================================
# MAIN DRAWING FUNCTION: MILITARY BATTERY (SCALABLE & FUSED)
# ==============================================================================
def draw_mil_battery(doc, offset_coords=(0, 0, 0), scale_factor=1.0):
    """
    Creates a fused Military-style battery (Tan/Black).
    All dimensions and positions are proportionally scaled by scale_factor.
    """
    S = scale_factor
    temp_objects = []
    all_shapes = []

    # --- COLORS ---
    c_tan = (0.82, 0.78, 0.65)
    c_black = (0.10, 0.10, 0.10)
    c_green = (0.00, 0.30, 0.15)
    c_silver = (0.75, 0.75, 0.75)

    # --- DIMENSIONS (SCALED) ---
    w = 120.0 * S
    d = 65.0 * S
    h = 130.0 * S

    # 1. MAIN BODY
    body = make_box(doc, "Bat_Case", w, d, h, 0, 0, 0, c_tan, offset_coords)
    all_shapes.append(body.Shape); temp_objects.append(body)

    # 2. TOP INTERFACE
    conn_x = 35 * S
    conn_y = d / 2 

    socket = make_cylinder(doc, "Conn_Socket", 14*S, 2*S, conn_x, conn_y, h, c_black, offset_coords)
    all_shapes.append(socket.Shape); temp_objects.append(socket)

    for i in range(5):
        angle = (360 / 5) * i
        rad = math.radians(angle)
        px = conn_x + (8 * S * math.cos(rad))
        py = conn_y + (8 * S * math.sin(rad))
        pin = make_cylinder(doc, f"Pin_{i}", 2*S, 3*S, px, py, h - (1*S), c_silver, offset_coords)
        all_shapes.append(pin.Shape); temp_objects.append(pin)

    # SOC Display
    disp_w = 40 * S
    disp_d = 40 * S
    disp_x = w - (50 * S)
    disp_y = (d - disp_d) / 2

    label = make_box(doc, "SOC_Label", disp_w, disp_d, 0.5*S, disp_x, disp_y, h, c_black, offset_coords)
    all_shapes.append(label.Shape); temp_objects.append(label)
    
    lcd1 = make_box(doc, "LCD_1", 30*S, 10*S, 0.6*S, disp_x + 5*S, disp_y + 25*S, h, c_green, offset_coords)
    all_shapes.append(lcd1.Shape); temp_objects.append(lcd1)
    
    lcd2 = make_box(doc, "LCD_2", 30*S, 10*S, 0.6*S, disp_x + 5*S, disp_y + 5*S, h, c_green, offset_coords)
    all_shapes.append(lcd2.Shape); temp_objects.append(lcd2)
    
    btn = make_cylinder(doc, "Push_Btn", 4*S, 2*S, disp_x + 35*S, disp_y + 20*S, h, c_silver, offset_coords)
    all_shapes.append(btn.Shape); temp_objects.append(btn)

    # 3. FRONT FACE DETAILS
    logo = make_box(doc, "Logo_Main", 20*S, 0.5*S, 10*S, 15*S, -0.5*S, h - (30*S), c_black, offset_coords)
    all_shapes.append(logo.Shape); temp_objects.append(logo)

    tx_x = 15 * S
    tx_z = h - (45 * S)

    title = make_box(doc, "Txt_Title", 50*S, 0.5*S, 3*S, tx_x, -0.5*S, tx_z, c_black, offset_coords)
    all_shapes.append(title.Shape); temp_objects.append(title)

    # Schematic/Diagram Frame
    sch_w, sch_h = 40*S, 25*S
    sch_x, sch_z = w - (55*S), h - (50*S)
    sch_f = make_box(doc, "Sch_Frame", sch_w, 0.5*S, sch_h, sch_x, -0.5*S, sch_z, c_black, offset_coords)
    all_shapes.append(sch_f.Shape); temp_objects.append(sch_f)

    # Recycle Icon
    rc_x, rc_z = w - (35*S), 40*S
    recycle = make_cylinder(doc, "Recycle_Circ", 10*S, 0.5*S, rc_x, -0.5*S, rc_z, c_black, offset_coords, axis=App.Vector(0, 1, 0))
    all_shapes.append(recycle.Shape); temp_objects.append(recycle)

    # Instruction Block
    inst_x, inst_z = 15*S, 20*S
    for i in range(6):
        line = make_box(doc, f"Inst_Line_{i}", 80*S, 0.5*S, 1.5*S, inst_x, -0.5*S, inst_z + (25*S) - (i * 4 * S), c_black, offset_coords)
        all_shapes.append(line.Shape); temp_objects.append(line)

    # --- FUSION STEP ---
    if all_shapes:
        fused_shape = reduce(lambda a, b: a.fuse(b), all_shapes)
        
        # Cleanup temporary objects so they don't clutter the tree
        for obj in temp_objects:
            doc.removeObject(obj.Name)
            
        final_obj = doc.addObject("Part::Feature", "MilBattery_Fused")
        final_obj.Shape = fused_shape
        final_obj.ViewObject.ShapeColor = c_tan
        
        doc.recompute()
        return final_obj
 



# ==============================================================================
# MAIN DRAWING FUNCTION: SHREDDED BATTERY CELL
# ==============================================================================

def draw_battery_cell(doc, offset_coords=(0, 0, 0), scale_factor=1.0):

    all_parts = []  # To collect shapes for final fusion
    S = scale_factor # Scale factor multiplier

    # --- DIMENSIONS (SCALED) ---
    radius = 20.0 * S
    height = 50.0 * S
    case_thickness = 1.0 * S
    layer_thickness = 0.8 * S
    num_layers = 8

    # --- COLORS ---
    c_case = (0.7, 0.7, 0.7)      # Steel grey
    c_cathode = (0.2, 0.4, 0.8)   # Blue
    c_anode = (0.8, 0.5, 0.2)     # Orange
    c_separator = (0.9, 0.9, 0.9) # White

    # 1. QUARTER CUT TOOL
    # We create the box that will cut the quarter out of the final assembly
    # Scaled dimensions ensure the cut tool is always large enough
    cut_box = Part.makeBox(radius + (5 * S), radius + (5 * S), height + (2 * S))
    cut_box.translate(App.Vector(offset_coords[0], offset_coords[1], offset_coords[2] - (1 * S)))

    # 2. OUTER CASE (Cylinder Shell)
    outer = Part.makeCylinder(radius, height)
    inner = Part.makeCylinder(radius - case_thickness, height)
    case_shell = outer.cut(inner)
    case_shell.translate(App.Vector(offset_coords[0], offset_coords[1], offset_coords[2]))
    
    # Apply cut and add to list
    case_final = case_shell.cut(cut_box)
    obj_case = doc.addObject("Part::Feature", "Case_Fe")
    obj_case.Shape = case_final
    obj_case.ViewObject.ShapeColor = c_case
    all_parts.append(case_final)

    # 3. INTERNAL LAYERS (Jelly Roll)
    current_r = radius - case_thickness
    
    for i in range(num_layers):
        # Determine Color
        if i % 3 == 0:
            color = c_cathode
            l_name = f"Cathode_{i}"
        elif i % 3 == 1:
            color = c_separator
            l_name = f"Separator_{i}"
        else:
            color = c_anode
            l_name = f"Anode_{i}"

        # Create shell for this layer
        r_out = current_r
        current_r -= layer_thickness
        r_in = current_r

        l_outer_cyl = Part.makeCylinder(r_out, height)
        l_inner_cyl = Part.makeCylinder(r_in, height)
        layer_shell = l_outer_cyl.cut(l_inner_cyl)
        layer_shell.translate(App.Vector(offset_coords[0], offset_coords[1], offset_coords[2]))
        
        # Apply quarter cut
        layer_final = layer_shell.cut(cut_box)
        
        # Add feature to doc (hidden)
        obj_l = doc.addObject("Part::Feature", l_name)
        obj_l.Shape = layer_final
        obj_l.ViewObject.ShapeColor = color
        obj_l.ViewObject.Visibility = False
        
        all_parts.append(layer_final)

    # 4. CENTRAL CORE
    core_shape = Part.makeCylinder(current_r, height)
    core_shape.translate(App.Vector(offset_coords[0], offset_coords[1], offset_coords[2]))
    core_final = core_shape.cut(cut_box)
    
    obj_core = doc.addObject("Part::Feature", "Core_Pin")
    obj_core.Shape = core_final
    obj_core.ViewObject.ShapeColor = (0.95, 0.95, 0.95)
    obj_core.ViewObject.Visibility = False
    all_parts.append(core_final)

    # 5. FINAL FUSION
    # Fuse everything together into one single object
    fused_shape = all_parts[0]
    for s in all_parts[1:]:
        fused_shape = fused_shape.fuse(s)

    final_obj = doc.addObject("Part::Feature", "Fused_Battery_Cell")
    final_obj.Shape = fused_shape
    final_obj.ViewObject.ShapeColor = c_case # Overall color
    
    print(f"Battery Cell drawing (Scale: {scale_factor}) and fusion complete.")



# ==============================================================================
# MAIN DRAWING FUNCTION: Shredded LiFePO4 PRISMATIC BATTERY
# ==============================================================================

def draw_prismatic_battery(doc, offset_coords=(0, 0, 0), scale_factor=1.0):
    all_shapes = []  
    S = scale_factor

    # --- DIMENSIONS (SCALED) ---
    w, d, h = 80.0 * S, 25.0 * S, 120.0 * S
    wall = 1.5 * S
    
    # --- COLORS (Matching Image) ---
    c_case = (0.8, 0.8, 0.8)      # Silver
    c_cathode = (0.4, 0.7, 1.0)   # Blue
    c_anode = (0.4, 0.2, 0.5)     # Purple
    c_separator = (1.0, 1.0, 0.9) # White/Cream

    # 1. CAN CASE WITH CUTAWAY
    outer_shape = Part.makeBox(w, d, h)
    inner_shape = Part.makeBox(w - 2*wall, d - 2*wall, h - wall)
    inner_shape.translate(App.Vector(wall, wall, wall))
    case_hollow = outer_shape.cut(inner_shape)
    
    # Create Side Cutout (Reveal internals)
    cut_w, cut_h = w * 0.6, h * 0.8
    side_cut = Part.makeBox(cut_w, d + (10.0 * S), cut_h)
    side_cut.translate(App.Vector(w * 0.4, -5.0 * S, h * 0.1))
    
    case_final = case_hollow.cut(side_cut)
    case_final.translate(App.Vector(offset_coords[0], offset_coords[1], offset_coords[2]))
    
    obj_case = doc.addObject("Part::Feature", "Prism_Case_Base")
    obj_case.Shape = case_final
    obj_case.ViewObject.ShapeColor = c_case
    all_shapes.append(case_final) # Already a Shape

    # 2. TOP PLATE & TERMINALS
    plate = make_box(doc, "Top_Plate", w, d, 4.0 * S, 0, 0, h, c_case, offset_coords)
    all_shapes.append(plate.Shape)
    
    term1 = make_box(doc, "Terminal_Pos", 12.0 * S, 12.0 * S, 6.0 * S, w * 0.3, d / 2.0 - (6.0 * S), h + (4.0 * S), c_case, offset_coords)
    all_shapes.append(term1.Shape)
    
    term2 = make_box(doc, "Terminal_Neg", 12.0 * S, 12.0 * S, 6.0 * S, w * 0.7, d / 2.0 - (6.0 * S), h + (4.0 * S), (0.3, 0.3, 0.3), offset_coords)
    all_shapes.append(term2.Shape)

    # 3. INTERNAL STACKS (Electrode Plates)
    for i in range(10):
        sx = wall + (2.0 * S) + (i * 3.0 * S)
        # Alternate colors to simulate stacked structure
        col = c_cathode if i % 2 == 0 else c_anode
        stack = make_box(doc, f"Stack_{i}", 1.5 * S, d - 2.0 * wall, h - (20.0 * S), sx, wall, 10.0 * S, col, offset_coords)
        all_shapes.append(stack.Shape)

    # 4. CURVED PEELED LAYERS (Bezier logic)
    def create_peel_shape(offset_y, color, name):
        # All control points scaled via w, d, h or direct S multiplication
        p1 = App.Vector(w * 0.4 + offset_coords[0], d / 2.0 + offset_y + offset_coords[1], 20.0 * S + offset_coords[2])
        p2 = App.Vector(w * 1.1 + offset_coords[0], d / 2.0 + offset_y + offset_coords[1], h / 2.0 + offset_coords[2])
        p3 = App.Vector(w * 0.9 + offset_coords[0], d * 1.2 + offset_y + offset_coords[1], h - (20.0 * S) + offset_coords[2])
        
        bez = Part.BezierCurve()
        bez.setPoles([p1, p2, p3])
        edge = bez.toShape()
        spine = Part.Wire([edge])
        
        # Profile for the sheet
        section = Part.makePolygon([
            App.Vector(0, 0, 0), 
            App.Vector(0, 0, h - (40.0 * S)), 
            App.Vector(0.5 * S, 0, h - (40.0 * S)), 
            App.Vector(0.5 * S, 0, 0), 
            App.Vector(0, 0, 0)
        ])
        section.translate(p1)
        
        peel_shape = spine.makePipeShell([Part.Wire([section])], True, False)
        obj_p = doc.addObject("Part::Feature", name)
        obj_p.Shape = peel_shape
        obj_p.ViewObject.ShapeColor = color
        obj_p.ViewObject.Visibility = False
        return peel_shape # Returns Shape

    # Peeling out: Cathode (Blue), Separator (White), Anode (Purple)
    all_shapes.append(create_peel_shape(3.0 * S, c_cathode, "Peel_Cathode"))
    all_shapes.append(create_peel_shape(0, c_separator, "Peel_Sep"))
    all_shapes.append(create_peel_shape(-3.0 * S, c_anode, "Peel_Anode"))

    # 5. FINAL FUSION
    if all_shapes:
        fused_shape = all_shapes[0]
        for s in all_shapes[1:]:
            fused_shape = fused_shape.fuse(s)

        final_obj = doc.addObject("Part::Feature", f"Fused_Battery_S{scale_factor}")
        final_obj.Shape = fused_shape
        final_obj.ViewObject.ShapeColor = c_case
        
        # Cleanup
        doc.removeObject("Prism_Case_Base")
        doc.removeObject("Top_Plate")
        doc.removeObject("Terminal_Pos")
        doc.removeObject("Terminal_Neg")
        for i in range(10): 
            try: doc.removeObject(f"Stack_{i}")
            except: pass
        doc.removeObject("Peel_Cathode")
        doc.removeObject("Peel_Sep")
        doc.removeObject("Peel_Anode")
        
        return final_obj


def make_hopper_loft(doc, name, top_w, top_l, bot_r, height, x, y, z, color, offset=(0,0,0)):
    # Top Rectangle
    p1 = App.Vector(-top_l/2, -top_w/2, height)
    p2 = App.Vector(top_l/2, -top_w/2, height)
    p3 = App.Vector(top_l/2, top_w/2, height)
    p4 = App.Vector(-top_l/2, top_w/2, height)
    wire_top = Part.makePolygon([p1, p2, p3, p4, p1])
    
    # Bottom Circle
    circle = Part.makeCircle(bot_r, App.Vector(0,0,0), App.Vector(0,0,1))
    wire_bot = Part.Wire(circle)
    
    # Loft
    loft = Part.makeLoft([wire_bot, wire_top], True)
    
    # Apply translation with offset
    loft.translate(App.Vector(x + offset[0], y + offset[1], z + offset[2]))
    
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = loft
    obj.ViewObject.ShapeColor = color
    return obj

def make_housing_profile(doc, name, length, w_bottom, w_top, h, x, y, z, color, offset=(0,0,0)):
    # Profile on YZ plane extruded along X
    y_bot = w_bottom / 2
    y_top = w_top / 2
    pts = [
        App.Vector(0, -y_bot, 0),
        App.Vector(0, y_bot, 0),
        App.Vector(0, y_top, h),
        App.Vector(0, -y_top, h),
        App.Vector(0, -y_bot, 0)
    ]
    poly = Part.makePolygon(pts)
    face = Part.Face(poly)
    prism = face.extrude(App.Vector(length, 0, 0))
    
    # Apply translation with offset
    # Note: original logic used x - length/2 as start point for extrusion
    prism.translate(App.Vector((x - length/2) + offset[0], y + offset[1], z + offset[2]))
    
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = prism
    obj.ViewObject.ShapeColor = color
    return obj

# ==========================================
# 4. MAIN BUILD ROUTINE
# ==========================================

def build_cleaner(doc, offset=(0,0,0)):
    """
    Builds the Grain Cleaner at the specified offset coordinates.
    """
    base_z = leg_height
    
    # --- A. STRUCTURAL FRAME ---
    # Beams
    make_box(doc, "Beam_L", total_length, frame_beam_size, frame_beam_size, 
             total_length/2 - section_len/2, -total_width/2, base_z, col_grey_paint, offset)
             
    make_box(doc, "Beam_R", total_length, frame_beam_size, frame_beam_size, 
             total_length/2 - section_len/2, total_width/2 - frame_beam_size, base_z, col_grey_paint, offset)
    
    # Legs
    for i in range(hopper_count + 1):
        x_pos = (i * section_len)
        make_box(doc, f"Leg_L_{i}", frame_beam_size, frame_beam_size, leg_height, 
                 x_pos, -total_width/2, 0, col_grey_paint, offset)
                 
        make_box(doc, f"Leg_R_{i}", frame_beam_size, frame_beam_size, leg_height, 
                 x_pos, total_width/2 - frame_beam_size, 0, col_grey_paint, offset)
        
        # Bracing (using make_box rotation logic)
        if i < hopper_count:
            brace_len = math.sqrt(section_len**2 + leg_height**2)
            angle = math.degrees(math.atan2(leg_height, section_len))
            
            # Note: Rotation in original was around (0,0,0) then translated. 
            # make_box rotates around (0,0,0) then translates. This logic holds.
            make_box(doc, f"Brace_{i}", brace_len, 10, 50, 
                     x_pos, -total_width/2 + frame_beam_size, 0, col_grey_paint, offset,
                     rotation_angle=-angle, rotation_axis=App.Vector(0,1,0))

    # --- B. HOPPERS ---
    hopper_h = 600.0
    outlet_r = 100.0
    for i in range(hopper_count):
        center_x = (i * section_len) + (section_len/2)
        h_len = section_len - 20
        h_wid = total_width - 20
        
        make_hopper_loft(doc, f"Hopper_{i}", h_wid, h_len, outlet_r, hopper_h, 
                         center_x, 0, base_z - hopper_h, col_grey_paint, offset)
                         
        make_cylinder(doc, f"Outlet_{i}", outlet_r, 100, 
                      center_x, 0, base_z - hopper_h - 100, col_grey_paint, offset)

    # --- C. UPPER HOUSING ---
    for i in range(hopper_count):
        center_x = (i * section_len) + (section_len/2)
        housing_len = section_len - 10
        
        make_housing_profile(doc, f"Housing_{i}", housing_len, total_width, top_flat_width, housing_height, 
                             center_x, 0, base_z + frame_beam_size, col_grey_paint, offset)
        
        # Inspection Door
        door_x = center_x - (housing_len-50)/2
        door_y = -(top_flat_width-50)/2
        door_z = base_z + frame_beam_size + housing_height
        
        make_box(doc, f"Door_{i}", housing_len - 50, top_flat_width - 50, 20, 
                 door_x, door_y, door_z, (0.6, 0.65, 0.67), offset)
        
        # Handles
        for h_side in [-1, 1]:
            h_y = h_side * (top_flat_width/2 - 10)
            make_box(doc, f"Latch_{i}_{h_side}", 50, 20, 30, 
                     center_x, h_y - 10, base_z + frame_beam_size + housing_height, col_handle_black, offset)

    # --- D. DISCHARGE CHUTE ---
    end_x = total_length
    # Box rotated around Y axis
    make_box(doc, "DischargeSpout", 600, 400, 400, 
             end_x, 0, base_z + 200, col_grey_paint, offset,
             rotation_angle=30, rotation_axis=App.Vector(0,1,0))
    
    # --- E. DRIVE MECHANISM ---
    make_box(doc, "BearingBlock", 150, 400, 150, 
             end_x, -200, base_z + housing_height/2, col_grey_paint, offset)
             
    # Drive Shaft (aligned X axis)
    # Helper expects axis=(1,0,0) for X alignment
    make_cylinder(doc, "DriveShaft", 40, 200, 
                  end_x, 0, base_z + housing_height/2 + 75, col_dark_metal, offset, axis=App.Vector(1,0,0))



def make_u_bend(doc, name, pipe_r, bend_r, x, y, z, rotation_z, color, offset=(0,0,0)):
    # Create a 180 degree torus segment
    # Major radius = bend_r, Minor radius = pipe_r
    # Angles: 0 to 180
    torus = Part.makeTorus(bend_r, pipe_r, App.Vector(0,0,0), App.Vector(0,0,1), 0, 180)
    
    # Orient vertically (arching over)
    torus.rotate(App.Vector(0,0,0), App.Vector(1,0,0), 90)
    
    # Rotate to face center
    torus.rotate(App.Vector(0,0,0), App.Vector(0,0,1), rotation_z)
    
    # Translate to position + Offset
    torus.translate(App.Vector(x + offset[0], y + offset[1], z + offset[2]))
    
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = torus
    obj.ViewObject.ShapeColor = color
    return obj

# Custom helper for Cone (as it's not in the standard requested list but needed for Cyclones)
def make_cone(doc, name, r1, r2, height, x, y, z, color, offset=(0,0,0)):
    shape = Part.makeCone(r1, r2, height)
    shape.translate(App.Vector(x + offset[0], y + offset[1], z + offset[2]))
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = shape
    obj.ViewObject.ShapeColor = color
    return obj

# ==========================================
# 4. MAIN BUILD ROUTINE
# ==========================================

def build_cluster(doc, offset=(0,0,0)):
    """
    Builds the Hydrocyclone cluster at the specified offset coordinates.
    """
    
    # Levels
    z_launder_base = 200.0
    z_cyclone_mid = z_launder_base + launder_height + 150
    z_cyclone_top = z_cyclone_mid + cyclone_len_cyl
    z_manifold_top = z_cyclone_top + 100
    
    # --- A. BOTTOM LAUNDER (TUB) ---
    # Outer Shell (Manual boolean cut required as helper make_cylinder adds object directly)
    # We will make two temporary cylinders, cut them, then add to doc
    l_outer = Part.makeCylinder(launder_radius, launder_height)
    l_inner = Part.makeCylinder(launder_radius - 20, launder_height)
    launder_shape = l_outer.cut(l_inner)
    launder_shape.translate(App.Vector(offset[0], offset[1], z_launder_base + offset[2]))
    
    obj_l = doc.addObject("Part::Feature", "Launder_Tub")
    obj_l.Shape = launder_shape
    obj_l.ViewObject.ShapeColor = col_grey_body
    
    # Discharge Spout
    make_cylinder(doc, "Launder_Out", 150, 200, 
                  -launder_radius, 0, z_launder_base + 200, col_grey_body, offset, axis=App.Vector(1,0,0))
    make_cylinder(doc, "Launder_Flange", 180, 20, 
                  -launder_radius-200, 0, z_launder_base + 200, col_dark_metal, offset, axis=App.Vector(1,0,0))

    # Legs
    for i in [45, 135, 225, 315]:
        rad = math.radians(i)
        lx = (launder_radius - 50) * math.cos(rad)
        ly = (launder_radius - 50) * math.sin(rad)
        make_cylinder(doc, f"Leg_{i}", 50, z_launder_base, 
                      lx, ly, 0, col_dark_metal, offset)

    # --- B. CENTRAL MANIFOLD ---
    make_cylinder(doc, "Feed_Manifold", tank_radius, z_manifold_top - z_launder_base + 100, 
                  0, 0, z_launder_base, col_grey_body, offset)
    
    # Dome Cap (Manual shape needed for Sphere)
    dome = Part.makeSphere(tank_radius)
    mat = App.Matrix()
    mat.scale(1.0, 1.0, 0.25)
    dome.transformShape(mat)
    dome.translate(App.Vector(offset[0], offset[1], z_manifold_top + 100 + offset[2]))
    
    obj_d = doc.addObject("Part::Feature", "Manifold_Cap")
    obj_d.Shape = dome
    obj_d.ViewObject.ShapeColor = col_grey_body

    # --- C. CYCLONES ---
    for i in range(num_cyclones):
        angle_deg = i * (360.0 / num_cyclones)
        angle_rad = math.radians(angle_deg)
        
        # Cyclone Center Coordinates
        cx = cluster_radius * math.cos(angle_rad)
        cy = cluster_radius * math.sin(angle_rad)
        
        # 1. Cone
        make_cone(doc, f"Cyc_Cone_{i}", cyclone_dia/5, cyclone_dia/2, cyclone_len_cone,
                  cx, cy, z_cyclone_mid - cyclone_len_cone, col_blue_cyc, offset)
        
        # 2. Cylinder Body
        make_cylinder(doc, f"Cyc_Cyl_{i}", cyclone_dia/2, cyclone_len_cyl,
                      cx, cy, z_cyclone_mid, col_blue_cyc, offset)
        
        # Flanges (Mid and Top)
        make_cylinder(doc, f"Flange_Mid_{i}", cyclone_dia/2 + 25, 20, 
                      cx, cy, z_cyclone_mid, col_dark_metal, offset)
        make_cylinder(doc, f"Flange_Top_{i}", cyclone_dia/2 + 25, 20, 
                      cx, cy, z_cyclone_top, col_dark_metal, offset)
        
        # 3. Inlet Pipe (Radial connection to Manifold)
        inlet_len = (cluster_radius - cyclone_dia/2) - tank_radius
        inlet_r = 70.0
        
        inlet = Part.makeCylinder(inlet_r, inlet_len)
        inlet.rotate(App.Vector(0,0,0), App.Vector(0,1,0), -90) # Align along X
        inlet.translate(App.Vector(tank_radius, 0, z_cyclone_mid + 100)) # Move to edge of tank
        inlet.rotate(App.Vector(0,0,0), App.Vector(0,0,1), angle_deg) # Rotate to radial position
        inlet.translate(App.Vector(offset[0], offset[1], offset[2])) # Apply global offset
        
        obj_in = doc.addObject("Part::Feature", f"Inlet_{i}")
        obj_in.Shape = inlet
        obj_in.ViewObject.ShapeColor = col_blue_cyc
        
        # 4. Valve (On Inlet)
        # Valve Body
        v_dist = tank_radius + (inlet_len * 0.4)
        vx = v_dist * math.cos(angle_rad)
        vy = v_dist * math.sin(angle_rad)
        vz = z_cyclone_mid + 100
        
        make_cylinder(doc, f"ValveBody_{i}", inlet_r + 20, 100, 
                      vx, vy, vz - 50, col_dark_metal, offset)
        # Valve Stem
        make_cylinder(doc, f"ValveStem_{i}", 15, 150, 
                      vx, vy, vz + 50, col_dark_metal, offset)
        
        # Handwheel (Manual Torus)
        wheel = Part.makeTorus(60, 10)
        wheel.translate(App.Vector(vx + offset[0], vy + offset[1], vz + 200 + offset[2]))
        
        obj_w = doc.addObject("Part::Feature", f"HandWheel_{i}")
        obj_w.Shape = wheel
        obj_w.ViewObject.ShapeColor = col_valve_wheel
        
        # 5. Overflow Pipe ("Candy Cane")
        # Vertical section up from cyclone
        pipe_r = 60.0
        make_cylinder(doc, f"Pipe_Up_{i}", pipe_r, 300, 
                      cx, cy, z_cyclone_top, col_grey_body, offset)
        
        # U-Bend (180 deg) pointing to center
        bend_radius = 200.0
        bend_z = z_cyclone_top + 300
        # Rotate bend to face INWARD (angle_deg + 180)
        make_u_bend(doc, f"Bend_{i}", pipe_r, bend_radius, cx, cy, bend_z, angle_deg + 180, col_grey_body, offset)
        
        # Downward pipe into manifold
        dx = (cluster_radius - (bend_radius*2)) * math.cos(angle_rad)
        dy = (cluster_radius - (bend_radius*2)) * math.sin(angle_rad)
        
        make_cylinder(doc, f"Pipe_Down_{i}", pipe_r, 200, 
                      dx, dy, z_manifold_top - 50, col_grey_body, offset)
        
        # 6. Support Bracket
        b_len = 200
        b_h = 200
        
        # We need a manual boolean cut for the wedge shape, then apply offset
        bracket = Part.makeBox(b_len, 20, b_h)
        cut_box = Part.makeBox(b_len + 10, 30, b_h + 10)
        cut_box.rotate(App.Vector(0,0,0), App.Vector(0,1,0), -45)
        cut_box.translate(App.Vector(0, -5, b_h))
        bracket = bracket.cut(cut_box)
        
        # Position
        bracket.translate(App.Vector(tank_radius, -10, z_cyclone_mid - 150))
        bracket.rotate(App.Vector(0,0,0), App.Vector(0,0,1), angle_deg)
        bracket.translate(App.Vector(offset[0], offset[1], offset[2]))
        
        obj_br = doc.addObject("Part::Feature", f"Bracket_{i}")
        obj_br.Shape = bracket
        obj_br.ViewObject.ShapeColor = col_grey_body




def make_hopper(doc, name, top_w, top_d, bot_w, bot_d, h, x, y, z, color, offset=(0,0,0)):
    # Top Rectangle (Larger)
    p1 = App.Vector(-top_w/2, -top_d/2, h)
    p2 = App.Vector(top_w/2, -top_d/2, h)
    p3 = App.Vector(top_w/2, top_d/2, h)
    p4 = App.Vector(-top_w/2, top_d/2, h)
    wire_top = Part.makePolygon([p1, p2, p3, p4, p1])
    
    # Bottom Rectangle (Smaller discharge)
    p1b = App.Vector(-bot_w/2, -bot_d/2, 0)
    p2b = App.Vector(bot_w/2, -bot_d/2, 0)
    p3b = App.Vector(bot_w/2, bot_d/2, 0)
    p4b = App.Vector(-bot_w/2, bot_d/2, 0)
    wire_bot = Part.makePolygon([p1b, p2b, p3b, p4b, p1b])
    
    # Loft
    loft = Part.makeLoft([wire_bot, wire_top], True)
    
    # Apply translation with offset
    loft.translate(App.Vector(x + offset[0], y + offset[1], z + offset[2]))
    
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = loft
    obj.ViewObject.ShapeColor = color
    return obj

# ==========================================
# 4. MAIN BUILD ROUTINE
# ==========================================

def build_dust_collector(doc, offset=(0,0,0)):
    """
    Builds the Dust Collector at the specified offset coordinates.
    """
    
    # Z-Coordinates
    z_floor = 0.0
    z_body_start = leg_height
    z_body_end = z_body_start + body_height
    z_hopper_discharge = z_body_start - hopper_height
    
    # --- A. LEGS & FRAME ---
    leg_size = 100.0
    # Legs are positioned at the corners of the main body width
    leg_positions = [
        (-width/2, -depth/2), (width/2 - leg_size, -depth/2),
        (-width/2, depth/2 - leg_size), (width/2 - leg_size, depth/2 - leg_size)
    ]
    
    for i, (lx, ly) in enumerate(leg_positions):
        # Leg Column
        make_box(doc, f"Leg_{i}", leg_size, leg_size, leg_height, 
                 lx, ly, 0, col_dark_grey, offset)
        
        # Foot Plate
        make_box(doc, f"Foot_{i}", leg_size+100, leg_size+100, 20, 
                 lx-50, ly-50, 0, col_dark_grey, offset)

    # Cross Bracing (Low level)
    brace_z = 300.0
    # Front/Back braces
    make_box(doc, "Brace_F", width, 60, 60, 
             -width/2, -depth/2 + 20, brace_z, col_dark_grey, offset)
             
    make_box(doc, "Brace_B", width, 60, 60, 
             -width/2, depth/2 - 80, brace_z, col_dark_grey, offset)
             
    # Side braces
    make_box(doc, "Brace_L", 60, depth, 60, 
             -width/2 + 20, -depth/2, brace_z, col_dark_grey, offset)
             
    make_box(doc, "Brace_R", 60, depth, 60, 
             width/2 - 80, -depth/2, brace_z, col_dark_grey, offset)

    # --- B. HOPPER ---
    # Creates the pyramid funnel
    make_hopper(doc, "Hopper", width, depth, discharge_size, discharge_size, hopper_height, 
                0, 0, z_hopper_discharge, col_grey_body, offset)
    
    # Discharge Flange
    make_box(doc, "DischargeFlange", discharge_size+100, discharge_size+100, 20, 
             -(discharge_size+100)/2, -(discharge_size+100)/2, z_hopper_discharge - 20, col_dark_grey, offset)

    # --- C. MAIN BODY ---
    # Main Box
    make_box(doc, "MainBody", width, depth, body_height, 
             -width/2, -depth/2, z_body_start, col_grey_body, offset)
    
    # Top Cap/Lid
    lid_h = 100
    make_box(doc, "TopLid", width+50, depth+50, lid_h, 
             -(width+50)/2, -(depth+50)/2, z_body_end, col_grey_body, offset)

    # --- D. STIFFENERS / RIBS ---
    # The image shows horizontal ribs wrapping around the body
    num_ribs = 4
    rib_spacing = body_height / num_ribs
    rib_thick = 40
    rib_depth = 50
    
    for i in range(num_ribs):
        rz = z_body_start + (i * rib_spacing) + (rib_spacing/2)
        # Create a hollow rectangle using 4 boxes
        
        # Front
        make_box(doc, f"Rib_F_{i}", width + 2*rib_depth, rib_depth, rib_thick, 
                 -width/2 - rib_depth, -depth/2 - rib_depth, rz, col_grey_body, offset)
                 
        # Back
        make_box(doc, f"Rib_B_{i}", width + 2*rib_depth, rib_depth, rib_thick, 
                 -width/2 - rib_depth, depth/2, rz, col_grey_body, offset)
                 
        # Left
        make_box(doc, f"Rib_L_{i}", rib_depth, depth, rib_thick, 
                 -width/2 - rib_depth, -depth/2, rz, col_grey_body, offset)
                 
        # Right
        make_box(doc, f"Rib_R_{i}", rib_depth, depth, rib_thick, 
                 width/2, -depth/2, rz, col_grey_body, offset)

    # --- E. SIDE INLET PIPE ---
    # Pipe entering the hopper area
    inlet_r = 250.0
    inlet_len = 600.0
    inlet_z = z_hopper_discharge + (hopper_height * 0.6)
    
    # Pipe aligned to X axis
    make_cylinder(doc, "InletPipe", inlet_r, inlet_len, 
                  width/2 - 100, 0, inlet_z, col_grey_body, offset, axis=App.Vector(1,0,0))
                  
    # Flange
    make_cylinder(doc, "InletFlange", inlet_r + 50, 30, 
                  width/2 + inlet_len - 30, 0, inlet_z, col_dark_grey, offset, axis=App.Vector(1,0,0))

    # --- F. TOP HEADER (PULSE JET SYSTEM) ---
    # Black pipe running along the front top edge
    header_dia = 150.0
    header_len = width - 200
    header_x = 0
    header_y = -depth/2 - 100 # In front of the box
    header_z = z_body_end + 150
    
    # The Header Tank (Cylinder rotated 90 deg around Y to align X)
    # The helper's axis=(1,0,0) handles X-alignment.
    # Note: original code used Part.makeCylinder and rotated manually.
    # Helper make_cylinder axis=1,0,0 rotates (0,0,0)->(0,1,0) 90 deg. 
    # Standard cylinder is along Z. Rotate around Y 90 deg makes it along X.
    make_cylinder(doc, "HeaderTank", header_dia/2, header_len, 
                  -header_len/2, header_y, header_z, col_black, offset, axis=App.Vector(1,0,0))
    
    # Valves connecting Header to Top Lid
    num_valves = 8
    valve_spacing = header_len / num_valves
    start_x = -header_len/2 + (valve_spacing/2)
    
    for i in range(num_valves):
        vx = start_x + (i * valve_spacing)
        
        # Connection Pipe (Horizontal from header to unit - Y axis)
        conn_len = 150
        make_cylinder(doc, f"ValvePipe_{i}", 20, conn_len, 
                      vx, header_y, header_z, col_black, offset, axis=App.Vector(0,1,0))
        
        # Valve Body (Vertical cylinder - Z axis)
        make_cylinder(doc, f"ValveBody_{i}", 30, 60, 
                      vx, header_y + 80, header_z + 20, col_valve, offset, axis=App.Vector(0,0,1))
        
        # Injection pipe (Elbow into lid - Vertical down)
        # Using Z axis, but position is shifted
        make_cylinder(doc, f"InjPipe_{i}", 20, 150, 
                      vx, header_y + 150, header_z - 150, col_black, offset, axis=App.Vector(0,0,1))




# Specialized helpers adapted to use offset
def make_loft(doc, name, bot_w, bot_d, top_w, top_d, h, x, y, z, color, offset=(0,0,0)):
    # Bottom Rectangle
    p1 = App.Vector(-bot_w/2, -bot_d/2, 0)
    p2 = App.Vector(bot_w/2, -bot_d/2, 0)
    p3 = App.Vector(bot_w/2, bot_d/2, 0)
    p4 = App.Vector(-bot_w/2, bot_d/2, 0)
    wire_bot = Part.makePolygon([p1, p2, p3, p4, p1])
    
    # Top Rectangle
    p1t = App.Vector(-top_w/2, -top_d/2, h)
    p2t = App.Vector(top_w/2, -top_d/2, h)
    p3t = App.Vector(top_w/2, top_d/2, h)
    p4t = App.Vector(-top_w/2, top_d/2, h)
    wire_top = Part.makePolygon([p1t, p2t, p3t, p4t, p1t])
    
    # Loft
    loft = Part.makeLoft([wire_bot, wire_top], True)
    loft.translate(App.Vector(x + offset[0], y + offset[1], z + offset[2]))
    
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = loft
    obj.ViewObject.ShapeColor = color
    return obj

def make_transition(doc, name, face_w, face_d, duct_w, duct_d, length, x, y, z, orient_x, color, offset=(0,0,0)):
    # Creates a transition duct (pyramid on its side)
    # orient_x = 1 (points right), -1 (points left)
    
    # Large Face (Attached to housing)
    p1 = App.Vector(0, -face_d/2, 0)
    p2 = App.Vector(0, face_d/2, 0)
    p3 = App.Vector(0, face_d/2, face_w)
    p4 = App.Vector(0, -face_d/2, face_w)
    wire_large = Part.makePolygon([p1, p2, p3, p4, p1])
    
    # Small Face (Duct flange)
    dx = length * orient_x
    p1s = App.Vector(dx, -duct_d/2, (face_w - duct_w)/2)
    p2s = App.Vector(dx, duct_d/2, (face_w - duct_w)/2)
    p3s = App.Vector(dx, duct_d/2, (face_w - duct_w)/2 + duct_w)
    p4s = App.Vector(dx, -duct_d/2, (face_w - duct_w)/2 + duct_w)
    wire_small = Part.makePolygon([p1s, p2s, p3s, p4s, p1s])
    
    loft = Part.makeLoft([wire_large, wire_small], True)
    loft.translate(App.Vector(x + offset[0], y + offset[1], z + offset[2]))
    
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = loft
    obj.ViewObject.ShapeColor = color
    return obj

# ==========================================
# 4. MAIN BUILD ROUTINE
# ==========================================

def build_esp(doc, offset=(0,0,0)):
    """
    Builds the Electrostatic Precipitator at the specified offset coordinates.
    """
    
    # Z-Levels
    z_ground = 0
    z_housing_bot = leg_h
    z_hopper_tip = z_housing_bot - hopper_h
    z_roof = z_housing_bot + housing_h
    
    # --- A. HOPPERS ---
    outlet_size = 300.0
    for i in range(num_mods):
        cx = (i * mod_width) + (mod_width/2)
        # Hopper Body
        make_loft(doc, f"Hopper_{i}", outlet_size, outlet_size, mod_width, mod_depth, hopper_h, 
                  cx, 0, z_hopper_tip, col_casing, offset)
                  
        # Flange
        make_box(doc, f"Flange_{i}", 400, 400, 50, 
                 cx - 200, -200, z_hopper_tip - 50, col_stiffener, offset)

    # --- B. MAIN HOUSING (WALLS) ---
    # Back Wall
    make_box(doc, "Wall_Back", total_width, 20, housing_h, 
             0, mod_depth/2, z_housing_bot, col_casing, offset)
             
    # Left Wall
    make_box(doc, "Wall_Left", 20, mod_depth, housing_h, 
             0, -mod_depth/2, z_housing_bot, col_casing, offset)
             
    # Right Wall
    make_box(doc, "Wall_Right", 20, mod_depth, housing_h, 
             total_width - 20, -mod_depth/2, z_housing_bot, col_casing, offset)
             
    # Roof
    make_box(doc, "Roof", total_width + 100, mod_depth + 100, 100, 
             -50, -mod_depth/2 - 50, z_roof, col_casing, offset)
    
    # Front Wall with Cutaway (Boolean operation requires manual offset)
    # 1. Create solid wall
    wall_f = Part.makeBox(total_width, 20, housing_h)
    wall_f.translate(App.Vector(0, -mod_depth/2, z_housing_bot))
    
    # 2. Create Cutout shape (window)
    cutout = Part.makeBox(total_width * 0.5, 100, housing_h * 0.6)
    cutout.translate(App.Vector(total_width * 0.4, -mod_depth/2 - 40, z_housing_bot + (housing_h*0.2)))
    
    # 3. Perform Cut
    wall_f_cut = wall_f.cut(cutout)
    
    # 4. Apply Offset
    wall_f_cut.translate(App.Vector(offset[0], offset[1], offset[2]))
    
    obj_wf = doc.addObject("Part::Feature", "Wall_Front_Cutaway")
    obj_wf.Shape = wall_f_cut
    obj_wf.ViewObject.ShapeColor = col_casing

    # --- C. INTERNAL COMPONENTS (VISIBLE THROUGH CUTAWAY) ---
    # Collecting Plates (Green)
    plate_gap = 400
    num_plates = int((total_width - 200) / plate_gap)
    plate_h = housing_h * 0.8
    plate_d = mod_depth * 0.8
    
    for i in range(num_plates):
        px = 200 + (i * plate_gap)
        make_box(doc, f"Plate_{i}", 20, plate_d, plate_h, 
                 px, -plate_d/2, z_housing_bot + (housing_h*0.1), col_plates, offset)
    
    # Rapping Beams (Red - Top and Bottom)
    beam_w = total_width - 100
    beam_d = mod_depth - 200
    
    # Top Beam
    make_box(doc, "Beam_Int_Top", beam_w, beam_d, 200, 
             50, -beam_d/2, z_housing_bot + housing_h - 400, col_internal_beam, offset)
             
    # Bottom Beam
    make_box(doc, "Beam_Int_Bot", beam_w, beam_d, 200, 
             50, -beam_d/2, z_housing_bot + 400, col_internal_beam, offset)
    
    # Discharge Electrodes (Thin frames between plates)
    for i in range(num_plates - 1):
        ex = 200 + (i * plate_gap) + (plate_gap/2)
        make_box(doc, f"Electrode_{i}", 5, plate_d - 100, plate_h - 200, 
                 ex, -(plate_d-100)/2, z_housing_bot + (housing_h*0.1) + 100, col_structure, offset)

    # --- D. EXTERNAL STIFFENERS (RIBS) ---
    # Horizontal beams wrapping the housing
    num_ribs = 4
    rib_spacing = housing_h / (num_ribs + 1)
    
    for i in range(num_ribs):
        rz = z_housing_bot + ((i + 1) * rib_spacing)
        
        # Front Rib (Cut by window - requires manual boolean + offset)
        rib_f = Part.makeBox(total_width, 50, 100)
        rib_f.translate(App.Vector(0, -mod_depth/2 - 50, rz))
        rib_f_cut = rib_f.cut(cutout) # Use same cutout to trim rib
        rib_f_cut.translate(App.Vector(offset[0], offset[1], offset[2]))
        
        obj_rf = doc.addObject("Part::Feature", f"Rib_F_{i}")
        obj_rf.Shape = rib_f_cut
        obj_rf.ViewObject.ShapeColor = col_stiffener
        
        # Side/Back Ribs
        make_box(doc, f"Rib_B_{i}", total_width, 50, 100, 
                 0, mod_depth/2, rz, col_stiffener, offset)
                 
        make_box(doc, f"Rib_L_{i}", 50, mod_depth, 100, 
                 -50, -mod_depth/2, rz, col_stiffener, offset)
                 
        make_box(doc, f"Rib_R_{i}", 50, mod_depth, 100, 
                 total_width, -mod_depth/2, rz, col_stiffener, offset)

    # --- E. TRANSITION DUCTS (INLET/OUTLET) ---
    # Pyramidal diffusers on sides
    t_len = 1000.0
    t_duct_size = 1500.0
    
    # Left Transition (Inlet)
    make_transition(doc, "Trans_Inlet", housing_h - 400, mod_depth - 400, t_duct_size, t_duct_size, t_len, 
                    0, 0, z_housing_bot + 200, -1, col_casing, offset)
    
    # Right Transition (Outlet)
    make_transition(doc, "Trans_Outlet", housing_h - 400, mod_depth - 400, t_duct_size, t_duct_size, t_len, 
                    total_width, 0, z_housing_bot + 200, 1, col_casing, offset)

    # --- F. SUPPORT STRUCTURE ---
    # Legs at corners and middle
    leg_coords = [0, total_width/2, total_width]
    
    for lx in leg_coords:
        # Front Leg
        make_box(doc, f"Leg_F_{lx}", 150, 150, z_housing_bot, 
                 lx - 75, -mod_depth/2 - 75, 0, col_structure, offset)
        # Back Leg
        make_box(doc, f"Leg_B_{lx}", 150, 150, z_housing_bot, 
                 lx - 75, mod_depth/2 - 75, 0, col_structure, offset)
        
    # Cross Bracing (Simple X)
    brace = Part.makeBox(total_width + 200, 20, 100)
    # Manual rotation for X? Original code just placed a horizontal bar.
    # We will keep it simple as per original
    brace.translate(App.Vector(-100 + offset[0], -mod_depth/2 - 75 + offset[1], leg_h/2 + offset[2]))
    
    obj_br = doc.addObject("Part::Feature", "Brace_Horiz_F")
    obj_br.Shape = brace
    obj_br.ViewObject.ShapeColor = col_structure


def make_hopper_shape(doc, name, x, y, z, rot_angle, color, offset=(0,0,0)):
    # Specialized shape logic kept, but refactored for offset
    w_top, l_top = 800, 800
    w_bot, l_bot = 400, 400
    h = 600
    
    p1 = App.Vector(-l_bot/2, -w_bot/2, 0)
    p2 = App.Vector(l_bot/2, -w_bot/2, 0)
    p3 = App.Vector(l_bot/2, w_bot/2, 0)
    p4 = App.Vector(-l_bot/2, w_bot/2, 0)
    wire_bot = Part.makePolygon([p1, p2, p3, p4, p1])
    
    p1t = App.Vector(-l_top/2 - 200, -w_top/2, h)
    p2t = App.Vector(l_top/2 - 200, -w_top/2, h)
    p3t = App.Vector(l_top/2 - 200, w_top/2, h)
    p4t = App.Vector(-l_top/2 - 200, w_top/2, h)
    wire_top = Part.makePolygon([p1t, p2t, p3t, p4t, p1t])
    
    loft = Part.makeLoft([wire_bot, wire_top], True)
    
    # Apply local rotation
    if rot_angle != 0:
        loft.rotate(App.Vector(0,0,0), App.Vector(0,1,0), -rot_angle)
    
    # Apply translation with offset
    loft.translate(App.Vector(x + offset[0], y + offset[1], z + offset[2]))
    
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = loft
    obj.ViewObject.ShapeColor = color
    return obj

# ==========================================
# 4. MAIN BUILD ROUTINE
# ==========================================

def build_scrubber(doc, offset=(0,0,0)):
    """
    Builds the Rotary Scrubber at the specified offset coordinates.
    """
    rad = math.radians(incline_angle)
    pivot_x = 3000
    pivot_z = leg_base_height + 200
    
    # --- A. STRUCTURAL FRAME ---
    beam_len = drum_len + 500
    beam_h = 200
    beam_w = 100
    start_z = pivot_z + (beam_len * math.sin(rad))
    start_x = pivot_x - (beam_len * math.cos(rad))
    
    # Left Beam (Box rotated around Y)
    make_box(doc, "Beam_L", beam_len, beam_w, beam_h, 
             start_x, -frame_width/2, start_z, col_black, offset,
             rotation_angle=-incline_angle, rotation_axis=App.Vector(0,1,0))
             
    # Right Beam
    make_box(doc, "Beam_R", beam_len, beam_w, beam_h, 
             start_x, frame_width/2 - beam_w, start_z, col_black, offset,
             rotation_angle=-incline_angle, rotation_axis=App.Vector(0,1,0))
             
    # Legs
    fractions = [0.1, 0.5, 0.9]
    for i, frac in enumerate(fractions):
        dist = beam_len * frac
        local_h = start_z - (dist * math.sin(rad))
        local_x = start_x + (dist * math.cos(rad))
        
        make_box(doc, f"Leg_L_{i}", 150, 150, local_h, 
                 local_x, -frame_width/2 - 25, 0, col_black, offset)
                 
        make_box(doc, f"Leg_R_{i}", 150, 150, local_h, 
                 local_x, frame_width/2 - 125, 0, col_black, offset)
                 
        make_box(doc, f"Foot_L_{i}", 250, 250, 20, 
                 local_x-50, -frame_width/2 - 75, 0, col_black, offset)
                 
        make_box(doc, f"Foot_R_{i}", 250, 250, 20, 
                 local_x-50, frame_width/2 - 175, 0, col_black, offset)
                 
        make_box(doc, f"Brace_{i}", 100, frame_width, 100, 
                 local_x + 25, -frame_width/2, local_h - 300, col_black, offset)

    # --- B. ROLLERS ---
    roller_locs = [0.2, 0.8]
    for i, frac in enumerate(roller_locs):
        dist = beam_len * frac
        rx = start_x + (dist * math.cos(rad))
        rz = start_z - (dist * math.sin(rad)) + beam_h
        
        # Roller Brackets
        make_box(doc, f"RollerBracket_L_{i}", 300, 100, 150, 
                 rx, -frame_width/2, rz, col_sepro_blue, offset,
                 rotation_angle=-incline_angle, rotation_axis=App.Vector(0,1,0))
                 
        make_box(doc, f"RollerBracket_R_{i}", 300, 100, 150, 
                 rx, frame_width/2 - 100, rz, col_sepro_blue, offset,
                 rotation_angle=-incline_angle, rotation_axis=App.Vector(0,1,0))
        
        # Left Wheel
        # Cylinder axis (1,0,0) -> Rotated 90 around Y. Then rotated -incline around Y.
        # This requires manual logic because helper make_cylinder aligns to cardinal axes first.
        # We'll create the shape, apply compound rotation, then translate with offset manually.
        
        w_shape = Part.makeCylinder(80, 50)
        w_shape.rotate(App.Vector(0,0,0), App.Vector(1,0,0), 90) # Orient horizontal (rolling direction)
        w_shape.rotate(App.Vector(0,0,0), App.Vector(0,1,0), -incline_angle) # Match incline
        
        # Calculate position + offset
        wx_l = rx + 150 + offset[0]
        wy_l = -frame_width/2 + 100 + offset[1]
        wz_l = rz + 150 + offset[2]
        
        w_shape.translate(App.Vector(wx_l, wy_l, wz_l))
        
        obj_wl = doc.addObject("Part::Feature", f"Wheel_L_{i}")
        obj_wl.Shape = w_shape
        obj_wl.ViewObject.ShapeColor = col_black
        
        # Right Wheel
        w_shape_r = Part.makeCylinder(80, 50)
        w_shape_r.rotate(App.Vector(0,0,0), App.Vector(1,0,0), 90)
        w_shape_r.rotate(App.Vector(0,0,0), App.Vector(0,1,0), -incline_angle)
        
        wx_r = rx + 150 + offset[0]
        wy_r = frame_width/2 - 150 + offset[1]
        wz_r = rz + 150 + offset[2]
        
        w_shape_r.translate(App.Vector(wx_r, wy_r, wz_r))
        
        obj_wr = doc.addObject("Part::Feature", f"Wheel_R_{i}")
        obj_wr.Shape = w_shape_r
        obj_wr.ViewObject.ShapeColor = col_black

    # --- C. DRUM ---
    drum_offset_z = 600
    drum_start_x = start_x + 200
    drum_start_z = start_z + beam_h + drum_offset_z
    seg_len = drum_len / 3
    
    for i in range(3):
        seg_dist = i * seg_len
        sx = drum_start_x + (seg_dist * math.cos(rad))
        sz = drum_start_z - (seg_dist * math.sin(rad))
        
        # Segment (Cylinder)
        # Helper make_cylinder axis=1,0,0 rotates 90 Y (aligns X).
        # We need alignment X, THEN rotation -incline around Y.
        # Since helper applies rotation_angle AFTER initial alignment, this works:
        # axis=(1,0,0) -> aligns with X
        # rotation_angle = -incline, rotation_axis = (0,1,0) -> rotates around Y
        
        # However, make_cylinder axis logic: 
        # if axis=(1,0,0): rotate (0,0,0), (0,1,0), 90.
        # We can't easily pass the compound rotation into the specific helper signature 
        # without modifying the helper or doing it manually like the wheels.
        # But wait, make_cylinder takes axis=Vector(). If we pass the actual inclined vector?
        # The helper logic provided hardcodes checks for (1,0,0) or (0,1,0).
        # We will do manual shape creation for complex rotations to ensure accuracy.
        
        cyl = Part.makeCylinder(drum_dia/2, seg_len)
        cyl.rotate(App.Vector(0,0,0), App.Vector(0,1,0), 90) # Align X
        cyl.rotate(App.Vector(0,0,0), App.Vector(0,1,0), -incline_angle) # Incline
        cyl.translate(App.Vector(sx + offset[0], offset[1], sz + offset[2]))
        
        obj_seg = doc.addObject("Part::Feature", f"DrumSeg_{i}")
        obj_seg.Shape = cyl
        obj_seg.ViewObject.ShapeColor = col_sepro_blue
        
        # Flange
        fx = sx + (seg_len * math.cos(rad))
        fz = sz - (seg_len * math.sin(rad))
        
        flange = Part.makeCylinder(drum_dia/2 + 40, 40)
        flange.rotate(App.Vector(0,0,0), App.Vector(0,1,0), 90)
        flange.rotate(App.Vector(0,0,0), App.Vector(0,1,0), -incline_angle)
        flange.translate(App.Vector(fx + offset[0], offset[1], fz + offset[2]))
        
        obj_fl = doc.addObject("Part::Feature", f"Flange_{i}")
        obj_fl.Shape = flange
        obj_fl.ViewObject.ShapeColor = col_metal
        
        # Tire
        if i != 1:
            tire_offset = seg_len * 0.5
            tx = sx + (tire_offset * math.cos(rad))
            tz = sz - (tire_offset * math.sin(rad))
            
            tire = Part.makeCylinder(drum_dia/2 + 20, 150)
            tire.rotate(App.Vector(0,0,0), App.Vector(0,1,0), 90)
            tire.rotate(App.Vector(0,0,0), App.Vector(0,1,0), -incline_angle)
            tire.translate(App.Vector(tx + offset[0], offset[1], tz + offset[2]))
            
            obj_tr = doc.addObject("Part::Feature", f"Tire_{i}")
            obj_tr.Shape = tire
            obj_tr.ViewObject.ShapeColor = col_metal

    # --- D. INLET & OUTLET ---
    make_hopper_shape(doc, "InletHopper", drum_start_x, 0, drum_start_z + 200, incline_angle, col_sepro_blue, offset)
    
    end_dist = drum_len
    ex = drum_start_x + (end_dist * math.cos(rad))
    ez = drum_start_z - (end_dist * math.sin(rad))
    
    pipe = Part.makeCylinder(drum_dia/2 - 100, 800)
    pipe.rotate(App.Vector(0,0,0), App.Vector(0,1,0), 90)
    pipe.rotate(App.Vector(0,0,0), App.Vector(0,1,0), -incline_angle)
    pipe.translate(App.Vector(ex + offset[0], offset[1], ez + offset[2]))
    
    obj_out = doc.addObject("Part::Feature", "OutletPipe")
    obj_out.Shape = pipe
    obj_out.ViewObject.ShapeColor = col_black

    # --- E. VENTS ---
    for i, dist_add in enumerate([1000, 2500]):
        px = drum_start_x + (dist_add * math.cos(rad))
        pz = drum_start_z - (dist_add * math.sin(rad))
        
        port = Part.makeCylinder(60, 400)
        port.rotate(App.Vector(0,0,0), App.Vector(0,1,0), -incline_angle) # Just incline (vertical relative to drum?)
        
        # Calculate shift relative to drum axis to place on top
        shift_z = (drum_dia/2) * math.cos(rad)
        shift_x = (drum_dia/2) * math.sin(rad)
        
        port.translate(App.Vector(px + shift_x + offset[0], offset[1], pz + shift_z + offset[2]))
        
        obj_pt = doc.addObject("Part::Feature", f"Vent_{i}")
        obj_pt.Shape = port
        obj_pt.ViewObject.ShapeColor = col_black




def build_swan_neck_conveyor(doc, offset=(0,0,0)):
    """
    Builds a Z-shape / Swan-neck conveyor at the specified offset.
    """
    
    # --- CALCULATION ---
    rad = math.radians(incline_angle)
    
    # Key Points (local coordinates relative to offset)
    # P1: Start of bottom section
    p1_x, p1_z = 0, leg_base_height
    
    # P2: Knee (End of bottom, Start of incline)
    p2_x, p2_z = bottom_len, leg_base_height
    
    # P3: Elbow (End of incline, Start of top)
    incline_run = incline_len * math.cos(rad)
    incline_rise = incline_len * math.sin(rad)
    p3_x = p2_x + incline_run
    p3_z = p2_z + incline_rise
    
    # P4: End of top section
    p4_x = p3_x + top_len
    p4_z = p3_z
    
    rail_h = 150.0
    guard_h = 250.0
    
    # ==========================
    # A. FRAME (Blue Channels)
    # ==========================
    
    # 1. Bottom Section Frame
    make_box(doc, "Frame_Bot_L", bottom_len, 50, rail_h, 
             p1_x, 0, p1_z - rail_h, col_frame_blue, offset)
    make_box(doc, "Frame_Bot_R", bottom_len, 50, rail_h, 
             p1_x, frame_width - 50, p1_z - rail_h, col_frame_blue, offset)
             
    # 2. Incline Section Frame
    make_box(doc, "Frame_Inc_L", incline_len, 50, rail_h, 
             p2_x, 0, p2_z - rail_h, col_frame_blue, offset,
             rotation_angle=-incline_angle, rotation_axis=App.Vector(0,1,0))
             
    make_box(doc, "Frame_Inc_R", incline_len, 50, rail_h, 
             p2_x, frame_width - 50, p2_z - rail_h, col_frame_blue, offset,
             rotation_angle=-incline_angle, rotation_axis=App.Vector(0,1,0))
             
    # 3. Top Section Frame
    make_box(doc, "Frame_Top_L", top_len, 50, rail_h, 
             p3_x, 0, p3_z - rail_h, col_frame_blue, offset)
    make_box(doc, "Frame_Top_R", top_len, 50, rail_h, 
             p3_x, frame_width - 50, p3_z - rail_h, col_frame_blue, offset)

    # ==========================
    # B. LEGS (Blue Supports)
    # ==========================
    leg_dim = 80.0
    
    # Leg Locations (X coordinates)
    leg_xs = [200, bottom_len - 200, p3_x + 200, p4_x - 200]
    mid_inc_x = p2_x + (incline_run / 2)
    
    for i, lx in enumerate(leg_xs + [mid_inc_x]):
        if lx <= p2_x: 
            lz = p1_z - rail_h
        elif lx >= p3_x: 
            lz = p3_z - rail_h
        else: 
            dist_along = (lx - p2_x)
            lz = (p2_z - rail_h) + (dist_along * math.tan(rad))
            
        make_box(doc, f"Leg_L_{i}", leg_dim, leg_dim, lz, 
                 lx, 0, 0, col_frame_blue, offset)
        make_box(doc, f"Leg_R_{i}", leg_dim, leg_dim, lz, 
                 lx, frame_width - leg_dim, 0, col_frame_blue, offset)
        make_box(doc, f"Cross_{i}", leg_dim, frame_width, leg_dim, 
                 lx, 0, lz - 200, col_frame_blue, offset)
        make_box(doc, f"Foot_L_{i}", leg_dim + 40, leg_dim + 40, 10, 
                 lx-20, -20, 0, col_frame_blue, offset)
        make_box(doc, f"Foot_R_{i}", leg_dim + 40, leg_dim + 40, 10, 
                 lx-20, frame_width - leg_dim - 20, 0, col_frame_blue, offset)

    # ==========================
    # C. BELT & PULLEYS
    # ==========================
    belt_thick = 10.0
    belt_y = (frame_width - belt_width) / 2
    
    make_box(doc, "Belt_Bot", bottom_len, belt_width, belt_thick, 
             p1_x, belt_y, p1_z, col_belt_black, offset)
             
    make_box(doc, "Belt_Inc", incline_len, belt_width, belt_thick, 
             p2_x, belt_y, p2_z, col_belt_black, offset,
             rotation_angle=-incline_angle, rotation_axis=App.Vector(0,1,0))
             
    make_box(doc, "Belt_Top", top_len, belt_width, belt_thick, 
             p3_x, belt_y, p3_z, col_belt_black, offset)
             
    make_cylinder(doc, "Pulley_Head", 100, belt_width + 20, 
                  p4_x, belt_y - 10, p3_z - 50, col_belt_black, offset, axis=App.Vector(0,1,0))
                  
    make_cylinder(doc, "Pulley_Tail", 100, belt_width + 20, 
                  p1_x, belt_y - 10, p1_z - 50, col_belt_black, offset, axis=App.Vector(0,1,0))

    # ==========================
    # D. ROLLERS
    # ==========================
    roller_spacing = 500.0
    roller_r = 40.0
    
    # Bottom Rollers
    num_bot = int(bottom_len / roller_spacing)
    for i in range(num_bot):
        rx = (i + 0.5) * roller_spacing
        make_cylinder(doc, f"Roller_Bot_{i}", roller_r, belt_width, 
                      rx, belt_y, p1_z - roller_r, col_roller_red, offset, axis=App.Vector(0,1,0))
                      
    # Incline Rollers (Manual Shape for correct rotation)
    num_inc = int(incline_len / roller_spacing)
    for i in range(num_inc):
        dist = (i + 0.5) * roller_spacing
        rx_local = dist * math.cos(rad)
        rz_local = dist * math.sin(rad)
        
        cyl = Part.makeCylinder(roller_r, belt_width)
        cyl.rotate(App.Vector(0,0,0), App.Vector(1,0,0), -90) 
        cyl.rotate(App.Vector(0,0,0), App.Vector(0,1,0), -incline_angle)
        cyl.translate(App.Vector(p2_x + rx_local + offset[0], belt_y + offset[1], p2_z + rz_local - roller_r + offset[2]))
        
        obj_r = doc.addObject("Part::Feature", f"Roller_Inc_{i}")
        obj_r.Shape = cyl
        obj_r.ViewObject.ShapeColor = col_roller_red

    # Top Rollers
    num_top = int(top_len / roller_spacing)
    for i in range(num_top):
        rx = p3_x + (i + 0.5) * roller_spacing
        make_cylinder(doc, f"Roller_Top_{i}", roller_r, belt_width, 
                      rx, belt_y, p3_z - roller_r, col_roller_red, offset, axis=App.Vector(0,1,0))

    # ==========================
    # E. SIDE GUARDS / HOPPERS
    # ==========================
    make_box(doc, "Guard_Bot_L", bottom_len, 10, guard_h, 
             p1_x, 0, p1_z, col_guard_beige, offset)
    make_box(doc, "Guard_Bot_R", bottom_len, 10, guard_h, 
             p1_x, frame_width - 10, p1_z, col_guard_beige, offset)
             
    make_box(doc, "Guard_Inc_L", incline_len, 10, guard_h, 
             p2_x, 0, p2_z, col_guard_beige, offset,
             rotation_angle=-incline_angle, rotation_axis=App.Vector(0,1,0))
    make_box(doc, "Guard_Inc_R", incline_len, 10, guard_h, 
             p2_x, frame_width - 10, p2_z, col_guard_beige, offset,
             rotation_angle=-incline_angle, rotation_axis=App.Vector(0,1,0))
             
    make_box(doc, "Guard_Top_L", top_len, 10, guard_h, 
             p3_x, 0, p3_z, col_guard_beige, offset)
    make_box(doc, "Guard_Top_R", top_len, 10, guard_h, 
             p3_x, frame_width - 10, p3_z, col_guard_beige, offset)

def make_spring_visual(doc, name, r, h, coils, x, y, z, offset=(0,0,0)):
    pitch = h / coils
    rings = []
    wire_r = 20.0  # Scaled from 2.0 to 20.0
    
    for i in range(coils):
        torus = Part.makeTorus(r, wire_r)
        torus.translate(App.Vector(x + offset[0], y + offset[1], z + (i * pitch) + offset[2]))
        rings.append(torus)
        
    comp = Part.makeCompound(rings)
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = comp
    obj.ViewObject.ShapeColor = mag_col_chrome

# ==========================================
# 4. MAIN BUILD ROUTINE
# ==========================================

def build_separator(doc, offset=(0,0,0)):
    """
    Builds the Magnetic Separator (10x Scale) at the specified offset.
    """
    
    # --- A. MAIN TANK BODY ---
    outer_box = Part.makeBox(mag_tank_len, mag_tank_width, mag_tank_height)
    inner_box = Part.makeBox(mag_tank_len - mag_wall_thick*2, mag_tank_width - mag_wall_thick*2, mag_tank_height)
    inner_box.translate(App.Vector(mag_wall_thick, mag_wall_thick, mag_wall_thick))
    
    # Cut inlet cutout at front top (Scaled 10x: 100->1000, 50->500)
    cutout = Part.makeBox(1000, mag_tank_width, 500)
    cutout.translate(App.Vector(mag_tank_len - 1000, 0, mag_tank_height - 500))
    
    tank_shape = outer_box.cut(inner_box).cut(cutout)
    tank_shape.translate(App.Vector(offset[0], offset[1], offset[2]))
    
    obj_tank = doc.addObject("Part::Feature", "TankBody")
    obj_tank.Shape = tank_shape
    obj_tank.ViewObject.ShapeColor = mag_col_grey_paint
    
    # Side Box (Motor Cover) - Left side (Scaled 10x: 50->500, 20->200)
    make_box(doc, "SideCover", mag_tank_len - 500, mag_side_box_width, mag_tank_height - 200, 
             0, -mag_side_box_width, 200, mag_col_grey_paint, offset)

    # --- B. DRUM & ROLLER ---
    # Position (Scaled 10x: 100->1000, 20->200)
    drum_x = 1000
    drum_z = mag_tank_height + 200
    
    # Main Drum (Lower)
    make_cylinder(doc, "MagneticDrum", mag_drum_dia/2, mag_drum_len, 
                  drum_x, mag_wall_thick, drum_z, mag_col_rubber, offset, axis=App.Vector(0,1,0))
    
    # Top Roller (Pressure)
    roller_z = drum_z + (mag_drum_dia/2) + (mag_roller_dia/2)
    make_cylinder(doc, "TopRoller", mag_roller_dia/2, mag_drum_len, 
                  drum_x, mag_wall_thick, roller_z, mag_col_rubber, offset, axis=App.Vector(0,1,0))
    
    # Bearings (Scaled 10x: 25->250, 10->100)
    make_cylinder(doc, "Bearing_L", 250, 100, 
                  drum_x, mag_wall_thick - 100, roller_z, mag_col_chrome, offset, axis=App.Vector(0,1,0))
    make_cylinder(doc, "Bearing_R", 250, 100, 
                  drum_x, mag_tank_width - mag_wall_thick, roller_z, mag_col_chrome, offset, axis=App.Vector(0,1,0))

    # --- C. SPRING TENSIONERS ---
    for side in [0, 1]:
        # (Scaled 10x: 15->150)
        y_pos = mag_wall_thick - 150 if side == 0 else mag_tank_width - mag_wall_thick + 150
        
        # 1. Vertical Rod (Scaled 10x: h 150->1500, r 6->60, x-40->x-400)
        rod_h = 1500
        rod_z = mag_tank_height
        make_cylinder(doc, f"Rod_{side}", 60, rod_h, 
                      drum_x - 400, y_pos, rod_z, mag_col_chrome, offset)
        
        # 2. Horizontal Arm (Scaled 10x: 80x20x20 -> 800x200x200)
        make_box(doc, f"Arm_{side}", 800, 200, 200, 
                 drum_x - 400, y_pos - 100, roller_z - 100, mag_col_steel, offset)
        
        # 3. Spring (Scaled 10x: r 10->100, h 60->600)
        make_spring_visual(doc, f"Spring_{side}", 100, 600, 10, 
                           drum_x - 400, y_pos, roller_z + 100, offset)
        
        # 4. Wingnut (Scaled 10x: Cone 8,4,10 -> 80,40,100 | Wings 40,5,10 -> 400,50,100)
        wn_z = roller_z + 100 + 600
        wn_cone = Part.makeCone(80, 40, 100)
        wn_cone.translate(App.Vector(drum_x - 400, y_pos, wn_z))
        wn_wings = Part.makeBox(400, 50, 100)
        wn_wings.translate(App.Vector(drum_x - 600, y_pos - 25, wn_z + 50))
        
        wn_shape = wn_cone.fuse(wn_wings)
        wn_shape.translate(App.Vector(offset[0], offset[1], offset[2]))
        
        obj_wn = doc.addObject("Part::Feature", f"Wingnut_{side}")
        obj_wn.Shape = wn_shape
        obj_wn.ViewObject.ShapeColor = mag_col_brass

    # --- D. DISCHARGE CHUTE ---
    chute_angle = 35 
    
    # 1. Bottom Plate (Scaled 10x: Thick 2->20, x+50->x+500, z-20->z-200)
    make_box(doc, "ChutePlate", mag_chute_len, mag_chute_width, 20, 
             drum_x + 500, mag_wall_thick, drum_z - 200, mag_col_steel, offset,
             rotation_angle=chute_angle, rotation_axis=App.Vector(0,1,0))
    
    # 2. Side Walls of Chute (Scaled 10x: height 50->500, thick 2->20)
    p1 = App.Vector(0,0,0)
    p2 = App.Vector(mag_chute_len, 0, 0)
    p3 = App.Vector(0, 0, 500) 
    
    wire = Part.makePolygon([p1, p2, p3, p1])
    face = Part.Face(wire)
    wall_tri = face.extrude(App.Vector(0, 20, 0)) 
    wall_tri.rotate(App.Vector(0,0,0), App.Vector(0,1,0), chute_angle)
    
    # Left Wall
    w1 = wall_tri.copy()
    w1.translate(App.Vector(drum_x + 500 + offset[0], mag_wall_thick + offset[1], drum_z - 200 + offset[2]))
    obj_cw1 = doc.addObject("Part::Feature", "ChuteWall_L")
    obj_cw1.Shape = w1
    obj_cw1.ViewObject.ShapeColor = mag_col_steel
    
    # Right Wall (Scaled 10x thick adjust: -2 -> -20)
    w2 = wall_tri.copy()
    w2.translate(App.Vector(drum_x + 500 + offset[0], mag_wall_thick + mag_chute_width - 20 + offset[1], drum_z - 200 + offset[2]))
    obj_cw2 = doc.addObject("Part::Feature", "ChuteWall_R")
    obj_cw2.Shape = w2
    obj_cw2.ViewObject.ShapeColor = mag_col_steel

    # --- E. OUTLET PORT (Scaled 10x: dia 600, len 400, x-800, z 500) ---
    port_dia = 600
    port_len = 400
    px = mag_tank_len - 800
    py = mag_tank_width
    pz = 500
    
    cyl_out = Part.makeCylinder(port_dia/2 + 100, port_len)
    cyl_out.rotate(App.Vector(0,0,0), App.Vector(1,0,0), -90)
    cyl_out.translate(App.Vector(px, py, pz))
    
    cyl_hole = Part.makeCylinder(port_dia/2, port_len + 100)
    cyl_hole.rotate(App.Vector(0,0,0), App.Vector(1,0,0), -90)
    cyl_hole.translate(App.Vector(px, py - 50, pz))
    
    port_shape = cyl_out.cut(cyl_hole)
    
    # Rings (Scaled 10x: Torus 2->20, spacing 10->100)
    for i in range(3):
        ring = Part.makeTorus(port_dia/2, 20)
        ring.rotate(App.Vector(0,0,0), App.Vector(1,0,0), 90)
        ring.translate(App.Vector(px, py + 100 + (i*100), pz))
        port_shape = port_shape.fuse(ring)
        
    port_shape.translate(App.Vector(offset[0], offset[1], offset[2]))
    obj_port = doc.addObject("Part::Feature", "OutletPort")
    obj_port.Shape = port_shape
    obj_port.ViewObject.ShapeColor = mag_col_grey_paint

    # --- F. MOUNTING FEET (Scaled 10x: 40->400, 10->100, hole 6->60) ---
    foot_sz = 400
    coords = [
        (0, -mag_side_box_width), 
        (mag_tank_len - foot_sz, -mag_side_box_width),
        (0, mag_tank_width),
        (mag_tank_len - foot_sz, mag_tank_width)
    ]
    
    for i, (fx, fy) in enumerate(coords):
        foot = Part.makeBox(foot_sz, foot_sz, 100)
        hole = Part.makeCylinder(60, 200)
        hole.translate(App.Vector(foot_sz/2, foot_sz/2, 0))
        foot = foot.cut(hole)
        foot.translate(App.Vector(fx + offset[0], fy + offset[1], offset[2]))
        
        obj_f = doc.addObject("Part::Feature", f"Foot_{i}")
        obj_f.Shape = foot
        obj_f.ViewObject.ShapeColor = mag_col_grey_paint



def build_ball_mill(offset=(0, 0, 0)):
    doc = ensure_document()
    
    # --- A. BASE FRAME STRUCTURE ---
    mill_beam_thickness = 200.0
    
    make_box(doc, "BM_BaseBeam_Left", ballmill_base_frame_len, mill_beam_thickness, mill_beam_thickness, 
             -ballmill_base_frame_len/2, -ballmill_base_frame_width/2, 0, ballmill_color_foundation, offset)
    
    make_box(doc, "BM_BaseBeam_Right", ballmill_base_frame_len, mill_beam_thickness, mill_beam_thickness, 
             -ballmill_base_frame_len/2, ballmill_base_frame_width/2 - mill_beam_thickness, 0, ballmill_color_foundation, offset)
    
    make_box(doc, "BM_BaseCross_Front", mill_beam_thickness, ballmill_base_frame_width - (2*mill_beam_thickness), mill_beam_thickness, 
             ballmill_base_frame_len/2 - mill_beam_thickness, -ballmill_base_frame_width/2 + mill_beam_thickness, 0, ballmill_color_foundation, offset)
    
    make_box(doc, "BM_BaseCross_Back", mill_beam_thickness, ballmill_base_frame_width - (2*mill_beam_thickness), mill_beam_thickness, 
             -ballmill_base_frame_len/2, -ballmill_base_frame_width/2 + mill_beam_thickness, 0, ballmill_color_foundation, offset)
    
    # --- B. SUPPORT PEDESTALS ---
    mill_pedestal_len = 400.0
    mill_ped_height = ballmill_rotation_axis_height - 400.0
    mill_ped_x_pos = ballmill_base_frame_len/2 - 400.0
    
    # Feed/Gear Side Pedestal
    make_box(doc, "BM_Pedestal_Feed", mill_pedestal_len, ballmill_base_frame_width, mill_ped_height, 
             mill_ped_x_pos, -ballmill_base_frame_width/2, mill_beam_thickness, ballmill_color_primary, offset)
    make_box(doc, "BM_Bearing_Housing_Feed", 500, 1000, 500, 
             mill_ped_x_pos - 50, -500, mill_beam_thickness + mill_ped_height, ballmill_color_primary, offset)
    
    # Discharge Side Pedestal
    mill_tail_x = -ballmill_base_frame_len/2 + 200.0
    make_box(doc, "BM_Pedestal_Discharge", mill_pedestal_len, ballmill_base_frame_width, mill_ped_height, 
             mill_tail_x, -ballmill_base_frame_width/2, mill_beam_thickness, ballmill_color_primary, offset)
    make_box(doc, "BM_Bearing_Housing_Discharge", 500, 1000, 500, 
             mill_tail_x - 50, -500, mill_beam_thickness + mill_ped_height, ballmill_color_primary, offset)

    # --- C. REVOLVING DRUM ASSEMBLY ---
    # Drum Shell
    drum_shell = Part.makeCylinder(ballmill_drum_diameter/2, ballmill_drum_length)
    drum_shell.rotate(App.Vector(0,0,0), App.Vector(0,1,0), 90)
    drum_shell.translate(App.Vector(-ballmill_drum_length/2 + offset[0], 0 + offset[1], ballmill_rotation_axis_height + offset[2]))
    
    obj_shell = doc.addObject("Part::Feature", "BM_Drum_Shell")
    obj_shell.Shape = drum_shell
    obj_shell.ViewObject.ShapeColor = ballmill_color_primary
    
    # Shell End Flanges
    mill_flange_width = 80.0
    mill_flange_dia = ballmill_drum_diameter + 100.0
    make_cylinder(doc, "BM_Flange_A", mill_flange_dia/2, mill_flange_width, 
                  ballmill_drum_length/2, 0, ballmill_rotation_axis_height, ballmill_color_primary, offset, axis=App.Vector(1,0,0))
    make_cylinder(doc, "BM_Flange_B", mill_flange_dia/2, mill_flange_width, 
                  -ballmill_drum_length/2 - mill_flange_width, 0, ballmill_rotation_axis_height, ballmill_color_primary, offset, axis=App.Vector(1,0,0))
    
    # End Cone Sections
    mill_cone_length = 400.0
    mill_trunnion_dia = 500.0
    
    # Forward Cone
    mill_cone_1 = Part.makeCone(mill_flange_dia/2, mill_trunnion_dia/2, mill_cone_length)
    mill_cone_1.rotate(App.Vector(0,0,0), App.Vector(0,1,0), 90)
    mill_cone_1.translate(App.Vector(ballmill_drum_length/2 + mill_flange_width + offset[0], offset[1], ballmill_rotation_axis_height + offset[2]))
    obj_c1 = doc.addObject("Part::Feature", "BM_Cone_Forward")
    obj_c1.Shape = mill_cone_1
    obj_c1.ViewObject.ShapeColor = ballmill_color_primary
    
    # Rear Cone
    mill_cone_2 = Part.makeCone(mill_flange_dia/2, mill_trunnion_dia/2, mill_cone_length)
    mill_cone_2.rotate(App.Vector(0,0,0), App.Vector(0,1,0), -90)
    mill_cone_2.translate(App.Vector(-ballmill_drum_length/2 - mill_flange_width + offset[0], offset[1], ballmill_rotation_axis_height + offset[2]))
    obj_c2 = doc.addObject("Part::Feature", "BM_Cone_Rear")
    obj_c2.Shape = mill_cone_2
    obj_c2.ViewObject.ShapeColor = ballmill_color_primary
    
    # Supporting Trunnions
    make_cylinder(doc, "BM_Trunnion_Feed", mill_trunnion_dia/2 - 50, 400, 
                  ballmill_drum_length/2 + mill_flange_width + mill_cone_length, 0, ballmill_rotation_axis_height, ballmill_color_primary, offset, axis=App.Vector(1,0,0))
    make_cylinder(doc, "BM_Trunnion_Discharge", mill_trunnion_dia/2 - 50, 400, 
                  -ballmill_drum_length/2 - mill_flange_width - mill_cone_length - 400, 0, ballmill_rotation_axis_height, ballmill_color_primary, offset, axis=App.Vector(1,0,0))

    # --- D. DRIVE GIRTH GEAR ---
    mill_gear_x_pos = (ballmill_drum_length/2) - 300
    mill_gear_base = Part.makeCylinder(ballmill_girth_gear_dia/2, ballmill_girth_gear_width)
    mill_gear_base.rotate(App.Vector(0,0,0), App.Vector(0,1,0), 90)
    mill_gear_base.translate(App.Vector(mill_gear_x_pos + offset[0], offset[1], ballmill_rotation_axis_height + offset[2]))
    
    obj_gear = doc.addObject("Part::Feature", "BM_Girth_Gear_Base")
    obj_gear.Shape = mill_gear_base
    obj_gear.ViewObject.ShapeColor = ballmill_color_primary
    
    # Gear Teeth Modeling
    mill_tooth_qty = 60
    mill_tooth_h, mill_tooth_w = 60.0, 40.0
    mill_teeth_list = []
    for i in range(mill_tooth_qty):
        tooth_angle = (360.0 / mill_tooth_qty) * i
        mill_t_shape = Part.makeBox(ballmill_girth_gear_width, mill_tooth_w, mill_tooth_h)
        mill_t_shape.translate(App.Vector(0, -mill_tooth_w/2, -mill_tooth_h/2))
        mill_t_shape.translate(App.Vector(0, 0, ballmill_girth_gear_dia/2))
        mill_t_shape.rotate(App.Vector(0,0,0), App.Vector(1,0,0), tooth_angle)
        mill_t_shape.translate(App.Vector(mill_gear_x_pos + offset[0], offset[1], ballmill_rotation_axis_height + offset[2]))
        mill_teeth_list.append(mill_t_shape)
    
    obj_teeth = doc.addObject("Part::Feature", "BM_Gear_Teeth")
    obj_teeth.Shape = Part.makeCompound(mill_teeth_list)
    obj_teeth.ViewObject.ShapeColor = ballmill_color_gears

    # --- E. LINER FASTENERS (BOLTS) ---
    mill_row_qty, mill_linear_qty = 12, 8
    mill_bolt_pitch = ballmill_drum_length / (mill_linear_qty + 1)
    mill_bolts_list = []
    for r in range(mill_row_qty):
        bolt_angle = (360.0 / mill_row_qty) * r
        for l in range(mill_linear_qty):
            bolt_x = -ballmill_drum_length/2 + (l + 1) * mill_bolt_pitch
            if abs(bolt_x - mill_gear_x_pos) < 200: continue
            mill_bolt = Part.makeCone(15, 10, 25)
            mill_bolt.translate(App.Vector(0, 0, ballmill_drum_diameter/2))
            mill_bolt.rotate(App.Vector(0,0,0), App.Vector(1,0,0), bolt_angle)
            mill_bolt.translate(App.Vector(bolt_x + offset[0], offset[1], ballmill_rotation_axis_height + offset[2]))
            mill_bolts_list.append(mill_bolt)
            
    obj_fasteners = doc.addObject("Part::Feature", "BM_Liner_Fasteners")
    obj_fasteners.Shape = Part.makeCompound(mill_bolts_list)
    obj_fasteners.ViewObject.ShapeColor = ballmill_color_components

    # --- F. TRUNNION BEARING CAPS ---
    mill_cap_radius, mill_cap_thick = 300.0, 50.0
    mill_cap_x_pos = ballmill_drum_length/2 + mill_flange_width + mill_cone_length + 400.0
    
    mill_cap_main = Part.makeCylinder(mill_cap_radius, mill_cap_thick)
    mill_cap_main.rotate(App.Vector(0,0,0), App.Vector(0,1,0), 90)
    
    mill_cap_bore = Part.makeCylinder(150, mill_cap_thick + 10)
    mill_cap_bore.rotate(App.Vector(0,0,0), App.Vector(0,1,0), 90)
    
    mill_cap_final = mill_cap_main.cut(mill_cap_bore)
    mill_cap_final.translate(App.Vector(mill_cap_x_pos + offset[0], offset[1], ballmill_rotation_axis_height + offset[2]))
    
    obj_cap = doc.addObject("Part::Feature", "BM_Bearing_Seal_Cap")
    obj_cap.Shape = mill_cap_final
    obj_cap.ViewObject.ShapeColor = ballmill_color_primary
    
    for i in range(8):
        bolt_circ_angle = (360/8) * i
        mill_arc = math.radians(bolt_circ_angle)
        mill_cy = 220 * math.cos(mill_arc)
        mill_cz = 220 * math.sin(mill_arc) + ballmill_rotation_axis_height
        make_cylinder(doc, f"BM_CapBolt_{i}", 15, 30, mill_cap_x_pos + mill_cap_thick, mill_cy, mill_cz, 
                      ballmill_color_components, offset, axis=App.Vector(1,0,0))



def build_trommel(offset=(0, 0, 0)):
    doc = ensure_document()
    # Height of the drum center
    trommel_z_axis = trommel_support_leg_height + (trommel_drum_dia/2) + 200
    
    # --- A. THE DRUM ASSEMBLY ---
    # Screen Mesh (Manual cut for thickness, then translate by offset)
    outer_cyl = Part.makeCylinder(trommel_drum_dia/2, trommel_drum_len)
    inner_cyl = Part.makeCylinder(trommel_drum_dia/2 - 20, trommel_drum_len)
    mesh_shape = outer_cyl.cut(inner_cyl)
    mesh_shape.rotate(App.Vector(0,0,0), App.Vector(0,1,0), 90)
    mesh_shape.translate(App.Vector(offset[0], offset[1], trommel_z_axis + offset[2]))
    
    obj_mesh = doc.addObject("Part::Feature", "Trommel_Mesh")
    obj_mesh.Shape = mesh_shape
    obj_mesh.ViewObject.ShapeColor = trommel_col_mesh_red
    obj_mesh.ViewObject.Transparency = 25
    
    # Longitudinal Ribs (Cage)
    num_ribs = 8
    for i in range(num_ribs):
        angle = (360.0 / num_ribs) * i
        rad = math.radians(angle)
        ry = (trommel_drum_dia/2) * math.cos(rad)
        rz = (trommel_drum_dia/2) * math.sin(rad)
        
        make_box(doc, f"Trommel_Rib_{i}", trommel_drum_len, 50, 50, 
                 0, ry, trommel_z_axis + rz - 25, trommel_col_green, offset)
        
    # Drive Tires
    make_cylinder(doc, "Trommel_Tire_F", trommel_drum_dia/2 + trommel_tire_thickness, trommel_tire_width, 
                  400, 0, trommel_z_axis, trommel_col_tire_black, offset, axis=App.Vector(1,0,0))
    make_cylinder(doc, "Trommel_Tire_R", trommel_drum_dia/2 + trommel_tire_thickness, trommel_tire_width, 
                  trommel_drum_len - 400 - trommel_tire_width, 0, trommel_z_axis, trommel_col_tire_black, offset, axis=App.Vector(1,0,0))

    # --- B. STRUCTURAL BASE ---
    trommel_beam_h, trommel_beam_w = 250, 150
    make_box(doc, "Trommel_MainBeam_L", trommel_drum_len + 400, trommel_beam_w, trommel_beam_h, 
             -200, -(trommel_frame_width/2), trommel_support_leg_height, trommel_col_green, offset)
    make_box(doc, "Trommel_MainBeam_R", trommel_drum_len + 400, trommel_beam_w, trommel_beam_h, 
             -200, (trommel_frame_width/2) - trommel_beam_w, trommel_support_leg_height, trommel_col_green, offset)
    
    # Support Legs
    leg_x_coords = [0, trommel_drum_len/2, trommel_drum_len]
    for i, lx in enumerate(leg_x_coords):
        make_box(doc, f"Trommel_Leg_L_{i}", 200, 200, trommel_support_leg_height, lx, -(trommel_frame_width/2)-25, 0, trommel_col_green, offset)
        make_box(doc, f"Trommel_Leg_R_{i}", 200, 200, trommel_support_leg_height, lx, (trommel_frame_width/2)-175, 0, trommel_col_green, offset)
        make_box(doc, f"Trommel_CrossBrace_{i}", 200, trommel_frame_width, 100, lx, -trommel_frame_width/2, 200, trommel_col_green, offset)

    # --- C. FEED HOPPER WALLS ---
    wall_l = trommel_drum_len - 200
    # Left Angled Wall
    make_box(doc, "Trommel_Hopper_Wall_L", wall_l, 20, trommel_hopper_wall_height, 
             100, -trommel_frame_width/2 + 200, trommel_support_leg_height + 200, trommel_col_green, offset, 
             rotation_angle=-30, rotation_axis=App.Vector(1,0,0))
    # Right Angled Wall
    make_box(doc, "Trommel_Hopper_Wall_R", wall_l, 20, trommel_hopper_wall_height, 
             100, trommel_frame_width/2 - 200, trommel_support_leg_height + 200, trommel_col_green, offset, 
             rotation_angle=30, rotation_axis=App.Vector(1,0,0))

    # --- D. DRIVE SYSTEM ---
    shaft_y_pos = trommel_frame_width/2 + 100
    shaft_z_pos = trommel_support_leg_height + 300
    make_cylinder(doc, "Trommel_DriveShaft", 40, trommel_drum_len, 0, shaft_y_pos, shaft_z_pos, trommel_col_drive_shaft, offset, axis=App.Vector(1,0,0))
    
    # Drive Wheels (That contact the tires)
    make_cylinder(doc, f"Trommel_DriveWheel_F", 150, trommel_tire_width, 400, shaft_y_pos-150, shaft_z_pos, trommel_col_tire_black, offset, axis=App.Vector(1,0,0))
    make_cylinder(doc, f"Trommel_DriveWheel_R", 150, trommel_tire_width, trommel_drum_len - 400 - trommel_tire_width, shaft_y_pos-150, shaft_z_pos, trommel_col_tire_black, offset, axis=App.Vector(1,0,0))
    
    # Motor & Housing
    make_cylinder(doc, "Trommel_Motor", 125, 450, -450, shaft_y_pos, shaft_z_pos, trommel_col_motor_blue, offset, axis=App.Vector(1,0,0))
    make_box(doc, "Trommel_Guard", 150, 200, 200, -50, shaft_y_pos-100, shaft_z_pos-100, trommel_col_green, offset)



def build_decline_conveyor(offset=(0, 0, 0)):
    doc = ensure_document()
    rad = math.radians(dec_decline_angle)
    
    # --- GEOMETRY CALCULATIONS ---
    # Knee Point (End of high flat, Start of decline)
    p1_x = dec_high_flat_len
    p1_z = dec_start_height
    
    # Elbow Point (End of decline, Start of low flat)
    p2_x = p1_x + (dec_slope_len * math.cos(rad))
    p2_z = p1_z - (dec_slope_len * math.sin(rad)) # Descending (Z decreases)
    
    # End Point
    p3_x = p2_x + dec_low_flat_len
    p3_z = p2_z

    # --- A. FRAME CHANNELS ---
    # 1. High Section (Top)
    make_box(doc, "DEC_Frame_High_L", dec_high_flat_len, 40, dec_rail_h, 0, 0, p1_z - dec_rail_h, dec_col_frame_grey, offset)
    make_box(doc, "DEC_Frame_High_R", dec_high_flat_len, 40, dec_rail_h, 0, dec_frame_width-40, p1_z - dec_rail_h, dec_col_frame_grey, offset)
    
    # 2. Decline Section (Sloping Down)
    # To rotate DOWN, we use a positive angle around Y but the math logic places it correctly
    make_box(doc, "DEC_Frame_Slope_L", dec_slope_len, 40, dec_rail_h, p1_x, 0, p1_z - dec_rail_h, dec_col_frame_grey, offset, 
             rotation_angle=dec_decline_angle, rotation_axis=App.Vector(0,1,0))
    make_box(doc, "DEC_Frame_Slope_R", dec_slope_len, 40, dec_rail_h, p1_x, dec_frame_width-40, p1_z - dec_rail_h, dec_col_frame_grey, offset, 
             rotation_angle=dec_decline_angle, rotation_axis=App.Vector(0,1,0))
             
    # 3. Low Section (Bottom)
    make_box(doc, "DEC_Frame_Low_L", dec_low_flat_len, 40, dec_rail_h, p2_x, 0, p2_z - dec_rail_h, dec_col_frame_grey, offset)
    make_box(doc, "DEC_Frame_Low_R", dec_low_flat_len, 40, dec_rail_h, p2_x, dec_frame_width-40, p2_z - dec_rail_h, dec_col_frame_grey, offset)

    # --- B. BELT & CLEATS ---
    belt_y = (dec_frame_width - dec_belt_width) / 2
    
    # High Belt
    make_box(doc, "DEC_Belt_High", dec_high_flat_len, dec_belt_width, 10, 0, belt_y, p1_z, dec_col_belt_blue, offset)
    # Slope Belt
    make_box(doc, "DEC_Belt_Slope", dec_slope_len, dec_belt_width, 10, p1_x, belt_y, p1_z, dec_col_belt_blue, offset, 
             rotation_angle=dec_decline_angle, rotation_axis=App.Vector(0,1,0))
    # Low Belt
    make_box(doc, "DEC_Belt_Low", dec_low_flat_len, dec_belt_width, 10, p2_x, belt_y, p2_z, dec_col_belt_blue, offset)

    # Cleats (Pockets to prevent material sliding down)
    num_cleats = 15
    for i in range(num_cleats):
        dist = (dec_slope_len / num_cleats) * i
        cx = p1_x + (dist * math.cos(rad))
        cz = p1_z - (dist * math.sin(rad)) + 10
        make_box(doc, f"DEC_Cleat_{i}", 20, dec_belt_width, 50, cx, belt_y, cz, dec_col_belt_blue, offset,
                 rotation_angle=dec_decline_angle, rotation_axis=App.Vector(0,1,0))

    # --- C. SUPPORT LEGS ---
    leg_dim = 80.0
    
    # High Legs (Tallest)
    make_box(doc, "DEC_Leg_High_L", leg_dim, leg_dim, p1_z - dec_rail_h, 200, 0, 0, dec_col_leg_dark, offset)
    make_box(doc, "DEC_Leg_High_R", leg_dim, leg_dim, p1_z - dec_rail_h, 200, dec_frame_width - leg_dim, 0, dec_col_leg_dark, offset)
    
    # Mid Legs (Under Slope)
    mid_x = p1_x + (p2_x - p1_x)/2
    mid_z = p1_z - (p1_z - p2_z)/2
    make_box(doc, "DEC_Leg_Mid_L", leg_dim, leg_dim, mid_z - dec_rail_h, mid_x, 0, 0, dec_col_leg_dark, offset)
    make_box(doc, "DEC_Leg_Mid_R", leg_dim, leg_dim, mid_z - dec_rail_h, mid_x, dec_frame_width - leg_dim, 0, dec_col_leg_dark, offset)
    
    # Low Legs (Shortest)
    make_box(doc, "DEC_Leg_Low_L", leg_dim, leg_dim, p2_z - dec_rail_h, p3_x - 400, 0, 0, dec_col_leg_dark, offset)
    make_box(doc, "DEC_Leg_Low_R", leg_dim, leg_dim, p2_z - dec_rail_h, p3_x - 400, dec_frame_width - leg_dim, 0, dec_col_leg_dark, offset)

    # --- D. END COMPONENTS ---
    # Intake Hopper at the TOP
    make_box(doc, "DEC_Intake_Hopper", 1000, dec_frame_width + 100, 500, 100, -50, p1_z, dec_col_frame_grey, offset)
    
    # Pulleys (Tail at top, Head at bottom)
    make_cylinder(doc, "DEC_Pulley_Top", 120, dec_frame_width + 40, 0, -20, p1_z - 120, dec_col_roller_silver, offset, axis=App.Vector(0,1,0))
    make_cylinder(doc, "DEC_Pulley_Bot", 120, dec_frame_width + 40, p3_x, -20, p3_z - 120, dec_col_roller_silver, offset, axis=App.Vector(0,1,0))


def build_centrifugal_concentrator(doc, offset=(0,0,0)):
    """
    Builds a dual-unit Centrifugal Concentrator at the specified numerical offset.
    """
    
    # We build two units side by side
    for unit_idx in [0, 1]:
        # Center X for this unit relative to the offset
        local_cx = unit_idx * centri_module_gap
        
        # --- A. MAIN DRUM BODY ---
        drum_z_start = centri_cradle_h - 200
        
        # 1. Main Bowl/Drum
        make_cylinder(doc, f"Centri_Drum_{unit_idx}", centri_drum_diameter/2, centri_drum_h, 
                      local_cx, 0, drum_z_start, centri_col_main_blue, offset)
        
        # 2. Top Rim Flange
        make_cylinder(doc, f"Centri_Rim_{unit_idx}", centri_drum_diameter/2 + 40, 40, 
                      local_cx, 0, drum_z_start + centri_drum_h - 40, centri_col_main_blue, offset)
        
        # 3. Bolts on Rim
        num_bolts = 12
        for i in range(num_bolts):
            ang = (360.0 / num_bolts) * i
            rad = math.radians(ang)
            bx = local_cx + (centri_drum_diameter/2 + 20) * math.cos(rad)
            by = (centri_drum_diameter/2 + 20) * math.sin(rad)
            bz = drum_z_start + centri_drum_h - 10
            make_cylinder(doc, f"Centri_Bolt_{unit_idx}_{i}", centri_bolt_r, 25, bx, by, bz, centri_col_bolt_silver, offset)

        # 4. Discharge Spouts
        spout_z = drum_z_start + 300
        # Outer Pipe
        make_cylinder(doc, f"Centri_Spout_Out_{unit_idx}", centri_spout_dia/2, 300, 
                      local_cx + centri_drum_diameter/2 - 50, 0, spout_z, centri_col_main_blue, offset, axis=App.Vector(1,0,0))
        # Inner Liner (Simulating the red interior)
        make_cylinder(doc, f"Centri_Spout_In_{unit_idx}", centri_spout_dia/2 - 10, 310, 
                      local_cx + centri_drum_diameter/2 - 50, 0, spout_z, centri_col_liner_maroon, offset, axis=App.Vector(1,0,0))

        # --- B. SUPPORT FRAME ---
        # Left Support Plate
        make_box(doc, f"Centri_Frame_L_{unit_idx}", 100, centri_cradle_w, centri_cradle_h, 
                 local_cx - centri_drum_diameter/2 - 100, -centri_cradle_w/2, 0, centri_col_main_blue, offset)
        
        # Right Support Plate
        make_box(doc, f"Centri_Frame_R_{unit_idx}", 100, centri_cradle_w, centri_cradle_h, 
                 local_cx + centri_drum_diameter/2, -centri_cradle_w/2, 0, centri_col_main_blue, offset)
        
        # Bottom Cross Beams
        make_box(doc, f"Centri_Base_F_{unit_idx}", centri_drum_diameter + 200, 100, 100, 
                 local_cx - centri_drum_diameter/2 - 100, -centri_cradle_w/2, 0, centri_col_main_blue, offset)
        make_box(doc, f"Centri_Base_B_{unit_idx}", centri_drum_diameter + 200, 100, 100, 
                 local_cx - centri_drum_diameter/2 - 100, centri_cradle_w/2 - 100, 0, centri_col_main_blue, offset)

        # Hydraulic Tilt Cylinder
        make_cylinder(doc, f"Centri_Hydraulic_{unit_idx}", 60, 500, 
                      local_cx - centri_drum_diameter/2 - 150, centri_cradle_w/2 + 20, 400, 
                      centri_col_dark_steel, offset, axis=App.Vector(0,0,1))

        # --- C. FEED HOSES ---
        # Vertical Riser
        make_cylinder(doc, f"Centri_Hose_Rise_{unit_idx}", centri_hose_radius, 800, 
                      local_cx, centri_cradle_w/2 + 200, drum_z_start, centri_col_hose_charcoal, offset)
        
        # Feed Arch (U-bend into center)
        # Using Part.makeTorus for the arch but applying the offset translation manually
        arch_z = drum_z_start + 800
        arch_y = centri_cradle_w/2 + 200 - centri_arch_radius
        
        arch_shape = Part.makeTorus(centri_arch_radius, centri_hose_radius, App.Vector(0,0,0), App.Vector(0,0,1), 0, 180)
        arch_shape.rotate(App.Vector(0,0,0), App.Vector(1,0,0), 90) # Stand upright
        arch_shape.rotate(App.Vector(0,0,0), App.Vector(0,0,1), 90) # Orient toward center
        arch_shape.translate(App.Vector(local_cx + offset[0], arch_y + offset[1], arch_z + offset[2]))
        
        obj_arch = doc.addObject("Part::Feature", f"Centri_Hose_Arch_{unit_idx}")
        obj_arch.Shape = arch_shape
        obj_arch.ViewObject.ShapeColor = centri_col_hose_charcoal

    # --- D. MANIFOLD SYSTEM ---
    # Horizontal Main Line (Across the front)
    manifold_y = -centri_cradle_w/2 - 150
    make_cylinder(doc, "Centri_Manifold_Main", 50, centri_module_gap + centri_drum_diameter, 
                  -centri_drum_diameter/2, manifold_y, 400, centri_col_main_blue, offset, axis=App.Vector(1,0,0))
    
    # Connection Ports
    for i in [0, 1]:
        make_cylinder(doc, f"Centri_Manifold_Conn_{i}", 50, 150, 
                      i * centri_module_gap, manifold_y, 400, centri_col_main_blue, offset, axis=App.Vector(0,1,0))




# --- 1. Flanged Pipe (Bolted sections using cylinders) ---
# Now accepts explicit start_p and end_p vectors from the layout
def create_jointed_pipe(doc, name, start_p, end_p, pipe_r, joint_r, color, offset=(0,0,0)):
    # Calculate Global Positions by applying offset to the passed coordinates
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

# --- 2. Smooth Duct (Continuous sweep along multiple points) ---
# Now accepts the point list directly from the layout
def create_duct(doc, name, path_points, radius, color, offset=(0,0,0)):
    # Apply offset to all points in the path
    global_points = []
    for p in path_points:
        global_points.append(App.Vector(p.x + offset[0], p.y + offset[1], p.z + offset[2]))
    
    # Create the path wire
    wire = Part.Wire(Part.makePolygon(global_points).Edges)
    # Create profile at the start point
    circle = Part.makeCircle(radius, global_points[0], global_points[1].sub(global_points[0]))
    profile = Part.Wire(circle)
    
    shape = wire.makePipe(profile)
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = shape
    obj.ViewObject.ShapeColor = color
    return obj

# --- 3. Angle Builder: Coordinates are now passed as arguments ---
def build_vessel_bolted_angle(doc, name, p_start, p_elbow, p_end, p_rad, j_rad, color, offset=(0,0,0)):
    # Calls the jointed pipe builder using the coordinates defined in layout
    # Segment 1: Start to Elbow
    create_jointed_pipe(doc, name + "_Seg1", p_start, p_elbow, p_rad, j_rad, color, offset)
    # Segment 2: Elbow to End
    create_jointed_pipe(doc, name + "_Seg2", p_elbow, p_end, p_rad, j_rad, color, offset)

# ==============================================================================
# MAIN DRAWING FUNCTION: SHREDDED PARTICLE (BLACK SPHERE)
# ==============================================================================

def draw_black_sphere(doc, name, offset_coords=(0, 0, 0), scale_factor=1.0):
    """
    Creates a dark matte particle.
    Proportionally scales the sphere based on scale_factor.
    """
    S = scale_factor 
    
    # --- COLORS ---
    c_dark_grey = (0.15, 0.15, 0.15)

    # --- DIMENSIONS (SCALED) ---
    radius = 50.0 * S

    # 1. GENERATE GEOMETRY
    particle_obj = make_sphere(
        doc, 
        name,      # Use the dynamic name passed from the loop
        radius, 
        0, 0, 0,   # Local coordinates
        c_dark_grey, 
        offset_coords
    )

    return particle_obj


# ==============================================================================
# MAIN DRAWING FUNCTION: GLOSSY BROWN SPHERE
# ==============================================================================

def draw_brown_sphere(doc, name, offset_coords=(0, 0, 0), scale_factor=1.0):
    """
    Creates a rich coppery-brown glossy sphere.
    Proportionally scales based on scale_factor.
    """
    S = scale_factor 
    
    # --- COLORS ---
    c_glossy_brown = (0.55, 0.25, 0.12)

    # --- DIMENSIONS (SCALED) ---
    radius = 50.0 * S

    # 1. GENERATE GEOMETRY
    sphere_obj = make_sphere(
        doc, 
        name,      # Use the dynamic name passed from the loop
        radius, 
        0, 0, 0,   # Local center coordinates
        c_glossy_brown, 
        offset_coords
    )

    return sphere_obj



# ==============================================================================
# MAIN DRAWING FUNCTION: GLOSSY SILVER SPHERE
# ==============================================================================

def draw_silver_sphere(doc, name, offset_coords=(0, 0, 0), scale_factor=1.0):
    """
    Creates a bright metallic silver glossy sphere.
    Proportionally scales based on scale_factor.
    """
    S = scale_factor 
    
    # --- COLORS ---
    c_glossy_silver = (0.75, 0.75, 0.80)

    # --- DIMENSIONS (SCALED) ---
    radius = 50.0 * S

    # 1. GENERATE GEOMETRY
    sphere_obj = make_sphere(
        doc, 
        name,      # Use the dynamic name passed from the loop
        radius, 
        0, 0, 0,   # Local center coordinates
        c_glossy_silver, 
        offset_coords
    )

    return sphere_obj

# ==============================================================================
# MAIN DRAWING FUNCTION: BATTERY SCHEMATIC (PLATE & GRANULAR DETAIL)
# ==============================================================================

def draw_battery_diagram(doc, offset_coords=(0, 0, 0), scale_factor=1.0):
    """
    Creates a fused battery diagram showing the current collectors, 
    anode/cathode granular layers, and the separator.
    """
    S = scale_factor
    temp_objects = []
    
    # --- COLORS (Matching the provided image) ---
    c_anode_cc = (0.95, 0.75, 0.10)   # Golden Yellow (Anode Current Collector)
    c_anode    = (0.45, 0.45, 0.45)   # Grey (Anode Material)
    c_sep      = (0.80, 0.90, 0.95)   # Light Blue (Separator)
    c_cathode  = (0.75, 0.85, 0.60)   # Light Green (Cathode Material)
    c_cathode_cc = (0.85, 0.85, 0.85) # Silver/White (Cathode Current Collector)
    c_shell    = (0.80, 0.80, 0.60)   # Tan/Yellow (Outer casing)

    # --- DIMENSIONS (Scaled) ---
    h = 120.0 * S       # Height
    d = 60.0 * S        # Depth
    layer_w = 12.0 * S  # Width of active layers
    cc_w = 4.0 * S      # Width of current collectors
    sep_w = 6.0 * S     # Width of separator
    part_r = 2.5 * S    # Radius of granular particles

    # 1. ANODE CURRENT COLLECTOR (Leftmost bar)
    temp_objects.append(make_box(doc, "Anode_CC", cc_w, d, h, 0, 0, 0, c_anode_cc, offset_coords))

    # 2. ANODE GRANULAR LAYER (Grey Spheres)
    # We build a grid of spheres to match the "Anode" label in your image
    anode_start_x = cc_w
    for r in range(5): # rows
        for c in range(8): # columns
            for dep in range(3): # depth
                px = anode_start_x + (r * 2.4 * S) + part_r
                py = (dep * 20 * S) + (c % 2 * 2 * S)
                pz = (c * 15 * S) + part_r
                # Add slight randomness for "granular" look
                rx, ry, rz = random.uniform(-1,1)*S, random.uniform(-1,1)*S, random.uniform(-1,1)*S
                temp_objects.append(make_sphere(doc, f"A_Part_{r}_{c}_{dep}", part_r, px+rx, py+ry, pz+rz, c_anode, offset_coords))

    # 3. SEPARATOR (Middle membrane)
    sep_x = anode_start_x + layer_w
    temp_objects.append(make_box(doc, "Separator", sep_w, d, h, sep_x, 0, 0, c_sep, offset_coords))

    # 4. CATHODE GRANULAR LAYER (Green Spheres)
    cathode_start_x = sep_x + sep_w
    for r in range(5): 
        for c in range(8):
            for dep in range(3):
                px = cathode_start_x + (r * 2.4 * S) + part_r
                py = (dep * 20 * S) + (c % 2 * 2 * S)
                pz = (c * 15 * S) + part_r
                rx, ry, rz = random.uniform(-1,1)*S, random.uniform(-1,1)*S, random.uniform(-1,1)*S
                temp_objects.append(make_sphere(doc, f"C_Part_{r}_{c}_{dep}", part_r, px+rx, py+ry, pz+rz, c_cathode, offset_coords))

    # 5. CATHODE CURRENT COLLECTOR (Rightmost bar)
    cc_cath_x = cathode_start_x + layer_w
    temp_objects.append(make_box(doc, "Cathode_CC", cc_w, d, h, cc_cath_x, 0, 0, c_cathode_cc, offset_coords))

    # 6. EXTERNAL CASING (The cylindrical cutaway look)
    # This represents the yellow cylinder on the left of the image
    shell_r = 80.0 * S
    shell_h = 160.0 * S
    shell_x = -120 * S # Positioned to the side
    
    # Outer Cylinder
    cyl_out = Part.makeCylinder(shell_r, shell_h)
    # Inner Cylinder (Hollow)
    cyl_in = Part.makeCylinder(shell_r - (4*S), shell_h)
    # Quarter cut to show internals
    cut_box = Part.makeBox(shell_r, shell_r, shell_h)
    
    shell_shape = cyl_out.cut(cyl_in).cut(cut_box)
    shell_shape.translate(App.Vector(shell_x + offset_coords[0], offset_coords[1], -20*S + offset_coords[2]))
    
    shell_obj = doc.addObject("Part::Feature", "Battery_Outer_Shell")
    shell_obj.Shape = shell_shape
    shell_obj.ViewObject.ShapeColor = c_shell
    temp_objects.append(shell_obj)

    # --- FUSION STEP ---
    if temp_objects:
        shapes_to_fuse = [obj.Shape for obj in temp_objects]
        fused_shape = shapes_to_fuse[0]
        for s in shapes_to_fuse[1:]:
            fused_shape = fused_shape.fuse(s)
        
        # Cleanup temporary objects
        for obj in temp_objects:
            doc.removeObject(obj.Name)
            
        final_obj = doc.addObject("Part::Feature", "Battery_Diagram_Fused")
        final_obj.Shape = fused_shape
        final_obj.ViewObject.ShapeColor = c_cathode # Default display color
        
        doc.recompute()
        return final_obj

# ==============================================================================
# MAIN DRAWING FUNCTION: LITHIUM-IODINE BATTERY (D-SHAPE SCHEMATIC)
# ==============================================================================

def draw_lithium_iodine_battery(doc, offset_coords=(0, 0, 0), scale_factor=1.0):
    """
    Creates a fused D-shaped battery schematic with symmetrical internal layers:
    Cathode -> Electrolyte -> Anode -> Nickel Mesh (Center)
    """
    S = scale_factor
    temp_objects = []

    # --- COLORS (Matching the image) ---
    c_can       = (0.85, 0.85, 0.85)   # Light Grey (Positive Can)
    c_cathode   = (1.0, 0.80, 0.65)    # Peach (Li/PVP complex)
    c_electro   = (1.0, 1.0, 0.0)      # Yellow (LiI crystals)
    c_anode     = (0.0, 0.15, 0.55)    # Dark Blue (Li-metal)
    c_mesh      = (0.75, 0.95, 0.80)   # Mint Green (Nickel Mesh)
    c_red_plus  = (0.85, 0.10, 0.10)   # Red (Positive Symbol)
    c_neg_bar   = (0.25, 0.35, 0.20)   # Dark Green (Negative Terminal)

    # --- DIMENSIONS (SCALED) ---
    bat_h = 100.0 * S      # Total height
    bat_w = 70.0 * S       # Total width (across the D)
    bat_d = 50.0 * S       # Depth (thickness of the cell)
    layer_t = 3.0 * S      # Thickness of individual active layers
    gap_w = 8.0 * S        # Center gap width

    # 1. MAIN BODY (PEACH CATHODE BULK)
    # We build a D-shape using a box and a half-cylinder
    rect_w = bat_w / 2
    body_box = Part.makeBox(rect_w, bat_d, bat_h)
    
    cyl_end = Part.makeCylinder(bat_d/2, bat_h)
    cyl_end.translate(App.Vector(rect_w, bat_d/2, 0))
    
    main_body = body_box.fuse(cyl_end)
    
    # Create the central cutaway slot (as seen in Image A)
    slot = Part.makeBox(gap_w, bat_d + 10*S, bat_h + 10*S)
    slot.translate(App.Vector(-gap_w/2, -5*S, -5*S))
    
    cathode_bulk = main_body.cut(slot)
    cathode_bulk.translate(App.Vector(offset_coords[0], offset_coords[1], offset_coords[2]))
    
    obj_cath = doc.addObject("Part::Feature", "Cathode_Bulk")
    obj_cath.Shape = cathode_bulk
    obj_cath.ViewObject.ShapeColor = c_cathode
    temp_objects.append(obj_cath)

    # 2. INTERNAL LAYERS (Symmetrical Sandwich)
    # Positioned within the cutaway slot
    layers = [
        ("Electrolyte", c_electro, gap_w/2 - layer_t),   # Outer layers of slot
        ("Anode",       c_anode,   gap_w/2 - 2*layer_t)  # Inner layers of slot
    ]

    for name, color, x_pos in layers:
        for side in [-1, 1]:
            layer_box = make_box(doc, f"{name}_{side}", layer_t, bat_d, bat_h, 
                                 x_pos * side - (layer_t if side == 1 else 0), 0, 0, 
                                 color, offset_coords)
            temp_objects.append(layer_box)

    # 3. NICKEL MESH (Center thin layer)
    mesh_w = 1.5 * S
    temp_objects.append(make_box(doc, "Nickel_Mesh_Center", mesh_w, bat_d, bat_h, 
                                -mesh_w/2, 0, 0, c_mesh, offset_coords))

    # 4. OUTER POSITIVE CAN (Grey Shell)
    # Thin layers on the flat back and curved end
    make_box(doc, "Can_Flat", 2*S, bat_d, bat_h, -rect_w, 0, 0, c_can, offset_coords)
    
    # Simple shell for the curved part
    can_outer = Part.makeCylinder(bat_d/2 + 1*S, bat_h)
    can_inner = Part.makeCylinder(bat_d/2, bat_h)
    can_curved = can_outer.cut(can_inner)
    can_curved.translate(App.Vector(rect_w, bat_d/2, 0))
    can_curved.translate(App.Vector(*offset_coords))
    
    obj_can = doc.addObject("Part::Feature", "Can_Curved")
    obj_can.Shape = can_curved
    obj_can.ViewObject.ShapeColor = c_can
    temp_objects.append(obj_can)

    # 5. TERMINALS & SYMBOLS
    # Negative Terminal Pin
    make_cylinder(doc, "Neg_Terminal_Pin", 2*S, 15*S, 0, bat_d/2, bat_h, (0.9, 0.9, 0.9), offset_coords)
    make_box(doc, "Neg_Terminal_Bar", 15*S, 2*S, 1*S, -7.5*S, bat_d/2 - 1*S, bat_h + 15*S, c_neg_bar, offset_coords)

    # Positive Symbol (Red Cross on side)
    cross_sz = 10 * S
    cross_t = 1 * S
    make_box(doc, "Plus_H", cross_sz, 0.2*S, cross_t, -rect_w - 1*S, bat_d/2 - cross_sz/2, bat_h * 0.7, c_red_plus, offset_coords)
    make_box(doc, "Plus_V", cross_t, 0.2*S, cross_sz, -rect_w - 1*S - cross_sz/2 + cross_t/2, bat_d/2 - cross_t/2, bat_h * 0.7 - cross_sz/2 + cross_t/2, c_red_plus, offset_coords)

    # --- FUSION STEP ---
    if temp_objects:
        shapes_to_fuse = [obj.Shape for obj in temp_objects]
        fused_shape = shapes_to_fuse[0]
        for s in shapes_to_fuse[1:]:
            fused_shape = fused_shape.fuse(s)
        
        # Cleanup
        for obj in temp_objects:
            doc.removeObject(obj.Name)
            
        final_obj = doc.addObject("Part::Feature", "LiI_Battery_Fused")
        final_obj.Shape = fused_shape
        final_obj.ViewObject.ShapeColor = c_can
        
        doc.recompute()
        return final_obj


# ==============================================================================
# MAIN DRAWING FUNCTION: CYLINDRICAL JELLY-ROLL BATTERY (DETAILED CROSS-SECTION)
# ==============================================================================

def draw_cylindrical_jellyroll(doc, offset_coords=(0, 0, 0), scale_factor=1.0):
    """
    Creates a fused cylindrical battery with a cutaway showing the internal 
    wound layers (Separator, Positive/Negative Electrodes) and unrolled sheets.
    """
    S = scale_factor
    all_parts = []

    # --- COLORS (Matching Image) ---
    c_housing   = (0.85, 0.88, 0.90)  # Light Grey/Steel
    c_sep       = (0.50, 0.85, 1.0)   # Cyan (Separator/Electrolyte)
    c_pos_elec  = (0.10, 0.50, 0.80)  # Dark Blue
    c_neg_elec  = (0.65, 0.75, 0.85)  # Light Blue Grey
    c_gasket    = (0.20, 0.20, 0.20)  # Black/Dark Grey
    c_terminal  = (0.95, 0.95, 0.98)  # Shiny Silver

    # --- DIMENSIONS (SCALED) ---
    radius = 50.0 * S
    height = 160.0 * S
    wall   = 2.0 * S
    layer_t = 1.2 * S
    num_layers = 12

    # 1. QUARTER CUTAWAY TOOL
    # Standard box to remove a quadrant for visibility
    cut_tool = Part.makeBox(radius * 1.5, radius * 1.5, height + (20 * S))
    cut_tool.translate(App.Vector(offset_coords[0], offset_coords[1], offset_coords[2] - (5 * S)))

    # 2. OUTER HOUSING & CONNECTION
    housing_out = Part.makeCylinder(radius, height)
    housing_in  = Part.makeCylinder(radius - wall, height)
    housing_shell = housing_out.cut(housing_in)
    housing_shell.translate(App.Vector(*offset_coords))
    
    final_housing = housing_shell.cut(cut_tool)
    obj_h = doc.addObject("Part::Feature", "Housing_Shell")
    obj_h.Shape = final_housing
    obj_h.ViewObject.ShapeColor = c_housing
    all_parts.append(final_housing)

    # 3. TOP CAP ASSEMBLY (Cap, Safety Valve, PTC)
    cap_z = height
    # Main Cap base
    cap_base = Part.makeCylinder(radius - wall, 6 * S)
    # Terminal Top (Connection)
    terminal = Part.makeCylinder(radius * 0.4, 4 * S)
    terminal.translate(App.Vector(0, 0, 6 * S))
    # Combine and add safety valve recess
    cap_assembly = cap_base.fuse(terminal)
    recess = Part.makeCylinder(radius * 0.15, 5 * S)
    recess.translate(App.Vector(0, 0, 7 * S))
    cap_assembly = cap_assembly.cut(recess)
    
    cap_assembly.translate(App.Vector(offset_coords[0], offset_coords[1], cap_z + offset_coords[2]))
    obj_cap = doc.addObject("Part::Feature", "Top_Cap_Assy")
    obj_cap.Shape = cap_assembly
    obj_cap.ViewObject.ShapeColor = c_terminal
    all_parts.append(cap_assembly)

    # Gasket (Seal ring)
    gasket = Part.makeCylinder(radius, 3 * S).cut(Part.makeCylinder(radius - wall, 3 * S))
    gasket.translate(App.Vector(offset_coords[0], offset_coords[1], cap_z - (3 * S) + offset_coords[2]))
    all_parts.append(gasket)

    # 4. INTERNAL JELLY-ROLL LAYERS
    curr_r = radius - (wall + 2 * S)
    for i in range(num_layers):
        # Cycling through the 3 internal components
        if i % 3 == 0: color = c_sep
        elif i % 3 == 1: color = c_pos_elec
        else: color = c_neg_elec
        
        r_out = curr_r
        curr_r -= layer_t
        r_in = curr_r
        
        layer = Part.makeCylinder(r_out, height - (15 * S)).cut(Part.makeCylinder(r_in, height - (15 * S)))
        layer.translate(App.Vector(offset_coords[0], offset_coords[1], 10 * S + offset_coords[2]))
        
        layer_cut = layer.cut(cut_tool)
        all_parts.append(layer_cut)

    # 5. UNROLLED/PEELED SHEETS (Right side of image)
    # We model these as curved boxes tangential to the cylinder
    for i, color in enumerate([c_sep, c_neg_elec, c_pos_elec, c_sep]):
        sheet_w = 40.0 * S
        sheet_h = height - (20 * S)
        sheet_t = layer_t
        
        sheet = Part.makeBox(sheet_t, sheet_w, sheet_h)
        # Offset and rotate sheets to look like unrolling
        sheet.rotate(App.Vector(0,0,0), App.Vector(0,0,1), -10 * i)
        sheet.translate(App.Vector(radius + (i * 10 * S), -sheet_w/2, 10 * S))
        sheet.translate(App.Vector(*offset_coords))
        all_parts.append(sheet)

    # 6. CENTRAL CORE (Mandrel/Hole)
    core = Part.makeCylinder(curr_r, height - (15 * S)).cut(cut_tool)
    core.translate(App.Vector(offset_coords[0], offset_coords[1], 10 * S + offset_coords[2]))
    all_parts.append(core)

    # --- FINAL FUSION ---
    if all_parts:
        fused_shape = all_parts[0]
        for s in all_parts[1:]:
            fused_shape = fused_shape.fuse(s)

        final_obj = doc.addObject("Part::Feature", "JellyRoll_Battery_Fused")
        final_obj.Shape = fused_shape
        final_obj.ViewObject.ShapeColor = c_housing
        
        doc.recompute()
        return final_obj


# ==========================================
# MAIN EXECUTION (WITH INTEGRATED JSON)
# ==========================================

def create_layout():
    doc = ensure_document()
    create_equipment(doc, (-3000, -500, 800))
    build_conveyor(doc, (4000.0, 200.0, -200.0))
    build_shredder(doc, (6300.0, -500.0, 0.0))
    pocket_conveyor(doc, offset=(12000, -100, 800))
    # Pyrolysis reactor positioned at the discharge of the screw conveyor
    # X = 18500 (10000 start + 8000 length + 500 gap)
    # Y = 700 (Aligned with screw Y)
    # Z = 0 (On ground)
    pyro_offset = (18500, 300, 0)
    build_reactor(doc, offset=pyro_offset)
    # Blue Storage Tank placed in front of Pyrolysis
    tank_offset = (20500, 4000, 0)
    build_tank(doc, offset=tank_offset) 
    # Build Connecting Pipe
    build_connecting_pipe(doc, pyro_offset, tank_offset)
    #Pneumatic Conveyor
    pneumatic_conveyor(doc, offset=(18000, 0, 0))
    # Build Crusher at specified coordinates (0, 0, 0)
    build_crusher(doc, offset=(26000, 0, 0))
    #Pocket conveyor
    pocket_conveyor(doc, offset=(31500, 0, 2900))
    pocket_conveyor(doc, offset=(79000,0,1000))
    pocket_conveyor(doc, offset=(91000,0,1000))
    #Screener
    build_cleaner(doc, offset=(37000, 800, 0))
    #Build Hydrocylone
    build_cluster(doc, offset=(26000, 6000, 0))
    #Buid Dust Collector
    build_dust_collector(doc, offset=(35000, 6000, 800))
    #Build ESP
    build_esp(doc, offset=(43000, 6000, 0))
    # Example: Build at origin (0, 0, 0)
    build_scrubber(doc, offset=(55000, 0, 0))
    #Pocket Conveyor
    pocket_conveyor(doc, offset = (47000, 0, 4000))
    #Build Conveyor
    build_swan_neck_conveyor(doc, offset=(59000, 0, 0))
    # Coordinates format: (X, Y, Z)
    build_separator(doc, offset=(66000, 0, 0)) 
    # Defining the Numerical Offset Coordinates
    dec_offset_coords = (69000.0, 0.0, 0.0)
    # Build the system
    build_decline_conveyor(offset=dec_offset_coords)
    #Ball Mill
    mill_placement_coords = (77500.0, -50.0, 0.0)
    build_ball_mill(offset=mill_placement_coords)
    # Placement coordinate defined as a numerical offset
    trommel_placement = (85000.0, 0.0, 0.0)
    # Build the equipment
    build_trommel(offset=trommel_placement)
    #Building centrifugal at specific numerical offset
    build_centrifugal_concentrator(doc, offset=(98000.0, 0.0, 0.0))
    # --- EXAMPLE 1: Bolted flanged pipes on top of Centrifugal Concentrator ---
    centri_pos = (100000.0, 0.0, 0.0)
    build_centrifugal_concentrator(doc, offset=centri_pos)
    # --- 1. PIPE: CRUSHER TO HYDROCYCLONE ---
    # From Crusher discharge (approx X+5000) to Hydrocyclone feed manifold
    crusher_output = App.Vector(27000, 0, 2500)
    cluster_intake = App.Vector(26000, 5000, 2500)
    create_jointed_pipe(doc, "Pipe_Crusher_Cyc", crusher_output, cluster_intake, 120, 160, col_pipe_yellow)
    # --- 2. PIPE: HYDROCYCLONE TO PULSE DUST COLLECTOR ---
    # From Cluster overflow to Dust Collector side inlet
    cluster_overflow = App.Vector(26000, 6000, 3500)
    dust_collector_inlet = App.Vector(34200, 6000, 3500)
    create_jointed_pipe(doc, "Pipe_Cyc_Dust", cluster_overflow, dust_collector_inlet, 150, 200, col_pipe_yellow)
    # --- 3. PIPE: PULSE DUST COLLECTOR TO ELECTROSTATIC PRECIPITATOR (ESP) ---
    # Using a duct path to handle the elevation and position change
    dust_out = App.Vector(36000, 6000, 3800) # Top of dust collector
    esp_in   = App.Vector(42000, 6000, 2500) # Side transition of ESP
    # Path with an intermediate elbow point
    esp_duct_path = [dust_out, App.Vector(40000, 6000, 4500), esp_in]
    create_duct(doc, "Duct_Dust_ESP", esp_duct_path, 200, col_steel_grey)
    # Usage in your main layout:
    draw_battery_diagram(doc, offset_coords=(0, 250, 850), scale_factor=3.5)
    draw_lithium_iodine_battery(doc, offset_coords=(0, 150, 850), scale_factor=3.5)
    draw_cylindrical_jellyroll(doc, offset_coords=(0, 300, 850), scale_factor=3.2)
    #Draw the spheres
    for i in range(5):
        x_loc = i * 400
        draw_black_sphere(doc, f"Anim_Particle_Black_{i}", offset_coords=(x_loc, 100, 850), scale_factor=1.5)
        draw_brown_sphere(doc, f"Anim_Particle_Brown_{i}", offset_coords=(x_loc, 250, 850), scale_factor=1.5)
        draw_silver_sphere(doc, f"Anim_Particle_Silver_{i}", offset_coords=(x_loc, 400, 850), scale_factor=1.5)
    
    for i in range(1):
        # Spacing set to 500 units along the X-axis starting from the provided coordinates
        draw_battery_cell(doc, offset_coords=(0 + (i * 500), 500, 850), scale_factor=3.5)
        draw_prismatic_battery(doc, offset_coords=(0 + (i * 500), 500, 850), scale_factor=3.5)

    battery_templates = [
        ("Smartphone", draw_smartphone_battery, 200, 850, 4.0),
        ("Samsung",    draw_samsung_battery,    200, 850, 4.0),
        ("LiPo",       draw_lipo_battery,       200, 850, 4.0),
        ("Flat",       draw_flat_battery_fused, 250, 850, 4.0),
        ("HP",         draw_hp_battery,         250,  850, 4.0),
        ("Black",      draw_black_battery,      250, 850, 4.0),
        ("Rugged",     draw_rugged_battery,     200, 850, 2.0),
        ("Military",   draw_mil_battery,        200, 850, 5.0)
    ]

    count_per_brand = 10
    spacing_x = 350.0 
    
    # List to store motion data for JSON
    animation_data = []

    for name, func, lane_y, height_z, scale in battery_templates:
        for i in range(count_per_brand):
            # Capture exact randomized position
            pos_x = 200 + (i * spacing_x) + random.uniform(-40, 40)
            pos_y = lane_y + random.uniform(-15, 15)
            
            # Draw the battery in FreeCAD
            obj = func(doc, offset_coords=(pos_x, pos_y, height_z), scale_factor=scale)
            unique_name = f"Anim_{name}_{i+1:02d}"
            obj.Label = unique_name
            
            # --- CREATE JSON WAYPOINTS FOR THIS BATTERY ---
            # Movement: Start -> Feeder Edge -> Belt End -> Shredder Drop
            waypoints = [
                {"frame": 1,   "pos": [pos_x, pos_y, height_z]},
                {"frame": 120, "pos": [4000, pos_y, height_z]},   # End of feeder
                {"frame": 260, "pos": [6800, 600, 100]},           # Center of belt, lower Z
                {"frame": 300, "pos": [7300, 600, -300]}           # Fall into shredder
            ]
            
            animation_data.append({
                "name": unique_name,
                "waypoints": waypoints
            })

    doc.recompute()

    # View Fit
    try:
        Gui.SendMsgToActiveView("ViewFit")
        Gui.activeDocument().activeView().viewAxonometric()
    except:
        pass

if __name__ == "__main__":
    create_layout()