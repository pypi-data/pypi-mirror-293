import numpy as np
from embdata.coordinate import Plane, Pose6D
from embdata.geometry import Transform3D
from embdata.sense.depth import Depth
from embdata.sense.image import Image
from embdata.sense.world import World
from embdata.sense.camera import Camera, Intrinsics, Distortion, Extrinsics
from mbodied.agents.sense.object_detection_agent import ObjectDetectionAgent  
from embdata.sense.zoe_depth import ZoeDepthAgent
from embdata.utils.geometry_utils import rotation_between_two_points as align_plane_normal_to_axis
import open3d as o3d
object_detection_agent = ObjectDetectionAgent()
zoe_depth_agent = ZoeDepthAgent()   
import mbench

if __name__ == "__main__":

    
    rgb_image = Image(path="embodied-agents/resources/bridge_example.jpeg", encoding="png", mode="RGB")
    # rgb_image = Image(path="embodied-agents/resources/color_image.png", encoding="png", mode="RGB")
    zoe_depth = zoe_depth_agent.act(image=rgb_image)

    print(f"Zoe depth: {zoe_depth}")
    print(zoe_depth.shape)

    # zoe_depth_image = Depth(array=zoe_depth, encoding="png", mode="I").save(path="embodied-agents/resources/zoe_depth_image.png", encoding="png", mode="I")

    # object_names = ["Remote Control, Spoon, Fork, Basket, Red Marker"]
    object_names = ["Bowl, Red Vegetable, Brush"]

    world: World = object_detection_agent.act(image=rgb_image, objects=object_names)


    # depth = Depth(path="embodied-agents/resources/depth_image.png", encoding="png", mode="I", size=(1280, 720),
    #               rgb=Image(path="embodied-agents/resources/color_image.png", encoding="png", mode="RGB"), 
    #               camera_params=Camera(intrinsic=Intrinsics(fx=911.0, fy=911.0, cx=653.0, cy=371.0), 
    #                                    distortion=Distortion(k1=0.0, k2=0.0, p1=0.0, p2=0.0, k3=0.0),
    #                                    extrinsic=Extrinsics(),
    #                                    depth_scale=0.001),
    #                 depth_unit="mm",
    #             )
    height, width = zoe_depth.shape
    depth = Depth(array=zoe_depth, encoding="png", mode="I", size=(width, height),
                  rgb=Image(path="embodied-agents/resources/bridge_example.jpeg", encoding="png", mode="RGB"), 
                  camera_params=Camera(intrinsic=Intrinsics(fx=1.5 * width, fy=1.5 * width, cx=width / 2, cy=height / 2), 
                                       distortion=Distortion(k1=0.0, k2=0.0, p1=0.0, p2=0.0, k3=0.0),
                                       extrinsic=Extrinsics(),
                                       depth_scale=0.001),
                    depth_unit="m",
                )
    
    # Segment the plane and obtain the point cloud
    plane: Plane = depth.segment_plane(threshold=0.01, min_samples=3, max_trials=1000)


    origin = Pose6D(x=0, y=0, z=0, roll=0, pitch=0, yaw=0)
    z_axis = np.array([0, 0, 1])
    origin_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.1, origin=np.array([0, 0, 0]))
    # Align plane normal with z-axis (in opposite direction)
    rotation_matrix = align_plane_normal_to_axis(-plane.normal, z_axis)

    print(f"Plane normal: {plane.normal}")
    transform = Transform3D(rotation=rotation_matrix)
    frames = []

    for obj in world.objects:
        depth.camera_params.depth_scale = 0.001
        point_3d = depth.camera_params.deproject(obj.pixel_coords, depth_image=depth.array)
        # Transform the 3D point to the plane frame
        transformed_pos = transform.transform(point_3d)
        print(f"Transformed position: {transformed_pos}")
        frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.1, origin=transformed_pos)

        frames.append(frame)

    plane.point_cloud.transform(transform.matrix())
    inlier_cloud = plane.point_cloud.select_by_index(plane.inliers)
    outlier_cloud = plane.point_cloud.select_by_index(plane.inliers, invert=True)

    # Color the inliers red
    inlier_cloud.paint_uniform_color([1, 0, 0])

    geometries = [plane.point_cloud] + frames + [inlier_cloud, outlier_cloud] + [origin_frame]
    o3d.visualization.draw_geometries(geometries)
    # world.depth = depth
    # world.camera_params = depth.camera_params
    # world.image = rgb_image

    # result = world.get_object(name="Remote Control", reference="plane")

    