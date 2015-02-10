#!/usr/bin/env python
# -*- coding: utf8 -*-
"""zebra-cups-minimal.py

Print the minimal document on the Zebra Label Printer.

We do expect to find the "zebra-raw" CUPS printer queue.
  
if you are using a Zebra USB printer on a Linux Machine, you should
have a look to list-cups-printer.py to identify the available 
CUPS printers

Copyright 2015 DMeurisse <info@mchobby.be> MC Hobby SPRL

Licence: CC-BY-SA-NC 

Cannot be reused for commercial product without agreement.
Please, contact us at <info@mchobby.be> 

------------------------------------------------------------------------
History:
  09 feb 2015 - Dominique - v 0.1 (first release). 
""" 
from pypcl import *
from pypcl import PrinterCupsAdapter
from pypcl import ZplDocument

PRINTER_ENCODING = 'cp850'
PRINTER_QUEUE_NAME = 'zebra-raw' # You have to add your Zebra as Generic > Raw printer in cups.
                                 # PRINTER_QUEUE_NAME is the shortname of the printer
                                 # in CUPS

def print_minimal_doc( ):
	""" Print the minimal document on Zebra. """
	
	print( 'Print the minimal ZPL document' )
	print( '------------------------------' )
	medium = PrinterCupsAdapter( printer_queue_name = PRINTER_QUEUE_NAME )
	d = ZplDocument( target_encoding = PRINTER_ENCODING, printer_adapter = medium, title = 'Minimal doc' )
	
	# Start a Print format
	d.format_start()
	
	# Write a field by assigning a font + size
	d.field( origin=(100,50), font=d.font('D',30,20), data=u'MC Hobby' )
	
	# write a second field by using default setting
	# Origin Y is set to 80. 80 = 50 (Y position here upper) + 30 (font height here upper).
	d.field( origin=(100,80), font=d.font('C'), data=u'Fun electronic hacking' ) 
	
	# End Print format
	d.format_end()

	
	medium.open() # Open the media for transmission. 
				  # With CUPS medium this open a temporary file
	try:
		d.send()  # With CUPS medium this send the data to the temporary file
		medium.flush() # With CUPS medium this close the temporary file and
		               #   sends to file to the print queue  
	finally:
		medium.close()  
		               
	
	del( medium )
    
if __name__ == '__main__':
	print_minimal_doc()
