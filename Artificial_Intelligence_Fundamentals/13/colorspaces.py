import cv2
import numpy as np


def get_frame(cap, scaling_factor):
    # Чткние текущего кадра
    _, frame = cap.read()

    # Изменение размера кадра
    frame = cv2.resize(frame, None, fx=scaling_factor,
            fy=scaling_factor, interpolation=cv2.INTER_AREA)

    return frame

if __name__=='__main__':
    cap = cv2.VideoCapture(0)

    scaling_factor = 0.5

    while True:
        frame = get_frame(cap, scaling_factor)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Определение HSV-пределов для цвета кожи
        lower = np.array([0, 70, 60])
        upper = np.array([50, 150, 255])

        # Построение маски
        mask = cv2.inRange(hsv, lower, upper)

        # Побитовое И для кадра и маски
        img_bitwise_and = cv2.bitwise_and(frame, frame, mask=mask)

        # Применение медианного размытия
        img_median_blurred = cv2.medianBlur(img_bitwise_and, 5)

        cv2.imshow('Input', frame)
        cv2.imshow('Output', img_median_blurred)

        c = cv2.waitKey(5)
        if c == 27:
            break

    cv2.destroyAllWindows()