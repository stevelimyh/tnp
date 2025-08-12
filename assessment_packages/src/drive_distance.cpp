/***************************************************************
 * WARNING:
 * Do NOT modify this file.
 * Any changes may cause the system to fail or behave unexpectedly.
 * Your submission may be invalidated if this file is altered.
 ***************************************************************/
#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include "nav_msgs/msg/odometry.hpp"
#include "assessment_interfaces/srv/drive_distance.hpp"

#include <cmath>

using std::placeholders::_1;
using std::placeholders::_2;

class DriveDistanceServer : public rclcpp::Node
{
public:
    DriveDistanceServer()
    : Node("drive_distance_server")
    {
        _cmd_vel_pub_node = rclcpp::Node::make_shared("distance_cmd_vel_pub_node");
        _odom_sub_node = rclcpp::Node::make_shared("distance_odom_sub_node");

        cmd_vel_pub_ = _cmd_vel_pub_node->create_publisher<geometry_msgs::msg::Twist>("cmd_vel", 10);
        odom_sub_ = _odom_sub_node->create_subscription<nav_msgs::msg::Odometry>("odom", 10,
                     std::bind(&DriveDistanceServer::odom_callback, this, _1));

        service_ = this->create_service<assessment_interfaces::srv::DriveDistance>(
            "drive_distance", std::bind(&DriveDistanceServer::handle_service, this, _1, _2));

        current_x_ = 0.0;
        current_y_ = 0.0;
        initial_x_ = 0.0;
        initial_y_ = 0.0;
        odom_ready_ = false;

        RCLCPP_INFO(this->get_logger(), "DriveDistance service ready.");
    }

private:
    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr cmd_vel_pub_;
    rclcpp::Subscription<nav_msgs::msg::Odometry>::SharedPtr odom_sub_;
    rclcpp::Service<assessment_interfaces::srv::DriveDistance>::SharedPtr service_;
    std::shared_ptr<rclcpp::Node> _cmd_vel_pub_node;
    std::shared_ptr<rclcpp::Node> _odom_sub_node;

    double current_x_, current_y_;
    double initial_x_, initial_y_;
    bool odom_ready_ = false;

    void odom_callback(const nav_msgs::msg::Odometry::SharedPtr msg)
    {
        current_x_ = msg->pose.pose.position.x;
        current_y_ = msg->pose.pose.position.y;
        odom_ready_ = true;
    }

    void handle_service(
        const std::shared_ptr<assessment_interfaces::srv::DriveDistance::Request> request,
        std::shared_ptr<assessment_interfaces::srv::DriveDistance::Response> response)
    {
        while (!odom_ready_ && rclcpp::ok()) {
            rclcpp::spin_some(this->_odom_sub_node);
            RCLCPP_INFO(this->get_logger(), "Waiting for odometry...");
            rclcpp::sleep_for(std::chrono::milliseconds(100));
        }

        initial_x_ = current_x_;
        initial_y_ = current_y_;

        RCLCPP_INFO(this->get_logger(), "Driving straight for %.2f meters...", request->distance);

        geometry_msgs::msg::Twist cmd_vel;
        cmd_vel.linear.x = request->max_translation_speed;  // m/s

        while (rclcpp::ok()) {
            double dx = current_x_ - initial_x_;
            double dy = current_y_ - initial_y_;
            double distance = std::sqrt(dx * dx + dy * dy);

            if (distance >= request->distance) {
                break;
            }

            cmd_vel_pub_->publish(cmd_vel);
            rclcpp::spin_some(this->_cmd_vel_pub_node);
            rclcpp::spin_some(this->_odom_sub_node);
        }

        // Stop the robot
        cmd_vel.linear.x = 0.0;
        cmd_vel_pub_->publish(cmd_vel);
        RCLCPP_INFO(this->get_logger(), "Target distance reached. Stopping.");

        response->success = true;
    }
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    std::shared_ptr<DriveDistanceServer> drive_distance_node = std::make_shared<DriveDistanceServer>();
    if (rclcpp::ok())
    {
        rclcpp::spin(drive_distance_node);
    }
    rclcpp::shutdown();
    return 0;
}
