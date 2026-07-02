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
conv_length = 4200.0
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

#Dust Collector
width = 2400.0
depth = 2200.0
body_height = 3200.0
hopper_height = 2000.0
leg_height = 2800.0  # Height from floor to bottom of main body

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

def make_sphere(doc, name, radius, x, y, z, color, offset=(0,0,0)):
    shape = Part.makeSphere(radius)
    shape.translate(App.Vector(x + offset[0], y + offset[1], z + offset[2]))
    
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = shape
    obj.ViewObject.ShapeColor = color
    return obj



# --------------------------------------------------------------------------
# FEEDER
# --------------------------------------------------------------------------
def make_robust_spring(doc, name, radius, height, coils, wire_rad, x, y, z, offset=(0,0,0)):
    pitch = height / coils
    rings = []
    for i in range(coils):
        torus = Part.makeTorus(radius, wire_rad)
        z_shift = (i * pitch) + (pitch / 2)
        torus.translate(App.Vector(x + offset[0], y + offset[1], z + z_shift + offset[2]))
        rings.append(torus)
    spring_compound = Part.makeCompound(rings)
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = spring_compound
    obj.ViewObject.ShapeColor = col_spring_steel
    return obj

def make_trapezoid_hopper(doc, name, b_len, b_width, t_len, t_width, height, x, y, z, color, offset=(0,0,0)):
    p1 = App.Vector(-b_len/2, -b_width/2, 0)
    p2 = App.Vector(b_len/2, -b_width/2, 0)
    p3 = App.Vector(b_len/2, b_width/2, 0)
    p4 = App.Vector(-b_len/2, b_width/2, 0)
    wire_bottom = Part.makePolygon([p1, p2, p3, p4, p1])
    p1t = App.Vector(-t_len/2, -t_width/2, height)
    p2t = App.Vector(t_len/2, -t_width/2, height)
    p3t = App.Vector(t_len/2, t_width/2, height)
    p4t = App.Vector(-t_len/2, t_width/2, height)
    wire_top = Part.makePolygon([p1t, p2t, p3t, p4t, p1t])
    shape = Part.makeLoft([wire_bottom, wire_top], True)
    shape.translate(App.Vector(x + b_len/2 + offset[0], y + b_width/2 + offset[1], z + offset[2]))
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = shape
    obj.ViewObject.ShapeColor = color
    return obj

def create_auger_segment(doc, name, dia, pitch, length, x, y, z, color, offset=(0,0,0)):
    radius = dia / 2.0
    helix = Part.makeHelix(pitch, length, radius)
    profile = Part.makeCircle(radius, App.Vector(radius, 0, 0), App.Vector(0, 1, 0))
    auger_solid = Part.Wire(helix.Edges).makePipe(Part.Wire([profile]))
    auger_solid.rotate(App.Vector(0,0,0), App.Vector(0,1,0), 90)
    auger_solid.translate(get_global(x + offset[0], y + offset[1], z + offset[2]))
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = auger_solid
    obj.ViewObject.ShapeColor = color
    return obj

# --- EQUIPMENT BUILDERS ---

def create_equipment(doc, offset=(0,0,0)):
    make_box(doc, "Wall_Left", feeder_length, wall_thickness, feeder_height, 0, 0, 0, col_steel_grey, offset)
    make_box(doc, "Flange_L_Top", feeder_length, 100, wall_thickness, 0, -80, feeder_height-20, col_steel_grey, offset)
    make_box(doc, "Flange_L_Bot", feeder_length, 100, wall_thickness, 0, -80, 0, col_steel_grey,  offset)
    make_box(doc, "Wall_Right", feeder_length, wall_thickness, feeder_height, 0, feeder_width-20, 0, col_steel_grey, offset)
    make_box(doc, "Flange_R_Top", feeder_length, 100, wall_thickness, 0, feeder_width-20, feeder_height-20, col_steel_grey, offset)
    make_box(doc, "Flange_R_Bot", feeder_length, 100, wall_thickness, 0, feeder_width-20, 0, col_steel_grey, offset)
    make_box(doc, "Wall_Back", wall_thickness, feeder_width, feeder_height, -20, 0, 0, col_steel_grey, offset)
    make_box(doc, "Floor", feeder_length - grizzly_length, feeder_width - 40, wall_thickness, 0, 20, 20, col_steel_grey, offset)
    make_box(doc, "Liner_L", feeder_length, 10, feeder_height-50, 0, 20, 30, col_liner_red, offset)
    make_box(doc, "Liner_R", feeder_length, 10, feeder_height-50, 0, feeder_width-30, 30, col_liner_red, offset)
    make_box(doc, "Liner_Floor", feeder_length - grizzly_length, feeder_width - 60, 10, 0, 30, 40, col_liner_red, offset)
    num_bars = 5
    bar_w = (feeder_width - 40) / (num_bars * 1.5)
    gap = bar_w * 0.5
    curr_y = 20 + gap/2
    start_x = feeder_length - grizzly_length
    for i in range(num_bars + 1):
        make_box(doc, f"Bar_{i}", grizzly_length, bar_w, 40, start_x, curr_y, 20, col_steel_grey, offset)
        make_box(doc, f"BarCap_{i}", grizzly_length, bar_w, 10, start_x, curr_y, 60, col_liner_red, offset)
        curr_y += bar_w + gap
    spring_h, spring_radius = 300, 60
    mounts = [(400, -150), (400, feeder_width + 150), (feeder_length - 400, -150), (feeder_length - 400, feeder_width + 150)]
    for i, (sx, sy) in enumerate(mounts):
        make_box(doc, f"SpringTop_{i}", 300, 300, 20, sx-150, sy-150, 0, col_steel_grey, offset)
        make_robust_spring(doc, f"Spring_{i}", spring_radius, spring_h, 8, 12, sx, sy, -spring_h, offset)
        make_box(doc, f"SpringBot_{i}", 350, 350, 20, sx-175, sy-175, -spring_h-20, col_steel_grey, offset)
        gusset_y = 0 if sy < 0 else feeder_width
        gusset_off = -20 if sy < 0 else 0
        make_box(doc, f"Gusset_{i}", 200, 150, 200, sx-100, gusset_y + gusset_off, -200, col_steel_grey, offset)
    ex_x = 1200
    make_box(doc, "ExciterBox", 800, feeder_width+200, 400, ex_x, -100, -400, col_steel_grey, offset)
    make_box(doc, "MotorBase", 600, 400, 50, ex_x, -700, -950, col_base_blue, offset)
    make_box(doc, "MotorPivot", 200, 300, 150, ex_x+200, -650, -900, col_base_blue, offset)
    make_cylinder(doc, "Motor", 250, 550, ex_x+300, -500, -500, col_motor_teal, offset, App.Vector(0,1,0))
    make_cylinder(doc, "Pulley_Top", 120, 60, ex_x+400, -150, -200, col_liner_red, offset, App.Vector(0,1,0))
    make_cylinder(doc, "Pulley_Bot", 80, 60, ex_x+300, -500, -500, col_liner_red, offset, App.Vector(0,1,0))
    for k in range(3):
        belt_off = k * 20
        make_box(doc, f"Belt_{k}", 15, 15, 680, ex_x+270, -180 + belt_off, -480, col_black_rubber, offset, -25, App.Vector(0,1,0))




# --------------------------------------------------------------------------
# CONVEYOR
# --------------------------------------------------------------------------
def build_conveyor(doc, offset=(0,0,0)):
    make_box(doc, "Rail_Left", conv_length, rail_thick, rail_height, 0, 0, conv_height - rail_height, col_frame_grey, offset)
    make_box(doc, "Rail_Right", conv_length, rail_thick, rail_height, 0, conv_width - rail_thick, conv_height - rail_height, col_frame_grey, offset)
    num_bolts = int(conv_length / 300)
    for i in range(num_bolts):
        bx, bz = 150 + (i * 300), conv_height - (rail_height/2)
        make_cylinder(doc, f"Bolt_L_{i}", 8, 5, bx, -5, bz, col_roller_silver, offset, App.Vector(0,1,0))
        make_cylinder(doc, f"Bolt_R_{i}", 8, 5, bx, conv_width, bz, col_roller_silver, offset, App.Vector(0,1,0))
    num_rollers, rollers_shape_list = int(conv_length / roller_pitch), []
    current_x, z_roller = (conv_length - ((num_rollers-1)*roller_pitch)) / 2, conv_height - (roller_dia/2) - 5
    for i in range(num_rollers):
        cyl = Part.makeCylinder(roller_dia/2, roller_width)
        cyl.rotate(App.Vector(0,0,0), App.Vector(1,0,0), -90)
        cyl.translate(App.Vector(current_x + offset[0], rail_thick + ((conv_width - 2*rail_thick - roller_width)/2) + offset[1], z_roller + offset[2]))
        rollers_shape_list.append(cyl)
        current_x += roller_pitch
    roller_compound = Part.makeCompound(rollers_shape_list)
    obj_r = doc.addObject("Part::Feature", "Rollers_Set")
    obj_r.Shape = roller_compound
    obj_r.ViewObject.ShapeColor = col_roller_silver
    leg_positions = [200, conv_length/2 - 50, conv_length - 300]
    for i, lx in enumerate(leg_positions):
        make_box(doc, f"Leg_L_{i}", 80, 80, conv_height - rail_height, lx, 0, 0, col_frame_grey, offset)
        make_box(doc, f"Leg_R_{i}", 80, 80, conv_height - rail_height, lx, conv_width - 80, 0, col_frame_grey, offset)
        make_box(doc, f"Leg_Brace_{i}", 80, conv_width, 60, lx, 0, conv_height - rail_height - 200, col_frame_grey, offset)
        make_cylinder(doc, f"Foot_Pad_L_{i}", 40, 20, lx + 40, 40, 0, col_foot_black, offset)
        make_cylinder(doc, f"Foot_Thread_L_{i}", 10, 100, lx + 40, 40, 0, col_roller_silver, offset)
        make_cylinder(doc, f"Foot_Pad_R_{i}", 40, 20, lx + 40, conv_width - 40, 0, col_foot_black, offset)
        make_cylinder(doc, f"Foot_Thread_R_{i}", 10, 100, lx + 40, conv_width - 40, 0, col_roller_silver, offset)
    box_x, box_y, box_z, box_w, box_h, box_d = (conv_length / 2) - 100, -150, conv_height - 500, 250, 400, 150
    make_box(doc, "ControlBox_Main", box_w, box_d, box_h, box_x, box_y, box_z, col_box_dark, offset)
    make_box(doc, "Mounting_Plate", box_w + 40, 20, box_h, box_x - 20, box_y + box_d, box_z, col_frame_grey, offset)
    make_cylinder(doc, "Btn_Stop", 20, 20, box_x + box_w/2, box_y, box_z + 300, col_button_red, offset,  App.Vector(0,1,0))
    make_cylinder(doc, "Btn_Start", 15, 15, box_x + box_w/2, box_y, box_z + 240, (0.2, 0.8, 0.2), offset, App.Vector(0,1,0))
    make_cylinder(doc, "Knob_Speed", 12, 25, box_x + box_w/2, box_y, box_z + 180, col_roller_silver, offset, App.Vector(0,1,0))
    make_cylinder(doc, "Cable_Gland", 15, 30, box_x + 50, box_y + box_d/2, box_z - 30, (0.1,0.1,0.1), offset)




