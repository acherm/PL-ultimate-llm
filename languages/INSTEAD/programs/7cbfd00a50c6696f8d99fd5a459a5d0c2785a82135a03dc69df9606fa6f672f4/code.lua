-- main.lua
-- "The Lighthouse" - A simple INSTEAD interactive fiction game

room {
    nam = 'main',
    title = 'Lighthouse Base',
    dsc = [[You stand at the base of a weathered lighthouse. Waves crash against
the rocks below. A rusted {iron ladder} leads up to the lamp room.
A worn {logbook} lies open on a barrel.]],
    obj = { 'ladder', 'logbook' },
}

room {
    nam = 'lamp_room',
    title = 'Lamp Room',
    dsc = [[The cramped lamp room smells of old oil. The great {Fresnel lens}
sits cold and dark. Through salt-stained glass you see only storm clouds.
The ladder leads back {down}.]],
    obj = { 'lens', 'ladder_down' },
}

obj {
    nam = 'ladder',
    disp = 'iron ladder',
    dsc = [[A rusted but sturdy iron ladder bolted to the lighthouse wall.]],
    act = function(s)
        p [[You climb the ladder up to the lamp room.]]
        walk('lamp_room')
    end,
    tak = false,
}

obj {
    nam = 'ladder_down',
    disp = 'down',
    dsc = [[The ladder leads back down to the base.]],
    act = function(s)
        p [[You descend the ladder.]]
        walk('main')
    end,
    tak = false,
}

obj {
    nam = 'logbook',
    disp = 'logbook',
    dsc = [[A weathered logbook, its pages yellowed and brittle.]],
    act = function(s)
        p [[You read the last entry: "Storm approaching from the northwest.]]
        p [[Fuel reserves critically low. The light must not go out. -- E.H."]],
    end,
    tak = function(s)
        p [[You tuck the logbook under your arm.]]
        return true
    end,
}

obj {
    nam = 'lens',
    disp = 'Fresnel lens',
    dsc = [[The magnificent Fresnel lens, designed to amplify a small flame
into a beam visible for miles. It is dusty from long disuse.]],
    act = function(s)
        p [[You run a hand along the cool glass. With fuel and a flame,]]
        p [[this lens could warn ships away from the rocks.]],
    end,
    tak = false,
}
