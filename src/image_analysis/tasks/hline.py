import cv2
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

def process_hline(input_path: Path, out_img: Path):
    img=cv2.imread(str(input_path))
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    edges=cv2.Canny(gray,50,150)
    lines=cv2.HoughLinesP(edges,1,np.pi/180,100,100,10)
    h=None;h_y=gray.shape[0]//2
    for l in lines or []:
        x1,y1,x2,y2=l[0]
        if abs(y1-h_y)<10 and abs(y2-h_y)<10:
            h=(x1,y1,x2,y2);break
    if h:
        x1,y1,x2,y2=h
        cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
        cv2.putText(img,"H-Line",(x1,y1-10),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,255),2)
    center=(gray.shape[1]//2,gray.shape[0]//2)
    cv2.circle(img,center,5,(0,0,255),-1)
    plt.imshow(cv2.cvtColor(img,cv2.COLOR_BGR2RGB));plt.axis('off');plt.show()
    cv2.imwrite(str(out_img),img)