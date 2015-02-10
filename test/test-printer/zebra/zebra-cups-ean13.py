#!/usr/bin/env python
# -*- coding: utf8 -*-
"""zebra-cups-ean13.py

Print a document with EAN13 on the Zebra Label Printer.
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
from pypcl import calculate_ean13

PRINTER_ENCODING = 'cp850'
PRINTER_QUEUE_NAME = 'zebra-raw' # You have to add your Zebra as Generic > Raw printer in cups.
                                 # PRINTER_QUEUE_NAME is the shortname of the printer
                                 # in CUPS

def print_ean13_doc( ):
	""" Print the ean13 document on Zebra. """
		
	# 3232 is used for belgian courrier, let say the following '1' to identify product and 576 for id_product
	ean_base = '323210000576'   
	ean13 = calculate_ean13( ean_base )
	print ean13
	
	print( 'Print the EAN13 ZPL document' )
	print( '----------------------------' )
	medium = PrinterCupsAdapter( printer_queue_name = PRINTER_QUEUE_NAME )
	d = ZplDocument( target_encoding = PRINTER_ENCODING, printer_adapter = medium, title = 'Barcode doc' )
	
	# Start a Print format
	d.format_start()

	# Write a BarCode field
	d.field( origin=(120,11), font=d.font('E'), data=u'RASPBERRY.' )
	d.field( origin=(120,42), font=d.font('E'), data=u'Pi.2......' )
	d.ean13( origin=(130,80), ean=unicode(ean13), height_dots = 50 )
	
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
	print_ean13_doc()
