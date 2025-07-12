import cv2
import numpy as np
from pathlib import Path


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
            'brightness': 128.0,          # Range: [0.0, 255.0], Default: 128.0
            'contrast': 128.0,            # Range: [0.0, 255.0], Default: 128.0
            'saturation': 128.0,          # Range: [0.0, 255.0], Default: 128.0
            'gain': 9.0,                  # Range: [0.0, 255.0], Default: 9.0
            'exposure': -6.0,             # Range: [-11.0, -2.0], Default: -5.0
            'focus': 0.0,                 # Range: [0.0, 255.0], Default: 0.0
            'sharpness': 128.0            # Range: [0.0, 255.0], Default: 128.0
        }

        # Calls initialize_camera to start up the webcam, but does not show frames yet
        self.initialize_camera()

    def initialize_camera(self):
        """Initializing camera for PCB imaging using DSHOW backend"""
        try:
            # This opens the camera while enforcing the DSHOW backend which is a Capture API backend.
            self.cap = cv2.VideoCapture(self.camera_id, cv2.CAP_DSHOW)

            # Raising an error if DSHOW backend can't be used and camera can't be opened since we can't adjust camera settings
            if not self.cap.isOpened():
                raise Exception(f"Cannot open camera {self.camera_id}")
            
            # Setting the resolution of the camera. The Logitech C920 shoots up to 1920x1080
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
            
            # Setting the camera settings defined when instantiating the WebcamPCBCapture object
            self.apply_camera_settings()

            # Successful initialization message which also prints the actual resolution of camera at startup
            self.is_initialized = True
            print(f"Camera initialized successfully at resolution: {self.get_actual_resolution()}")

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
                try:
                    # Setting the value directly
                    success = self.cap.set(property_map[setting], value)

                    # Printing the actual setting on camera
                    if success:
                        actual_value = self.cap.get(property_map[setting])
                        print(f"Successfully set {setting}: {value} (Actual value: {actual_value})")
                    else:
                        print(f"Failed to setting the setting {setting} to {value}")

                except Exception as e:
                    print(f"Error setting {setting}: {e}")

    def get_actual_resolution(self):
        """Getting the actual camera resolution"""
        
        # Checking to make sure that the camera is open
        if not self.cap:
            print("Camera is not initialized so we cannot apply camera settings")
            return
        
        # Getting width and height values reported through openCV
        width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        return width, height

    def capture_frame(self):
        """Function to capture a single frame"""
        if not self.is_initialized:
            print("Could not capture frame, camera is not initialized")
            return None
        
        # Capturing a frame and returning it
        ret, frame = self.cap.read()
        if ret:
            return frame
        return None

class PCBTestingSession:
    """Testing manager for PCB Defect Detection"""

    def __init__(self, output_dir="./test_results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok = True)

        # Initializing the webcam by instantiating the WebcamPCBCapture class
        self.webcam = WebcamPCBCapture()

    def live_preview(self):
        """Live camera preview"""

        # Checking to make sure camera is initialized
        if not self.webcam.is_initialized:
            print("Camera is not initialized.")
            return
        
        # Displaying live video feed from camera
        while True:
            if self.webcam.capture_frame:
                cv2.imshow('PCB Camera Preview', self.webcam.capture_frame())
            else:
                break

            # Closing camera feed 
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def close(self):
        """Cleaning up all resources"""
        self.webcam.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    # Instantiating test session for camera
    test = PCBTestingSession()

    # Testing live preview
    test.live_preview()

    # Clean up resources
    test.close()
