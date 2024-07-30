## Volume Hand Controller

### Overview
This Python project implements a real-time volume control system using hand gestures. By detecting and tracking the index, thumb, and pinky fingers, the system allows users to increase, decrease, or set the master volume of a system. The distance between the index and thumb fingers controls the volume level, while the pinky finger is used to set a fixed volume value within a predefined boundary.

### Technologies Used
* **Python:** Programming language for implementing the project logic.
* **OpenCV:** Library for computer vision tasks, including image processing and video capture.
* **NumPy:** Library for numerical operations and array manipulation.
* **Math:** Standard Python library for mathematical functions.
* **Custom Hand Tracking Module:** A user-defined module for hand detection and tracking.

### How It Works
1. **Hand Detection:** The system uses the OpenCV library to capture video frames from the camera.
2. **Landmark Detection:** The hand tracking module identifies key points (landmarks) on the detected hand, including the index finger, thumb, and pinky finger.
3. **Volume Control:**
   * The distance between the index and thumb fingers is calculated to determine the desired volume level.
   * The pinky finger is used to set a fixed volume level within a predefined range.
4. **Volume Adjustment:** The calculated volume level is applied to the system's master volume.

### Usage
* Ensure required libraries (OpenCV, NumPy, Math) are installed.
* Run the main Python script.
* The system will capture video frames and process hand gestures to control the volume.

### Potential Improvements
* Using good graphic cards will improve the performance.
* Add features like mute/unmute functionality or volume customization.
* Improve user interface for better interaction.

**Note:** This project demonstrates the potential of computer vision for human-computer interaction and can be further extended based on specific requirements.
 








## AI Virtual Mouse

### Overview
This Python-based project implements a virtual mouse controlled by hand gestures. By detecting and tracking the index and middle fingers, users can manipulate the computer mouse cursor and perform click actions. The project utilizes OpenCV for computer vision tasks, NumPy for numerical operations, and PyAutoGUI for mouse control.

### Features
* **Real-time hand tracking:** Detects and tracks the index and middle fingers.
* **Cursor control:** Moves the computer mouse cursor based on the position of the index finger.
* **Click simulation:** Simulates mouse clicks by analyzing the position of the index and middle fingers.
* **Fixed frame:** Ensures accurate cursor movement within a defined screen area.

### Technologies Used
* **Python:** Programming language for project implementation.
* **OpenCV:** Computer vision library for image processing and hand detection.
* **NumPy:** Library for numerical operations and array manipulation.
* **PyAutoGUI:** Library for controlling mouse and keyboard actions.
* **Custom Hand Tracking Module:** User-defined module for hand tracking logic.

### Installation
Ensure you have the following libraries installed:
1. opencv-python
2. numpy
3. PyAutoGUI

### Usage
1. Run the main Python script.
2. Position your hand in front of the camera.
3. Move your index finger to control the mouse cursor.
4. Bring your index and middle fingers close together to simulate a click.

### Known Limitations
* Accuracy of hand tracking might be affected by lighting conditions and hand movements.
* Potential for unintended clicks due to accidental finger movements.

### Future Improvements
* Using good graphic cards will improve the performance.
* Add support for additional mouse actions (e.g., right-click, scrolling).
* Develop a user-friendly interface for calibration and settings.

### Contributing
Contributions to improve the project are welcome. Please feel free to open issues or pull requests.

**Note:** This project demonstrates the potential of computer vision for human-computer interaction and can be further extended based on specific requirements.
