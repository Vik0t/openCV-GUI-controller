import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)
blank_image = np.zeros(shape=[400, 400, 3], dtype=np.uint8)
center = (199, 199)
cv.namedWindow('GUI')


def on_next(*args):
    print(args[1])


def on_previous(*args):
    print(args[1])


def on_check(*args):
    print('checkbox', args[1])


cv.createButton('<-', on_previous, 'go back')
cv.createButton('->', on_next, 'go next')

cv.createButton('checkbox1', on_check, 1)
cv.createButton('checkbox2', on_check, 2)


def on_mouse_event(event, x, y, flags, param):
    # left button is pressed +
    # mouse moves
    if flags == cv.EVENT_FLAG_LBUTTON:
        cv.rectangle(blank_image, (x - 500, y - 500), (x + 500, y + 500), (0, 0, 0), -1)
        cv.circle(blank_image, (x, y), 12, (0, 0, 255), -1)
        global angle, A, B, C
        b = np.radians(np.array([199, 199]))
        a = np.radians(np.array([199, 0]))
        c = np.radians(np.array([x, y]))

        avec = a - b
        cvec = c - b

        lat = b[0]
        avec[1] *= np.cos(lat)
        cvec[1] *= np.cos(lat)

        deg = np.degrees(np.arccos(np.dot(avec, cvec) / (np.linalg.norm(avec) * np.linalg.norm(cvec))))
        if x <= 199:
            deg = 360 - deg
        print(deg)


cv.setMouseCallback('GUI', on_mouse_event)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    cv.imshow('image', frame)
    cv.imshow('GUI', blank_image)
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
