Sub Main
    ' Create a new document with formatted text
    FileNew
    Insert "WordBasic Macro Example"
    InsertPara
    InsertPara

    ' Format the title
    StartOfDocument
    Bold 1
    Font "Arial", 16
    CenterPara
    EndOfLine
    Bold 0
    Font "Times New Roman", 12
    LeftPara

    ' Add content
    Insert "This is a simple WordBasic macro that demonstrates:"
    InsertPara
    Insert "- Document creation"
    InsertPara
    Insert "- Text formatting"
    InsertPara
    Insert "- Paragraph styling"
    InsertPara
    InsertPara
    Insert "WordBasic was the macro language for Microsoft Word "
    Insert "versions 6.0 and 7.0 (Word 95) before being replaced by VBA."
End Sub