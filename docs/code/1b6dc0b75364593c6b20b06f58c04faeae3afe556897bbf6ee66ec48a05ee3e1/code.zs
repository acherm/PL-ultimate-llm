/*
    Auto-save script for GZDoom
    by JP LeBreton

    To use:
    - copy this file into your GZDoom directory
    - add the following to your gzdoom.ini file, in the [Global.Autoload] section:
        Path=autosave.zs
    - when you start a game, the script will be active
    - saves to a slot named "autosave"
    - by default, saves every 5 minutes

    To configure:
    - in the GZDoom console (~ key), type e.g.:
        autosave_interval 10
    - this will set the save interval to 10 minutes
    - this setting will be saved to your .ini file

*/

class AutoSaveHandler : StaticEventHandler
{
    // save interval in minutes
    private CVar autoSaveInterval;

    // time of last save, in tics
    private int lastSaveTime;

    override void OnRegister()
    {
        // register our CVar
        autoSaveInterval = CVar.Get(
            "autosave_interval",      // cvar name
            5,                        // default value
            CVAR_ARCHIVE              // flags
            );
    }

    override void WorldTick()
    {
        // don't run in menus
        if (gamestate != GS_LEVEL)
        {
            return;
        }

        // don't run if player is dead
        let p = players[consoleplayer];
        if (!p || !p.mo || p.health <= 0)
        {
            return;
        }

        // time since last save, in minutes
        let timeSinceLastSave = (gametic - lastSaveTime) / (35.0 * 60.0);

        if (timeSinceLastSave >= autoSaveInterval.GetFloat())
        {
            Console.Printf("Auto-saving...");
            SendNetworkEvent("AutoSave");
            lastSaveTime = gametic;
        }
    }

    override void NetworkProcess(ConsoleEvent e)
    {
        if (e.Name == "AutoSave")
        {
            Game.Save("autosave", "Auto-save");
        }
    }
}