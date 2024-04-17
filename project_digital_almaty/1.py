import cv2
import dlib
import imutils
import numpy as np
from pathlib import Path
import os
import pandas as pd
import time

df_cam1 = pd.DataFrame(columns=['face_id', 'encoding'])
df_cam2 = pd.DataFrame(columns=['face_id', 'encoding'])
df_cam3 = pd.DataFrame(columns=['face_id', 'encoding'])

# Инициализация детектора лиц dlib
detector = dlib.get_frontal_face_detector()


def detect_faces(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    return faces


def process_video_with_tracking(input_video, output_folder, known_faces, camera_name):
    capture = cv2.VideoCapture(str(input_video))

    frame_id = 0
    skip_frames = 0
    last_detection_time = {}
    absence_threshold = 1  # установим порог в 1 секунду

    # Папка для сохранения данных о тех, кто сошел с маршрута
    output_folder_suspects = os.path.join(output_folder, 'suspects', camera_name)
    os.makedirs(output_folder_suspects, exist_ok=True)

    while True:
        frame_id += 1

        for _ in range(skip_frames):
            success, _ = capture.read()
            if not success:
                break

        success, frame = capture.read()

        if success:
            frame = imutils.resize(frame, width=800)

            # Обнаружение лиц на кадре
            faces = detect_faces(frame)

            # Проверяем, есть ли новые лица на кадре
            for face in faces:
                # Проходим только по лицам, которые не известны
                if not any(
                        np.array_equal(kf['face_location'], [face.left(), face.top(), face.right(), face.bottom()]) for
                        kf in known_faces):
                    # Здесь вы можете выполнить распознавание и добавление лица в список known_faces
                    face_id = f'{camera_name}_{frame_id}_{len(known_faces) + 1}'  # создаем новый face_id
                    known_faces.append({'face_location': [face.left(), face.top(), face.right(), face.bottom()],
                                        'face_id': face_id, 'last_detection_time': time.time()})

                    # Рисуем прямоугольник вокруг лица
                    x, y, right, bottom = known_faces[-1]['face_location']
                    cv2.rectangle(frame, (x, y), (right, bottom), (255, 255, 255), 1)

                    # Сохраняем фото лица в папку faces
                    face_path = os.path.join(output_folder,
                                             f'faces/{camera_name}/{input_video.stem}_{frame_id}_{face_id}.jpg')
                    cv2.imwrite(face_path, frame[y:bottom, x:right])

                    print('\033[92m' + face_path + '\033[0m')

            # Проверка на схождение с маршрута
            for known_face in known_faces:
                elapsed_time = time.time() - known_face['last_detection_time']
                if elapsed_time > absence_threshold:
                    print(f'\033[91m{known_face["face_id"]} сошел с маршрута\033[0m')

                    # Сохранение данных о том, кто сошел с маршрута в текстовый файл
                    face_id = known_face["face_id"]
                    suspect_data = f"Face ID: {face_id}\nTime of Last Detection: {elapsed_time:.2f} seconds\n"
                    suspect_file_path = os.path.join(output_folder_suspects,
                                                     f"suspect_{camera_name}_{input_video.stem}_{face_id}.txt")

                    with open(suspect_file_path, 'w') as suspect_file:
                        suspect_file.write(suspect_data)

                    print(f'\033[93mSaved suspect data to {suspect_file_path}\033[0m')

                    # Сохранение фото того, кто сошел с маршрута
                    x, y, right, bottom = known_face['face_location']
                    face_path = os.path.join(output_folder_suspects,
                                             f"suspect_{camera_name}_{input_video.stem}_{face_id}.jpg")
                    cv2.imwrite(face_path, frame[y:bottom, x:right])

                    print(f'\033[93mSaved suspect photo to {face_path}\033[0m')

                    # Удаляем известное лицо из списка, чтобы не выводить его на каждом кадре
                    known_faces.remove(known_face)

            frame_path = os.path.join(output_folder, f'frames/{camera_name}/{input_video.stem}_{frame_id}.jpg')
            cv2.imwrite(frame_path, frame)

        else:
            break


if __name__ == "__main__":
    output_folder = 'datas/detection_video/output'
    os.makedirs(os.path.join(output_folder, 'faces', 'cam_1'), exist_ok=True)
    os.makedirs(os.path.join(output_folder, 'frames', 'cam_1'), exist_ok=True)

    known_faces = []
    process_video_with_tracking(Path('datas/detection_video/input/cam_1.MOV'), output_folder, known_faces, 'cam_1')

    for input_video, camera_name in zip(
            [Path('datas/detection_video/input/cam_2.MOV'), Path('datas/detection_video/input/cam_3.MOV')],
            ['cam_2', 'cam_3']):
        known_faces = []
        process_video_with_tracking(input_video, output_folder, known_faces, camera_name)
