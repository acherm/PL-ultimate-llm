@* Hello World Program.
This is a simple WEB program that prints a greeting message.

@c
@<Include files@>@;
program hello(output);
begin
  @<Print the greeting@>@;
end.

@ We need to include standard definitions.
@<Include files@>=
{No special includes needed for this simple program}

@ The greeting consists of a simple message.
@<Print the greeting@>=
writeln('Hello, World!');
writeln('This is a WEB program')
