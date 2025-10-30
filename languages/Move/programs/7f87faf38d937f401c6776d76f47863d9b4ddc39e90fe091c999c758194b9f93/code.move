// In file: sources/tutorial.move

module 0x0::tutorial {

    use std::vector;

    struct Cookie has store, drop {
        val: u8,
    }

    struct CookieJar has key {
        cookies: vector::Vector<Cookie>,
    }

    fun init_module(sender: &signer) {
        move_to(sender, CookieJar { cookies: vector::empty() });
    }

    public entry fun add_cookie(jar: &mut CookieJar, val: u8) {
        vector::push_back(&mut jar.cookies, Cookie { val });
    }

    public entry fun remove_cookie(jar: &mut CookieJar): u8 {
        vector::pop_back(&mut jar.cookies).val
    }

    public entry fun get_cookies_length(jar: &signer CookieJar): u64 {
        vector::length(&jar.cookies)
    }

}