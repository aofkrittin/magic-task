**File description**
- A.mp4: Video of a person waving 5 times at a fairly consistent speed, to be converted into Pose estimation data and used as the basis of a waving pattern
- B.mp4: Video of a person waving 10 times at inconsistent speeds, to be analysed and fed into an algorithm that counts the number of waves in real-time
- magic.py: Code containing the class for running the solution for task A and B.
- B.py: Code for running the task B.
- requirements.txt: Necessary python packages for running the task.
- Magic_Tech__CV_ML_Engineer_Test.pdf: Instruction for the take-home task.

**Instruction**
- The file "magic.py" contains the class for running the solution for task A and B.
- If you run "magic.py", the IDE will assume that you are using "A.mp4" as an input.
- Run "B.py" for a result for video B.

**Assumptions**
- The camera spec is outputting 25 frames per second, as indicated in the video file.
- The variables min_threshold and max_threshold are assumed to be 35 and 55 respectively. This comes from a pure observation from the result produced by using the video A.mp4.

**Reasoning**
- In this work, we use MediaPipe to determine the keypoint on a body, such as a shoulder, an elbow, a wrist, or a face, etc in order to count the number of waving motion a user is producing. 
- The waving motion is created by making an arcing motion with the arm, using the elbow as the pivotal joint and repeating the same motion in the opposite direction. 
- One complete motion is a downward arcing motion until the certain point and followed by an upward arcing motion, or vice versa. The motion can therefore be viewed as the amount of angle between two vectors, from the elbow to the wrist, and from the elbow to the shoulder, i.e. when the arm is moving up, the angle will be decreasing and finally reach the minimum threshold angle (counted as 50% completion), and when it is moving down, the angle will increase and arrive at the maximum threshold angle (counted as 100% completion). This process can be reversed, when the starting angle is the opposite.
- Applying MediaPipe solution, we can determine the positions of the keypoints and compute the two vectors. Then, we can use dot product to compute the angle between the two vectors.

**Possible extension**
- The work can be extended to apply to various exercise movements, if the keypoints of which are important to the movement, are indicated. For example, a  push up movement can be viewed as an angle between the same two vectors and also how the lines connecting from the feet to shoulders are.
- Furthermore, as every user will have different body types, a specific exercise motion as detected by MediaPipe cannot be achieved in the same way as the other users'. To make the program more generalisable, some certain machine learning technique such as neural network can be applied to learn the proper way of exercising for different body types (which will require a lot of parameters).
