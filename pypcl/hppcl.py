#!/usr/bin/env python
# -*- coding: utf8 -*-
"""hppcl.py

Class to print PCL document on Hewlett-Packard PCL Printer.

This class exposes method to help in generating PCL command enclosed
within the Text Stream to print.
  
Copyright 2015 DMeurisse <info@mchobby.be> MC Hobby SPRL

Licence: CC-BY-SA-NC 

Cannot be reused for commercial product without agreement.
Please, contact us at <info@mchobby.be> 

------------------------------------------------------------------------
History:
  01 feb 2015 - Dominique - v 0.1 (première release)
  05 feb 2015 - Dominique - Changing structure of PRINTER_SYMBOL_SET
"""
from pypcl import PclDocument, PyPclError, PCL_DATA_TYPE 

class HpPclDocument( PclDocument ):
	""" Class with helper function to generate PCL content for
		Hewlett Packard printer supporting PCL """
	PRINTER_CRLF = chr(13)+chr(10) # Go to begin of next line
	PRINTER_CR   = chr(13)         # return at the begin of the same line	
	PRINTER_ESC  = chr(27)
	
	PRINTER_CPI = [ 5, 9, 10, 12, 15, 16, 16.66, 20 ] # Character Per Inch supporter
	
	# Printer Units
	#   See PCL 5 "Printer Language Technical Referenc Manual", Cursor Positionning, pg 97
	PRINTER_UNIT_PCL = 0 
	
	PRINTER_UNITS = { PRINTER_UNIT_PCL: 'Unit PCL. default unit-per-inch = 300 dots per inch' }
	
	# Graphic Raster Infortmation
	RASTER_DPI_RESOLUTIONS = [75, 100, 150, 200, 300, 600] # Supported resolution when printing graphics 
	
	# Paper Source
	PRINTER_PAPER_SOURCE = { 0:  'Print the current page', # paper source remains unchanged.
							 1:  'Feed paper from the a printer-specific tray.', # prefered value to use when init the printer job
							 2:  'Feed paper from manual input.',
							 3:  'Feed envelope from manual input.',
							 4:  'Feed paper from lower tray.',
							 5:  'Feed from optional paper source.',
							 6:  'Feed envelope from optional envelope. feeder 1' }
							 
	PRINTER_SYMBOL_SET = { 'ISO-69'     : ('1F', 'ISO 69 : French'), 
						   'ISO-8859-1' : ('0N', 'ISO 8859-1 Latin 1 (ECMA-94)' ), 
						   'ASCII'      : ('0U', 'ISO 6:ASCII'), 
						   'LEGAL'      : ('1U', 'Legal'), 
					       'ROMAN-8'    : ('8U', 'Roman-8'),         # would allow to draw european/french accents and ponctuation
                           'PC-8'       : ('10U', 'PC-8, PC-437' ),  # would allow to draw ASCII borders, Code Page 437
                           'PC-437'     : ('10U', 'PC-8, PC-437' ),  # duplicate the name for easiest usage
                           'PC-850'     : ('12U', 'PCL PC-850 Multilingual'), # Rocks for french printing, Code Page 850 
                           'BARCODE-3-9': ('0Y' , '3 of 9 Barcode'), 
                           'ANSI'       : ('19U', 'Windows 3.1 Latin 1 (ANSI)') } 

	PRINTER_TYPEFACE = { 'Line Printer' : 0,
						 'Arial' : 16602,
						 'Antique Olive' : 4168,
						 'ITC Avant Garde' : 4127,
						 'CG Century Schoolbook' : 4119,
						 'CG Times' : 4101,
						 'Univers' : 4148 }
						 
	PRINTER_STYLE = { 'upright' : 0, #(upright, solid)
					  'italic': 1, 
					  'condensed': 4, 
					  'condensed-italic': 5, 
					  'compressed': 8, # or extra condensed
					  'expanded': 24,
					  'outline': 32, 
					  'inline': 64, 
					  'shadowed': 128, 
					  'outline-shadowed': 160 } 
					  
	PRINTER_STROKE_WEIGHT = { 'ultra-thin': -7,
							  'extra-thin': -6,
							  'thin': -5,
							  'extra-light': -4,
							  'light': -3,
							  'demi-light': -2,
							  'semi-light': -1,
							  'text': 0, # Medium, Book, or
							  'semi-bold': 1,
							  'demi-bold': 2,
							  'bold': 3,
							  'extra-bold': 4,
							  'black': 5,
							  'extra-black': 6,
							  'ultra-black': 7 }
							  
	def __init__(  self, target_encoding = 'cp850', printer_adapter = None, title = '' ):
		""" initialisisation of PclDocument and specific HpPclDocument information """
		super( HpPclDocument, self ).__init__( target_encoding, printer_adapter, title )
		
		# Define the Default Printer Unit
		self._current_unit = self.PRINTER_UNIT_PCL
		self._unit_per_inch = 300 # Nombre of unit per inch (default, UNIT_PCL is dot-per-inch and set to 300 dot per inch) 
							  
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
	# === Properties ===
	@property
	def current_unit( self ):
		""" identify the type of unit used on the printer (one of the PRINTER_UNITS).
			default is PRINTER_UNIT_PCL """
			
		return self._current_unit
		
	@property
	def unit_per_inch( self ):
		""" Returns the number of "unit per inch". This depends on:
		1) the current_unit currently selected on the printer
		2) the potential change of unit_per_inch (résolution) for PCL Printing 
		
		The usual default is PCL_UNIT with 300 dots_per_inch as unit_per_inch
		"""
		return self._unit_per_inch
				
			
	# === HP Specific Tools ===
	def write_esc( self, unicode_seq ):
		""" Append ESCAPE SEQUENCE command string in the document """
		self.append( (PCL_DATA_TYPE.PCL,self.PRINTER_ESC+unicode_seq) )
		# raw debugging print( unicode_seq + ' ')
		
	def reset_printer( self ):
		""" send a RESET PRINTER to pcl printer """
		self.write_esc( u'E' )
	
	# === HP PCL features ===	
	def paper_source( self, source = 1 ):
		""" set the paper source for the printer. Should be one of
		the HpPclDocument.PRINTER_PAPER_SOURCE values. 

		The default 1 value is "Feed paper from the a printer-specific tray.
		which rocks on usual printing with PCL from HP3015 tray"

		*** IMPORTANT ***:
		The Paper Source command causes the current page to be printed
		and the cursor to be moved to the left edge of the logical page at the
		top margin position for the next page"""
		
		assert isinstance( source, int ), 'source must be an integer!'
		assert source in self.PRINTER_PAPER_SOURCE.keys(), 'source must be a PRINTER_PAPER_SOURCE.keys() value'
		
		self.write_esc( u'&l%iH' % source )
		
	def symbol_set( self, value = 'PC-850' ):
		""" Set the symbol set for the document (PCL PC-850 by default). 
		Only one can be selected at the time. If the specified symbol set 
		does not exist, Roman-8 is automatically selected by the printer.
		
		The Symbol Set identifies the specific set of symbols in a
		font. “Symbols” are the alphanumeric, punctuation, or any other
		printable characters or symbols which may be included.
		
		By example, Roman-8 & PC-850 would allow you to use accentuation
		like é where PC-8 would allow you to draw ASCII like borders."""
		assert isinstance( value, str ), 'value must be string'
		assert value in self.PRINTER_SYMBOL_SET, 'value not in PRINTER_SYMBOL_SET'
		
		self.write_esc( u'(%s' % self.PRINTER_SYMBOL_SET[value][0] ) # use the PCL code of Symbol_set
		
	def pitch( self, characters_per_inch = 10 ):
		""" Set the pitch - character size in 'Character Per Inch'.  Should be
		in the range of supported HpPclDocument.PRINTER_CPI values. 
		
		5   cpi  =  36+ columns in portrait, ? landscape   -- reserve it for big title 
		9   cpi  = 
		10  cpi  =  80 columns in portrait, 113+ landscape -- Normal Text, column header
		12  cpi  =  96 columns in portrait, 136  landscape -- detailed information (smaller) 
		15  cpi  =                                         -- used for small and discrete information
		16  cpi  = 132 columns in portrait, 160 landscape -- 16.66 cpi
		20  cpi  = 160 columns in portrait, 220+ landscape
		"""
		assert isinstance(characters_per_inch, int) or isinstance(characters_per_inch,float), 'parameter must be an int or float'
		assert characters_per_inch in self.PRINTER_CPI, 'must be one of the PRINTER_CPI values %s' % self.PRINTER_CPI
		
		if isinstance(characters_per_inch, int):
			self.write_esc( u'(s%iH' % characters_per_inch )
		else:
			self.write_esc( u'(s%.2fH' % characters_per_inch )

	def spacing( self, fixed_spacing = True ):
		""" Allow to define the character spacing for the primary selected
		font. By default, it is Fixed spacing, otherwise proportinal 
		spacing will be used. Proportionnal spacing is applied only
		if the selected primary font supports it. """
		assert isinstance( fixed_spacing, bool ), 'parameter must be boolean'
		
		self.write_esc( u'(s%iP' % (0 if fixed_spacing else 1) ) # use )s%iP to fix the secondary font spacing
		
	def horizontal_motion_index( self, increment = 0 ):
		""" Allow to define the HMI (horizontal motion index). Read the
		technical reference about "Horizontal Motion Index" for more
		information. 
		
		increment (int): is the 1/120 inch of index increment. 0 to 
				disable the feature."""
		
		assert isinstance( increment, int ), 'parameter must be int' 
		
		self.write_esc( u'&k%iH' % increment )

	def vertical_motion_index( self, increment = 6 ):
		""" Allow to define the VMI (vertical motion index). Read
		the technical reference about 'Horizontal Motion Index" for
		more information.
		
		increment (int): is the 1/48 inch index increment. 0 to no
			vertical movement.
			
		The default factory setting is 8.
		vmi = 8 -> 6 lines-per-inch.
		vmi = 6 -> 8 lines-per-inch (recommended) 
		
		Common setting:
		  vmi = 7.27 -> allow to print 66 lines on a portrait page
		                 (with a half inch margin on the top and bottom)
		       (10 inch-height / 66 lines-per-page ) x 48 = 7.27 
		       
		  vmi = 5.45 -> allow to print 66 lines on a landscape letter page
		                 (with a half inch margin on the top and bottom)

		       (7.5 inch-heigh / 66 lines-per-page ) x 48 = 5.45
		       
		  vmi = 6 -> allow to print up to 84 lignes on a A4 page!
					 should be verified!
				29.5cm - 1.1cm margin top - 1.7cm margin bottom = 26.7cm
				26.7cm / 2.54 cm-per-inch = 10.51 inch
				
				vmi = 11.51 inch / 84 lines-per-page * 48 = 6.57
				
		  vmi = 8 -> allow to print up to 63 lines on a A4 page!
					 should be verified
					 
				29.5cm - 1.1cm margin top - 1.7cm margin bottom = 26.7cm
				26.7cm / 2.54 cm-per-inch = 10.51 inch

				vmi = 11.51 inch / 63 lines-per-page * 48 = 8.007
		  """
			
		assert isinstance( increment, int) or isinstance( increment, float ), 'parameter must be int or float'
		
		if isinstance( increment, int ):
			self.write_esc( u'&l%iD' % increment)
		else:
			self.write_esc( u'&l%.4fD' % increment)

	def typeface_familly( self, typeface_name ):
		""" Change the primary font TypeFace (design of the font) with one
		of the supported PRINTER_TYPEFACE values """
		
		assert isinstance( typeface_name, str ), 'typeface must be a string' 
		assert typeface_name in self.PRINTER_TYPEFACE.keys(), 'invalid typeface name %s' % typeface 
		
		self.write_esc( u'(s%iT' % self.PRINTER_TYPEFACE[typeface_name] )

	def height( self, height_point = 12 ):
		""" Change the height of the font (in point) with default 
			to 12 point (as mentionned in the PCL documentation).
			
			Accordingly to the documentation, this value is ignored
			when using 'fixed spacing font' (but stored anyway to be used 
			when using a non 'fixed spacing font')"""
		assert isinstance( height_point, int ) or isinstance( height_point, float ), 'parameter must be float or int'
		
		if isinstance( height_point, int ):
			self.write_esc( u'(s%iV' % height_point )
		else:
			self.write_esc( u'(s%.2fV' % height_point )

	def style( self, style_name ):
		""" The style (font-style) identifies the posture of a character, 
		its width, and structure of the font symbols. """
		
		assert isinstance( style_name, str), 'parameter must be a string' 
		assert style_name in self.PRINTER_STYLE, 'invalid %s style_name' % style_name
		
		self.write_esc( u'(s%iS' % self.PRINTER_STYLE[style_name] ) 

	def stroke_weight( self, stroke_name ):
		""" designates the thickness of the strokes that compose the 
		characters of a font. """
		
		assert isinstance( stroke_name, str ), 'parameter must be a string'
		assert stroke_name in self.PRINTER_STROKE_WEIGHT, 'invalid %s stroke_name' % stroke_name 
		
		self.write_esc( u'(s%iB' % self.PRINTER_STROKE_WEIGHT[stroke_name] )
		
	def bold( self, set_bold = True ):
		""" Easiest switch of bold/non-bold text. """
		self.stroke_weight( 'bold' if set_bold else 'text' )
		
	def cursor_move( self, position, unit = None ):
		""" Move the cursor to x,y position. Distance expressed in PCL Unit.
		
		By default, PCL Unit is unit_per_inch = 300 dot/inch """
		if unit == None:
			unit = self._current_unit
		
		assert unit in self.PRINTER_UNITS, "This unit is not supported"
		assert isinstance( position, tuple ) and len(position)==2, "position must be a (x_position,y_position) tuple" 
		
		self.write_esc( u'*p%ix%iY' % position )
		
	# === Raster Graphic BASIC TOOLS ===
	
	def raster_start_graphic( self, at_current_cursor_pos = True ):
		""" Start Raster Graphic (with data)
			False : 0 -> At x-position = 0
			True : 1 -> At current x-position of the cursor position """
		self.write_esc( u'*r%iA' % (1 if at_current_cursor_pos else 0 ) )
	
	def raster_end_graphic( self ):
		""" Ends a Raster Graphic part """
		self.write_esc( u'*rC' )
		
	def raster_presentation_mode( self ):
		""" Raster Graphic Presentation Mode.
		
		*** ONLY SUPPORT A DEFAULT AT THE MOMENT ***
		
		use the default  0 -> Orientation of the logical page. """
		self.write_esc( u'*r%iF' % (0) )

	def raster_set_resolution( self, dpi_resolution = 75 ):
		""" Set the Raster Graphics resolution in dpi (default = 75 dpi) """
		assert isinstance( dpi_resolution, int ), 'params must be int' 
		assert dpi_resolution in self.RASTER_DPI_RESOLUTIONS, 'dpi_resolution must be in %s' % ( self.RASTER_DPI_RESOLUTIONS )
		
		self.write_esc( u'*t%iR' % (dpi_resolution) )

	 
	def raster_senddata_str( self, lst ):
		""" Print the image, stored as list of bit (encoded into string for
			easy code writing, use a space every 8 bits for reading, 
			the space are ignored by the code)
		
			example:
				>>> d.raster_senddata_str( ['00000000 00000000 10000000 00000000', '00000000 00000000 11000000 00000000' ] ) 
		"""
		assert isinstance( lst, list ) and len( lst )>0, 'parameter must be a list of string' 
		assert isinstance( lst[0], str), 'parameter must be a list of string'
		
		lst_int = []
		for line in [l.replace(' ','') for l in lst]:
			lst_int.append( [int(c) for c in line] )	

		# Here, lst_int contains a structure like the following
		# print( lst_int )
		# [ [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
		#   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
		#   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
		#   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ]
		return self.raster_senddata_int( lst_int )

	def raster_senddata_int( self, lst ):
		""" Print the image, stored as list of integer (one integer per bit).
			This function is reserverd for easy code writing
		
			example:
				>>> d.raster_senddata_int( [ [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ] ) 
		"""
		assert isinstance( lst, list ) and len( lst )>0, 'parameter must be a list of (list of int). Each int 1 or 0 is a dot!'
		assert isinstance( lst[0], list) and len(lst[0])>0 , 'parameter must be a list of (list of int). Each int 1 or 0 is a dot!'
		assert isinstance( lst[0][0], int ), 'parameter must be a list of (list of int). Each int 1 or 0 is a dot!'
		
		def split_by_n( seq, n ):
			"""A generator to divide a sequence into chunks of n units."""
			while seq:
				yield seq[:n]
				seq = seq[n:]
				
		def arr_to_bytes( lst ):
			""" this function produce a "bytes" type from list of ASCII code 
		
				arr_to_bytes( [0,0,248,0] ) -> '\x00\x00\xf8\x00' 
			"""
			return bytes( ''.join( [ chr(x) for x in lst ] ) )
		
		
		# Create an array of Bit position and corresponding Decimal Weight
		lBitWeight = [ (iIndex,2**(7-iIndex)) for iIndex in range(8) ]
		
		for row in lst:
			#print( '--- ROW ---' )
			lDecValue = [] # List of the decimal value to eject to the printer
			iByteCount =  len(row)/8
			if len(row)%8 > 0: # if we have some bits more then add a byte
				iByteCount += 1
			self.write_esc( u'*b%iW' % iByteCount ) # how many bytes to write.

			#Split in seq of 8 int/8 bits.
			for bits in split_by_n( row, 8 ):
				# Ensure just 8 bits (pad right with 0 if needed) 
				bits = bits+[0]*(8-len(bits))
				# encode the bits as a decimal value
				iDecValue = 0
				for iIndex, iWeight in lBitWeight:
					iDecValue += bits[iIndex]*iWeight
				lDecValue.append( iDecValue )

			#print( lDecValue )
			self.write_bytes( arr_to_bytes( lDecValue ) )
