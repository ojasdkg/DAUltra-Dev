from pathlib import Path
import cv2
from typing import List
from image_analysis.processing import load_image, preprocess_edges, compute_scaling, save_csv, save_image

def process_arcs(input_path: Path, ref_dim: float, min_length: float,
                 target_labels: List[str], csv_out: Path, img_out: Path) -> None:
    img = load_image(input_path)
    contours = preprocess_edges(img)
    scale = compute_scaling(contours, ref_dim, closed=True)
    valid, out = [], img.copy()
    idx = 1
    for cnt in contours:
        length = cv2.arcLength(cnt, False) * scale
        if length >= min_length:
            label = f"A{idx}"
            if not target_labels or label in target_labels:
                valid.append({"S.No.": len(valid)+1, "Index": label, "Length(mm)": f"{length:.2f}"})
                cv2.drawContours(out, [cnt], -1, (0,255,0), 2)
                M = cv2.moments(cnt)
                if M['m00']:
                    cx, cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
                    cv2.putText(out, f"{label}:{length:.2f}", (cx,cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0),1)
            idx += 1
    save_image(out, img_out)
    save_csv(valid, ["S.No.","Index","Length(mm)"], csv_out)