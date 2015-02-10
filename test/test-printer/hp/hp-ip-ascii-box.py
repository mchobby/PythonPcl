#!/usr/bin/env python
# -*- coding: utf8 -*-
"""hp-ip-minimal.py

Test the box border drawing (ASCII like) under code page 850 
on a NETWORKED HP Printer.

This method can allow you to easily improve the design of document
content BUT required the usage of the PCL Symbol Set "PC-850 multilingual" 
sheet.  
  
Copyright 2015 DMeurisse <info@mchobby.be> MC Hobby SPRL

Licence: CC-BY-SA-NC 

Cannot be reused for commercial product without agreement.
Please, contact us at <info@mchobby.be> 

------------------------------------------------------------------------
History:
  02 feb 2015 - Dominique - v 0.1 (first release)
""" 
from pypcl import *
from pypcl import HpPclDocument

PRINTER_IP = '192.168.1.206'
PRINTER_PORT = 9100
PRINTER_ENCODING = 'cp850'

def print_ascii_box_doc( printer_socket ):
	""" Generate the PCL document containg an ASCII like box.

	
	parameters:
		printer_socket : tuple (PRINTER_IP, PRINTER_PORT). On which
						 socket to print.
	"""
	
	print( 'Minimal ASCII Box Document printing' )
	print( '-----------------------------------' )
	print( 'Printer IP: %s\nPrinter Port: %i' % printer_socket )
	medium = PrinterSocketAdapter( printer_socket )
	
	# Very simple printout + usual initialization commands
	d = HpPclDocument( 'cp850', medium)
	d.reset_printer() # PCL to reset the printer
	d.symbol_set()    # Set the default symbol set (PC-850)
	d.horizontal_motion_index() # Set the default HMI to 0 = no horizontal motion
	d.paper_source()  # Set the default paper source to Tray + eject current page if any.
	d.pitch()         # Set 10 cpi size characters
	
	# Draw an ASCII like box with content (see symbol set PC-850 for details)
	# We do need to *** write binary data *** into the PclDocument
	# --- Line 1 ---
	d.write_bytes( bytes( chr(0xDA)+ chr(0xC4)*10+chr( 0xBF ) ) ) 
	d.writeln()
	# --- Line 2 --- 
	d.write_bytes( bytes( chr(0xB3) ) ) 
	d.write( u'Bordering ' )
	d.write_bytes( bytes( chr(0xB3) ) )
	d.writeln()
	# --- Line 3 ---
	d.write_bytes( bytes( chr(0xC0) + chr(0xC4)*10 + chr( 0xD9 ) ) ) 
		
	medium.open() # Open the media for transmission
	try:
		d.send() # Send the content of the current document
	finally:
		medium.close()
	
	del( d )
	del( medium )
    
if __name__ == '__main__':
	print_ascii_box_doc( (PRINTER_IP, PRINTER_PORT) )
