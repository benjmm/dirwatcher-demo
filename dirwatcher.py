#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import datetime
import time
import argparse
import os

logger = logging.getLogger(__file__)


def watch_directory(args):
    # keys are filenames and values are last line read

    # Look at directory and get a list of files from it
    # Add those to dictionary if not already present
    # Log file as new

    # Look at file dictionary and compare that to what is in the directory
    # Remove files from dictionary if no longer present
    # Log file as removed

    # Open each file in the dictionary starting at the last line read
    # Search for & update log if magic text found
    # Keep track of last line read for each file

    watching_files = {}
    logger.info(
        'Watching Directory: {}, File Ext: {}, '
        'Polling Interval: {}, Magic Text: {}'.format(
            args.path, args.ext, args.interval, args.magic
        ))

    while True:
        try:
            logger.info("Inside Watch Loop")
            time.sleep(args.interval)

            dentries = [dentry.name for dentry in os.scandir(args.path)]

            for dentry in dentries:
                if dentry.endswith(args.ext):
                    if dentry not in watching_files:
                        watching_files[dentry] = 0
                        print(f"{dentry} found")
                        print(watching_files)
            for filename in list(watching_files.keys()):
                if filename not in dentries:
                    print(f"{filename} removed")
                    del(watching_files[filename])
                    print(watching_files)
        # except KeyboardInterrupt:
        #     print("KeyboardInterrupt detected")
            # break
        except FileNotFoundError as e:
            print(e)


def find_magic(filename, starting_line, magic_word):
    pass


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--ext', type=str, default='.txt',
                        help='Text file extension to watch')
    parser.add_argument('-i', '--interval', type=float,
                        default=1.0, help='Number of seconds between polling')
    parser.add_argument('path', help='Directory path to watch')
    parser.add_argument('magic', help='String to watch for')
    return parser


def main():
    logging.basicConfig(
        format='%(asctime)s.%(msecs)03d %(name)-12s %(levelname)-8s'
        '[%(threadName)-12s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logger.setLevel(logging.DEBUG)
    app_start_time = datetime.datetime.now()
    logger.info(
        '\n'
        '-------------------------------------------------------------------\n'
        '    Running {0}\n'
        '    Started on {1}\n'
        '-------------------------------------------------------------------\n'
        .format(__file__, app_start_time.isoformat())
    )
    parser = create_parser()
    args = parser.parse_args()
    watch_directory(args)
    uptime = datetime.datetime.now()-app_start_time
    logger.info(
        '\n'
        '-------------------------------------------------------------------\n'
        '    Stopped {0}\n'
        '    Uptime was {1}\n'
        '-------------------------------------------------------------------\n'
        .format(__file__, str(uptime))
    )


if __name__ == '__main__':
    main()
