const std = @import("std");

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};;
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    const address = try std.net.Address.parseIp("127.0.0.1", 8080);
    var server = std.net.StreamServer.init(.{});
    defer server.deinit();

    try server.listen(address);
    std.log.info("listening on {}", .{address});

    while (true) {
        const connection = try server.accept();
        try handle_request(allocator, connection);
    }
}

fn handle_request(allocator: std.mem.Allocator, connection: std.net.StreamServer.Connection) !void {
    defer connection.stream.close();

    var buf: [1024]u8 = undefined;
    const n = try connection.stream.read(&buf);

    const response =
        "HTTP/1.1 200 OK\r\n" ++
        "Content-Type: text/plain\r\n" ++
        "\r\n" ++
        "Hello, World!\n";

    _ = try connection.stream.write(response);
}