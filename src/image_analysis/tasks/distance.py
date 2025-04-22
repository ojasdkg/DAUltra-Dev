import cv2
import math
from pathlib import Path
from typing import Tuple

def align_point(x:int,y:int,ref_x:int,ref_y:int)->Tuple[int,int]:
    dx,dy=abs(x-ref_x),abs(y-ref_y)
    return (x,ref_y) if dx>dy else (ref_x,y)

def process_distance(input_path: Path, ref_mm: float, csv_out: Path):
    global img, pts, ref_pix
    img=cv2.imread(str(input_path))
    pts,ref_pix=[],None
    def click(event,x,y,flags,param):
        # nonlocal pts,ref_pix
        if event==cv2.EVENT_LBUTTONDOWN:
            if pts:
                x,y=align_point(x,y,pts[0][0],pts[0][1])
            pts.append((x,y))
            cv2.circle(img,(x,y),5,(0,0,255),-1)
            if len(pts)==2:
                dx,dy=pts[1][0]-pts[0][0],pts[1][1]-pts[0][1]
                pix=math.hypot(dx,dy)
                if ref_pix is None:
                    ref_pix=pix
                else:
                    mm= pix * (ref_mm/ref_pix)
                    cv2.line(img,pts[0],pts[1],(255,0,0),2)
                    cv2.putText(img,f"{mm:.2f}mm",((pts[0][0]+pts[1][0])//2, (pts[0][1]+pts[1][1])//2),
                                cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),1)
                pts=[]
                cv2.imshow("img",img)
    cv2.imshow("img",img)
    cv2.setMouseCallback("img",click)
    cv2.waitKey(0);cv2.destroyAllWindows()