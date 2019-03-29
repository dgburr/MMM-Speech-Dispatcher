#!/usr/bin/env python
# File:        avs_client.py
# Created:     29/03/2019 by Daniel Burr <dburr@dburr.net>
# Description: Python client for communicating with AVS (Alexa Voice Service)
# License:     GNU Public License, version 3
#
# Uses the simple-tts module (which internally uses festival) to convert
# the request to speech.  This speech is then sent to AVS using the
# alexa-client module.
#
# Based on alexa-client (https://github.com/ewenchou/alexa-client.git)
#
# FIXME:
# 1. Optimise by doing parallel encoding/playback
# 2. Improve accuracy by improving festival/pico2wave quality

import getopt, sys, signal
from alexa_client import AlexaClient
from simple_tts import tts
import subprocess
import shlex


running = True

def signal_handler(signal, frame):
    global running
    running = False
    sys.exit(1)


class Client:
    def __init__(self, verbose):
        self.verbose = verbose

    def play_mp3(self, filename):
        """Plays MP3 file
        @param: filename: The file path of the MP3 file to play.
        @type: filename: str
        """
        cmd_str = "mpg123 -q " + filename
        cmd = shlex.split(cmd_str)

        # Popen and communicate() to make sure all the audio finishes playing
        p = subprocess.Popen(cmd)
        p.communicate()

    def speak(self, text):
        alexa = AlexaClient()
        request = tts("Simon says, " + text)
        response = alexa.ask(request)
        if response:
            self.play_mp3(response)
        alexa.clean()

        print("FINISHED_UTTERANCE")
        sys.stdout.flush()


def help(name):
    print("%s: python wrapper for communicating with the Alexa Voice Service\n" % name)
    print("Usage:")
    print("\t--debug: Increase verbosity")
    print("\t--help:  This message\n")
    sys.exit(2)


def main():
    # capture SIGINT signal, e.g., Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    try:
        opts, args = getopt.getopt(sys.argv[1:], "dh", ["debug", "help"])
    except getopt.GetoptError as err:
        print(str(err))
        help(sys.argv[0])
    debug = False
    for opt, arg in opts:
        if opt in ("-d", "--debug"):
            debug = True
        else:
            help(sys.argv[0])
            sys.exit()

    client = Client(debug)

    while running == True:
        client.speak(raw_input())

if __name__ == "__main__":
    main()
