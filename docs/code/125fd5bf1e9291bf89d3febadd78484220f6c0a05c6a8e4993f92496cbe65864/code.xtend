package example4

import java.io.BufferedReader
import java.io.InputStreamReader
import java.io.PrintWriter
import java.net.ServerSocket

class BasicWebServer {
	def static void main(String[] args) {
		val server = new ServerSocket(8080)
		while (true) {
			val socket = server.accept
			val reader = new BufferedReader(new InputStreamReader(socket.inputStream))
			val writer = new PrintWriter(socket.outputStream)
			try {
				while (reader.readLine != '') {}
				writer.println('HTTP/1.0 200 OK')
				writer.println('Content-Type: text/html')
				writer.println('')
				writer.println('<html><body>Hello World</body></html>')
				writer.flush
			} finally {
				writer.close
				reader.close
				socket.close
			}
		}
	}
}