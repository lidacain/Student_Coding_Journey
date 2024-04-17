import cv2
import numpy as np
import face_recognition
import imutils
from pathlib import Path
import os
import pandas as pd


df_cam1 = pd.DataFrame(columns=['face_id', 'encoding'])
df_cam2 = pd.DataFrame(columns=['face_id', 'encoding'])
df_cam3 = pd.DataFrame(columns=['face_id', 'encoding'])


def process_video(input_video, output_folder, known_faces, camera_name):
    # Загрузка видео
    capture = cv2.VideoCapture(str(input_video))

    frame_id = 0  # Инициализация счетчика кадров

    skip_frames = 0  # Пропускать кадров перед обработкой следующего

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
                    face_path = os.path.join(output_folder, f'faces/{camera_name}/{input_video.stem}_{frame_id}_{len(known_faces)}.jpg')

                    # Сохранение изображения лица на диск
                    cv2.imwrite(face_path, frame[top:bottom, left:right])

                    # Информируем консоль
                    print('\033[92m' + face_path + '\033[0m')

            # Сохраняем кадр с видео
            frame_path = os.path.join(output_folder, f'frames/{camera_name}/{input_video.stem}_{frame_id}.jpg')
            cv2.imwrite(frame_path, frame)

        else:
            break

if __name__ == "__main__":
    # Папка для сохранения выходных данных
    output_folder = 'datas/detection_video/output'
    os.makedirs(os.path.join(output_folder, 'faces', 'cam_1'), exist_ok=True)
    os.makedirs(os.path.join(output_folder, 'frames', 'cam_1'), exist_ok=True)

    # Список с известными лицами
    known_faces = []

    # Первая камера
    process_video(Path('datas/detection_video/input/cam_1.MOV'), output_folder, known_faces, 'cam_1')

    # Последующие камеры
    for input_video, camera_name in zip([Path('datas/detection_video/input/cam_2.MOV'), Path('datas/detection_video/input/cam_3.MOV')], ['cam_2', 'cam_3']):
        # Перезагрузка известных лиц для каждой новой камеры
        known_faces = []
        process_video(input_video, output_folder, known_faces, camera_name)
