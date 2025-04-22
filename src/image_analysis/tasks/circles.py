from pathlib import Path
import cv2
import numpy as np
from image_analysis.processing import load_image, preprocess_edges, compute_scaling, save_csv, save_image
from typing import List

def process_circles(input_path: Path, ref_dim: float, min_radius: float,
                    target_labels: List[str], csv_out: Path, img_out: Path) -> None:
    img = load_image(input_path)
    contours = preprocess_edges(img)
    scale = compute_scaling(contours, ref_dim, closed=True)
    outer = max(contours, key=cv2.contourArea)
    (ox,oy), orad = cv2.minEnclosingCircle(outer)
    valid, out = [], img.copy()
    idx = 1
    for cnt in contours:
        (x,y), r = cv2.minEnclosingCircle(cnt)
        mm = r * scale
        if mm >= min_radius and np.hypot(x-ox,y-oy)+r <= orad:
            label = f"C{idx}"
            if not target_labels or label in target_labels:
                valid.append({"S.No.": len(valid)+1, "Index": label, "Radius(mm)": f"{mm:.2f}",
                              "Diameter(mm)": f"{2*mm:.2f}"})
                cv2.circle(out, (int(x),int(y)), int(r), (255,0,0),2)
                cv2.putText(out, label, (int(x),int(y)), cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),1)
                cv2.putText(out, f"D={2*mm:.2f}", (int(x)+int(r),int(y)), cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),1)
            idx+=1
    save_image(out, img_out)
    save_csv(valid, ["S.No.","Index","Radius(mm)","Diameter(mm)"], csv_out)