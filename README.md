## Finding Lane Boundaries on the Road

The project is a software pipeline that does road lane boundaries identification on images or video. The project uses two assumptions:
- camera is mounted at the center of a car
- lane lines are parallel

##

**How to start with your own camera**

Here is required steps with some description:

1. Set image width and height parameters according to your camera configuration

`main.py`, line 35 
``` 
w, h = 1280, 720
``` 

2. Prepare camera calibration images for image distortion correction

Camera calibration requires images of [chess board pattern](images/pattern.png) taken by the camera from different angles and distances. 
`camera.load_calibration_images` function at line 38 of `main.py` accepts path to the calibration images and number of inner corners per a chessboard row and column. 
If you are using given pattern, you need to update only path parameter value.

3. Define initial lane vanishing point distance

Lane vanishing point distance is a distance from bottom of an image to lane perspective center in pixels. 
It don't have to be precise value - program will adjust it during video frames processing.

4. Set meters per pixel coefficient that corresponds to bottom of an image for proper scailing.

[//]: # (Image References)

[image1]: ./examples/undistort_output.png "Undistorted"
[image2]: ./test_images/test1.jpg "Road Transformed"
[image3]: ./examples/binary_combo_example.jpg "Binary Example"
[image4]: ./examples/warped_straight_lines.jpg "Warp Example"
[image5]: ./examples/color_fit_lines.jpg "Fit Visual"
[image6]: ./examples/example_output.jpg "Output"
[video1]: ./project_video.mp4 "Video"

##
### Detailed program description 

**Camera Calibration**

Coming soon...