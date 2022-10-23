#!/usr/bin/env python3

from array import array
import cv2
import mediapipe as mp
import numpy as np
import matplotlib.pyplot as plt

class magicmodel():

    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_style = mp.solutions.drawing_styles
    mp_pose = mp.solutions.pose

    starting_flag = True
    starting_theta = 0
    n_wave = 0
    halfwave_flag = False
    current_completion = 0
    image_height = 0
    image_width = 0
    
    def __init__(self, input_video, min_threshold, max_threshold, fps=25):
        self.video = cv2.VideoCapture(input_video)
        self.min_threshold = min_threshold
        self.max_threshold = max_threshold
        self.fps = fps


    def wave(self, landmark, time=0):
        """
        landmark = dictionary for two 2D Lists 'x' and 'y' landmark
        overtime = ending time for the video (s)
        """

        X_shoulder = landmark[12].x * self.image_width
        X_elbow = landmark[14].x * self.image_width
        X_wrist = landmark[16].x * self.image_width

        Y_shoulder = landmark[12].y * self.image_height
        Y_elbow = landmark[14].y * self.image_height
        Y_wrist = landmark[16].y * self.image_height

        v1 = np.array([X_shoulder - X_elbow, Y_shoulder - Y_elbow])
        v2 = np.array([X_wrist - X_elbow, Y_wrist - Y_elbow])

        #Calculate dot product
        dot_product = np.dot(v1, v2)

        #Determine the angle between the two vectors
        current_angle = dot_product/(np.linalg.norm(v1) * np.linalg.norm(v2)) * 180/np.pi


        if (self.starting_flag):
            self.starting_theta = current_angle
            self.starting_flag = False

        #A case when the arm is curled up when start
        if (np.linalg.norm(self.min_threshold - self.starting_theta) > np.linalg.norm(self.max_threshold - self.starting_theta)):

            if (self.halfwave_flag):
                self.current_completion = abs(current_angle - self.min_threshold)/(self.max_threshold - self.min_threshold) * 50 + 50
            else:
                self.current_completion = abs(current_angle - self.max_threshold)/(self.max_threshold - self.min_threshold) * 50

            if (current_angle < self.min_threshold):
                self.halfwave_flag = True
                self.current_completion = 50.0
            elif (current_angle > self.max_threshold) and (not self.halfwave_flag):
                self.current_completion = 0.0
            elif (current_angle > self.max_threshold) and (self.halfwave_flag):
                self.halfwave_flag = False
                self.n_wave = self.n_wave + 1
                self.current_completion = 0

        #A case when the arm is extended when start
        else:

            if (not self.halfwave_flag):
                self.current_completion = abs(current_angle - self.min_threshold)/(self.max_threshold - self.min_threshold) * 50 + 50
            else:
                self.current_completion = abs(current_angle - self.max_threshold)/(self.max_threshold - self.min_threshold) * 50

            if (current_angle > self.max_threshold):
                self.halfwave_flag = True
                self.current_completion = 50.0
            elif (current_angle < self.min_threshold) and (not self.halfwave_flag):
                self.current_completion = 0.0
            elif (current_angle < self.min_threshold) and (self.halfwave_flag):
                self.halfwave_flag = False
                self.n_wave = self.n_wave + 1
                self.current_completion = 0

        print("The current pose is shown at " + str(time) + "seconds")

        return self.current_completion, self.n_wave


    def count_wave(self, plot=False):
        
        success_flag, image = self.video.read()

        cc = 1

        with self.mp_pose.Pose(min_detection_confidence=0.5,
                    min_tracking_confidence=0.5) as pose:

            while success_flag:

                results = pose.process(image)
                
                self.image_height, self.image_width, _ = image.shape

                image.flags.writeable = True
                
                if (plot):
                    self.mp_drawing.draw_landmarks(image, 
                    results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec = self.mp_drawing_style.get_default_pose_landmarks_style())

                    cv2.imshow("MediaPipe result", cv2.flip(image, 1))

                    if cv2.waitKey(5) & 0xFF == 27:
                        break

                keypoints_array = results.pose_landmarks.landmark

                percent_completion, wave_count = self.wave(keypoints_array, time=cc/self.fps)

                print("percent completion of the current wave: ", percent_completion, " percent")
                print("the number of waves: ", wave_count)

                cc = cc + 1
                success_flag, image = self.video.read()



if __name__ == "__main__":
    magic = magicmodel(input_video="A.mp4", min_threshold = 35, max_threshold = 55)
    magic.count_wave(plot=False)