# --------------------------------------------------------------------------
# SHREDDER
# --------------------------------------------------------------------------
def build_shredder(doc, offset=(0,0,0)):
    beam_size = 200.0
    make_box(doc, "Beam_Bot_F", frame_len, beam_size, beam_size, 0, 0, 0, COL_FRAME_GREY, offset)
    make_box(doc, "Beam_Bot_B", frame_len, beam_size, beam_size, 0, frame_width-beam_size, 0, COL_FRAME_GREY, offset)
    make_box(doc, "Beam_Top_F", frame_len, beam_size, beam_size, 0, 0, frame_height, COL_FRAME_GREY, offset)
    make_box(doc, "Beam_Top_B", frame_len, beam_size, beam_size, 0, frame_width-beam_size, frame_height, COL_FRAME_GREY, offset)
    leg_coords = [0, frame_len/2 - 100, frame_len - beam_size]
    for i, lx in enumerate(leg_coords):
        make_box(doc, f"Leg_F_{i}", beam_size, beam_size, frame_height, lx, 0, 0, COL_FRAME_GREY, offset)
        make_box(doc, f"Leg_B_{i}", beam_size, beam_size, frame_height, lx, frame_width-beam_size, 0, COL_FRAME_GREY, offset)
        make_box(doc, f"Cross_Bot_{i}", beam_size, frame_width, beam_size/2, lx, 0, 50, COL_FRAME_GREY, offset)
        make_box(doc, f"Cross_Top_{i}", beam_size, frame_width, beam_size, lx, 0, frame_height, COL_FRAME_GREY, offset)
    box_x, box_y, box_z = (frame_len - box_len) / 2, (frame_width - box_width) / 2, frame_height + beam_size
    make_box(doc, "ShredderBox", box_len, box_width, box_height, box_x, box_y, box_z, COL_BOX_GREEN, offset)
    rib_thick, rib_depth = 40, 40
    for i in range(4):
        rx = box_x + (i * (box_len/3))
        make_box(doc, f"Rib_V_{i}", rib_thick, box_width + 2*rib_depth, box_height, rx, box_y - rib_depth, box_z, COL_BOX_GREEN, offset)
    for i in range(3):
        rz = box_z + (i * (box_height/2))
        make_box(doc, f"Rib_H_{i}", box_len, box_width + 2*rib_depth, rib_thick, box_x, box_y - rib_depth, rz, COL_BOX_GREEN, offset)
    make_trapezoid_hopper(doc, "Hopper", box_len, box_width, box_len + 500, box_width + 500, 800.0, box_x, box_y, box_z + box_height, COL_HOPPER_BLUE, offset)
    gb_x, gb_len = box_x + box_len + 50, 800
    make_box(doc, "Gearbox_Main", gb_len, box_width, 700, gb_x, box_y, box_z, COL_HOPPER_BLUE, offset)
    make_cylinder(doc, "Bearing_R", 250, 200, gb_x, box_y + box_width/2, box_z + 300, COL_HOPPER_BLUE, offset, App.Vector(1,0,0))
    make_box(doc, "Guard_R", 100, box_width, 800, gb_x + gb_len, box_y, box_z, COL_MOTOR_GREY, offset)
    br_x = box_x - 500
    make_box(doc, "BearingBox_L", 450, box_width, 600, br_x, box_y, box_z, COL_HOPPER_BLUE, offset)
    make_cylinder(doc, "Shaft_L", 100, 100, box_x - 100, box_y + box_width/2, box_z + 300, COL_SHAFT_RED, offset, App.Vector(1,0,0))
    motor_rad, motor_len, motor_x, motor_z = 250, 600, box_x - 200, 300 
    make_cylinder(doc, "Motor_L", motor_rad, motor_len, motor_x, frame_width/2, motor_z, COL_MOTOR_GREY, offset, App.Vector(1,0,0))
    make_box(doc, "MotorBase_L", motor_len, 500, 50, motor_x, (frame_width/2)-250, motor_z - motor_rad, col_frame_grey, offset)
    motor_x_r = gb_x + 100
    make_cylinder(doc, "Motor_R", motor_rad, motor_len, motor_x_r, frame_width/2, motor_z, COL_MOTOR_GREY, offset, App.Vector(1,0,0))
    make_box(doc, "MotorBase_R", motor_len, 500, 50, motor_x_r, (frame_width/2)-250, motor_z - motor_rad, col_frame_grey, offset)
    make_box(doc, "BeltCover_L", 150, 400, frame_height, motor_x, (frame_width/2)-200, motor_z, col_frame_grey, offset)
    make_box(doc, "BeltCover_R", 150, 400, frame_height, motor_x_r, (frame_width/2)-200, motor_z, col_frame_grey, offset)




# --------------------------------------------------------------------------
# SCREW CONVEYOR
# --------------------------------------------------------------------------
def screw_conveyor(doc, offset=(0,0,0)):
    outer_r, inner_r = trough_dia / 2.0, (trough_dia / 2.0) - trough_thick
    cyl_outer = Part.makeCylinder(outer_r, trough_len)
    cyl_outer.rotate(App.Vector(0,0,0), App.Vector(0,1,0), 90)
    cyl_inner = Part.makeCylinder(inner_r, trough_len)
    cyl_inner.rotate(App.Vector(0,0,0), App.Vector(0,1,0), 90)
    box_cut = Part.makeBox(trough_len, trough_dia, trough_dia)
    box_cut.translate(App.Vector(0, -trough_dia/2, 0))
    trough_shape = cyl_outer.cut(cyl_inner).cut(box_cut)
    trough_shape.translate(App.Vector(offset[0], offset[1], offset[2]))
    t_obj = doc.addObject("Part::Feature", "Trough_Steel")
    t_obj.Shape = trough_shape
    t_obj.ViewObject.ShapeColor = col_steel_grey
    lc_outer = Part.makeCylinder(inner_r, trough_len)
    lc_outer.rotate(App.Vector(0,0,0), App.Vector(0,1,0), 90)
    lc_inner = Part.makeCylinder(inner_r - 5.0, trough_len)
    lc_inner.rotate(App.Vector(0,0,0), App.Vector(0,1,0), 90)
    l_box_cut = Part.makeBox(trough_len, trough_dia, trough_dia)
    l_box_cut.translate(App.Vector(0, -trough_dia/2, 0))
    liner_shape = lc_outer.cut(lc_inner).cut(l_box_cut)
    liner_shape.translate(App.Vector(*offset)) 
    l_obj = doc.addObject("Part::Feature", "Trough_Liner")
    l_obj.Shape = liner_shape
    l_obj.ViewObject.ShapeColor = col_blue_liner
    num_segments = int(trough_len / segment_len)
    for i in range(num_segments):
        seg_x = i * segment_len
        create_auger_segment(doc, f"Auger_{i}", augur_dia, augur_pitch, segment_len, seg_x, 0, 0, col_steel_grey, offset)
        make_cylinder(doc, f"Shaft_{i}", 40, segment_len, seg_x, 0, 0, col_steel_grey, offset, axis=App.Vector(1,0,0))
    make_box(doc, "EndPlate", 30.0, trough_dia+100, trough_dia/2 + 200, trough_len, -(trough_dia+100)/2, -trough_dia/2, col_steel_grey, offset)
    make_box(doc, "MotorShelf", 600, 600, 20, trough_len, 250, 200, col_steel_grey, offset)
    motor_rad = 250.0 / 2.0
    make_cylinder(doc, "MotorBody", motor_rad, 450.0, trough_len + 50, 400, 200 + motor_rad + 20, col_motor_grey, offset, axis=App.Vector(1,0,0))
    make_box(doc, "BeltGuard", 150, 400, 700, trough_len + 500, -200, -200, col_guard_yellow, offset)
    spacing = trough_len / 4.0
    for i in range(5):
        fx = i * spacing
        make_box(doc, f"Saddle_{i}", 20, trough_dia+100, 20, fx, -(trough_dia+100)/2, -trough_dia/2, col_steel_grey, offset)
        make_box(doc, f"Leg_{i}", 20, 400, 300, fx, -200, -trough_dia/2 - 300, col_steel_grey, offset)
        make_box(doc, f"Foot_{i}", 100, 500, 20, fx-40, -250, -trough_dia/2 - 320, col_steel_grey, offset)
    lid_len, lid_w = 1500, trough_dia + 50
    make_box(doc, "Lid_1", lid_len, lid_w, 10, 500, -lid_w/2, 0, col_lid_metal, offset)
    make_box(doc, "Lid_2", lid_len, lid_w, 10, 2500, -lid_w/2, 0, col_lid_metal, offset, rotation_axis=App.Vector(1,0,0), rotation_angle=60)
    make_box(doc, "Lid_3", lid_len, lid_w, 10, 4500, -lid_w/2, 0, col_lid_metal, offset)



# --------------------------------------------------------------------------
# CRUSHER
# --------------------------------------------------------------------------
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


# --------------------------------------------------------------------------
# POCKET CONVEYOR
# --------------------------------------------------------------------------

def pocket_conveyor(doc, offset=(0,0,0)):
    """
    Draws a cleated/pocket conveyor based on the reference image.
    Offset allows placement at specific global coordinates.
    """
    
    # --- Parameters ---
    conv_len = 7000.0
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


# --------------------------------------------------------------------------
# PULSE DUCT COLLECTOR
# --------------------------------------------------------------------------
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


# --------------------------------------------------------------------------
# ESP
# --------------------------------------------------------------------------

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




# --------------------------------------------------------------------------
# BALL MILL
# --------------------------------------------------------------------------
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



