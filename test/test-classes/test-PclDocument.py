#!/usr/bin/env python
# -*- coding: utf8 -*-
"""test-PclDocument.py

Test the features of the base class PclDocument. 
  
Copyright 2015 DMeurisse <info@mchobby.be> MC Hobby SPRL

Licence: CC-BY-SA-NC 

Cannot be reused for commercial product without the agreement.
Please, contact us at <info@mchobby.be> 

------------------------------------------------------------------------
History:
  01 feb 2015 - Dominique - v 0.1 (première release)
""" 

from pypcl import *

l = PclDocument()
l.append( (PCL_DATA_TYPE.PCL, u'test' ) )
l.append( (PCL_DATA_TYPE.TEXT, u'test2' ) )
l.append( (PCL_DATA_TYPE.TEXT, u'test3' ) )
l = l +  (1, u'test4') 

print( len(l) )
print( l )
