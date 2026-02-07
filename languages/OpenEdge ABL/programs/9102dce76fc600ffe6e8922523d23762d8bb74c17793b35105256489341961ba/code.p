/* Hello World with File Operations in OpenEdge ABL */
DEFINE VARIABLE cMessage AS CHARACTER NO-UNDO.
DEFINE VARIABLE iCounter AS INTEGER NO-UNDO.

/* Simple loop demonstrating ABL syntax */
DO iCounter = 1 TO 5:
    cMessage = "Hello, World! Iteration: " + STRING(iCounter).
    DISPLAY cMessage WITH FRAME frame-a.
END.

/* Display system information */
MESSAGE "OpenEdge ABL Version:" SKIP
        PROVERSION
        VIEW-AS ALERT-BOX INFORMATION.