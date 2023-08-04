import cv2
import numpy as np
import imutils

def detect(img, color_space="HSV"):

    if color_space == 'HSV':
        color_frame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        color_ranges = {
            "yellow": (np.array([15, 20, 180]), np.array([35, 255, 255])),
            "blue": (np.array([100, 70, 80]), np.array([130, 255, 255])),
            "green": (np.array([40, 30, 110]), np.array([80, 255, 255])),
            # Lower range for red
            "red1": (np.array([0, 120, 70]), np.array([10, 255, 255])),
            # Upper range for red
            "red2": (np.array([160, 120, 70]), np.array([180, 255, 255])),
        }
    elif color_space == 'Lab':
        color_frame = cv2.cvtColor(img, cv2.COLOR_BGR2Lab)
        color_ranges = {
            "yellow": (np.array([20, 110, 180]), np.array([100, 128, 255])),
            "blue": (np.array([20, 80, 110]), np.array([100, 127, 150])),
            "green": (np.array([20, 50, 80]), np.array([100, 128, 127])),
            "red": (np.array([20, 150, 150]), np.array([60, 255, 255])),
        }
    elif color_space == 'YCrCB':
        color_ranges = {
            "yellow": (np.array([60, 100, 100]), np.array([100, 255, 255])),
            "blue": (np.array([20, 50, 80]), np.array([100, 255, 255])),
            "green": (np.array([30, 100, 60]), np.array([90, 255, 255])),
            # Lower range for red
            "red1": (np.array([0, 100, 100]), np.array([10, 255, 255])),
            # Upper range for red
            "red2": (np.array([170, 100, 100]), np.array([180, 255, 255])),
        }
        color_frame = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
    else:
        raise ValueError("Invalid color space. Choose 'HSV' or 'Lab'.")

    kernel = np.ones((4,4), np.uint8)
    opening = cv2.morphologyEx(color_frame, cv2.MORPH_OPEN, kernel)
    color_frame = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

    if color_space == 'HSV' or color_space == 'YCrCB':
        red_mask1 = cv2.inRange(color_frame, *color_ranges["red1"])
        red_mask2 = cv2.inRange(color_frame, *color_ranges["red2"])
        red_mask = cv2.bitwise_or(red_mask1, red_mask2)
        color_masks = {color: cv2.inRange(color_frame, low, high) for color, (low, high) in color_ranges.items() if color not in ["red1", "red2"]}
        color_masks["red"] = red_mask  # Add the combined red mask
    else:
        color_masks = {color: cv2.inRange(color_frame, low, high) for color, (low, high) in color_ranges.items()}


    contours = {color: imutils.grab_contours(cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE))
                for color, mask in color_masks.items()}

    results = {}
    for color, cnts in contours.items():
        largest = 0
        second_largest = 0
        largest_rect = (0, 0, 0, 0)
        second_largest_rect = (0, 0, 0, 0)

        for contour in cnts:
            rect = cv2.boundingRect(contour)
            x, y, w, h = rect
            area = w * h
            if area > largest:
                largest, second_largest = area, largest
                largest_rect, second_largest_rect = rect, largest_rect
            elif area > second_largest:
                second_largest = area
                second_largest_rect = rect

        results[color] = (second_largest_rect, largest_rect)

    for color, ((x1, y1, w1, h1), (x2, y2, w2, h2)) in results.items():
        cv2.rectangle(img, (x1, y1), (x1 + w1, y1 + h1), (255, 0, 0), 2)
        cv2.rectangle(img, (x2, y2), (x2 + w2, y2 + h2), (255, 0, 0), 2)
        cv2.putText(img, f'{color}_cube_holder', (x2, y2 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
        cv2.putText(img, f'{color}_cube', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

    return results, img
