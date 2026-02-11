import ballerina/http;
import ballerina/io;

public function main() returns error? {
    http:Client clientEp = check new ("http://postman-echo.com");

    string payload = "Hello from Ballerina";
    http:Response response = check clientEp->post("/post", payload);
    json result = check response.getJsonPayload();

    io:println("Status code: " + response.statusCode.toString());
    io:println("Content-Type: " + (check response.getHeader("content-type")));
    io:println("Payload: ", result);
    return;
}