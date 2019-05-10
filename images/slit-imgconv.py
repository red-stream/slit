#! /usr/local/bin/python
import sys
import site
import getopt
import string
from PIL import Image

def usage():
    print "SLIT - IMAGE CONVERT"
    print "USAGE: python slit-imgconv.py [option] infile outfile"
    print
    print "OPTIONS:"
    print
    print "  -c <format>  convert to format (default is given by extension)"
    print 
    print "  -b           batch conversion, buf infile and outfile must be directoies."
    print "               if the outfile directory does not exist. it will be created."
    print "               else the files in the directory may be overwritten."
    print 
    print "  -g           convert to greyscale"
    print "  -p           convert to palette image (using standard palette)"
    print "  -r           convert to rgb"
    print
    print "  -o           optimize output (trade speed for size)"
    print "  -q <value>   set compression quality (0-100, JPEG only)"
    print
    print "  -f           list supported file formats"
    sys.exit(0)

def PIL_conv(src, dst):
    try:
        img = Image.open(src)
        if convert and img.mode != convert:
            img.draft(convert, img.size)
            img = img.convert(convert)
        if format:
            apply(img.save, (dst, format), options)
        else:
            apply(img.save, (dst,), options)
    except:
        print "cannot convert image",
        print "(%s:%s)" % (sys.exc_type, sys.exc_value)

def batch_conv_pair(src, dst):
    import os
    tmp_list = list()
    pair = list()
    x_dst = False
    try:
        tmp_list = os.listdir(src)
    except:
        print "cannot convert image",
        print "(%s:%s)" % (sys.exc_type, sys.exc_value)

    try:
        os.listdir(dst)
        x_dst = True
    except OSError as ex:
        import errno
        if ex.errno != errno.ENOENT:
            print "cannot convert image",
            print "(%s:%s)" % (sys.exc_type, sys.exc_value)
    
    suffix = "jpg"
    if format:
        suffix = string.lower(format)

    for file in tmp_list:
        pair.append([(("%s/%s") % (src, file)), (("%s/%s.%s") % (dst, os.path.splitext(file)[0], suffix))])

    return x_dst, tuple(pair)

if len(sys.argv) == 1:
    usage()

try:
    opt, argv = getopt.getopt(sys.argv[1:], "c:bdfgopq:r")
except getopt.error, v:
    print v
    sys.exit(1)

batch = False
format = None
convert = None

options = { }

for o, a in opt:

    if o == "-f":
        Image.init()
        id = Image.ID[:]
        id.sort()
        print "Supported formats (* indicates output format):"
        for i in id:
            if Image.SAVE.has_key(i):
                print i+"*",
            else:
                print i,
        sys.exit(0)

    elif o == "-c":
        format = a

    if o == "-g":
        convert = "L"
    elif o == "-p":
        convert = "P"
    elif o == "-r":
        convert = "RGB"

    elif o == "-o":
        options["optimize"] = 1
    elif o == "-q":
        options["quality"] = string.atoi(a)
    elif o == '-b':
        batch = True
    

if len(argv) != 2:
    usage()

if batch:
    x_dst, convert_pair = batch_conv_pair(argv[0], argv[1])

    if x_dst == False:
        import os
        os.mkdir(argv[1])
    elif "continue" != raw_input("The OUTPUT DIR:\"%s\" is NOT EMPTY directory. Your files may be OVERWRITTEN. Are you sure you want to continue?[continue]:" % argv[1]):
        sys.exit(1)

    for src_img, dst_img in convert_pair:
        print src_img, ">", dst_img
        PIL_conv(src_img, dst_img)

else:
    PIL_conv(argv[0], argv[1])
