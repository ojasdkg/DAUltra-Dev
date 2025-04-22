import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def process_coords(input_path: Path):
    img = cv2.imread(str(input_path))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,50,150)
    contours,_ = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    arcs=[]
    for cnt in contours:
        approx=cv2.approxPolyDP(cnt,0.02*cv2.arcLength(cnt,True),True)
        if len(approx)>5:
            arcs.append(approx)
    out=img.copy()
    for arc in arcs:
        cv2.drawContours(out,[arc],-1,(0,255,0),2)
    plt.imshow(cv2.cvtColor(out,cv2.COLOR_BGR2RGB));plt.show()
    if arcs:
        sa,ea = tuple(arcs[0][0][0]), tuple(arcs[0][-1][0])
        click.echo(f"Start:{sa}, End:{ea}")
    else:
        click.echo("No prominent arcs detected.")