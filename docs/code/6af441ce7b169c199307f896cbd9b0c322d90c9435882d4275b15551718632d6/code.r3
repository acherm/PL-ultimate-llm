Rebol [
    Title: "Simple HTTP Server"
    Date: 1-Jan-2019
]

port: open/custom tcp://:8080 [
    Title: "HTTP Server"
    handler: func [port] [
        request: parse port/data ["GET" copy path to " "]
        path: to file! either path = "/" ["index.html"][path]
        either exists? path [
            data: read path
            response: rejoin [
                "HTTP/1.1 200 OK^/"
                "Content-Type: text/html^/"
                "Content-Length: " length? data "^/^/"
                data
            ]
        ][
            response: "HTTP/1.1 404 Not Found^/^/"
        ]
        write port response
        close port
    ]
]

wait port