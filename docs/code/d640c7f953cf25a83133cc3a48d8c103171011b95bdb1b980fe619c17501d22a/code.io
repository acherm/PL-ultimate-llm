Server := Object clone

Server start := method(
    socket := ServerSocket clone
    socket setPort(8000)
    socket listen()

    while(true,
        connection := socket accept
        response := "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<h1>Hello from Io!</h1>"
        connection write(response)
        connection close
    )
)