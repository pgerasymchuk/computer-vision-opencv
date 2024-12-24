import os
import numpy as np
import cv2
import open3d as o3d

ply_header = '''ply
format ascii 1.0
element vertex %(vert_num)d
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
end_header
'''

def write_ply(fn, verts, colors):
    verts = verts.reshape(-1, 3)
    colors = colors.reshape(-1, 3)
    verts = np.hstack([verts, colors])
    with open(fn, 'wb') as f:
        f.write((ply_header % dict(vert_num=len(verts))).encode('utf-8'))
        np.savetxt(f, verts, fmt='%f %f %f %d %d %d ')

def compute_disparity_and_point_cloud(imgL, imgR, Q, min_disp=5, num_disp=128):
    window_size = 5
    stereo = cv2.StereoSGBM_create(
        minDisparity=min_disp,
        numDisparities=num_disp,
        blockSize=9,
        P1=8 * 3 * window_size**2,
        P2=32 * 3 * window_size**2,
        disp12MaxDiff=1,
        uniquenessRatio=15,
        speckleWindowSize=50,
        speckleRange=5,
    )

    # Computing disparity between images
    disp = stereo.compute(imgL, imgR).astype(np.float32) / 16.0

    # Generating 3D point cloud
    points = cv2.reprojectImageTo3D(disp, Q)
    colors = cv2.cvtColor(imgL, cv2.COLOR_BGR2RGB)
    mask = disp > disp.min()
    out_points = points[mask]
    out_colors = colors[mask]
    return out_points, out_colors

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.abspath(__file__))
    imgL = cv2.pyrDown(cv2.imread(os.path.join(base_dir, '1.jpg')))
    imgM = cv2.pyrDown(cv2.imread(os.path.join(base_dir, '2.jpg')))
    imgR = cv2.pyrDown(cv2.imread(os.path.join(base_dir, '3.jpg')))

    h, w = imgL.shape[:2]
    f = 0.8 * w
    Q = np.float32([[1, 0, 0, -0.5 * w],
                    [0, -1, 0, 0.5 * h],
                    [0, 0, 0, -f],
                    [0, 0, 1, 0]])

    points1, colors1 = compute_disparity_and_point_cloud(imgL, imgM, Q)

    points2, colors2 = compute_disparity_and_point_cloud(imgM, imgR, Q)

    out_points = np.vstack([points1, points2])
    out_colors = np.vstack([colors1, colors2])

    out_fn = os.path.join(base_dir, 'out_merged.ply')
    write_ply(out_fn, out_points, out_colors)

    # Rendering 3-D model
    pcd = o3d.io.read_point_cloud(out_fn)
    o3d.visualization.draw_geometries([pcd], width=650, height=650, left=20, top=20)
