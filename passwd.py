#!/usr/bin/env python
import sys
import os
import argparse,string,random

""" generate random password string: http://stackoverflow.com/a/2257449 """

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def main():
    usage = "usage: %prog [options]  "
    parser = argparse.ArgumentParser(description='generate password string')
    parser.add_argument("-length", metavar='length', type=int, help="integer length of password", default=6)
    args=parser.parse_args()
    print id_generator(args.length)


if __name__ == "__main__":
    main()
