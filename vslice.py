#!/usr/bin/env python
#
# Slice an image into the specified number of vertical slices.
#
# Andy Duplain <trojanfoe@gmail.com> 26-Feb-2014
#
# 修改切分部分，允许图元之间存在间隙，同时允许输入，行数列数
#
# spritePig <wuanshi5@gmail.com> 4-5-2016
#

import sys, os
from optparse import OptionParser
from PIL import Image

progName = None

def vslice(inputName, outputPath, baseName, sliceNumW, sliceNumH, sliceGapW, sliceGapH, options):

    if options.zeroFill:
        outputFileFormat = "{0}-{1:03d}.png"
    else:
        outputFileFormat = "{0}-{1}.png"        

    image = Image.open(inputName)
    width, height = image.size
    sliceWidth = (width - (sliceNumW-1)*sliceGapW) / sliceNumW
    sliceHeight = (height - (sliceNumH-1)*sliceGapH) / sliceNumH
    

    print "{0}: Image size={1}x{2}, sliceNum={3},{4}".format(progName, width, height, sliceWidth, sliceHeight)
    if sliceWidth <= 1 or sliceHeight <= 1:
        print "slice width or height too small!"

    for row in range(0, sliceNumH):
        y = row*sliceHeight + row*sliceGapH

        for col in range(0, sliceNumW):
            # Box is (left, upper, right, bottom) and NOT (x, y, width, height)...
            x = col*sliceWidth + col*sliceGapW
            box = (x, y, x + sliceWidth, y + sliceHeight)
            slice = image.crop(box)
            slice.load()

            if options.cropOutput:
                outputImage = Image.new(image.mode, (sliceWidth, sliceHeight))
                outputImage.paste(slice, (0, 0, sliceWidth, sliceHeight))
            else:
                outputImage = Image.new(image.mode, (width, height))
                outputImage.paste(slice, box)

            outputName = os.path.join(outputPath, outputFileFormat.format(baseName, row*sliceNumW + col + 1))
            outputImage.save(outputName, "PNG")
            print "{0}: Saved slice {1} to {2}".format(progName, row*sliceNumW + col + 1, outputName)
    
    return True

def main():
    global progName
    progName = os.path.basename(sys.argv[0])
    parser.add_option("-c", "--crop-output", dest="cropOutput", action="store_true", default=False, help="Crop output image to slice")
    parser.add_option("-z", "--zero-fill", dest="zeroFill", action="store_true", default=False, help="Zero-fill numbered output filenames")
    (options, args) = parser.parse_args()
    if len(args) != 6:
        parser.error("Incorrect number of arguments")

    inputName = args[0]
    outputPath = args[1]
    sliceNumW = int(args[2])
    sliceNumH = int(args[3])
    sliceGapW = int(args[4])
    sliceGapH = int(args[5])

    if sliceNumH < 2 or sliceNumW < 2:
        parser.error("Incorrect number of slices")

    if sliceGapW <= 0 or sliceGapH <= 0:
        parser.error("Incorrect gap size!")

    if not os.path.exists(outputPath):
        os.mkdir(outputPath)

    baseName = os.path.splitext(inputName)[0]

    vslice(inputName, outputPath, baseName, sliceNumW, sliceNumH, sliceGapW, sliceGapH, options)

    print "{0}: Done.".format(progName)
    return 0

if __name__ == "__main__":
    sys.exit(main())
