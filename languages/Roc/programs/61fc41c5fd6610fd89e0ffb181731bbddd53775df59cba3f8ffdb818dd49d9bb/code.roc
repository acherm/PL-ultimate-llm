app "http-requests"
    packages { pf: "platform/main.roc" }
    imports [pf.Http, pf.Task.{ Task }]
    provides [main] to pf

main : Task {} *
main =
    request = Http.request {
        method: Get,
        host: "api.github.com",
        path: "/repos/roc-lang/roc/commits",
        headers: [("Accept", "application/vnd.github.v3+json")],
        body: Http.emptyBody,
    }

    request
    |> Http.send
    |> Task.onErr handleError
    |> Task.map handleResponse

handleError : Http.HttpError -> Task {} *
handleError = \err ->
    dbg err
    Task.ok {}

handleResponse : Http.Response -> {}
handleResponse = \response ->
    dbg response
    {}