import numpy as np
import cv2 as cv

cap = cv.VideoCapture(0)
# Get current width of frame
width = cap.get(cv.CAP_PROP_FRAME_WIDTH)   # float
# Get current height of frame
height = cap.get(cv.CAP_PROP_FRAME_HEIGHT) # float
# Define the codec and create VideoWriter object
fourcc = cv.VideoWriter_fourcc(*'XVID')
outReg = cv.VideoWriter('regular.avi', fourcc, 30, (int(width),int(height)))

if not cap.isOpened():
    print("Cannot open camera")
    exit()
    
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    corners = cv.goodFeaturesToTrack(gray,25,0.01,10)
    corners = np.int0(corners)
   
    for i in corners:
        x,y = i.ravel()
        cv.circle(frame,(x,y),3,255,-1)
    
    # Display the resulting frame
    cv.imshow('frame', frame)
    outReg.write(frame)
    
    if cv.waitKey(1) == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
