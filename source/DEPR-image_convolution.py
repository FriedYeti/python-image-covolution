import os
import PIL.Image
import time
from Tkinter import *

# =============================================Initialize Variables=============================================#
size = 256, 256  # Size of thumbnail image displayed
newValue = list((0, 0, 0))
convMask = 3
normalizer = 1
errorMessage = ""

previewBox = 0

convMatrix = [[0 for x in range(convMask)] for x in range(convMask)]  # matrix used for 2D image convolution
newColor = list((0, 0, 0))
for x in range(0, convMask):
    for y in range(0, convMask):
        convMatrix[x][y] = 0
        # cnt = cnt+1
convMatrix[1][1] = 1

# ----------------------------------------------Load Images----------------------------------------------#
image = PIL.Image.open("bumbleKoda.png")  # Open default image to memory
thumbnailImage = PIL.Image.open("bumbleKoda.png")  # Open another copy of image, to be used as thumbnail
thumbnailImage.thumbnail(size, PIL.Image.ANTIALIAS)  # Turn thumbnailImage into a image with max 'size' of size

# ----------------------------------------------Pre Process Images----------------------------------------------#
if image.mode != 'RGB':  # Removes alpha channel if RGBA, sets to RGB if other
    image = image.convert('RGB')
if thumbnailImage.mode != 'RGB':
    thumbnailImage = image.convert('RGB')

pixels = image.load()  # Holds all pixel data as a 3 tuple in a 2D array
thumbnailPixels = thumbnailImage.load()
newPixels = pixels  # To be used when processing, will hold new image while processing

imageWidth = image.size[0]
imageHeight = image.size[1]

# =============================================Initialize GUI=============================================#
root = Tk()  # Initialize Tkinter for GUI


# ----------------------------------------------GUI Functions----------------------------------------------#
def image_load():  # loads the image and displays it on screen
    global thumbnailImage
    global pixels
    global thumbnailPixels
    global newPixels
    global image
    global imageWidth
    global imageHeight
    global size
    global errorMessage
    global previewBox
    global newImage

    filePath = path.get()  # Retrieve file path from UI

    start = time.clock()  # timer (debug message)
    if filePath == "":
        errorMessage = "Error: Image path is blank"
        update_error()

    elif os.path.isfile(filePath) == FALSE:
        errorMessage = "Error: File does not exist"
        update_error()

    else:
        image = PIL.Image.open(filePath)  # Open image to memory
        newImage = image
        thumbnailImage = PIL.Image.open(filePath)  # Open another copy of image, to be used as thumbnail

        if image.mode != 'RGB':  # Removes alpha channel if RGBA, sets to RGB if grayscale/monotone
            image = image.convert('RGB')
        if thumbnailImage.mode != 'RGB':
            thumbnailImage = image.convert('RGB')

        imageWidth = image.size[0]
        imageHeight = image.size[1]

        pixels = image.load()  # 2D array containing all of the pixel data in image
        thumbnailPixels = thumbnailImage.load()  # 2D array containing all fo the pixel data in thumbnailImage
        newPixels = newImage.load()  # to be used in processing, holds new image while processing
        thumbnailImage.thumbnail(size,
                                 PIL.Image.ANTIALIAS)  # Turn thumbnailImage into a image with max width and height of 'size'
        thumbnailImage.save("tempThumbnail.gif")  # image to be loaded to UI

        photo = PhotoImage(file="tempThumbnail.gif")  # load image to UI
        display_image.configure(image=photo)
        display_image.photo = photo

        stop = time.clock()  # timer (debug message)
        print "Image loaded and displayed in %f seconds." % (stop - start)  # debug message

        errorMessage = ""  # Clears error message on UI
        update_error()


def apply_matrix():  # Need to properly set this up!
    global pixels
    global newPixels
    global image
    global imageHeight
    global imageWidth
    global newImage
    global convMatrix
    global convMask
    global normalizer
    global previewBox

    if previewBox:
        imageStart = 2
        imageStopWidth = 128
        imageStopHeight = 128
    else:
        imageStart = 2
        imageStopWidth = imageWidth-2
        imageStopHeight = imageHeight-2

    start = time.clock()  # timer (debug message)
    for x in range(imageStart, imageStopWidth):  # Image Rows, ignore outside pixels
        print x,"/",(imageStopWidth)
        for y in range(imageStart, imageStopHeight):  # Image Columns, ignore outside pixels
            newColor = list((0, 0, 0))  # clear newColor for next loop
            for r in range((-convMask + 1)/2, (convMask - 1)/2 + 1):  # +/- X values for convolution
                for q in range((-convMask + 1)/2, (convMask - 1)/2 + 1):  # +/- Y values for convolution
                    color = list(pixels[x + r, y + q])  # receive color of pixel being weighted and added
                    for i in range(0, 3):  # for each R, G, and B
                        newValue[i] = color[i] * convMatrix[q + 1][r + 1] / normalizer
                        newColor[i] = newColor[i] + newValue[i]  # sum all in r and q area
            for j in range(0, 3):  # clip R,G,B channels
                if newColor[j] > 255:
                    newColor[j] = 255
                elif newColor[j] < 0:
                    newColor[j] = 0
            newPixels[x, y] = tuple(newColor)  # convert back to tuple, store in new location

    newImage.save("processedImage.png")
    newImage.thumbnail(size, PIL.Image.ANTIALIAS)  # processed image to be displayed to UI
    newImage.save("processedImageThumbnail.gif")
    newImage = PIL.Image.open("processedImage.png") #reload to avoid resize issues
    update_image()
    stop = time.clock()  # timer (debug message)
    print "Image processed in", (stop - start), "seconds."  # debug message

