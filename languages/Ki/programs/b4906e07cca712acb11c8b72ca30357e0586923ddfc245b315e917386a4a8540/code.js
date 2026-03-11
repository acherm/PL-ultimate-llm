function somefunc (a) {
  ki (toJs (filter (fn [el] (isEven el)) (range a))).forEach(function(el) {
      console.log(el);
      });
  return [0, 1, 2, 3, 4].filter(ki (fn [el] (isEven el)));
}
console.log(somefunc(5));
// => 0
// => 2
// => 4
// [0 2 4]
