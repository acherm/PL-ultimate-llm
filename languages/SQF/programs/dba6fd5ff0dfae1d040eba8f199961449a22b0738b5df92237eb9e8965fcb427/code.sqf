// Spawn a group of AI units and set them on a patrol
private _grp = createGroup [east, true];

// Create 4 units in the group at a specified position
private _spawnPos = [2000, 2000, 0];
for "_i" from 1 to 4 do {
    private _unit = _grp createUnit ["O_Soldier_F", _spawnPos, [], 5, "FORM"];
    _unit setSkill 0.6;
};

// Define waypoints for patrol route
private _waypoints = [
    [2000, 2200, 0],
    [2200, 2200, 0],
    [2200, 2000, 0],
    [2000, 2000, 0]
];

// Add waypoints to the group
{
    private _wp = _grp addWaypoint [_x, 50];
    _wp setWaypointType "MOVE";
    _wp setWaypointSpeed "LIMITED";
    _wp setWaypointBehaviour "SAFE";
    _wp setWaypointFormation "STAG COLUMN";
} forEach _waypoints;

// Set the last waypoint to cycle back to the first
private _wpCycle = _grp addWaypoint [_waypoints select 0, 50];
_wpCycle setWaypointType "CYCLE";

// Log the patrol setup
systemChat format ["Patrol group %1 created with %2 units", _grp, count units _grp];
