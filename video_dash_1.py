#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 14:56:54 2022

@author: saulo
"""

import moviepy.editor as mp
from moviepy.editor import *

video = mp.VideoFileClip('video_3_dash.mp4').cutout(0, 3)
video = video.cutout(14.40, 14.44)
video.write_videofile("video_dash_post.mp4", fps=30)
