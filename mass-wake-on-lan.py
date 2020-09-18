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


def wakeMac(mac, ip, interface):
    if pingTarget(ip, interface) == 0:
        print('%s is up!' % ip)
    else:
        #subprocess.Popen(['etherwake', '-i', '%s' % interface, '%s' % mac]):
        print('Would run etherwake -i %s %s' % (interface, mac))
    return


def pingTarget(ip, interface):
    print('\nPinging %s...' % (ip))
    child = subprocess.Popen(['ping', '-c', '1', '%s' % (ip)], stdout=subprocess.PIPE)
    streamdata = child.communicate()[0]
    return child.returncode


def wakeGroup(group, interface):
    for target in group:
        # this part will be multi threaded
        mac = target['mac']
        ip = target['ip']
        wakeMac(mac, ip, interface)
    return



def main():
    # will need to fail gracefully if not given arguments
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

    print('\n\nDone :)\n')


def test():
    args = getArguments()
    file = args.file
    interface = args.i

    with open(file) as f:
        data = json.load(f)

    for group in data['groups']:
        print(group)
        for target in group:
            print('\t' + target['ip'])
            print('\t' + target['mac'] + '\n')


if __name__ == '__main__':
    main()
    #test()
