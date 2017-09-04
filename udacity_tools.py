"""
Helper functions provided by Udacity or based on code from their 'Self Driving Car Term 1' Course, 
with some minor changes.
"""
import cv2
import numpy as np


def overlay_windows(img, centers, width, height, color=(0, 255, 0)):
    # TODO: Change format of centers to be (all_left, all_right). Generally clean up syntax.
    if len(centers) > 0:
        # Points used to draw all the left and right windows
        l_points = np.zeros((img.shape[0], img.shape[1]))
        r_points = np.zeros((img.shape[0], img.shape[1]))

        # Go through each level and draw the windows
        for level in range(0, len(centers)):
            # Window_mask is a function to draw window areas
            l_mask = single_window_mask(img, centers[level][0], width, height, level)
            r_mask = single_window_mask(img, centers[level][1], width, height, level)
            # Add graphic points from window mask here to total pixels found
            l_points[(l_points == 255) | ((l_mask == 1))] = 1
            r_points[(r_points == 255) | ((r_mask == 1))] = 1

        # Draw the results
        template = np.array(r_points + l_points, np.uint8)  # add both left and right window pixels together
        template = np.array(cv2.merge((template * color[0], template * color[1], template * color[2])),
                            np.uint8)  # make window pixels green
        if len(img.shape) == 2 or img.shape[2] == 1:
            img = np.array(cv2.merge((img, img, img)), np.uint8)  # making 3 color channels
        return cv2.addWeighted(img, 1, template, 0.5, 0.0)  # overlay the original image with window results


def single_window_mask(img_ref, center, width, height, level):
    """
    Creates a rectangular mask centered along x axis at `center` and y axis at `level`*`height` from the bottom of the
    image.
    """
    output = np.zeros((img_ref.shape[0], img_ref.shape[1]))
    output[int(img_ref.shape[0] - (level + 1) * height):int(img_ref.shape[0] - level * height),
    max(0, int(center - width / 2)):min(int(center + width / 2), img_ref.shape[1])] = 1
    return output
