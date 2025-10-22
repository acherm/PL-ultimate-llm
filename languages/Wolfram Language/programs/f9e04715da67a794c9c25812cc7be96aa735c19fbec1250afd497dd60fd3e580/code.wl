mandelbrotSet[c_] := NestWhileList[#^2 + c &, 0, Abs[#] <= 2 &, 1, 50];
MandelbrotPlot[n_] := DensityPlot[
Length[mandelbrotSet[x + I y]], {x, -2, 1}, {y, -1.5, 1.5},
PlotPoints -> n,
ColorFunction -> (GrayLevel[1 - #] &),
Frame -> False,
PlotRangePadding -> None
]