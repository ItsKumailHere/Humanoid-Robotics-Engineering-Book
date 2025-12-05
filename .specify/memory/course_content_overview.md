# Physical AI & Humanoid Robotics Course Synopsis

## Core Concept
Bridge digital AI to physical robotics through embodied intelligence—AI systems understanding and operating in physical reality.

## Four Core Modules

**Module 1: ROS 2 (Robotic Nervous System)**
- Middleware for robot control: nodes, topics, services
- Python-ROS integration via rclpy
- URDF for humanoid robot description

**Module 2: Digital Twin (Gazebo & Unity)**
- Physics simulation: gravity, collisions
- High-fidelity rendering, human-robot interaction
- Sensor simulation: LiDAR, depth cameras, IMUs

**Module 3: NVIDIA Isaac™ (AI-Robot Brain)**
- Isaac Sim: photorealistic simulation, synthetic data
- Isaac ROS: hardware-accelerated VSLAM, navigation
- Nav2: bipedal path planning

**Module 4: Vision-Language-Action (VLA)**
- Voice-to-action via OpenAI Whisper
- LLM cognitive planning (natural language → ROS 2 actions)
- Capstone: autonomous humanoid executing voice commands

## 13-Week Timeline
- **Weeks 1-2:** Physical AI foundations, sensors
- **Weeks 3-5:** ROS 2 architecture, Python packages
- **Weeks 6-7:** Gazebo/Unity simulation, URDF/SDF
- **Weeks 8-10:** NVIDIA Isaac SDK, RL, sim-to-real
- **Weeks 11-12:** Humanoid kinematics, locomotion, manipulation
- **Week 13:** GPT integration, conversational robotics

## Assessments
ROS 2 package | Gazebo simulation | Isaac perception pipeline | Capstone: simulated conversational humanoid

## Hardware Requirements

**Essential Workstation (per student):**
- GPU: NVIDIA RTX 4070 Ti+ (12GB+ VRAM)
- CPU: Intel i7 13th Gen+ / AMD Ryzen 9
- RAM: 64GB DDR5 (32GB minimum)
- OS: Ubuntu 22.04 LTS

**Edge AI Kit:**
- Jetson Orin Nano/NX (8-16GB)
- Intel RealSense D435i (vision)
- USB IMU, microphone/speaker

**Robot Options:**
- Budget: Unitree Go2 ($1,800-$3,000)
- Humanoid: Unitree G1 (~$16k) or Hiwonder TonyPi (~$600)
- Premium: Unitree G1 for full sim-to-real

**Economy Student Kit (~$700):**
Jetson Orin Nano Super ($249) + RealSense D435i ($349) + ReSpeaker Mic ($69) + accessories ($30)

**Cloud Alternative:**
AWS g5.2xlarge (~$205/quarter) + local Jetson kit ($700) + robot ($3,000)