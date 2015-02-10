#!/usr/bin/env python
# -*- coding: utf8 -*-
"""hp-ip-minimal.py

  Generate the PCL document printing a same line with various 
  font and style. Test on a NETWORKED HP Printer.
		  
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

def print_font_demo( printer_socket ):
	""" Generate the PCL document printing a same line with various 
		font and styles.
		
		=== PAY ATTENTION === 
		The way the printer will act with various commands and print
		depend on the selected font (the font kind), the printer model
		and the parameters (not all the parameters works for a font).
		
		You will find many documentation in the "PCL 5 Printer Language
		Technical Reference Manual", Ch 8: PCL Font Selection 
		
	parameters:
		printer_socket : tuple (PRINTER_IP, PRINTER_PORT). On which
						 socket to print.
	"""
	
	print( 'Font demo' )
	print( '---------' )
	print( 'Printer IP: %s\nPrinter Port: %i' % printer_socket )
	medium = PrinterSocketAdapter( printer_socket )
	
	d = HpPclDocument( 'cp850', medium)
	d.reset_printer() # PCL to reset the printer
	d.paper_source()  # Set the default paper source to Tray + eject current page if any.
	
	d.pitch( 12 )     # Set 12 cpi size characters
	d.bold() 
	d.writeln( u'Here an exemple of font assignment' )
	d.writeln()
	d.bold( False )
	
	# Follow this sequence of characteristic when assigning a font
	#  1) Symbol set      (eg: ASCII)
    #  2) Spacing         (eg: Fixed)
	#  3) Pitch           (eg: 16.66)
	#  4) Height          (eg: 8.5 point)
	#  5) Style           (eg: Upright)
	#  6) Stroke weight   (eg: Medium)
	#  7) Typeface family (eg: Line Printer)
	
	for typeface_name in d.PRINTER_TYPEFACE.keys(): 
		d.symbol_set() # CP-850 
		d.spacing() # Set fixed
		d.pitch( 16.66 )
		d.height( 8.5 )
		d.style( 'upright' )
		#d.style( 'italic' )
		
		d.stroke_weight( 'text' ) # You can use set bold for easier bold switch on/off
		d.typeface_familly( typeface_name ) 
		d.writeln( u'Printing abcdef.klmnopq ABC ITC.GAU with %s typeface' % typeface_name )
					
	medium.open() # Open the media for transmission
	try:
		d.send() # Send the content of the current document
	finally:
		medium.close()
	
	del( d )
	del( medium )
    
if __name__ == '__main__':
	print_font_demo( (PRINTER_IP, PRINTER_PORT) )
