import cv2
import numpy as np


class WebcamPCBCapture:
    """Webcam capture system optimized for PCB Imaging"""

    def __init__(self, camera_id = 0, resolution = (1920, 1080)):
        self.camera_id = camera_id
        self.resolution = resolution
        self.cap = None
        self.is_initialized = False

        # I will be utilizing these camera settings to adjust for optimal PCB inspection settings
        self.camera_settings = {
            'brightness': 128, # Middle range
            'contrast': 130,
            'hue': 0,
            'gain': 64,
            'exposure': -6,
            'white_balance': 4600,
            'focus': 0,
            'sharpness': 130
        }

        # Calls initialize_camera to start up the webcam, but does not show frames yet
        self.initialize_camera()

    def initialize_camera(self):
        """Initializing camera for PCB imaging using MSMF backend"""
        try:
            # This opens the camera while enforcing the MSMF backend which is a Capture API backend.
            self.cap = cv2.VideoCapture(self.camera_id, cv2.CAP_MSMF)

            # Fallback to default Capture API backend 
            if not self.cap.isOpened():
                self.cap = cv2.VideoCapture(self.camera_id)

            # Raising an error if neither backends can be used and camera can't be opened
            if not self.cap.isOpened():
                raise Exception(f"Cannot open camera {self.camera_id}")
            
            # Setting the resolution of the camera. The Logitech C920 shoots up to 1920x1080
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
            
            # Setting the camera settings defined when instantiating the WebcamPCBCapture object
            self.apply_camera_settings()

            # Successful initialization message which also prints the actual resolution of camera at startup
            self.is_initialized = True
            print(f"Camera initialized successfully at resolution: {self.get_actual_resolution}")

        except Exception as e:
            print(f"Error initializing camera: {e}")
            self.is_initialized = False

    def apply_camera_settings(self):
        """
        This function is used to apply the camera settings which were defined in 
        the constructor and initialize_camera functions
        """

        # Checking to make sure that the camera is open
        if not self.cap:
            print("Camera is not initialized so we cannot apply camera settings")
            return

class PCBTestingSession:
    """Testing manager for PCB Defect Detection"""

    def __init__(self, model, config, output_dir="test_results"):
        self.model = model
        self.config = config
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok = True)

    # Initializing the webcam by instantiating the WebcamPCBCapture class
    self.webcam = WebcamPCBCapture()