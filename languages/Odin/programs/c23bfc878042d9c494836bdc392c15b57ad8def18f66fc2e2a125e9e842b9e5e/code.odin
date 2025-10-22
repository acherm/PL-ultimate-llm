package snake

import "core:fmt"
import "core:math/rand"
import "vendor:sdl2"

WINDOW_WIDTH :: 800
WINDOW_HEIGHT :: 600
TILE_SIZE :: 20

Direction :: enum {
    UP,
    DOWN,
    LEFT,
    RIGHT,
}

Snake :: struct {
    x, y: i32,
    dx, dy: i32,
    direction: Direction,
    length: i32,
    tail_x: [100]i32,
    tail_y: [100]i32,
}

main :: proc() {
    sdl2.Init(sdl2.INIT_VIDEO)
    window := sdl2.CreateWindow("Snake", sdl2.WINDOWPOS_CENTERED, sdl2.WINDOWPOS_CENTERED, WINDOW_WIDTH, WINDOW_HEIGHT, sdl2.WINDOW_SHOWN)
    renderer := sdl2.CreateRenderer(window, -1, sdl2.RENDERER_ACCELERATED)

    snake := Snake{
        x = WINDOW_WIDTH/2,
        y = WINDOW_HEIGHT/2,
        dx = TILE_SIZE,
        dy = 0,
        direction = .RIGHT,
        length = 1,
    }

    food_x := rand.int31_max(WINDOW_WIDTH/TILE_SIZE) * TILE_SIZE
    food_y := rand.int31_max(WINDOW_HEIGHT/TILE_SIZE) * TILE_SIZE

    game_over := false
    for !game_over {
        event: sdl2.Event
        for sdl2.PollEvent(&event) {
            #partial switch event.type {
            case .QUIT:
                game_over = true
            case .KEYDOWN:
                #partial switch event.key.keysym.sym {
                case .UP:
                    if snake.direction != .DOWN {
                        snake.direction = .UP
                        snake.dx = 0
                        snake.dy = -TILE_SIZE
                    }
                }
            }
        }
    }
}