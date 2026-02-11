def server = new ServerSocket(8080)
while (true) {
    server.accept() { socket ->
        socket.withStreams { input, output ->
            def reader = input.newReader()
            def writer = output.newWriter()
            def line
            while ((line = reader.readLine()) && line.length() > 0) {
                println line
            }
            writer << "HTTP/1.1 200 OK\n"
            writer << "Content-Type: text/plain\n\n"
            writer << "Hello, World!\n"
            writer.flush()
        }
    }
}