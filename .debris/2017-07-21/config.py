#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
import ConfigParser
import os
import logging
logger = logging.getLogger("config file")
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s : %(lineno)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

DEFAULT_VALUES = dict(
    config=os.path.join(os.path.dirname(sys.argv[0]), ".uploadr.ini"),
    FILES_DIR = "/tmp/flickr",
    FLICKR = {
            "title"                 : "",
            "description"           : "",
            "tags"                  : "flickr-uploader",
            "is_public"             : "0",
            "is_friend"             : "0",
            "is_family"             : "0",
            "api_key"               : "f1e51d46d02c774ecdf528593144fe38",
            "secret"                : "4d6eca5570e9673e"
            },
    TOKEN_PATH = os.path.join(os.path.dirname(sys.argv[0]), ".flickrToken"),
    DB_PATH = os.path.join(os.path.dirname(sys.argv[0]), ".flickrdb"),
    SLEEP_TIME = 1*60,
    DRIP_TIME = 1*9,
    LOCK_PATH = os.path.join(os.path.dirname(sys.argv[0]), ".flickrlock"),
    EXCLUDED_FOLDERS = ["@eaDir","#recycle",".picasaoriginals","_ExcludeSync","Corel Auto-Preserve","Originals","Automatisch beibehalten von Corel"],
    IGNORED_REGEX = ["^\._","^\." ],
    ALLOWED_EXT = ["jpg","png","avi","mov","mpg","mp4","3gp","mkv", "ts"],
    CONVERT_RAW_FILES = True,
    RAW_EXT = ["3fr", "ari", "arw", "bay", "crw", "cr2", "cap", "dcs", "dcr", "dng", "drf", "eip", "erf", "fff", "iiq", "k25", "kdc", "mdc", "mef", "mos", "mrw", "nef", "nrw", "obm", "orf", "pef", "ptx", "pxn", "r3d", "raf", "raw", "rwl", "rw2", "rwz", "sr2", "srf", "srw", "x3f"],
    RAW_TOOL_PATH = "/usr/local/bin/",
    RAW_SKIP_CREATE_ORIGINAL = True,
    FILE_MAX_SIZE = 1*1024*1024*1024,
    MANAGE_CHANGES = True,
    FULL_SET_NAME_NEW = True,
    FULL_SET_NAME = True,
    SOCKET_TIMEOUT = 60,
    MAX_UPLOAD_ATTEMPTS = 10,
    REMOVE_DELETE_FLICKR = False,
    TITLE_FILENAME = True,
    TAG_FILENAME = True, 
    TAG_SETNAME = True,
    WAIT_NEXT_UPLOAD = False,
    SET_TYPE = True,
    CHECK_LOCAL_MD5CHECKSUM = False,

)

COMMAND_LINE_ONLY_ARGS = ["create_config"]

class Options:

    def __init__(self, args):
#        self.parser = argparse.ArgumentParser(description="Example script.")
        self.parser = argparse.ArgumentParser(description='Upload files to Flickr.')
        self.args = args

        self.parser.add_argument("-cc", "--create-config",
                            dest="create_config",
                            help="Create configuration file with default values")

        self.parser.add_argument("-c", "--config",
                            dest="config",
                            help="Path to uploadr.ini")

        self.parser.add_argument('-d', '--daemon', action='store_true',
                            dest="DAEMON",
                            help='Run forever as a daemon')

        self.parser.add_argument('-i', '--title', default=False,
                            dest="TITLE",
                            help='Title for uploaded files')

        self.parser.add_argument('-e', '--description', default=False,
                            dest="DESCRIPTION",
                            help='Description for uploaded files')

        self.parser.add_argument('-t', '--tags', default=False,
                            dest="TAGS",
                            help='Space-separated tags for uploaded files')

        self.parser.add_argument('-r', '--drip-feed', action='store_true',
                            dest="DRIP_FEED",
                            help='Wait a bit between uploading individual files')

        self.parser.add_argument('-p', '--processes', default=False,
                            dest="PROCESSES",
                            help='Number of photos to upload simultaneously')

        self.parser.add_argument('-n', '--dry-run', default=False,
                            dest="DRY_RUN",
                            help='Dry run')

        self.parser.add_argument('-g', '--remove-ignored', default=False,
                            dest="REMOVE_IGNORED",
                            help='Remove previously uploaded files, now ignored')

        self.parser.add_argument('-m', '--max-uploadfiles', default=False,
                            dest="MAX_UPLOADFILES",
                            help='Max number of photos/movies to upload')

        self.parser.add_argument('-a', '--album', default=False,
                            dest="ALBUM",
                            help='Add to album')

        self.parser.add_argument('-fd', '--files_dir', default=False,
                            dest="FILES_DIR",
                            help='Dir where images are')

        self.options = self.parser.parse_args()
#        print "repo-branch from command line is: {}".format(self.options.repo_branch)


    def get_options(self):
        return self.options

    def get_parser(self):
        return self.parser

