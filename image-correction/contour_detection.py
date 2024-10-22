from PIL import Image, ImageDraw
from pylab import *

class Img:
    def __init__(self, path_to_image):
        self.image = Image.open(path_to_image).convert('RGB')
        self.draw = ImageDraw.Draw(self.image)
        self.width = self.image.size[0]
        self.height = self.image.size[1]
        self.pix = self.image.load()


def vector_circuit (im):
    figure()
    contour(im, origin='image')
    axis('equal')
    plt.title('Detected circuit')
    show()

def monochrome(img, factor):
    for i in range(img.width):
        for j in range(img.height):
            a = img.pix[i, j][0]
            b = img.pix[i, j][1]
            c = img.pix[i, j][2]
            s = a + b + c
            if s > (((255 + factor) // 2) * 3):
                a, b, c = 255, 255, 255
            else:
                a, b, c = 0, 0, 0

            img.draw.point((i, j), (a, b, c))

    return img

if __name__ == '__main__':

    while 1:
        path_to_file = input('Enter the path to the input image (default: "input.jpg"): ')
        if path_to_file == '':
            path_to_file = 'input.jpg'

        img = Img(path_to_file)

        choice = int(input('Do you want to apply monochrome transformation before processing: \
                            \n 0 - no \
                            \n 1 - yes '))
        if choice:
            factor = int(input('Enter factor for monochrome transformation: '))

            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
            ax1.imshow(img.image)
            ax1.set_title('Original image')

            img = monochrome(img, factor)

            ax2.imshow(img.image)
            ax2.set_title('Monochrome image')
            plt.show()

        else:
            fig, ax = plt.subplots()
            ax.imshow(img.image)
            ax.set_title('Original image')
            plt.show()

        vector_circuit(array(img.image.convert('L')))

        print('\n----- operation finished -----\n')
