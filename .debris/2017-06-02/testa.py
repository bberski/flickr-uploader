# -*- coding: utf-8 -*-

import pyexiftool.exiftool as exiftool
from pprint import pprint
import sys
import time
import datetime
import mimetypes
'''
files = ["/mnt/Delad/Bilder/2flickr/CIMG3206.AVI", "/mnt/Delad/Bilder/2flickr/P1050137.AVI", 
    "/mnt/Delad/Bilder/2flickr/20150226_154620.mp4", "/mnt/Delad/Bilder/2flickr/IMG_4128.MOV",
    "/mnt/Delad/Bilder/2flickr/MOV00479.3gp", "/mnt/Delad/Bilder/2flickr/IMG_1079.m4v"]
files = ["/Volumes/Delad/Bilder/2flickr/CIMG3206.AVI", "/Volumes/Delad/Bilder/2flickr/P1050137.AVI", 
    "/Volumes/Delad/Bilder/2flickr/20150226_154620.mp4", "/Volumes/Delad/Bilder/2flickr/IMG_4128.MOV",
    "/Volumes/Delad/Bilder/2flickr/IMG_1079.m4v", "/Volumes/Delad/Bilder/2flickr/MOV00479.3gp",
    "/Volumes/Delad/Bilder/2flickr/IMG_7945.JPG"]
'''
files = ["/tmp/Iphone/IMG_4565.JPG", "/tmp/Iphone/IMG_4544.JPG", "/Volumes/Delad/Bilder/Test/20170414_154531.JPG", "/Volumes/Delad/Bilder/Test/Mirjam.JPG", "/tmp/Iphone/KUHB6327.mov"]

#files = "/Volumes/Delad/Bilder/2flickr/CIMG3206.AVI"
#files = "/Volumes/Delad/Bilder/2flickr/P1050137.AVI"
#files = "/Volumes/Delad/Bilder/2flickr/MOV00479.3gp"

def parse_prefix(line, fmt):
    try:
        t = time.strptime(line, fmt)
    except ValueError as v:
        if len(v.args) > 0 and v.args[0].startswith('unconverted data remains: '):
            line = line[:-(len(v.args[0]) - 26)]
            t = time.strptime(line, fmt)
        else:
            raise
    return t

def getdate(intag, infile):
    with exiftool.ExifTool() as et2:
        date = et2.get_tag(intag, infile)
    return date

def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y:%m:%d %H:%M:%S')
    except ValueError:
        return None
    return date_text


with exiftool.ExifTool() as et:
    metadata = et.get_metadata_batch(files)
    print("-"*100)
for d in metadata:
    file = d["SourceFile"]
    filetype = mimetypes.guess_type(file)
    print "FileType", filetype[0]
    date = getdate("EXIF:DateTimeOriginal", file)
    Type = "EXIF:DateTimeOriginal"
    if not date:
        date = getdate("RIFF:DateTimeOriginal", file)
        Type = "RIFF:DateTimeOriginal"
    if not date:
        date = getdate("QuickTime:MediaCreateDate", file)
        Type = "QuickTime:MediaCreateDate"

    if not date:
        date = getdate("FileModifyDate", file)
        Type = "FileModifyDate"
    else:
        if not validate(date):
            date = getdate("FileModifyDate", file)
            Type = "FileModifyDate"


    date = parse_prefix(date, '%Y:%m:%d %H:%M:%S')
    date = time.strftime('%Y-%m-%d %H:%M:%S', date)
    print "Date "+ str(date) +", Type "+ Type +", "+ file
    print("-"*100)
