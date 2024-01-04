cmake_minimum_required(VERSION 3.14)

include(cmake/CPM.cmake)
project(personal_cpp_tools)

OPTION(USE_TABLE_REPORT "whether to compile table_report.cpp" OFF)
OPTION(USE_COROUTINE "whether to complie coroutine directory" OFF)

set(CMAKE_CXX_STANDARD "14")
set(CMAKE_CXX_FLAGS_DEBUG "-fPIC -O0 -g -Wall")



if(USE_TABLE_REPORT)
  message(STATUS "To compile table_report.cpp")
  add_executable(table_report table_report.cpp)
  install(TARGETS table_report
          RUNTIME DESTINATION bin)
endif()