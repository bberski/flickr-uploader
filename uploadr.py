#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

    flickr-uploader designed for Synology Devices
    Upload a directory of media to Flickr to use as a backup to your local storage.

    Features:

    -Uploads both images and movies (JPG, PNG, GIF, AVI, MOV, 3GP files)
    -Stores image information locally using a simple SQLite database
    -Automatically creates "Sets" based on the folder name the media is in
    -Ignores ".picasabackup" directory
    -Automatically removes images from Flickr when they are removed from your local hard drive

    Requirements:

    -Python 2.7+
    -File write access (for the token and local database)
    -Flickr API key (free)

    Setup:

    Go to http://www.flickr.com/services/apps/create/apply and apply for an API key Edit the following variables in the uploadr.ini

    FILES_DIR = "files/"
    FLICKR = { "api_key" : "", "secret" : "", "title" : "", "description" : "", "tags" : "auto-upload", "is_public" : "0", "is_friend" : "0", "is_family" : "1" }
    SLEEP_TIME = 1 * 60
    DRIP_TIME = 1 * 60
    DB_PATH = os.path.join(FILES_DIR, "fickerdb")
    Place the file uploadr.py in any directory and run:

    $ ./uploadr.py

    It will crawl through all the files from the FILES_DIR directory and begin the upload process.

    Upload files placed within a directory to your Flickr account.

   Inspired by:
        http://micampe.it/things/flickruploadr
        https://github.com/joelmx/flickrUploadr/blob/master/python3/uploadr.py

   Usage:

   cron entry (runs at the top of every hour )
   0  *  *  *  * /full/path/to/uploadr.py > /dev/null 2>&1

   This code has been updated to use the new Auth API from flickr.

   You may use this code however you see fit in any form whatsoever.


