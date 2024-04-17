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


def process_video(input_video, output_folder, known_faces_df, camera_name):
    # Загрузка видео
    capture = cv2.VideoCapture(str(input_video))

    frame_id = 0  # Инициализация счетчика кадров

    skip_frames = 0  # Пропускать 5 кадров перед обработкой следующего

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
                matches = known_faces_df['encoding'].apply(lambda x: face_recognition.compare_faces([x], face_encoding)[0])

                if not any(matches):
                    # Если лицо не найдено в списке известных лиц, добавляем его в датафрейм
                    known_faces_df = pd.concat([known_faces_df, pd.DataFrame({'face_id': [len(known_faces_df) + 1], 'encoding': [face_encoding]})], ignore_index=True)

                    # Рисует белый квадрат на картинке по координатам
                    cv2.rectangle(
                        frame,
                        (left, top),
                        (right, bottom),
                        (255, 255, 255),
                        1
                    )

                    # Путь к директории с качественными изображениями
                    face_path = os.path.join(output_folder, f'faces/{camera_name}/{input_video.stem}_{frame_id}_{len(known_faces_df)}.jpg')

                    # Сохранение изображения лица на диск
                    cv2.imwrite(face_path, frame[top:bottom, left:right])

                    # Информируем консоль
                    print('\033[92m' + face_path + '\033[0m')

            # Сохраняем кадр с видео
            frame_path = os.path.join(output_folder, f'frames/{camera_name}/{input_video.stem}_{frame_id}.jpg')
            cv2.imwrite(frame_path, frame)

        else:
            break

    return known_faces_df


def find_common_faces(cam1_df, cam2_df, cam3_df):
    common_faces_cam1_cam2 = pd.merge(cam1_df, cam2_df, on='face_id', how='inner')
    common_faces_cam1_cam3 = pd.merge(cam1_df, cam3_df, on='face_id', how='inner')

    return common_faces_cam1_cam2, common_faces_cam1_cam3


if __name__ == "__main__":
    # Обрабатываем видео для каждой камеры
    df_cam1 = process_video(Path('datas/detection_video/input/cam_1.MOV'), 'datas/detection_video/output', df_cam1, 'cam_1')
    df_cam2 = process_video(Path('datas/detection_video/input/cam_2.MOV'), 'datas/detection_video/output', df_cam2, 'cam_2')
    df_cam3 = process_video(Path('datas/detection_video/input/cam_3.MOV'), 'datas/detection_video/output', df_cam3, 'cam_3')

    # Проводим сравнение лиц
    common_faces_cam1_cam2, common_faces_cam1_cam3 = find_common_faces(df_cam1, df_cam2, df_cam3)

    print("Common faces between cam_1 and cam_2:")
    print(common_faces_cam1_cam2)

    print("\nCommon faces between cam_1 and cam_3:")
    print(common_faces_cam1_cam3)

