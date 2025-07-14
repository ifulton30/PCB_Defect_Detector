Developer: Phillip Le

# PCB Defect Detector
The following educational project will utilize OpenCV and PyTorch to interface with a Logitech C920 webcam for defect analysis on various
PCBs. I will be developing a CNN to detect various failure modes such as scratches, chipped edges, misalignment, and missing components.

# About the data
This section will be used to describe the data used in the model

# Figures
This section will contain all the metrics and demo images from learning over the duration of this project

# References
This section will list all the machine learning/computer vision techniques used along with the research papers studied to proceed with this project

[1] Zhu, X., Cheng, D., Zhang, Z., Lin, S., & Dai, J. (2019, April 11). An empirical study of spatial attention mechanisms in deep networks. arXiv.org. https://arxiv.org/abs/1904.05873

Webcam Capture API Backends:
https://docs.opencv.org/3.4/d4/d15/group__videoio__flags__base.html#gga023786be1ee68a9105bf2e48c700294dab6ac3effa04f41ed5470375c85a23504

List of all available VideoCapture properties that we can adjust:
https://docs.opencv.org/4.x/d4/d15/group__videoio__flags__base.html#gaeb8dd9c89c10a5c63c139bf7c4f5704d

After testing the different camera settings, I realized that I needed to be very careful with the setting the camera settings as they do not reset to default settings after releasing the capture.
These were the default settings on my Logitech C920 that I found through testing on a Jupyter notebook
BRIGHTNESS: Range [0.0, 255.0], Current: 128.0
CONTRAST: Range [0.0, 255.0], Current: 128.0
SATURATION: Range [0.0, 255.0], Current: 128.0
HUE: Not settable, Current: -1.0
GAIN: Range [0.0, 255.0], Current: 9.0
EXPOSURE: Range [-11.0, -2.0], Current: -5.0
WHITE_BALANCE: Not settable, Current: -1.0
FOCUS: Range [0.0, 250.0], Current: 0.0
SHARPNESS: Range [0.0, 255.0], Current: 128.0
