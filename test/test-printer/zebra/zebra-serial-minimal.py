#!/usr/bin/env python
# -*- coding: utf8 -*-
"""Zebra-serial-minimal.py

Test the minimal document printing on a USB-SERIAL HP Printer
*** WHEN CUPS IS NOT INSTALLED!!! ***. 
  
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
							PrinterSerialAdapter roughly tested.
  
""" 
from pypcl import *
from pypcl import ZplDocument
from pypcl import PrinterSerialAdapter

PRINTER_DEVICE = '/dev/usb/lp0'
PRINTER_BAUD = 9600
PRINTER_ENCODING = 'cp850'

def print_minimal_doc( printer_device, printer_baud ):
	""" Generate the mininal ZPL document and print it on USB-Serial printer.
	
	parameters:
		printer_serial : tuple (PRINTER_SERIAL, PRINTER_BAUD). On which
						 serial port to print.
	"""
	
	print( 'Minimal ZPL Document printing' )
	print( '-----------------------------' )
	print( 'Printer Serial: %s\nPrinter Baud: %i' % (printer_device, printer_baud) )
	medium = PrinterSerialAdapter( printer_device, printer_baud )
	
	# Very simple printout + usual initialization commands
	d = ZplDocument( 'cp850', medium)
	
	# d.reset_printer() # PCL to reset the printer
	
	d.writeln( u'First' )
	d.writeln( u'Ticket' )
			
	medium.open() # Open the media for transmission
	try:
		d.send() # Send the content of the current document
	finally:
		medium.close()
	
	del( d )
	del( medium )
    
if __name__ == '__main__':
	print_minimal_doc( PRINTER_DEVICE, PRINTER_BAUD )
