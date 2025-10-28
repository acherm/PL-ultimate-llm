// Feather disable all

/// @function                scr_state_machine()
/// @description             A simple state machine.
/// @returns {Struct}
function scr_state_machine() constructor {
    
    // The current state
    state = noone;
    
    // The previous state
    previous_state = noone;
    
    /// @function                step()
    /// @description             Steps the state machine.
    static step = function() {
        if (is_struct(state)) {
            if (variable_struct_exists(state, "step")) {
                state.step();
            }
        }
    }
    
    /// @function                set_state(_state)
    /// @description             Changes the state of the state machine.
    /// @param {Struct} _state   The state to change to.
    static set_state = function(_state) {
        if (state != _state) {
            previous_state = state;
            state = _state;
            
            if (is_struct(previous_state)) {
                if (variable_struct_exists(previous_state, "on_exit")) {
                    previous_state.on_exit();
                }
            }
            
            if (is_struct(state)) {
                if (variable_struct_exists(state, "on_enter")) {
                    state.on_enter();
                }
            }
        }
    }
}