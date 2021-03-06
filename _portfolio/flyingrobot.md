---
title: "Autonomous Flying Robot"
excerpt: ---
date: 2018-09-10
tags:
  - px4
  - autopilot
  - uav
  - quadcopter
  - indoor-flight
  - pixhawk
  - ROS
  - robot
  - object detection
  - deep learning
  - YOLO
  - Movidius
collection: portfolio
---

This is the demonstration of autonomous quadrotor developed by me using [Robot Operating System (ROS)](http://www.ros.org/) and [Pixhawk Firmware](https://px4.io/).

This project was completed at the University of Cincinnati as a part of [Cooperative Distributed Systems Lab](https://ceas.uc.edu/research/centers-labs/cooperative-distributed-systems-lab.html). The objective of the project was to develop a robot to assist first responders in search and rescue missions in the post-disaster scenarios. The robot was designed and developed to fly in the cluttered indoor environment without GPS or any external positioning feedback.

For obstacle avoidance, laser sensors, as well as sonar sensors, were used. The robot was equipped with a camera to do object detection. For object detection, [YOLO](https://pjreddie.com/darknet/yolo/) was used.

Video Links:
* [Pixhawk for Quadcopter Waypoint Navigation using External Position Estimation](https://youtu.be/U_rrq_xeDkc)
<iframe width="560" height="315" src="https://www.youtube.com/embed/U_rrq_xeDkc" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

* [Pixhawk Quadrotor Test for Robustness to Disturbance](https://www.youtube.com/watch?v=qzLG4EuJ_VQ)
<iframe width="560" height="315" src="https://www.youtube.com/embed/qzLG4EuJ_VQ" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


<br>
<br>

References:

\[1\]. Redmon, J., Farhadi, A. (2018). Yolov3: An incremental improvement. arXiv preprint arXiv:1804.02767.

\[2\]. [Intel<sup>&reg;</sup> Movidius<sup>&trade;</sup> Neural Compute Stick](https://software.intel.com/en-us/neural-compute-stick)
