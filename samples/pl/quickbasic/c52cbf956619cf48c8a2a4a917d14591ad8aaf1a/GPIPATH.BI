'**************************************************************
'*
'* Include File: GpiPath.BI
'*
'* Requires:     PMBase.BI (RECTL type)
'*
'* Description:  Path control functions
'*
'*************************************************************
' ** general clipping functions
DECLARE FUNCTION GpiSetGraphicsField%( BYVAL HPS AS LONG,_
				       BYVAL PRECTL AS LONG )

DECLARE FUNCTION GpiQueryGraphicsField%( BYVAL HPS AS LONG,_
					 BYVAL PRECTL AS LONG )

DECLARE FUNCTION GpiSetViewingLimits%( BYVAL HPS AS LONG,_
				       BYVAL PRECTL AS LONG )

DECLARE FUNCTION GpiQueryViewingLimits%( BYVAL HPS AS LONG,_
					 BYVAL PRECTL AS LONG )
 
'  modes for GpiModifyPath
CONST  MPATHSTROKE	    =  6
 
'  modes for GpiFillPath
CONST  FPATHALTERNATE	    =  0
CONST  FPATHWINDING	    =  2
 
'  modes for GpiSetClipPath
CONST  SCPALTERNATE	    =  0
CONST  SCPWINDING	    =  2
CONST  SCPAND		    =  4
CONST  SCPRESET 	    =  0
 
' ** Path and Clip Path functions
DECLARE FUNCTION  GpiBeginPath%( BYVAL HPS AS LONG,_
				 BYVAL ALONG AS LONG )

DECLARE FUNCTION  GpiEndPath%( BYVAL HPS AS LONG )

DECLARE FUNCTION  GpiCloseFigure%( BYVAL HPS AS LONG )

DECLARE FUNCTION  GpiModifyPath%( BYVAL HPS AS LONG,_
				  BYVAL ALONG AS LONG,_
				  BYVAL BLONG AS LONG )

DECLARE FUNCTION  GpiFillPath&( BYVAL HPS AS LONG,_
				BYVAL ALONG AS LONG,_
				BYVAL BLONG AS LONG )

DECLARE FUNCTION  GpiSetClipPath%( BYVAL HPS AS LONG,_
				   BYVAL ALONG AS LONG,_
				   BYVAL BLONG AS LONG )
 
DECLARE FUNCTION  GpiStrokePath&( BYVAL HPS AS LONG,_
				  BYVAL ALONG AS LONG,_
				  BYVAL ULONG AS LONG )
 
