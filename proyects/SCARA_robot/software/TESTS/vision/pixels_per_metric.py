"""
This script processes video input or a saved image to detect objects, measure their dimensions, 
and display the results using OpenCV.
"""

# Import necessary packages
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import imutils
import cv2

# USERS' SETTINGS
camara = 0  # Camera index (change if multiple cameras are connected)


# -------------------------------
# Utility Functions
# -------------------------------

def midpoint(ptA, ptB):
    """
    Calculate the midpoint between two points.
    :param ptA: First point (x, y)
    :param ptB: Second point (x, y)
    :return: Midpoint (x, y)
    """
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

# -------------------------------
# Object Measurement Functions
# -------------------------------

def measure_obj(cnts, image):
    """
    Measure the dimensions of objects in the image based on contours.
    :param cnts: List of contours
    :param image: Original image
    :return: Processed image and bounding box
    """
    for c in cnts:
        # Ignore small contours
        if cv2.contourArea(c) < 100:
            continue

        # Compute the rotated bounding box of the contour
        orig = image.copy()
        box = cv2.minAreaRect(c)
        box = cv2.boxPoints(box) if not imutils.is_cv2() else cv2.cv.BoxPoints(box)
        box = np.array(box, dtype="int")

        # Order the points and draw the bounding box
        box = perspective.order_points(box)
        cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)

        # Draw the corner points
        for (x, y) in box:
            cv2.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)

        return orig, box

def draw_objs(orig, box, pixelsPerMetric=None):
    """
    Draw the bounding box, midpoints, and dimensions of the object.
    :param orig: Original image
    :param box: Bounding box points
    :param pixelsPerMetric: Calibration factor (pixels per metric unit)
    :return: Processed image
    """
    # Unpack the bounding box points
    (tl, tr, br, bl) = box

    # Compute midpoints
    (tltrX, tltrY) = midpoint(tl, tr)
    (blbrX, blbrY) = midpoint(bl, br)
    (tlblX, tlblY) = midpoint(tl, bl)
    (trbrX, trbrY) = midpoint(tr, br)

    # Draw midpoints
    for (x, y) in [(tltrX, tltrY), (blbrX, blbrY), (tlblX, tlblY), (trbrX, trbrY)]:
        cv2.circle(orig, (int(x), int(y)), 5, (255, 0, 0), -1)

    # Draw lines between midpoints
    cv2.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)), (255, 0, 255), 2)
    cv2.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)), (255, 0, 255), 2)

    # Compute distances
    dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
    dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

    # Calibrate pixels per metric if not provided
    if pixelsPerMetric is None:
        pixelsPerMetric = dB / 10  # Example: 10 units as reference

    # Compute object dimensions
    dimA = dA / pixelsPerMetric
    dimB = dB / pixelsPerMetric

    # Draw dimensions on the image
    cv2.putText(orig, "{:.1f}in".format(dimA), (int(tltrX - 15), int(tltrY - 10)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)
    cv2.putText(orig, "{:.1f}in".format(dimB), (int(trbrX + 10), int(trbrY)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)

    return orig

# -------------------------------
# Main Function
# -------------------------------

def process_frame(frame):
    """
    Process a single frame to detect and measure objects.
    :param frame: Input frame
    :return: Processed frame
    """
    # Convertir a YCrCb y separar canales
    ycrcb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
    y, cr, cb = cv2.split(ycrcb)
    y_channel = cv2.merge([y, y, y])
    cr_channel = cv2.merge([cr, cr, cr])
    cb_channel = cv2.merge([cb, cb, cb])

    # Preprocess the frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)

    # Edge detection and contour finding
    edged = cv2.Canny(gray, 50, 100)
    edged = cv2.dilate(edged, None, iterations=1)
    edged = cv2.erode(edged, None, iterations=1)
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts, _ = contours.sort_contours(cnts)

    # Process contours
    try:
        orig, box = measure_obj(cnts, frame)
        orig = draw_objs(orig, box)
    except TypeError:
        # Skip if no valid contour is found
        orig = frame

    return orig, gray, edged

def main():
    """
    Main function to capture video or process an image and display results.
    """
    mode = input("Enter 'camera' to use the camera or 'image' to process a saved image: ").strip().lower()

    if mode == "camera":
        # Initialize video capture
        cap = cv2.VideoCapture(camara)
        if not cap.isOpened():
            print("Error: Unable to open the camera.")
            return

        while True:
            # Capture frame
            ret, frame = cap.read()
            if not ret:
                print("Error: Unable to capture frame.")
                break

            # Process the frame
            orig, gray, edged = process_frame(frame)

            # Display results
            cv2.imshow("Detected Object", orig)
            cv2.imshow("Grayscale", gray)
            cv2.imshow("Edges", edged)

            # Exit on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release resources
        cap.release()
        cv2.destroyAllWindows()

    elif mode == "image":
        image_path = input("Enter the path to the image: ").strip()
        frame = cv2.imread(image_path)
        if frame is None:
            print("Error: Unable to load the image.")
            return

        # Process the image
        orig, gray, edged = process_frame(frame)

        # Display results
        cv2.imshow("Detected Object", orig)
        cv2.imshow("Grayscale", gray)
        cv2.imshow("Edges", edged)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    else:
        print("Invalid mode. Please enter 'camera' or 'image'.")

# -------------------------------
# Entry Point
# -------------------------------

if __name__ == "__main__":
    main()