import os
import cv2
from matplotlib import pyplot as plt

def to_rgb(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB) if len(img.shape) == 3 else img

def display_adjacent_images(img1, img2, title1, title2, cmap1=None, cmap2=None):
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(to_rgb(img1), cmap=cmap1)
    plt.title(title1)
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(to_rgb(img2), cmap=cmap2)
    plt.title(title2)
    plt.axis('off')

    plt.tight_layout()
    plt.show()

def read_image(path):
    img = cv2.imread(path)
    return img

def preprocess_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    edged = cv2.Canny(gray, 100, 200)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
    return closed

def find_contours(img):
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
    contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    img_with_contours = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR) if len(img.shape) != 3 else img.copy()
    total = 0

    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        area = w * h
        print(f"Contour Area: {area}")

        cv2.drawContours(img_with_contours, [c], -1, (0, 255, 0), 2)
        total += 1
    print(f"Found {total} contours.")
    return img_with_contours


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path1 = os.path.join(base_dir, "low_quality.jpg")
    path2 = os.path.join(base_dir, "high_quality.jpg")

    img1 = read_image(path1)
    img2 = read_image(path2)

    display_adjacent_images(img1, img2, "Low quality", "High quality")

    img1 = preprocess_image(img1)
    img2 = preprocess_image(img2)

    display_adjacent_images(img1, img2, "Low quality", "High quality")

    img1 = find_contours(img1)
    img2 = find_contours(img2)

    display_adjacent_images(img1, img2, "Low quality", "High quality")
