#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import tkinter as tk
from threading import Thread

class TeleopControlsGUI(Node):
    def __init__(self):
        super().__init__('teleop_controls_gui')
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.vel_msg = Twist()
        
        # Initialize speeds
        self.linear_speed = 1.0  # m/s
        self.angular_speed = 1.0  # rad/s
        
        # Create the main window
        self.root = tk.Tk()
        self.root.title("Robot Teleop")
        
        # Create speed control frame
        speed_frame = tk.Frame(self.root)
        speed_frame.pack(pady=10)
        
        # Linear speed control
        tk.Label(speed_frame, text="Linear Speed:").pack()
        self.linear_scale = tk.Scale(speed_frame, from_=-10.0, to=10.0, resolution=1.0, orient=tk.HORIZONTAL, length=300)
        self.linear_scale.set(self.linear_speed)
        self.linear_scale.pack()
        
        # Angular speed control
        tk.Label(speed_frame, text="Angular Speed:").pack()
        self.angular_scale = tk.Scale(speed_frame, from_=0.0, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, length=300)
        self.angular_scale.set(self.angular_speed)
        self.angular_scale.pack()
        
        # Status label
        self.status_label = tk.Label(self.root, text="Use keyboard arrow keys to control the robot")
        self.status_label.pack(pady=10)
        
        # Bind keyboard events
        self.root.bind('<KeyPress>', self.on_press)
        self.root.bind('<KeyRelease>', self.on_release)
        
        # Initialize movement flags
        self.moving_forward = False
        self.moving_backward = False
        self.turning_left = False
        self.turning_right = False
        
        # Initialize Twist message
        self.vel_msg.linear.x = 0.0
        self.vel_msg.linear.y = 0.0
        self.vel_msg.linear.z = 0.0
        self.vel_msg.angular.x = 0.0
        self.vel_msg.angular.y = 0.0
        self.vel_msg.angular.z = 0.0
        
        # Start the update loop
        self.update_movement()

    def on_press(self, event):
        if event.keysym == 'Up':
            self.moving_forward = True
            self.status_label.config(text="Moving Forward")
        elif event.keysym == 'Down':
            self.moving_backward = True
            self.status_label.config(text="Moving Backward")
        elif event.keysym == 'Left':
            self.turning_left = True
            self.status_label.config(text="Turning Left")
        elif event.keysym == 'Right':
            self.turning_right = True
            self.status_label.config(text="Turning Right")

    def on_release(self, event):
        if event.keysym == 'Up':
            self.moving_forward = False
        elif event.keysym == 'Down':
            self.moving_backward = False
        elif event.keysym == 'Left':
            self.turning_left = False
        elif event.keysym == 'Right':
            self.turning_right = False
            
        if not any([self.moving_forward, self.moving_backward, 
                   self.turning_left, self.turning_right]):
            self.vel_msg.linear.x = 0.0
            self.vel_msg.angular.z = 0.0
            self.publisher.publish(self.vel_msg)
            self.status_label.config(text="Stopped")

    def update_movement(self):
        try:
            if self.moving_forward:
                self.vel_msg.linear.x = float(self.linear_scale.get())
            elif self.moving_backward:
                self.vel_msg.linear.x = -float(self.linear_scale.get())
            else:
                self.vel_msg.linear.x = 0.0
                
            if self.turning_left:
                self.vel_msg.angular.z = float(self.angular_scale.get())
            elif self.turning_right:
                self.vel_msg.angular.z = -float(self.angular_scale.get())
            else:
                self.vel_msg.angular.z = 0.0
                
            # Ensure other values are explicitly set to 0.0
            self.vel_msg.linear.y = 0.0
            self.vel_msg.linear.z = 0.0
            self.vel_msg.angular.x = 0.0
            self.vel_msg.angular.y = 0.0
            
            self.publisher.publish(self.vel_msg)
            
        except (ValueError, TypeError) as e:
            self.get_logger().error(f'Error in update_movement: {str(e)}')
            
        self.root.after(100, self.update_movement)

def main():
    rclpy.init()
    node = TeleopControlsGUI()
    
    # Create a separate thread for the ROS spin
    spin_thread = Thread(target=rclpy.spin, args=(node,))
    spin_thread.start()
    
    try:
        node.root.mainloop()
    finally:
        node.destroy_node()
        rclpy.shutdown()
        spin_thread.join()

if __name__ == '__main__':
    main()