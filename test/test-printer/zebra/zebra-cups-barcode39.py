#!/usr/bin/env python
# -*- coding: utf8 -*-
"""zebra-cups-barcode39.py

Print a document with BARCODE39 on the Zebra Label Printer.
BarCode39 bar codes can contains alphanumeric content.

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

def print_barcode39_doc( ):
	""" Print the Barcode39 document on Zebra. """
	
	print( 'Print the Barcode39 ZPL document' )
	print( '--------------------------------' )
	medium = PrinterCupsAdapter( printer_queue_name = PRINTER_QUEUE_NAME )
	d = ZplDocument( target_encoding = PRINTER_ENCODING, printer_adapter = medium, title = 'Barcode doc' )
	
	# Start a Print format
	d.format_start()

	# Origin Y is set to 80. 80 = 50 (Y position here upper) + 30 (font height here upper).
	#d.field( origin=(100,80), font=d.font('C'), data=u'Fun electronic hacking' ) 
	
	# Write a BarCode field
	d.field( origin=(120,11), font=d.font('E'), data=u'RASPBERRY.' )
	d.field( origin=(120,42), font=d.font('E'), data=u'Pi.2......' )
	d.barcode39( origin=(110,80), data=u'P0576', height_dots = 50 )
	
	d.field( origin=(140,160), font=d.font('C'), data=u'MC Hobby sprl' )
	d.field( origin=(130,180), font=d.font('C'), data=u'shop.mchobby.be' )
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
	print_barcode39_doc()
