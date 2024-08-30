# Using World and Depth to Get Object Poses

```python
from embdata.sense import World, RealObject, Image, Depth, Camera, Intrinsics, Distortion, PixelCoords, Pose
from importlib_resources import files
import mbodied
depth_image_path = files("mbodied") / "resources/depth_image.png"
color_image_path = files("mbodied") / "resources/color_image.png"
camera = Camera(
        intrinsic=Intrinsics(fx=911, fy=911, cx=653, cy=371), 
        distortion=Distortion(k1=0.0, k2=0.0, p1=0.0, p2=0.0, k3=0.0),
        depth_scale=0.001
)

pose_camera_frame = Pose(x=0.0, y=0.2032, z=0.0, roll=-np.pi/2, pitch=0.0, yaw=-np.pi/2)

world = World(
      objects=[RealObject(name="apple", pose_camera_frame, pixel_coords=PixelCoords(u=320, v=240))],
      image=Image(array=np.zeros([480, 640, 3], dtype=np.uint8), mode="RGB", encoding="png"), 
      depth=Depth(path=depth_image_path,
                camera_params=camera, 
                rgb=Image(color_image_path, encoding="png"),
      ),
      camera=camera,
)

object = world.objects["apple"]
print(object.pose)

object_plane_pose = world.get_object("apple", reference="plane")
print(object_plane_pose)


```

## Async Get Object Poses

```python
import asyncio
object = asyncio.run(world.aget_object("apple"))
```