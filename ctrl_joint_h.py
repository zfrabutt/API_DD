#!/usr/bin/env python3
#Modified Given Code
import rospy
import socket
from gazebo_msgs.srv import ApplyJointEffort
from gazebo_msgs.srv import GetJointProperties
from std_msgs.msg import Header


def setRot(pub, val, direction):
    buff = ApplyJointEffort()
    buff.effort = val

    start_time = rospy.Time(0,0)
    end_time = rospy.Time(0.01,0)
    if direction == "l":
        buff.joint_name = "dd_robot::left_wheel_hinge"
        pub(buff.joint_name,  buff.effort, start_time, end_time)
    if direction == "r":
        buff.joint_name = "dd_robot::right_wheel_hinge"
        pub(buff.joint_name, -buff.effort, start_time, end_time)


def getPos(pub):
    buff = GetJointProperties()
    buff.joint_name = 'dd_robot::left_wheel_hinge'

    val = pub(buff.joint_name)
    leftw = val.rate[0]
    buff.joint_name = 'dd_robot::right_wheel_hinge'
    val = pub(buff.joint_name)
    rightw = val.rate[0]
    v = (leftw, rightw)
    return v


def talker(val, direction):
    rospy.init_node('dd_ctrl', anonymous=True)
    pub    = rospy.ServiceProxy('/gazebo/apply_joint_effort',ApplyJointEffort)
    pubget = rospy.ServiceProxy('/gazebo/get_joint_properties',GetJointProperties)
    rate = rospy.Rate(10) # 10hz

    setRot(pub, val, direction)
    v = getPos(pubget)
    buff = str(v[0]) + " " + str(v[1])+
    print(v)
    rate.sleep()

if __name__ == '__main__':
    try:
        UDP_IP = '127.0.0.1'
        UDP_PORT = 5005
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((UDP_IP, UDP_PORT))

        while True:                
            data, addr = sock.recvfrom(1024)
            s = data.split(" ")
            talker(int(s[0]), s[1])
            

    except rospy.ROSInterruptException:
        pass
