# Python Image Covolution
This was my term project for my Applied DSP class. It is currently a 3x3 matrix convolution (expandable) that has a GUI built from TKinter.

This program was my first foray into python programming, and since I previously used mostly C programming, I followed my old syntax scheme instead of following the (better) python naming and syntax scheme.

The program was programmed using globals and did not take advantage of many python features (which is very confusing now).

I am thinking of rewriting it to both A) improve my python, and B) to attempt to improve the speed by using numpy or OpenCL, or simply by using threads.

<br>

***

### Dependencies

* python 2.7
* PIL

<br>

***

### Example:

Taking the picture of my sister's dog:

![Original Image](https://github.com/FriedYeti/python-image-covolution/blob/master/bumbleKoda.png)

and applying an edge detection matrix:

![Convolution Matrix](https://github.com/FriedYeti/python-image-covolution/blob/master/ConvolutionMatrix.png)

gives the following result:

![Processed Image](https://github.com/FriedYeti/python-image-covolution/blob/master/processedImage.png)

***
<br>

### Explanations of image convolution:

[Wikipedia](https://en.wikipedia.org/wiki/Kernel_(image_processing))

[Interactive Explanation](http://setosa.io/ev/image-kernels/)
