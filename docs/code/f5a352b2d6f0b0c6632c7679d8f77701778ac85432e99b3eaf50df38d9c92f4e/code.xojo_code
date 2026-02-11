Protected Function Operator_Convert() As String
  Return Me.ToString
End Function

Protected Function Operator_Lookup(key As String) As JSONItem
  If mType = kTypeObject Then
    If mChildren.HasKey(key) Then
      Return mChildren.Value(key)
    End If
  End If
  
  Return Nil
End Function

Protected Function Operator_Lookup(index As Integer) As JSONItem
  If mType = kTypeArray And index >= 0 And index <= UBound(mChildrenArray) Then
    Var child As JSONItem = mChildrenArray(index)
    Return child
  End If
  
  Return Nil
End Function

Sub Append(item As JSONItem)
  If mType <> kTypeArray Then
    Raise New NilObjectException
  End If
  
  mChildrenArray.Add(item)
End Sub

Sub Constructor()
  mChildren = New Dictionary
  mChildrenArray = New JSONItem()
  mType = kTypeNull
End Sub

Sub Constructor(source As String)
  mChildren = New Dictionary
  mChildrenArray = New JSONItem()
  Parse(source)
End Sub

Sub Constructor(value As Variant)
  mChildren = New Dictionary
  mChildrenArray = New JSONItem()
  
  If value IsA String Then
    mType = kTypeString
    mValue = value.StringValue
  ElseIf value IsA Integer Then
    mType = kTypeNumber
    mValue = value.IntegerValue
  ElseIf value IsA Double Then
    mType = kTypeNumber
    mValue = value.DoubleValue
  ElseIf value IsA Boolean Then
    mType = kTypeBoolean
    mValue = value.BooleanValue
  ElseIf value IsA JSONItem Then
    mType = value.Type
    mValue = value.Value
    If mType = kTypeObject Then
      mChildren = value.mChildren
    ElseIf mType = kTypeArray Then
      mChildrenArray = value.mChildrenArray
    End If
  Else
    mType = kTypeNull
  End If
End Sub

Function IndexOf(item As JSONItem) As Integer
  If mType <> kTypeArray Then
    Raise New NilObjectException
  End If
  
  For i As Integer = 0 To mChildrenArray.LastIndex
    If mChildrenArray(i) = item Then
      Return i
    End If
  Next
  
  Return -1
End Function

Function IndentString(level As Integer) As String
  Var s As String
  For i As Integer = 1 To level
    s = s + "  "
  Next
  Return s
End Function

Sub Insert(index As Integer, item As JSONItem)
  If mType <> kTypeArray Then
    Raise New NilObjectException
  End If
  
  If index < 0 Or index > mChildrenArray.LastIndex + 1 Then
    Raise New OutOfBoundsException
  End If
  
  mChildrenArray.Add(index, item)
End Sub

Function IsNull() As Boolean
  Return mType = kTypeNull
End Function

Sub Parse(source As String)
  // Simple JSON parser - this is a basic implementation
  // For production, use a proper parser
  mSource = source.Trim
  mIndex = 0
  SkipWhitespace
  
  If Not mSource.Middle(mIndex, 1) = "{" And Not mSource.Middle(mIndex, 1) = "[" Then
    // Assume it's a primitive value
    ParseValue
  Else
    ParseObjectOrArray
  End If
End Sub

Private Sub ParseObjectOrArray
  If mSource.Middle(mIndex, 1) = "{" Then
    mType = kTypeObject
    mIndex = mIndex + 1
    SkipWhitespace
    While mIndex < mSource.Len And mSource.Middle(mIndex, 1) <> "}"
      Var key As String = ParseString
      SkipWhitespace
      If mSource.Middle(mIndex, 1) <> ":" Then
        // Error
        Return
      End If
      mIndex = mIndex + 1
      SkipWhitespace
      Var value As JSONItem = ParseValue
      mChildren.Value(key) = value
      SkipWhitespace
      If mSource.Middle(mIndex, 1) = "," Then
        mIndex = mIndex + 1
        SkipWhitespace
      End If
    Wend
    If mIndex < mSource.Len Then
      mIndex = mIndex + 1 // Skip }
    End If
  ElseIf mSource.Middle(mIndex, 1) = "[" Then
    mType = kTypeArray
    mIndex = mIndex + 1
    SkipWhitespace
    While mIndex < mSource.Len And mSource.Middle(mIndex, 1) <> "]"
      Var value As JSONItem = ParseValue
      mChildrenArray.Add(value)
      SkipWhitespace
      If mSource.Middle(mIndex, 1) = "," Then
        mIndex = mIndex + 1
        SkipWhitespace
      End If
    Wend
    If mIndex < mSource.Len Then
      mIndex = mIndex + 1 // Skip ]
    End If
  End If
