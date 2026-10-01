:- module mercuryprobelib.

:- interface.
:- import_module io.

:- pred write_hello(io::di, io::uo) is det.
:- pred write_global_value(io::di, io::uo) is det.

:- implementation.
:- import_module string, list.

:- mutable(global, int, 561, ground, [untrailed,
    foreign_name("C", "GLOBAL"), attach_to_io_state]).

:- pragma foreign_export("C", write_hello(di, uo),
    "write_hello").

write_hello(!IO) :-
    io.write_string("Hello World\n", !IO).

:- pragma foreign_export("C", write_global_value(di, uo),
    "write_global_value").

write_global_value(!IO) :-
    get_global(Value, !IO),
    io.format("The new value of global is %d.\n", [i(Value)], !IO).

:- initialise initialiser/2.

:- pred initialiser(io::di, io::uo) is det.

initialiser(!IO) :-
    io.write_string("mercuryprobelib: the initialiser has now been invoked.\n",
        !IO).

:- finalise finaliser/2.

:- pred finaliser(io::di, io::uo) is det.

finaliser(!IO) :-
    io.write_string("mercuryprobelib: the finaliser has now been invoked.\n",
        !IO).

:- end_module mercuryprobelib.