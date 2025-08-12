cmake_minimum_required(VERSION 3.8)
project(assessment_packages)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(assessment_interfaces REQUIRED)
find_package(tf2 REQUIRED)
find_package(tf2_geometry_msgs REQUIRED)

install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}/
)

add_executable(drive_distance src/drive_distance.cpp)
ament_target_dependencies(drive_distance rclcpp geometry_msgs nav_msgs assessment_interfaces)
install(TARGETS drive_distance DESTINATION lib/${PROJECT_NAME})

add_executable(rotate_angle src/rotate_angle.cpp)
ament_target_dependencies(rotate_angle rclcpp geometry_msgs nav_msgs tf2 tf2_geometry_msgs assessment_interfaces)
install(TARGETS rotate_angle DESTINATION lib/${PROJECT_NAME})


if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
