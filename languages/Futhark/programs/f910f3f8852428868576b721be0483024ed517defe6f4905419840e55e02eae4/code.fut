fun matmul [N][M][K] (A: [N][M]i32) (B: [M][K]i32): [N][K]i32 =
  map (\row_A: [M]i32 ->
         map (\col_B: [M]i32 ->
                reduce (+) 0 (map2 (*) row_A col_B)
             ) (transpose B)
      ) A