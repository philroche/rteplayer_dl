# -*- coding: utf-8 -*-

"""Console script for rteplayer_dl."""
import sys
import click

from rteplayer_dl.rteplayer import download


@click.command()
@click.option('--video-xml', envvar='RTEPLAYER_PROGRAMME_VIDEO_XML',
              required=True,
              help="URL to the xml with all video data.")
@click.option('--video-directory', envvar='RTEPLAYER_VIDEO_DIRECTORY',
              required=False,
              help="Where should downloaded videos be saved?",
              type=click.Path(exists=True), default=None)
@click.option('--video-source', type=click.Choice(['mp4', 'ismv']),
              required=False,
              help='Use ismv (much larger download but higher resolution) or '
                   'mp4 as the video source',
              default='mp4')
@click.option('--overwrite', is_flag=True, default=False,
              help='Overwrite existing files with same name')
@click.option('--debug', is_flag=True, default=False,
              help='Print debug output')
def main(video_xml, video_directory, video_source, overwrite, debug):
    """Console script for rteplayer_dl."""
    download(video_xml, video_directory, video_source, overwrite, debug)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
