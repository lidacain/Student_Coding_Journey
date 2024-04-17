import cv2
import numpy as np


def get_frame(cap, scaling_factor):
    _, frame = cap.read()

    frame = cv2.resize(frame, None, fx=scaling_factor,
                       fy=scaling_factor, interpolation=cv2.INTER_AREA)

    return frame


if __name__ == '__main__':
    cap = cv2.VideoCapture(0)

    # Определение объекта для вычитания фона
    bg_subtractor = cv2.createBackgroundSubtractorMOG2()

    # Определение количества кадров для обучения
    history = 100

    # Определение скорости обучения
    learning_rate = 1.0 / history

    while True:
        frame = get_frame(cap, 0.5)

        # Применение алгоритма вычитания фона
        mask = bg_subtractor.apply(frame, learningRate=learning_rate)

        # Преобразование маски в изображение BGR
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

        cv2.imshow('Input', frame)
        cv2.imshow('Output', mask & frame)

        c = cv2.waitKey(10)
        if c == 27:
            break

    cap.release()

    cv2.destroyAllWindows()