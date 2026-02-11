import net

fn main() {
    net.http_server(8080) { req, res in
        res.status(200)
        res.body = 'Hello, World!'
    }
}