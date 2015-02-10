#!/usr/bin/env python
# -*- coding: utf8 -*-
"""list-cups-printers.py

List the available printer queues installed on the local computer.
You will identify the available printer installed on CUPS (see
  all de demo*.* files for more informations).

We do expect to find the "zebra-raw" printer.
  
if you are using a Zebra USB printer on a Linux Machine, you should
have a look to zebra-cups-minimal.py

Before starting this script, you should have a look to the demo-x.x files
where you will learn lots of things.

Copyright 2015 DMeurisse <info@mchobby.be> MC Hobby SPRL

Licence: CC-BY-SA-NC 

Cannot be reused for commercial product without agreement.
Please, contact us at <info@mchobby.be> 

------------------------------------------------------------------------
History:
  07 feb 2015 - Dominique - v 0.1 (first release). 
							PrinterCupsAdapter roughly tested.
  
""" 
from pypcl import *
from pypcl import PrinterCupsAdapter

PRINTER_ENCODING = 'utf8'

def list_cups_printer( ):
	""" List the cups printer available on the system. """
	
	print( 'List CUPS printer' )
	print( '-----------------' )
	medium = PrinterCupsAdapter()
	
	medium.open() # Open the media for transmission
	try:
		medium.dump_printers()
	finally:
		medium.close()
	
	del( medium )
    
if __name__ == '__main__':
	list_cups_printer()
