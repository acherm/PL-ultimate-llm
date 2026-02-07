; GDL program to plot a sine wave
PRO plot_sine
  ; Generate x values from 0 to 2*pi
  x = FINDGEN(100) * 2 * !PI / 99.0
  
  ; Calculate sine values
  y = SIN(x)
  
  ; Create the plot
  PLOT, x, y, TITLE='Sine Wave', XTITLE='x', YTITLE='sin(x)', $
        LINESTYLE=0, THICK=2
  
  ; Print some information
  PRINT, 'Maximum value: ', MAX(y)
  PRINT, 'Minimum value: ', MIN(y)
END

; Call the procedure
plot_sine