# --------------------------------------------------------------------------
# DECLINE CONVEYOR
# --------------------------------------------------------------------------
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



# --------------------------------------------------------------------------
# CURVE CONVEYOR
# --------------------------------------------------------------------------

def curv_conveyor(doc, name_prefix, start_angle, offset_coords):
    """
    Builds a conveyor starting at 'start_angle' and sweeping -90 degrees (Right Turn).
    offset_coords: (x,y,z) tuple passed to helper functions.
    """
    # Dimensions
    inner_radius = 2800.0
    belt_width = 1000.0
    outer_radius = inner_radius + belt_width
    frame_height = 700.0
    belt_thickness = 300.0
    leg_height = 900.0
    sweep = -80.0 # Right Turn
    
    # Colors
    col_belt = (0.1, 0.4, 0.9)    # Blue
    col_frame = (0.7, 0.7, 0.7)   # Grey
    col_chain = (0.9, 0.8, 0.1)   # Yellow
    col_motor = (0.2, 0.3, 0.5)   # Dark Blue

    # 1. REVOLVED SURFACES (Belt, Frames)
    make_revolve_segment(doc, f"{name_prefix}_Belt", inner_radius + 5, belt_width - 10, belt_thickness, -belt_thickness, sweep, start_angle, col_belt, offset_coords)
    make_revolve_segment(doc, f"{name_prefix}_FrameIn", inner_radius, 5, frame_height, -frame_height + 20, sweep, start_angle, col_frame, offset_coords)
    make_revolve_segment(doc, f"{name_prefix}_FrameOut", outer_radius - 5, 5, frame_height, -frame_height + 20, sweep, start_angle, col_frame, offset_coords)
    make_revolve_segment(doc, f"{name_prefix}_Guard", outer_radius, 20, frame_height + 10, -frame_height + 20, sweep, start_angle, col_frame, offset_coords)

    # 2. LEGS (Calculated based on angle)
    # We create legs at relative angles 10, 45, 80 along the sweep
    leg_rel_angles = [-10, -45, -80]
    
    for i, rel_ang in enumerate(leg_rel_angles):
        # The absolute angle in the world
        abs_angle_deg = start_angle + rel_ang
        rad = math.radians(abs_angle_deg)
        leg_size = 40.0
        
        # Polar Coordinates
        ix = inner_radius * math.cos(rad)
        iy = inner_radius * math.sin(rad)
        ox = outer_radius * math.cos(rad)
        oy = outer_radius * math.sin(rad)
        dist = outer_radius - inner_radius
        
        # Inner Post
        make_box(doc, f"{name_prefix}_L{i}_In", leg_size, leg_size, leg_height, 
                 ix - leg_size/2, iy - leg_size/2, -leg_height, col_frame, offset_coords, rotation_angle=abs_angle_deg)
        # Outer Post
        make_box(doc, f"{name_prefix}_L{i}_Out", leg_size, leg_size, leg_height, 
                 ox - leg_size/2, oy - leg_size/2, -leg_height, col_frame, offset_coords, rotation_angle=abs_angle_deg)
        # Cross Beam
        make_box(doc, f"{name_prefix}_L{i}_Beam", dist + leg_size, leg_size, leg_size, 
                 ix - leg_size/2, iy - leg_size/2, -leg_height/2, col_frame, offset_coords, rotation_angle=abs_angle_deg)

    # 3. CHAIN PINS
    num_rollers = 20
    step = sweep / num_rollers
    for i in range(int(num_rollers) + 1):
        rel_ang = i * step
        abs_angle_deg = start_angle + rel_ang
        rad = math.radians(abs_angle_deg)
        
        x = (outer_radius - 15) * math.cos(rad)
        y = (outer_radius - 15) * math.sin(rad)
        
        make_box(doc, f"{name_prefix}_Pin{i}", 15, 5, 5, x, y, 8.0, col_chain, offset_coords, rotation_angle=abs_angle_deg)

    # 4. MOTOR (Placed at the Start Angle on Outer Radius)
    rad_motor = math.radians(start_angle)
    mx = (outer_radius) * math.cos(rad_motor)
    my = (outer_radius) * math.sin(rad_motor)
    mz = -25
    
    # We must rotate the motor box to align with the start tangent
    make_box(doc, f"{name_prefix}_MBox", 120, 100, 100, mx - 60, my - 50, mz, col_motor, offset_coords, rotation_angle=start_angle)
    # The cylinder axis usually points perpendicular, or along Y local. 
    # To keep it simple in this specific syntax, we use a box or pre-calculated cylinder placement.
    # Using Y-axis cylinder rotated by start_angle
    cyl_x = mx + (60 * math.cos(rad_motor))
    cyl_y = my + (60 * math.sin(rad_motor))
    
    # Note: make_cylinder with 'axis' only supports X or Y alignment. 
    # For arbitrary diagonal alignment (NE/SW/etc), simple axis arguments aren't enough without 'Rotation' object.
    # We will stick to the box for the motor to ensure stability across all 4 angles in this snippet.

# --------------------------------------------------------------------------
# 3. FOUR SEPARATE CODES (CALLED FUNCTIONS)
# --------------------------------------------------------------------------

def create_north_facing_conveyor(doc, offset=(0,0,0)):
    # North-East Quadrant (Start 0, Sweep 90) or North-West?
    # Let's assume Standard Right Turn ending pointing North.
    # Input West (180), Turn Right (-90) -> Output North (90)? No.
    # Input West (180 deg). Turn Right (CW) -> 180 - 90 = 90 (North).
    curv_conveyor(doc, "North", 180, offset)

def create_south_facing_conveyor(doc, offset=(0,0,0)):
    # Input East (0 deg). Turn Right (CW) -> 0 - 90 = -90 (South).
    curv_conveyor(doc, "South", 0, offset)

def create_east_facing_conveyor(doc, offset=(0,0,0)):
    # Input North (90 deg). Turn Right (CW) -> 90 - 90 = 0 (East).
    curv_conveyor(doc, "East", 90, offset)

def create_west_facing_conveyor(doc, offset=(0,0,0)):
    # Input South (-90/270 deg). Turn Right (CW) -> -90 - 90 = -180 (West).
    curv_conveyor(doc, "West", 270, offset)



# --------------------------------------------------------------------------
# MAGNETIC SEPARATOR
# --------------------------------------------------------------------------
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


# --------------------------------------------------------------------------
# INCLINED CONVEYOR
# --------------------------------------------------------------------------

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



# --------------------------------------------------------------------------
# SPIRAL CONCENTRATOR
# --------------------------------------------------------------------------
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



# --------------------------------------------------------------------------
# GRAVITY CONCENTRATOR
# --------------------------------------------------------------------------

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


# --------------------------------------------------------------------------
# PIPING CONNECTIONS
# --------------------------------------------------------------------------
def build_duct_connection(doc):
    """
    Builds a connecting duct (pipe) between the Pulse Duct Collector outlet and the ESP inlet.
    Positions are calculated based on the fixed offsets used in create_layout.
    """
    # --- Dimensions & Coordinates ---
    # Dust Collector is at (31000, 250, 0) with depth 2200
    # ESP is at (31000, 6000, 0) with depth 2000
    
    dc_center_y = 250.0
    dc_depth = 2200.0
    esp_center_y = 6000.0
    esp_depth = 2000.0
    
    # Calculate connection points
    start_y = dc_center_y + (dc_depth / 2)  # Back face of DC
    end_y = esp_center_y - (esp_depth / 2)  # Front face of ESP
    
    pipe_x = 31000.0        # Centerline X
    pipe_z = 4500.0         # Elevation Height
    pipe_radius = 300.0
    pipe_length = end_y - start_y
    
    # --- Geometry Creation ---
    
    # 1. Main Duct Pipe (Aligned along Y-axis)
    make_cylinder(doc, "Duct_DC_ESP_Main", pipe_radius, pipe_length, 
                  pipe_x, start_y, pipe_z, col_black, (0,0,0), axis=App.Vector(0,1,0))

    # 2. Flange at Dust Collector Side
    make_cylinder(doc, "Duct_Flange_Start", pipe_radius + 50, 40, 
                  pipe_x, start_y, pipe_z, col_dark_metal, (0,0,0), axis=App.Vector(0,1,0))
                  
    # 3. Flange at ESP Side
    make_cylinder(doc, "Duct_Flange_End", pipe_radius + 50, 40, 
                  pipe_x, end_y - 40, pipe_z, col_dark_metal, (0,0,0), axis=App.Vector(0,1,0))
                  
    # 4. Support Stands (Legs holding up the pipe)
    num_supports = 2
    support_spacing = pipe_length / (num_supports + 1)
    
    for i in range(num_supports):
        sy = start_y + ((i + 1) * support_spacing)
        
        # Vertical Leg
        make_box(doc, f"Duct_Support_Leg_{i}", 100, 100, pipe_z - pipe_radius, 
                 pipe_x - 50, sy - 50, 0, col_frame_grey, (0,0,0))
                 
        # Saddle/Cradle under pipe
        make_box(doc, f"Duct_Support_Cradle_{i}", 200, 100, 100, 
                 pipe_x - 100, sy - 50, pipe_z - pipe_radius - 50, col_frame_grey, (0,0,0))



# --------------------------------------------------------------------------
# CURVE CONVEYOR
# --------------------------------------------------------------------------

def make_revolve_segment(doc, name, r_start, width, height, z_start, sweep_angle, start_rotation, color, offset=(0,0,0)):
    # 1. Create Profile at Angle 0 (X-axis)
    p1 = App.Vector(r_start, 0, z_start)
    p2 = App.Vector(r_start + width, 0, z_start)
    p3 = App.Vector(r_start + width, 0, z_start + height)
    p4 = App.Vector(r_start, 0, z_start + height)
    wire = Part.makePolygon([p1, p2, p3, p4, p1])
    face = Part.Face(wire)
    
    # 2. Revolve to create the arc length
    shape = face.revolve(App.Vector(0,0,0), App.Vector(0,0,1), sweep_angle)
    
    # 3. Rotate to the correct cardinal direction (Start Angle)
    if start_rotation != 0:
        shape.rotate(App.Vector(0,0,0), App.Vector(0,0,1), start_rotation)

    # 4. Translate using your requested syntax logic
    shape.translate(App.Vector(offset[0], offset[1], offset[2]))
    
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = shape
    obj.ViewObject.ShapeColor = color
    return obj


