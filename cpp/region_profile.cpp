#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <cmath>
#include <algorithm>
#include <syscall.h>
#include <unistd.h>
#include <sstream>

using namespace std;

namespace phigent {
namespace _profile {

inline double now_ms() {
  timespec ts;
  clock_gettime(CLOCK_MONOTONIC, &ts);
  return 1e+3 * static_cast<double>(ts.tv_sec) +
         1e-6 * static_cast<double>(ts.tv_nsec);
}

template<typename T>
std::string toString(std::vector<T>& vec) {
  std::ostringstream oss;
  for (auto num : vec) {
    oss << num << ", ";
  }
  std::string str = oss.str(); // str: "1234"
}

struct Summary {
  struct Entry {
    int line, count;
    long tid;
    double sx1, sx1err;
    double sx2, sx2err;
    std::string file, func, name;
    std::vector<float> nums;
  };

  int cur_level, cur_index, warm_up;
  pthread_mutex_t lock;
  std::vector<Entry> elem;

  Summary();
  ~Summary();
  int id(int line, std::string file, std::string func, std::string name);
  void add(int level, int id, double val);
  std::string to_csv();
  std::string to_tab();
};


Summary::Summary() : cur_level(0), cur_index(0), warm_up(16) {
  pthread_mutex_init(&lock, NULL);
  char const* slevel = getenv("PPERF_LEVEL");
  if (slevel) cur_level = atoi(slevel);
  char const* swarm = getenv("PPERF_WARM");
  if (swarm) warm_up = atoi(swarm);
}

Summary::~Summary() {
  string csv = to_csv();
  string tab = to_tab();
  std::cout << "~Summary()" << std::endl;
  std::cout << csv << std::endl;
  std::cout << tab << std::endl;
  // if (csv.size()) dumpFile("dcv_profile.csv", csv.data(), csv.size());
  // if (tab.size()) fputs(tab.data(), stdout);
  pthread_mutex_destroy(&lock);
}

int Summary::id(int line, std::string file, std::string func,
                std::string name) {
  int id = -1;
  pthread_mutex_lock(&lock);
  if (cur_index < 1024) {
    id = cur_index++;
    Entry e{line, 0, 0, 0, 0, 0, 0, file, func, name, {}};
    e.nums.reserve(2048);
    e.tid = syscall(SYS_gettid);
    elem.push_back(std::move(e));
  } else
    // LogWarn(
    //     format("discard entry `{}' in file `{:s}' function `{:s}' line {:d}\n",
    //            name, file, func, line));
  pthread_mutex_unlock(&lock);
  return id;
}

void Summary::add(int level, int id, double val) {
  std::cout << "PPERF_LEVEL=" << cur_level << std::endl;
  std::cout << "level=" << level << std::endl;
  std::cout << "val=" << val << std::endl;

  if (level <= cur_level) {
    pthread_mutex_lock(&lock);
    if (static_cast<unsigned>(id) < static_cast<unsigned>(cur_index)) {
      auto& e = elem[id];
      if (e.count < 16384) {
        if (++(e.count) > warm_up) {
          e.sx1 += val;
          e.sx2 += val * val;
          // kahan(e.sx1, e.sx1err, val);
          // kahan(e.sx2, e.sx2err, val * val);
          e.nums.push_back(static_cast<float>(val));
        }
      }
    }
    pthread_mutex_unlock(&lock);
  }
}

std::string Summary::to_csv() {
  string d;
  char info[1024];
  pthread_mutex_lock(&lock);
  for (int i = 0; i < cur_index; ++i) {
    Entry& e = elem[i];
    int n = e.count - warm_up;
    if (n <= 0) continue;
    double var = (e.sx2 - e.sx1 * e.sx1 / n) / n;
    snprintf(info, sizeof(info), "\"%s\",%ld,%d,%f,%f,\"%s\",\"%s\",%d,\"",
             e.name.data(), e.tid, n, e.sx1 / n, sqrt(var), e.file.data(),
             e.func.data(), e.line);
    d += info;
    d += toString(e.nums);
    std::cout << d << std::endl;
    d += "\"\n";
  }
  pthread_mutex_unlock(&lock);
  if (d.size()) d = "name,tid,len,mean,std,file,func,line,statistic\n" + d;
  return d;
}

std::string Summary::to_tab() {
  string d;
  char info[1024];
  vector<int> argidx;
  vector<string> line;
  line.push_back("name,tid,len,mean,std,min,max,50%,90%,");
  pthread_mutex_lock(&lock);
  for (int i = 0; i < cur_index; ++i) argidx.push_back(i);
  sort(argidx.begin(), argidx.end(),
       [this](int i, int k) { return elem[i].name < elem[k].name; });
  for (int i : argidx) {
    Entry& e = elem[i];
    int n = e.count - warm_up;
    float* p = e.nums.data();
    if (n <= 0) continue;
    double var = (e.sx2 - e.sx1 * e.sx1 / n) / n;
    sort(e.nums.begin(), e.nums.end());
    snprintf(info, sizeof(info), "%s,%ld,%d,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,",
             e.name.data(), e.tid, n, e.sx1 / n, sqrt(var), p[0], p[n - 1],
             p[n / 2], p[min((n * 9 + 5) / 10, n - 1)]);
    line.push_back(info);
  }
  std::cout << "FGQ:" << toString(line) << std::endl;
  pthread_mutex_unlock(&lock);
  if (line.size() < 2) return d;

  vector<int> col;
  for (string const& l : line) {
    int n = static_cast<int>(l.size());
    int p = 0, c = 0;
    for (int q = 0; q < n; ++q) {
      if (l[q] != ',') continue;
      if (c < static_cast<int>(col.size()))
        col[c] = max(col[c], q - p);
      else
        col.push_back(q - p);
      ++c;
      p = q + 1;
    }
  }
  string hhead("\n┌");
  string hline("\n├");
  string htail("\n└");
  for (size_t i = 0; i < col.size(); ++i) {
    for (int k = -2; k != col[i]; ++k) {
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
  d.swap(hhead);
  for (string const& l : line) {
    int p = 0, c = 0;
    int n = static_cast<int>(l.size());
    d += "│";
    for (int q = 0; q < n; ++q) {
      if (l[q] != ',') continue;
      int k = q - p;
      d += " ";
      if (c == 0) {
        d.append(l.data() + p, k);
        d.resize(d.size() + col[c] - k, ' ');
      } else {
        d.resize(d.size() + col[c] - k, ' ');
        d.append(l.data() + p, k);
      }
      ++c;
      p = q + 1;
      d += " │";
    }
    if (l.begin() != line.back().begin()) d += hline;
  }
  d += htail;
  return d;
}

Summary Summary_Global;

struct ProfileRegion {
  int id, level;
  double t;
  ~ProfileRegion() { Summary_Global.add(level, id, now_ms() - t); }
};
}  // namespace _profile
}

#if 1

#define CVAUX_CONCAT_EXP(a, b) a##b
#define CVAUX_CONCAT(a, b) CVAUX_CONCAT_EXP(a,b)
#define PROFILE_FN_RESET(tag) \
  CVAUX_CONCAT(_profile_id_, tag) = phigent::_profile::now_ms()

#define PROFILE_FN_DEF(tag)                                   \
  static thread_local double CVAUX_CONCAT(_profile_id_, tag); \
  PROFILE_FN_RESET(tag)

#define PROFILE_FN_STEP(tag, level, name)                               \
  static thread_local int CVAUX_CONCAT(CVAUX_CONCAT(_profile_id_, tag), \
                                       __LINE__) =                      \
      phigent::_profile::Summary_Global.id(__LINE__, __FILE__,          \
                                           __PRETTY_FUNCTION__, name);  \
  phigent::_profile::Summary_Global.add(                                \
      level, CVAUX_CONCAT(CVAUX_CONCAT(_profile_id_, tag), __LINE__),   \
      phigent::_profile::now_ms() - CVAUX_CONCAT(_profile_id_, tag))

#define PROFILE_FN_RING(tag, level, name) \
  PROFILE_FN_STEP(tag, level, name);      \
  PROFILE_FN_RESET(tag)

#define PROFILE_REGION(level, name)                                          \
  static thread_local int CVAUX_CONCAT(_profile_id_, __LINE__) =             \
      phigent::_profile::Summary_Global.id(__LINE__, __FILE__,               \
                                           __PRETTY_FUNCTION__, name);       \
  phigent::_profile::ProfileRegion CVAUX_CONCAT(_PROFILE_FUNCTION_,          \
                                                __LINE__) {                  \
    CVAUX_CONCAT(_profile_id_, __LINE__), level, phigent::_profile::now_ms() \
  }

#define PROFILE_FN_VAL(level, name, val)                               \
  static thread_local int CVAUX_CONCAT(_profile_id_, __LINE__) =       \
      phigent::_profile::Summary_Global.id(__LINE__, __FILE__,         \
                                           __PRETTY_FUNCTION__, name); \
  phigent::_profile::Summary_Global.add(                               \
      level, CVAUX_CONCAT(_profile_id_, __LINE__), val)

#define PROFILE_DISABLE                                                  \
  __atomic_store_n(&(phigent::_profile::Summary::global().cur_level), 0, \
                   __ATOMIC_SEQ_CST)

#else

#define PROFILE_FN_RESET(tag)
#define PROFILE_FN_DEF(tag)
#define PROFILE_FN_STEP(tag, level, name)
#define PROFILE_FN_RING(tag, level, name)
#define PROFILE_REGION(level, name)
#define PROFILE_FN_VAL(level, name, val)
#define PROFILE_DISABLE

#endif

void func() {
  PROFILE_REGION(1, "FUNC");
  std::cout << "in func" << std::endl;
  return;
}

int main () {
  func();
  return 0;
}