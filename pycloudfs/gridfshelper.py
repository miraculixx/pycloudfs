#!/usr/bin/env python

import mongoengine
from datetime import datetime
import gridfs
import urlparse
import argparse
import os
import sys

"""
A simple gridfs helper

This is a simple implementation to updload and download files from a
mongo gridfs collection.

usage: gridfshelper.py [-h] [--url URL] [--collection COLLECTION]
                       [--cmd COMMAND] [--file FILE]

GridFSHelper Usage

optional arguments:
  -h, --help            show this help message and exit
  --url URL             url of mongo instance to be used
  --collection COLLECTION
                        name of the collection in mongo instance
  --cmd COMMAND         transaction type [list, upload, download]
  --file FILE           name of the file to be uploaded or downloaded
@Author : Gaurav Ghimire
"""


class GridFSHelper(object):
    """docstring for GridFSHelper"""
    def __init__(self, mongo_url='', collection=''):
        self.mongo_url = mongo_url
        self.collection = collection

    def __get_fs_instance(self):
        """
        Get List of files
        """
        self.parsed_url = urlparse.urlparse(self.mongo_url)
        self.database_name = self.parsed_url.path[1:]
        try:
            db = getattr(mongoengine.connect(
                self.database_name,
                host=self.mongo_url,
                connect=False,
                serverSelectionTimeoutMS=2500), self.database_name)
            fs = gridfs.GridFS(db, collection=self.collection)
        except Exception, e:
            raise e
            sys.exit(1)
        return fs

    def get_list(self):
        """
        Retrieve list of files in gridfs collection
        """
        fs = self.__get_fs_instance()
        return fs.list()

    def get_fileid(self, filename):
        """
        Returns the gridfs object id
        """
        fs = self.__get_fs_instance()
        return fs.get_last_version(filename)._id

    def gridfs_cleanup(self):
        """
        Cleans up the gridfs removing file that are a week old
        """
        fs = self.__get_fs_instance()
        source_list = self.get_list()
        for grid_file in source_list:
            file_id = self.get_fileid(grid_file)
            creation_date = file_id.generation_time
            now = datetime.now()
            tdelta = now - creation_date
            if tdelta.days > 7:
                fs.delete(file_id)
                print "Deleted file %s" % grid_file

    def get_file(self, filename, asfile=False):
        """
        Download file from gridfs
        """
        fs = self.__get_fs_instance()
        file_id = fs.get_last_version(filename)._id
        try:
            file = fs.get(file_id)
        except Exception, e:
            print "An error occured while downloading file %s" % filename
            raise e
            sys.exit(1)
        if asfile:
            return file
        f = open(filename, 'w')
        f.write(file.read())
        f.close()

    def put_file(self, filename):
        """
        Upload a file from local to gridfs
        """
        fs = self.__get_fs_instance()
        try:
            fs.put(open(filename, 'r'), filename=os.path.basename(filename))
        except Exception, e:
            print "An error occured while uploading file %s" % filename
            raise e
            sys.exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="GridFSHelper Usage")
    parser.add_argument(
        '--url',
        action='store',
        help="url of mongo instance to be used")
    parser.add_argument(
        '--collection',
        action='store',
        help="name of the collection in mongo instance")
    parser.add_argument(
        '--cmd',
        action='store',
        help="transaction type [upload, download]",
        dest="command")
    parser.add_argument(
        '--file',
        action='store',
        help="name of the file to be uploaded or downloaded",
        dest="file")

    # print help if no argument is given
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    if not args.url:
        print "FATAL!! URL of mongodb instance is required!"
        parser.print_help()
        sys.exit(1)

    if not args.collection:
        print "FATAL!! Name of collection is required!"
        parser.print_help()
        sys.exit(1)

    if args.command != 'list' and not args.file:
        print "FATAL!! Please specify the filename!"
        parser.print_help()
        sys.exit(1)

    if args.command == 'list':
        gf = GridFSHelper()
        gf.mongo_url = args.url
        gf.collection = args.collection
        file_list = gf.get_list()
        if len(file_list) > 0:
            print "List of files in collection %s :" % gf.collection
            print "====================================================="
            print '\n'.join(file_list)
            print "====================================================="
            print "Total of %s files in collection" % len(file_list)
            print ".....End of list....."
        else:
            print "File list is empty..."
    elif args.command == "download":
        gf = GridFSHelper()
        gf.mongo_url = args.url
        gf.collection = args.collection
        downloadfile = args.file
        gf.get_file(downloadfile)
        print "File: %s has been downloaded!" % downloadfile
    elif args.command == "upload":
        # TBD :
        # checks for duplicates
        # prompts for replacing, overwrite, abort
        gf = GridFSHelper()
        gf.mongo_url = args.url
        gf.collection = args.collection
        uploadfile = args.file
        gf.put_file(uploadfile)
        print "File: %s has been uploaded!" % uploadfile
