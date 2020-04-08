#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging
import datetime
import time
import argparse
import os
import linecache
import signal

# help from Bryan Fernandez to get OS signals working correctly


# if sys.version_info[0] < 3:
#     raise Exception("This program requires python3 interpreter")

exit_flag = False

logger = logging.getLogger(__file__)


def signal_handler(sig_num, frame):
    """
    This is a handler for SIGTERM and SIGINT. Other signals can be mapped here as well (SIGHUP?)
    Basically it just sets a global flag, and main() will exit it's loop if the signal is trapped.
    :param sig_num: The integer signal number that was trapped from the OS.
    :param frame: Not used
    :return None
    """
    global exit_flag
    logger.warn('Received ' + signal.Signals(sig_num).name)
    exit_flag = True


def watch_directory(args):

    # Dictionary of tracked files and current line for each:
    watching_filepaths = {}

    # Current iteration of the main execution loop:
    loop_iter = 0

    while not exit_flag:
        try:
            loop_iter += 1

            # Create/reset variable for list of files matching requested extension:
            files_list = []

            # Implement polling interval:
            time.sleep(args.interval)

            # Ongoing visual indication of activity in terminal:
            print(
                f"Directory: {args.path}, "
                f"Extension: {args.ext}, "
                f"Magic Word: {args.magic}, "
                f"Iteration: {loop_iter}, "
                f"PID: {os.getpid()}")

            # Raise FileNotFound on every iteration if path does not exist:
            os.listdir(args.path)

            # Build files_list of files found with specified extension:
            for root, dirs, files in os.walk(args.path):
                for filename in files:
                    if filename.endswith(args.ext):
                        files_list.append(os.path.join(root, filename))

            # Add new items to watching_filepaths based on files_list:
            for filepath in files_list:
                if filepath not in watching_filepaths:
                    logger.info(f"{filepath} found")
                    watching_filepaths[filepath] = 1

            # Remove item from watching_filepaths if not in current files_list
            # else scan item for magic text and update current_line:
            for filepath in list(watching_filepaths.keys()):
                if filepath not in files_list:
                    logger.info(f"{filepath} removed")
                    del(watching_filepaths[filepath])
                else:
                    current_line = watching_filepaths[filepath]
                    while True:
                        linecache.checkcache(filepath)
                        line = linecache.getline(filepath, current_line)
                        if (line == ""):
                            break
                        elif args.magic in line:
                            logger.info(
                                f"Magic found in {filepath} "
                                f"on line {current_line}"
                            )
                            current_line += 1
                        else:
                            current_line += 1
                        watching_filepaths[filepath] = current_line
        except FileNotFoundError as e:
            logger.info(e)


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

    app_start_time = datetime.datetime.now()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    parser = create_parser()
    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)s.%(msecs)03d %(name)-12s '
                        '%(levelname)-8s [%(threadName)-12s] %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        handlers=[
                            logging.FileHandler("dirwatcher.log", mode='a'),
                            logging.StreamHandler()
                        ]
                        )

    logger.setLevel(logging.DEBUG)

    logger.info(
        '\n'
        '-------------------------------------------------------------------\n'
        '    Running {0}\n'
        '    PID: {1}\n'
        '    Started on: {2}\n'
        '    Watching Directory: {3}\n'
        '    File Ext: {4}\n'
        '    Polling Interval: {5}\n'
        '    Magic Text: {6}\n'
        '-------------------------------------------------------------------\n'
        .format(__file__, os.getpid(), app_start_time.isoformat(),
                args.path, args.ext, args.interval, args.magic)
    )

    while not exit_flag:
        try:
            watch_directory(args)
            # while not exit_flag:
            #     print("Tick...")
            #     time.sleep(1)
            #     print("Tock...")

        except Exception as e:
            logger.info(e)
        finally:
            uptime = datetime.datetime.now()-app_start_time
            logger.info(
                '\n'
                '-------------------------------------------------------------------\n'
                '    Stopped {0}\n'
                '    Uptime: {1}\n'
                '-------------------------------------------------------------------\n'
                .format(__file__, str(uptime))
            )

    # print("I have shut down gracefully.")


if __name__ == '__main__':
    main()
