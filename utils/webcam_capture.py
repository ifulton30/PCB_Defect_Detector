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
        # The MSMF Capture API backend doesn't seem to support changing the camera settings, so we will
        # be utilizing the DSHOW backend instead which I have tested in util/testing/test.ipynb
        self.camera_settings = {
            'brightness': 128,          # Range: [0.0, 255.0]
            'contrast': 128,            # Range: [0.0, 255.0]
            'saturation': 128,          # Range: [0.0, 255.0]
            'gain': 64,                 # Range: [0.0, 255.0]
            'exposure': -6,             # Range: [-11.0, -2.0]
            'focus': 0,                 # Range: [0.0, 255.0]
            'sharpness': 128            # Range: [0.0, 255.0]
        }

        # Calls initialize_camera to start up the webcam, but does not show frames yet
        self.initialize_camera()

    def initialize_camera(self):
        """Initializing camera for PCB imaging using DSHOW backend"""
        try:
            # This opens the camera while enforcing the DSHOW backend which is a Capture API backend.
            self.cap = cv2.VideoCapture(self.camera_id, cv2.CAP_MSMF)

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
        
        # Mapping the openCV properties
        property_map = {
            'brightness': cv2.CAP_PROP_BRIGHTNESS,
            'contrast': cv2.CAP_PROP_CONTRAST,
            'saturation': cv2.CAP_PROP_SATURATION,
            'gain': cv2.CAP_PROP_GAIN,
            'exposure': cv2.CAP_PROP_EXPOSURE,
            'focus': cv2.CAP_PROP_FOCUS,
            'sharpness': cv2.CAP_PROP_SHARPNESS
        }

        # Iterating through the camera settings
        for setting, value in self.camera_settings.items():
            # Checking to make sure the camera settings exist in the property map above
            if setting in property_map:
                
                # Normalizing the camera settings to range between 0-1 for OpenCV (Except for exposure which
                # could be negative). They currently can range between 0-255
                if setting in ['exposure']:
                    normalized_value = value
                else:
                    normalized_value = value / 255.0

                success = self.cap.set(property_map[setting], normalized_value)



class PCBTestingSession:
    """Testing manager for PCB Defect Detection"""

    def __init__(self, model, config, output_dir="test_results"):
        self.model = model
        self.config = config
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok = True)

    # Initializing the webcam by instantiating the WebcamPCBCapture class
    self.webcam = WebcamPCBCapture()