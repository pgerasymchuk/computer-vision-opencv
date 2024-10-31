import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt

def get_contours_blur(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, threshold1=100, threshold2=200)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def get_contours_equalize_hist(frame, to_plot):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    hist, bins = np.histogram(frame.flatten(), 256, (0, 256))
    cdf = hist.cumsum()
    cdf_normalized = cdf * hist.max() / cdf.max()

    if to_plot:
        plt.plot(cdf_normalized, color='b')
        plt.hist(frame.flatten(), 256, range=(0, 256), color='r')
        plt.xlim([0, 256])
        plt.legend(('cdf', 'histogram'), loc='upper left')
        plt.show()

    cdf_m = np.ma.masked_equal(cdf, 0)
    cdf_m = (cdf_m - cdf_m.min()) *255 / (cdf_m.max() - cdf_m.min())
    cdf = np.ma.filled(cdf_m,0).astype('uint8')
    frame = cdf[frame]

    blurred = cv2.GaussianBlur(frame, (5, 5), 0)
    edges = cv2.Canny(blurred, threshold1=100, threshold2=200)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def get_contours_monochrome(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, monochrome = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
    blurred = cv2.GaussianBlur(monochrome, (5, 5), 0)
    edges = cv2.Canny(blurred, threshold1=100, threshold2=200)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def draw_frame_with_contours(frame, contours, window_name):
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        area = cv2.contourArea(c)

        if 5 < w < 100 and 5 < h < 100 and 30 < area < 150:
            cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)

    cv2.imshow(window_name, frame)



if __name__ == '__main__':

    cap = cv2.VideoCapture(sys.argv[1] if len(sys.argv) > 1 else 'video.mp4')

    to_plot_histogram = True
    while cap.isOpened():

        ret, fr = cap.read()
        if not ret:
            break

        height, width = fr.shape[:2]
        fr = cv2.resize(fr, (width // 3, height // 3))
        cv2.imshow('Original', fr)

        contours_blur = get_contours_blur(fr.copy())
        draw_frame_with_contours(fr.copy(), contours_blur, 'Blur')

        contours_equalize_hist = get_contours_equalize_hist(fr.copy(), to_plot_histogram)
        draw_frame_with_contours(fr.copy(), contours_equalize_hist, 'Brightness Histogram Correction')
        to_plot_histogram = False

        contours_monochrome = get_contours_monochrome(fr.copy())
        draw_frame_with_contours(fr.copy(), contours_monochrome, 'Monochrome')

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
