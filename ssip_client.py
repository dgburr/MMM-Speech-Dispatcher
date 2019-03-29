#!/usr/bin/env python3
# File:        ssip_client.py
# Created:     27/03/2019 by Daniel Burr <dburr@dburr.net>
# Description: Python client for communicating with speech-dispatcher
# License:     GNU Public License, version 3
#
# Uses the speechd python module to communicate with speech-dispatcher
# via SSIP (Speech Synthesis Interface Protocol), see
# https://freebsoft.org/doc/speechd/ssip.html

import getopt, sys, signal
from speechd import SSIPClient, CallbackType
from threading import Semaphore


running = True

def signal_handler(signal, frame):
    global running
    running = False
    sys.exit(1)


class Client:
    def __init__(self, verbose):
        self.client = SSIPClient('ssip_client')
        self.notifier = Semaphore(0)
        self.verbose = verbose

    def __del__(self):
        self.client.close()

    def set_output_module(self, name):
        supported = self.client.list_output_modules()
        if(name not in supported):
            print("%s is not a supported output module, keeping current setting (%s)" % (name, self.client.get_output_module()), file=sys.stderr)
        else:
            self.client.set_output_module(name)

    def set_voice(self, name):
        supported = map(lambda x: ' '.join(x), self.client.list_synthesis_voices())
        if(name not in supported):
            print("%s is not a supported synthesis voice, trying to set as normal voice" % name, file=sys.stderr)
            self.client.set_voice(name)
        else:
            self.client.set_synthesis_voice(name)

    def set_rate(self, rate):
            self.client.set_rate(rate)

    def set_language(self, lang):
            self.client.set_language(lang)

    def dump_config(self):
        print("\tCurrent output module:", end=' ')
        print(self.client.get_output_module())
        print("\tSupported output modules:", end=' ')
        print(self.client.list_output_modules())
        print("\tSupported synthesis voices: ", end=' ')
        print(self.client.list_synthesis_voices())

    def notify(self, arg):
        if(arg == CallbackType.END):
            self.notifier.release()

    def speak(self, text):
        self.client.speak(text, self.notify, CallbackType.END)
        self.notifier.acquire()
        print("FINISHED_UTTERANCE")


def help(name):
    print("%s: python wrapper for communicating with speech-dispatcher\n" % name)
    print("Usage:")
    print("\t--module=<module>: Use the specified output module (e.g. \"espeak-ng\", \"festival\", \"pico-generic\")")
    print("\t--voice=<voice>:   Use the specified voice (e.g. \"english_rp en gb-x-r\" or \"female2\")")
    print("\t--language=<lang>: Speaking language (e.g. \"en\")")
    print("\t--rate=<rate>:     Speaking rate (integer between -100 and 100)")
    print("\t--debug:           Increase verbosity")
    print("\t--help:            This message\n")
    print("All arguments are optional.  If they are not specified, then speech-dispatcher will")
    print("use the default configuration specified in it's configuration file.")
    sys.exit(2)


def main():
    # capture SIGINT signal, e.g., Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    try:
        opts, args = getopt.getopt(sys.argv[1:], "m:v:l:r:dh", ["module=", "voice=", "language=", "rate=", "debug", "help"])
    except getopt.GetoptError as err:
        print(str(err))
        help(sys.argv[0])
    module = None
    voice = None
    language = None
    rate = None
    debug = False
    for opt, arg in opts:
        if opt in ("-m", "--module"):
            module = arg
        elif opt in ("-v", "--voice"):
            voice = arg
        elif opt in ("-l", "--language"):
            language = arg
        elif opt in ("-r", "--rate"):
            rate = int(arg)
        elif opt in ("-d", "--debug"):
            debug = True
        else:
            help(sys.argv[0])
            sys.exit()

    client = Client(debug)

    if debug:
        print("Before configuration:")
        client.dump_config()

    # order is important for setting module and voice
    if(module != None):
        client.set_output_module(module)
    if(voice != None):
        client.set_voice(voice)
    if(language != None):
        client.set_language(language)
    if(rate != None):
        client.set_rate(rate)

    if debug:
        print("After configuration:")
        client.dump_config()

    while running == True:
        client.speak(input())


if __name__ == "__main__":
    main()
