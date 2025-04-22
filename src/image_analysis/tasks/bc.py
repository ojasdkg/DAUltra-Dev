import math
from typing import List, Tuple

def calculate_radius(center: Tuple[float,float], points: List[Tuple[float,float]]) -> float:
    if not points:
        return None
    x_c,y_c = center
    return math.hypot(points[0][0]-x_c, points[0][1]-y_c)

if __name__=='__main__':
    import click
    from image_analysis.tasks.bc import calculate_radius

    @click.command()
    @click.option('--center', required=True, help='x,y')
    @click.option('--points', nargs=2, required=True, help='x1,y1 x2,y2')
    def cli(center, points):
        cx,cy = map(float,center.split(','))
        pts=[tuple(map(float,p.split(','))) for p in points]
        r = calculate_radius((cx,cy),pts)
        click.echo(f"Radius of the circle: {r}")

    cli()