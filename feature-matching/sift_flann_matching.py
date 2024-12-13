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
    gray = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    edged = cv2.Canny(gray, 100, 200)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
    return closed

def find_contours(img, original_img):
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
    contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    img_with_contours = original_img.copy()
    cv2.drawContours(img_with_contours, contours, -1, (0, 255, 0), 2)
    total = 0

    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        area = w * h
        print(f"Contour Area: {area}")
        total += 1

    print(f"Found {total} contours.")
    return img_with_contours

def sift_feature_matching(img1, img2, original_img1, original_img2):
    sift = cv2.SIFT_create()

    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

    matchesMask = [[0, 0] for i in range(len(matches))]

    valid_matches = 0
    for i, pair in enumerate(matches):
        if len(pair) == 2 and pair[0].distance < 0.8 * pair[1].distance:
            matchesMask[i] = [1, 0]
            valid_matches += 1

    draw_params = dict(matchColor=(0, 255, 0),
                       singlePointColor=(255, 0, 0),
                       matchesMask=matchesMask,
                       flags=cv2.DrawMatchesFlags_DEFAULT)

    img3 = cv2.drawMatchesKnn(original_img1, kp1, original_img2, kp2, matches, None, **draw_params)

    cv2.imshow('sift_feature_matching', img3)
    if cv2.waitKey(0) & 0xff == 27:
        cv2.destroyAllWindows()
    print("Number of valid matches:", valid_matches)
    print("Probability of identification:", valid_matches / len(matches))

if __name__ == "__main__":
    images_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "satellite-segmentation")
    path1 = os.path.join(images_dir, "low_quality.jpg")
    path2 = os.path.join(images_dir, "high_quality.jpg")

    img1 = read_image(path1)
    img2 = read_image(path2)

    display_adjacent_images(img1, img2, "Low quality", "High quality")

    preprocessed_img1 = preprocess_image(img1)
    preprocessed_img2 = preprocess_image(img2)

    img1 = find_contours(preprocessed_img1, img1)
    img2 = find_contours(preprocessed_img2, img2)

    display_adjacent_images(img1, img2, "Low quality", "High quality")

    sift_feature_matching(preprocessed_img1, preprocessed_img2, img1, img2)
