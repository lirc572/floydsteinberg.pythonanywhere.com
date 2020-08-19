# -*- coding: utf-8 -*-
"""
@author: lirc572
Convert an image to PPM format for EPD75BHD library (https://github.com/lirc572/EPD75BHD)
This script implements the Floyd–Steinberg dithering algorithm to
convert images to a format that only has 3 colors: red, black and
white, without grayscale.
For more information on Floyd–Steinberg algorithm, refer to its Wikipedia page.
"""
__all__ = ['dither']

import sys
import os

from PIL import Image

def euclideanDistance(color1, color2):
    return ((color1[0]-color2[0])**2+(color1[1]-color2[1])**2+(color1[2]-color2[2])**2)

def findClosestColor(color):
    dist_red   = euclideanDistance(color, (255, 0, 0))
    dist_black = euclideanDistance(color, (0, 0, 0))
    dist_white = euclideanDistance(color, (255, 255, 255))
    if (dist_red<=dist_black and dist_red<=dist_white):
        return (255, 0, 0)
    if (dist_black<=dist_red and dist_black<=dist_white):
        return (0, 0, 0)
    if (dist_white<=dist_black and dist_white<=dist_red):
        return (255, 255, 255)

def colorDiff(color1, color2):
    return (color1[0]-color2[0], color1[1]-color2[1], color1[2]-color2[2])

def colorSum(color1, color2):
    return toValidColor((int(color1[0]+color2[0]), int(color1[1]+color2[1]), int(color1[2]+color2[2])))

def toValidColor(color):
    color = list(color)
    for i in range(3):
        if color[i] < 0:
            color[i] = 0
        elif color[i] > 255:
            color[i] = 255
    return tuple(color)

def dither(src, tgt, w, h):
    try:
        img = Image.open(src)
    except:
        print('Error reading image "%s"' % (src,))
        return False
    if w and h:
        img = img.resize((w, h))
    print(img.format, img.size, img.mode)
    print('Converting to rbw ppm...')
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            old_pixel   = img.getpixel((x, y))
            new_pixel   = findClosestColor(old_pixel)
            img.putpixel((x, y), new_pixel)
            quant_error = colorDiff(old_pixel, new_pixel)
            if x+1 < img.size[0]:
                img.putpixel((x+1, y), colorSum(img.getpixel((x+1, y)), tuple(map(lambda x: x*7/16, quant_error))))
            if x > 0 and y+1 < img.size[1]:
                img.putpixel((x-1, y+1), colorSum(img.getpixel((x-1, y+1)), tuple(map(lambda x: x*3/16, quant_error))))
            if y+1 < img.size[1]:
                img.putpixel((x, y+1), colorSum(img.getpixel((x, y+1)), tuple(map(lambda x: x*5/16, quant_error))))
            if x+1 < img.size[0] and y+1 < img.size[1]:
                img.putpixel((x+1, y+1), colorSum(img.getpixel((x+1, y+1)), tuple(map(lambda x: x/16, quant_error))))
    if os.path.exists(src):
        os.remove(src)
    img.save('%s.png' % (tgt,))
    ppm_content = "P3\n%d %d\n1\n" % (img.size)
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            px = tuple(img.getpixel((x, y))[:3])
            pix = (1,0,0) if px==(255,0,0) else (1,1,1) if px==(255,255,255) else (0,0,0)
            ppm_content += "%d %d %d\n" % pix
    with open('%s.ppm' % (tgt,), 'w') as f:
        f.write(ppm_content)
    print('Conversion finished!')
    return True