#!/usr/bin/env python
# -*- coding: utf8 -*-
"""test-HpPclDocument.py

Test the features of the HP PCL Printing class. 
  
Copyright 2015 DMeurisse <info@mchobby.be> MC Hobby SPRL

Licence: CC-BY-SA-NC 

Cannot be reused for commercial product without the agreement.
Please, contact us at <info@mchobby.be> 

------------------------------------------------------------------------
History:
  02 feb 2015 - Dominique - v 0.1 (first release)
""" 
from pypcl import *
from pypcl import HpPclDocument

def test_direct():
	""" Demontrate usage of the HpPclDocument list structure. You should
	use the exposed method. """
	 
	print ('Direct HpPclDocument appending' )
	print ('------------------------------' )
	d = HpPclDocument()
	d.append( (PCL_DATA_TYPE.PCL, u'test' ) )
	d.append( (PCL_DATA_TYPE.TEXT, u'test2' ) )
	d.append( (PCL_DATA_TYPE.TEXT, u'test3' ) )
	d = d +  (1, u'test4') 

	print( '#items: %i' % len(d) )
	print( d )
	del( d )

def test_minimal_doc():
	""" Generate the mininal PCL document """
	
	print( 'Minimal HpPclDocument' )
	print( '---------------------' )
	d = HpPclDocument()
	d.reset_printer()
	d.write( u'This is my first document' )
	d.write( u'which accept ecute é and others' )
	
	print( '#items: %i' % len(d) )
	print( d )
	del( d )
    
if __name__ == '__main__':
	test_direct()
	test_minimal_doc()
