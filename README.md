# Road Following in CoppeliaSim

This project simulates autonomous robot navigation using vision-based road following in a CoppeliaSim environment. Robots detect and follow a path using a vision sensor and a PID control loop. Python is used to control the simulation remotely via the ZMQ API.

---

## Project Structure

```plaintext
.
├── CoppeliaSimScene.ttt         # Simulation scene with robot models and road paths
├── constants.py                 # Configuration for resolution, PID gains, thresholds, and robot IDs
├── utils.py                     # Image acquisition, thresholding, and centroid detection
├── robot.py                     # Robot class with PID control and motion logic
└── main_controller.py           # Main script to start and run the simulation
```

---

## Requirements

- **CoppeliaSim Edu**
- **Python 3.x**

Install required libraries with:

```bash
pip install coppeliasim-zmqremoteapi-client opencv-python numpy
```

---

## Setup Instructions

1. Open `CoppeliaSimScene.ttt` in CoppeliaSim.
2. Run `main_controller.py` to start the simulation.
3. Robots will follow the predefined paths using vision-based control.

---

## How It Works

### Vision-Based Path Detection

Each robot captures images using an onboard vision sensor. The images are processed using OpenCV:

- Convert to grayscale
- Apply binary thresholding
- Detect the centroid of the road blob using image moments

### PID Control

The deviation between the desired path center and the detected centroid is used to compute:

```plaintext
error = desired_centroid - actual_centroid
```

A PID controller adjusts the motor speeds proportionally:

- **P**: Direct response to error
- **I**: Accumulates error over time
- **D**: Predicts future error

This results in smooth steering adjustments to keep the robot centered on the road.

---

## Highlights

- Modular Python code with clearly separated logic for control and vision
- Real-time control loop with simulation stepping
- Supports multiple robots simultaneously
- Visual debug output using OpenCV for tuning and testing

---

## References

- Correll et al. (2019). *Introduction to Autonomous Robots*
- Siciliano & Sciavicco (2010). *Robotics: Modelling, Planning and Control*
- Dudek & Jenkin (2000). *Computational Principles of Mobile Robotics*
