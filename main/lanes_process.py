"""
Lanes process
1. detects lanes
2. return steer values as errors

TODO::you can use radius of curvature to calculate the steer value.
"""
import cv2
import numpy as np

class Lane:
    def __init__(self):
        self.left_lane_xa = False
        self.right_lane_xa = False
        

    def edge_detection(self,img, thresh_min = 20, thresh_max = 100,s_thresh_min = 170, s_thresh_max = 255 ):
        """
        finds the reqired edges for lane 

        Parameters
        ----------
        ticker : str
            The ticker symbol of the equity.
        thresh_min : int, optional 
            min x gradient threshold. By default "20".
        thresh_max : int, optional
            max x gradient threshold. By default "100".
        s_thresh_min : int, optional
            min saturation threshold. By default "170".
        s_thresh_max : int, optional
            max saturation threshold. By default "255"
        img : image

        Returns
        -------
        combined_binary: 
            contain index where manginute of s_channel and x_sobel is 1  
            
        """
         # Convert to Grayscale image
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        # Sobel x
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0) # Take the derivative in x
        abs_sobelx = np.absolute(sobelx) # Absolute x derivative to accentuate lines away from horizontal
        scaled_sobel = np.uint8(255*abs_sobelx/np.max(abs_sobelx))

        # Threshold x gradient
        sxbinary = np.zeros_like(scaled_sobel)
        sxbinary[(scaled_sobel >= thresh_min) & (scaled_sobel <= thresh_max)] = 1


        # Convert to HLS channel
        hls = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
        s_channel = hls[:,:,2] #only saturation channel

       
        # Threshold color channel
        s_binary = np.zeros_like(s_channel)
        s_binary[(s_channel >= s_thresh_min) & (s_channel <= s_thresh_max)] = 1


    # Combine the two binary thresholds
        combined_binary = np.zeros_like(sxbinary)
        combined_binary[(s_binary == 1) | (sxbinary == 1)] = 255

        return combined_binary
    
        
    def find_lane_pixels(self, binary_warped, nwindows = 5, margin=10, minpix=20):
        """
        Finds the pixels of lane using sliding window approach

        Parameters
        ----------
        binary_wrapped : image
            generally used image which has been transformed
        nwindows : int
            The number of sliding windows. Default = 6
        margin : int
            The width of the windows = +/- margin. Default = 30
        
        min_pix : int
            minimum number of pixels found to recenter window. Default = 20

        Returns
        ------- 
        leftx: x index of left lane
        lefty: y index of left lanel
        rightx:x index of right lane
        righty:y index of right lane      
        """
          # Take a histogram of the bottom half of the image
        histogram = np.sum(binary_warped[binary_warped.shape[0]//2:,:], axis=0)

        # Finds the peak of the left and right halves of the histogram
        # These will be the starting point for the left and right lines
        midpoint = int(histogram.shape[0]//2)
        leftx_base = np.argmax(histogram[:(midpoint)])
        rightx_base = np.argmax(histogram[(midpoint):]) + midpoint
        

        # Set height of windows - based on nwindows above and image shape
        window_height = binary_warped.shape[0]//nwindows
        # Identify the x and y positions of all nonzero pixels in the image
        nonzero = binary_warped.nonzero()
        nonzeroy = np.array(nonzero[0])
        nonzerox = np.array(nonzero[1])
        # Current positions to be updated later for each window in nwindows
        leftx_current = leftx_base
        rightx_current = rightx_base

        # Create empty lists to receive left and right lane pixel indices
        left_lane_inds = []
        right_lane_inds = []

        # Step through the windows one by one
        for window in range(nwindows):
            # Identify window boundaries in x and y (and right and left)
            win_y_low = binary_warped.shape[0] - (window+1)*window_height
            win_y_high = binary_warped.shape[0] - window*window_height
            win_xleft_low = leftx_current - margin
            win_xleft_high = leftx_current + margin
            win_xright_low = rightx_current - margin
            win_xright_high = rightx_current + margin
            
            # Identify the nonzero pixels in x and y within the window #
            good_left_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & 
                (nonzerox >= win_xleft_low) &  (nonzerox < win_xleft_high)).nonzero()[0]
            good_right_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & 
                (nonzerox >= win_xright_low) &  (nonzerox < win_xright_high)).nonzero()[0]
            
            # Append these indices to the lists
            left_lane_inds.append(good_left_inds)
            right_lane_inds.append(good_right_inds)
            
            # If you found > minpix pixels, recenter next window on their mean position
            if len(good_left_inds) > minpix:
                leftx_current = int(np.mean(nonzerox[good_left_inds]))
            if len(good_right_inds) > minpix:        
                rightx_current = int(np.mean(nonzerox[good_right_inds]))

        # Concatenate the arrays of indices (previously was a list of lists of pixels)
        try:
            left_lane_inds = np.concatenate(left_lane_inds)
            right_lane_inds = np.concatenate(right_lane_inds)
        except ValueError:
            # Avoids an error if the above is not implemented fully
            pass

        # Extract left and right line pixel positions
        leftx = nonzerox[left_lane_inds]
        lefty = nonzeroy[left_lane_inds] 
        rightx = nonzerox[right_lane_inds]
        righty = nonzeroy[right_lane_inds]
        
        if(self.left_lane_xa):
            left_lane_inds = ((nonzerox > (self.left_fit[0]*(nonzeroy**2) + self.left_fit[1]*nonzeroy + 
                        self.left_fit[2] - margin)) & (nonzerox < (self.left_fit[0]*(nonzeroy**2) + 
                        self.left_fit[1]*nonzeroy + self.left_fit[2] + margin)))
            leftx = nonzerox[left_lane_inds]
            lefty = nonzeroy[left_lane_inds] 

        if(self.right_lane_xa ):
            right_lane_inds = ((nonzerox > (self.right_fit[0]*(nonzeroy**2) + self.right_fit[1]*nonzeroy + 
                        self.right_fit[2] - margin)) & (nonzerox < (self.right_fit[0]*(nonzeroy**2) + 
                        self.right_fit[1]*nonzeroy + self.right_fit[2] + margin)))
    
            rightx = nonzerox[right_lane_inds]
            righty = nonzeroy[right_lane_inds] 

        return leftx, lefty, rightx, righty

        
    def get_error(self, transformed_image, left_turn=False, right_turn = False):
        """
        Fits the two degree polynomial from image using three steps
        1. Finds the index of lane using find_lane_pixels method from above
        2. Fit a second order polynomial 
        3. calculate error
        Parameters
        ----------
        transformed_image: image
            image which has been transformed

        Returns
        ------- 
        out_img, final_error
        out_img : image of stack of binary warped
        
        """
        error = []
        # Find our lane pixels first
        if(self.right_lane_xa &  self.left_lane_xa):
            leftx, lefty, rightx, righty = self.search_around_poly(transformed_image)
        else:
            leftx, lefty, rightx, righty = self.find_lane_pixels(transformed_image)
        
        ploty = np.linspace(0, transformed_image.shape[0]-1, transformed_image.shape[0] )
        
        if right_turn == False:
            #check whether the left lane is captured
            if len(leftx)>150:
                self.left_lane_xa = True
                # Fit a second order polynomial to each using `np.polyfit`
                self.left_fit = np.polyfit(lefty, leftx, 2)
                try:
                    left_fitx = self.left_fit[0]*ploty**2 + self.left_fit[1]*ploty + self.left_fit[2]
                except TypeError:
                    # Avoids an error if `left` and `right_fit` are still none or incorrect
                    print('The function failed to fit a left line!')
                    left_fitx = 1*ploty**2 + 1*ploty
                # append the error
                plotycurve = np.array(list(zip(left_fitx,ploty))).reshape((-1,1,2))
                transformed_image = cv2.polylines(transformed_image, pts=np.int32([plotycurve]),
                                isClosed=False, color=(250,250,250),
                                thickness=8)
                error.append( (left_fitx - np.ones(left_fitx.shape) * (left_fitx[len(left_fitx)-1]) ).mean() )
            else:
                self.left_lane_xa = False
        
        if left_turn == False:
        #check whether the right lane is captured
            if len(rightx)> 150:
                self.right_lane_xa = True
                self.right_fit = np.polyfit(righty, rightx, 2)
                try:
                    right_fitx = self.right_fit[0]*ploty**2 + self.right_fit[1]*ploty + self.right_fit[2]
                except TypeError:
                    # Avoids an error if `left` and `right_fit` are still none or incorrect
                    print('The function failed to fit a right line!')
                    right_fitx = 1*ploty**2 + 1*ploty
                #append right side error
                plotycurve = np.array(list(zip(right_fitx,ploty))).reshape((-1,1,2))
                transformed_image = cv2.polylines(transformed_image, pts=np.int32([plotycurve]),
                                isClosed=False, color=(250,250,250),
                                thickness=8)
                error.append( (right_fitx - np.ones(right_fitx.shape) * (right_fitx[len(right_fitx)-1]) ).mean() )
            else:
                self.right_lane_xa = False

        if(len(error) != 0):
            final_error = sum(error)/len(error)
        else:
            final_error = 0
        return final_error, transformed_image

    def search_around_poly(self, binary_warped):
        # HYPERPARAMETER
        # Choose the width of the margin around the previous polynomial to search
        margin = 10

        # Grab activated pixels
        nonzero = binary_warped.nonzero()
        nonzeroy = np.array(nonzero[0])
        nonzerox = np.array(nonzero[1])

        leftx = []
        lefty = []
        rightx = []
        righty = []
        
        ### Set the area of search based on activated x-values ###
        ### within the +/- margin of our polynomial function ###
        if(self.left_lane_xa):
            left_lane_inds = ((nonzerox > (self.left_fit[0]*(nonzeroy**2) + self.left_fit[1]*nonzeroy + 
                        self.left_fit[2] - margin)) & (nonzerox < (self.left_fit[0]*(nonzeroy**2) + 
                        self.left_fit[1]*nonzeroy + self.left_fit[2] + margin)))
            leftx = nonzerox[left_lane_inds]
            lefty = nonzeroy[left_lane_inds] 

        if(self.right_lane_xa ):
            right_lane_inds = ((nonzerox > (self.right_fit[0]*(nonzeroy**2) + self.right_fit[1]*nonzeroy + 
                        self.right_fit[2] - margin)) & (nonzerox < (self.right_fit[0]*(nonzeroy**2) + 
                        self.right_fit[1]*nonzeroy + self.right_fit[2] + margin)))
    
            rightx = nonzerox[right_lane_inds]
            righty = nonzeroy[right_lane_inds]        
        return leftx,lefty, rightx, righty



