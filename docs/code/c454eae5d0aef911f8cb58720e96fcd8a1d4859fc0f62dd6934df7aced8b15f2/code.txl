%       Extract initializers from C declarations
%       
%       David A. Penny
%       Copyright (c) 1993-2006 Queen's University at Kingston

#pragma -case

include "C.grm"

define program
    [C_source]
end define

rule main
    replace [program]
        P [C_source]
    by
        P [extractInitializers]
end rule


%
%  For each declarator with an initializer, we extract the initializer
%  into a separate assignment statement.  For example,
%
%       int i = 1, j, k = 2;
%
%  becomes
%
%       int i, j, k;
%       i = 1;
%       k = 2;
%
function extractInitializers
    replace [declaration]
        StorageSpec [opt storage_class_specifiers] TypeSpec [type_specifier] InitList [init_declarator_list] Semi [;]
    construct NewInitList [init_declarator_list]
        InitList [stripInitializers]
    construct Assignments [repeat statement]
        InitList [makeAssignments]
    by
        StorageSpec TypeSpec NewInitList Semi
        Assignments
end function


function stripInitializers
    replace [init_declarator_list]
        ID [id] EQ [=] Init [initializer]
    by
        ID
end function


function makeAssignments
    replace [init_declarator_list]
        ID [id] EQ [=] Init [initializer]
    construct Assignment [statement]
        ID = Init ;
    by
        Assignment
end function


%
%  The following rules are to prevent the transformation from being
%  applied to things that are not declarators.
%
rule dummy
    replace $ [init_declarator_list]
        L [init_declarator_list]
    by
        L
end rule

rule dummy2
    replace $ [statement]
        S [statement]
    by
        S
end rule