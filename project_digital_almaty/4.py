import cv2
import face_recognition
import imutils
from pathlib import Path
import os
import pandas as pd
from mtcnn import MTCNN

# Загружаем MTCNN
detector = MTCNN()

df_cam1 = pd.DataFrame(columns=['face_id', 'encoding'])
df_cam2 = pd.DataFrame(columns=['face_id', 'encoding'])
df_cam3 = pd.DataFrame(columns=['face_id', 'encoding'])

def process_video_mtcnn(input_video, output_folder, known_faces_df, camera_name):
    # Загрузка видео
    capture = cv2.VideoCapture(str(input_video))

    frame_id = 0  # Инициализация счетчика кадров

    skip_frames = 5  # Пропускать 5 кадров перед обработкой следующего

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

            # Детекция лиц с использованием MTCNN
            results = detector.detect_faces(rgb_frame)

            # Работа с лицами
            for face_data in results:
                x, y, w, h = face_data['box']

                # Ограничивающий прямоугольник лица
                face = rgb_frame[y:y+h, x:x+w]

                # Преобразование координат в объект full_object_detection
                face_location = face_recognition.face_locations(face)
                face_location = [face_recognition_api.Facedetector._rect_to_css(face) for face in face_location]
                face_location = [face_recognition_api.Facedetector._css_to_rect(face) for face in face_location]

                # Получение кодировки лица с использованием face_recognition
                face_encoding = face_recognition.face_encodings(rgb_frame, face_location)

                # Проверяем, есть ли кодировка (некоторые лица могут не распознаваться)
                if face_encoding:
                    # Ищем лицо в списке известных лиц
                    matches = known_faces_df['encoding'].apply(lambda x: face_recognition.compare_faces([x], face_encoding[0]))

                    if not any(matches):
                        # Если лицо не найдено в списке известных лиц, добавляем его в датафрейм
                        known_faces_df = known_faces_df.append({'face_id': len(known_faces_df) + 1, 'encoding': face_encoding[0]}, ignore_index=True)

                        # Рисует белый квадрат на картинке по координатам
                        cv2.rectangle(
                            frame,
                            (x, y),
                            (x + w, y + h),
                            (255, 255, 255),
                            1
                        )

                        # Путь к директории с качественными изображениями
                        face_path = os.path.join(output_folder, f'faces/{camera_name}/{input_video.stem}_{frame_id}_{len(known_faces_df)}.jpg')

                        # Сохранение изображения лица на диск
                        cv2.imwrite(face_path, frame[y:y+h, x:x+w])

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
    # Создаем датафреймы для каждой камеры
    df_cam1 = pd.DataFrame(columns=['face_id', 'encoding'])
    df_cam2 = pd.DataFrame(columns=['face_id', 'encoding'])
    df_cam3 = pd.DataFrame(columns=['face_id', 'encoding'])

    # Обрабатываем видео для каждой камеры
    df_cam1 = process_video_mtcnn(Path('datas/detection_video/input/cam_1.MOV'), 'datas/detection_video/output', df_cam1, 'cam_1')
    df_cam2 = process_video_mtcnn(Path('datas/detection_video/input/cam_2.MOV'), 'datas/detection_video/output', df_cam2, 'cam_2')
    df_cam3 = process_video_mtcnn(Path('datas/detection_video/input/cam_3.MOV'), 'datas/detection_video/output', df_cam3, 'cam_3')

    # Находим общие лица между камерами
    common_faces_cam1_cam2, common_faces_cam1_cam3 = find_common_faces(df_cam1, df_cam2, df_cam3)

    print("Common faces between cam_1 and cam_2:")
    print(common_faces_cam1_cam2)

    print("\nCommon faces between cam_1 and cam_3:")
    print(common_faces_cam1_cam3)
