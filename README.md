## Finding Lane Boundaries on the Road

The project is a software pipeline that does road lane boundaries identification on images or video. The project uses two assumptions:
- camera is mounted at the center of a car
- lane lines are parallel

##

**How to start with your own camera**

[//]: # (Image References)

[img_corners]: ./images/corners.png "Internal corners nx=9, ny=6"
[img_distortion_example]: ./images/distortion_example.jpg "Barrel distortion example"
[img_undistortion_example]: ./images/undistorted.png "Image undistortion example"
[img_example_input_image]: ./images/example_input_image.jpg "Initial frame"
[gif_pipeline_visualisation]: ./images/pipeline.gif "Pipeline visualisation"
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
![alt text][img_corners]
- path_pattern - path to prepared calibration chessboard images

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

Optical distortion is a camera lens error that deforms and bends physically straight lines and makes them appear curvy on image. Camera I used also produces distorted images:
![alt text][img_distortion_example]

The process of image undistortion looks next:
- for given (nx, ny) pattern I collect actual coordinates on real calibration images. I use `cv2.findChessboardCorners` function to find the coordinates.
```
camera.load_calibration_images(nx=9, ny=6, path_pattern="../input/camera_calibration/calibration*.jpg")
```
- I obtain distortion coefficients from collected data using `cv2.calibrateCamera` function.
```
camera.calibrate()
```
- and finally I can apply distortion coefficients to each frame of a video stream with help of `cv2.undistort` function
```
undistorted_image = camera.undistort(bgr_frame)
```

Here is how an undistortion result is look like:
![alt text][img_undistortion_example]
The result is not perfect, but it is a way better than source image. I would assume more calibration images should make the end result even better.

**Image processing pipeline**

Image processing pipeline is defined in [ImageProcessor](https://github.com/wakeful-sun/lane-finder/blob/master/code/image_processor.py) class. The class constructor function accepts all parties involved in frame processing.
And it has next stages:
- frame undistortion
- color threshold filtering
- perspective transformation to bird view
- lane lines detection
- lane validation
- lane mask creation
- lane mask perspective transformation from bird view
- original frame image and transformed lane mask concatenation
- frame text information output

![alt text][gif_pipeline_visualisation]

*Frame undistortion:*

```
undistorted_image = self.camera.undistort(bgr_frame)
```


Coming soon...