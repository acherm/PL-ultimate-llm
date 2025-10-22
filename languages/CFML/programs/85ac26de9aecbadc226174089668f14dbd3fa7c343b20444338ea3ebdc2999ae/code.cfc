component {
    public any function init() {
        return this;
    }

    public boolean function authenticate(string username, string password) {
        var authenticated = false;
        if (len(trim(username)) && len(trim(password))) {
            var user = entityLoad('User', {
                username = username,
                password = hash(password, 'SHA-512')
            }, true);
            if (!isNull(user)) {
                authenticated = true;
                session.auth = {
                    isLoggedIn = true,
                    user = user
                };
            }
        }
        return authenticated;
    }

    public void function logout() {
        structDelete(session, 'auth');
    }
}