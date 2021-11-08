# Magic-Text
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

<hr>

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
<hr>

Examples:

MagicText.exe add -i card.png -t text\WhiteText.wepb

    Add the Magic Text from text\WhiteText.wepb to card.png and output
    card.webp using max compression

MagicText.exe remove -i card.webp -o card.png

    Remove the magic text and output as card.png

MagicText.exe prep -i text\blacktext.png

    This will create blacktext.webp for use with the add command
    see notes below on required specs of input.
    
<hr>

Notes on the prep input images:

    The input image should be the same aspect ratio of images it is to be
    applied to and the size of the max expected size for the add input images.
    They should be a transparent image other than the small text/image you
    wish to be adding to other files. You can create these images easily with
    Photoshop, Gimp and many other tools.

    Example: A 3288 x 4488 image with white text close to the bottom right
    corner with everything transparent other than the text itself.
    
    See Examples directory for some samples
