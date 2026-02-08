bring cloud;

let bucket = new cloud.Bucket();
let queue = new cloud.Queue();
let counter = new cloud.Counter();

queue.setConsumer(inflight (message: str) => {
  let count = counter.inc();
  bucket.put("message-${count}", message);
  log("Stored message #${count}: ${message}");
});

let api = new cloud.Api();

api.post("/message", inflight (req: cloud.ApiRequest): cloud.ApiResponse => {
  let body = req.body ?? "no message";
  queue.push(body);
  return cloud.ApiResponse {
    status: 200,
    body: "Message queued successfully"
  };
});

api.get("/count", inflight (req: cloud.ApiRequest): cloud.ApiResponse => {
  let count = counter.peek();
  return cloud.ApiResponse {
    status: 200,
    body: "Total messages: ${count}"
  };
});
