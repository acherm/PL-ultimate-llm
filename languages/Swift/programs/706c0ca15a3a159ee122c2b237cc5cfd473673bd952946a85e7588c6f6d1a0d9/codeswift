import Foundation

public enum Markdown {
    case header(Int, String)
    case paragraph(String)
    case codeBlock(String, String)
    case unorderedList([String])
    case orderedList([String])
    case horizontalRule
    case image(String, String)
    case link(String, String)
    case bold(String)
    case italic(String)
    case strikethrough(String)
    case inlineCode(String)
}

extension Markdown {
    public var html: String {
        switch self {
        case.header(let level, let text):
            return "<h\(level)>\(text)</h\(level)>"
        case.paragraph(let text):
            return "<p>\(text)</p>"
        case.codeBlock(let code, let language):
            return "<pre><code class='\(language)'>\(code)</code></pre>"
        case.unorderedList(let items):
            return "<ul>\(items.map { "<li>\($0)</li>" }.joined())</ul>"
        case.orderedList(let items):
            return "<ol>\(items.map { "<li>\($0)</li>" }.joined())</ol>"
        case.horizontalRule:
            return "<hr>"
        case.image(let url, let alt):
            return "<img src='\(url)' alt='\(alt)'>"
        case.link(let url, let text):
            return "<a href='\(url)'>\(text)</a>"
        case.bold(let text):
            return "<b>\(text)</b>"
        case.italic(let text):
            return "<i>\(text)</i>"
        case.strikethrough(let text):
            return "<s>\(text)</s>"
        case.inlineCode(let code):
            return "<code>\(code)</code>"
        }
    }
}