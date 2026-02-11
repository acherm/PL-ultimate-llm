implement Hello;

include "sys.m";

sys: Sys;

init()
{
	sys = load Sys Sys->PATH;
	sys->print("Hello world\n");
}