def curv_conveyor(doc, name_prefix, start_angle, offset_coords):
    """
    Builds a conveyor starting at 'start_angle' and sweeping -90 degrees (Right Turn).
    offset_coords: (x,y,z) tuple passed to helper functions.
    """
    # Dimensions
    inner_radius = 2800.0
    belt_width = 1500.0
    outer_radius = inner_radius + belt_width
    frame_height = 300.0
    belt_thickness = 20.0
    leg_height = 1200.0
    sweep = -90.0 # Right Turn
    
    # Colors
    col_belt = (0.1, 0.4, 0.9)    # Blue
    col_frame = (0.7, 0.7, 0.7)   # Grey
    col_chain = (0.9, 0.8, 0.1)   # Yellow
    col_motor = (0.2, 0.3, 0.5)   # Dark Blue

    # 1. REVOLVED SURFACES (Belt, Frames)
    make_revolve_segment(doc, f"{name_prefix}_Belt", inner_radius + 5, belt_width - 10, belt_thickness, -belt_thickness, sweep, start_angle, col_belt, offset_coords)
    make_revolve_segment(doc, f"{name_prefix}_FrameIn", inner_radius, 5, frame_height, -frame_height + 20, sweep, start_angle, col_frame, offset_coords)
    make_revolve_segment(doc, f"{name_prefix}_FrameOut", outer_radius - 5, 5, frame_height, -frame_height + 20, sweep, start_angle, col_frame, offset_coords)
    make_revolve_segment(doc, f"{name_prefix}_Guard", outer_radius, 20, frame_height + 10, -frame_height + 20, sweep, start_angle, col_frame, offset_coords)

    # 2. LEGS (Calculated based on angle)
    # We create legs at relative angles 10, 45, 80 along the sweep
    leg_rel_angles = [-10, -45, -80]
    
    for i, rel_ang in enumerate(leg_rel_angles):
        # The absolute angle in the world
        abs_angle_deg = start_angle + rel_ang
        rad = math.radians(abs_angle_deg)
        leg_size = 40.0
        
        # Polar Coordinates
        ix = inner_radius * math.cos(rad)
        iy = inner_radius * math.sin(rad)
        ox = outer_radius * math.cos(rad)
        oy = outer_radius * math.sin(rad)
        dist = outer_radius - inner_radius
        
        # Inner Post
        make_box(doc, f"{name_prefix}_L{i}_In", leg_size, leg_size, leg_height, 
                 ix - leg_size/2, iy - leg_size/2, -leg_height, col_frame, offset_coords, rotation_angle=abs_angle_deg)
        # Outer Post
        make_box(doc, f"{name_prefix}_L{i}_Out", leg_size, leg_size, leg_height, 
                 ox - leg_size/2, oy - leg_size/2, -leg_height, col_frame, offset_coords, rotation_angle=abs_angle_deg)
        # Cross Beam
        make_box(doc, f"{name_prefix}_L{i}_Beam", dist + leg_size, leg_size, leg_size, 
                 ix - leg_size/2, iy - leg_size/2, -leg_height/2, col_frame, offset_coords, rotation_angle=abs_angle_deg)

    # 3. CHAIN PINS
    num_rollers = 20
    step = sweep / num_rollers
    for i in range(int(num_rollers) + 1):
        rel_ang = i * step
        abs_angle_deg = start_angle + rel_ang
        rad = math.radians(abs_angle_deg)
        
        x = (outer_radius - 15) * math.cos(rad)
        y = (outer_radius - 15) * math.sin(rad)
        
        make_box(doc, f"{name_prefix}_Pin{i}", 15, 5, 5, x, y, 8.0, col_chain, offset_coords, rotation_angle=abs_angle_deg)

    # 4. MOTOR (Placed at the Start Angle on Outer Radius)
    rad_motor = math.radians(start_angle)
    mx = (outer_radius) * math.cos(rad_motor)
    my = (outer_radius) * math.sin(rad_motor)
    mz = -25
    
    # We must rotate the motor box to align with the start tangent
    make_box(doc, f"{name_prefix}_MBox", 120, 100, 100, mx - 60, my - 50, mz, col_motor, offset_coords, rotation_angle=start_angle)
    # The cylinder axis usually points perpendicular, or along Y local. 
    # To keep it simple in this specific syntax, we use a box or pre-calculated cylinder placement.
    # Using Y-axis cylinder rotated by start_angle
    cyl_x = mx + (60 * math.cos(rad_motor))
    cyl_y = my + (60 * math.sin(rad_motor))
    
    # Note: make_cylinder with 'axis' only supports X or Y alignment. 
    # For arbitrary diagonal alignment (NE/SW/etc), simple axis arguments aren't enough without 'Rotation' object.
    # We will stick to the box for the motor to ensure stability across all 4 angles in this snippet.

# --------------------------------------------------------------------------
# 3. FOUR SEPARATE CODES (CALLED FUNCTIONS)
# --------------------------------------------------------------------------

def create_north_facing_conveyor(doc, offset=(0,0,0)):
    # North-East Quadrant (Start 0, Sweep 90) or North-West?
    # Let's assume Standard Right Turn ending pointing North.
    # Input West (180), Turn Right (-90) -> Output North (90)? No.
    # Input West (180 deg). Turn Right (CW) -> 180 - 90 = 90 (North).
    curv_conveyor(doc, "North", 180, offset)

def create_south_facing_conveyor(doc, offset=(0,0,0)):
    # Input East (0 deg). Turn Right (CW) -> 0 - 90 = -90 (South).
    curv_conveyor(doc, "South", 0, offset)

def create_east_facing_conveyor(doc, offset=(0,0,0)):
    # Input North (90 deg). Turn Right (CW) -> 90 - 90 = 0 (East).
    curv_conveyor(doc, "East", 90, offset)



# ==============================================================================
# MAIN DRAWING FUNCTION: VERTICAL COMPONENT PCB
# ==============================================================================

def build_vertical_component_pcb(doc, offset=(0,0,0), scale_factor=1.0):
    """
    Draws the vertical PCB with top IC, scattered SOICs, and crystal.
    """
    
    S = scale_factor
    objects_to_group = []

    # --- COLORS ---
    c_green_pcb  = (0.00, 0.50, 0.25)  # Medium Green
    c_black      = (0.15, 0.15, 0.15)  # IC Body
    c_silver     = (0.85, 0.85, 0.90)  # Solder / Crystal
    c_tan        = (0.75, 0.65, 0.50)  # Capacitors
    c_trace      = (0.20, 0.70, 0.40)  # Lighter Green Traces
    c_text       = (0.90, 0.90, 0.90)  # White Silk Screen

    # --- DIMENSIONS ---
    w, d, h = 100.0 * S, 160.0 * S, 2.0 * S # Vertical Aspect
    
    # 1. BASE BOARD
    board = make_box(doc, "PCB_Substrate", w, d, h, 0, 0, 0, c_green_pcb, offset)
    objects_to_group.append(board)

    # 2. LARGE TOP CHIP (Partially visible)
    # A massive black block at the top
    top_ic_w = 60.0 * S
    top_ic_d = 40.0 * S
    tx = (w - top_ic_w) / 2
    ty = d - 30 * S # Positioned so top hangs off or sits high
    
    objects_to_group.append(make_box(doc, "IC_Top_Big", top_ic_w, top_ic_d, 3*S, tx, ty, h, c_black, offset))
    # Dot
    objects_to_group.append(make_cylinder(doc, "IC_Top_Dot", 2*S, 0.5*S, tx+top_ic_w/2, ty+10*S, h+3*S, (0.3,0.3,0.3), offset))

    # 3. SMALLER SOIC CHIPS (Middle)
    # Two rectangular chips in the middle area
    soic_w, soic_d = 12*S, 12*S
    
    # Chip 1 (Left-ish)
    cx1, cy1 = 40*S, 90*S
    objects_to_group.append(make_box(doc, "SOIC_1_Body", soic_w, soic_d, 2*S, cx1, cy1, h, c_black, offset))
    # Pins
    for i in range(4):
        px = cx1 - 2*S
        py = cy1 + (i * 3 * S)
        objects_to_group.append(make_box(doc, f"SOIC1_PinL_{i}", 2*S, 1.5*S, 1*S, px, py, h, c_silver, offset))
        objects_to_group.append(make_box(doc, f"SOIC1_PinR_{i}", 2*S, 1.5*S, 1*S, px+soic_w+2*S, py, h, c_silver, offset))

    # Chip 2 (Right-ish)
    cx2, cy2 = 65*S, 85*S
    objects_to_group.append(make_box(doc, "SOIC_2_Body", soic_w, soic_d, 2*S, cx2, cy2, h, c_black, offset))
    for i in range(4):
        px = cx2 - 2*S
        py = cy2 + (i * 3 * S)
        objects_to_group.append(make_box(doc, f"SOIC2_PinL_{i}", 2*S, 1.5*S, 1*S, px, py, h, c_silver, offset))
        objects_to_group.append(make_box(doc, f"SOIC2_PinR_{i}", 2*S, 1.5*S, 1*S, px+soic_w+2*S, py, h, c_silver, offset))

    # 4. CRYSTAL OSCILLATOR (Bottom Right)
    # Shiny metallic rectangle
    crys_w, crys_d = 10*S, 14*S
    crx, cry = 80*S, 30*S
    objects_to_group.append(make_box(doc, "Crystal_Body", crys_w, crys_d, 3*S, crx, cry, h, c_silver, offset))
    # Pads underneath corners
    objects_to_group.append(make_box(doc, "Crystal_Pad1", 2*S, 2*S, 0.5*S, crx-1*S, cry-1*S, h, c_silver, offset))
    objects_to_group.append(make_box(doc, "Crystal_Pad2", 2*S, 2*S, 0.5*S, crx+crys_w, cry+crys_d, h, c_silver, offset))

    # 5. DENSE SMD FIELD (Scattered everywhere)
    # Generating lots of tiny resistors/capacitors
    for i in range(50):
        # Random positions
        rx = random.uniform(5*S, w - 5*S)
        ry = random.uniform(5*S, d - 40*S) # Keep away from very top IC
        
        # Avoid the big chips areas roughly
        if (ry > 80*S and ry < 110*S): continue # Skip middle band
        
        # Orientation
        is_vert = random.choice([True, False])
        rw, rl = (2*S, 4*S) if is_vert else (4*S, 2*S)
        
        color = random.choice([c_black, c_tan])
        name = f"SMD_{i}"
        
        # Body
        objects_to_group.append(make_box(doc, name, rw, rl, 1.5*S, rx, ry, h, color, offset))
        # Pads
        if is_vert:
            objects_to_group.append(make_box(doc, name+"_P1", rw, 1*S, 0.5*S, rx, ry-1*S, h, c_silver, offset))
            objects_to_group.append(make_box(doc, name+"_P2", rw, 1*S, 0.5*S, rx, ry+rl, h, c_silver, offset))
        else:
            objects_to_group.append(make_box(doc, name+"_P1", 1*S, rl, 0.5*S, rx-1*S, ry, h, c_silver, offset))
            objects_to_group.append(make_box(doc, name+"_P2", 1*S, rl, 0.5*S, rx+rw, ry, h, c_silver, offset))

    # 6. VIAS (The field of dots)
    # Create a grid of tiny silver rings
    for x in range(0, int(w/S), 8):
        for y in range(0, int(d/S), 8):
            vx = x * S
            vy = y * S
            # Random dropout to make it look natural
            if random.random() > 0.3:
                objects_to_group.append(make_cylinder(doc, f"Via_{x}_{y}", 1*S, 0.2*S, vx, vy, h, c_silver, offset))

    # 7. TRACES
    # Winding lines connecting things
    for i in range(12):
        tx = random.uniform(10*S, 90*S)
        ty = random.uniform(10*S, 140*S)
        
        # Vertical run
        v_len = random.uniform(10*S, 30*S)
        objects_to_group.append(make_box(doc, f"Trace_V_{i}", 0.6*S, v_len, 0.1*S, tx, ty, h, c_trace, offset))
        # 45 degree jog (simulated with small blocks)
        objects_to_group.append(make_box(doc, f"Trace_Jog_{i}", 2*S, 0.6*S, 0.1*S, tx+0.5*S, ty+v_len, h, c_trace, offset))

    # 4. GROUPING
    group = doc.addObject("App::DocumentObjectGroup", "Vertical_Component_PCB")
    group.Group = objects_to_group
    
    print(f"Vertical PCB generated at {offset} with colors retained.")


