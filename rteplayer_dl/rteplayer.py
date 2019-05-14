# -*- coding: utf-8 -*-

"""Main module."""
import os
import re
import requests
import signal
import sys
from bs4 import BeautifulSoup
import ffmpeg
import youtube_dl
from rteplayer_dl.lib import findnth


def download(video_xml, video_directory, video_source='mp4', overwrite=False,
             debug=False):

    if debug:
        print('Press Ctrl+C to cancel downloads.')
        print("downloading {} ...".format(video_xml))
    r = requests.get(video_xml, allow_redirects=True)

    if debug:
        print("parsing video index URL and video title from XML ...")
    video_embed_xml = BeautifulSoup(r.content, 'lxml')
    video_index_url = video_embed_xml.find_all('video')[0].get('src')
    video_index_url_base_index = findnth(video_index_url, "/", 8)
    base_index_url = '{}/'.format(video_index_url[:video_index_url_base_index])
    if debug:
        print("video index URL = {}".format(base_index_url))
    video_title_element = video_embed_xml.find(lambda tag: tag.name == "meta"
                                               and "title"
                                               in tag.attrs['name'])
    video_title = video_title_element.attrs['content']
    if debug:
        print("video title = {}".format(video_title))

    if debug:
        print("downloading html from video index ...")
    r = requests.get(base_index_url, allow_redirects=True)

    if debug:
        print("parsing mp4 video URL from index html ...")
    video_index_html = BeautifulSoup(r.content, 'html.parser')
    video_elements = video_index_html.find_all(lambda tag: tag.name == "a"
                                               and video_source
                                               in tag.attrs['href'])

    if len(video_elements) > 1:
        # find the highest resolution file to download.
        # I have determined that if there are multiple ismvs then the highest
        # res streeam is that with the highest second component of the
        # filename.
        video_filename = None
        highest_resolution_video = None
        for video_element in video_elements:
            _filename = video_element.attrs['href']
            # Example filename:
            # IP000061389-1556476261769_5d0f3ed8cf714b4a82c2d0f968c7c1d0.ismv
            resolution_identifier_regex = \
                re.compile(r'-(?P<resolution_identifier>[\d]+?)_')

            resolution_identifier_matches = resolution_identifier_regex.search(
                _filename)
            if resolution_identifier_matches:
                resolution_identifier = int(
                    resolution_identifier_matches.group(
                        'resolution_identifier'
                    ))
            else:
                # I have found that some lists of ismv files do not conform
                # to the same filename pattern. As such  -
                # just ignore those that don't conform.
                resolution_identifier = 0

            if not highest_resolution_video or \
                    resolution_identifier > \
                    highest_resolution_video:
                highest_resolution_video = resolution_identifier
                video_filename = _filename

    else:
        video_element = video_elements[0]
        video_filename = video_element.attrs['href']

    abs_video_url = '{}{}'.format(base_index_url, video_filename)

    if debug:
        print("video url = {}".format(abs_video_url))

    video_local_path = "{}.{}".format(video_title, video_source)
    mp4_video_path = "{}.mp4".format(video_title)
    if video_directory:
        video_local_path = os.path.join(video_directory, video_local_path)
        mp4_video_path = os.path.join(video_directory, mp4_video_path)

    mp4_exists = os.path.isfile(mp4_video_path)
    if not overwrite and mp4_exists:
        print("{} already exists. Pass `--overwrite` to force download."
              .format(mp4_video_path))
        sys.exit(0)

    def download_signal_handler(sig, frame):
        print('')
        print('You have cancelled all downloads.')
        print('Cleaning up any partial downloads...')
        partial_download_path = '{}.part'.format(video_local_path)
        os.remove(partial_download_path)
        print('Cleaning up complete.')
        sys.exit(0)

    signal.signal(signal.SIGINT, download_signal_handler)

    ydl = youtube_dl.YoutubeDL({'outtmpl': video_local_path})
    if debug:
        print("downloading mp4 video using youtube-dl ...")
    with ydl:
        ydl.download([abs_video_url])
        if debug:
            print("video downloaded successfully")
        if video_source != 'mp4':
            if debug:
                print("Converting from ismv to mp4 using ffmpeg ...")
            # Convert to mp4 from ismv
            stream = ffmpeg.input(video_local_path)
            stream = ffmpeg.output(stream, mp4_video_path,
                                   vcodec='copy',
                                   acodec='copy')
            stream = ffmpeg.overwrite_output(stream)
            ffmpeg.run(stream)
            if debug:
                print("Successfully converted ismv to mp4.")
            # remove the ismv as we no longer need it
            if debug:
                print("Removing ismv no longer required")
            os.remove(video_local_path)
