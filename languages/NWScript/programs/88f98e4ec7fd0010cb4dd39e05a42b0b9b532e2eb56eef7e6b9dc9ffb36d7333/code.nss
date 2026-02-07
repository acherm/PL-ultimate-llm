// Script that fires when a creature enters a trigger
void main()
{
    object oPC = GetEnteringObject();
    
    // Check if the entering object is a player character
    if (!GetIsPC(oPC))
        return;
    
    // Speak a greeting message
    string sGreeting = "Welcome, " + GetName(oPC) + "!";
    SpeakString(sGreeting);
    
    // Create a visual effect
    effect eVFX = EffectVisualEffect(VFX_FNF_SUMMON_MONSTER_1);
    ApplyEffectAtLocation(DURATION_TYPE_INSTANT, eVFX, GetLocation(oPC));
    
    // Give the player some gold
    GiveGoldToCreature(oPC, 100);
}
