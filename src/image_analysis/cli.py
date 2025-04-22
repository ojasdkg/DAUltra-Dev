import click
from pathlib import Path
from image_analysis.tasks.arcs import process_arcs
from image_analysis.tasks.circles import process_circles
from image_analysis.tasks.center import process_center
from image_analysis.tasks.bc import calculate_radius
from image_analysis.tasks.coords import process_coords
from image_analysis.tasks.distance import process_distance
from image_analysis.tasks.hline import process_hline
from image_analysis.tasks.hline_center import process_hline_center
from image_analysis.tasks.zcoords_slam import process_zslam
from image_analysis.tasks.zcoords_stereo import process_zstereo

@click.group()
def cli():
    "Image Analysis CLI"
    pass

@cli.command()
@click.option('--input', 'inp', required=True)
@click.option('--ref-dim', default=25.0)
@click.option('--min-length', default=2.0)
@click.option('--labels', multiple=True)
@click.option('--csv', 'csvp', default='arcs.csv')
@click.option('--annot', 'anp', default='arcs_out.jpg')
def arcs(inp, ref_dim, min_length, labels, csvp, anp):
    process_arcs(Path(inp), ref_dim, min_length, list(labels), Path(csvp), Path(anp))

# (similar click wrappers for other commands)...

if __name__=='__main__':
    cli()