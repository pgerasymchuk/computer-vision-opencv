import random
import sys
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt

class Img:
    def __init__(self, path_to_image):
        self.image = Image.open(path_to_image).convert('RGB')
        self.draw = ImageDraw.Draw(self.image)
        self.width = self.image.size[0]
        self.height = self.image.size[1]
        self.pix = self.image.load()

class ImageProcessor:
    def _ensure_pixels_range(self, pixels):
        for i in range(len(pixels)):
            if pixels[i] < 0:
                pixels[i] = 0
            if pixels[i] > 255:
                pixels[i] = 255
        return pixels

    def _create_diagonal_gradient_mask(self, width, height, direction):
        # direction: '13', '31', '24' or '42'
        # 1  2
        # 4  3

        mask = Image.new('L', (width, height))

        for y in range(height):
            for x in range(width):

                match direction:
                    case '13':
                        gradient_value = int(255 * ((x + y) / (width + height)))

                    case '31':
                        gradient_value = int(255 * (((width - x) + (height - y)) / (width + height)))

                    case '24':
                        gradient_value = int(255 * (((width - x) + y) / (width + height)))

                    case '42':
                        gradient_value = int(255 * ((x + (height - y)) / (width + height)))

                    case _:
                        print("'direction' parameter can take values '13', '31', '24' or '42' only!")
                        return

                mask.putpixel((x, y), gradient_value)
        return mask

    def _create_center_gradient_mask(self, width, height, direction):
        # direction: 'out' or 'in'

        center_x, center_y = width // 2, height // 2
        max_distance = (center_x ** 2 + center_y ** 2) ** 0.5

        mask = Image.new('L', (width, height))

        for y in range(height):
            for x in range(width):

                distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5

                match direction:
                    case 'out':
                        gradient_value = int(255 * (distance / max_distance))

                    case 'in':
                        gradient_value = 255 - int(255 * (distance / max_distance))

                    case _:
                        print("'direction' parameter can take values 'out' or 'in' only!")
                        return

                mask.putpixel((x, y), gradient_value)
        return mask

    def change_brightness(self, img):
        factor = int(input('Enter the factor of the brightness change (recommended range -100, 100): '))

        for i in range(img.width):
            for j in range(img.height):

                a = img.pix[i, j][0] + factor
                b = img.pix[i, j][1] + factor
                c = img.pix[i, j][2] + factor

                a, b, c = self._ensure_pixels_range([a, b, c])
                img.draw.point((i, j), (a, b, c))
        return img

    def shades_of_gray(self, img):
        for i in range(img.width):
            for j in range(img.height):

                a = img.pix[i, j][0]
                b = img.pix[i, j][1]
                c = img.pix[i, j][2]
                S = (a + b + c) // 3

                img.draw.point((i, j), (S, S, S))
        return img

    def negative(self, img):
        for i in range(img.width):
            for j in range(img.height):

                a = img.pix[i, j][0]
                b = img.pix[i, j][1]
                c = img.pix[i, j][2]

                img.draw.point((i, j), (255 - a, 255 - b, 255 - c))
        return img

    def sepia(self, img):
        sepia_type = input("Enter type of sepia: \n\tUniform:  '0' \
          \n\tDiagonal: '13' - top-left to bottom-right \n\t \
                    '31' - bottom-right to top-left \n\t \
                    '24' - top-right to bottom-left \n\t \
                    '42' - bottom-left to top-right \
          \n\tCenter:   'out' - from the center \n\t \
                    'in'  - to the center ")

        depth = int(input('Enter sepia coefficient: '))
        img_copy = img.image.copy()

        for i in range(img.width):
            for j in range(img.height):

                a = img.pix[i, j][0]
                b = img.pix[i, j][1]
                c = img.pix[i, j][2]
                S = (a + b + c) // 3
                a = S + depth * 2
                b = S + depth
                c = S

                a, b, c = self._ensure_pixels_range([a, b, c])
                img.draw.point((i, j), (a, b, c))

        match sepia_type:
            case '0':
                return img

            case '13' | '31' | '24' | '42':
                img.image = Image.composite(img.image, img_copy, self._create_diagonal_gradient_mask(img.width, img.height, sepia_type))
                return img

            case 'out' | 'in':
                img.image = Image.composite(img.image, img_copy, self._create_center_gradient_mask(img.width, img.height, sepia_type))
                return img

            case _:
                print("'sepia_type' parameter can take values '0', '13', '31', '24', '42', 'out' or 'in' only!")

    def noise(self, img):
        factor = int(input('Enter noise coefficient: '))
        for i in range(img.width):
            for j in range(img.height):
                rand = random.randint(-factor, factor)
                a = img.pix[i, j][0] + rand
                b = img.pix[i, j][1] + rand
                c = img.pix[i, j][2] + rand

                a, b, c = self._ensure_pixels_range([a, b, c])
                img.draw.point((i, j), (a, b, c))
        return img

    def monochrome(self, img):
        factor = int(input('Enter coefficient for monochrome transformation: '))

        for i in range(img.width):
            for j in range(img.height):
                a = img.pix[i, j][0]
                b = img.pix[i, j][1]
                c = img.pix[i, j][2]
                S = a + b + c
                if S > (((255 + factor) // 2) * 3):
                    a, b, c = 255, 255, 255
                else:
                    a, b, c = 0, 0, 0

                img.draw.point((i, j), (a, b, c))
        return img


if __name__ == "__main__":

    while 1:
        file_start = sys.argv[1] if len(sys.argv) > 1 else 'image.jpg'
        image = Img(file_start)
        image_old = image.image.copy()
        img_proc = ImageProcessor()

        mode = int(input('Enter type of the operation: \
                           \n1 - change brightness \
                           \n2 - shades of gray \
                           \n3 - negative \
                           \n4 - sepia \
                           \n5 - noise \
                           \n6 - monochrome \n'))
        match mode:
            case 1:
                img_proc.change_brightness(image)
            case 2:
                img_proc.shades_of_gray(image)
            case 3:
                img_proc.negative(image)
            case 4:
                img_proc.sepia(image)
            case 5:
                img_proc.noise(image)
            case 6:
                img_proc.monochrome(image)
            case _:
                print('Incorrect input, try again')
                continue

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6, 3))

        ax1.imshow(image_old)
        ax1.set_title('Original image')
        ax1.tick_params(labelleft=False, labelbottom=False)

        ax2.set_title('Modified image')
        ax2.imshow(image.image)
        ax2.tick_params(labelleft=False, labelbottom=False)

        plt.show()
        print('\n----- Operation finished -----\n')