def parse_args():
    """ Parses the command line arguments, and returns dictionary with all of them.

    The arguments have dashes in the names, but they are stored in fields with underscores.

    :return: arguments
    :rtype: dictionary
    """
    options = Options(sys.argv).get_options()
    result = options.__dict__
    logger.debug("COMMAND LINE OPTIONS: {}".format(result))

    if options.create_config:
        logger.debug("Creating configuration file at: {}".format(options.create_config))
        with open(options.create_config, "w") as c:
            c.write("[{}]\n".format(CONFIG_SECTION_NAME))
            for key in sorted(DEFAULT_VALUES.keys()):
                value = DEFAULT_VALUES[key]
                c.write("{}={}\n".format(key, value or ""))
        exit(0)
    return result

CONFIG_SECTION_NAME = "Config"
def read_config(fname, section_name=CONFIG_SECTION_NAME):
    """ Reads a configuration file.

    Here the field names contain the dashes, in args parser we have underscores.
    So additionally I will convert the dashes to underscores here.

    :param fname: name of the config file
    :return: dictionary with the config file content
    :rtype: dictionary
    """
    config = ConfigParser.RawConfigParser()
    #fix uppercase
    config.optionxform = str
    logger.debug("Config file: {}" .format(fname))
    try:
        with open(os.path.join(os.path.dirname(sys.argv[0]), fname)) as f:
            config.readfp(f)
#        with open(fname) as f:
#            config.readfp(f)
    except IOError:
        print "Config filen finns inte", os.path.join(os.path.dirname(sys.argv[0]), fname)
        logger.debug("Config filen finns inte", os.path.join(os.path.dirname(sys.argv[0]), fname))
        sys.exit(0)
#        return None
    try:
        config.read(fname)
        result = {key.replace(
        '-','_'):val for key, val in config.items(section_name)}
#        print "RESULT", result
        logger.debug("Read config file {}".format(fname))
#        logger.debug("CONFIG FILE OPTIONS: {}".format(result))
    except Exception as e :
        print str(e)
        return None

    return result

def merge_options(first, second, default={}):
    """
    This
     function merges the first argument dictionary with the second.
    The second overrides the first.
    Then it merges the default with the already merged dictionary.

    This is needed, because if the user will set an option `a` in the config file,
    and will not provide the value in the command line options configuration,
    then the command line default value will override the config one.

    With the three-dictionary solution, the algorithm is:
    * get the default values
    * update with the values from the config file
    * update with the command line options, but only for the values
      which are not None (all not set command line options will have None)

    As it is easier and nicer to use the code like:
        options.path
    then:
        options['path']
    the merged dictionary is then converted into a namedtuple.

    :param first: first dictionary with options
    :param second: second dictionary with options
    :return: object with both dictionaries merged
    :rtype: namedtuple
    """
    from collections import namedtuple
    options = default
    options.update(first)
    options.update({key:val for key,val in second.items() if val is not None})
#    logger.debug("MERGED OPTIONS: {}".format(options))
    return namedtuple('OptionsDict', options.keys())(**options)


def dict_difference(first, second, omit_keys=[]):
    """
    Calculates the difference between the keys of the two dictionaries,
    and returns a tuple with the differences.

    :param first:     the first dictionary to compare
    :param second:    the second dictionary to compare
    :param omit_keys: the keys which should be omitted,
                      as for example we know that it's fine that one dictionary
                      will have this key, and the other won't

    :return: The keys which are different between the two dictionaries.
    :rtype: tuple (first-second, second-first)
    """
    keys_first = set(first.keys())
    keys_second = set(second.keys())
    keys_f_s = keys_first - keys_second - set(omit_keys)
    keys_s_f = keys_second - keys_first - set(omit_keys)

    return (keys_f_s, keys_s_f)


def build_options():
    """
    Builds an object with the merged opions from the command line arguments,
    and the config file.

    If there is an option in command line which doesn't exist in the config file,
    then the command line default value will be used. That's fine, the script
    will just print an info about that.

    If there is an option in the config file, which doesn't exist in the command line,
    then it looks like an error. This time the script will show this as error information,
    and will exit.

    If there is the same option in the command line, and the config file,
    then the command line one overrides the config one.
    """
    options = parse_args()
    config = read_config(options['config'] or DEFAULT_VALUES['config'])
    if config == None:
        merged_options = merge_options(DEFAULT_VALUES, {}, DEFAULT_VALUES)

    else:
        (f, s) = dict_difference(DEFAULT_VALUES, config, COMMAND_LINE_ONLY_ARGS)
        if f:
            for o in f:
                logger.debug("There is an option, which is missing in the config file,"
                            "that's fine, I will use the \n<{}> value: <{}>".format(o, DEFAULT_VALUES[o]))
        if s:
            logger.error("There are options, which are in the config file, but are not supported:")
            for o in s:
                logger.error(o)
#            exit(2)
        merged_options = merge_options(config, options, DEFAULT_VALUES)
#        print "merged", merged_options
    return merged_options


class UpgradeService():

    def __init__(self, options):
        if not options:
            exit(1)
        self.options = options

    def run(self):
        pass

if __name__ == "__main__":
    options = build_options()
    upgrade_service = UpgradeService(options)
#    print "repo-branch value to be used is: {}".format(upgrade_service.options.repo_branch)
#    upgrade_service.run()
    print "RES", options
