include std/net/http.e
include std/net/url.e

constant DEFAULT_PORT = 8080
constant DEFAULT_DOC_ROOT = "."

enum SERVE_STATIC, SERVE_EUPHORIA

function get_file_type(sequence path)
    sequence ext = fileext(path)
    switch ext do
        case ".txt" then return "text/plain"
        case ".html", ".htm" then return "text/html"
        case ".jpg", ".jpeg" then return "image/jpeg"
        case ".gif" then return "image/gif"
        case ".png" then return "image/png"
        case else return "application/octet-stream"
    end switch
end function

procedure main()
    atom server = create(DEFAULT_PORT)
    puts(1, "Server started on port " & sprint(DEFAULT_PORT) & "\n")
    while true do
        object client = accept(server)
        if atom(client) then continue end if
        sequence request = receive(client)
        sequence headers = parse_headers(request)
        sequence path = headers["path"]
        sequence full_path = DEFAULT_DOC_ROOT & path
        if file_exists(full_path) then
            sequence content_type = get_file_type(full_path)
            sequence content = read_file(full_path)
            send_response(client, 200, "OK", content_type, content)
        else
            send_response(client, 404, "Not Found", "text/plain", "404 - File not found")
        end if
        close(client)
    end while
end procedure

main()