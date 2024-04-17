import cv2


# Compute the frame differences
def frame_diff(prev_frame, cur_frame, next_frame):
    # Разность между текущим кадром и следующим кадром
    diff_frames_1 = cv2.absdiff(next_frame, cur_frame)

    # Разность между текущим кадром и предыдущим кадром
    diff_frames_2 = cv2.absdiff(cur_frame, prev_frame)

    # Вернуть разность между двумя разностями
    return cv2.bitwise_and(diff_frames_1, diff_frames_2)


def get_frame(cap, scaling_factor):
    # Чтение текущего кадра
    _, frame = cap.read()

    # Изменение размера кадра
    frame = cv2.resize(frame, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)

    # Преобразование в оттенки серого
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    return gray


if __name__ == '__main__':
    # Запуск веб-камеры
    cap = cv2.VideoCapture(0)

    # Определение коэффициента масштабирования для кадров
    scaling_factor = 0.5

    # Чтение первого кадра
    prev_frame = get_frame(cap, scaling_factor)

    # Чтение второго кадра
    cur_frame = get_frame(cap, scaling_factor)

    # Чтение третьего кадра
    next_frame = get_frame(cap, scaling_factor)

    while True:
        # Отображение разности между кадрами
        cv2.imshow('Object Movement', frame_diff(prev_frame, cur_frame, next_frame))

        # Обновление переменных
        prev_frame = cur_frame
        cur_frame = next_frame

        # Чтение следующего кадра
        next_frame = get_frame(cap, scaling_factor)

        key = cv2.waitKey(10)
        if key == 27:
            break

    cv2.destroyAllWindows()