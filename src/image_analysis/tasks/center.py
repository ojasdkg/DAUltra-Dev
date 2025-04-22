from pathlib import Path
import cv2
import numpy as np
from image_analysis.processing import load_image, preprocess_edges, compute_scaling, save_csv, save_image

def process_center(input_path: Path, ref_dim: float, min_radius: float,
                   csv_out: Path, img_out: Path) -> None:
    img = load_image(input_path)
    contours = preprocess_edges(img)
    scale = compute_scaling(contours, ref_dim, closed=True)
    outer = max(contours, key=cv2.contourArea)
    (ox,oy), orad = cv2.minEnclosingCircle(outer)
    valid, out = [], img.copy()
    idx=1
    for cnt in contours:
        (x,y),r = cv2.minEnclosingCircle(cnt)
        mm = r*scale
        if mm >= min_radius and np.hypot(x-ox,y-oy)+r <= orad:
            label=f"C{idx}"
            if label=="C10":
                valid.append({"S.No.":1, "Index":label, "Radius(mm)":f"{mm:.2f}", "Center(X,Y)":(int(x),int(y))})
                cv2.circle(out,(int(x),int(y)),int(r),(255,0,0),2)
                cv2.putText(out,label,(int(x),int(y)),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),1)
            idx+=1
    save_image(out,img_out)
    save_csv(valid,["S.No.","Index","Radius(mm)","Center(X,Y)"],csv_out)