void create() {
    set_name("sword");
    set_short("A sharp sword");
    set_long("This is a very sharp sword.");
    set_weight(1500);
    set_value(50);
    set_type("weapon");
    set_wc(8);
}

void init() {
    ::init();
    add_action("wield_sword", "wield");
}

int wield_sword(string str) {
    if(str == "sword") {
        write("You wield the sword.");
        return 1;
    }
    return 0;
}
