import cv2
import numpy as np
import face_recognition
import imutils

# Загрузка видео
capture = cv2.VideoCapture('datas/detection_video/input/cam_3.MOV')

frame_id = 0  # Инициализация счетчика кадров

# Список с известными лицами
known_faces = []

skip_frames = 5  # Пропускать 4 кадров перед обработкой следующего

while True:
    frame_id += 1

    # Пропускаем кадры
    for _ in range(skip_frames):
        success, _ = capture.read()
        if not success:
            break

    # Получение кадра
    success, frame = capture.read()

    # Если есть кадр
    if success:
        # Уменьшение размера кадра
        frame = imutils.resize(frame, width=800)

        # Замена BGR на RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Нахождение лиц в текущем кадре
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        # Работа с лицами
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):

            # Увеличиваем размер ограничивающего прямоугольника
            top = max(0, top - 10)
            left = max(0, left - 10)
            bottom = min(frame.shape[0], bottom + 10)
            right = min(frame.shape[1], right + 10)

            # Ищем лицо в списке известных лиц
            matches = face_recognition.compare_faces(known_faces, face_encoding)

            if not any(matches):
                # Если лицо не найдено в списке известных лиц, добавляем его
                known_faces.append(face_encoding)

                # Рисует белый квадрат на картинке по координатам
                cv2.rectangle(
                    frame,
                    (left, top),
                    (right, bottom),
                    (255, 255, 255),
                    1
                )

                # Путь к директории с качественными изображениями
                face_path = 'datas/detection_video/output/faces/{}_{}.jpg'.format(frame_id, len(known_faces))

                # Сохранение изображения лица на диск в директории selected
                cv2.imwrite(face_path, frame[top:bottom, left:right])

                # Информируем консоль
                print('\033[92m' + face_path + '\033[0m')

        # Сохраняем кадр с видео
        cv2.imwrite('datas/detection_video/output/frames/' + str(frame_id) + '.jpg', frame)

    else:
        break
