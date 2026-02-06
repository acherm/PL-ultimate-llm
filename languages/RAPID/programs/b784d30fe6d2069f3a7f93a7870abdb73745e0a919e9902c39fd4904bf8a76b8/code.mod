MODULE MainModule
    CONST robtarget Home := [[300, 0, 400], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget PickPos := [[400, 100, 50], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget PlacePos := [[400, -100, 50], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];

    PROC main()
        MoveJ Home, v1000, z50, tool0;

        ! Pick operation
        MoveL Offs(PickPos, 0, 0, 100), v500, z10, tool0;
        MoveL PickPos, v200, fine, tool0;
        SetDO DO_Gripper, 1;
        WaitTime 0.5;
        MoveL Offs(PickPos, 0, 0, 100), v500, z10, tool0;

        ! Place operation
        MoveL Offs(PlacePos, 0, 0, 100), v500, z10, tool0;
        MoveL PlacePos, v200, fine, tool0;
        SetDO DO_Gripper, 0;
        WaitTime 0.5;
        MoveL Offs(PlacePos, 0, 0, 100), v500, z10, tool0;

        MoveJ Home, v1000, z50, tool0;
    ENDPROC
ENDMODULE
