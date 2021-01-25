import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
# если раскомментить, то будет находить и глаза, но работает не 100%:
# не находит все глаза и/или находит лишнего
img = cv2.imread('w.jpg')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.3, 5)

i = 0
for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 123), 2)
    i = i + 1
    cv2.putText(img, ('Face_%03d' % i), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 123), 1, cv2.LINE_AA)
    roi_gray = gray[y:y + h, x:x + w]
    roi_color = img[y:y + h, x:x + w]
    # eyes = eye_cascade.detectMultiScale(roi_gray)
    # for (ex, ey, ew, eh) in eyes:
    #     cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (255, 255, 0), 2)

cv2.imshow('img', img)
cv2.waitKey(0)
cv2.imwrite('result.jpg', img)
# cv2.destroyAllWindows()


