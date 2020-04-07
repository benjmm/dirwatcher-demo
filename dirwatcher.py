#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import datetime
import time
import argparse
import os
import linecache
import signal

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
    # log the associated signal name (the python3 way)
    logger.warn('Received ' + signal.Signals(sig_num).name)
    # log the signal name (the python2 way)
    signames = dict((k, v) for v, k in reversed(sorted(signal.__dict__.items()))
                    if v.startswith('SIG') and not v.startswith('SIG_'))
    logger.warn('Received ' + signames[sig_num])
    exit_flag = True


def watch_directory(args):

    watching_filepaths = {}
    loop_iter = 0

    logger.info(
        f"Watching Directory: {args.path}, "
        f"File Ext: {args.ext}, "
        f"Polling Interval: {args.interval}, "
        f"Magic Text: {args.magic}"
    )

    while True:
        try:
            loop_iter += 1
            print(
                f"Scanning directory {args.path}, "
                f"iteration number {loop_iter}")
            time.sleep(args.interval)

            files_list = []

            os.listdir(args.path)

            for root, dirs, files in os.walk(args.path):
                for filename in files:
                    if filename.endswith(args.ext):
                        files_list.append(os.path.join(root, filename))

            for filepath in files_list:
                if filepath not in watching_filepaths:
                    logger.info(f"{filepath} found")
                    watching_filepaths[filepath] = 1

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

        except KeyboardInterrupt:
            logger.info("KeyboardInterrupt detected")
            break
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
    logging.basicConfig(format='%(asctime)s.%(msecs)03d %(name)-12s '
                        '%(levelname)-8s [%(threadName)-12s] %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        handlers=[
                            logging.FileHandler("dirwatcher.log", mode='a'),
                            logging.StreamHandler()
                        ]
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

    # Hook these two signals from the OS ..
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    # Now my signal_handler will get called if OS sends either of these to my process.

    parser = create_parser()
    args = parser.parse_args()

    while not exit_flag:
        try:
            watch_directory(args)
        except Exception as e:
            logger.info(e)

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
