$PBExportHeader$n_dwr_dw_storage.sru
forward
global type n_dwr_dw_storage from nonvisualobject
end type
end forward

shared variables
String is_name[]
String is_syntax[]
String is_comment[]

end variables

global type n_dwr_dw_storage from nonvisualobject
end type
global n_dwr_dw_storage n_dwr_dw_storage

forward prototypes
public subroutine of_clear ()
public subroutine of_add_dw (string as_name, string as_syntax, string as_comment)
public function integer of_storetopbl (string as_pbl)
end prototypes

public subroutine of_clear ();String ls_empty[]

is_name[] = ls_empty[]
is_syntax[] = ls_empty[]
is_comment[] = ls_empty[]

end subroutine

public subroutine of_add_dw (string as_name, string as_syntax, string as_comment);Long ll_next

ll_next = UpperBound(is_name[]) + 1
is_name[ll_next] = as_name
is_syntax[ll_next] = as_syntax
is_comment[ll_next] = as_comment

end subroutine

public function integer of_storetopbl (string as_pbl);Int li_ret
Long ll_i

If FileExists(as_pbl) And Not FileDelete(as_pbl) Then
	Return -1
End If

li_ret = LibraryCreate(as_pbl)
If li_ret <> 1 Then 
	Return li_ret
End If
String ls_errors
For ll_i = 1 To UpperBound(is_name[])
	li_ret = LibraryImport( &
		as_pbl, &
		is_name[ll_i], &
		ImportDatawindow!,  &
		is_syntax[ll_i], &
		ls_errors, &
		is_comment[ll_i] &
	)
Next
Return 1
end function

on n_dwr_dw_storage.create
call super::create
TriggerEvent( this, "constructor" )
end on

on n_dwr_dw_storage.destroy
TriggerEvent( this, "destructor" )
call super::destroy
end on

