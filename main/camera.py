"""
Camera process
1. undistort image using camera matrix 
"""

import cv2 as cv
import numpy as np

def undistort(img):
    """
    undistort the image 
    parameter
    -------
    mtx is camera matrix from camera calibration.ipynd
    dst is from camera calibration.ipynd
    """
    # mtx is my camera matrix
    # TODO:: find your camera matrix by running camera_calibration.ipynb 
    mtx = np.array([[1.00049876e+03, 0.00000000e+00, 3.07778943e+02],
       [0.00000000e+00, 1.00387552e+03, 2.98942853e+02],
       [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
    
    dist = np.array([-0.34791078, -0.12886468, -0.02174711, -0.00403055, -0.18004229])
    h,  w = img.shape[:2]
    newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
    dst = cv.undistort(img, mtx, dist, None, newcameramtx)
    # crop the image
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    return dst

def perspective_transform(image):
    """
    transform the image

    Parameters
    ----------
    image: one channel image
    src : nd_array
        eg:np.float32([           
                    [20, 48], [60, 100],
                    [125, 80], [40, 120]
                    ])

    dst : nd_array
        eg: np.float32([                
                [30, 60], [70, 250],
                [200, 90], [80,200]
                    ])

    Returns
    -------
    warped: warped image 
    """
        #TODO::  change values of src and dst as per your image
        # Note: It depend upon your camera position
    src = np.float32([
        [134,386],[253,326],
        [468,326],[610,386]
    ])

    dst = np.float32([      
        [192,410],[192,250],
        [538,250],[538,410]
    ])
    transform_matrix = cv.getPerspectiveTransform(src, dst)
    img_size = (image.shape[1], image.shape[0])
    warped = cv.warpPerspective(image, transform_matrix, img_size, flags=cv.INTER_LINEAR)

    return warped

