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

<h2>Commands:</h2>

   <b>add</b>     This adds Magic Text to an image

   <b>remove</b>  This removes Magic Text to an image

   <b>prep</b>    This creates a Magic Text image for use with the add command

<h2>Options:</h2>

   <b>-i</b>   Input image filename for add, remove or prep (Required)

   <b>-o</b>   Output image filename for add, remove or prep (optional)
            if not specified output will be a webp file in the same
            directory as the input and will overwrite if filename exists.
            All files are saved lossless.

   <b>-t</b>   Magic Text filename. Required for add command.

   <b>-x</b>   PNG Compression level (optional) will default to 5 if
            not specified for add/remove and 6 for prep.
            Options: 5,6,7,8,9 (all compression is lossless)
<hr>

<h2>Examples:</h2>

    MagicText.exe add -i card.png -t text\WhiteText.wepb

   Add the Magic Text from text\WhiteText.wepb to card.png and output
   card.webp using max compression

    MagicText.exe remove -i card.webp -o card.png

   Remove the magic text and output as card.png

    MagicText.exe prep -i text\blacktext.png

   This will create blacktext.webp for use with the add command
   see notes below on required specs of input.
    
<hr>

<h2>Notes on the prep input images:</h2>

   The input image should be the same aspect ratio of images it is to be
   applied to and the size of the max expected size for the add input images.
   They should be a transparent image other than the small text/image you
   wish to be adding to other files. You can create these images easily with
   Photoshop, Gimp and many other tools.

   Example: A 3288 x 4488 image with white text close to the bottom right
   corner with everything transparent other than the text itself.
    
   <b>See Examples directory for some samples</b>
<hr>
<h2>How this software works</h2>

The short answer is we take the input image, remove the alpha layer, add back an alpha layer making all pixels non transparent (Alpha 255) and the magic text is resized to match your input and added with an Alpha value of 254. In this process pixels are flat out replaced by the Magic Text. We also set key pixels in each corner to either Alpha 253 or Alpha 252 as a key to identify an image that has Magic Text. To remove the Magic Text we make sure the key exists and then remove the key by setting the Alpha of those corner pixels to 255. We then create a mask of all pixels that are below Alpha 255, in this case it that will be just the Magic Text we put there. This mask is sort of like using a magic wand in PhotoShop. We replace those pixels with something similar to content-aware fill in PhotoShop, in this case OpenCV Image Inpainting, to replace those pixels.

<hr>
<h2>Future considerations & improvments</h2>

The way the key code works could be improved as it currently can leave corner pixels behind that was Magic Text if Magic Text was added to a corner pixel. This could be easily fixed in a future version. Basically any part of this program could be replaced with a future or better library and still work with existing images. Currently I am using a combination of Python Pillow and OpenCV. I originally was working with Pillow until I found OpenCV and it's Image Inpainting. Some methods are still using Pillow though they could be converted to OpenCV or Numpy code. From the little expermenting I did Pillow did a better job at compressing PNG at level 6 or higher than OpenCV and that is one reason I have not changed any code on that end. It should be possible to take advantage of CUDA or many other things. This code also could be converted to C++ or something else if there is a need/reason. For now this working code with the logic in place.
