# Praat script to get pitch statistics
# This script reads a sound file and extracts pitch information

sound = Read from file: "input.wav"
selectObject: sound

# Create a pitch object
pitch = To Pitch: 0.0, 75, 500
selectObject: pitch

# Get pitch statistics
mean_pitch = Get mean: 0, 0, "Hertz"
min_pitch = Get minimum: 0, 0, "Hertz", "Parabolic"
max_pitch = Get maximum: 0, 0, "Hertz", "Parabolic"

# Print results
writeInfoLine: "Pitch Statistics:"
appendInfoLine: "Mean pitch: ", fixed$(mean_pitch, 2), " Hz"
appendInfoLine: "Minimum pitch: ", fixed$(min_pitch, 2), " Hz"
appendInfoLine: "Maximum pitch: ", fixed$(max_pitch, 2), " Hz"

# Clean up
removeObject: sound, pitch
