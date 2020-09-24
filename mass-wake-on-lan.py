#!/usr/bin/env python3

import argparse
import json
import os
import subprocess
import time
from threading import Thread



def getArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', help='interface from which to send wake on lan packets', type=str)
    parser.add_argument('-file', help='json file that contains target mac addresses', type=str)
    parser.add_argument('-delay', help='delay (in seconds) before checking if a target is up before sending another wake packet', type=int)
    parser.add_argument('-limit', help='number of attempts to wake a target before giving up', type=int)

    args = parser.parse_args()
    return args


def wakeMac(mac, ip, interface, delay, limit):
    attempts = 0
    while attempts <= limit:
        if attempts == limit:
            print('Could not wake %s :(' % ip)
            os._exit(1)
        if pingTarget(ip, interface) != 0:
            #subprocess.Popen(['etherwake', '-i', '%s' % interface, '%s' % mac]):
            print('Would run etherwake -i %s %s' % (interface, mac))
            time.sleep(delay)
            attempts = attempts + 1
        else:
            print('%s is up!' % ip)
            break
    return


def pingTarget(ip, interface):
    print('\nPinging %s...' % (ip))
    child = subprocess.Popen(['ping', '-c', '1', '%s' % ip], stdout=subprocess.PIPE)
    streamdata = child.communicate()[0]
    return child.returncode


def wakeGroup(group, interface, delay, limit):
    # create threads for multithreading 
    threads = []
    for target in group:
        mac = target['mac']
        ip = target['ip']
        thread = Thread(target=wakeMac, args=(mac, ip, interface, delay, limit))
        thread.start()
        threads.append(thread)
    for thread in threads:
        # wait for all threads to complete before continuing
        thread.join()
    return



def main():
    # will need to fail gracefully if not given arguments
    args = getArguments()
    file = args.file
    interface = args.i
    delay = args.delay
    limit = args.limit

    # load json
    # will need validate that the json is structured properly before progressing
    with open(file) as f:
        data = json.load(f)
    
    # cycle through the groups and send wake command to macs in that group
    for group in data['groups']:
        wakeGroup(group, interface, delay, limit)

    print('\n\nDone :)\n')
    os._exit(0)



if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
