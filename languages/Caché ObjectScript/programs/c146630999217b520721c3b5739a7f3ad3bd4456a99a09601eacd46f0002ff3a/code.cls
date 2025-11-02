Class Package.Sample.API Extends %CSP.REST
{

Parameter HandleCorsRequest = 1;

XData UrlMap [ XMLNamespace = "http://www.intersystems.com/urlmap" ]
{
<Routes>
  <Route Url="/hello" Method="GET" Call="GetHello" />
  <Route Url="/hello/:name" Method="GET" Call="GetHelloName" />
  <Route Url="/hello" Method="POST" Call="PostHello" />
</Routes>
}

ClassMethod GetHello() As %Status
{
    Return ..%SetStatusCode(..#HTTP200OK, "Hello world")
}

ClassMethod GetHelloName(pName As %String) As %Status
{
    Return ..%SetStatusCode(..#HTTP200OK, "Hello "_pName)
}

ClassMethod PostHello() As %Status
{
    Set tSC = $$$OK
    Try {
        Set tRequest = ..%Request
        Set tJSON = {}.%FromJSON(tRequest.Content)
        Set tName = tJSON.name
        Set tSC = ..%SetStatusCode(..#HTTP200OK, "Hello "_tName)
    } Catch(e) {
        Set tSC = e.AsStatus()
    }
    Return tSC
}

}