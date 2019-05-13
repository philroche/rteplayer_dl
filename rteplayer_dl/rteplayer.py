# -*- coding: utf-8 -*-

"""Main module."""
import os
import requests
from bs4 import BeautifulSoup
import ffmpeg
import youtube_dl
from rteplayer_dl.lib import findnth


def download(video_xml, video_directory, video_source='mp4', debug=False):
    if debug:
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
        highest_resolution_ismv = None
        for video_element in video_elements:
            _filename = video_element.attrs['href']
            _components = _filename.split('_')
            resolution_determining_component = _components[0]
            _components = resolution_determining_component.split('-')
            resolution_determining_component = int(_components[1])
            if not highest_resolution_ismv or \
                    resolution_determining_component > highest_resolution_ismv:
                highest_resolution_ismv = resolution_determining_component
                video_filename = _filename
    else:
        video_element = video_elements[0]
        video_filename = video_element.attrs['href']

    abs_video_url = '{}{}'.format(base_index_url, video_filename)

    if debug:
        print("video url = {}".format(abs_video_url))

    video_local_path = "{}.{}".format(video_title, video_source)

    if video_directory:
        video_local_path = os.path.join(video_directory, video_local_path)

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
            mp4_video_path = "{}.mp4".format(video_title)
            mp4_video_path = os.path.join(video_directory, mp4_video_path)
            stream = ffmpeg.input(video_local_path)
            stream = ffmpeg.output(stream, mp4_video_path)
            stream = ffmpeg.overwrite_output(stream)
            ffmpeg.run(stream)
            if debug:
                print("Successfully converted ismv to mp4.")
            # remove the ismv as we no longer need it
            if debug:
                print("Removing ismv no longer required")
            os.remove(video_local_path)