def update_image():  # Updates image displayed on UI to most recently processed one

    photo = PhotoImage(file="processedImageThumbnail.gif")
    display_image.configure(image=photo)
    display_image.photo = photo


def update_matrix():  # updates the normalizer and each value of the convolution matrix to what was entered by user
    global normalizer
    global convMatrix
    convMatrix[0][0] = int(matrix_1_1.get())
    convMatrix[0][1] = int(matrix_1_2.get())
    convMatrix[0][2] = int(matrix_1_3.get())
    convMatrix[1][0] = int(matrix_2_1.get())
    convMatrix[1][1] = int(matrix_2_2.get())
    convMatrix[1][2] = int(matrix_2_3.get())
    convMatrix[2][0] = int(matrix_3_1.get())
    convMatrix[2][1] = int(matrix_3_2.get())
    convMatrix[2][2] = int(matrix_3_3.get())
    normalizer = int(normalizer_entry.get())


def update_error():  # updates the error message displayed on screen
    global error_message
    error_message.configure(text=errorMessage)  # updates text displayed

def swap_checkbox_value():
    global previewBox
    if previewBox == 1:
        previewBox=0;
    else:
        previewBox=1;
    print previewBox

# ----------------------------------------------GUI Widgets----------------------------------------------#
# -------------------------Left Side Widgets-------------------------#
frame = Frame(root, bg="white")  # base frame for other elements
frame.pack(side=LEFT)

quit_button = Button(frame, text="QUIT", command=frame.quit)
quit_button.pack(side=BOTTOM, fill=X)

apply_filter = Button(frame, text="Apply Matrix Filter", command=apply_matrix)
apply_filter.pack(side=TOP, fill=X)

preview_checkbox = Checkbutton(frame, text="Small Section Preview", command=swap_checkbox_value)
preview_checkbox.pack(side=TOP, fill=X)

load_image = Button(frame, text="Load Image", command=image_load)
load_image.pack(side=TOP, fill=X)

path = Entry(frame)  # text entry field, for Load image
path.pack(side=TOP, fill=X)

photo = PhotoImage(file="blankThumbnail.gif")
display_image = Label(frame, image=photo)
display_image.photo = photo
display_image.pack(side=BOTTOM)

# -------------------------Right Side Widgets-------------------------#
frame_right = Frame(root) #main right frame
frame_right.pack(side=RIGHT)

frame_right_first = Frame(frame_right) #holds Update button and normalizer entry
frame_right_first.pack(side=TOP)

frame_right_second = Frame(frame_right) #holds first row of convolution matrix
frame_right_second.pack(side=TOP)

frame_right_third = Frame(frame_right) #holds second row of convolution matrix
frame_right_third.pack(side=TOP)

frame_right_fourth = Frame(frame_right) #holds third row of convolution matrix
frame_right_fourth.pack(side=TOP)

frame_right_fifth = Frame(frame_right) #hold error message
frame_right_fifth.pack(side=TOP)

update_matrix_button = Button(frame_right_first, text="Update Matrix", command=update_matrix)
update_matrix_button.pack(side=LEFT)

normalizer_entry = Entry(frame_right_first, width=2)
normalizer_entry.pack(side=LEFT)

matrix_1_1 = Entry(frame_right_second, width=2)
matrix_1_1.pack(side=LEFT)

matrix_1_2 = Entry(frame_right_second, width=2)
matrix_1_2.pack(side=LEFT)

matrix_1_3 = Entry(frame_right_second, width=2)
matrix_1_3.pack(side=LEFT)

matrix_2_1 = Entry(frame_right_third, width=2)
matrix_2_1.pack(side=LEFT)

matrix_2_2 = Entry(frame_right_third, width=2)
matrix_2_2.pack(side=LEFT)

matrix_2_3 = Entry(frame_right_third, width=2)
matrix_2_3.pack(side=LEFT)

matrix_3_1 = Entry(frame_right_fourth, width=2)
matrix_3_1.pack(side=LEFT)

matrix_3_2 = Entry(frame_right_fourth, width=2)
matrix_3_2.pack(side=LEFT)

matrix_3_3 = Entry(frame_right_fourth, width=2)
matrix_3_3.pack(side=LEFT)

error_message = Label(frame_right_fifth, relief=RIDGE, wraplength=150)
error_message.pack(side=LEFT)

# =============================================Run GUI=============================================#
root.mainloop()  # main loop for Tkint
root.destroy()  # clears the window, fully ending task

if os.path.isfile("tempThumbnail.gif"):  # clean up working directory of temp files
    os.remove("tempThumbnail.gif")
if os.path.isfile("processedImageThumbnail.gif"):
    os.remove("processedImageThumbnail.gif")
