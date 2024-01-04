#include <net/if.h>
#include <sys/ioctl.h>
#include <unistd.h>

#include <fstream>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <vector>

std::string getMacAddress(const std::string& interface = "eth0") {
  std::ifstream file("/sys/class/net/" + interface + "/address");
  if (file) {
    std::string macAddress;
    std::getline(file, macAddress);
    return macAddress;
  }
  return "";
}

int main() {
  std::string interface = "eth0";  // 指定你想要获取MAC地址的网络接口名称
  std::string macAddress = getMacAddress(interface);
  if (!macAddress.empty()) {
    std::cout << "MAC Address of " << interface << ": " << macAddress
              << std::endl;
  } else {
    std::cout << "Failed to retrieve MAC Address of " << interface << std::endl;
  }
  return 0;
}
