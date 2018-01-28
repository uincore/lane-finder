## Finding Lane Boundaries on the Road

The project is a software pipeline that does road lane boundaries identification on images or video. The project uses two assumptions:
- camera is mounted at the center of a car
- lane lines are parallel

##

**How to start with your own camera**

[//]: # (Image References)

[image1]: ./images/corners.png "Internal corners nx=9, ny=6"
[image2]: ./test_images/test1.jpg "Road Transformed"
[image3]: ./examples/binary_combo_example.jpg "Binary Example"
[image4]: ./examples/warped_straight_lines.jpg "Warp Example"
[image5]: ./examples/color_fit_lines.jpg "Fit Visual"
[image6]: ./examples/example_output.jpg "Output"
[video1]: ./project_video.mp4 "Video"

Here is required steps with some description:

1. Prepare set of camera calibration images for image distortion correction

Camera calibration requires images of [chess board pattern](images/pattern.png) taken by the camera from different angles and distances. 

2. Update [camera configuration](https://github.com/wakeful-sun/lane-finder/blob/105d35d85a5edc6c61776560e8a3858a6aa0f6e2/code/main.py#L35) and [camera calibration](https://github.com/wakeful-sun/lane-finder/blob/105d35d85a5edc6c61776560e8a3858a6aa0f6e2/code/main.py#L38) parameters

Camera calibration is built on top of [OpenCV](https://docs.opencv.org/3.3.1/dc/dbb/tutorial_py_calibration.html) library

```
w, h = 1280, 720

camera = Camera(w, h)
camera.load_calibration_images(nx=9, ny=6, path_pattern="path_to_camera_calibration_images")
camera.calibrate()
```

- w, h - camera image width and height
- nx, ny - number of internal corners per a chessboard row (ny) and column (nx). Here is a visualization of nx=9 ny=6 chessboard:
![alt text][image1]
- path_pattern - path to prepared calibration images

3. Define initial [lane vanishing point distance](https://github.com/wakeful-sun/lane-finder/blob/105d35d85a5edc6c61776560e8a3858a6aa0f6e2/code/main.py#L25)

```
initial_vanishing_point_distance = 310
```

Lane vanishing point distance is a distance from bottom of an image to lane perspective center in pixels. 
It don't have to be precise value - program will adjust it during video frames processing.

4. Set [meters per pixel coefficient](https://github.com/wakeful-sun/lane-finder/blob/105d35d85a5edc6c61776560e8a3858a6aa0f6e2/code/main.py#L26) that corresponds to bottom of an image for proper scailing.

```
x_meters_per_pixel = 3.7 / 700
```

##
### Detailed program description 

**Camera Calibration**

Coming soon...