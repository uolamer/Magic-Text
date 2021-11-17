# To package up as executable, run this in command prompt:
# (windows w/ UPX) C:\Python\Python39\Scripts\pyinstaller.exe --onefile --icon=MagicText.ico --upx-dir UPX\upx-3.96-win32 MagicText.py
# Edit UPX directory as needed or omit the UPX flags to build without.
import os
import sys
from PIL import Image
import numpy as np
import cv2
import argparse

# Show general info if ran with no arguments
def show_help():
    print('''
 • ▌ ▄ ·.  ▄▄▄·  ▄▄ • ▪   ▄▄·     ▄▄▄▄▄▄▄▄ .▐▄• ▄ ▄▄▄▄▄
 ·██ ▐███▪▐█ ▀█ ▐█ ▀ ▪██ ▐█ ▌▪    •██  ▀▄.▀· █▌█▌▪•██    
 ▐█ ▌▐▌▐█·▄█▀▀█ ▄█ ▀█▄▐█·██ ▄▄     ▐█.▪▐▀▀▪▄ ·██·  ▐█.▪  v1.0 by
 ██ ██▌▐█▌▐█ ▪▐▌▐█▄▪▐█▐█▌▐███▌     ▐█▌·▐█▄▄▌▪▐█·█▌ ▐█▌·  DrainLife
 ▀▀  █▪▀▀▀ ▀  ▀ ·▀▀▀▀ ▀▀▀·▀▀▀      ▀▀▀  ▀▀▀ •▀▀ ▀▀ ▀▀▀   
This program uses a custom method to apply an image of usually text on
another image so it can later be easily be identified and removed via a
method similar to content-aware fill in photoshop or gimp resynthesizer.

The alpha channel of the image is lost when adding Magic Text. This is
typically irrelivant unless the image needs transparency. Removing Magic Text
from an solid background should cause zero damage to an image. On varied
backgrounds the results can vary. The less varied the background and less
pixels added the less damage done.

It is not recommended to alter images with Magic Text on them without first
removing the Magic Text with this tool as it could cause this tool not to
recognize the Magic Text for removal.
──────────────────────────────────────────────────────────────────────────────
Commands:
    add     This adds Magic Text to an image
    remove  This removes Magic Text to an image
    prep    This creates a Magic Text image for use with the add command

Options: 
    -i      Input image filename for add, remove or prep (Required)

    -o      Output image filename for add, remove or prep (optional)
            if not specified output will be a webp file in the same
            directory as the input and will overwrite if filename exists.
            All files are saved lossless.

    -t      Magic Text filename. Required for add command.
    
    -x      PNG Compression level (optional) will default to 5 if
            not specified for add/remove and 6 for prep.
            Options: 5,6,7,8,9 (all compression is lossless)
──────────────────────────────────────────────────────────────────────────────
Examples:

MagicText.exe add -i card.png -t text\\WhiteText.wepb

    Add the Magic Text from text\\WhiteText.wepb to card.png and output
    card.webp using max compression

MagicText.exe remove -i card.webp -o card.png 

    Remove the magic text and output as card.png

MagicText.exe prep -i text\\blacktext.png

    This will create blacktext.webp for use with the add command
    see notes below on required specs of input.
──────────────────────────────────────────────────────────────────────────────
Notes on the prep input images:

    The input image should be the same aspect ratio of images it is to be
    applied to and the size of the max expected size for the add input images.
    They should be a transparent image other than the small text/image you
    wish to be adding to other files. You can create these images easily with
    Photoshop, Gimp and many other tools.
    
    Example: A 3288 x 4488 image with white text close to the bottom right
    corner with everything transparent other than the text itself.
──────────────────────────────────────────────────────────────────────────────''')
    sys.exit()

# Show help if no arguments are specified
if (len(sys.argv) < 2):
    show_help()

