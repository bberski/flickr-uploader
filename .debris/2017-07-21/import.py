#!/usr/bin/env python
# -*- coding: utf-8 -*-

import config
import sys





def ppprint (invar):
    print invar.split(".")[1],"=", eval(invar)
#    invar = eval(invar)
#    nyvar = invar.split(".")[1]
#    invar.split(".")[1] = "SSS"
#    print "XDDD", invar



args = config.build_options()
upgrade_service = config.UpgradeService(args)

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


