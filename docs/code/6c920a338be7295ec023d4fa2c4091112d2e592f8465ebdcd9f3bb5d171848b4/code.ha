use fmt;
use net;
use net::tcp;
use net::http;

export fn main() void = {
	const addr = net::address(
		net::ip::v4::LOOPBACK,
		8080,
	);
	const listener = match (tcp::listen(addr)) {
		case let l: tcp::listener => l,
		case let err: tcp::error => {
			fmt::fatalf("Error listening on {}: {}", addr, err);
		},
	};
	defer tcp::close(listener);

	for (true) {
		const conn = match (tcp::accept(listener)) {
			case let c: tcp::connection => c,
			case let err: tcp::error => {
				fmt::errorf("Error accepting connection: {}", err);
				continue;
			},
		};
		defer tcp::close(conn);

		const request = match (http::recvrequest(conn)) {
			case let r: http::request => r,
			case let err: http::error => {
				fmt::errorf("Error receiving request: {}", err);
				continue;
			},
		};
		defer http::freerequest(request);

		http::sendresponse(conn, 200, [
			("content-type", "text/plain"),
		], "Hello from Hare!\n") as http::response;
	};
};
