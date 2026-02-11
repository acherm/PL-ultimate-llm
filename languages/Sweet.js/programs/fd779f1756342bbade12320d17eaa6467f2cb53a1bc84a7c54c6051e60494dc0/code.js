syntax function = function (ctx) {
  let name = ctx.next().value;
  let params = ctx.next().value;
  let body = ctx.next().value;
  return #`function ${name} ${params} ${body}`;
}

function add(a, b) {
  return a + b;
}

console.log(add(2, 3));
