import vibe.vibe;

void main()
{
    auto settings = new HTTPServerSettings;
    settings.port = 8080;
    settings.bindAddresses = ["::1", "127.0.0.1"];

    listenHTTP(settings, &handleRequest);
    runApplication();
}

void handleRequest(HTTPServerRequest req, HTTPServerResponse res)
{
    res.writeBody("Hello, World!");
}