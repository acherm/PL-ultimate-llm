/mob
    Login()
        ..()
        world << "[src] has joined the game!"
        src << "Welcome to the game!"

    Logout()
        ..()
        world << "[src] has left the game!"

    verb/say(msg as text)
        world << "[src] says: [msg]"

    verb/examine(atom/target as mob|obj in view())
        src << "You examine [target]."
        src << "Description: [target.desc]"
