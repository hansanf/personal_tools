#include <vector>
#include <iostream>

int main() {
  std::vector<int> a(10, 0);
  std::cout << "size=" << sizeof(a) << std::endl;

  return 0;
}