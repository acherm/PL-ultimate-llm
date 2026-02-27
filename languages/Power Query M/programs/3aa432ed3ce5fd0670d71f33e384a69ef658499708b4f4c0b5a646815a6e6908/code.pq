let
    Fibonacci = List.Generate(
        () => [a = 0, b = 1, idx = 0],
        each [idx] < 15,
        each [a = [b], b = [a] + [b], idx = [idx] + 1],
        each [a]
    ),
    AsTable = Table.FromList(Fibonacci, Splitter.SplitByNothing(), {"Value"}),
    WithIndex = Table.AddIndexColumn(AsTable, "N", 0, 1),
    Reordered = Table.ReorderColumns(WithIndex, {"N", "Value"})
in
    Reordered