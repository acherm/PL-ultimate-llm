#include <sourcemod>

public Plugin:myinfo =
{
    name = "Hello World",
    author = "AlliedModders LLC",
    description = "Prints a message to the server console.",
    version = "1.0",
    url = "http://www.alliedmods.net/"
};

public OnPluginStart()
{
    PrintToServer("Hello, world!");
}