def add_text(input,output,compression,text):

    im = Image.open(input).convert('RGB') # Open input file
    txt = Image.open(text) # Open Magic Text file
    txt = txt.resize(im.size) # Resize text to match image
    txtp = txt.load() # Load text for scripting by pixel
    im = im.convert('RGBA')

    # Loop through all pixels merging image.
    for y in range(im.height):
        for x in range(im.width):
            if (txtp[x,y][3] == 254):
                r, g, b, a = txtp[x,y]
                im.putpixel( (x, y), (r, g, b, a) )

    # Create key to idenfity images that need processing later
    # The key is simply reducing the alpha value of the corners
    # by 1 while knowing near by pixels are 254/255
    txtp = im.load() #reusing old variable as it isnt needed anymore

    r, g, b, a = txtp[0,0] # Read in corner pixel
    a -= 1
    im.putpixel( (0, 0), (r, g, b, a) )
    r, g, b, a = txtp[im.width-1, 0]
    a -= 1
    im.putpixel( (im.width-1, 0), (r, g, b, a) )
    r, g, b, a = txtp[0, im.height-1]
    a -= 1
    im.putpixel( (0, im.height-1), (r, g, b, a) )
    r, g, b, a = txtp[im.width-1, im.height-1]
    a -= 1
    im.putpixel( (im.width-1, im.height-1), (r, g, b, a) )

    _, output_extension = os.path.splitext(output)
    if (output_extension.lower() == ".png" and compression < 6):
        # For 5 and below save with OpenCV using IMWRITE_PNG_STRATEGY_HUFFMAN_ONLY / cv2.IMWRITE_PNG_STRATEGY,2
        im = cv2.cvtColor(np.asarray(im), cv2.COLOR_RGBA2BGRA) # Covert PIL image to OpenCV
        cv2.imwrite(output, im, [cv2.IMWRITE_PNG_COMPRESSION, compression, cv2.IMWRITE_PNG_STRATEGY,2])# save our output
    elif (output_extension.lower() == ".png"):
        # PIL does a little better compression
        # im = im[:,:,::-1] # Fix color order for PIL BGR to RGB - Commented out as opened with PIL
        # im = Image.fromarray(im) # Convert array to image for PIL - Commented out as opened with PIL
        im.save(output, "PNG", option='optimize', compress_level=compression) # Save with PNG with PIL
    else:
        # Save WebP file via CV as it is faster & better
        im = cv2.cvtColor(np.asarray(im), cv2.COLOR_RGBA2BGRA) # Covert PIL image to OpenCV
        cv2.imwrite(output, im)
    sys.exit()

def remove_text(input,output,compression):

    # Read in the file.
    im = cv2.imread(input, cv2.IMREAD_UNCHANGED)
    if im is None:
        print('input file failed to open not a valid image')
        sys.exit()
    
    #Verify key exists
    if (im.shape[2] == 4 and (im[0,0][3] == 254 or im[0,0][3] == 253) and (im[im.shape[0]-1,0][3] == 254 or im[im.shape[0]-1,0][3] == 253) and (im[0,im.shape[1]-1][3] == 254 or im[0,im.shape[1]-1][3] == 253) and (im[im.shape[0]-1,im.shape[1]-1][3] == 254 or im[im.shape[0]-1,im.shape[1]-1][3] == 253) and im[1,1][3] > 253 and im[im.shape[0]-2,1][3] > 253 and im[1,im.shape[1]-2][3] > 253 and im[im.shape[0]-2,im.shape[1]-2][3] > 253):
        im[0,0][3] += 1 # Remove Key
        im[im.shape[0]-1,0][3] += 1 # Remove Key
        im[0,im.shape[1]-1][3] += 1 # Remove Key
        im[im.shape[0]-1,im.shape[1]-1][3] += 1 # Remove Key
        _, mask = cv2.threshold(im[:, :, 3], 254, 255, cv2.THRESH_BINARY_INV) # Create a PROPER mask to idenfity Magic Text
        im = im[:,:,:3] # Drop Alpha layer as inpaint needs it removed
        im = cv2.inpaint(im, mask, 3, cv2.INPAINT_NS) # Using NS Method for Magic Text removal
    else:
         print('Magic Text not found or image has been edited or corrupted')
         sys.exit()

    _, output_extension = os.path.splitext(output)
    if (output_extension.lower() == ".png" and compression < 6):
        # For 5 and below save with OpenCV using IMWRITE_PNG_STRATEGY_HUFFMAN_ONLY / cv2.IMWRITE_PNG_STRATEGY,2
        cv2.imwrite(output, im, [cv2.IMWRITE_PNG_COMPRESSION, compression, cv2.IMWRITE_PNG_STRATEGY,2])# save our output
    elif (output_extension.lower() == ".png"):
        # PIL does a little better compression
        im = im[:,:,::-1] # Fix color order for PIL BGR to RGB
        im = Image.fromarray(im) # Convert array to image for PIL
        im.save(output, "PNG", option='optimize', compress_level=compression) # Save with PNG with PIL
    else:
        # Save WebP file via CV as it is faster & better
        cv2.imwrite(output, im)
    sys.exit()

