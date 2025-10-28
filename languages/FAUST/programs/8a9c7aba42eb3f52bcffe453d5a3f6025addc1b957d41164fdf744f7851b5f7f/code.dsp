import("stdfaust.lib");
freq = hslider("freq", 1000, 50, 2000, 0.01);
process = os.oscsin(freq);