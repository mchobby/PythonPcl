#!/usr/bin/env python
# -*- coding: utf8 -*-
"""hp-ip-raster-bitmap.py

How to print a Raster Graphic from Bitmap file on NETWORKED HP Printer.
This sample use no compression method.

See the following article to figure out how to create the bitmap file with Gimp
http://domeu.blogspot.be/2015/03/transformer-une-image-en-bmp-2-couleurs.html

This method can allow you to easily improve the design of document
content BUT required the usage of the PCL Symbol Set "PC-850 multilingual" 
sheet.  
  
Copyright 2015 DMeurisse <info@mchobby.be> MC Hobby SPRL

Licence: CC-BY-SA-NC 

Cannot be reused for commercial product without agreement.
Please, contact us at <info@mchobby.be> 

------------------------------------------------------------------------
History:
  27 feb 2015 - Dominique - v 0.1 (created from hp-ip-raster-unencoded.py with better coding)
""" 
from pypcl import *
from pypcl import HpPclDocument
from scipy import misc

PRINTER_IP = '192.168.1.206'
PRINTER_PORT = 9100
PRINTER_ENCODING = 'cp850'

def print_raster_graphic_unencoded( printer_socket ):
	""" Generate the PCL document containg a raw graphic image.
	    This sample is a basic implementation injecting raw esc sequences
	
	parameters:
		printer_socket : tuple (PRINTER_IP, PRINTER_PORT). On which
						 socket to print.
	"""
	
	print( 'Minimal Raster Graphic printing' )
	print( '-------------------------------' )
	print( 'Printer IP: %s\nPrinter Port: %i' % printer_socket )
	medium = PrinterSocketAdapter( printer_socket )
	
	# Very simple printout + usual initialization commands
	d = HpPclDocument( 'cp850', medium)
	d.reset_printer() # PCL to reset the printer

	d.write( u'Raster Graphic Test' )
    # Move the cursor to PCL unit position (300,400) within the PCL
    # coordinate system
    #   x-position: 300 unit @ 300 dot/inch --> 1 inch --> 2.54cm
    #   y-position: 400 unit @ 300 dot/inch --> 1.33 inch --> 3.38cm 
	d.cursor_move( (0,50) )
	
	# Set the Raster Graphics resolution (75 dpi)
	d.raster_set_resolution()
	
	# Raster Graphic Presentation Mode
	# -> Orientation of the logical page
	d.raster_presentation_mode() 
	 
	# Start Raster Graphic
	#  0 -> At x-position = 0
	#  1 -> At current x-position of the cursor position
	d.raster_start_graphic( at_current_cursor_pos = True ) 

	# Load the image present in local path
	# bitmap_tiny.bmp makes 100 pixels width & 101 pixels height.
	# @ raster_set_resolution = 75 dot per inch 
	# => 1.33 inch width x 1.34 inch width = ~3.378cm x ~3.403cm 
	image = misc.imread( 'bitmap_tiny.bmp', flatten='0' )
	print( "Image size (h,w) = (%i,%i)" % (len(image),len(image[0]) ) )
	
	
	
	d.raster_senddata_bitmap( image )

	# End Raster Graphic
	d.raster_end_graphic()
	
	# Move to position 
    # Move the cursor to PCL unit position (300,400) within the PCL
    # coordinate system
    #    This example use the 300 dots/inch as refernce for coordonate
    #    y-pos = under the raster --> 4 cm --> 1.57 inch @ 300 dot/inch --> 472 dots
	d.cursor_move( (300, 472) )

	d.writeln( u'End of test' )
		
	medium.open() # Open the media for transmission
	try:
		d.send() # Send the content of the current document
	finally:
		medium.close()
	
	del( d )
	del( medium )
    
if __name__ == '__main__':
	print_raster_graphic_unencoded( (PRINTER_IP, PRINTER_PORT) )
