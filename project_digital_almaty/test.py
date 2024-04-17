import cv2
import numpy as np
import face_recognition
import imutils
from pathlib import Path
import os
import pandas as pd
import time

df_cam1 = pd.DataFrame(columns=['face_id', 'encoding'])
df_cam2 = pd.DataFrame(columns=['face_id', 'encoding'])
df_cam3 = pd.DataFrame(columns=['face_id', 'encoding'])


def process_video_with_tracking(input_video, output_folder, known_faces, camera_name):
    capture = cv2.VideoCapture(str(input_video))

    frame_id = 0
    skip_frames = 0
    last_detection_time = {}
    absence_threshold = 1  # установим порог в 0.5 секунды

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
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                top = max(0, top - 10)
                left = max(0, left - 10)
                bottom = min(frame.shape[0], bottom + 10)
                right = min(frame.shape[1], right + 10)

                # Проверяем, есть ли лицо в известных
                match_index = next((i for i, known_face in enumerate(known_faces) if
                                    face_recognition.compare_faces([known_face['encoding']], face_encoding)[0]), None)

                if match_index is not None:
                    # Лицо уже известно, обновляем время последнего обнаружения
                    known_faces[match_index]['last_detection_time'] = time.time()
                    face_id = known_faces[match_index]['face_id']
                else:
                    # Лицо не найдено в списке известных лиц, добавляем его
                    face_id = f'{camera_name}_{frame_id}_{len(known_faces) + 1}'  # создаем новый face_id
                    known_faces.append(
                        {'encoding': face_encoding, 'last_detection_time': time.time(), 'face_id': face_id})

                    cv2.rectangle(
                        frame,
                        (left, top),
                        (right, bottom),
                        (255, 255, 255),
                        1
                    )

                    face_path = os.path.join(output_folder,
                                             f'faces/{camera_name}/{input_video.stem}_{frame_id}_{face_id}.jpg')

                    cv2.imwrite(face_path, frame[top:bottom, left:right])

                    print('\033[92m' + face_path + '\033[0m')

            # Проверка на схождение с маршрута
            for known_face in known_faces:
                elapsed_time = time.time() - known_face['last_detection_time']
                print(f'{known_face} - Время с последнего обнаружения: {elapsed_time:.2f} секунд')
                if elapsed_time > absence_threshold:
                    print(f'\033[91m{known_face} сошел с маршрута\033[0m')

                    # Сохранение данных о том, кто сошел с маршрута в текстовый файл
                    face_id = f"{camera_name}_{frame_id}_{known_face['face_id']}"
                    suspect_data = f"Face ID: {face_id}\nTime of Last Detection: {elapsed_time:.2f} seconds\n"
                    suspect_file_path = os.path.join(output_folder_suspects, f"suspect_{camera_name}_{input_video.stem}_{known_face['face_id']}.txt")

                    with open(suspect_file_path, 'w') as suspect_file:
                        suspect_file.write(suspect_data)

                    print(f'\033[93mSaved suspect data to {suspect_file_path}\033[0m')

                    # Сохранение фото того, кто сошел с маршрута
                    suspect_photo_path = os.path.join(output_folder_suspects, f"suspect_{camera_name}_{input_video.stem}_{known_face['face_id']}.jpg")
                    cv2.imwrite(suspect_photo_path, frame[top:bottom, left:right])

                    print(f'\033[93mSaved suspect photo to {suspect_photo_path}\033[0m')

            frame_path = os.path.join(output_folder, f'frames/{camera_name}/{input_video.stem}_{frame_id}.jpg')
            cv2.imwrite(frame_path, frame)

        else:
            break


if __name__ == "__main__":
    output_folder = 'datas/detection_video/output'
    os.makedirs(os.path.join(output_folder, 'faces', 'cam_1'), exist_ok=True)
    os.makedirs(os.path.join(output_folder, 'frames', 'cam_1'), exist_ok=True)

    known_faces_cam1 = []
    process_video_with_tracking(Path('datas/detection_video/input/cam_1.MOV'), output_folder, known_faces_cam1, 'cam_1')

    os.makedirs(os.path.join(output_folder, 'faces', 'cam_2'), exist_ok=True)
    os.makedirs(os.path.join(output_folder, 'frames', 'cam_2'), exist_ok=True)

    known_faces_cam2 = []
    process_video_with_tracking(Path('datas/detection_video/input/cam_2.MOV'), output_folder, known_faces_cam2, 'cam_2')

    os.makedirs(os.path.join(output_folder, 'faces', 'cam_3'), exist_ok=True)
    os.makedirs(os.path.join(output_folder, 'frames', 'cam_3'), exist_ok=True)

    known_faces_cam3 = []
    process_video_with_tracking(Path('datas/detection_video/input/cam_3.MOV'), output_folder, known_faces_cam3, 'cam_3')
