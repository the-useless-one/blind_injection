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
#  Copyright 2012 Yannick Méheut <useless (at) utouch (dot) fr>

import requests

def reverse_md5(hash_to_reverse):
	'''
	This function is used to reverse a MD5 hash.
	It uses an online tool: http://md5.gromweb.com/query/
	It then parses the result page to find the plain password.
	'''

	url = 'http://md5.gromweb.com/query/{0}'.format(hash_to_reverse)
	r = requests.get(url)

	# We retrieve the result page
	plain_password = r.text

	if plain_password:
		return plain_password
	else:
		return 'error: couldn\'t reverse hash'

def reverse_hash(hash_to_reverse):
	length = len(hash_to_reverse)

	if length == 32:
		return reverse_md5(hash_to_reverse)
	else:
		raise NotImplementedError

