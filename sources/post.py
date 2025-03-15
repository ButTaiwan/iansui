import glob
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._v_h_e_a import table__v_h_e_a

for file in Path("fonts").glob("**/*.ttf"):
	font = TTFont(str(file))
	if font["gasp"].gaspRange != {65535: 0x000A}:
		font["gasp"].gaspRange = {65535: 0x000A}

	try:
		del font["prep"]
	except KeyError:
		pass

	# In this case, the sTypo values are set 60 units beyond the emBox (940 vs 880). So we subtract 60 from the side-specific locations, and set the heights to match the UPM (or emBox). 

	#Calculate the adjustment to the sTypo metrics versus the emBox. (this assumes sTypo is set based on emBox)
	glyphHeight = font["OS/2"].sTypoAscender - font["OS/2"].sTypoDescender 
	adjustment = int((glyphHeight - font["head"].unitsPerEm	) / 2)

	#if this adjustment value is 0, as in to say the sTypo values are set aligned with the emBox, then no adjustments will occur. 

	newHeight = font["head"].unitsPerEm
	
	for i in font["vmtx"].metrics:
		if font["vmtx"].metrics[i][0] == glyphHeight:
			font["vmtx"].metrics[i] = (newHeight,font["vmtx"].metrics[i][1]-adjustment)
	
	table__v_h_e_a.recalc(font["vhea"],font)
	font.save(file)