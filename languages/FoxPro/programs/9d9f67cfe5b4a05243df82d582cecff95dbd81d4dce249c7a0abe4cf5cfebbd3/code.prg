************************************************************************
*  TextToHTML
*
FUNCTION TextToHTML(tcText,llNoHtml)
************************************************************************
*  Author: Rick Strahl
*          (c) West Wind Technologies, 1996-2003
*          http://www.west-wind.com/
*
* Converted from a C# function I wrote
* http://www.west-wind.com/weblog/posts/1154.aspx
*
* Pass in a block of text and it will be converted to 'HTML'
* Specifically it encodes the text and then replaces carriage returns
* with <br> tags.
*
* It can also optionally wrap the text in <pre> tags which is
* useful for displaying code.
*
* llNoHtml - if .t. doesn't HTML encode the text
************************************************************************
LPARAMETERS tcText, llNoHtml, llPreTag
LOCAL lcText

IF EMPTY(tcText)
   RETURN ""
ENDIF

IF VARTYPE(llNoHtml) # "L"
   llNoHtml = .f.
ENDIF
IF VARTYPE(llPreTag) # "L"
   llPreTag = .f.
ENDIF

IF !llNoHtml
   lcText = HtmlEncode(tcText)
ELSE
   lcText = tcText
ENDIF

IF llPreTag
   lcText = "<pre>" + lcText + "</pre>"
ELSE
   lcText = STRTRAN(lcText,CHR(13),"",1)
   lcText = STRTRAN(lcText,CHR(10),"<br />" + CHR(10))
ENDIF

RETURN lcText
* EOF TextToHTML()


************************************************************************
*  HtmlEncode
*
FUNCTION HtmlEncode(cString)
************************************************************************
*  Turns an string into an HTML encoded string
************************************************************************
cString = STRTRAN(cString,"&","&amp;")
cString = STRTRAN(cString,"<","&lt;")
cString = STRTRAN(cString,">","&gt;")
cString = STRTRAN(cString,'"',"&quot;")
cString = STRTRAN(cString,"'","&#39;")

* For <pre> formatting
cString = STRTRAN(cString,CHR(9),"&nbsp;&nbsp;&nbsp;&nbsp;")

RETURN cString
* EOF HtmlEncode()