# ==============================================================================
# MAIN DRAWING FUNCTION: GREEN PCB WITH CENTRAL QFP
# ==============================================================================

def build_central_chip_pcb(doc, offset=(0,0,0), scale_factor=1.0):
    """
    Draws the PCB with a large central chip and side diodes.
    """
    
    S = scale_factor
    objects_to_group = []

    # --- COLORS ---
    c_pcb_green  = (0.25, 0.65, 0.35)  # Lighter, vivid green
    c_black      = (0.10, 0.10, 0.12)  # Chip bodies
    c_silver     = (0.85, 0.85, 0.90)  # Pins and solder pads
    c_text_white = (0.90, 0.90, 0.90)  # Silk screen text
    c_tan        = (0.75, 0.65, 0.50)  # SMD Capacitors
    c_trace_light= (0.40, 0.75, 0.50)  # Light green traces

    # --- DIMENSIONS ---
    w, d, h = 140.0 * S, 110.0 * S, 2.0 * S
    
    # 1. BASE BOARD
    board = make_box(doc, "PCB_Substrate", w, d, h, 0, 0, 0, c_pcb_green, offset)
    objects_to_group.append(board)

    # 2. CENTRAL QFP CHIP (The main feature)
    chip_size = 40.0 * S
    cx = (w - chip_size) / 2
    cy = (d - chip_size) / 2 + 10*S # Slightly offset upwards
    
    # Main Body
    objects_to_group.append(make_box(doc, "IC_Main_Body", chip_size, chip_size, 3*S, cx, cy, h, c_black, offset))
    
    # Orientation Circles (Dimples)
    objects_to_group.append(make_cylinder(doc, "Dimple_TL", 2*S, 0.5*S, cx+4*S, cy+chip_size-4*S, h+3*S, (0.2,0.2,0.2), offset))
    objects_to_group.append(make_cylinder(doc, "Dimple_BL", 2*S, 0.5*S, cx+4*S, cy+4*S, h+3*S, (0.2,0.2,0.2), offset))
    objects_to_group.append(make_cylinder(doc, "Dimple_TR", 2*S, 0.5*S, cx+chip_size-4*S, cy+chip_size-4*S, h+3*S, (0.2,0.2,0.2), offset))

    # Dense Pin Arrays (4 Sides)
    pin_len = 2.5 * S
    pin_w = 0.6 * S
    pin_gap = 1.0 * S # Dense spacing
    num_pins = int(chip_size / pin_gap)
    
    for i in range(num_pins):
        pos = i * pin_gap
        # Top
        objects_to_group.append(make_box(doc, f"Pin_T_{i}", pin_w, pin_len, 1*S, cx+pos, cy+chip_size, h, c_silver, offset))
        # Bottom
        objects_to_group.append(make_box(doc, f"Pin_B_{i}", pin_w, pin_len, 1*S, cx+pos, cy-pin_len, h, c_silver, offset))
        # Left
        objects_to_group.append(make_box(doc, f"Pin_L_{i}", pin_len, pin_w, 1*S, cx-pin_len, cy+pos, h, c_silver, offset))
        # Right
        objects_to_group.append(make_box(doc, f"Pin_R_{i}", pin_len, pin_w, 1*S, cx+chip_size, cy+pos, h, c_silver, offset))

    # 3. RIGHT SIDE DIODES/POWER COMPONENTS
    # Three distinct black rectangles with silver tabs on the right
    diode_w, diode_h = 12*S, 8*S
    diode_x = w - 25*S
    diode_start_y = 30*S
    
    for i in range(3):
        dy = diode_start_y + (i * 20 * S)
        # Black Body
        objects_to_group.append(make_box(doc, f"Diode_Body_{i}", diode_w, diode_h, 3*S, diode_x, dy, h, c_black, offset))
        # Silver Tab (Left)
        objects_to_group.append(make_box(doc, f"Diode_Tab_{i}", 3*S, diode_h, 1*S, diode_x-3*S, dy, h, c_silver, offset))
        # Silver Contacts (Right - two small ones)
        objects_to_group.append(make_box(doc, f"Diode_Con1_{i}", 2*S, 2*S, 1*S, diode_x+diode_w, dy+1*S, h, c_silver, offset))
        objects_to_group.append(make_box(doc, f"Diode_Con2_{i}", 2*S, 2*S, 1*S, diode_x+diode_w, dy+5*S, h, c_silver, offset))
        # Nearby Capacitor
        objects_to_group.append(make_box(doc, f"Diode_Cap_{i}", 4*S, 6*S, 2*S, diode_x-10*S, dy+1*S, h, c_tan, offset))

    # 4. LEFT SIDE RESISTOR COLUMN
    # Vertical column of small components on the far left
    res_x = 10 * S
    for i in range(5):
        ry = 40*S + (i * 12 * S)
        # Resistor Body
        objects_to_group.append(make_box(doc, f"Res_Left_{i}", 5*S, 3*S, 1*S, res_x, ry, h, c_black, offset))
        objects_to_group.append(make_box(doc, f"Res_L_Pad_{i}", 1*S, 3*S, 1*S, res_x-1*S, ry, h, c_silver, offset))
        objects_to_group.append(make_box(doc, f"Res_R_Pad_{i}", 1*S, 3*S, 1*S, res_x+5*S, ry, h, c_silver, offset))
        
        # Text simulation (White box next to it)
        objects_to_group.append(make_box(doc, f"Silk_Text_{i}", 1*S, 8*S, 0.1*S, res_x+8*S, ry-2*S, h, c_text_white, offset))

    # 5. BOTTOM CONNECTOR PADS
    # The grid of through-holes at the bottom
    pad_y = 5 * S
    for i in range(10):
        px = 20*S + (i * 10 * S)
        # Silver ring
        objects_to_group.append(make_cylinder(doc, f"Via_Ring_{i}", 3*S, 0.5*S, px, pad_y, h, c_silver, offset))
        # Dark hole
        objects_to_group.append(make_cylinder(doc, f"Via_Hole_{i}", 1.5*S, 0.6*S, px, pad_y, h, c_black, offset))
        # Trace line going up
        objects_to_group.append(make_box(doc, f"Trace_Up_{i}", 1*S, 15*S, 0.1*S, px-0.5*S, pad_y, h, c_trace_light, offset))

    # 6. TOP EDGE COMPONENTS
    top_y = d - 15*S
    for i in range(4):
        tx = 30*S + (i * 20 * S)
        objects_to_group.append(make_box(doc, f"Top_Comp_{i}", 8*S, 5*S, 2*S, tx, top_y, h, c_tan, offset))
        objects_to_group.append(make_box(doc, f"Top_Comp_PadL_{i}", 2*S, 5*S, 1*S, tx-2*S, top_y, h, c_silver, offset))
        objects_to_group.append(make_box(doc, f"Top_Comp_PadR_{i}", 2*S, 5*S, 1*S, tx+8*S, top_y, h, c_silver, offset))

    # 7. TRACE PATTERNS (Visual noise)
    # Adding thin lighter green lines to simulate the busy copper layer
    for i in range(20):
        # Random horizontal traces
        tx = random.uniform(10*S, 100*S)
        ty = random.uniform(10*S, 100*S)
        tl = random.uniform(5*S, 20*S)
        objects_to_group.append(make_box(doc, f"Deco_Trace_H_{i}", tl, 0.5*S, 0.1*S, tx, ty, h, c_trace_light, offset))
        
        # Random vertical traces
        vx = random.uniform(10*S, 100*S)
        vy = random.uniform(10*S, 100*S)
        vl = random.uniform(5*S, 20*S)
        objects_to_group.append(make_box(doc, f"Deco_Trace_V_{i}", 0.5*S, vl, 0.1*S, vx, vy, h, c_trace_light, offset))

    # 4. GROUPING
    group = doc.addObject("App::DocumentObjectGroup", "Central_Chip_PCB_Assembly")
    group.Group = objects_to_group
    
    print(f"Central Chip PCB generated at {offset} with colors retained.")


# ==============================================================================
# MAIN DRAWING FUNCTION: GREEN PCB (COLORED ASSEMBLY)
# ==============================================================================

