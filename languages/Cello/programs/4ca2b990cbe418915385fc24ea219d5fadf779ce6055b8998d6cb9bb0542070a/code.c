#include "Cello.h"

int main(int argc, char** argv) {
  var items = new(Array, Int);

  push(items, $I(1));
  push(items, $I(2));
  push(items, $I(3));

  foreach(item in items) {
    print("Item: %$\n", item);
  }

  delete(items);

  return 0;
}
