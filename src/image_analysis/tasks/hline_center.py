import cv2
import numpy as np
import matplotlib.pyplot as plt
import csv, os
from pathlib import Path

def process_hline_center(input_path: Path, csv_out: Path):
    img=cv2.imread(str(input_path))
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    edges=cv2.Canny(gray,50,150)
    lines=cv2.HoughLinesP(edges,1,np.pi/180,100,100,10)
    cy=gray.shape[0]//2
    h=None;thr=15
    for l in lines or []:
        x1,y1,x2,y2=l[0]
        if abs(y1-y2)<10 and abs(y1-cy)<thr:
            h=(x1,y1,x2,y2);break
    if not h:
        h=(0,cy,gray.shape[1],cy)
    x1,y1,x2,y2=h
    cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
    cv2.circle(img,(gray.shape[1]//2,cy),5,(0,255,0),-1)

    # interactive plot
    plt.ion();fig,ax=plt.subplots();ax.imshow(cv2.cvtColor(img,cv2.COLOR_BGR2RGB));ax.axis('off')
    headers=["X","Y","Dist(mm)","Label"]
    with open(csv_out,'w',newline='') as f:csv.writer(f).writerow(headers)
    pix_per_mm=242/25
    cnt=1
    def onclick(e):
        nonlocal cnt
        if e.xdata and e.ydata:
            x,y=int(e.xdata),int(e.ydata)
            dist=(cy-y)/pix_per_mm
            lab=f"A{cnt}";cnt+=1
            ax.plot([x,x],[y,cy],'g--');ax.scatter(x,y);ax.text(x+5,y-5,f"{lab}:{dist:.2f}mm")
            fig.canvas.draw()
            with open(csv_out,'a',newline='') as f:csv.writer(f).writerow([x,y,f"{dist:.2f}",lab])
    fig.canvas.mpl_connect('button_press_event',onclick)
    plt.show()