def build_green_pcb_colored(doc, offset=(0,0,0), scale_factor=1.0):
    """
    Draws the complex green PCB. Uses a Group to retain individual colors.
    """
    
    S = scale_factor
    objects_to_group = []

    # --- COLORS (Based on the image) ---
    c_green_pcb  = (0.00, 0.40, 0.20)  # Deep Green Board
    c_copper     = (0.70, 0.50, 0.20)  # Dull Gold/Copper Traces
    c_solder     = (0.85, 0.85, 0.85)  # Silver/Solder
    c_black      = (0.10, 0.10, 0.10)  # ICs and Resistors
    c_blue_cap   = (0.10, 0.40, 0.80)  # The bright blue box capacitors
    c_coil_wire  = (0.85, 0.55, 0.30)  # Bright copper wire
    c_white      = (0.95, 0.95, 0.95)  # Silk screen
    c_elec_blue  = (0.10, 0.10, 0.40)  # Dark blue radial capacitor

    # --- DIMENSIONS ---
    w, d, h = 160.0 * S, 120.0 * S, 2.0 * S
    trace_z = 0.2 * S

    # 1. BASE BOARD
    board = make_box(doc, "PCB_Base", w, d, h, 0, 0, 0, c_green_pcb, offset)
    objects_to_group.append(board)

    # 2. COPPER TRACES (The complex pathing)
    # Helper to draw traces easily
    def add_trace(name, x, y, width, length, is_vert):
        if is_vert:
            t = make_box(doc, name, width, length, trace_z, x, y, h, c_copper, offset)
        else:
            t = make_box(doc, name, length, width, trace_z, x, y, h, c_copper, offset)
        objects_to_group.append(t)

    # Left heavy trace (zig-zag)
    add_trace("Trace_L_1", 20*S, 10*S, 4*S, 40*S, True)
    add_trace("Trace_L_2", 20*S, 50*S, 10*S, 4*S, False)
    add_trace("Trace_L_3", 30*S, 50*S, 4*S, 40*S, True)
    
    # Center massive bus
    add_trace("Trace_C_1", 50*S, 20*S, 8*S, 80*S, True)
    add_trace("Trace_C_2", 50*S, 100*S, 20*S, 8*S, False) # Top connector
    
    # Right side network
    add_trace("Trace_R_1", 100*S, 80*S, 40*S, 3*S, False)
    add_trace("Trace_R_2", 120*S, 60*S, 3*S, 20*S, True)
    
    # The distinct Y-shape junction (Top Right)
    add_trace("Trace_Y_Stem", 130*S, 90*S, 3*S, 15*S, True)
    # Angled bits approximated with small boxes
    objects_to_group.append(make_box(doc, "Trace_Y_L", 10*S, 3*S, trace_z, 120*S, 105*S, h, c_copper, offset))
    objects_to_group.append(make_box(doc, "Trace_Y_R", 10*S, 3*S, trace_z, 140*S, 105*S, h, c_copper, offset))

    # 3. COMPONENTS

    # -- Top Left: Black IC --
    ic_x, ic_y = 10*S, 90*S
    objects_to_group.append(make_box(doc, "IC_Black_TL", 25*S, 25*S, 4*S, ic_x, ic_y, h, c_black, offset))
    # Pins
    for i in range(6):
        py = ic_y + (i * 4 * S)
        objects_to_group.append(make_box(doc, f"Pin_L_{i}", 2*S, 1*S, 1*S, ic_x-2*S, py, h, c_solder, offset))

    # -- Top Right: Blue Box Capacitors --
    cap_x, cap_y = 80*S, 105*S
    objects_to_group.append(make_box(doc, "Cap_Blue_1", 20*S, 8*S, 10*S, cap_x, cap_y, h, c_blue_cap, offset))
    objects_to_group.append(make_box(doc, "Cap_Blue_2", 20*S, 8*S, 10*S, cap_x + 25*S, cap_y, h, c_blue_cap, offset))

    # -- Bottom Right: Copper Coil (Inductor) --
    coil_x, coil_y = 120*S, 20*S
    # Core
    objects_to_group.append(make_box(doc, "Coil_Core", 20*S, 15*S, 15*S, coil_x, coil_y, h, c_black, offset))
    # Windings (Cylinders)
    for i in range(6):
        wx = coil_x + (i * 3.2 * S) + 1*S
        wc = make_cylinder(doc, f"Winding_{i}", 15.5*S, 2*S, wx, coil_y + 7.5*S, h + 7.5*S, c_coil_wire, offset, axis=App.Vector(1,0,0))
        objects_to_group.append(wc)

    # -- Bottom Right: Electrolytic Capacitor (Blue Cylinder) --
    elec_x, elec_y = 100*S, 25*S
    objects_to_group.append(make_cylinder(doc, "Elec_Cap_Body", 6*S, 15*S, elec_x, elec_y, h, c_elec_blue, offset))
    objects_to_group.append(make_cylinder(doc, "Elec_Cap_Top", 6*S, 0.5*S, elec_x, elec_y, h+15*S, c_solder, offset))

    # -- Small SMDs (Resistors/Caps) scattered --
    # Creating a cluster near the bottom left
    for i in range(4):
        for j in range(3):
            sx = 20*S + (i * 5 * S)
            sy = 20*S + (j * 8 * S)
            # Black body
            objects_to_group.append(make_box(doc, f"SMD_{i}_{j}", 2*S, 4*S, 1.5*S, sx, sy, h, c_black, offset))
            # Silver ends
            objects_to_group.append(make_box(doc, f"SMD_End1_{i}_{j}", 2*S, 0.5*S, 1.5*S, sx, sy, h, c_solder, offset))
            objects_to_group.append(make_box(doc, f"SMD_End2_{i}_{j}", 2*S, 0.5*S, 1.5*S, sx, sy+3.5*S, h, c_solder, offset))

    # -- Solder Pads / Vias (Gold circles) --
    # Right side grid
    for i in range(3):
        for j in range(3):
            px = 140*S + (i * 5 * S)
            py = 60*S + (j * 5 * S)
            pad = make_cylinder(doc, f"Pad_Gold_{i}_{j}", 1.5*S, 0.5*S, px, py, h, c_copper, offset)
            objects_to_group.append(pad)

    # 4. GROUPING
    # This preserves the color of every object while keeping the tree clean.
    group = doc.addObject("App::DocumentObjectGroup", "Green_PCB_Assembly")
    group.Group = objects_to_group
    
    print(f"Green PCB generated at {offset} with colors retained.")


# ==============================================================================
# MAIN DRAWING FUNCTION: RAYTHEON CIRCUIT BOARD (FUSED)
# ==============================================================================

def build_raytheon_pcb(doc, offset=(0, 0, 0), scale_factor=1.0):
    """
    Draws the Raytheon Circuit Board based on the provided image.
    collects all parts and fuses them into one object.
    """

    # --- SCALE FACTOR ---
    S = scale_factor

    # List to hold temporary objects for fusion
    temp_objects = []

    # --- COLORS ---
    col_pcb_brown = (0.35, 0.15, 0.10)  # The dark brownish/red substrate
    col_ceramic = (0.90, 0.90, 0.85)   # White/Beige ceramic chip body
    col_gold_lid = (0.85, 0.70, 0.20)  # The bright Raytheon gold lids
    col_silver = (0.75, 0.75, 0.80)    # Pins and solder pads
    col_smd_tan = (0.70, 0.50, 0.30)   # Capacitor color
    col_smd_black = (0.10, 0.10, 0.10) # Resistor/IC color

    # --- DIMENSIONS (SCALED) ---
    board_w = 140.0 * S
    board_h = 110.0 * S
    board_thick = 2.0 * S

    # 1. PCB SUBSTRATE
    temp_objects.append(make_box(doc, "PCB_Substrate", board_w, board_h, board_thick,
                                 0, 0, 0, col_pcb_brown, offset))

    # 2. LARGE RAYTHEON CHIPS (Gold Lidded QFPs)
    def draw_gold_chip(chip_name, cx, cy, cw, ch):
        z_surf = board_thick

        # Ceramic Body
        temp_objects.append(make_box(doc, f"{chip_name}_Body", cw, ch, 3.0 * S,
                                     cx, cy, z_surf, col_ceramic, offset))

        # Gold Lid
        lid_margin = 2.0 * S
        temp_objects.append(make_box(doc, f"{chip_name}_Lid", cw - (2 * lid_margin), ch - (2 * lid_margin), 0.5 * S,
                                     cx + lid_margin, cy + lid_margin, z_surf + 3.0 * S, col_gold_lid, offset))

        # Pins
        pin_len = 2.0 * S
        pin_h = 1.0 * S

        temp_objects.append(make_box(doc, f"{chip_name}_Pins_L", pin_len, ch - 4 * S, pin_h,
                                     cx - pin_len, cy + 2 * S, z_surf, col_silver, offset))

        temp_objects.append(make_box(doc, f"{chip_name}_Pins_R", pin_len, ch - 4 * S, pin_h,
                                     cx + cw, cy + 2 * S, z_surf, col_silver, offset))

        temp_objects.append(make_box(doc, f"{chip_name}_Pins_T", cw - 4 * S, pin_len, pin_h,
                                     cx + 2 * S, cy + ch, z_surf, col_silver, offset))

        temp_objects.append(make_box(doc, f"{chip_name}_Pins_B", cw - 4 * S, pin_len, pin_h,
                                     cx + 2 * S, cy - pin_len, z_surf, col_silver, offset))

    # Place Left Chip
    draw_gold_chip("Chip_Raytheon_L", 20 * S, 40 * S, 35 * S, 35 * S)

    # Place Right Chip
    draw_gold_chip("Chip_Raytheon_R", 85 * S, 40 * S, 35 * S, 35 * S)

    # 3. BOTTOM HYBRID CHIP
    bx, by, bw, bh = 50 * S, 10 * S, 25 * S, 18 * S
    draw_gold_chip("Chip_Hybrid_Bot", bx, by, bw, bh)

    # 4. SMD COMPONENTS
    def draw_smd_row(row_name, start_x, start_y, count, spacing, is_vertical=False):
        smd_l = 3.0 * S
        smd_w = 1.5 * S
        smd_h = 1.5 * S

        for i in range(count):
            if is_vertical:
                px = start_x
                py = start_y + (i * spacing)

                temp_objects.append(make_box(doc, f"{row_name}_{i}_Body", smd_w, smd_l, smd_h,
                                             px, py, board_thick, col_smd_tan, offset))

                temp_objects.append(make_box(doc, f"{row_name}_{i}_Cap1", smd_w, 0.5 * S, smd_h,
                                             px, py, board_thick, col_silver, offset))

                temp_objects.append(make_box(doc, f"{row_name}_{i}_Cap2", smd_w, 0.5 * S, smd_h,
                                             px, py + smd_l - 0.5 * S, board_thick, col_silver, offset))
            else:
                px = start_x + (i * spacing)
                py = start_y

                temp_objects.append(make_box(doc, f"{row_name}_{i}_Body", smd_l, smd_w, smd_h,
                                             px, py, board_thick, col_smd_tan, offset))

                temp_objects.append(make_box(doc, f"{row_name}_{i}_Cap1", 0.5 * S, smd_w, smd_h,
                                             px, py, board_thick, col_silver, offset))

                temp_objects.append(make_box(doc, f"{row_name}_{i}_Cap2", 0.5 * S, smd_w, smd_h,
                                             px + smd_l - 0.5 * S, py, board_thick, col_silver, offset))

    # Top Edge Row
    draw_smd_row("SMD_Top", 10 * S, 95 * S, 15, 8 * S, is_vertical=False)

    # Between Chips
    draw_smd_row("SMD_Mid_Col1", 65 * S, 45 * S, 5, 6 * S, is_vertical=True)
    draw_smd_row("SMD_Mid_Col2", 75 * S, 45 * S, 5, 6 * S, is_vertical=True)

    # Right Side Grid
    for r in range(4):
        draw_smd_row(f"SMD_Right_R{r}", 125 * S, 10 * S + (r * 20 * S), 3, 5 * S, is_vertical=True)

    # Bottom Left Cluster
    draw_smd_row("SMD_BotLeft", 10 * S, 10 * S, 4, 8 * S, is_vertical=False)
    draw_smd_row("SMD_BotLeft2", 10 * S, 20 * S, 4, 8 * S, is_vertical=False)

    # 5. SMALL ICs (Black Chips)
    soic_locs = [(15 * S, 80 * S), (80 * S, 85 * S), (110 * S, 5 * S)]
    for i, (lx, ly) in enumerate(soic_locs):
        temp_objects.append(make_box(doc, f"SOIC_{i}", 8 * S, 5 * S, 2 * S,
                                     lx, ly, board_thick, col_smd_black, offset))

        for p in range(4):
            temp_objects.append(make_box(doc, f"SOIC_{i}_LegT_{p}", 1 * S, 1 * S, 1 * S,
                                         lx + (p * 2 * S), ly + 5 * S, board_thick, col_silver, offset))

            temp_objects.append(make_box(doc, f"SOIC_{i}_LegB_{p}", 1 * S, 1 * S, 1 * S,
                                         lx + (p * 2 * S), ly - 1 * S, board_thick, col_silver, offset))

    # --------------------------------------------------------------------------
    # FUSION LOGIC
    # --------------------------------------------------------------------------
    if temp_objects:
        shapes_to_fuse = [obj.Shape for obj in temp_objects]

        fused_shape = shapes_to_fuse[0]

        if len(shapes_to_fuse) > 1:
            fused_shape = reduce(lambda a, b: a.fuse(b), shapes_to_fuse[1:], fused_shape)

        for obj in temp_objects:
            doc.removeObject(obj.Name)

        final_obj = doc.addObject("Part::Feature", "Raytheon_Fused")
        final_obj.Shape = fused_shape

        final_obj.ViewObject.ShapeColor = col_pcb_brown

        print(f"Raytheon Board Fused Model generated at offset {offset} with scale {S}")
        return final_obj


