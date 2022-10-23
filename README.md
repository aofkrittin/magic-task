**Instruction**
- The file "magic.py" contains the class for running the solution for task A and B.
- If you run "magic.py", the IDE will assume that you are using "A.mp4" as an input.
- Run "B.py" for a result for video B.

**Assumptions**
- The camera spec is outputting 25 frames per second, as indicated in the video file.
- The variables min_threshold and max_threshold are assumed to be 35 and 55 respectively. This comes from a pure observation from the result produced by using the video A.mp4

**Reasoning**
- In this work, we use MediaPipe to determine the keypoint on a body, such as a shoulder, an elbow, a wrist, or a face, etc in order to count the number of waving motion a user is producing. 
- The waving motion is created by making an arcing motion with the arm, using the elbow as the pivotal joint and repeating the same motion in the opposite direction. 
- One complete motion is a downward arcing motion until the certain point and followed by an upward arcing motion, or vice versa. The motion can therefore be viewed as the amount of angle between two vectors, from the elbow to the wrist, and from the elbow to the shoulder, i.e. when the arm is moving up, the angle will be decreasing and finally reach the minimum threshold angle (counted as 50% completion), and when it is moving down, the angle will increase and arrive at the maximum threshold angle (counted as 100% completion). This process can be reversed, when the starting angle is the opposite.
- Applying MediaPipe solution, we can determine the positions of the keypoints and compute the two vectors. Then, we can use dot product to compute the angle between the two vectors.

**Extension**
