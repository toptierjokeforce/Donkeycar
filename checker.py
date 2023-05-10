import cv2

cam = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier("cascade_face.xml")

while True:
    key = cv2.waitKey(1) & 0xFF
    img = cam.read()  # Capture frame by frame
    src = img
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.05,
        minNeighbors=8,
        minSize=(55, 55),
        flags=cv2.CASCADE_SCALE_IMAGE)

    for (x, y, w, h) in faces:
        print('Found'+str(len(faces)) + "Faces!")
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y + h, x:x + w]
    cv2.imshow("Face Detection", img)
    if key == 32:
        break
cam.release()
cv2.destroyAllWindows()


