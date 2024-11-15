#!/usr/bin/env python3

# MIT License
# 
# Copyright (c) 2024 ricaun
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Convert SVT to Multi-Page Tiff using Output extension.
"""

### Versions
## 1.0.0 - 2024-11-13 - Initial Release
## 1.0.1 - 2024-11-13 - Change python license to comment.
## 1.1.0 - 2024-11-14 - Add `take_multiple_snapshot` to improve speed.

__version__ = "1.1.0"

import os
import io
import inkex

from PIL import Image, TiffImagePlugin
from inkex.command import write_svg, inkscape
from inkex.extensions import TempDirMixin, OutputExtension

def take_multiple_snapshot(svg, dirname, name="snapshot", ext="png", dpis=[96,144,192,288,384], **kwargs):
	"""
	Take multiple snapshot of the given svg file.

	Resulting filenames is yielded back, after generator finishes, the
	files is deleted so you must deal with the file inside the for loop.
	"""
	
	svg_file = write_svg(svg, dirname, name + ".svg")
	ext_files = [os.path.join(dirname, name + str(dpi) + '.' + str(ext).lower()) for dpi in dpis]

	actions = " ".join([
		f"export-filename:{file}; export-dpi:{dpi}; export-do;"
		for file, dpi in zip(ext_files, dpis)
	])

	inkscape(
		svg_file, actions=actions, **kwargs
	)
	return ext_files

class MultiPageTiffOutput(OutputExtension):
	def add_arguments(self, pars):
		pars.add_argument("--tab")
		pars.add_argument("--compression", default="tiff_deflate")
		# Dpi
		pars.add_argument("--dpi_10", type=inkex.Boolean, default=True)
		pars.add_argument("--dpi_15", type=inkex.Boolean, default=True)
		pars.add_argument("--dpi_20", type=inkex.Boolean, default=True)
		pars.add_argument("--dpi_30", type=inkex.Boolean, default=True)
		pars.add_argument("--dpi_40", type=inkex.Boolean, default=True)
		pars.add_argument("-i", "--dpi", type=float, default=96.0)

	def save(self, stream):
		self.tiff_file = os.path.join(self.tempdir, "input.tiff")

		d = self.options.dpi
		images = []
		dpis = []
		if self.options.dpi_10: dpis.append(d)
		if self.options.dpi_15: dpis.append(d*1.5)
		if self.options.dpi_20: dpis.append(d*2.0)
		if self.options.dpi_30: dpis.append(d*3.0)
		if self.options.dpi_40: dpis.append(d*4.0)
		
		filenames = take_multiple_snapshot(
			self.document,
			dirname=self.tempdir,
			dpis=dpis,
		)
		
		for filename in filenames:
			img = Image.open(filename)
			images.append(img)

		# Save the images as a multi-page TIFF with specified DPI
		with TiffImagePlugin.AppendingTiffWriter(self.tiff_file, new=True) as tf:
			for im in images:
				im.save(tf, dpi=im.info["dpi"],compression=(self.options.compression or None))
				tf.newFrame()

		if os.path.isfile(self.tiff_file):
			with open(self.tiff_file, "rb") as fhl:
				stream.write(fhl.read())

if __name__ == "__main__":
	MultiPageTiffOutput().run()
