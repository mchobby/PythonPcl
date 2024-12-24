#!/usr/bin/env python
# -*- coding: utf8 -*-
"""toolbox.py

contains many tools functions and class.

Copyright 2015 DMeurisse <info@mchobby.be> MC Hobby SPRL

Licence: CC-BY-SA-NC 

Cannot be reused for commercial product without agreement.
Please, contact us at <info@mchobby.be> 

------------------------------------------------------------------------
History:
  09 feb 2015 - Dominique - v 0.1 (first release)
"""
from functools import reduce

def ean13_checksum(ean_base):
	"""Calculates the checksum for EAN13-Code.
	   special thanks to python-barcode
	   http://code.google.com/p/python-barcode/source/browse/barcode/ean.py?r=3e6fe8dbabbf49726a4f156657511e941f7743df
	
	ean_base (str) - the 12 first positions of the ean13. 
	
	returns (int) - the checkdigit (one number)
	
	example: ean13_checksum( '323210000576' ) --> 1
	"""
	sum_ = lambda x, y: int(x) + int(y)
	evensum = reduce(sum_, ean_base[::2])
	oddsum = reduce(sum_, ean_base[1::2])
	return (10 - ((evensum + oddsum * 3) % 10)) % 10

def calculate_ean13( ean_base ):
	"""compose the full ean13 from ean base (12 position) + calculated checksum
	
	example: calculate_ean13( '323210000576' ) --> '3232100005761' """
	return ean_base+str(ean13_checksum(ean_base))
