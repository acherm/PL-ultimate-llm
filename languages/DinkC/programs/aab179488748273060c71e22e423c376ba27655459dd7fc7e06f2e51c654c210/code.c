// bonca.c
void main(void)
{
    sp_base_walk(&current_sprite, 530);
    sp_speed(&current_sprite, 1);
    sp_brain(&current_sprite, 9);
    sp_touch_damage(&current_sprite, 2);
    sp_hitpoints(&current_sprite, 10);
    sp_exp(&current_sprite, 10);
    sp_base_attack(&current_sprite, 540);
    sp_strength(&current_sprite, 5);
    sp_distance(&current_sprite, 40);
    sp_range(&current_sprite, 35);
    sp_target(&current_sprite, 1);
    int &attack_wait = 0;
}

void attack(void)
{
    playsound(31, 22050,0,&current_sprite, 0);
    &attack_wait = random(4000, 0);
    sp_attack_wait(&current_sprite, &attack_wait);
}

void die(void)
{
    int &editor_sprite = sp_editor_num(&current_sprite);
    if (&editor_sprite != 0)
        editor_type(&editor_sprite, 6);

    &save_x = sp_x(&current_sprite, -1);
    &save_y = sp_y(&current_sprite, -1);
    external("emake","medium");
}