def prep_text(input,output,compression):

    im = Image.open(input) # Open input

    if im.mode != "RGBA":
        print ('This image is ' + im.mode + ' but this script requires RGBA')
        sys.exit()

    pix = im.load()

    i = 0
    found = 0
    # For loop to extract and print all pixels
    for y in range(im.height):
        for x in range(im.width):
            # getting pixel value using getpixel() method
            r, g, b, a = pix[x,y]
            if a:
                im.putpixel( (x, y), (r, g, b, 254) ) # Change all non transparent pixels to Alpha 254
                found += 1
            i += 1

    _, output_extension = os.path.splitext(output)
    if (output_extension.lower() == ".png" and compression < 6):
        # For 5 and below save with OpenCV using IMWRITE_PNG_STRATEGY_HUFFMAN_ONLY / cv2.IMWRITE_PNG_STRATEGY,2
        #im = Image.fromarray(im) # Convert array to image for PIL
        im = cv2.cvtColor(np.asarray(im), cv2.COLOR_RGBA2BGRA) # Covert PIL image to OpenCV
        cv2.imwrite(output, im, [cv2.IMWRITE_PNG_COMPRESSION, compression, cv2.IMWRITE_PNG_STRATEGY,2])# save our output
    elif (output_extension.lower() == ".png"):
        # PIL does a little better compression
        #im = im[:,:,::-1] # Fix color order for PIL BGR to RGB - Commented out as I opened with PIL
        #im = Image.fromarray(im) # Convert array to image for PIL - Commented out as I opened with PIL
        #im = im.load()
        im.save(output, "PNG", option='optimize', compress_level=compression) # Save with PNG with PIL
    else:
        # Save WebP file via CV as it is faster & better
        # im = Image.fromarray(im) # Convert array to image for PIL - Commented out as I opened with PIL
        im = cv2.cvtColor(np.asarray(im), cv2.COLOR_RGBA2BGRA) # Covert PIL image to OpenCV
        cv2.imwrite(output, im)
    sys.exit()


my_parser = argparse.ArgumentParser()
my_parser.add_argument('mode',
                       type=str,
                       help='The mode: add, remove or prep',
                       choices=['add', 'remove', 'prep']
                       )
my_parser.add_argument('-i',
                       '--input',
                       type=str,
                       help='The input image file name',
                       required=True)
my_parser.add_argument('-o',
                       '--output',
                       type=str,
                       help='The output image file name'
                       )
my_parser.add_argument('-t',
                       '--text',
                       type=str,
                       help='The prepped text image for the add command'
                       )
my_parser.add_argument('-x',
                       '--compression',
                       help='Optional: 1 through 9. Default is 5. Only applies to PNG saving',
                       type=int,
                       choices=list(range(1, 10))
                       )

args = my_parser.parse_args()

# Verify required variables and files exist and are valid
if not os.path.isfile(args.input):
    print('File does not exist: ' + args.input)
    sys.exit()

if (args.mode == 'add' and not args.text):
    print('add requires you to also specify a Maigic Test file')
    sys.exit()

if (args.mode == 'add' and not os.path.isfile(args.text)):
    print('File does not exist: ' + str(args.text))
    sys.exit()

# Verify removal or prep image is WebP/PNG
_, file_extension = os.path.splitext(args.input)
if ((args.mode == 'remove' or args.mode == 'prep') and not (file_extension.lower() == ".webp" or file_extension.lower() == ".png")):
    print('Magic Text can only remove or prep from PNG/WebP files')
    sys.exit()
elif not (file_extension.lower() == ".webp" or file_extension.lower() == ".png" or file_extension.lower() == ".jpg" or file_extension.lower() == ".jpeg"):
    print('Magic Text can only add to PNG/WebP/JPG/JPEG files')
    sys.exit()

# If output is not specified overwite input
if not args.output:
    args.output = args.input 

#Verify output is WebP/PNG
_, file_extension = os.path.splitext(args.output)
if not (file_extension.lower() == ".webp" or file_extension.lower() == ".png"):
    print('Magic Text can only save to PNG/WebP files')
    sys.exit()

if not args.compression:
    args.compression = 5

# Forcing level 6 compression for prep images
if (args.mode == 'prep' and args.compression < 6):
    args.compression = 6


# Due to speed difference using:
# Using PIL to save PNG, its 50% faster than cv2 at level 7
# im = Image.fromarray(im)
# im.save('delete.webp', option='optimize')

# Using OpenCV to save WebP
# cv2.imwrite('delete.webp', im)

# TO DO: Check for extra var when using add
if (args.mode == 'add'):
    add_text(args.input,args.output,args.compression,args.text)
elif (args.mode == 'remove'):
    remove_text(args.input,args.output,args.compression)
elif (args.mode == 'prep'):
    prep_text(args.input,args.output,args.compression)
else:
    print('no match ' + str(len(sys.argv)))
    show_help()

sys.exit()