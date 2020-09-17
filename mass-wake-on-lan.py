#!/usr/bin/env python3

import json
import subprocess
import argparse


def getArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='json file that contains target mac addresses', type=str)

    args = parser.parse_args()
    return args


def wakeMac(mac):
    #subprocess.call(["etherwake", "-i eth0 %s" % mac]):
    print('Would run etherwake -i eth0 %s' % mac)
    return


def wakeGroup(group):
    for mac in group:
        # this part will be multi threaded
        # also need to ping the target before sending wake packet
        wakeMac(mac)
    return



def main():
    args = getArguments()
    file = args.file

    # load json
    with open(file) as f:
        data = json.load(f)
    
    # cycle through the groups and send wake command to macs in that group
    for group in data['groups']:
        wakeGroup(group)
            


if __name__ == '__main__':
    main()
