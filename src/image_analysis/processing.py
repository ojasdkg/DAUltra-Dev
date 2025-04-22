import cv2
import numpy as np
from pathlib import Path
from typing import List, Tuple

def load_image(path: Path) -> np.ndarray:
    img = cv2.imread(str(path))
    if img is None:
        raise FileNotFoundError(f"Cannot load image: {path}")
    return img

def preprocess_edges(img: np.ndarray) -> List[np.ndarray]:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 100, 200)
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def compute_scaling(contours: List[np.ndarray], ref_dim: float, closed: bool=True) -> float:
    ref = max(contours, key=cv2.contourArea)
    length = cv2.arcLength(ref, closed)
    if length <= 0:
        raise ValueError("Reference contour has zero length.")
    return ref_dim / length

def save_csv(rows: List[dict], headers: List[str], path: Path) -> None:
    import csv
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

def save_image(img: np.ndarray, path: Path) -> None:
    cv2.imwrite(str(path), img)