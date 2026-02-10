# ADRIFT Hello World Task

Task: greet
    Command: say hello
    Restrictions:
        - Must be: Location = "Starting Room"
    Actions:
        - Display message: "Hello, World! Welcome to ADRIFT interactive fiction."
        - Increase score by 10

Task: look_around
    Command: look
    Actions:
        - Display message: "You are in a simple room. There's nothing special here, but you can try saying hello."

Location: Starting Room
    Description: "A simple starting location for your adventure."
    Short Description: "Starting Room"