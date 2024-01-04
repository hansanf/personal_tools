#include <string>
#include <utility>
#include <vector>
#include <cstdio>

/// @brief 以表格的形式规范输出
/// @param table 
void vv_report(std::vector<std::vector<std::string>>& table) {
  std::vector<size_t> col; // table每列的最大长度
  for (auto const& s : table)
    for (size_t i = 0; i < s.size(); ++i) {
      if (col.size() < i + 1)
        col.push_back(s[i].size());
      else
        col[i] = std::max(col[i], s[i].size());
    }

  std::string display;
  std::string hhead("\n┌");
  std::string hline("\n├");
  std::string htail("\n└");
  for (size_t i = 0; i < col.size(); ++i) {
    for (size_t k = -2; k != col[i]; ++k) {
      hhead += "─";
      hline += "─";
      htail += "─";
    }
    if (i != col.size() - 1) {
      hhead += "┬";
      hline += "┼";
      htail += "┴";
    } else {
      hhead += "┐\n";
      hline += "┤\n";
      htail += "┘\n";
    }
  }
  display += hhead;
  for (auto const& s : table) {
    display += "│";
    for (size_t i = 0; i < s.size(); ++i) {
      display += " ";
      if (i == 0) {
        display += s[i];
        display.resize(display.size() + col[i] - s[i].size(), ' ');
      } else {
        display.resize(display.size() + col[i] - s[i].size(), ' ');
        display += s[i];
      }
      display += " │";
    }
    for (size_t i = s.size(); i < col.size(); ++i) {
      display.resize(display.size() + col.size(), ' ');
      display += "  │";
    }
    if (s.begin() != table.back().begin()) display += hline;
  }
  display += htail;
  fputs(display.data(), stdout);
  fflush(stdout);
}

int main() {
  std::vector<std::vector<std::string>> table = {
      {"name", "age", "height"},
      {"f", "1", "2"},
      {"g", "10", "20"},
      {"Hank", "27", "176"}};
  vv_report(table);
/*
    ┌──────┬─────┬────────┐
    │ name │ age │ height │
    ├──────┼─────┼────────┤
    │ f    │   1 │      2 │
    ├──────┼─────┼────────┤
    │ g    │  10 │     20 │
    ├──────┼─────┼────────┤
    │ Hank │  27 │    176 │
    └──────┴─────┴────────┘
*/
  return 0;
}
