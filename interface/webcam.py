import cv2
import os
import streamlit as st
import numpy as np
import av

# function to save video frames to a file
def save_video(frames, width, height, output_path):
    # Create the output stream
    output_stream = av.open(output_path, "w")
    output_video_stream = output_stream.add_stream("libx264", rate=30)
    output_video_stream.width = width
    output_video_stream.height = height

    # Create the output container
    output_container = av.open(output_path, "r+")

    # Mux the frames into the container
    output_container.mux(output_video_stream, frames)

    # Get the absolute path of the saved video file
    video_file_path = os.path.abspath(output_path)

    return video_file_path

class VideoRecorder:
    def __init__(self):
        self.recording = False
        self.frame_count = 0
        self.frames = []
        self.path = os.environ.get("VIDEO_PATH")
        self.output_stream = None

    def recv(self, frame):
        if self.recording:
            self.frames.append(frame.to_ndarray(format="bgr24"))
            self.frame_count += 1

            # # Update the progress bar
            # st.progress_bar.progress(self.frame_count / 30)

            # # Write the frame to the output stream
            # self.output_stream.write(frame)

        return frame

    def start_recording(self):
        self.recording = True
        self.frame_count = 0
        self.frames = []

        # # Create a new output stream
        # self.output_stream = av.open(self.path, "w")

        # # Create a new video stream
        # self.video_stream = self.output_stream.add_stream("libx264", 30)

        # # Set the format and codec for the output video
        # self.video_stream.format = "mp4"
        # self.video_stream.codec = "h264"

    def stop_recording(self):
        self.recording = False
        video_file_path = None

        # # Close the output stream
        # self.output_stream.close()

        # if self.frame_count > 0:
        #     # Define the frame variable
        #     frame = self.frames[0]

        #     # Get the width and height of the frame
        #     width, height = frame.shape[:2]

        #     if os.path.isdir(self.path):
        #         output_video_name = os.path.join(self.path, "recorded_vid_stream.mp4")
        #     else:
        #         output_video_name = self.path

        #     # Save the recorded frames to a video file using the save_video function
        #     video_file_path = save_video(self.frames, width, height, output_video_name)

        #     # Reset the frames list
        #     self.frames = []

        #     return video_file_path
        if self.frame_count > 0:
            # Define the frame variable
            frame = self.frames[0]

            # Get the width and height of the frame
            width, height = frame.shape[:2]

            if os.path.isdir(self.path):
                output_video_name = os.path.join(self.path, "recorded_vid_stream.mp4")
            else:
                output_video_name = self.path

            # Save the recorded frames to a video file using OpenCV
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            out = cv2.VideoWriter(output_video_name, fourcc, 30, (width, height))
            video_frames = self.frames
            for frame in video_frames:
                out.write(frame)
            out.release()

            # Get the video file path
            video_file_path = os.path.abspath("recorded_vid_stream.mp4")

            # Reset the frames list
            self.frames = []

        return video_file_path
