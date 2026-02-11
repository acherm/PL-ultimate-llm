import kotlinx.html.*

fun main() {
    println(renderToString { html { body { h1 { "+Kotlinx.html" } } } })
}