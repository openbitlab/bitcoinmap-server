#!/usr/bin/python
#
# Copyright (c) 2013-2014 Pavol Rusnak <stick@gk2.sk>
#
# This file is part of Coinmap
#
# Coinmap is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import os
import json
import json.encoder
from overpass import parser as overpass_parser

destdir = "/var/www/data/bitcoinmap"
scriptdir = os.path.dirname(os.path.abspath(__file__))

coins = {
	'Bitcoin': 'XBT',
	'Litecoin': 'XLT',
}

parsers = {
	'overpass': overpass_parser,
}

# update data/currencies
with open(scriptdir + '/coins.js', 'w') as f:
	f.write('function get_coins() { return ["%s"]; }\n' % '", "'.join(sorted(coins.keys())))

# call individual parsers
for name, parser in parsers.iteritems():
	pts = []
	
	pts1 = parser.get_points('bitcoin',coins['Bitcoin'])
	pts2 = [] #parser.get_points('litecoin',coins['Litecoin'])
	pts = pts1 + pts2
		
	json.encoder.FLOAT_REPR = lambda x: str(x) # fix for 52.1989256 showing as 52.198925299999999
	json.dump(pts, open(destdir + '/bitcoin.json', 'w'), separators = (',\n', ':'))
