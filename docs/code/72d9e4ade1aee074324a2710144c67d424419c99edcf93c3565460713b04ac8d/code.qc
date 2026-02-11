// Simple QuakeC weapon firing function
void() W_FireShotgun =
{
    local vector dir;
    
    sound (self, CHAN_WEAPON, "weapons/guncock.wav", 1, ATTN_NORM);
    
    msg_entity = self;
    WriteByte (MSG_ALL, SVC_SMALLKICK);
    
    self.currentammo = self.ammo_shells = self.ammo_shells - 1;
    dir = aim (self, 100000);
    FireBullets (6, dir, '0.04 0.04 0');
};

void() W_FireSuperShotgun =
{
    local vector dir;
    
    if (self.currentammo == 1)
    {
        W_FireShotgun ();
        return;
    }
    
    sound (self, CHAN_WEAPON, "weapons/shotgn2.wav", 1, ATTN_NORM);
    
    msg_entity = self;
    WriteByte (MSG_ALL, SVC_BIGKICK);
    
    self.currentammo = self.ammo_shells = self.ammo_shells - 2;
    dir = aim (self, 100000);
    FireBullets (14, dir, '0.14 0.08 0');
};
