import cv2

class WebcamPCBCapture:
    """Webcam capture system optimized for PCB Imaging"""

    def __init__(self, camera_id = 0, resolution = (1920, 1080)):
        self.camera_id = camera_id
        self.resolution = resolution
        self.cap = None
        self.is_initialized = False

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

        self.initialize_camera()

    def initialize_camera(self):
        """Initializing camera for PCB imaging"""
        try:
            self.cap = cv2.VideoCapture(self.camera_id, cv2.CAP_DSHOW)

            if not self.cap.isOpened():
                self.cap = cv2.VideoCapture(self.camera_id)

        except Exception as e:
            print(f"Error initializing camera: {e}")
            self.is_initialized = False