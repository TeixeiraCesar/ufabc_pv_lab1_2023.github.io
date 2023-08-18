import cv2
import numpy as np

# Load the video
video_path = "VideoPV.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Could not open the video.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Resize the frame to a smaller size (you can adjust the dimensions)
    resized_frame = cv2.resize(frame, (800, 600))

    # Convert the resized frame to HSV
    hsv_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2HSV)

    # Define the HSV range for blue color
    lower_blue = np.array([100, 60, 60])
    upper_blue = np.array([130, 255, 255])

    # Create a mask to segment blue objects
    mask_blue = cv2.inRange(hsv_frame, lower_blue, upper_blue)

    # Apply morphological opening to remove noise
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask_open = cv2.morphologyEx(mask_blue, cv2.MORPH_OPEN, kernel)

    # Find contours of blue objects in the segmented image
    contours, _ = cv2.findContours(mask_open, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw bounding boxes around blue objects
    #for contour in contours:
    #    area = cv2.contourArea(contour)
    #    if area > 100:  # Adjust the area threshold as needed
    #        x, y, w, h = cv2.boundingRect(contour)
    #        cv2.rectangle(resized_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Draw green bounding box

    # Create a bounding box that engulfs all blue objects
    blue_objects_roi = None
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 100:  # Adjust the area threshold as needed
            x, y, w, h = cv2.boundingRect(contour)
            if blue_objects_roi is None:
                blue_objects_roi = (x, y, x + w, y + h + 20)  # Extend the ROI downward by 20 pixels
            else:
                x_min, y_min, x_max, y_max = blue_objects_roi
                x_min = min(x_min, x)
                y_min = min(y_min, y)
                x_max = max(x_max, x + w)
                y_max = max(y_max, y + h + 20)  # Extend the ROI downward by 20 pixels
                blue_objects_roi = (x_min, y_min, x_max, y_max)

    # Create a sub-ROI within the main ROI, starting from the bottom
    if blue_objects_roi is not None:
        x_min, y_min, x_max, y_max = blue_objects_roi
        sub_roi_height = (y_max - y_min) // 8  # 2/10 of the main ROI height
        sub_roi = resized_frame[y_max - sub_roi_height: y_max, x_min: x_max]

        # Convert the sub-ROI to HSV
        hsv_sub_roi = cv2.cvtColor(sub_roi, cv2.COLOR_BGR2HSV)

        # Define the HSV range for blue color in sub-ROI
        lower_blue_sub_roi = np.array([100, 60, 60])
        upper_blue_sub_roi = np.array([130, 255, 255])

        # Create mask to segment blue objects in sub-ROI
        mask_blue_sub_roi = cv2.inRange(hsv_sub_roi, lower_blue_sub_roi, upper_blue_sub_roi)

        # Apply morphological opening to remove noise in sub-ROI mask
        kernel_sub_roi = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        mask_open_sub_roi = cv2.morphologyEx(mask_blue_sub_roi, cv2.MORPH_OPEN, kernel_sub_roi)

        # Find contours of blue objects in sub-ROI
        contours_sub_roi, _ = cv2.findContours(mask_open_sub_roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw contours of blue objects in sub-ROI
        for contour in contours_sub_roi:
            if cv2.contourArea(contour) > 100:
                cv2.drawContours(sub_roi, [contour], -1, (0, 0, 255), 2)  # Draw the contour in red

        # Write the result based on the number of blue objects detected in sub-ROI
        if len(contours_sub_roi) == 5:
            result_text = "Passou"
            result_color = (0, 255, 10)  # Green
        else:
            result_text = "Reprovado"
            result_color = (0, 0, 255)  # Red

        # Draw the main ROI contour
        cv2.drawContours(resized_frame, [np.array([(x_min, y_max - sub_roi_height), (x_max, y_max - sub_roi_height),
                                                   (x_max, y_max), (x_min, y_max)])], -1, (255, 0, 0), 2)

        # Write the number of blue objects in the sub-ROI on the image (with blue font)
        cv2.putText(resized_frame, f"Conectores Corretos Presentes: {len(contours_sub_roi)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        # Write the result text on the image
        cv2.putText(resized_frame, result_text, (300, 550), cv2.FONT_HERSHEY_SIMPLEX, 3, result_color, 5)

    # Display the frame with drawn contours and ROIs
    cv2.imshow('Objects Contours', resized_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()