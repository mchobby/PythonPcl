#!/usr/bin/env python
# -*- coding: utf8 -*-
"""zpl.py

Class to print Zebra PCL document on my Zebra Label Printer LP 2824 Plus.

This class exposes method to help in generating ZPL command enclosed
within the Text Stream to print.
  
Copyright 2015 DMeurisse <info@mchobby.be> MC Hobby SPRL

Licence: CC-BY-SA-NC 

Cannot be reused for commercial product without agreement.
Please, contact us at <info@mchobby.be> 

------------------------------------------------------------------------
History:
  07 feb 2015 - Dominique - v 0.1 (première release)
"""

from pypcl import *

class ZplDocument( PclDocument ):
	""" Class with helper function to generate ZPL content for
		Zebra printer supporting ZCL.
	
		Have been tested on a Zebra LP 2824 Plus Label Printer and
		Direct Thermal Paper Zipship labels "Z-select 2000d Label 
		32x25mm 2580/roll" """
	PRINTER_CRLF = chr(10)          # CR/LF for Zebra can be a #10 LineFeed char
	#PRINTER_CR   = chr(13)         # return at the begin of the same line	
	PRINTER_ESC  = chr(0x5E)        # ^ escape command for ZPL
	
	# Font Information - coming from ZPL II programming Guide, pg 373
	# The tuple is formatted as follow  
	#    (Heigh,Width) - default Height and Height in dots
	#    [types]       - list of types U=uppercase,L=Lowercase, D=descenders (goes below the base line)
	#    IntercharGap  - int, space between characters in dots. -1 for Proportional.
	#    BaseLine      - lambda, define where is positionned the baseline from the top of the matrix.
	#                         this is important for Descenders font where some characters like "p" can go under the base line.
	#                    The parameter of lambda function is Height. May return an int or a float
	#
	# Note that some definitions are missing and remplaced by None 
	# See also wikipedia Typograpgy article:
	#    http://en.wikipedia.org/wiki/Descender 
	PRINTER_FONT = { 'A' : ( (9,5)  , ['U','L','D'], 1, lambda h: 7     ),
					 'B' : ( (11,7) , ['U']        , 2, lambda h: 11    ),
					 'C' : ( (18,10), ['U','L','D'], 2, lambda h: 14    ),
					 'D' : ( (18,10), ['U','L','D'], 2, lambda h: 14    ),
					 'E' : ( (28,15), ['OCR-B']    , 5, lambda h: 23    ),
					 'F' : ( (26,13), ['U','L','D'], 3, lambda h: 21    ),
					 'G' : ( (60,40), ['U','L','D'], 8, lambda h: 48    ),
					 'H' : ( (21,13), ['OCR-A']    , 6, lambda h: 21    ),
					 'O' : ( (15,12), []           ,-1, lambda h: 3*h/4 ),
					 'GS': ( (24,24), ['SYMBOL']   ,-1, lambda h: 3*h/4 ),
					 'P' : None,
					 'Q' : None,
					 'R' : None,
					 'S' : None,
					 'T' : None, # Use 17, 8 as size for a nice Bold effect
					 'U' : None,
					 'V' : None }
					 
	PRINTER_ORIENTATION_NORMAL   = 'N'
	PRINTER_ORIENTATION_ROTATED  = 'R' # rotated 90 degrees (clockwise)
	PRINTER_ORIENTATION_INVERTED = 'I' # inverted 180 degrees
	PRINTER_ORIENTATION_BOTTOMUP = 'B' # read from bottom up, 270 degrees
	
	
	PRINTER_ORIENTATION = [ PRINTER_ORIENTATION_NORMAL, PRINTER_ORIENTATION_ROTATED, PRINTER_ORIENTATION_INVERTED, PRINTER_ORIENTATION_BOTTOMUP ]	 	

	# === Override ===	
	def sending( self ):
		""" sending() is called when PclDocument.send() want  me to 
		send the data to the printer over the medium """
		for pcl_line_tuple in self:
			if pcl_line_tuple[0] == PCL_DATA_TYPE.PCL:
				self.printer_adapter.send( bytes( pcl_line_tuple[1].encode( 'UTF-8' ) ) ) # Escape sequences are in UTF8
			elif pcl_line_tuple[0] == PCL_DATA_TYPE.TEXT:
				self.printer_adapter.send( bytes( pcl_line_tuple[1].encode( self.target_encoding ) ) )
			else: # Binary 
				self.printer_adapter.send( pcl_line_tuple[1] ) # Tuple[1] already contains a bytes() type	
		
	# === Tools ===
	def print_quantity( self, qty ):
		self.writeln( u'^PQ%i,0,0,Y' % qty)
		
	def format_start( self ):
		self.writeln( u'^XA' )
		
	def format_end( self ):
		self.writeln( u'^XZ' )
		
	def field( self, origin, font, data ):
		""" allows to write a field data in one shot
		
		origin (tuple) = (x_position_dots, y_position_dots). (50,50) or (50,100) for 1.25" x 1" label on LP 2824.
		font (tuple) = (font_type, font_height_dots, font_width_dots ). See definition of field_font() for more info. 
		data (unicode) = Data to print out. """
		
		self.field_origin( origin )
		if font != None: 
			self.field_font( font ) # font type, font width dot, font height dots
		self.field_data( data )
		self.field_separator()
		
	def barcode39( self, origin, data, height_dots = 50 ):
		""" allows to draw a barcode 39 on the label """
		assert isinstance( origin, tuple ) and len( origin )==2, "origin must be a tuple (x-dots,y-dots)"
		assert isinstance( origin[0], int ) and isinstance( origin[1], int ), "origin must contains integers values" 
		assert isinstance( data, unicode ), "Data must be unicode string" 
		assert isinstance( height_dots, int ), "height_dots must be an interger"
		
		self.field_origin( origin )
		self.field_barcode39( ZplDocument.PRINTER_ORIENTATION_NORMAL, False, height_dots, True, False )
		self.field_data( data )
		self.field_separator()
		
	def ean13( self, origin, ean, height_dots = 50 ):
		""" allows to draw a ean13 on the label """
		assert isinstance( origin, tuple ) and len( origin )==2, "origin must be a tuple (x-dots,y-dots)"
		assert isinstance( origin[0], int ) and isinstance( origin[1], int ), "origin must contains integers values" 
		assert isinstance( ean, unicode ), "Data must be unicode string"
		assert ( len( ean )==13 ) and (ean.isdigit() ), "ean must have 13 digits only"  
		assert isinstance( height_dots, int ), "height_dots must be an integer"
		
		self.field_origin( origin )
		self.field_ean13( ZplDocument.PRINTER_ORIENTATION_NORMAL, height_dots, True, False )
		self.field_data( ean )
		self.field_separator()

	def field_origin( self,origin ):
		""" set the origin of a field data """ 
		assert isinstance( origin, tuple ) and len(origin)==2, "origin must be a tuple (x-dots,y-dots)"
		assert isinstance( origin[0], int ) and isinstance( origin[1], int ), "origin must contains integers values" 
		 
		self.write( u'^FO%i,%i' % origin )
	
	def field_barcode39( self, orientation = PRINTER_ORIENTATION_NORMAL, mod43_checksum = False, height_dots = 50, interpretation_line = True, interpretation_above = False ):
		""" Write a field entry for barcode 39. Data must be send into a field_data() """
		assert orientation in self.PRINTER_ORIENTATION, "Invalid orientation %s not in range %s" % ( orientation, self.PRINTER_ORIENTATION.keys() ) 
		
		self.write( u'^B3%s,%s,%i,%s,%s' % ( orientation, 'Y' if mod43_checksum else 'N', height_dots, 'Y' if interpretation_line else 'N', 'Y' if interpretation_above else 'N' ) )
	
	def field_ean13( self, orientation = PRINTER_ORIENTATION_NORMAL, height_dots = 50, interpretation_line = True, interpretation_above = False ): 
		assert orientation in self.PRINTER_ORIENTATION, "Invalid orientation %s not in range %s" % ( orientation, self.PRINTER_ORIENTATION.keys() ) 
		
		self.write( u'^BE%s,%i,%s,%s' % ( orientation, height_dots, 'Y' if interpretation_line else 'N', 'Y' if interpretation_above else 'N' ) )
		   
	def field_font( self, font ):
		""" Set the font of a field 
		
		font (tuple) - (zebra-font-code, font-height-dots, font-width-dots)
					   see PRINTER_FONT dictionnary for available values.
					   Smallest font is 18,10 -> 180, 100
					   
					   You can use the function font() to create the tuple.
		"""
		assert isinstance( font, tuple ) and len(font)==3, "font must be a tuple (font-code,height-dots,width-dots)"
		assert isinstance( font[0], str ), "font code must be str" 
		assert font[0] in self.PRINTER_FONT, "invalid font %s" % font[0]
		assert isinstance( font[1], int ) and isinstance( font[2], int ), "font height and width must contains integers values" 
		
		self.write( u'^A%sN,%i,%i' % font )
	
	def font( self, font_code, font_height_dots = None, font_width_dots = None ):
		""" Create a font tuple for field_font(). 
		
		It is better to use this function because we could improve font
		support in the future ;-)
		
		Good documentation on font can be found in "ZPL II programming Guide"
		   pg 371, "Fonts and bar codes". 
		See also Font Typography on wikipedia
		   http://en.wikipedia.org/wiki/Descender
		See also the PRINTER_FONT structure
		
		A good font sample is font('D',36,20) which fit into a 1.25" x 1.00" label """
		
		assert isinstance( font_code, str ), 'font_code must be string' 
		assert ((font_height_dots == None) or isinstance( font_height_dots, int)) and ((font_width_dots == None) or isinstance( font_width_dots, int )), "height and width must be integers"
		assert font_code in self.PRINTER_FONT, "invalid font %s, not in PRINTER_FONT %s" % (bfont_code, self.PRINTER_FONT.keys() )
		#assert (font_height_dots == None) or (18 <= font_height_dots <= 180), "height must be in between 18..180"
		#assert (font_width_dots == None) or (10 <= font_width_dots <= 100), "width must be in between 10..100"
		
		if font_height_dots == None:
			if self.PRINTER_FONT[font_code] == None:
				raise PyPclError( 'cannot resolve default height for font %s' % font_code )
			else:
				font_height_dots = self.PRINTER_FONT[font_code][0][0] # PRINTER_FONT[font_code][0] -> first tuple item => (default_height,default_width)
		if font_width_dots == None:
			if self.PRINTER_FONT[font_code] == None:
				raise PyPclError( 'cannot resolve default width for font %s' % font_code )
			else:
				font_width_dots = self.PRINTER_FONT[font_code][0][1] # PRINTER_FONT[font_code][0] -> first tuple item => (default_height,default_width)
		
		return ( font_code, font_height_dots, font_width_dots )	
		
	def field_data( self, data ):
		""" just send the data of the field. Should be followed by field
		separator """
		assert isinstance( data, unicode ), 'Data must be unicode' 
		
		self.writeln( u'^FD%s' % data )

	def field_separator( self ):
		""" each field (starting with field_origin() must ends with field_separator() """
		self.writeln( u'^FS' )
