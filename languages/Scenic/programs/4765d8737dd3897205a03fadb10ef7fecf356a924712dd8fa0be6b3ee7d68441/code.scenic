# Scenic scenario: basic object placement and constraint example
# Demonstrates core Scenic language features for scenario generation

model scenic.models.basic

# Define the ego object (the primary agent) at the origin
ego = Object with width 4, with height 2, at 0 @ 0

# Place another object at a random position in front
other = Object with width 2, with height 2,
        at Range(5, 10) @ Range(-2, 2),
        facing toward ego

# Require a minimum separation distance between the objects
require (distance from other to ego) > 3
