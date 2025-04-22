import cv2
import numpy as np
from pathlib import Path

def process_zstereo(left_path: Path, right_path: Path, focal: float=0.8, baseline: float=0.5):
    left = cv2.imread(str(left_path),cv2.IMREAD_GRAYSCALE)
    right= cv2.imread(str(right_path),cv2.IMREAD_GRAYSCALE)
    if left.shape!=right.shape:
        h,w=min(left.shape[0],right.shape[0]),min(left.shape[1],right.shape[1])
        left=cv2.resize(left,(w,h)); right=cv2.resize(right,(w,h))
    stereo=cv2.StereoBM_create(16,15)
    disp=stereo.compute(left,right).astype(np.float32)
    def click(event,x,y,flags,param):
        if event==cv2.EVENT_LBUTTONDOWN:
            d=disp[y,x]
            if d!=0:
                z=(focal*baseline)/d
                print(f"Point({x},{y}) Disp={d} Z={z}")
    cv2.imshow("Left",left); cv2.setMouseCallback("Left",click)
    cv2.waitKey(0);cv2.destroyAllWindows()