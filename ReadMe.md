### Robot arm control with PyGame

* The program uses PyGame as a controller program which communicates with V-REP Virtual Robot Experimentation platform.
* Serves as a Graphical mouse based control to move a target in Cartesian space.
* Commands are sent to V-REP simulation platform to change position of a target object.
* Robot arm is configured to reach the target object using inverse kinematics.



### Instructions to Run

1. After creating virtual-env and installing all dependencies from requirements.txt
2. Download V-REP and assign path to installation directory to vrep_dir variable in the "IK_Scaled.py"
3. Also to enable the V-rep python remote api and bindings put the  required 3 files in the "vrep_boilerplate" directory. 2 files are from  python bindings while the 3rd one is Operating system specific remote api library file.
4. Make sure the IK_Test_7DOF.ttt file is in same directory.
5. run the "IK_Scaled.py" file with python.



### Demo

![Robot Arm Control](media/output.gif "Demo")