"""
import httplib
import sys
import argparse
import mimetools
import mimetypes
import os
import time
import urllib
import urllib2
import webbrowser
import sqlite3 as lite
import json
from xml.dom.minidom import parse
import hashlib
import fcntl
import errno
import subprocess
import re
import ConfigParser
from multiprocessing.pool import ThreadPool
#BBerski
#from ConfigParser import SafeConfigParser
import datetime
import struct
import pyexiftool.exiftool as exiftool
import config
import logging
# encoding=utf8
reload(sys)
sys.setdefaultencoding('utf8')



if sys.version_info < (2, 7):
    sys.stderr.write("This script requires Python 2.7 or newer.\n")
    sys.stderr.write("Current version: " + sys.version + "\n")
    sys.stderr.flush()
    sys.exit(1)

#
# Read Config from .uploadr.ini file
#

# change .uploadr.ini to uploadr.ini


def ppprintX (invar):
    try:
        print invar.split(".")[1],"=", eval(invar)
    except Exception as e :
        print invar.split(".")[1],"= None"

def ppprint (invar):
    print invar.split(".")[1],"=", eval(invar)


def configfileread():


#    if args.configfile :
#        upload_ini = args.configfile
#    else:
#        upload_ini = ".uploadr.ini"
#    print "Config File:", upload_ini

#Global var
    global FILES_DIR
    global FLICKR
    global SLEEP_TIME
    global DRIP_TIME
    global DB_PATH
    global LOCK_PATH
    global TOKEN_PATH
    global EXCLUDED_FOLDERS
    global IGNORED_REGEX
    global ALLOWED_EXT
    global RAW_EXT
    global FILE_MAX_SIZE
    global MANAGE_CHANGES
    global RAW_TOOL_PATH
    global CONVERT_RAW_FILES
    global RAW_SKIP_CREATE_ORIGINAL
    global FULL_SET_NAME
    global SOCKET_TIMEOUT
    global MAX_UPLOAD_ATTEMPTS
    global REMOVE_DELETE_FLICKR
    global FULL_SET_NAME_NEW
    global TITLE_FILENAME
    global TAG_FILENAME
    global TAG_SETNAME
    global WAIT_NEXT_UPLOAD
    global SET_TYPE
    global CHECK_LOCAL_MD5CHECKSUM
    global MAX_UPLOADFILES
    global DAEMON
    global DRY_RUN
    global PROCESSES
    global ALBUM
    global DRIP_FEED
    global TITLE
    global DESCRIPTION
    global TAGS
    global MD5DB
    

#    try:
#        config = ConfigParser.SafeConfigParser()
#        config.read(os.path.join(os.path.dirname(sys.argv[0]), upload_ini))
#    except ConfigParser.ParsingError, err:
#        print 'Could not parse:', err




#    FILES_DIR = eval(config.get('Config', 'FILES_DIR'))
#    FLICKR = eval(config.get('Config', 'FLICKR'))
#    SLEEP_TIME = eval(config.get('Config', 'SLEEP_TIME'))
#    DRIP_TIME = eval(config.get('Config', 'DRIP_TIME'))
#    DB_PATH = eval(config.get('Config', 'DB_PATH'))
#    LOCK_PATH = eval(config.get('Config', 'LOCK_PATH'))
#    TOKEN_PATH = eval(config.get('Config', 'TOKEN_PATH'))
#    EXCLUDED_FOLDERS = eval(config.get('Config', 'EXCLUDED_FOLDERS'))
#    IGNORED_REGEX = [re.compile(regex) for regex in eval(config.get('Config', 'IGNORED_REGEX'))]
#    ALLOWED_EXT = eval(config.get('Config', 'ALLOWED_EXT'))
#    RAW_EXT = eval(config.get('Config', 'RAW_EXT'))
#    FILE_MAX_SIZE = eval(config.get('Config', 'FILE_MAX_SIZE'))
#    MANAGE_CHANGES = eval(config.get('Config', 'MANAGE_CHANGES'))
#    RAW_TOOL_PATH = eval(config.get('Config', 'RAW_TOOL_PATH'))
#    CONVERT_RAW_FILES = eval(config.get('Config', 'CONVERT_RAW_FILES'))
#    RAW_SKIP_CREATE_ORIGINAL = eval(config.get('Config', 'RAW_SKIP_CREATE_ORIGINAL'))
#    FULL_SET_NAME = eval(config.get('Config', 'FULL_SET_NAME'))
#    SOCKET_TIMEOUT = eval(config.get('Config', 'SOCKET_TIMEOUT'))
#    MAX_UPLOAD_ATTEMPTS = eval(config.get('Config', 'MAX_UPLOAD_ATTEMPTS'))
#    REMOVE_DELETE_FLICKR = eval(config.get('Config', 'REMOVE_DELETE_FLICKR'))
#    FULL_SET_NAME_NEW = eval(config.get('Config', 'FULL_SET_NAME_NEW'))
#    TITLE_FILENAME = eval(config.get('Config', 'TITLE_FILENAME'))
#    TAG_FILENAME = eval(config.get('Config', 'TAG_FILENAME'))
#    TAG_SETNAME = eval(config.get('Config', 'TAG_SETNAME'))
#    WAIT_NEXT_UPLOAD = eval(config.get('Config', 'WAIT_NEXT_UPLOAD'))
#    SET_TYPE = eval(config.get('Config', 'SET_TYPE'))
#    CHECK_LOCAL_MD5CHECKSUM = eval(config.get('Config', 'CHECK_LOCAL_MD5CHECKSUM'))

    
    ppprint("args.FILES_DIR")
    ppprint("args.FLICKR")
    ppprint("args.SLEEP_TIME")
    ppprint("args.DRIP_TIME")
    ppprint("args.DB_PATH")
    ppprint("args.LOCK_PATH")
    ppprint("args.TOKEN_PATH")
    ppprint("args.EXCLUDED_FOLDERS")
    ppprint("args.IGNORED_REGEX")
    ppprint("args.ALLOWED_EXT")
    ppprint("args.RAW_EXT")
    ppprint("args.FILE_MAX_SIZE")
    ppprint("args.MANAGE_CHANGES")
    ppprint("args.RAW_TOOL_PATH")
    ppprint("args.CONVERT_RAW_FILES")
    ppprint("args.RAW_SKIP_CREATE_ORIGINAL")
    ppprint("args.FULL_SET_NAME")
    ppprint("args.SOCKET_TIMEOUT")
    ppprint("args.MAX_UPLOAD_ATTEMPTS")
    ppprint("args.REMOVE_DELETE_FLICKR")
    ppprint("args.FULL_SET_NAME_NEW")
    ppprint("args.TITLE_FILENAME")
    ppprint("args.TAG_FILENAME")
    ppprint("args.TAG_SETNAME")
    ppprint("args.WAIT_NEXT_UPLOAD")
    ppprint("args.SET_TYPE")
    ppprint("args.CHECK_LOCAL_MD5CHECKSUM")
    ppprint("args.TITLE")
    ppprint("args.DAEMON")
    ppprint("args.DESCRIPTION")
    ppprint("args.TAGS")
    ppprint("args.DRIP_FEED")
    ppprint("args.PROCESSES")
    ppprint("args.DRY_RUN")
    ppprint("args.REMOVE_IGNORED")
    ppprint("args.MAX_UPLOADFILES")
    ppprint("args.ALBUM")
    ppprint("args.MD5DB")



    FILES_DIR = args.FILES_DIR
    FLICKR=eval(args.FLICKR)
    SLEEP_TIME=eval(args.SLEEP_TIME)
    DRIP_TIME=eval(args.DRIP_TIME)
    DB_PATH=eval(args.DB_PATH)
    LOCK_PATH=eval(args.LOCK_PATH)
    TOKEN_PATH=eval(args.TOKEN_PATH)
    EXCLUDED_FOLDERS=eval(args.EXCLUDED_FOLDERS)
    IGNORED_REGEX=[re.compile(regex) for regex in eval(args.IGNORED_REGEX)]
    ALLOWED_EXT=eval(args.ALLOWED_EXT)
    RAW_EXT=eval(args.RAW_EXT)
    FILE_MAX_SIZE=eval(args.FILE_MAX_SIZE)
    MANAGE_CHANGES=eval(args.MANAGE_CHANGES)
    RAW_TOOL_PATH=eval(args.RAW_TOOL_PATH)
    CONVERT_RAW_FILES=eval(args.CONVERT_RAW_FILES)
    RAW_SKIP_CREATE_ORIGINAL=eval(args.RAW_SKIP_CREATE_ORIGINAL)
    FULL_SET_NAME=eval(args.FULL_SET_NAME)
    SOCKET_TIMEOUT=eval(args.SOCKET_TIMEOUT)
    MAX_UPLOAD_ATTEMPTS=eval(args.MAX_UPLOAD_ATTEMPTS)
    REMOVE_DELETE_FLICKR=eval(args.REMOVE_DELETE_FLICKR)
    FULL_SET_NAME_NEW=eval(args.FULL_SET_NAME_NEW)
    TITLE_FILENAME=eval(args.TITLE_FILENAME)
    TAG_FILENAME=eval(args.TAG_FILENAME)
    TAG_SETNAME=eval(args.TAG_SETNAME)
    WAIT_NEXT_UPLOAD=eval(args.WAIT_NEXT_UPLOAD)
    SET_TYPE=eval(args.SET_TYPE)
    CHECK_LOCAL_MD5CHECKSUM=eval(args.CHECK_LOCAL_MD5CHECKSUM)
    TITLE=args.TITLE
    DAEMON=args.DAEMON
    DESCRIPTION=args.DESCRIPTION
    TAGS=args.TAGS
    DRIP_FEED=args.DRIP_FEED
    PROCESSES=args.PROCESSES
    DRY_RUN=args.DRY_RUN
    REMOVE_IGNORED=args.REMOVE_IGNORED
    MAX_UPLOADFILES=args.MAX_UPLOADFILES
    ALBUM=args.ALBUM
    MD5DB=args.MD5DB

    '''
    FILES_DIR = args.FILES_DIR
    FLICKR=eval(args.FLICKR)
    SLEEP_TIME=eval(args.SLEEP_TIME)
    DRIP_TIME=eval(args.DRIP_TIME)
    DB_PATH=eval(args.DB_PATH)
    LOCK_PATH=eval(args.LOCK_PATH)
    TOKEN_PATH=eval(args.TOKEN_PATH)
    EXCLUDED_FOLDERS=eval(args.EXCLUDED_FOLDERS)
    IGNORED_REGEX=eval(args.IGNORED_REGEX)
    ALLOWED_EXT=eval(args.ALLOWED_EXT)
    RAW_EXT=eval(args.RAW_EXT)
    FILE_MAX_SIZE=eval(args.FILE_MAX_SIZE)
    MANAGE_CHANGES=args.MANAGE_CHANGES
    RAW_TOOL_PATH=args.RAW_TOOL_PATH
    CONVERT_RAW_FILES=args.CONVERT_RAW_FILES
    RAW_SKIP_CREATE_ORIGINAL=args.RAW_SKIP_CREATE_ORIGINAL
    FULL_SET_NAME=args.FULL_SET_NAME
    SOCKET_TIMEOUT=eval(args.SOCKET_TIMEOUT)
    MAX_UPLOAD_ATTEMPTS=args.MAX_UPLOAD_ATTEMPTS
    REMOVE_DELETE_FLICKR=args.REMOVE_DELETE_FLICKR
    FULL_SET_NAME_NEW=args.FULL_SET_NAME_NEW
    TITLE_FILENAME=args.TITLE_FILENAME
    TAG_FILENAME=args.TAG_FILENAME
    TAG_SETNAME=args.TAG_SETNAME
    WAIT_NEXT_UPLOAD=args.WAIT_NEXT_UPLOAD
    SET_TYPE=args.SET_TYPE
    CHECK_LOCAL_MD5CHECKSUM=args.CHECK_LOCAL_MD5CHECKSUM
    TITLE=args.TITLE
    DAEMON=args.DAEMON
    DESCRIPTION=args.DESCRIPTION
    TAGS=args.TAGS
    DRIP_FEED=args.DRIP_FEED
    PROCESSES=args.PROCESSES
    DRY_RUN=args.DRY_RUN
    REMOVE_IGNORED=args.REMOVE_IGNORED
    MAX_UPLOADFILES=args.MAX_UPLOADFILES
    ALBUM=args.ALBUM

    '''

#    sys.exit(0)


#Fixar Lista
'''
1. skip_create_set måste göras om. funkar inte
- inget album
- laddar upp en fil och nästkommande ok, skip_create_set=True
'''


class APIConstants:
    """ APIConstants class
    """

    base = "https://api.flickr.com/services/"
    rest = base + "rest/"
    auth = base + "auth/"
    upload = base + "upload/"
    replace = base + "replace/"

    def __init__(self):
        """ Constructor
       """
        pass


api = APIConstants()


def getdate(intag, infile):
    with exiftool.ExifTool() as et:
        date = et.get_tag(intag, infile)
    return date

def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y:%m:%d %H:%M:%S')
    except ValueError:
        return None
    return date_text

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


#try:
#    import httplib
#except:
#    import http.client as httplib

def have_internet():
    conn = httplib.HTTPConnection("www.google.com", timeout=5)
    try:
        conn.request("HEAD", "/")
        conn.close()
        return True
    except:
        conn.close()
        return False

def movieCreateDate(infile_id, inmov, inlast_modified):
    create_date = getdate("EXIF:DateTimeOriginal", inmov)
    Type = "EXIF:DateTimeOriginal"
    if not create_date:
        create_date = getdate("RIFF:DateTimeOriginal", inmov)
        Type = "RIFF:DateTimeOriginal"
    if not create_date:
        create_date = getdate("QuickTime:MediaCreateDate", inmov)
        Type = "QuickTime:MediaCreateDate"
    if not create_date:
        create_date = getdate("FileModifyDate", inmov)
        Type = "FileModifyDate"
    else:
        if not validate(create_date):
            create_date = getdate("FileModifyDate", inmov)
            Type = "FileModifyDate"
    print "Find Date: "+ str(create_date) +", Type: "+ Type +", "+ inmov
    print "*****It is a movie file, add Date Taken******"
    try:
        create_date = parse_prefix(create_date, '%Y:%m:%d %H:%M:%S')
        create_date = time.strftime('%Y-%m-%d %H:%M:%S', create_date)
        res_set_date = flick.photos_set_dates(infile_id, create_date)
    except (IOError, ValueError, httplib.HTTPException):
        print(str(sys.exc_info()))
        print("Error setting date")
    if res_set_date['stat'] != 'ok':
        raise IOError(res_set_date)
    print("Successfully set date for file: " + inmov.encode('utf-8') + " date: " + str(create_date))

def imageCreateDate(infile_id, inmov, inlast_modified):
    create_date = getdate("EXIF:DateTimeOriginal", inmov)
    Type = "EXIF:DateTimeOriginal"
    if create_date:
        print "EXIF:DateTimeOriginal OK ", inmov
        return True
    if not create_date:
        create_date = getdate("CreateDate", inmov)
        Type = "Create Date"
    if not create_date:
        create_date = getdate("FileModifyDate", inmov)
        Type = "FileModifyDate"
    else:
        if not validate(create_date):
            create_date = getdate("FileModifyDate", inmov)
            Type = "FileModifyDate"
    print "Find Date: "+ str(create_date) +", Type: "+ Type +", "+ inmov
    print "*****It is a image file, add Date Taken******"
    try:
        create_date = parse_prefix(create_date, '%Y:%m:%d %H:%M:%S')
        create_date = time.strftime('%Y-%m-%d %H:%M:%S', create_date)
        res_set_date = flick.photos_set_dates(infile_id, create_date)
    except (IOError, ValueError, httplib.HTTPException):
        print(str(sys.exc_info()))
        print("Error setting date")
    if res_set_date['stat'] != 'ok':
        raise IOError(res_set_date)
    print("Successfully set date for file: " + inmov.encode('utf-8') + " date: " + str(create_date))



class Uploadr:
    """ Uploadr class
    """

    token = None
    perms = ""

    def __init__(self):
        """ Constructor
        """
        self.token = self.getCachedToken()


    def signCall(self, data):
        """
        Signs args via md5 per http://www.flickr.com/services/api/auth.spec.html (Section 8)
        """
        keys = data.keys()
        keys.sort()
        foo = ""
        for a in keys:
            foo += (a + data[a])

        f = FLICKR["secret"] + "api_key" + FLICKR["api_key"] + foo
        return hashlib.md5(f).hexdigest()

    def urlGen(self, base, data, sig):
        """ urlGen
        """
        data['api_key'] = FLICKR["api_key"]
        data['api_sig'] = sig
        encoded_url = base + "?" + urllib.urlencode(data)
        return encoded_url

    def authenticate(self):
        """ Authenticate user so we can upload files
        """

        print("Getting new token")
        self.getFrob()
        self.getAuthKey()
        self.getToken()
        self.cacheToken()

    def getFrob(self):
        """
        flickr.auth.getFrob

        Returns a frob to be used during authentication. This method call must be
        signed.

        This method does not require authentication.
        Arguments

        "api_key" (Required)
        Your API application key. See here for more details.
        """

        d = {
            "method": "flickr.auth.getFrob",
            "format": "json",
            "nojsoncallback": "1"
        }
        sig = self.signCall(d)
        url = self.urlGen(api.rest, d, sig)
        try:
            response = self.getResponse(url)
            if (self.isGood(response)):
                FLICKR["frob"] = str(response["frob"]["_content"])
            else:
                self.reportError(response)
        except:
            print("Error: cannot get frob:" + str(sys.exc_info()))

    def getAuthKey(self):
        """
        Checks to see if the user has authenticated this application
        """
        d = {
            "frob": FLICKR["frob"],
            "perms": "delete"
        }
        sig = self.signCall(d)
        url = self.urlGen(api.auth, d, sig)
        ans = ""
        try:
            webbrowser.open(url)
            print("Copy-paste following URL into a web browser and follow instructions:")
            print(url)
            ans = raw_input("Have you authenticated this application? (Y/N): ")
        except:
            print(str(sys.exc_info()))
        if (ans.lower() == "n"):
            print("You need to allow this program to access your Flickr site.")
            print("Copy-paste following URL into a web browser and follow instructions:")
            print(url)
            print("After you have allowed access restart uploadr.py")
            sys.exit()

    def getToken(self):
        """
        http://www.flickr.com/services/api/flickr.auth.getToken.html

        flickr.auth.getToken

        Returns the auth token for the given frob, if one has been attached. This method call must be signed.
        Authentication

        This method does not require authentication.
        Arguments

        NTC: We need to store the token in a file so we can get it and then check it insted of
        getting a new on all the time.

        "api_key" (Required)
           Your API application key. See here for more details.
        frob (Required)
           The frob to check.
        """

        d = {
            "method": "flickr.auth.getToken",
            "frob": str(FLICKR["frob"]),
            "format": "json",
            "nojsoncallback": "1"
        }
        sig = self.signCall(d)
        url = self.urlGen(api.rest, d, sig)
        try:
            res = self.getResponse(url)
            if (self.isGood(res)):
                self.token = str(res['auth']['token']['_content'])
                self.perms = str(res['auth']['perms']['_content'])
                self.cacheToken()
            else:
                self.reportError(res)
        except:
            print(str(sys.exc_info()))

    def getCachedToken(self):
        """
        Attempts to get the flickr token from disk.
       """
#        print "TYP", type(TOKEN_PATH)
#        print "VAR", TOKEN_PATH
        if (os.path.exists(TOKEN_PATH)):
#            print open(TOKEN_PATH).read()
            return open(TOKEN_PATH).read()
        else:
            return None

    def cacheToken(self):
        """ cacheToken
        """

        try:
            open(TOKEN_PATH, "w").write(str(self.token))
        except:
            print("Issue writing token to local cache ", str(sys.exc_info()))

    def checkToken(self):
        """
        flickr.auth.checkToken

        Returns the credentials attached to an authentication token.
        Authentication

        This method does not require authentication.
        Arguments

        "api_key" (Required)
            Your API application key. See here for more details.
        auth_token (Required)
            The authentication token to check.
        """

        if (self.token == None):
            return False
        else:
            d = {
                "auth_token": str(self.token),
                "method": "flickr.auth.checkToken",
                "format": "json",
                "nojsoncallback": "1"
            }
            sig = self.signCall(d)
            url = self.urlGen(api.rest, d, sig)
            try:
                res = self.getResponse(url)
                if (self.isGood(res)):
                    self.token = res['auth']['token']['_content']
                    self.perms = res['auth']['perms']['_content']
                    return True
                else:
                    self.reportError(res)
            except:
                print(str(sys.exc_info()))
            return False

    def removeIgnoredMedia(self):
        print("*****Removing ignored files*****")

        if (not self.checkToken()):
            self.authenticate()
        con = lite.connect(DB_PATH)
        con.text_factory = str

        with con:
            cur = con.cursor()
            cur.execute("SELECT files_id, path FROM files")
            rows = cur.fetchall()

            for row in rows:
                if (self.isFileIgnored(row[1].decode('utf-8'))):
                    success = self.deleteFile(row, cur)
        print("*****Completed ignored files*****")

    def removeDeletedMedia(self):
        """ Remove files deleted at the local source
        loop through database
        check if file exists
        if exists, continue
        if not exists, delete photo from fickr
        http://www.flickr.com/services/api/flickr.photos.delete.html
        """

        print("*****Removing deleted files*****")

        if (not self.checkToken()):
            self.authenticate()
        con = lite.connect(DB_PATH)
        con.text_factory = str

        with con:
            cur = con.cursor()
            cur.execute("SELECT files_id, path FROM files")
            rows = cur.fetchall()

            for row in rows:
                if (not os.path.isfile(row[1].decode('utf-8'))):
                    success = self.deleteFile(row, cur)
        print("*****Completed deleted files*****")


    def photos_create_dict_checksum(self, infile):
        file_checksum = self.md5Checksum(infile)
        if file_checksum:
            return (file_checksum, infile)

    def photos_create_md5_checksum(self, infile):
        file_checksum = self.md5Checksum(infile)
        if file_checksum:
            return file_checksum

    def photos_search_checksum(self, infile):
        file_checksum = self.md5Checksum(infile)
        search = self.photos_search(file_checksum)
#        print "search", search
        if search:
            if int(search["photos"]["total"]) > 0:
                if MD5DB:
                    #Fixa Set/Album
                    file_id = search["photos"]["photo"][0]["id"]
                    file_info = self.photos_getallcontexts(file_id)
                    if 'set' in file_info.keys():
                        photo_set = file_info["set"]
                    if photo_set:
                        #Borde fixa att välja största id set/album, 0 verkar vara den sist skapade.
                        set_id = photo_set[0]["id"]
                        set_name = photo_set[0]["title"]
                    file = infile
                    last_modified = os.stat(file).st_mtime;
                    set_id = photo_set[0]["id"]
                    set_name = photo_set[0]["title"]
                    con = lite.connect(DB_PATH)
                    with con:
                        cur = con.cursor()
                        cur.execute(
                        'INSERT INTO files (files_id, path, set_id, md5, last_modified, tagged) VALUES (?, ?, ?, ?, ?, 1)',
                            (file_id, file, set_id, file_checksum, last_modified))
                        print("OK on Flickr" + file + " add in DB to set "+ set_name)
#                print "On Flickr"
                file_name = search["photos"]["photo"][0]["title"]
                print "Search on Flickr:"+ infile +" md5Checksum:"+ file_checksum + " = On Flickr img:" + file_name
                return None
            else:
                print "Search on Flickr:"+ infile +" md5Checksum:"+ file_checksum + " = Not on Flickr" 
#                print "Not on Flickr"
                return infile
        else:
            logging.info("---PHOTO SEARCH CHECKSUM ERROR---")
            logging.info(infile)
            return infile



    def check_local_duplicate_checksum(self, inlist):
        print("*****Check duplicate files local*****")
        md5Dict = {}
        md5List =[]
        for infile in inlist:
            file_checksum = self.md5Checksum(infile)
            md5Dict[file_checksum] = infile
        if md5Dict:
            md5List = md5Dict.values()
            duplicatenr = len(inlist)-len(md5List)
            print "Local duplicate file(s): " + str(duplicatenr)
        return md5List


    def upload(self):
        """ upload
        """

        print("*****Uploading files*****")
        print("**"+FILES_DIR+"**")

        allMedia = self.grabNewFiles()
        self.maxFiles = [0]
        # If managing changes, consider all files
        if MANAGE_CHANGES:
            changedMedia = allMedia
        # If not, then get just the new and missing files
        else:
            con = lite.connect(DB_PATH)
            with con:
                cur = con.cursor()
                cur.execute("SELECT path FROM files")
                existingMedia = set(file[0] for file in cur.fetchall())
                changedMedia = set(allMedia) - existingMedia
        changedMedia_count = len(changedMedia)

        print("Found " + str(changedMedia_count) + " files")
#Måste nog flytta CHECK_LOCAL_MD5CHECKSUM innan process kontroll
        if PROCESSES:
            if WAIT_NEXT_UPLOAD:
                print("-"*100)
                print("******Warning no WAIT_NEXT_UPLOAD************")
                print("-"*100)
            if len(changedMedia) > 0:
                self.pool = ThreadPool(processes=int(PROCESSES))

##              #lägga in try här, fick (error(65, 'No route to host'),)
#        try:
#            self.mypage = urllib2.urlopen(self.url + 'MainPage.htm', timeout=30).read()
#        except urllib2.URLError:
#            sys.stderr.write("Error: system at %s not responding\n" % self.url)
#            sys.exit(1)
                if MD5DB:
                    print "*****Check md5 against DB*****"
                    resultat_dict = dict(self.pool.map(self.photos_create_dict_checksum, changedMedia))
                    resultat_md5 = self.pool.map(self.photos_create_md5_checksum, changedMedia)
                    con = lite.connect(DB_PATH)
                    with con:
                        cur = con.cursor()
                        cur.execute("SELECT md5 FROM files")
                        dbmd5Media = set(file[0] for file in cur.fetchall())
                        changedmd5Media = set(resultat_md5) - dbmd5Media
                    new = [resultat_dict[x] for x in changedmd5Media]
                    changedMedia = new

                print "Number of new:", len(changedMedia)
                resultat = self.pool.map(self.photos_search_checksum, changedMedia)
                resultat = filter(None, resultat)
                self.pool.close() #we are not adding any more processes
                self.pool.join() #tell it to wait until all threads are done before going on
                if CHECK_LOCAL_MD5CHECKSUM:
                    resultat = self.check_local_duplicate_checksum(resultat)
                resultat = sorted(resultat)

                if MAX_UPLOADFILES:
                    self.Media_count = int(MAX_UPLOADFILES)
                    resultat = resultat[0:int(MAX_UPLOADFILES)]
                else:
                    self.Media_count = len(resultat)

                self.pool = ThreadPool(processes=int(PROCESSES))
                success = self.pool.map(self.uploadFile, resultat)
                self.pool.close() #we are not adding any more processes
                self.pool.join() #tell it to wait until all threads are done before going on
                if int(self.maxFiles[0])  >= int(PROCESSES):
                    print "Max success uploaded files: "+ str(self.maxFiles[0])
                    print("-"*100)
                    return 
        else:
            if MD5DB:
                print "*****Check md5 against DB*****"
                count = 0
                resultat_dict = {}
                for i, file in enumerate(changedMedia):
                    resultat = self.photos_create_dict_checksum(file)
                    resultat_dict[resultat[0]] = resultat[1]

                count = 0
                resultat_md5 = []
                for i, file in enumerate(changedMedia):
                    resultat = self.photos_create_md5_checksum(file)
                    resultat_md5.append(resultat)

                con = lite.connect(DB_PATH)
                with con:
                    cur = con.cursor()
                    cur.execute("SELECT md5 FROM files")
                    dbmd5Media = set(file[0] for file in cur.fetchall())
                    changedmd5Media = set(resultat_md5) - dbmd5Media
                new = [resultat_dict[x] for x in changedmd5Media]
                changedMedia = new
            print "Number of new:", len(changedMedia)

            count = 0
            resultat = []
            for i, file in enumerate(changedMedia):
                res = self.photos_search_checksum(file)
                resultat.append(res)

            changedMedia = filter(None, resultat)

            if MAX_UPLOADFILES:
                self.Media_count = int(MAX_UPLOADFILES)
            else:
                self.Media_count = len(changedMedia)

            count = 0
            for i, file in enumerate(changedMedia):
                print("-"*100)
                success = self.uploadFile(file)
                if DRIP_FEED and success and i != changedMedia_count - 1:
                    print("Waiting " + str(DRIP_TIME) + " seconds before next upload")
                    time.sleep(DRIP_TIME)
                if success == "success":
                    count = count + 1;
                #Om MAX_UPLOADFILES uppnått
                if (success  == "Stop"):
                    count = count + 1;
                    print "Max success uploaded files: "+ str(self.maxFiles[0])
                    print("" + str(count) + " files processed (uploaded, md5ed or timestamp checked)")
                    print("-"*100)
                    return
                if (count % 100 == 0):
                    print("" + str(count) + " files processed (uploaded, md5ed or timestamp checked)")
            if (count % 100 > 0):
                print("" + str(count) + " files processed (uploaded, md5ed or timestamp checked)")
        print("-"*100)
        print("*****Completed uploading files*****")

    def get_photo_datetime(self, photo):
        try:
            photo_date = getdate("EXIF:DateTimeOriginal", photo)
        except ValueError:
            # Unable to parse photo title as datetime
            pass
        photo_date = datetime.datetime.strptime(photo_date, '%Y:%m:%d %H:%M:%S')
        return photo_date

    def set_timestamp_if_different(self, photo_datetime, filename):
        """Set the access and modified times of a file to the specified
        datetime.

        Args:
            photo_datetime (datetime.datetime)
        """
        try:
            timestamp = time.mktime(photo_datetime.timetuple())
            if timestamp != os.path.getmtime(filename):
                os.utime(filename, (timestamp, timestamp))
        except OverflowError:
            self._progress('Error updating timestamp for: %s' % filename)

    def checkRaw(self, infilename, ext):
        dirpath = os.path.dirname(os.path.abspath(infilename))
        filename = os.path.basename(infilename)
        fileExt = filename.split(".")[-1]
        filename = filename.split(".")[0]
        if (os.path.exists(dirpath + "/" + filename + "." + ext)) and (not os.path.exists(dirpath + "/" + filename + ".JPG")):
            return True
        else:
            return False

    def grabNewRawFiles(self, infiles):
        files = []
        for ext in RAW_EXT:
            print ("About to convert files with extension:" + ext + " files.")
            for f in infiles:
                checkraw = self.checkRaw(f, ext)
                if checkraw:
                    dirpath = os.path.dirname(os.path.abspath(f))
                    files.append(os.path.normpath(f).replace("'", "\'"))
        files.sort()
        return files



    def grabNewAllFiles(self):
        """ grabNewAllFiles
        """
        files = []
        for dirpath, dirnames, filenames in os.walk(unicode(FILES_DIR), followlinks=True):
            if '.picasaoriginals' in dirnames:
                dirnames.remove('.picasaoriginals')
            if '@eaDir' in dirnames:
                dirnames.remove('@eaDir')
            for f in filenames:
                filePath = os.path.join(dirpath, f)
                if self.isFileIgnored(filePath):
                    print "Ignored dir: ", filePath
                    continue
                if any(ignored.search(f) for ignored in IGNORED_REGEX):
                    print "Ignored: ", f
                    continue
                files.append(os.path.normpath(dirpath + "/" + f).replace("'", "\'"))
        files.sort()
        return files


#Kanske lite klumpig filnamn...

    def convertRawFilesRun(self, infilename):
        dirpath = os.path.dirname(os.path.abspath(infilename))
        filename = os.path.basename(infilename)
        fileExt = filename.split(".")[-1]
        filename = filename.split(".")[0]
        ext = fileExt.lower()
#        if (not os.path.exists(dirpath + "/" + filename + ".JPG")):
        if (os.path.exists(infilename)) and (not os.path.exists(dirpath + "/" + filename + ".JPG")) :
            print("About to create JPG from raw " + infilename)
    
            flag = ""
            if ext == "cr2":
                flag = "PreviewImage"
            else:
                flag = "JpgFromRaw"
    
            command = RAW_TOOL_PATH + "exiftool -b -" + flag + " -w .JPG -ext " + ext + " -r '" + infilename + "'"
            print(command)
    
            p = subprocess.call(command, shell=True)
            #Gör smartare
            if (RAW_SKIP_CREATE_ORIGINAL):
                command = RAW_TOOL_PATH + "exiftool -overwrite_original -tagsfromfile '" + infilename + "' -r -all:all -ext JPG '" + dirpath + "/" + filename + ".JPG'"
                print ("Skip create "+ dirpath + "/" + filename + ".JPG_original")
                print ("About to copy tags from " + infilename + " to JPG.")
                p = subprocess.call(command, shell=True)
                print ("Finished copying tags.")
            else:
                if (not os.path.exists(dirpath + "/" + filename + ".JPG_original")):
                    print ("Create "+ dirpath + "/" + filename + ".JPG_original")
                    command = RAW_TOOL_PATH + "exiftool -tagsfromfile '" + infilename + "' -r -all:all -ext JPG '" + dirpath + "/" + filename + ".JPG'"
                    print ("About to copy tags from " + infilename + " to JPG.")
                    p = subprocess.call(command, shell=True)
                    print ("Finished copying tags.")
    
            photo = dirpath + "/" + filename + ".JPG"
            photo_date = self.get_photo_datetime(photo)
            self.set_timestamp_if_different(photo_date, photo)

    def convertRawFiles(self):
        """ convertRawFiles
        """
        if (not CONVERT_RAW_FILES):
            return

        print "*****Converting files*****"
        filenames = self.grabNewAllFiles()
        filenamesraw = self.grabNewRawFiles(filenames)
        set_max = 0
        filenames = sorted(filenames)
        filenamesraw = sorted(filenamesraw)
        if len(filenamesraw) > 0:
            if not os.path.isfile(RAW_TOOL_PATH + "exiftool"):
                print "Wrong path to exiftool"
                print "RAW_TOOL_PATH = " + RAW_TOOL_PATH
                sys.exit()
        if PROCESSES:
            if len(filenamesraw) > 0:
                if MAX_UPLOADFILES:
                    filenames = filenamesraw[0:int(MAX_UPLOADFILES)]
                self.pool = ThreadPool(processes=int(PROCESSES))
                self.pool.map(self.convertRawFilesRun, filenames)
                self.pool.close() #we are not adding any more processes
                self.pool.join() #tell it to wait until all threads are done before going on
        else:
            for f in filenamesraw:
                dirpath = os.path.dirname(os.path.abspath(f))
                f2 = os.path.basename(f)
                fileExt = f2.split(".")[-1]
                filename = f2.split(".")[0]
                ext = fileExt.lower()
                if (not os.path.exists(dirpath + "/" + filename + ".JPG")):
                    print("About to create JPG from raw " + f)

                    flag = ""
                    if ext == 'cr2':
                        flag = "PreviewImage"
                    else:
                        flag = "JpgFromRaw"

                    command = RAW_TOOL_PATH + "exiftool -b -" + flag + " -w .JPG -ext " + ext + " -r '" + f + "'"
                    print(command)
                    p = subprocess.call(command, shell=True)
#Gör smartare
                    if (RAW_SKIP_CREATE_ORIGINAL):
                        command = RAW_TOOL_PATH + "exiftool -overwrite_original -tagsfromfile '" + f + "' -r -all:all -ext JPG '" + dirpath + "/" + filename + ".JPG'"
                        print ("Skip create "+ dirpath + "/" + filename + ".JPG_original")
                        print ("About to copy tags from " + f + " to JPG.")
                        p = subprocess.call(command, shell=True)
                        print ("Finished copying tags.")
                    else:
                        if (not os.path.exists(dirpath + "/" + filename + ".JPG_original")):
                            print ("Create "+ dirpath + "/" + filename + ".JPG_original")
                            command = RAW_TOOL_PATH + "exiftool -tagsfromfile '" + f + "' -r -all:all -ext JPG '" + dirpath + "/" + filename + ".JPG'"
                            print ("About to copy tags from " + f + " to JPG.")
                            p = subprocess.call(command, shell=True)
                            print ("Finished copying tags.")

                    photo = dirpath + "/" + filename + ".JPG"
                    photo_date = self.get_photo_datetime(photo)
                    self.set_timestamp_if_different(photo_date, photo)
                    set_max = set_max + 1
                    if MAX_UPLOADFILES:
                        if (set_max >= int(MAX_UPLOADFILES)):
                            return

        print "*****Completed converting files*****"

    def grabNewFiles(self):
        """ grabNewFiles
        """

        files = []
        for dirpath, dirnames, filenames in os.walk(unicode(FILES_DIR), followlinks=True):
            for f in filenames:
                filePath = os.path.join(dirpath, f)
                if self.isFileIgnored(filePath):
                    continue
                if any(ignored.search(f) for ignored in IGNORED_REGEX):
                    print "Ignored: ", f
                    continue
                ext = os.path.splitext(os.path.basename(f))[1][1:].lower()
                if ext in ALLOWED_EXT:
                    fileSize = os.path.getsize(dirpath + "/" + f)
                    if (fileSize < FILE_MAX_SIZE):
                        files.append(os.path.normpath(dirpath + "/" + f).replace("'", "\'"))
                    else:
                        print("Skipping file due to size restriction: " + ( os.path.normpath( dirpath.encode('utf-8') + "/" + f.encode('utf-8') ) ) )
        files.sort()
        return files

    def isFileIgnored(self, filename):
        for excluded_dir in EXCLUDED_FOLDERS:
            if excluded_dir in os.path.dirname(filename):
                return True

        return False

    def uploadFile(self, file):
        """ uploadFile
        """
        if DRY_RUN :
            print("Dry Run Uploading: " + file + "...")
            return True
        success = False
        con = lite.connect(DB_PATH)
        con.text_factory = str
        with con:
            cur = con.cursor()
            cur.execute("SELECT rowid,files_id,path,set_id,md5,tagged,last_modified FROM files WHERE path = ?", (file,))
            row = cur.fetchone()
            print("Check: " + file + "...")
            last_modified = os.stat(file).st_mtime;
            file_checksum = self.md5Checksum(file)
            search_result = self.photos_search(file_checksum)
            photo_set = None
            if int(search_result["photos"]["total"]) > 0 and row is None:
                print "Photo/Movie already exist on Flickr: "+ file +" md5="+ file_checksum +" not in DB, fixit"
                #Fixa Set/Album
                file_id = search_result["photos"]["photo"][0]["id"]
                file_info = self.photos_getallcontexts(file_id)
                if 'set' in file_info.keys():
                    photo_set = file_info["set"]
                if photo_set:
                    #Borde fixa att välja största id set/album, 0 verkar vara den sist skapade.
                    set_id = photo_set[0]["id"]
                    set_name = photo_set[0]["title"]
                    cur.execute(
                    'INSERT INTO files (files_id, path, set_id, md5, last_modified, tagged) VALUES (?, ?, ?, ?, ?, 1)',
                        (file_id, file, set_id, file_checksum, last_modified))
                    print(file + " add in DB to set "+ set_name)
                else:
#Temp lösning att set_id = ""
                    cur.execute(
                    'INSERT INTO files (files_id, path, set_id, md5, last_modified, tagged) VALUES (?, ?, ?, ?, ?, 1)',
                        (file_id, file, "", file_checksum, last_modified))
                    print(file + " no set on Flickr")
                return False
            if int(search_result["photos"]["total"]) > 0 and row:
                print("Flickr ok DB ok " + file + "...")
                return False                
            if int(search_result["photos"]["total"]) == 0 and row:
                print "??? In DB but not on Flickr, fixit ...."
                self.deleteFiledb(row)
                row = None
            if row is None:
                print("Uploading: " + file + "...")

                print("File <" + str(self.maxFiles[0] + 1) + "><" + str(self.Media_count) + ">")
                if FULL_SET_NAME_NEW:
                    if FULL_SET_NAME:
                        setName = str(datetime.datetime.now().strftime('%Y/%m/%d'))
                    else:
                        setName = str(datetime.datetime.now().strftime('%Y%m%d'))
                else:
                    if FULL_SET_NAME:
                        setName = os.path.relpath(os.path.dirname(file), FILES_DIR)
                    else:
                        head, setName = os.path.split(os.path.dirname(file))
                try:
                    photo = ('photo', file.encode('utf-8'), open(file, 'rb').read())
                    if TITLE:  # Replace
                        FLICKR["title"] = TITLE
                    if DESCRIPTION:  # Replace
                        FLICKR["description"] = DESCRIPTION
                    if TAGS:  # Append
                        FLICKR["tags"] += " " + TAGS
                    if TITLE_FILENAME:
                        base=os.path.basename(file)
                        FLICKR["title"] = os.path.splitext(base)[0]
                    d = {
                        "auth_token": str(self.token),
                        "perms": str(self.perms),
                        "title": str(FLICKR["title"]),
                        "description": str(FLICKR["description"]),
                        # replace commas to avoid tags conflicts
                        "tags": '{} {} checksum:{}'.format(FLICKR["tags"], setName.encode('utf-8'), file_checksum).replace(',', ''),
                        "is_public": str(FLICKR["is_public"]),
                        "is_friend": str(FLICKR["is_friend"]),
                        "is_family": str(FLICKR["is_family"])
                    }
                    sig = self.signCall(d)
                    d["api_sig"] = sig
                    d["api_key"] = FLICKR["api_key"]
                    url = self.build_request(api.upload, d, (photo,))
                    res = None
                    search_result = None
#                    for x in range(0, MAX_UPLOAD_ATTEMPTS):
#                        try:
                    res = parse(urllib2.urlopen(url, timeout=SOCKET_TIMEOUT))
#                            res = urllib2.urlopen(url, timeout=SOCKET_TIMEOUT)
#                            print "RES1", res, url
#                            print str(res.toxml())
                    search_result = None
                    status = res.documentElement.attributes['stat'].value
                    if res.documentElement.attributes['stat'].value == "ok":
                        photoID = res.getElementsByTagName("photoid")[0].childNodes[0].data
                        print "*** File: <" +file+ "> Status: <" +status+ ">, FlickrId: <" +photoID+ "> ***"
                        self.maxFiles[0] =  self.maxFiles[0] + 1
                        success = "success"
                    else:
                        plist = res.getElementsByTagName("err")[0]
                        errCode = plist.attributes["code"].value
                        msgTxt = plist.attributes["msg"].value
                        print "***VARNING File: <" +file+ "> Status: <" +status+ ">, Errcode: <" +errCode+ ">, Msg: <" +msgTxt+ "> ***"
                        logging.info("***VARNING File: <" +file+ "> Status: <" +status+ ">, Errcode: <" +errCode+ ">, Msg: <" +msgTxt+ "> ***")
                        logging.info("---xml info---")
                        logging.info(str(res.toxml()))
#                        success = False
                        return False
#                                return "error"

#                        except (IOError, httplib.HTTPException): #Om uppladdning misslyckas, kolla om filen kommit upp.
#                        print "RES2", res
#                        print(str(sys.exc_info()))
#                        print("Check is file already uploaded, sleep 10 s.")
#                        time.sleep(10)
#                        search_result = self.photos_search(file_checksum)
#                        if search_result["stat"] != "ok":
#                            raise IOError(search_result)

#                        if int(search_result["photos"]["total"]) == 0:
#                            if x == MAX_UPLOAD_ATTEMPTS - 1:
#                                raise ValueError("Reached maximum number of attempts to upload, skipping")

#                            print("Not found, reuploading")
#                            continue

#                        if int(search_result["photos"]["total"]) > 1:
#                            raise IOError("More then one file with same checksum, collisions? " + search_result)

#                        if int(search_result["photos"]["total"]) == 1:
#                            break
                    search_result = self.photos_search(file_checksum)
                    if not search_result and res.documentElement.attributes['stat'].value != "ok":
                        print("A problem occurred while attempting to upload the file: " + file)
                        raise IOError(str(res.toxml()))

                    print("Successfully uploaded the file: " + file)
                    print "*****Add tag", FLICKR["tags"] + " to " + file

                    if WAIT_NEXT_UPLOAD:
                        search_result = self.photos_search(file_checksum)
                        while (int(search_result["photos"]["total"])) == 0:
                            print("Waiting 0.5 second check "+ file +" exist on Flickr")
                            time.sleep(.5)
                            search_result = self.photos_search(file_checksum)
                        print(file +" ok on Flickr")

                    if int(search_result["photos"]["total"]) == 0:
                        search_result = None
                    if search_result:
                        file_id = int(search_result["photos"]["photo"][0]["id"])
                    else:
                        file_id = int(str(res.getElementsByTagName('photoid')[0].firstChild.nodeValue))
                    #Add tags
                    if TAG_SETNAME:
                        if FULL_SET_NAME_NEW:
                            if FULL_SET_NAME:
                                res_add_tag = self.photos_add_tag(file_id, str(datetime.datetime.now().strftime('%Y/%m/%d')), file)
                            else:
                                res_add_tag = self.photos_add_tag(file_id, str(datetime.datetime.now().strftime('%Y%m%d')), file)
                    if TAG_FILENAME:
                        base=os.path.basename(file)
                        fileName = os.path.splitext(base)[0]
                        res_add_tag = self.photos_add_tag(file_id, fileName, file)
                    #Get exif Create_date or FileModifyDate
                    filetype = mimetypes.guess_type(file)
                    if 'video' in filetype[0]:
                        movieCreateDate(file_id, file, last_modified)
                    #Check exif:date
                    if 'image' in filetype[0]:
                        imageCreateDate(file_id, file, last_modified)
                    # Add to db
                    cur.execute(
                        'INSERT INTO files (files_id, path, md5, last_modified, tagged) VALUES (?, ?, ?, ?, 1)',
                        (file_id, file, file_checksum, last_modified))

                    success = "success"
                except:
                    print(str(sys.exc_info()))

            elif MANAGE_CHANGES:
                if int(search_result["photos"]["total"]) > 0:
                    print "Photo already exist on Flickr: "+ file +" md5="+ file_checksum
                    success = False
                if (row[6] == None):
                    cur.execute('UPDATE files SET last_modified = ? WHERE files_id = ?', (last_modified, row[1]))
                    con.commit()
                if (row[6] != last_modified):
                    fileMd5 = self.md5Checksum(file)
                    if (fileMd5 != str(row[4])):
                        self.replacePhoto(file, row[1], row[4], fileMd5, last_modified, cur, con);
#            if success == "success":
#                self.maxFiles =  self.maxFiles + 1
            if MAX_UPLOADFILES:
                if  int(self.maxFiles[0]) >= int(MAX_UPLOADFILES):
                    return "Stop"
            return success

    def replacePhoto(self, file, file_id, oldFileMd5, fileMd5, last_modified, cur, con):

        if DRY_RUN :
            print("Dry Run Replace file " + file + "...")
            return True

        success = False
        print("Replacing the file: " + file + "...")
        try:
            photo = ('photo', file.encode('utf-8'), open(file, 'rb').read())

            d = {
                "auth_token": str(self.token),
                "photo_id": str(file_id)
            }
            sig = self.signCall(d)
            d["api_sig"] = sig
            d["api_key"] = FLICKR["api_key"]
            url = self.build_request(api.replace, d, (photo,))
            #Get exif Create_date or FileModifyDate
            filetype = mimetypes.guess_type(file)
            if 'video' in filetype[0]:
                movieCreateDate(file_id, file, last_modified)
            res = None
            res_add_tag = None
            res_get_info = None
            for x in range(0, MAX_UPLOAD_ATTEMPTS):
                try:
                    res = parse(urllib2.urlopen(url, timeout=SOCKET_TIMEOUT))
                    if res.documentElement.attributes['stat'].value == "ok":
                        photo_name = os.path.basename(file)
                        res_add_tag = self.photos_add_tags(file_id, ['checksum:{}'.format(fileMd5)], file)
                        if res_add_tag['stat'] == 'ok':
                            res_get_info = flick.photos_get_info(file_id)
                            if res_get_info['stat'] == 'ok':
                                tag_id = None
                                for tag in res_get_info['photo']['tags']['tag']:
                                    if tag['raw'] == 'checksum:{}'.format(oldFileMd5):
                                        tag_id = tag['id']
                                        break
                                if not tag_id:
                                    print("Can't find tag {} for file {}".format(tag_id, file_id))
                                    break
                                else:
                                    self.photos_remove_tag(tag_id)
                    break
                except (IOError, ValueError, httplib.HTTPException):
                    print(str(sys.exc_info()))
                    print("Replacing again")
                    time.sleep(5)

                    if x == MAX_UPLOAD_ATTEMPTS - 1:
                        raise ValueError("Reached maximum number of attempts to replace, skipping")
                    continue

            if res.documentElement.attributes['stat'].value != "ok" \
                    or res_add_tag['stat'] != 'ok' \
                    or res_get_info['stat'] != 'ok':
                print("A problem occurred while attempting to upload the file: " + file)

            if res.documentElement.attributes['stat'].value != "ok":
                raise IOError(str(res.toxml()))

            if res_add_tag['stat'] != 'ok':
                raise IOError(res_add_tag)

            if res_get_info['stat'] != 'ok':
                raise IOError(res_get_info)

            print("Successfully replaced the file: " + file)

            # Add to set
            cur.execute('UPDATE files SET md5 = ?,last_modified = ? WHERE files_id = ?',
                        (fileMd5, last_modified, file_id))
            con.commit()
            success = True
        except:
            print(str(sys.exc_info()))

        return success

    def deleteFile(self, file, cur):

        if DRY_RUN :
            print("Deleting file: " + file[1].decode('utf-8'))
            return True

        success = False
        print("Deleting file: " + file[1].decode('utf-8'))

        try:
            d = {
                # FIXME: double format?
                "auth_token": str(self.token),
                "perms": str(self.perms),
                "format": "rest",
                "method": "flickr.photos.delete",
                "photo_id": str(file[0]),
                "format": "json",
                "nojsoncallback": "1"
            }
            sig = self.signCall(d)
            url = self.urlGen(api.rest, d, sig)
            res = self.getResponse(url)
            if (self.isGood(res)):

                # Find out if the file is the last item in a set, if so, remove the set from the local db
                cur.execute("SELECT set_id FROM files WHERE files_id = ?", (file[0],))
                row = cur.fetchone()
                cur.execute("SELECT set_id FROM files WHERE set_id = ?", (row[0],))
                rows = cur.fetchall()
                if (len(rows) == 1):
                    print("File is the last of the set, deleting the set ID: " + str(row[0]))
                    cur.execute("DELETE FROM sets WHERE set_id = ?", (row[0],))

                # Delete file record from the local db
                cur.execute("DELETE FROM files WHERE files_id = ?", (file[0],))
                print("Successful deletion.")
                success = True
            else:
                if (res['code'] == 1):
                    # File already removed from Flicker
                    cur.execute("DELETE FROM files WHERE files_id = ?", (file[0],))
                else:
                    self.reportError(res)
        except:
            # If you get 'attempt to write a readonly database', set 'admin' as owner of the DB file (fickerdb) and 'users' as group
            print(str(sys.exc_info()))
        return success

    def deleteFiledb(self, file):

        if DRY_RUN :
            print("Deleting file in DB: " + file[2].decode('utf-8'))
            return True

        success = False
        print("Deleting file in DB: " + file[2].decode('utf-8'))
        con = lite.connect(DB_PATH)
        con.text_factory = str
        cur = con.cursor()
        cur.execute("SELECT files_id FROM files WHERE files_id = ?", (file[1],))
        row = cur.fetchone()
        # Delete file record from the local db
        cur.execute("DELETE FROM files WHERE files_id = ?", (file[1],))
        con.commit()
        print("Successful deletion in DB file: "+ file[2].decode('utf-8'))
        success = True
#        except:
#            # If you get 'attempt to write a readonly database', set 'admin' as owner of the DB file (fickerdb) and 'users' as group
#            print(str(sys.exc_info()))
        return success


    def logSetCreation(self, setId, setName, primaryPhotoId, cur, con):
        print("adding set to DB: " + setName.decode('utf-8'))
        success = False
        cur.execute("INSERT INTO sets (set_id, name, primary_photo_id) VALUES (?,?,?)",
                    (setId, setName, primaryPhotoId))
#        cur.execute("UPDATE files SET set_id = ? WHERE files_id = ?", (setId, primaryPhotoId))
        con.commit()
        return True

    def build_request(self, theurl, fields, files, txheaders=None):
        """
        build_request/encode_multipart_formdata code is from www.voidspace.org.uk/atlantibots/pythonutils.html

        Given the fields to set and the files to encode it returns a fully formed urllib2.Request object.
        You can optionally pass in additional headers to encode into the opject. (Content-type and Content-length will be overridden if they are set).
        fields is a sequence of (name, value) elements for regular form fields - or a dictionary.
        files is a sequence of (name, filename, value) elements for data to be uploaded as files.
        """

        content_type, body = self.encode_multipart_formdata(fields, files)
        if not txheaders: txheaders = {}
        txheaders['Content-type'] = content_type
        txheaders['Content-length'] = str(len(body))

        return urllib2.Request(theurl, body, txheaders)

    def encode_multipart_formdata(self, fields, files, BOUNDARY='-----' + mimetools.choose_boundary() + '-----'):
        """ Encodes fields and files for uploading.
        fields is a sequence of (name, value) elements for regular form fields - or a dictionary.
        files is a sequence of (name, filename, value) elements for data to be uploaded as files.
        Return (content_type, body) ready for urllib2.Request instance
        You can optionally pass in a boundary string to use or we'll let mimetools provide one.
        """

        CRLF = '\r\n'
        L = []
        if isinstance(fields, dict):
            fields = fields.items()
        for (key, value) in fields:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"' % key)
            L.append('')
            L.append(value)
        for (key, filename, value) in files:
            filetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
            L.append('Content-Type: %s' % filetype)
            L.append('')
            L.append(value)
        L.append('--' + BOUNDARY + '--')
        L.append('')
        body = CRLF.join(L)
        content_type = 'multipart/form-data; boundary=%s' % BOUNDARY  # XXX what if no files are encoded
        return content_type, body

    def isGood(self, res):
        """ isGood
        """

        if (not res == "" and res['stat'] == "ok"):
            return True
        else:
            return False

    def reportError(self, res):
        """ reportError
        """

        try:
            print("Error: " + str(res['code'] + " " + res['message']))
        except:
            print("Error: " + str(res))

    def getResponse(self, url):
        """
        Send the url and get a response.  Let errors float up
        """
        res = None
        try:
            res = urllib2.urlopen(url, timeout=SOCKET_TIMEOUT).read()
        except urllib2.HTTPError, e:
            print(e.code)
            print "urllib2.HTTPError"
            logging.info("---urllib2.HTTPError---")
            logging.info(url)
            logging.info(e)
            return None
        except urllib2.URLError, e:
            print(e.args)
            print "urllib2.URLError"
            logging.info("---urllib2.URLError---")
            logging.info(url)
            logging.info(e)
            return None
        return json.loads(res, encoding='utf-8')

    def run(self):
        """ run
        """

        while (True):
            self.upload()
            print("Last check: " + str(time.asctime(time.localtime())))
            time.sleep(SLEEP_TIME)

    def createSetsRun(self,row):
        con = lite.connect(DB_PATH)
        con.text_factory = str
        with con:
            cur = con.cursor()
            if FULL_SET_NAME_NEW:
                if FULL_SET_NAME:
                    setName = str(datetime.datetime.now().strftime('%Y/%m/%d'))
                else:
                    setName = str(datetime.datetime.now().strftime('%Y%m%d'))
            else:
                if FULL_SET_NAME:
                    setName = os.path.relpath(os.path.dirname(row[1]), FILES_DIR)
                else:
                    head, setName = os.path.split(os.path.dirname(row[1]))
            flickrsetId = self.getFlickrSetsId(setName)
            print("adding file to set: " + row[1].decode('utf-8') +" to " + setName.decode('utf-8'))
            self.addFileToSet(flickrsetId, row, cur, True)
            con.commit()

#Verkar bli db lock, om man inte har con.commit()
            if ALBUM and not setName == ALBUM:
                setName = ALBUM
                flickrsetId = self.getFlickrSetsId(setName)
                print("adding file to Album: " + row[1].decode('utf-8') +" to " + setName.decode('utf-8'))
                self.addFileToSet(flickrsetId, row, cur, False)
                con.commit()

    def createSets(self):
        print('*****Creating Sets*****')
        if DRY_RUN :
            return True
        con = lite.connect(DB_PATH)
        con.text_factory = str
        with con:
            cur = con.cursor()
            cur.execute("SELECT files_id, path, set_id FROM files WHERE set_id IS NULL OR set_id = ''")

            files = cur.fetchall()
            files = self.photo_movie
            if PROCESSES:
                if len(files) > 0:
                    self.pool = ThreadPool(processes=int(PROCESSES))
                    resultat = self.pool.map(self.createSetsRun, files)
                    self.pool.close() #we are not adding any more processes
                    self.pool.join() #tell it to wait until all threads are done before going on
                    return
            else:
                for row in files:
                    resultat = self.createSetsRun(row)

        print('*****Completed creating sets*****')

    def createAlbumFlickr(self, row):
        con = lite.connect(DB_PATH)
        con.text_factory = str
        with con:
            cur = con.cursor()
            album = row[0]
            fileid = row[1]
            flickrsetId = self.getFlickrSetsId(album)
            if not flickrsetId:
                print "Created the set: " + album.decode('utf-8')
                setId = self.createSet(album, fileid, cur, con, True)
 #               print "setId", setId
            else:
                print "Already set exist: "+ album.decode('utf-8')

    def createSetsTypeRun(self,row):
        con = lite.connect(DB_PATH, timeout=1)
        con.text_factory = str
        with con:
            cur = con.cursor()
            #Get exif Create_date or FileModifyDate
            filetype = mimetypes.guess_type(row[1])
            if 'video' in filetype[0]:
                setName = "All_Video"
            else:
                setName = "All_Photo"
            flickrsetId = self.getFlickrSetsId(setName)
            print("Special, adding file to set: " + row[1].decode('utf-8') +" to "+ setName.decode('utf-8'))
            self.addFileToSet(flickrsetId, row, cur, False)

    def createFlickrAlbum(self):
        print('*****Creating Flickr Album*****')
        if DRY_RUN :
            return True
        con = lite.connect(DB_PATH)
        con.text_factory = str
        albumList = []
        albumDict = {}
        with con:
            cur = con.cursor()
            cur.execute("SELECT files_id, path, set_id FROM files WHERE set_id IS NULL OR set_id = ''")
            files = cur.fetchall()
            #Special make new list to use in CreatingSets/CreatingSetsType
            self.photo_movie = files
            #Fix All_Video and All_Photo
            for row in files:
                if SET_TYPE:
                    filetype = mimetypes.guess_type(row[1])
                    if 'video' in filetype[0]:
                        setName = "All_Video"
                        albumDict[setName] = row[0]
                    else:
                        setName = "All_Photo"
                        albumDict[setName] = row[0]
                albumDict[setName] = row[0]
                #Fix Full_set_name to set
                if FULL_SET_NAME_NEW:
                    if FULL_SET_NAME:
                        setName = str(datetime.datetime.now().strftime('%Y/%m/%d'))
                    else:
                        setName = str(datetime.datetime.now().strftime('%Y%m%d'))
                else:
                    if FULL_SET_NAME:
                        setName = os.path.relpath(os.path.dirname(row[1]), FILES_DIR)
                    else:
                        head, setName = os.path.split(os.path.dirname(row[1]))
                albumDict[setName] = row[0]
            if ALBUM and files:
#                albumDict[args.album] = row[0]
                albumDict[ALBUM] = row[0]
            albumList = [(k,v) for k,v in albumDict.items()]
#            print albumList
#            sys.exit()
            if PROCESSES:
                if len(albumList) > 0:
                    self.pool = ThreadPool(processes=int(PROCESSES))
                    resultat = self.pool.map(self.createAlbumFlickr, albumList)
                    self.pool.close() #we are not adding any more processes
                    self.pool.join() #tell it to wait until all threads are done before going on
            else:
                for row in albumList:
                    resultat = self.createAlbumFlickr(row)


    def createSetsType(self):
        print('*****Creating Sets Type*****')
        if DRY_RUN :
            return True
        con = lite.connect(DB_PATH)
        con.text_factory = str
        with con:
            cur = con.cursor()
            cur.execute("SELECT files_id, path, set_id FROM files WHERE set_id IS NULL OR set_id = ''")
            files = cur.fetchall()

            if PROCESSES:
                if len(files) > 0:
                    self.pool = ThreadPool(processes=int(PROCESSES))
                    resultat = self.pool.map(self.createSetsTypeRun, files)
                    self.pool.close() #we are not adding any more processes
                    self.pool.join() #tell it to wait until all threads are done before going on
                    return
            else:
                for row in files:
                    resultat = self.createSetsTypeRun(row)
        print('*****Completed creating sets to All_Photo/All_Video*****')

    def addFileToSet(self, setId, file, cur, CreateInDb):
        if DRY_RUN :
                return True
        try:
            d = {
                "auth_token": str(self.token),
                "perms": str(self.perms),
                "format": "json",
                "nojsoncallback": "1",
                "method": "flickr.photosets.addPhoto",
                "photoset_id": str(setId),
                "photo_id": str(file[0]),
            }
            sig = self.signCall(d)
            url = self.urlGen(api.rest, d, sig)
            res = self.getResponse(url)
            if (self.isGood(res)):
                if CreateInDb:
                    print("Successfully added file " + str(file[1]))
                    cur.execute("UPDATE files SET set_id = ? WHERE files_id = ?", (setId, file[0]))

            else:
                if (res['code'] == 1):
                    print("Photoset not found, creating new set...")
                    if FULL_SET_NAME_NEW:
                        if FULL_SET_NAME:
                            setName = str(datetime.datetime.now().strftime('%Y/%m/%d'))
                        else:
                            setName = str(datetime.datetime.now().strftime('%Y%m%d'))
                    else:
                        if FULL_SET_NAME:
                            setName = os.path.relpath(os.path.dirname(file[1]), FILES_DIR)
                        else:
                            head, setName = os.path.split(os.path.dirname(file[1]))
                    con = lite.connect(DB_PATH)
                    con.text_factory = str
                    self.createSet(setName, file[0], cur, con, True)
                elif (res['code'] == 3):
                    print(str(file[1]) +" "+ res['message'] + "... updating DB")
                    cur.execute("UPDATE files SET set_id = ? WHERE files_id = ?", (setId, file[0]))
                else:
                    self.reportError(res)
        except:
            print(str(sys.exc_info()))

    def createSet(self, setName, primaryPhotoId, cur, con, CreateInDb):
        print("Creating new set: " + setName.decode('utf-8'))

        if DRY_RUN :
                return True

        try:
            d = {
                "auth_token": str(self.token),
                "perms": str(self.perms),
                "format": "json",
                "nojsoncallback": "1",
                "method": "flickr.photosets.create",
                "primary_photo_id": str(primaryPhotoId),
                "title": setName

            }

            sig = self.signCall(d)

            url = self.urlGen(api.rest, d, sig)
            res = self.getResponse(url)
            if (self.isGood(res)):
                if CreateInDb:
                    self.logSetCreation(res["photoset"]["id"], setName, primaryPhotoId, cur, con)
                    print "adding file to set: "+ str(primaryPhotoId) +" to "+ setName + " as primary photo"
                    return res["photoset"]["id"]
            else:
                print("Error upload", d)
                self.reportError(res)
        except:
            print(str(sys.exc_info()))
        return False

    def setupDB(self):
        print("Setting up the database: " + DB_PATH)
        con = None
        try:
            con = lite.connect(DB_PATH)
            con.text_factory = str
            cur = con.cursor()
            cur.execute('CREATE TABLE IF NOT EXISTS files (files_id INT, path TEXT, set_id INT, md5 TEXT, tagged INT)')
            cur.execute('CREATE TABLE IF NOT EXISTS sets (set_id INT, name TEXT, primary_photo_id INTEGER)')
            cur.execute('CREATE UNIQUE INDEX IF NOT EXISTS fileindex ON files (path)')
            cur.execute('CREATE INDEX IF NOT EXISTS setsindex ON sets (name)')
            con.commit()
            cur = con.cursor()
            cur.execute('PRAGMA user_version')
            row = cur.fetchone()
            if (row[0] == 0):
                print('Adding last_modified column to database');
                cur = con.cursor()
                cur.execute('PRAGMA user_version="1"')
                cur.execute('ALTER TABLE files ADD COLUMN last_modified REAL');
                con.commit()
            con.close()
        except lite.Error, e:
            print("Error: %s" % e.args[0])
            if con != None:
                con.close()
            sys.exit(1)
        finally:
            print("Completed database setup")

    def md5Checksum(self, filePath):
        with open(filePath, 'rb') as fh:
            m = hashlib.md5()
            while True:
                data = fh.read(8192)
                if not data:
                    break
                m.update(data)
            return m.hexdigest()

    # Method to clean unused sets
    def removeUselessSetsTable(self):
        print('*****Removing empty Sets from DB*****')
        if DRY_RUN :
                return True


        con = lite.connect(DB_PATH)
        con.text_factory = str
        with con:
            cur = con.cursor()
            cur.execute("SELECT set_id, name FROM sets WHERE set_id NOT IN (SELECT set_id FROM files)")
            unusedsets = cur.fetchall()

            for row in unusedsets:
                print("Unused set spotted about to be deleted: " + str(row[0]) + " (" + row[1].decode('utf-8') + ")")
                cur.execute("DELETE FROM sets WHERE set_id = ?", (row[0],))
            con.commit()

        print('*****Completed removing empty Sets from DB*****')

    # Display Sets
    def displaySets(self):
        con = lite.connect(DB_PATH)
        con.text_factory = str
        with con:
            cur = con.cursor()
            cur.execute("SELECT set_id, name FROM sets")
            allsets = cur.fetchall()
            for row in allsets:
                print("Set: " + str(row[0]) + "(" + row[1] + ")")


    # Get sets from Flickr
    def getFlickrSets(self):
        print('*****Adding Flickr Sets to DB*****')
        if DRY_RUN :
                return True

        con = lite.connect(DB_PATH)
        con.text_factory = str
        try:
            d = {
                "auth_token": str(self.token),
                "perms": str(self.perms),
                "format": "json",
                "nojsoncallback": "1",
                "method": "flickr.photosets.getList"
            }
            url = self.urlGen(api.rest, d, self.signCall(d))
            res = self.getResponse(url)
            if (self.isGood(res)):
                cur = con.cursor()
                for row in res['photosets']['photoset']:
                    setId = row['id']
                    setName = row['title']['_content']
                    primaryPhotoId = row['primary']
                    cur.execute("SELECT set_id FROM sets WHERE set_id = '" + setId + "'")
                    foundSets = cur.fetchone()
                    if foundSets == None:
                        print(u"Adding set #{0} ({1}) with primary photo #{2}".format(setId, setName, primaryPhotoId))
                        cur.execute("INSERT INTO sets (set_id, name, primary_photo_id) VALUES (?,?,?)",
                                    (setId, setName, primaryPhotoId))
                con.commit()
                con.close()
            else:
                print(d)
                self.reportError(res)
        except:
            print(str(sys.exc_info()))
        print('*****Completed adding Flickr Sets to DB*****')

    # Get setId from name on Flickr
    def getFlickrSetsId(self, insetName):
        if DRY_RUN :
                return True

        try:
            d = {
                "auth_token": str(self.token),
                "perms": str(self.perms),
                "format": "json",
                "nojsoncallback": "1",
                "method": "flickr.photosets.getList"
            }
            url = self.urlGen(api.rest, d, self.signCall(d))
            res = self.getResponse(url)
            if (self.isGood(res)):
                for row in res['photosets']['photoset']:
                    setId = row['id']
                    setName = row['title']['_content']
                    if insetName == setName:
                        return setId
            else:
                print(d)
                self.reportError(res)
        except:
            print(str(sys.exc_info()))
        return None

    def getFlickrSetInfo(self,setId):
        if DRY_RUN :
                return True

        try:
            d = {
                "auth_token": str(self.token),
                "perms": str(self.perms),
                "format": "json",
                "nojsoncallback": "1",
                "method": "flickr.photosets.getInfo",
                "photoset_id": str(setId),
            }
            url = self.urlGen(api.rest, d, self.signCall(d))
            res = self.getResponse(url)
            if (self.isGood(res)):
                Find = True
                return Find, res
            else:
                Find = False
                return Find, res
        except:
            print(str(sys.exc_info()))

    def photos_search(self, checksum):
        data = {
            "auth_token": str(self.token),
            "perms": str(self.perms),
            "format": "json",
            "nojsoncallback": "1",
            "method": "flickr.photos.search",
            "user_id": "me",
            "tags": 'checksum:{}'.format(checksum),
        }

        url = self.urlGen(api.rest, data, self.signCall(data))
        resultat = self.getResponse(url)
#        return self.getResponse(url)
        if resultat:
            return resultat
        else:
            print "ERROR"
            return None

    def people_get_photos(self):
        data = {
            "auth_token": str(self.token),
            "perms": str(self.perms),
            "format": "json",
            "nojsoncallback": "1",
            "user_id": "me",
            "method": "flickr.people.getPhotos",
            "per_page": "1"
        }

        url = self.urlGen(api.rest, data, self.signCall(data))
        return self.getResponse(url)

    def photos_get_not_in_set(self):
        data = {
            "auth_token": str(self.token),
            "perms": str(self.perms),
            "format": "json",
            "nojsoncallback": "1",
            "method": "flickr.photos.getNotInSet",
            "per_page": "1"
        }

        url = self.urlGen(api.rest, data, self.signCall(data))
        return self.getResponse(url)

    def photos_add_tags(self, photo_id, tags, photo):
        tags = [tag.replace(',', '') for tag in tags]
        data = {
            "auth_token": str(self.token),
            "perms": str(self.perms),
            "format": "json",
            "nojsoncallback": "1",
            "method": "flickr.photos.addTags",
            "photo_id": str(photo_id),
            "tags": ','.join(tags)
        }
        print "*****Add tag "+ str(tags) +" to "+ str(photo) +"*****"
        url = self.urlGen(api.rest, data, self.signCall(data))
        return self.getResponse(url)

    def photos_add_tag(self, photo_id, tags, photo):
        if not FULL_SET_NAME_NEW:
            tags = [tag.replace(',', '') for tag in tags]
        tags =  ''.join(tags)
        data = {
            "auth_token": str(self.token),
            "perms": str(self.perms),
            "format": "json",
            "nojsoncallback": "1",
            "method": "flickr.photos.addTags",
            "photo_id": str(photo_id),
            "tags": tags
        }
        print "*****Add tag "+ tags +" to "+ str(photo) +"*****"
        url = self.urlGen(api.rest, data, self.signCall(data))
        return self.getResponse(url)

    def photos_get_info(self, photo_id):
        data = {
            "auth_token": str(self.token),
            "perms": str(self.perms),
            "format": "json",
            "nojsoncallback": "1",
            "method": "flickr.photos.getInfo",
            "photo_id": str(photo_id),
        }

        url = self.urlGen(api.rest, data, self.signCall(data))
        return self.getResponse(url)

    def photos_getallcontexts(self, photo_id):
        data = {
            "auth_token": str(self.token),
            "perms": str(self.perms),
            "format": "json",
            "nojsoncallback": "1",
            "method": "flickr.photos.getAllContexts",
            "photo_id": str(photo_id),
        }

        url = self.urlGen(api.rest, data, self.signCall(data))
        return self.getResponse(url)

    def photos_mod_date(self, photo_id, mod_date):
        data = {
            "auth_token": str(self.token),
            "perms": str(self.perms),
            "format": "json",
            "nojsoncallback": "1",
            "method": "flickr.photos.setDates",
            "date_taken": str( mod_date ),
            "photo_id": str(photo_id),
        }
        print("*****Update date_taken "+ str(mod_date) +"*****")
        url = self.urlGen(api.rest, data, self.signCall(data))
        return self.getResponse(url)

    def photos_remove_tag(self, tag_id):
        data = {
            "auth_token": str(self.token),
            "perms": str(self.perms),
            "format": "json",
            "nojsoncallback": "1",
            "method": "flickr.photos.removeTag",
            "tag_id": str(tag_id),
        }

        url = self.urlGen(api.rest, data, self.signCall(data))
        return self.getResponse(url)

    # Update Date/Time on Flickr for Video files
    def photos_set_dates(self, photo_id, datetxt):
        data = {
            "auth_token": str(self.token),
            "perms": str(self.perms),
            "format": "json",
            "nojsoncallback": "1",
            "method": "flickr.photos.setDates",
            "photo_id": str(photo_id),
            "date_taken": str(datetxt)
        }
        url = self.urlGen(api.rest, data, self.signCall(data))
        return self.getResponse(url)

    def print_stat(self):
        con = lite.connect(DB_PATH)
        con.text_factory = str
        with con:
            cur = con.cursor()
            cur.execute("SELECT Count(*) FROM files")

            print 'Total photos on local DB: {}'.format(cur.fetchone()[0])

        res = self.people_get_photos()
        if res["stat"] != "ok":
            raise IOError(res)
        print 'Total photos on flickr: {}'.format(res["photos"]["total"])

        res = self.photos_get_not_in_set()
        if res["stat"] != "ok":
            raise IOError(res)
        print 'Photos not in sets on flickr: {}'.format(res["photos"]["total"])
#        print "res", res
        

   


print("--------- Start time: " + time.strftime("%c") + " ---------")
if __name__ == "__main__":
    '''
    logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(levelname)s %(filename)s:%(lineno)s - %(funcName)20s() %(message)s',
                filename='debug.log',
                filemode='w')
    logging.debug('Started')
    errors = logging.FileHandler('error.log')
    errors.setLevel(logging.ERROR)
    logging.getLogger('').addHandler(errors)
    '''
    # Ensure that only once instance of this script is running




    global args
    args = config.build_options()
    upgrade_service = config.UpgradeService(args)
#    print "args", args.config
    if not os.path.exists(args.config):
        print "args", args.config
        sys.exit()
    logname = time.strftime("%Y%m%d_%H%M%S")
    logpathname = os.path.join(os.path.dirname(sys.argv[0]), logname + ".err")
    logging.basicConfig(filename=logpathname, level=logging.INFO)
    logging.getLogger("upload.py")

#    parser = argparse.ArgumentParser(description='Upload files to Flickr.')
#    parser.add_argument('-d', '--daemon', action='store_true',
#                        help='Run forever as a daemon')
#    parser.add_argument('-i', '--title', action='store',
#                        help='Title for uploaded files')
#    parser.add_argument('-e', '--description', action='store',
#                        help='Description for uploaded files')
#    parser.add_argument('-t', '--tags', action='store',
#                        help='Space-separated tags for uploaded files')
#    parser.add_argument('-r', '--drip-feed', action='store_true',
#                        help='Wait a bit between uploading individual files')
#    parser.add_argument('-p', '--processes',
#                        help='Number of photos to upload simultaneously')
#    parser.add_argument('-n', '--dry-run', action='store_true',
#                        help='Dry run')
#    parser.add_argument('-g', '--remove-ignored', action='store_true',
#                        help='Remove previously uploaded files, now ignored')
#    parser.add_argument('-m', '--max-uploadfiles',
#                        help='Max number of photos/movies to upload')
#    parser.add_argument('-a', '--album',
#                        help='Add to album')
#    parser.add_argument('-c', '--configfile',
#                        help='Read configfile, in same dir as program')
#    args = parser.parse_args()

    configfileread()

    '''
    if MAX_UPLOADFILES:
        print "T", MAX_UPLOADFILES
    else:
        print "N", MAX_UPLOADFILES
    sys.exit()
    '''

    f = open(LOCK_PATH, 'w')
    try:
        fcntl.lockf(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError, e:
        if e.errno == errno.EAGAIN:
            sys.stderr.write('[%s] Script already running.\n' % time.strftime('%c'))
            sys.exit(-1)
        raise



#    print DRY_RUN
#    print(args)
#    print type(args.salbum)
#    sys.exit()

    if MAX_UPLOADFILES:
        print "Max upload photo/movies = "+ MAX_UPLOADFILES
    flick = Uploadr()

    if FILES_DIR == "" or not (os.path.isdir(FILES_DIR)):
        print "FILES_DIR = ", FILES_DIR
        print("Please configure the name of the folder in the script with media available to sync with Flickr.")
        sys.exit()
#    print "TYPE", type(FLICKR), FLICKR
    if FLICKR["api_key"] == "" or FLICKR["secret"] == "":
        print("Please enter an API key and secret in the script file (see README).")
        sys.exit()

#Checka internet, annars
    internet = have_internet()
    if not internet:
        print "No internet :("
        sys.exit(1)



    flick.setupDB()
    flick.checkToken()
#    print "xxx", xx
    if DAEMON:
        flick.run()
    else:
        if not flick.checkToken():
            flick.authenticate()
        flick.displaySets()
        flick.removeUselessSetsTable()
        flick.getFlickrSets() #Add flickrsets to DB
        flick.convertRawFiles()
        flick.upload() #Upload Files
        if REMOVE_DELETE_FLICKR == True:
            flick.removeDeletedMedia()
            if REMOVE_IGNORED:
                flick.removeIgnoredMedia()
        else:
            print("*****Removing deleted files INACTIVE*****")
        flick.createFlickrAlbum()
        if SET_TYPE:
            flick.createSetsType()
        flick.createSets()
        flick.print_stat()

#remove logg file if empty
if os.path.getsize(logpathname) == 0:
        print "Remove " + logpathname + " is empty"
        os.remove(logpathname)

print("--------- End time: " + time.strftime("%c") + " ---------")
