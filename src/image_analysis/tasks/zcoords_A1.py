import cv2
import numpy as np
import open3d as o3d
from pathlib import Path

def process_zslam(left_path: Path, right_path: Path):
    img1, img2 = map(lambda p: cv2.imread(str(p)), (left_path, right_path))
    gray1, gray2 = map(lambda i: cv2.cvtColor(i,cv2.COLOR_BGR2GRAY), (img1,img2))
    sift = cv2.SIFT_create()
    kp1, des1 = sift.detectAndCompute(gray1,None)
    kp2, des2 = sift.detectAndCompute(gray2,None)
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1,des2,k=2)
    good = [m for m,n in matches if m.distance <0.85*n.distance]
    pts1 = np.float32([kp1[m.queryIdx].pt for m in good])
    pts2 = np.float32([kp2[m.trainIdx].pt for m in good])
    h,w = gray1.shape
    f = max(h,w)
    K = np.array([[f,0,w//2],[0,f,h//2],[0,0,1]],float)
    E,mask = cv2.findEssentialMat(pts1,pts2,K,cv2.RANSAC,0.999,5.0)
    in1, in2 = pts1[mask.ravel()>0], pts2[mask.ravel()>0]
    _,R,t,maskp = cv2.recoverPose(E,in1,in2,K)
    in1, in2 = in1[maskp.ravel()>0], in2[maskp.ravel()>0]
    P1 = K.dot(np.hstack((np.eye(3),np.zeros((3,1)))))
    P2 = K.dot(np.hstack((R,t)))
    pts4D = cv2.triangulatePoints(P1,P2,in1.T.astype(np.float32),in2.T.astype(np.float32))
    pts3D = (pts4D[:3]/pts4D[3]).T
    pcd = o3d.geometry.PointCloud()
    pcd.points=o3d.utility.Vector3dVector(pts3D)
    try:
        o3d.visualization.gui.Application.instance.initialize()
        vis = o3d.visualization.O3DVisualizer("3D",800,600)
        vis.add_geometry("pcd",pcd)
        for p in pts3D: vis.add_3d_label(p,f"({p[0]:.2f},{p[1]:.2f},{p[2]:.2f})")
        vis.show(True); o3d.visualization.gui.Application.instance.run()
    except AttributeError:
        o3d.visualization.draw_geometries([pcd])