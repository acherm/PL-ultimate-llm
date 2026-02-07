"Verb: say
This verb allows a player to speak in a room

if (dobjstr == "")
  player:tell("Say what?");
  return;
endif

message = dobjstr;
player.location:announce(player.name, " says, \"", message, "\"");
player:tell("You say, \"", message, "\"");
