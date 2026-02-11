#include <cstdio>

enum class Color {
  Red,
  Green,
  Blue
};

int main() {
  // Use Circle's reflection feature to iterate over enum values
  @meta for(int i = 0; i < @enum_count(Color); ++i) {
    @meta Color color = @enum_value(Color, i);
    printf("%s\n", @enum_name(color));
  }
  return 0;
}