End Sub

Private Function ParseString() As String
  If mSource.Middle(mIndex, 1) <> "\" Then
    // Error
    Return ""
  End If
  mIndex = mIndex + 1
  Var start As Integer = mIndex
  While mIndex < mSource.Len And mSource.Middle(mIndex, 1) <> "\""
    mIndex = mIndex + 1
  Wend
  Var s As String = mSource.Middle(start, mIndex - start)
  mIndex = mIndex + 1 // Skip closing "
  Return s
End Function

Private Function ParseValue() As JSONItem
  SkipWhitespace
  Var c As String = mSource.Middle(mIndex, 1)
  Var item As New JSONItem
  If c = "{"
    item = New JSONItem
    item.mType = kTypeObject
    // Parse object
  ElseIf c = "["
    item = New JSONItem
    item.mType = kTypeArray
    // Parse array
  ElseIf c = "\""
    item = New JSONItem(ParseString)
    item.mType = kTypeString
  ElseIf c = "true"
    item = New JSONItem(True)
    mIndex = mIndex + 4
  ElseIf c = "false"
    item = New JSONItem(False)
    mIndex = mIndex + 5
  ElseIf c = "null"
    item = New JSONItem
    mIndex = mIndex + 4
  Else
    // Number
    Var start As Integer = mIndex
    While mIndex < mSource.Len And IsNumeric(mSource.Middle(mIndex, 1)) Or mSource.Middle(mIndex, 1) = "." Or mSource.Middle(mIndex, 1) = "-" Or mSource.Middle(mIndex, 1) = "e" Or mSource.Middle(mIndex, 1) = "E"
      mIndex = mIndex + 1
    Wend
    Var numStr As String = mSource.Middle(start, mIndex - start)
    If numStr.IndexOf(".") > 0 Or numStr.IndexOf("e") > 0 Or numStr.IndexOf("E") > 0 Then
      item = New JSONItem.CDbl(numStr)
    Else
      item = New JSONItem.CInt(numStr)
    End If
    item.mType = kTypeNumber
  End If
  Return item
End Function

Private Sub SkipWhitespace
  While mIndex < mSource.Len And (mSource.Middle(mIndex, 1) = " " Or mSource.Middle(mIndex, 1) = Chr(9) Or mSource.Middle(mIndex, 1) = Chr(10) Or mSource.Middle(mIndex, 1) = Chr(13))
    mIndex = mIndex + 1
  Wend
End Sub

Function ToString(pretty As Boolean = False, indentLevel As Integer = 0) As String
  Var indent As String = If(pretty, IndentString(indentLevel), "")
  
  Select Case mType
  Case kTypeNull
    Return "null"
  Case kTypeString
    Return "\"" + mValue.StringValue.ReplaceAll("\"", "\\\"") + "\""
  Case kTypeNumber
    Return mValue.StringValue
  Case kTypeBoolean
    Return If(mValue.BooleanValue, "true", "false")
  Case kTypeArray
    Var s As String = "["
    If pretty Then s = s + EndOfLine
    For i As Integer = 0 To mChildrenArray.LastIndex
      Var child As JSONItem = mChildrenArray(i)
      If i > 0 Then s = s + If(pretty, IndentString(indentLevel + 1), "") + "," + If(pretty, EndOfLine, " ")
      s = s + If(pretty, IndentString(indentLevel + 1), "") + child.ToString(pretty, indentLevel + 1)
    Next
    If pretty And mChildrenArray.LastIndex >= 0 Then s = s + EndOfLine
    s = s + indent + "]"
    Return s
  Case kTypeObject
    Var s As String = "{" + If(pretty, EndOfLine, " ")
    Var keys() As Variant = mChildren.Keys
    For i As Integer = 0 To keys.LastIndex
      Var key As String = keys(i)
      Var value As JSONItem = mChildren.Value(key)
      If i > 0 Then s = s + "," + If(pretty, EndOfLine, " ")
      s = s + If(pretty, IndentString(indentLevel + 1), "") + "\"" + key.ReplaceAll("\"", "\\\"") + "\":" + If(pretty, " ", "") + value.ToString(pretty, indentLevel + 1)
    Next
    If pretty And keys.LastIndex >= 0 Then s = s + EndOfLine
    s = s + indent + "}"
    Return s
  End Select
End Function

Property Type As JSONTypes
  Return mType
End Property

Property Value As Variant
  If mType = kTypeNull Then
    Return Nil
  End If
  Return mValue
End Property