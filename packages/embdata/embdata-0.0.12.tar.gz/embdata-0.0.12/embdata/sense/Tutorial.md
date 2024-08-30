# Tutorial: Estimating Object Positions in 3D Space Using Pixels and Depth Maps

In this tutorial, we will explore how to estimate the positions of objects in 3D space using the Embodied Agents and Embodied Data libraries. This process involves leveraging pixel coordinates, depth maps, and basic transformations to achieve a clear understanding of spatial relationships in a scene.

## Overview of the Process

The workflow for extracting and manipulating spatial information is structured as follows:

1. **Input**: Begin with an image and its corresponding depth image.
2. **Object Detection**: Identify objects within the scene and extract their pixel coordinates `(u, v)`.
3. **Plane Segmentation**: Make a point cloud using the **RGB** and **Depth** Images, and perform plane segmentation.
4. **Deprojection**: Convert the 2D pixel coordinates `(u, v)` into 3D coordinates `(x, y, z)`.
5. **Transformation**: Align these 3D coordinates with a plane in the camera frame or another reference frame using transformation tools.


## Step 1: Working with the Image Class

The `Image` class provides a flexible way to load and manipulate images from various data sources, such as file paths, URLs, NumPy arrays, or Base64 strings.

### Example: Loading and Converting Images

```python
rgb_image = Image(path="resources/color_image.png", encoding="png", mode="RGB")

# Convert to NumPy array
rgb_image_array = rgb_image.array

# Convert to PIL Image
rgb_image_pil = rgb_image.pil

# Convert to Base64
rgb_image_base64 = rgb_image.base64

# Get the file path
rgb_image_path = rgb_image.path

```

You can also specify the mode when loading the image. The default mode is RGB, but other options include:

- **RGB**: 3-channel color image.
- **L**: Grayscale image.
- **I**: 16-bit raw value image.


## Step 2: Using the Depth Class to Load the Depth Image

The `Depth` class extends the `Image` class to handle depth data, offering additional functionalities necessary for 3D spatial analysis.

### Example: Creating a Depth Image Instance

If you're working with raw depth data from cameras like RealSense, ensure the encoding is set to PNG and the mode to `I` (16-bit). The `Depth` class can also accept an instance of the `Image` class and `Camera` parameters, which are crucial for creating point clouds.

```python 
depth = Depth(
    path="resources/depth_image.png", 
    encoding="png", 
    mode="I", 
    size=(1280, 720),
    rgb=Image(path="resources/color_image.png", encoding="png", mode="RGB"), 
    camera_params=Camera(
        intrinsic=Intrinsics(fx=911.0, fy=911.0, cx=653.0, cy=371.0), 
        distortion=Distortion(k1=0.0, k2=0.0, p1=0.0, p2=0.0, k3=0.0),
        extrinsic=Extrinsics(),
        depth_scale=1000.0
    ),
    depth_unit="m"
)
```

## Step 3: Defining an Instance of the World Class

The `World` class acts as a comprehensive data container, encapsulating all necessary information to describe a spatial scene. This class is integral for tasks related to robot manipulation and planning.

### Key Fields in the World Class

- **Image**: The primary image of the scene.
- **Depth Image**: The corresponding depth data.
- **Annotated Image**: An optional image with annotations.
- **Objects**: A collection of detected objects, each with associated attributes such as:
  - **Name**
  - **Bounding Box**
  - **Pose** (x, y, z, roll, pitch, yaw)
  - **Pixel Coordinates** (u, v)
  - **Mask**
- **Camera Parameters**: Including intrinsics, distortion, and extrinsics.


## Step 4: Object Detection

Object detection involves using an image and a text prompt to identify objects in a scene. The detection agent populates the `World` instance with data such as object names, bounding boxes, and pixel coordinates.

### Example: Detecting Objects in a Scene

```python
from embodied.agents.sense.object_detection_agent import ObjectDetectionAgent    

world: World = object_detection_agent.act(image=rgb_image, objects=object_names)
```


## Step 5: Integrating Images and Depth Data into the World
Once the objects have been detected, it is essential to integrate all relevant data into the World instance. This step links the images, depth data, and camera parameters, providing a complete representation of the scene.

```python
world.depth = depth
world.camera_params = depth.camera_params
world.image = rgb_image
```

## Step 6: Getting Object Poses Aligned with the Plane in the Camera Frame
The final step involves retrieving the poses of all objects in the camera frame, aligned with a specified plane. This process ensures that the object poses are accurate and correctly oriented relative to the plane.

### Example: Retrieving Object Poses

```python
relative_pose = world.get_object("all", reference="plane")
```

### How the `get_object` Method Works
1. **Plane Segmentation**: The method first segments the plane in the depth data.
2. **Rotation Alignment**: It then calculates the rotation between the plane's normal and the current z-axis.
3. **Deprojection**: The 2D pixel coordinates (u, v) are deprojected into 3D coordinates (x, y, z).
4. **Transformation**: The 3D points are transformed so that the z-axis aligns with the plane's normal.
5. **Object Positioning**: Finally, the method retrieves the object's position relative to the specified reference frame.


## Step 7: Visualization
Once the object poses are retrieved and aligned, you can visualize the results to ensure everything is correctly positioned and oriented.

```python
world.show()
```
