Red [
    Title: "Game of Life"
    Author: "Nenad Rakocevic"
]

size: 60x40
cell: 10
board: array/initial size/x * size/y no
offsets: [1x0 1x1 0x1 -1x1 -1x0 -1x-1 0x-1 1x-1]

view [
    title "Conway's Game of Life"
    canvas: base size * cell black
    rate 20
    on-time [
        next-gen: copy board
        repeat y size/y [
            repeat x size/x [
                cnt: 0
                pos: as-pair x y
                foreach offset offsets [
                    p: pos + offset
                    if all [p/x > 0 p/x <= size/x p/y > 0 p/y <= size/y][
                        if board/((p/y - 1 * size/x) + p/x)[
                            cnt: cnt + 1
                        ]
                    ]
                ]
                idx: (y - 1 * size/x) + x
                either board/:idx [
                    if cnt < 2 [next-gen/:idx: no]
                    if cnt > 3 [next-gen/:idx: no]
                ][
                    if cnt = 3 [next-gen/:idx: yes]
                ]
            ]
        ]
        board: next-gen
        canvas/draw: clear []
        repeat y size/y [
            repeat x size/x [
                if board/((y - 1 * size/x) + x) [
                    append canvas/draw [
                        fill-pen white box
                        (as-pair x - 1 y - 1 * cell)
                        (as-pair x y * cell)
                    ]
                ]
            ]
        ]
    ]
    on-down [
        pos: event/offset / cell + 1x1
        if all [pos/x > 0 pos/x <= size/x pos/y > 0 pos/y <= size/y][
            idx: (pos/y - 1 * size/x) + pos/x
            board/:idx: not board/:idx
        ]
    ]
]