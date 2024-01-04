#include <chrono>
#include <functional>
#include <iostream>
#include <thread>

#define __TIC__(tag) \
  auto __##tag##_start_time = std::chrono::high_resolution_clock::now();

#define __TOC__(tag)                                                           \
  auto __##tag##_end_time = std::chrono::high_resolution_clock::now();         \
  std::cout << #tag << " time cost: "                                          \
            << std::chrono::duration<double, std::micro>(__##tag##_end_time -  \
                                                         __##tag##_start_time) \
                   .count()                                                    \
            << "us" << std::endl;

using std::chrono::microseconds;
using std::chrono::milliseconds;
static const constexpr auto kTimerSpin = microseconds(100);

class FpsCounter {
 public:
  FpsCounter() { start_time_ = std::chrono::high_resolution_clock::now(); }
  void AddOne() { frame_count_++; };
  float Compute() {
    const auto time_now = std::chrono::high_resolution_clock::now();
    auto dur_ms = std::chrono::duration_cast<std::chrono::milliseconds>(
                      time_now - start_time_)
                      .count();
    if (0 == dur_ms) {
      return 0;
    }
    return static_cast<float>(frame_count_) / dur_ms * 1000;
  }
  size_t FrameCount() const { return frame_count_; }
  float Update(size_t frame_count,
               std::chrono::high_resolution_clock::time_point start_time) {
    auto fps = Compute();
    frame_count_ = frame_count;
    start_time_ = start_time;
    return fps;
  }

 private:
  std::chrono::high_resolution_clock::time_point start_time_;
  size_t frame_count_ = 0;
};

class FixIntervalTimer {
  using PGSteadyClock =
      std::conditional<std::chrono::high_resolution_clock::is_steady,
                       std::chrono::high_resolution_clock,
                       std::chrono::steady_clock>::type;

 public:
  FixIntervalTimer(const int& interval_ms) {
    now = PGSteadyClock::now();
    tick_interval = milliseconds(interval_ms);
    end = now + tick_interval;
    // std::cout << "begin: " <<
    // std::chrono::time_point_cast<std::chrono::milliseconds>(now).time_since_epoch().count()
    // << std::endl;
    fps.AddOne();
  }

  // void SetInterval(const int interval) { interval_ = interval; }
  // int GetInterval() const { return interval_; }
  ~FixIntervalTimer() {
    auto toc = PGSteadyClock::now();
    if (toc >= end) {
      return;
    }
    auto elapsed =
        std::chrono::duration_cast<std::chrono::microseconds>(toc - now);
    auto sleep_time = tick_interval - elapsed - kTimerSpin;
    std::cout << "need to sleep: " << sleep_time.count() << "us" << std::endl;
    std::this_thread::sleep_for(tick_interval - elapsed - kTimerSpin);
    // std::this_thread::sleep_for(end - toc - kTimerSpin);

    now = PGSteadyClock::now();
    while (now < end) {
      std::this_thread::yield();
      now = PGSteadyClock::now();
      std::cout << "FGQ" << std::endl;
    }
    // std::cout << "end: " <<
    // std::chrono::time_point_cast<std::chrono::milliseconds>(end).time_since_epoch().count()
    // << std::endl;
    std::cout << "FPS= " << fps.Compute() << std::endl;
  }

 private:
  std::chrono::milliseconds tick_interval;
  std::chrono::steady_clock::time_point now;
  std::chrono::steady_clock::time_point end;
  FpsCounter fps;
};

// int main() {

//   for (int i = 0; i < 100; i++) {
//     FixIntervalTimer a(50);
//     __TIC__(i)
//     std::this_thread::sleep_for(milliseconds(25));
//     __TOC__(i)
//   }
//   return 0;
// }

#include <chrono>
#include <iostream>
#include <thread>

int main() {
  using namespace std::chrono_literals;

  std::cout << "Hello waiter\n" << std::flush;

  const auto start = std::chrono::high_resolution_clock::now();
  std::this_thread::sleep_for(100ms);  //// 睡眠误差在3ms 左右
  const auto end = std::chrono::high_resolution_clock::now();
  const std::chrono::duration<double, std::milli> elapsed = end - start;
  std::cout << "Waited " << elapsed.count() << '\n';
}