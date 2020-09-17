#!/usr/bin/env python3

import json
import subprocess
import argparse


def getArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', help='interface from which to send wake on lan packets', type=str)
    parser.add_argument('-file', help='json file that contains target mac addresses', type=str)

    args = parser.parse_args()
    return args


def wakeMac(mac, interface):
    #subprocess.Popen(['etherwake', '-i', '%s' % interface, '%s' % mac]):
    print('Would run etherwake -i %s %s' % (interface, mac))
    return


def pingTarget(mac, ip, interface):
    print('\nPinging %s...' % (ip))
    child = subprocess.Popen(['ping', '-c', '1', '%s' % (ip)], stdout=subprocess.PIPE)
    streamdata = child.communicate()[0]
    # check exit code
    if child.returncode != 0:
        wakeMac(mac, interface)
    else:
        print('%s is up!' % (ip))



def wakeGroup(group, interface):
    for target in group:
        # this part will be multi threaded
        mac = target['mac']
        ip = target['ip']
        pingTarget(mac, ip, interface)
        return



def main():
    args = getArguments()
    file = args.file
    interface = args.i

    # load json
    # will need validate that the json is structured properly before progressing
    with open(file) as f:
        data = json.load(f)
    
    # cycle through the groups and send wake command to macs in that group
    for group in data['groups']:
        wakeGroup(group, interface)
            


if __name__ == '__main__':
    main()
