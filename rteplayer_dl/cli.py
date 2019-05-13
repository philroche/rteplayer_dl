# -*- coding: utf-8 -*-

"""Console script for rteplayer_dl."""
import sys
import click

from .rteplayer_dl import download


@click.command()
@click.option('--video-xml', envvar='RTEPLAYER_PROGRAMME_VIDEO_XML',
              required=True,
              help="URL to the xml with all video data.")
@click.option('--video-directory', envvar='RTEPLAYER_VIDEO_DIRECTORY',
              required=False,
              help="Where should downloaded videos be saved?",
              type=click.Path(exists=True), default=None)
@click.option('--debug', is_flag=True, default=False,
              help='Print debug output')
def main(video_xml, video_directory, debug):
    """Console script for rteplayer_dl."""
    download(video_xml, video_directory, debug)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
