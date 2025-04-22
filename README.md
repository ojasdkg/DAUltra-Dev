# Optimized Image Analysis

A unified CLI for detecting arcs, circles, centers, distances, lines, and 3D coordinates from images.

## Installation

```bash
pip install -e .
```

## Commands

```bash
image-analysis arcs    --input in.jpg --ref-dim 25 --min-length 2 --labels A1 A2 --csv arcs.csv --annot arcs_out.jpg
image-analysis circles --input in.jpg --ref-dim 25 --min-radius 1  --labels C1 C2 --csv circ.csv --annot circ_out.jpg
image-analysis center  --input in.jpg --ref-dim 25 --min-radius 1  --csv cen.csv --annot cen_out.jpg
image-analysis bc      --center 3,4 --points 6,8 0,4
image-analysis coords  --input arcs.jpg
image-analysis distance --input side.jpg --ref-mm 10 --csv dist.csv
image-analysis hline   --input side.jpg --out hline.jpg
image-analysis hline-center --input side.jpg --csv click.csv
image-analysis zcoords-slam --left left.jpg --right right.jpg
image-analysis zcoords-stereo --left left.jpg --right right.jpg
