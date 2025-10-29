include "console.iol"

interface GreeterInterface {
RequestResponse:
    greet( GreetingRequest )( GreetingResponse )
}

type GreetingRequest: void {
    .name: string
}

type GreetingResponse: void {
    .greeting: string
}

outputPort Greeter {
    Location: "socket://localhost:8000"
    Protocol: http {
        .format = "json"
    }
    Interfaces: GreeterInterface
}

inputPort GreeterIn {
    Location: "socket://localhost:8000"
    Protocol: http {
        .format = "json"
    }
    Interfaces: GreeterInterface
}

main
{
    greet( request )( response ) {
        response.greeting = "Hello, " + request.name + "!"
    }
}