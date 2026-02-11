inkling "2.0"

type SimState {
    cart_position: number,
    cart_velocity: number,
    pole_angle: number,
    pole_velocity: number
}

type SimAction {
    command: number<Left = -1, Right = 1>
}

type SimConfig {
    episode_length: number
}

graph (input: SimState): SimAction {
    concept balance(input): SimAction {
        curriculum {
            source simulator (action: SimAction, config: SimConfig): SimState {
            }
        }
    }
    output balance
}
