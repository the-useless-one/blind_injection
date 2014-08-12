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
#  Copyright 2014 Yannick Méheut <useless (at) utouch (dot) fr>

import os
import sys
import argparse

import injection

def parse_arguments():
    '''
    This function is used to parse the arguments given on the command line.
    '''

    # We define an argument parser
    parser = argparse.ArgumentParser()

    # We define the arguments needed to perform the injection
    parser.add_argument('-u', '--url', required=True,
        help='URL where the injection will be performed')
    parser.add_argument('-s', '--string', type=str, required=True,
        help='string the script will look for in the binary search')
    parser.add_argument('-c', '--column', type=str, required=True,
        help='column you want to get')
    parser.add_argument('-t', '--table', type=str, required=True,
        help='table where the column is')
    parser.add_argument('-w', '--where', type=str, required=False,
        help='WHERE condition', default='')
    parser.add_argument('-i', '--index', type=int, required=False,
        help='index of the desired row', default=0)

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
    print('Blind Injection (Copyright 2014 Yannick Méheut <useless (at) utouch (dot) fr>)\n')

    # We get the argument
    args = parse_arguments()

    # We perform the injection
    result = injection.injection(args.url, args.string, args.column,
            args.table, args.where, args.index)

    if result:
        print('found: {0}'.format(result))
    else:
        print('no result found')

if __name__ == '__main__':
    main()

