/***************************************************************
 * WARNING:
 * Do NOT modify this file.
 * Any changes may cause the system to fail or behave unexpectedly.
 * Your submission may be invalidated if this file is altered.
 ***************************************************************/
#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include "nav_msgs/msg/odometry.hpp"
#include "assessment_interfaces/srv/rotate_angle.hpp"
#include <tf2/LinearMath/Quaternion.h>
#include <tf2/LinearMath/Matrix3x3.h>
#include <cmath>

using std::placeholders::_1;
using std::placeholders::_2;

class RotateAngleServer : public rclcpp::Node
{
public:
    RotateAngleServer()
    : Node("drive_angle_server")
    {
        _cmd_vel_pub_node = rclcpp::Node::make_shared("angle_cmd_vel_pub_node");
        _odom_sub_node = rclcpp::Node::make_shared("angle_odom_sub_node");

        cmd_vel_pub_ = _cmd_vel_pub_node->create_publisher<geometry_msgs::msg::Twist>("cmd_vel", 10);
        odom_sub_ = _odom_sub_node->create_subscription<nav_msgs::msg::Odometry>("odom", 10,
                     std::bind(&RotateAngleServer::odom_callback, this, _1));

        service_ = this->create_service<assessment_interfaces::srv::RotateAngle>(
            "rotate_angle", std::bind(&RotateAngleServer::handle_service, this, _1, _2));

        current_yaw_ = 0.0;
        odom_ready_ = false;

        RCLCPP_INFO(this->get_logger(), "RotateAngle service ready.");
    }

private:
    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr cmd_vel_pub_;
    rclcpp::Subscription<nav_msgs::msg::Odometry>::SharedPtr odom_sub_;
    rclcpp::Service<assessment_interfaces::srv::RotateAngle>::SharedPtr service_;
    std::shared_ptr<rclcpp::Node> _cmd_vel_pub_node;
    std::shared_ptr<rclcpp::Node> _odom_sub_node;

    double current_yaw_;
    bool odom_ready_ = false;

    void odom_callback(const nav_msgs::msg::Odometry::SharedPtr msg)
    {
        current_yaw_ = get_yaw_from_quaternion(msg->pose.pose.orientation);
        odom_ready_ = true; 
    }

    double get_yaw_from_quaternion(const geometry_msgs::msg::Quaternion &q)
    {
        tf2::Quaternion quat(q.x, q.y, q.z, q.w);
        tf2::Matrix3x3 mat(quat);
        double roll, pitch, yaw;
        mat.getRPY(roll, pitch, yaw);
        return yaw;
    }

    void handle_service(
      const std::shared_ptr<assessment_interfaces::srv::RotateAngle::Request> request,
      std::shared_ptr<assessment_interfaces::srv::RotateAngle::Response> response)
    {
        while (!odom_ready_ && rclcpp::ok()) {
            rclcpp::spin_some(this->_odom_sub_node);
            RCLCPP_INFO(this->get_logger(), "Waiting for odometry...");
            rclcpp::sleep_for(std::chrono::milliseconds(100));
        }
    
        double initial_yaw = current_yaw_;
        double target_angle = request->angle;
        double max_speed = std::abs(request->max_rotation_speed);
    
        double direction = (target_angle >= 0.0) ? 1.0 : -1.0;
    
        RCLCPP_INFO(this->get_logger(), "Rotating %.2f radians at max speed %.2f rad/s", target_angle, max_speed);
    
        geometry_msgs::msg::Twist cmd_vel;
        cmd_vel.angular.z = direction * max_speed;
    
    
        while (rclcpp::ok()) {
            rclcpp::spin_some(this->_odom_sub_node);
    
            double delta_yaw = current_yaw_ - initial_yaw;
    
            while (delta_yaw > M_PI) delta_yaw -= 2 * M_PI;
            while (delta_yaw < -M_PI) delta_yaw += 2 * M_PI;
    
            if (std::abs(delta_yaw) >= std::abs(target_angle)) {
                break;
            }
            cmd_vel_pub_->publish(cmd_vel);
        }
    
        // Stop the robot after rotation
        cmd_vel.angular.z = 0.0;
        cmd_vel.linear.x = 0.0;
        cmd_vel_pub_->publish(cmd_vel);
    
        RCLCPP_INFO(this->get_logger(), "Rotation complete. Final yaw: %.2f radians", current_yaw_);
    
        response->success = true;
    }
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    std::shared_ptr<RotateAngleServer> drive_angle_node = std::make_shared<RotateAngleServer>();
    if (rclcpp::ok())
    {
        rclcpp::spin(drive_angle_node);
    }
    rclcpp::shutdown();
    return 0;
}
