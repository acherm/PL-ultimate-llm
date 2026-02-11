Structure TSnake
  x.i
  y.i
  dx.i
  dy.i
  length.i
  List segments.TPoint()
EndStructure

Structure TPoint
  x.i
  y.i
EndStructure

#CELL_SIZE = 10
#GRID_WIDTH = 40
#GRID_HEIGHT = 30

Global snake.TSnake
Global food.TPoint

Procedure InitGame()
  snake\x = #GRID_WIDTH / 2
  snake\y = #GRID_HEIGHT / 2
  snake\dx = 1
  snake\dy = 0
  snake\length = 3
  ClearList(snake\segments())
  
  food\x = Random(#GRID_WIDTH - 1)
  food\y = Random(#GRID_HEIGHT - 1)
EndProcedure

Procedure OpenWindow()
  OpenWindow(0, 0, 0, #GRID_WIDTH * #CELL_SIZE, #GRID_HEIGHT * #CELL_SIZE, "Snake", #PB_Window_ScreenCentered)
  CreateGadgetList(WindowID(0))
EndProcedure

InitGame()
OpenWindow()

Repeat
  event = WaitWindowEvent(10)
  
  If event = #PB_Event_KeyDown
    Select EventKey()
      Case #PB_Key_Left
        If snake\dx = 0
          snake\dx = -1
          snake\dy = 0
        EndIf
      Case #PB_Key_Right
        If snake\dx = 0
          snake\dx = 1
          snake\dy = 0
        EndIf
    EndSelect
  EndIf
  
  snake\x + snake\dx
  snake\y + snake\dy
  
  StartDrawing(WindowOutput(0))
  Box(0, 0, WindowWidth(0), WindowHeight(0), RGB(0, 0, 0))
  Circle(food\x * #CELL_SIZE + #CELL_SIZE/2, food\y * #CELL_SIZE + #CELL_SIZE/2, #CELL_SIZE/2, RGB(255, 0, 0))
  ForEach snake\segments()
    Box(snake\segments()\x * #CELL_SIZE, snake\segments()\y * #CELL_SIZE, #CELL_SIZE, #CELL_SIZE, RGB(0, 255, 0))
  Next
  StopDrawing()
Until event = #PB_Event_CloseWindow