# ==============================================================================
# MAIN DRAWING FUNCTION: GREEN PCB WITH SQUARE SHIELD (FUSED)
# ==============================================================================

def build_green_shield_pcb(doc, offset=(0, 0, 0), scale_factor=1.0):
    """
    Draws the Green PCB with the distinct square metal shield, capacitors,
    and connectors as seen in the reference image.
    Fuses all parts into a single object.
    """

    # --- SCALE FACTOR ---
    S = scale_factor

    # List to hold temporary objects for fusion
    temp_objects = []

    # --- COLORS ---
    col_pcb_green = (0.0, 0.6, 0.3)      # The main board color
    col_silver = (0.85, 0.85, 0.90)      # Shield and solder
    col_black = (0.1, 0.1, 0.1)          # Chips
    col_orange = (0.9, 0.5, 0.1)         # Caps
    col_white = (0.95, 0.95, 0.95)       # Connectors
    col_purple = (0.3, 0.1, 0.6)         # Large Cap

    # --- DIMENSIONS (SCALED) ---
    board_w = 100.0 * S
    board_h = 100.0 * S
    board_thick = 2.0 * S

    # 1. PCB SUBSTRATE
    temp_objects.append(
        make_box(doc, "ShieldPCB_Base", board_w, board_h, board_thick,
                 0, 0, 0, col_pcb_green, offset)
    )

    # 2. THE SQUARE METAL SHIELD (Bottom Left Quadrant)
    # Formed by 4 walls
    shield_x, shield_y = 15 * S, 15 * S
    shield_size = 40 * S
    wall_thick = 2 * S
    wall_h = 3 * S

    # Left Wall
    temp_objects.append(
        make_box(doc, "Shield_L", wall_thick, shield_size, wall_h,
                 shield_x, shield_y, board_thick, col_silver, offset)
    )

    # Right Wall
    temp_objects.append(
        make_box(doc, "Shield_R", wall_thick, shield_size, wall_h,
                 shield_x + shield_size - wall_thick, shield_y, board_thick, col_silver, offset)
    )

    # Bottom Wall
    temp_objects.append(
        make_box(doc, "Shield_B", shield_size - 2 * wall_thick, wall_thick, wall_h,
                 shield_x + wall_thick, shield_y, board_thick, col_silver, offset)
    )

    # Top Wall
    temp_objects.append(
        make_box(doc, "Shield_T", shield_size - 2 * wall_thick, wall_thick, wall_h,
                 shield_x + wall_thick, shield_y + shield_size - wall_thick,
                 board_thick, col_silver, offset)
    )

    # Chip inside the shield
    temp_objects.append(
        make_box(doc, "Shield_IC", 10 * S, 10 * S, 1.5 * S,
                 shield_x + 15 * S, shield_y + 15 * S, board_thick, col_black, offset)
    )

    # 3. CAPACITORS (Orange ones on left, Purple on right)

    # Three Orange Caps (Top Left area)
    cap_locs = [(15 * S, 70 * S), (25 * S, 60 * S), (10 * S, 55 * S)]
    for i, (cx, cy) in enumerate(cap_locs):
        temp_objects.append(
            make_cylinder(doc, f"Cap_Orange_{i}", 4 * S, 10 * S,
                          cx, cy, board_thick, col_orange, offset)
        )

    # One Large Purple Cap (Top Right)
    temp_objects.append(
        make_cylinder(doc, "Cap_Purple", 8 * S, 15 * S,
                      80 * S, 85 * S, board_thick, col_purple, offset)
    )

    # 4. WHITE CONNECTORS
    # Top Edge (3-pin JST style)
    temp_objects.append(
        make_box(doc, "Conn_Top", 15 * S, 6 * S, 8 * S,
                 40 * S, 90 * S, board_thick, col_white, offset)
    )

    # Bottom Edge (2-pin JST style)
    temp_objects.append(
        make_box(doc, "Conn_Bot", 12 * S, 6 * S, 8 * S,
                 30 * S, 5 * S, board_thick, col_white, offset)
    )

    # 5. INTEGRATED CIRCUITS (Black Chips)

    # Central QFP Chip
    temp_objects.append(
        make_box(doc, "IC_Central", 14 * S, 14 * S, 2.5 * S,
                 60 * S, 45 * S, board_thick, col_black, offset)
    )

    # Voltage Regulator (Right side, TO-220 style)
    temp_objects.append(
        make_box(doc, "Regulator_Body", 10 * S, 5 * S, 4 * S,
                 85 * S, 50 * S, board_thick, col_black, offset)
    )

    # Metal Tab for regulator
    temp_objects.append(
        make_box(doc, "Regulator_Tab", 10 * S, 5 * S, 1 * S,
                 85 * S, 50 * S, board_thick, col_silver, offset)
    )

    # 6. HEADER PINS (Bottom Right)
    # 2x4 Pin Header
    header_x, header_y = 60 * S, 15 * S
    for r in range(2):
        for c in range(4):
            px = header_x + (c * 3 * S)
            py = header_y + (r * 3 * S)

            # Black base
            temp_objects.append(
                make_box(doc, f"HeaderBase_{r}_{c}", 2.5 * S, 2.5 * S, 2 * S,
                         px, py, board_thick, col_black, offset)
            )

            # Silver pin
            temp_objects.append(
                make_box(doc, f"HeaderPin_{r}_{c}", 1 * S, 1 * S, 8 * S,
                         px + 0.75 * S, py + 0.75 * S, board_thick, col_silver, offset)
            )

    # 7. HEAT SINK (Top Center - Aluminum fins)
    temp_objects.append(
        make_box(doc, "Heatsink_Base", 20 * S, 5 * S, 10 * S,
                 35 * S, 80 * S, board_thick, col_silver, offset)
    )

    for i in range(4):
        fin_x = 35 * S + (i * 5 * S)
        temp_objects.append(
            make_box(doc, f"Heatsink_Fin_{i}", 1 * S, 5 * S, 12 * S,
                     fin_x, 80 * S, board_thick, col_silver, offset)
        )

    # --------------------------------------------------------------------------
    # FUSION LOGIC
    # --------------------------------------------------------------------------
    if temp_objects:
        shapes_to_fuse = [obj.Shape for obj in temp_objects]

        fused_shape = shapes_to_fuse[0]

        if len(shapes_to_fuse) > 1:
            fused_shape = reduce(lambda a, b: a.fuse(b), shapes_to_fuse[1:], fused_shape)

        # Cleanup temp objects (removes intermediate parts from tree)
        for obj in temp_objects:
            doc.removeObject(obj.Name)

        # Create final fused object
        final_obj = doc.addObject("Part::Feature", "Green_Shield_PCB")
        final_obj.Shape = fused_shape

        # Set the primary color (Green), though fused objects take one color
        final_obj.ViewObject.ShapeColor = col_pcb_green

        print(f"Green Shield PCB generated at {offset}")
        return final_obj


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
# MAIN DRAWING FUNCTION: GOLD SPHERE (NUGGET)
# ==============================================================================

