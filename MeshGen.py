from random import randint

from PIL import Image
from gtk._gtk import image_new_from_animation


class MeshGen():

    def __init__(self):
        self.__minContrastColorInterval = 0.03
        self.__minContrastPixelInterval = 2
        self.__generatedContrastPointSize = 1


    def __showStatus(self, total, percent):
        per = percent * 20 / total
        out = "\r["
        for i in range(0, 20):
            out += "#" if i < per else ">" if i == per else " "
        out += "] %d of %d" % (percent, total)
        print out,


    def __rgbToGrey(self, pixel):
        return 0.299 * float(pixel[0]) + 0.587 * float(pixel[1]) + 0.114 * float(pixel[2])


    def __rgbToGreyPixel(self, pixel):
        p = int(self.__rgbToGrey(pixel))
        return (p, p, p)

    def __getPixel(self, img, x, y):
        return None if (x < 0 or y < 0 or x >= img.size[0] or y >= img.size[1]) else img.getpixel((x, y))


    def __getContrastPixel(self, img, x, y):
        pixels = img.load()
        maxIntensity = None
        minIntensity = None
        c = 0
        for x_ in range(x - self.__minContrastPixelInterval / 2, x + self.__minContrastPixelInterval / 2):
            for y_ in range(y - self.__minContrastPixelInterval / 2, y + self.__minContrastPixelInterval / 2):
                c += 1
                if self.__getPixel(img, x_, y_):
                    intensity = float(self.__rgbToGrey(pixels[x_, y_])) / 256.0
                    if not maxIntensity or not minIntensity:
                        maxIntensity = minIntensity = intensity
                    elif intensity > maxIntensity:
                        maxIntensity = intensity
                    elif intensity < minIntensity:
                        minIntensity = intensity

        intensity = maxIntensity - minIntensity
        if intensity >= self.__minContrastColorInterval:
            return intensity

        return None


    def __generateIntensityMatrix(self, imageIn):
        imageOut = Image.new("RGB", imageIn.size, "black")
        pixelsOut = imageOut.load()
        count = 0
        for x in range(imageOut.size[0]):  # for every pixel:
            for y in range(imageOut.size[1]):
                count += 1
                rand = randint(3, 50)
                if x % rand == 0 and y % rand == 0:
                    self.__showStatus(imageOut.size[0] * imageOut.size[1], count)
                    intensity = self.__getContrastPixel(imageIn, x, y)
                    if intensity:
                        pix = int(256 * intensity)
                        pixelsOut[x, y] = (0, 0, 0)
                    else:
                        pixelsOut[x, y] = (255, 255, 255)
                else:
                    pixelsOut[x, y] = (255, 255, 255)

        return imageOut


    def mesh(self, imageIn):
        imageOut = self.__generateIntensityMatrix(imageIn)
        imageOut.show()


imageIn = Image.open("in.png")
imageIn = imageIn.resize((int(imageIn.size[0] * 0.5), int(imageIn.size[1] * 0.5)))

mg = MeshGen()
mg.mesh(imageIn)
