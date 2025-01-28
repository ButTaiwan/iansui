# MenuTitle: [Iansui] Make build version
# -*- coding: utf-8 -*-
__doc__ = """
Make build version due to fontmake do not support corner components very well.
"""

from GlyphsApp import Glyphs, GSPath, GSComponent
#from AppKit import NSAffineTransform

err = False
for thisGlyph in Glyphs.font.glyphs:
	try:
		sourcelayer = thisGlyph.layers['Regular']
		#smartcomps = [comp for comp in sourcelayer.components if comp.componentName[0:6] == '_part.']
		corners = [hint for hint in sourcelayer.hints if hint.isCorner]
		if len(corners) == 0: continue

		print("Glyph: %s" % thisGlyph.name)
		sourcelayer.decomposeCorners()
		#if len(smartcomps) > 0:
		#	for comp in smartcomps: comp.decompose()

	except Exception as e:
		Glyphs.showMacroWindow()
		print("\n⚠️ Script Error:\n")
		import traceback
		print(traceback.format_exc())
		err = True

if not err:
	filePath = GetSaveFile(message="Select the file of build version to save", ProposedFileName="Iansui-build.glyphspackage", filetypes="glyphspackage")
	if filePath is not None:
		Font.save(filePath)