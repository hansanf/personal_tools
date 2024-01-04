#include <string>
#include <regex>
#include <vector>
#include <iostream>
/*
  c++11 开始支持regex
*/

int main () {
  // std::string s = "Quick brown fox.";
  std::string s = "a.txt,b.txt,c.txt";
  // std::regex delimiter("\\s+"); // whitespace
  std::regex delimiter(",");
  // std::vector<std::string> result;

  // std::copy(std::sregex_token_iterator(s.begin(), s.end(), delimiter, -1),
  //           std::sregex_token_iterator(),
  //           std::back_inserter(result));

  std::vector<std::string> result(
      std::sregex_token_iterator(s.begin(), s.end(), delimiter, -1),
      std::sregex_token_iterator());

  for(auto x : result) {
    std::cout << x << std::endl;
  }
  return 0;
}