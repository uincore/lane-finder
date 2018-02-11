## Finding Lane Boundaries on the Road

The project is a software pipeline that does road lane boundaries identification on images or on video. The project uses two assumptions:
- camera is mounted at the center of a car
- camera optical axis is on car's center line
- lane lines are parallel
- lane lines could be white or yellow

##

**How to start with your own camera**

[//]: # (Image References)

[img_corners]: ./images/corners.png "Internal corners nx=9, ny=6"
[img_chessboard_distorted]: ./images/chessboard_distorted.png "Barrel distortion example"
[img_chessboard_undistorted]: ./images/chessboard_undistorted.png "Image undistortion example"
[gif_pipeline_visualisation]: ./images/pipeline.gif "Pipeline visualisation"
[gif_road_image_undistortion]: ./images/road_image_undistortion.gif "Road image undistortion"
[img_visual_ray_method]: ./images/visual_ray_method.png "Visual ray method visualization"
[img_source_points]: ./images/source_points.jpg "Source points"
[img_lane_uml]: ./images/lane_uml.png "Lane UML"

Here is required steps with some description:

1. Prepare set of camera calibration images for image distortion correction

Camera calibration requires images of [chess board pattern](images/pattern.png) taken by the camera from different angles and distances. 

2. Update [camera configuration](https://github.com/wakeful-sun/lane-finder/blob/105d35d85a5edc6c61776560e8a3858a6aa0f6e2/code/main.py#L35) and [camera calibration](https://github.com/wakeful-sun/lane-finder/blob/105d35d85a5edc6c61776560e8a3858a6aa0f6e2/code/main.py#L38) parameters

``` python
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

``` python
initial_vanishing_point_distance = 310
```

Lane vanishing point distance is a distance from bottom of an image to straight lane perspective center on flat road in pixels. 
It don't have to be precise value - program will adjust it during video frames processing.

4. Set [meters per pixel coefficient](https://github.com/wakeful-sun/lane-finder/blob/105d35d85a5edc6c61776560e8a3858a6aa0f6e2/code/main.py#L26) that corresponds to bottom of an image for proper scailing.

``` python
x_meters_per_pixel = 3.7 / 700
```

##
### Detailed program description 

**Camera Calibration**

Optical distortion is a camera lens error that deforms and bends physically straight lines and makes them appear curvy on image. 
Camera I used also produces distorted images. Camera calibration produces distortion coefficients, that can be applied to any camera image for distortion minimisation. My camera calibration is built on top of [OpenCV](https://docs.opencv.org/3.3.1/dc/dbb/tutorial_py_calibration.html) library and consits of:

- collecting calibration data. For given (nx, ny) pattern I retrieve actual coordinates from each real calibration chessboard image using `cv2.findChessboardCorners` function
``` python
camera.load_calibration_images(nx=9, ny=6, path_pattern="../input/camera_calibration/calibration*.jpg")
```
- actual camera calibration. In order to get distortion coefficients I pass collected calibration data to `cv2.calibrateCamera` function
``` python
camera.calibrate()
```

Now instance of [`Camera`](https://github.com/wakeful-sun/lane-finder/blob/master/code/camera.py) class contains distortion coefficients which can be applied to any camera image. Distorted camera image and distortion coefficient are passed to `cv2.undistort` function which produces new undistorted image
``` python
undistorted_image = camera.undistort(bgr_frame)
```
Here is an example of image distortion minimisation:

|![alt text][img_chessboard_distorted] |![alt text][img_chessboard_undistorted]|
|:---:|:---:|
| original image | undistorted image | 

The result is not perfect, but it is a way better than source image. I would assume more calibration images should make the end result even better.

##

**Image processing pipeline**

Image processing pipeline is defined in [`ImageProcessor`](https://github.com/wakeful-sun/lane-finder/blob/master/code/image_processor.py) class. The class constructor function accepts all parties involved in frame processing.

![alt text][gif_pipeline_visualisation]

The pipeline consists of next stages:
- frame undistortion
- color threshold filtering
- perspective transformation to top-down view
- lane lines detection
- lane validation
- lane mask creation
- lane mask perspective transformation back from top-down view
- undistorted image and transformed lane mask concatenation
- frame text information output

<h6>Frame undistortion</h6>

``` python
undistorted_image = self.camera.undistort(bgr_frame)
```

![alt text][gif_road_image_undistortion]

<h6>Color threshold filtering</h6>

``` python
bw_image_filtered = self.threshold.execute(undistorted_image)
```
Using an assumption that lane lines could be white or yellow, I created color filter for highlighting yellow and white objects on images. The filter converts image to HSV format and then applies actual color boundaries. The result is black & wight image.

|<img src="./images/001_undistorted_image.png" alt="Undistorted road image" width="400px">|<img src="./images/002_bw_image_filtered.png" alt="Color threshold" width="400px">|
|:---:|:---:|
| undistorted image | result of color threshold filtering |

<h6>Perspective transformation to top-down view</h6>

``` python
bw_bird_view = self.perspective_transform.execute(bw_image_filtered, transform_to="top_down_view")
```
In order to be able to get lane physical parameters (like curvature, distances, angle between car central line and road lane central line) we need to apply a perspective transform, so that it looks like we are viewing the road from the top. 

Perspective transformation requires source and destination points. How to choose them? 
I've started from an assumption that lane lines are parallel on real road. 
So correct transformation to top-down view should have parallel lane lines. 
Then using image of **straight lane** below I found lane vanishing point **VP** and simply measured distance to it from the bottom of the image (**A_VP**). 
Initial [vanishing point](https://github.com/wakeful-sun/lane-finder/blob/105d35d85a5edc6c61776560e8a3858a6aa0f6e2/code/main.py#L25) is a configurable parameter that have to be set for certain camera position. 
Another configurable parameter is [**AE** distance](https://github.com/wakeful-sun/lane-finder/blob/20d6176f70656511e2f1241fe01e686b929ff340/code/main.py#L28).

|![alt text][img_source_points]|
|:---:|
|**straight lane on flat road**|

Knowing **A_VP**, **BC** (which is equal **AE**) and **AB** (`image_width/2`) distances and some basic trigonometry we can found [**CD**](https://github.com/wakeful-sun/lane-finder/blob/20d6176f70656511e2f1241fe01e686b929ff340/code/image_operations/transformation_parameters.py#L70) distance. 

```
CD = BC * AB / A_VP
```

And finally it gives us [source points](https://github.com/wakeful-sun/lane-finder/blob/20d6176f70656511e2f1241fe01e686b929ff340/code/image_operations/transformation_parameters.py#L40-L49)

Now I decided not to pick up static destination points for perspective transformation, because it will produce deformed image. Equal scaling along axes will give me opportunity of visual validation of top-down view. 
That also should simplify measurement of lane curvature, distances and car position angles. 

The algorithm program uses for producing size of equally scaled along (x, y) axis top-down view image is built with help of refinement known as [**visual ray method**](https://www.handprint.com/HP/WCL/perspect2.html). 

|![alt text][img_visual_ray_method]|
|:---:|
|**visual ray method applied to straight lane**|

The resulting top-down view image size:
- width is the same with as the one of source image
- height [**DF**](https://github.com/wakeful-sun/lane-finder/blob/20d6176f70656511e2f1241fe01e686b929ff340/code/image_operations/transformation_parameters.py#L76-L78) can be found using known parameters and trigonometric equation:
```
(2 * D_VP + DF) / A'F = (2 * VP - CD) / AC
```
so
```
DF = A'F * (2 * VP - CD) / AC - 2 * D_VP
```

And here is how undistorted image to top-down view image perspective transformation result is look like:

|<img src="./images/002_bw_image_filtered.png" alt="Front view" width="400px">|<img src="./images/003_bw_bird_view.png" alt="Top-down view" width="400px">|
|:---:|:---:|
| undistorted image | result of perspective transformation |

<h6>Lane lines detection</h6>

``` python
self.lane.update(bw_bird_view)
```

Road lane is described in separate [`Lane`](https://github.com/wakeful-sun/lane-finder/blob/master/code/lane/lane.py) class.
It is responsible for lane lines detection and holding the detection result between updates. So its state can used by validation and visualization components later in pipeline.

|![alt text][img_lane_uml]|
|:---:|
|Lane class diagram|           

`Lane` object is initialized one time in [main.py](https://github.com/wakeful-sun/lane-finder/blob/0a07a8f2a9544717371ae0a6102f2d787a150e39/code/main.py#L45-L49) and passed as constructor parameter to `ImageProcessor`

``` python
sliding_window_container = SlidingWindowsContainer()
sliding_window_line_detector = SlidingWindowLineDetector(sliding_window_container)
curved_line_factory = CurvedLineFactory(sliding_window_line_detector)

lane = Lane(curved_line_factory, x_meters_per_pixel)
```
#
*Lane line objects initialization*

In initial state `Lane` object has [empty lane lines](https://github.com/wakeful-sun/lane-finder/blob/0a07a8f2a9544717371ae0a6102f2d787a150e39/code/lane/lane.py#L13-L14).
[On first](https://github.com/wakeful-sun/lane-finder/blob/0a07a8f2a9544717371ae0a6102f2d787a150e39/code/lane/lane.py#L51-L52) `update` method invocation both left and right lane lines [are initialized with](https://github.com/wakeful-sun/lane-finder/blob/0a07a8f2a9544717371ae0a6102f2d787a150e39/code/lane/lane.py#L72-L73) new instances of [`LaneLine`](https://github.com/wakeful-sun/lane-finder/blob/0a07a8f2a9544717371ae0a6102f2d787a150e39/code/lane/lane_line.py) class.
`LaneLine` constructor function requires `start_x` parameter, which is approximate `x` coordinate of lane line at very bottom of the image. This parameter is used exclusively by lane line detection algorithm.
So the program [identifies start points](https://github.com/wakeful-sun/lane-finder/blob/0a07a8f2a9544717371ae0a6102f2d787a150e39/code/lane/lane.py#L76-L86) for each line first.
#
*Lane line detection*

When initialization is done the program [invokes `update` functon](https://github.com/wakeful-sun/lane-finder/blob/0a07a8f2a9544717371ae0a6102f2d787a150e39/code/lane/lane.py#L54-L55) on each lane line instance.
``` python
self.left_line.update(bw_image)
self.right_line.update(bw_image)
```
And `LaneLine` forvars this call to the party that does actual lane line detection - to [`CurvedLineFactory`](https://github.com/wakeful-sun/lane-finder/blob/master/code/line_factory/sliding_window/curved_line_factory.py). 
Detection result is written to [`CurvedLine`](https://github.com/wakeful-sun/lane-finder/blob/master/code/line_factory/curved_line.py) instance.
```python
self.line = self.curved_line_factory.create(bw_image, self.start_x)
```
`CurvedLineFactory` uses sliding window method for lane line detection. 
Sliding window detection algorithm itself is implemented in [`SlidingWindowLineDetector`](https://github.com/wakeful-sun/lane-finder/blob/master/code/line_factory/sliding_window/sliding_window_line_detector.py) class.


#


##
Coming soon...