def draw_gold_sphere(doc, name, offset_coords=(0, 0, 0), scale_factor=1.0):
    """
    Creates a glossy golden sphere representing a gold nugget or particle.
    Proportionally scales based on scale_factor.
    """
    S = scale_factor 
    
    # --- COLORS ---
    # Metallic Gold approximation (Red-Green mix with low Blue)
    c_gold = (0.85, 0.70, 0.10)

    # --- DIMENSIONS (SCALED) ---
    radius = 50.0 * S

    # 1. GENERATE GEOMETRY
    # Uses the make_sphere helper defined at the top of your script
    sphere_obj = make_sphere(
        doc, 
        name,      # Use the dynamic name passed from the loop
        radius, 
        0, 0, 0,   # Local center coordinates
        c_gold, 
        offset_coords
    )

    return sphere_obj


# ==============================================================================
# MAIN DRAWING FUNCTION: METAL POWDER PARTICLE (SEM STYLE)
# ==============================================================================

def draw_powder_particle(doc, name, offset_coords=(0, 0, 0), scale_factor=1.0):
    """
    Creates a matte grey sphere representing a metal powder particle 
    (as seen in SEM imagery).
    Proportionally scales based on scale_factor.
    """
    S = scale_factor 
    
    # --- COLORS ---
    # Matte Grey (Standard metal powder appearance)
    c_powder_grey = (0.65, 0.65, 0.65)

    # --- DIMENSIONS (SCALED) ---
    radius = 50.0 * S

    # 1. GENERATE GEOMETRY
    # Uses the make_sphere helper defined at the top of your script
    sphere_obj = make_sphere(
        doc, 
        name,      # Use the dynamic name passed from the loop
        radius, 
        0, 0, 0,   # Local center coordinates
        c_powder_grey, 
        offset_coords
    )

    return sphere_obj


def create_layout():
    doc = ensure_document()
    create_equipment(doc, (0, 0, 800))
    build_conveyor(doc, (4000.0, 200.0, 0.0))
    build_shredder(doc, (6500.0, -500.0, 0.0))
    # Pocket conveyor starts at 10000, 0, 1400. Length is 8000.
    # End of pocket conveyor is approx 17000.
    pocket_conveyor(doc, offset=(10000, -450, 750))
    #Build Crusher at specified coordinates (0, 0, 0)
    build_crusher(doc, offset=(18500, 300, 0))
    #Pocket conveyor
    pocket_conveyor(doc, offset=(24600, -150, 3500))
    pocket_conveyor(doc, offset=(63600, -150, 3500))
    #Buid Dust Collector
    build_dust_collector(doc, offset=(31000, 250, 0))
    #Build ESP
    build_esp(doc, offset=(31000, 6000, 0))
    # Defining the Numerical Offset Coordinates
    dec_offset_coords = (32000.0, 0.0, 0.0)
    # Build the system
    build_decline_conveyor(offset=dec_offset_coords)
    #Ball Mill
    mill_placement_coords = (39500.0, 300.0, 0.0)
    build_ball_mill(offset=mill_placement_coords)
    # 2. Create NORTH Conveyor shifted by X=2000
    create_north_facing_conveyor(doc, offset=(43000, 650, 0))
    # Coordinates format: (X, Y, Z)
    build_separator(doc, offset=(42000, 3500, 0))
    #Build ESP
    build_esp(doc, offset=(31000, 6000, 0))
    #Build Conveyor
    build_swan_neck_conveyor(doc, offset=(41000, 0, 0))
    # Coordinates format: (X, Y, Z)
    build_esp(doc, offset=(48000, 0, 0))
    # Coordinates format: (X, Y, Z)
    build_separator(doc, offset=(55000, 0, 0))
    #Build Conveyor
    build_swan_neck_conveyor(doc, offset=(49000, 0, 0))
    # Example: Build at origin (0, 0, 0)
    build_scrubber(doc, offset=(62000, 100, 0))
    #Build Conveyor
    build_swan_neck_conveyor(doc, offset=(56000, 0, 0))
    #Building centrifugal at specific numerical offset
    build_centrifugal_concentrator(doc, offset=(70000.0, 0.0, 0.0))
    #Connecting Pipe
    build_duct_connection(doc)
    # --- PCB GENERATION LOOP ---
    for i in range(10):
        # Calculate spacing: 400mm gap between each set along the Y-axis
        y_shift = i * 0.0 
        
        # 1. Vertical Component PCB
        build_vertical_component_pcb(doc, offset=(-100, y_shift, 510), scale_factor=1.35)
        
        # 2. Central Chip PCB
        build_central_chip_pcb(doc, offset=(-150, y_shift, 510), scale_factor=1.45)
        
        # 3. Green Colored PCB
        build_green_pcb_colored(doc, offset=(-250, y_shift, 510), scale_factor=1.75)
        
        # 4. Raytheon Fused PCB
        build_raytheon_pcb(doc, offset=(0, y_shift, 510), scale_factor=2.5)
        
        # 5. NEW: Green Shield Fused PCB (Added here)
        # Positioned at X = -350 to sit to the left of the others
        build_green_shield_pcb(doc, offset=(-350, y_shift, 510), scale_factor=1.5)

    # --- PARTICLE GENERATION LOOP ---
    for i in range(10):
        # 1. Ten Black Spheres (Waste)
        draw_black_sphere(doc, f"Black_Sphere_{i}", 
            offset_coords=(0 + (i * 200), 300 + random.uniform(-150, 150), 850), 
            scale_factor=random.uniform(0.8, 1.5))
            
        # 2. Ten Brown Spheres (Copper)
        draw_brown_sphere(doc, f"Brown_Sphere_{i}", 
            offset_coords=(1 + (i * 200), 400 + random.uniform(-150, 150), 850), 
            scale_factor=random.uniform(0.8, 1.5))
            
        # 3. Ten Silver Spheres (Steel)
        draw_silver_sphere(doc, f"Silver_Sphere_{i}", 
            offset_coords=(2 + (i * 200), 500 + random.uniform(-150, 150), 850), 
            scale_factor=random.uniform(0.8, 1.5))

        # 4. Ten Gold Spheres (Nuggets)
        draw_gold_sphere(doc, f"Gold_Sphere_{i}", 
            offset_coords=(3 + (i * 200), 600 + random.uniform(-150, 150), 850), 
            scale_factor=1.2)

        # 5. NEW: Ten Powder Particles (From your SEM image)
        # Positioned at Y=700 to separate them from the others
        draw_powder_particle(doc, f"Powder_Particle_{i}", 
            offset_coords=(4 + (i * 200), 700 + random.uniform(-150, 150), 850), 
            scale_factor=1.0)

    doc.recompute()
    try:
        Gui.SendMsgToActiveView("ViewFit")
        Gui.activeDocument().activeView().viewAxonometric()
    except:
        pass
    print("Combined assembly complete: Feeder -> Conveyor -> Shredder -> Screw -> Pyrolysis -> Pipe -> Tank-> Crusher->Hydrocyclone -> Pulse Duct Collector ->ESP -> Screener -> Conveyor -> DMS-> Conveyor -> Magnetic Separator-> Conveyor -> Mill -> Conveyor ->Screener-> Conveyor ->DMS")

import csv
import os
import math

def generate_and_save_mining_plant_report():
    """
    Analyzes the mining plant equipment dimensions from the FreeCAD script,
    calculates occupied areas, and saves a CSV report to the user's home directory.
    """
    
    # Equipment Data extracted from the provided script:
    # Format: (Name, Length_mm, Width_mm, Quantity)
    # Lengths and widths are based on the frame/base dimensions defined in the code.
    
    equipment_data = [
        ("Vibrating Feeder", 4000, 1200, 1),
        ("Standard Conveyor", 3000, 800, 1),
        ("Industrial Shredder", 4500, 1600, 1),
        ("Pocket Conveyor", 8000, 1000, 1),
        ("Mobile Crusher Unit", 3800, 2200, 1),
        ("Pocket Conveyor", 6000, 1000, 2),
        ("Pulse Dust Collector", 2400, 2200, 1),
        ("Electrostatic Precipitator (ESP)", 3000, 2000, 3), # Called 3 times in layout
        ("Decline Conveyor", 7050, 1000, 1), # Approx length: high + slope_proj + low
        ("Industrial Ball Mill", 5000, 2400, 1),
        ("Curved Conveyor (North)", 4000, 4000, 1), # Footprint of 90-deg sweep
        ("Magnetic Separator", 3500, 3200, 2), # Tank width + side box width
        ("Swan Neck (Z) Conveyor", 6600, 1000, 3), # Approx project length based on angles
        ("Rotary Scrubber", 5500, 1100, 1),
        ("Centrifugal Concentrator", 6500, 3300, 1) # Dual unit module
    ]

    # File Path (Saves to your user home folder)
    file_path = os.path.expanduser("~/mining_plant_equipment_list.csv")

    header = ["Equipment Name", "Quantity", "Length (m)", "Width (m)", "Footprint Area (m2)"]
    rows_to_save = []
    grand_total_area = 0.0

    # Process and convert mm to meters
    for name, length_mm, width_mm, qty in equipment_data:
        l_m = length_mm / 1000.0
        w_m = width_mm / 1000.0
        unit_area = l_m * w_m
        total_item_area = unit_area * qty
        grand_total_area += total_item_area
        rows_to_save.append([name, qty, f"{l_m:.2f}", f"{w_m:.2f}", f"{total_item_area:.2f}"])

    # 1. SAVE TO CSV
    try:
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(rows_to_save)
            writer.writerow([]) 
            writer.writerow(["GRAND TOTAL OCCUPIED AREA", "", "", "", f"{grand_total_area:.2f}"])
        print(f"\n✅ Equipment report successfully stored at: {file_path}")
    except Exception as e:
        print(f"❌ Error saving CSV: {e}")

    # 2. PRINT SUMMARY TO CONSOLE
    print("\n" + "="*85)
    print(f"{'MINING PLANT EQUIPMENT LIST':^85}")
    print("="*85)
    print(f"{'Equipment Name':<35} | {'Qty':<4} | {'L (m)':<7} | {'W (m)':<7} | {'Area (m2)':<10}")
    print("-" * 85)
    for row in rows_to_save:
        print(f"{row[0]:<35} | {row[1]:<4} | {row[2]:<7} | {row[3]:<7} | {row[4]:<10}")
    print("-" * 85)
    print(f"{'TOTAL FOOTPRINT AREA:':<57} {grand_total_area:>10.2f} m2")
    print("="*85)

if __name__ == "__main__":
    create_layout()
    generate_and_save_mining_plant_report()