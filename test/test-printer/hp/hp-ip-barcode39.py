#!/usr/bin/env python
# -*- coding: utf8 -*-
"""hp-ip-minimal.py

Test the document printing with BarCode on a NETWORKED HP Printer. 
  
Copyright 2015 DMeurisse <info@mchobby.be> MC Hobby SPRL

Licence: CC-BY-SA-NC 

Cannot be reused for commercial product without agreement.
Please, contact us at <info@mchobby.be> 

------------------------------------------------------------------------
History:
  05 feb 2015 - Dominique - v 0.1 (first release)
""" 
from pypcl import *
from pypcl import HpPclDocument
from pypcl import Barcode39
# from hpcode39 import Barcode39

PRINTER_IP = '192.168.1.203'
PRINTER_PORT = 9100
PRINTER_ENCODING = 'cp850'

def print_barcode_doc( printer_socket ):
	""" Generate the mininal PCL document INCLUDING CODE39 BARCODE
	and print it on network printer.
	
	parameters:
		printer_socket : tuple (PRINTER_IP, PRINTER_PORT). On which
						 socket to print.
	"""
	
	print( 'Minimal Barcode Document printing' )
	print( '---------------------------------' )
	print( 'Printer IP: %s\nPrinter Port: %i' % printer_socket )
	medium = PrinterSocketAdapter( printer_socket )
	
	# Very simple printout + usual initialization commands
	d = HpPclDocument( 'cp850', medium)
	d.reset_printer() # PCL to reset the printer
	d.spacing()       # Set the default Fixed spacing
	d.pitch()         # Default 10 characters per inch
	d.horizontal_motion_index() # Set the default HMI to 0 = no horizontal motion
	d.paper_source()  # Set the default paper source to Tray + eject current page if any.
	d.symbol_set()    # Set the default symbol set (PC-850)
	
	d.writeln( u'This a demonstration document' )
	d.writeln( u'including BarCode39 generation' )
	d.writeln()
	d.writeln( u'You can read the barcode with a product like Barcode')
	d.writeln( u' Reader/Scanner Module - CCD Camera - USB Interface' ) 
	d.writeln( u'Such module is available at http://shop.mchobby.be' )
	d.writeln( u'Those module are usually configured for Qwerty Keyboards' )
	d.writeln( u' where numbers are accessible on the first row' )
	d.writeln( u'When using French keyboards, you have to press the' )
	d.writeln( u' Shift key (or Shift Lock) to activate the numeric' )
	d.writeln( u' value on the first row' )
	d.writeln( u'Surprisingly, on Linux Mint, you have to press down the' )
	d.writeln( u' RIGHT SHIFT KEY to activate numbers on the first row!' )
	d.writeln( u' The best option is certainly to reconfigure your scanner' )
	d.writeln()
	d.writeln( u'Now, enjoy the Barcode 39 reading with your scanner :-) ')
	d.writeln()
	
	bc = Barcode39( d ) # Owner must be the document	
	bc.write( u'MCHP00189' ) # Write the bar code into the document
	d.writeln()
	d.writeln( '    '+bc.barcode_message(u'MCHP00189' ) )
	d.writeln()
	
	d.pitch(15) # 15 characters per inch
	bc.write( u'GGN00030365' ) # Write the barcode in the document
	d.writeln()
	d.writeln( '    '+bc.barcode_message(u'GGN00030365' ) )
		
	medium.open() # Open the media for transmission
	try:
		d.send() # Send the content of the current document
	finally:
		medium.close()
	
	del( d )
	del( medium )
    
if __name__ == '__main__':
	print_barcode_doc( (PRINTER_IP, PRINTER_PORT) )
