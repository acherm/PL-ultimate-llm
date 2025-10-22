open System

type Cell = Alive | Dead
type Grid = Cell[,]

let initGrid size =
    let r = Random()
    Array2D.init size size (fun _ _ -> if r.Next(2) = 0 then Dead else Alive)

let countNeighbors (grid: Grid) row col =
    let size = Array2D.length1 grid
    let mutable count = 0
    for r in (max 0 (row-1))..(min (size-1) (row+1)) do
        for c in (max 0 (col-1))..(min (size-1) (col+1)) do
            if not (r = row && c = col) && grid.[r,c] = Alive then
                count <- count + 1
    count

let nextGeneration (grid: Grid) =
    let size = Array2D.length1 grid
    Array2D.init size size (fun r c ->
        match grid.[r,c], countNeighbors grid r c with
        | Alive, (2 | 3) -> Alive
        | Dead, 3 -> Alive
        | _ -> Dead)

let printGrid (grid: Grid) =
    let size = Array2D.length1 grid
    for r in 0..size-1 do
        for c in 0..size-1 do
            printf "%s" (if grid.[r,c] = Alive then "█" else " ")
        printfn ""
    printfn ""

let rec gameLoop grid =
    Console.Clear()
    printGrid grid
    System.Threading.Thread.Sleep(100)
    gameLoop (nextGeneration grid)

[<EntryPoint>]
let main argv =
    gameLoop (initGrid 20)
    0