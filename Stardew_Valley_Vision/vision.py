import cv2 as cv
import numpy as np

class computerVision:
    def __init__(self, cropped_images_to_detect):
        # Define parameters:
        self.templates = []
        self.template_sizes = []
        # Get and save the required parameters (template and sizes) for all cropped images in the given list:
        for img in cropped_images_to_detect:
            # Template:
            cropped_img = cv.imread(img, cv.IMREAD_UNCHANGED)
            self.templates.append(cropped_img)
            # Sizes:
            cropped_w = cropped_img.shape[1]
            cropped_h = cropped_img.shape[0]
            self.template_sizes.append((cropped_w, cropped_h))
    # Detect cropped images on the main image:
    def detect_cropped_image(self, main_img, threshold, method=cv.TM_CCOEFF_NORMED):
        self.main_img = main_img
        # Generate results for each template:
        self.rectangles = []
        for i in range(len(self.templates)):
            # Get detected cropped image locations on the main image:
            result = cv.matchTemplate(self.main_img, self.templates[i], method)
            locations = np.where(result >= threshold)
            # Zip the detected cropped image locations into (X, Y) position tuples:
            locations = list(zip(*locations[::-1]))
            # Create the rectangles list [x, y, w, h] to avert overlapping positions:
            for loc in locations:
                w, h = self.template_sizes[i]
                rect = [int(loc[0]), int(loc[1]), int(w), int(h)]
                self.rectangles.append(rect)
                # For single points:
                self.rectangles.append(rect)
        # Group the rectangles list:
        self.rectangles, weights = cv.groupRectangles(self.rectangles, 1, 0.7)
    # Draw rectangles or markers on the detected croppped images:
    def get_and_draw_points(self, result_type, rect_color=(255,0,255), rect_type=cv.LINE_4, rect_thickness=3, marker_color=(255,0,255), marker_type=cv.MARKER_STAR, marker_size=25, marker_thickness=3):
        self.detected_center_points = []
        if(len(self.rectangles)):
            # Loop all detected image locations in the rectangles list:
            for (x, y, w, h) in self.rectangles:
                # Define the rectangle box points:
                top_left = (x, y)
                bottom_right = (x + w, y + h)
                # Define the rectangle center points for drawing markers:
                center_x = x + int(w/2)
                center_y = y + int(h/2)
                # Save the center points:
                self.detected_center_points.append((center_x, center_y))
                # Draw results on the main image:
                if(result_type == 'boxes'):
                    # Draw rectangles around the detected cropped images:
                    cv.rectangle(self.main_img, top_left, bottom_right, color=rect_color, thickness=rect_thickness, lineType=rect_type)
                elif(result_type == 'markers'):
                    # Draw markers on the detected cropped images:
                    cv.drawMarker(self.main_img, (center_x, center_y), marker_color, marker_type, marker_size, marker_thickness)
        return self.main_img
        # Clear the rectangles list to avoid errors:
        self.rectangles = []
    # Get the center points of the detected cropped images:
    def get_center_points(self):
        return self.detected_center_points