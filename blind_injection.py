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

import os, sys, getopt
from blind_functions import *

def usage():
    '''
    This function is used to display the help message.
    It is displayed when the user uses the -h or --help options,
    when he forgets a mandatory argument, or when he uses an
    unknown option.
    '''

    print('-h, --help\tDisplay this message')
    print('-u, --url\tURL to perform the injection')
    print('-c, --chars\tFile of authorized characters')
    print('-s, --string\tString when success')
    print('--crack_hash\tUse the option if you want')
    print('\t\tthe program to reverse the hash')
    print('-l, --length\tLength of the field to retrieve')
    print('\t\tThe default value is 32 (md5 hash)')


def main():
    '''
    This is the main function. It parses the arguments
    and call the functions necessary to the injection.
    '''

    # We display a copyright message
    print('Blind Injection (Copyright 2012 Yannick Méheut <useless@utouch.fr>)\n')

    # We define the parameters
    target_url, authorized_characters, string_when_success = '', '', ''
    crack_hash = False
    length = 32

    # We retrieve the arguments
    try:
	opts, args = getopt.getopt(sys.argv[1:],
	    'hu:c:s:l:',
	    ['help', 'url=', 'chars=', 'string=', 'crack_hash', 'length='])
    except getopt.Getopterror as error:
	print(error)
	usage()
	sys.exit(1)

    for o, a in opts:
	if (o == '-h' or o == '--help'):
	    usage()
	    sys.exit()
	elif (o == '-u' or o == '--url'):
	    target_url = str(a)
	elif (o == '-c' or o == '--chars'):
	    if os.access(a, os.R_OK):
	    characters_file = open(a, 'r')
	    authorized_characters = characters_file.read()
	elif (o == '-s' or o == '--string'):
	    string_when_success = str(a)
	elif (o == '--crack_hash'):
	    crack_hash = True
	elif (o == '-l' or o == '--length'):
	    length = int(a)
	else:
	    print('unknown option: {0}'.format(0))
	    usage()
	    sys.exit(1)

    # If a mandatory argument is missing, we display and
    # error message, we call usage and we exit
    if not target_url:
	print('error: URL not specified')
	usage()
	sys.exit(1)
    if not authorized_characters:
	print('error: file of authorized characters not specified')
	usage()
	sys.exit(1)
    if not string_when_success:
	print('error: string when success not specified')
	usage()
	sys.exit(1)

    hash_password = blind_injection(target_url,
	authorized_characters,
	string_when_success,
	length)

    # We check if we need to reverse the hash
    if (crack_hash):
	reverse_hash(hash_password)

if __name__ == '__main__':
    main()

