# -*- coding: utf-8 -*-

"""Main module."""
import os
import requests
from bs4 import BeautifulSoup
import youtube_dl
from .lib import findnth


def download(video_xml, video_directory, debug):
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
    mp4_element = video_index_html.find(lambda tag: tag.name == "a" and
                                        "mp4" in tag.attrs['href'])
    mp4_url = mp4_element.attrs['href']
    abs_mp4_url = '{}{}'.format(base_index_url, mp4_url)

    if debug:
        print("video url = {}".format(abs_mp4_url))

    video_path = "{}.mp4".format(video_title)
    if video_directory:
        video_path = os.path.join(video_directory, video_path)
    ydl = youtube_dl.YoutubeDL({'outtmpl': video_path})
    if debug:
        print("downloading mp4 video using youtube-dl ...")
    with ydl:
        ydl.download([abs_mp4_url])
        if debug:
            print("video downloaded successfully")
