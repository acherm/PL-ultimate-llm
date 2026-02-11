// Parametric Involute Bevel and Spur Gears by GregFrost
// It is licensed under the Creative Commons - GNU LGPL 2.1 license.
// © 2010 by GregFrost, thingiverse.com/Amp
// http://www.thingiverse.com/thing:3575

// Simple Test:
test_bevel_gears();

module test_bevel_gears()
{
    bevel_gear_pair (gear1_teeth=41,
    gear2_teeth=7,
    axis_angle=90,
    outside_circular_pitch=460);
}

module bevel_gear_pair (gear1_teeth = 41,
    gear2_teeth = 7,
    axis_angle = 90,
    outside_circular_pitch=1000)
{
    outside_pitch_radius1 = gear1_teeth * outside_circular_pitch / 360;
    outside_pitch_radius2 = gear2_teeth * outside_circular_pitch / 360;
    pitch_apex1=outside_pitch_radius2 * sin(axis_angle)
        + (outside_pitch_radius2 * cos(axis_angle) + outside_pitch_radius1) / tan(axis_angle);
    cone_distance = sqrt(pow(pitch_apex1, 2) + pow(outside_pitch_radius1, 2));
    pitch_apex2 = sqrt(pow(cone_distance, 2) - pow(outside_pitch_radius2, 2));
    echo("cone_distance", cone_distance);
    pitch_angle1 = asin(outside_pitch_radius1 / cone_distance);
    pitch_angle2 = asin(outside_pitch_radius2 / cone_distance);
    echo("pitch_angle1, pitch_angle2", pitch_angle1, pitch_angle2);
    rotate([0,0,90])
    translate([0,0,pitch_apex1])
    rotate([-pitch_angle1,0,0])
    bevel_gear (number_of_teeth=gear1_teeth,
        cone_distance=cone_distance,
        face_width=10,
        outside_circular_pitch=outside_circular_pitch,
        pressure_angle=30,
        clearance = 0.2,
        bore_diameter=5);
}